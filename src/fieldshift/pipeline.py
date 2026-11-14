"""End-to-end pipeline: lat/lon + current rotation + priorities -> scored, explained rotations."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import pandas as pd

from . import features as F
from .config import end_year_for, field_at
from .crops import load_crops
from .fetch.appeears import load_ndvi, load_smap
from .fetch.base import FetchResult
from .fetch.power import fetch_power
from . import compare
from .rotations import ClimateClimatology, Rotation, generate_candidates
from .scoring import (DailyClimate, Weights, classify_by_demand, irrigation_demand_by_year,
                      planting_table, score_rotation, summarize)


NDVI_BARE_THRESHOLD = 0.2   # configurable: NDVI below this = bare soil
MIN_YEARS_ANOMALY = 4       # a calendar-month z-score needs several years of the same month


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
    ndvi: FetchResult | None = None
    smap: FetchResult | None = None
    ndvi_curve: pd.DataFrame | None = None
    ndvi_bare_windows: list = field(default_factory=list)
    observed_bare_days: float | None = None
    smap_anomaly: pd.DataFrame | None = None
    root_wetness: pd.DataFrame | None = None     # POWER GWETROOT summary, always available


@dataclass
class RotationResult:
    rotation: Rotation
    scores: pd.DataFrame
    summary: dict[str, dict[str, float]]
    tied: dict[str, bool] = field(default_factory=dict)


def build_context(lat: float, lon: float, start_year: int = 2001, end_year: int | None = None,
                  rain_factor: float = 1.0, temp_delta: float = 0.0) -> FieldContext:
    """Fetch (cached) POWER data, optionally perturb it for what-if runs, compute features."""
    end_year = end_year or end_year_for(lat, lon)
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
    fld = field_at(lat, lon)
    if fld is not None and not fld.satellite:      # regional presets: say so explicitly instead of searching files
        why = "no satellite NDVI/SMAP point has been requested for this preset field"
        ndvi, smap = FetchResult.failed("MODIS NDVI", why), FetchResult.failed("SMAP soil moisture", why)
    else:
        ndvi, smap = load_ndvi(lat, lon), load_smap(lat, lon)
    sources = [res]
    curve, wins, obs, sm_anom = None, [], None, None
    root_w = F.root_wetness_summary(daily)
    gaps = ["Soil: not used in the scores (shown for information only; see the Soil section for its status)."]
    def span_years(df: pd.DataFrame) -> float:
        return (df.index.max() - df.index.min()).days / 365.25

    if ndvi.ok:
        sources.append(ndvi)
        nd_years = span_years(ndvi.data)
        curve = F.ndvi_seasonal_curve(ndvi.data["ndvi"])
        wins = F.bare_windows_from_ndvi(curve, NDVI_BARE_THRESHOLD)
        ob = F.observed_bare_days_per_year(ndvi.data["ndvi"], NDVI_BARE_THRESHOLD)
        obs = float(ob.median()) if len(ob) else None
        gaps.append(f"Satellite NDVI ({ndvi.meta['n_valid']}/{ndvi.meta['n_total']} observations pass quality checks, "
                    f"{ndvi.date_range}) is shown and compared with the crop calendar; the scores still use the calendar."
                    + (f" It covers only {nd_years:.1f} years, so the seasonal curve is a rough picture, not a climatology." if nd_years < 5 else ""))
    else:
        gaps.append(f"Vegetation (MODIS NDVI) not loaded: bare periods come from crop calendars, not satellite. ({ndvi.message})")
    if smap.ok:
        sources.append(smap)
        sm_years = span_years(smap.data)
        if sm_years >= MIN_YEARS_ANOMALY:
            sm_anom = F.soil_moisture_anomaly(smap.data.rename(columns={"soil_moisture": "SMAP"}), "SMAP")
            gaps.append(f"SMAP soil moisture ({smap.date_range}) is shown for information; the scores do not use it.")
        else:
            gaps.append(f"SMAP soil moisture loaded ({smap.date_range}) but it covers only {sm_years:.1f} years: a wetter/drier-than-normal "
                        f"anomaly needs at least {MIN_YEARS_ANOMALY} years, so none is shown; NASA POWER root-zone wetness (GWETROOT, model-based, ~50 km) is shown instead.")
    else:
        gaps.append(f"SMAP soil moisture is not usable for this field ({smap.message}); NASA POWER root-zone wetness "
                    f"(GWETROOT, a model estimate on a ~50 km grid, not a satellite measurement) is shown instead.")
    gaps += [
        "Slope/erosion terrain (SRTM) not loaded: erosion score uses crop cover only.",
        "Irrigation water availability and soil salinity are unknown for this field.",
        "ET0 is computed from NASA POWER (MERRA-2) variables; it can differ from station-based ET0.",
        "Dry/normal/wet classes use irrigation demand (crop water need minus effective rain); actual "
        "water supply (rivers, snowmelt, canals) is not observed - use the irrigation-supply slider.",
        "Temperatures come from ~50 km reanalysis (MERRA-2) that runs hot over irrigated land, so hot-day counts and ET0 are likely overstated.",
        "Crop parameters are approximate regional values, not field trials.",
    ]
    if fld is not None:
        gaps.extend(fld.gap_notes)                 # field-specific notes (e.g. a common local crop that is not modelled)
    miss = {k: v for k, v in F.completeness(daily).items() if v > 0.01}
    if miss:
        gaps.append(f"POWER has gaps in: {', '.join(miss)}.")
    return FieldContext(lat, lon, elev, daily, ann, cls, clim, sources, gaps, ndvi, smap, curve, wins, obs, sm_anom, root_w)


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

    scored: dict[tuple, pd.DataFrame] = {}

    def score(rot: Rotation) -> pd.DataFrame:     # one scoring per rotation (memoised planting scores underneath)
        if rot.crops not in scored:
            scored[rot.crops] = score_rotation(rot, db, dc, weights, classes, irrigation_supply)
        return scored[rot.crops]

    def quick(rot: Rotation) -> float:  # used only to rank candidates within a rule family
        return float(score(rot)["total_abs"].median())

    rots = generate_candidates(current, db, ctx.clim, quick, n_alternatives, pinned, n_per_rule)
    out = [RotationResult(r, score(r), {}) for r in rots]
    compare.apply(out, weights)
    return out


def choose(pool: list[RotationResult], weights: Weights, n: int = 4,
           force: tuple[tuple[str, ...], ...] = ()) -> tuple[list[RotationResult], dict[str, bool]]:
    """Pick the rotations to display: current + the best candidate of each rule family (top n by fit).

    `pool` is every feasible candidate (current first). Scores are normalised first over the whole pool to
    choose, then again over the displayed options only (the fit is "compared among these options").
    Returns (display, tied-criteria flags). Works on copies, so the cached pool is never mutated.
    """
    from copy import copy
    pool = [RotationResult(r.rotation, r.scores.copy(), r.summary) for r in pool]
    compare.apply(pool, weights)
    best: dict[str, RotationResult] = {}
    for r in pool[1:]:
        if r.rotation.rule not in best or r.summary["fit"]["median"] > best[r.rotation.rule].summary["fit"]["median"]:
            best[r.rotation.rule] = r
    picks = sorted(best.values(), key=lambda r: -r.summary["fit"]["median"])[:n]
    for crops in force:
        hit = next((r for r in pool[1:] if r.rotation.crops == tuple(crops)), None)
        if hit and hit not in picks:
            picks = picks[:n - 1] + [hit]
    display = [pool[0], *picks]
    tied = compare.apply(display, weights)
    display[1:] = sorted(display[1:], key=lambda r: -r.summary["fit"]["median"])
    return display, tied
