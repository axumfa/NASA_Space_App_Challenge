"""Transparent scoring of rotations, per cycle start year, from climate features and crop traits.

Subscores are 0-100. Per planting we compute (from that year's daily weather):
  suitability  = 100 * temp_fit * (1 - 0.5*frost_pen) * (1 - 0.5*heat_pen) * gdd_sufficiency
  ETc          = sum(Kc_d * ET0_d);  effective rain = min(0.8 * P, ETc);  irrigation = ETc - eff. rain
Rotation-level (per year of the cycle):
  water_saving = 100 * (1 - irrigation_mm_per_year / 1200)
  nitrogen     = 100 * sum(n_credit) / years / 50
  soil_om      = 100 * sum(om * days) / (365 * years) / 0.6
  erosion      = 100 * sum(cover * days) / (365 * years) / 0.8
  forage       = 100 * sum(forage * yield_factor) / years / 0.6
  income       = 100 * sum(income * yield_factor) / years / 0.9      (yield_factor = suitability/100)
  pest_break   = 100 * (1 - share of cyclic neighbours from the same family)
Total = weighted mean of the six priority subscores x (0.6 + 0.4*suitability/100) x (0.85 + 0.15*pest_break/100).
"""
from __future__ import annotations

from dataclasses import dataclass, fields

import numpy as np
import pandas as pd

from .crops import Crop, kc_curve
from .features import gdd_daily
from .rotations import Planting, Rotation

PRIORITIES = ["water_saving", "soil_om", "nitrogen", "erosion", "forage", "income"]
REF_IRRIGATION_MM = 1200.0
GDD_CAP = 30.0


@dataclass
class Weights:
    water_saving: float = 1.0
    soil_om: float = 1.0
    nitrogen: float = 1.0
    erosion: float = 1.0
    forage: float = 1.0
    income: float = 1.0

    def as_dict(self) -> dict[str, float]:
        return {f.name: getattr(self, f.name) for f in fields(self)}


class DailyClimate:
    """Numpy view of the daily weather for fast window slicing."""

    def __init__(self, df: pd.DataFrame):
        self.start = df.index[0]
        self.n = len(df)
        self.tmin, self.tmax = df["T2M_MIN"].values, df["T2M_MAX"].values
        self.tmean, self.et0, self.p = df["T2M"].values, df["ET0"].values, df["PRECTOTCORR"].values
        self.first_year, self.last_year = df.index.year.min(), df.index.year.max()

    def window(self, year: int, start: int, days: int) -> slice | None:
        i0 = (pd.Timestamp(year=year, month=1, day=1) - self.start).days + start
        return slice(i0, i0 + days) if i0 >= 0 and i0 + days <= self.n else None


def _trapezoid(t: np.ndarray, tmin: float, lo: float, hi: float, tmax: float) -> np.ndarray:
    up = np.clip((t - tmin) / max(lo - tmin, 1e-6), 0, 1)
    down = np.clip((tmax - t) / max(tmax - hi, 1e-6), 0, 1)
    return np.minimum(up, down)


def score_planting(pl: Planting, crop: Crop, clim: DailyClimate, sl: slice) -> dict[str, float]:
    tmean, tmin, tmax = clim.tmean[sl], clim.tmin[sl], clim.tmax[sl]
    temp_fit = float(_trapezoid(tmean, crop["t_min"], *crop["t_opt"], crop["t_max"]).mean())
    frost_days = int((tmin <= crop["frost_kill_c"]).sum())
    heat_days = int((tmax >= crop["heat_thr_c"]).sum())
    frost_pen = min(1.0, frost_days / 3)
    heat_pen = min(1.0, (heat_days / pl.days) / 0.4)  # 40% of season days hot = full penalty
    gdd = float(gdd_daily(tmin, tmax, crop["gdd_base"], GDD_CAP).sum())
    gdd_suff = min(1.0, gdd / crop["gdd_req"]) if crop["gdd_req"] > 0 else 1.0
    suit = 100 * temp_fit * (1 - 0.5 * frost_pen) * (1 - 0.5 * heat_pen) * gdd_suff
    etc = float((np.array(kc_curve(crop, pl.days)) * clim.et0[sl]).sum())
    rain = float(clim.p[sl].sum())
    eff = min(0.8 * rain, etc)
    return dict(suitability=suit, temp_fit=temp_fit, frost_days=frost_days, heat_days=heat_days,
                gdd=gdd, etc_mm=etc, rain_mm=rain, eff_rain_mm=eff, irrigation_mm=etc - eff)


