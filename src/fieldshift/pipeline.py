"""End-to-end pipeline: lat/lon + current rotation + priorities -> scored, explained rotations."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import pandas as pd

from . import features as F
from .crops import load_crops
from .fetch.base import FetchResult
from .fetch.power import fetch_power
from .rotations import ClimateClimatology, Rotation, generate_candidates
from .scoring import (DailyClimate, Weights, classify_by_demand, irrigation_demand_by_year,
                      planting_table, score_rotation, summarize)


@dataclass
class FieldContext:
    lat: float
    lon: float
    elevation_m: float
    daily: pd.DataFrame
    annual: pd.DataFrame            # incl. year_class
    year_classes: pd.Series
    clim: ClimateClimatology
    sources: list[FetchResult]
    gaps: list[str] = field(default_factory=list)


@dataclass
class RotationResult:
    rotation: Rotation
    scores: pd.DataFrame
    summary: dict[str, dict[str, float]]


def build_context(lat: float, lon: float, start_year: int = 2001, end_year: int | None = None,
                  rain_factor: float = 1.0, temp_delta: float = 0.0) -> FieldContext:
    """Fetch (cached) POWER data, optionally perturb it for what-if runs, compute features."""
    end_year = end_year or dt.date.today().year - 1
    res = fetch_power(lat, lon, start_year, end_year)
    if not res.ok:
        raise RuntimeError(f"NASA POWER is required but failed: {res.message}")
    daily = res.data.copy()
    if rain_factor != 1.0:
        daily["PRECTOTCORR"] *= rain_factor
    if temp_delta:
        daily[["T2M", "T2M_MAX", "T2M_MIN"]] += temp_delta
    elev = float(res.meta.get("elevation_m") or 0.0)
    daily = F.add_et0(daily, lat, elev)
    ann = F.annual_features(daily, lat)
    cls = F.classify_years(ann)
    ann["year_class"] = cls
    clim = ClimateClimatology.from_daily(daily, F.frost_table(daily, lat))
    gaps = [
        "Soil: SoilGrids not loaded yet (no texture/organic carbon/pH in the scores).",
        "Vegetation (MODIS NDVI) not loaded: bare periods come from crop calendars, not satellite.",
        "SMAP soil moisture not loaded: root-zone wetness from NASA POWER (model, ~50 km) is used instead.",
        "Slope/erosion terrain (SRTM) not loaded: erosion score uses crop cover only.",
        "Irrigation water availability and soil salinity are unknown for this field.",
        "ET0 is computed from NASA POWER (MERRA-2) variables; it can differ from station-based ET0.",
        "Dry/normal/wet classes use irrigation demand (crop water need minus effective rain); actual "
        "water supply (rivers, snowmelt, canals) is not observed - use the irrigation-supply slider.",
        "Reanalysis (MERRA-2) over irrigated land tends to run hot and dry (it does not see irrigation), "
        "which can overstate ET0 and heat days.",
        "Crop parameters are approximate regional values, not field trials.",
    ]
    miss = {k: v for k, v in F.completeness(daily).items() if v > 0.01}
    if miss:
        gaps.append(f"POWER has gaps in: {', '.join(miss)}.")
    return FieldContext(lat, lon, elev, daily, ann, cls, clim, [res], gaps)


def run(ctx: FieldContext, current: tuple[str, ...], weights: Weights | None = None,
        n_alternatives: int = 4, irrigation_supply: float = 1.0,
        pinned: tuple[tuple[str, ...], ...] = (), n_per_rule: int = 1) -> list[RotationResult]:
    """Generate candidate rotations (current first) and score every one.

    Year classes are terciles of the *current* rotation's irrigation demand, shared by all
    candidates so dry/normal/wet columns are comparable.
    """
    weights = weights or Weights()
    db = load_crops()
    dc = DailyClimate(ctx.daily)
    from .rotations import schedule
    cur = schedule(current, db)
    demand = irrigation_demand_by_year(cur, planting_table(cur, db, dc))
    classes = classify_by_demand(demand)

    def quick(rot: Rotation) -> float:  # used only to rank candidates within a rule family
        return float(score_rotation(rot, db, dc, weights, classes, irrigation_supply)["total"].median())

    rots = generate_candidates(current, db, ctx.clim, quick, n_alternatives, pinned, n_per_rule)
    return [RotationResult(r, sc, summarize(sc)) for r in rots
            for sc in [score_rotation(r, db, dc, weights, classes, irrigation_supply)]]