def static_subscores(rot: Rotation, db: dict[str, Crop]) -> dict[str, float]:
    """Subscores that depend only on crop traits and the calendar (not on yearly weather)."""
    k = rot.cycle_years
    pls = [(p, db[p.crop_id]) for p in rot.plantings]
    n = sum(c["n_credit"] for _, c in pls) / k
    om = sum(c["om"] * p.days for p, c in pls) / (365 * k)
    cover = sum(c["cover"] * p.days for p, c in pls) / (365 * k)
    fam = [c["family"] for _, c in pls]
    same = sum(fam[i] == fam[(i + 1) % len(fam)] for i in range(len(fam))) if len(fam) > 1 else 1
    pest = 100 * (1 - same / max(len(fam), 1))
    return dict(nitrogen=min(100, 100 * n / 50), soil_om=min(100, 100 * om / 0.6),
                erosion=min(100, 100 * cover / 0.8), pest_break=pest,
                bare_days=rot.bare_days_per_year())


def score_year(rot: Rotation, db: dict[str, Crop], clim: DailyClimate, year: int,
               weights: Weights, static: dict[str, float] | None = None) -> dict[str, float] | None:
    static = static or static_subscores(rot, db)
    k = rot.cycle_years
    per = []
    for p in rot.plantings:
        sl = clim.window(year, p.start, p.days)
        if sl is None:
            return None
        per.append((p, db[p.crop_id], score_planting(p, db[p.crop_id], clim, sl)))
    suit = float(np.mean([r["suitability"] for _, _, r in per]))
    irr = sum(r["irrigation_mm"] for _, _, r in per) / k
    forage = sum(c["forage"] * r["suitability"] / 100 for _, c, r in per) / k
    income = sum(c["income"] * r["suitability"] / 100 for _, c, r in per) / k
    sub = dict(water_saving=float(np.clip(100 * (1 - irr / REF_IRRIGATION_MM), 0, 100)),
               soil_om=static["soil_om"], nitrogen=static["nitrogen"], erosion=static["erosion"],
               forage=float(np.clip(100 * forage / 0.6, 0, 100)),
               income=float(np.clip(100 * income / 0.9, 0, 100)))
    w = weights.as_dict()
    prior = sum(w[m] * sub[m] for m in PRIORITIES) / max(sum(w.values()), 1e-9)
    total = prior * (0.6 + 0.4 * suit / 100) * (0.85 + 0.15 * static["pest_break"] / 100)
    return dict(year=year, total=total, suitability=suit, pest_break=static["pest_break"],
                irrigation_mm_per_year=irr, bare_days=static["bare_days"],
                heat_days=sum(r["heat_days"] for _, _, r in per) / k,
                frost_days=sum(r["frost_days"] for _, _, r in per) / k, **sub)


def score_rotation(rot: Rotation, db: dict[str, Crop], clim: DailyClimate, weights: Weights,
                   year_classes: pd.Series) -> pd.DataFrame:
    """One row per cycle start year with all subscores and the year's dry/normal/wet class."""
    static = static_subscores(rot, db)
    rows = [r for y in range(clim.first_year, clim.last_year + 1)
            if (r := score_year(rot, db, clim, y, weights, static)) is not None]
    df = pd.DataFrame(rows).set_index("year")
    df["year_class"] = year_classes.reindex(df.index)
    return df


def summarize(scores: pd.DataFrame, cols: list[str] | None = None) -> dict[str, dict[str, float]]:
    """Median and p10-p90 across all years and for each year class, per column."""
    cols = cols or ["total", *PRIORITIES, "suitability", "pest_break", "irrigation_mm_per_year",
                    "heat_days", "frost_days"]
    out: dict[str, dict[str, float]] = {}
    for c in cols:
        s = scores[c]
        d = {"median": s.median(), "p10": s.quantile(.1), "p90": s.quantile(.9)}
        for cls, g in scores.groupby("year_class"):
            d[f"median_{cls}"] = g[c].median()
        out[c] = d
    return out
