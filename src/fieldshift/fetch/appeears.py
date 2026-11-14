"""Parse manually downloaded AppEEARS point-sample CSVs (data/raw/) for MODIS NDVI and SMAP soil moisture.

Expected products (AppEEARS "point sample" CSV output):
  MOD13Q1.061  250 m 16-day NDVI, layers *_250m_16_days_NDVI and *_250m_16_days_pixel_reliability
  SPL3SMP_E.006 9 km daily soil moisture, layers ..._AM_soil_moisture(+_qual_flag) and ..._PM_soil_moisture_pm(+_qual_flag_pm)
Column names are matched by regular expression (they differ slightly between AppEEARS versions). If the
required columns are missing, a ValueError lists the columns found. A file may hold several points; the
row group nearest to the requested lat/lon (within MAX_DEG) is used.

QA applied before any value is used:
  NDVI  : pixel_reliability must be 0 (good) or 1 (marginal); 2 (snow/ice), 3 (cloudy), -1 (no data) rejected;
          fill -3000 rejected; scale factor 0.0001.
  SMAP  : retrieval_qual_flag bit 0 must be 0 (recommended quality); fill -9999 rejected; AM and PM averaged.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from ..config import RAW_DIR
from .base import FetchResult

MAX_DEG = 0.1
NDVI_SCALE = 0.0001
NDVI_FILL = -3000
SMAP_FILL = -9999
QUAL_FILL = 65534      # uint16 fill of retrieval_qual_flag (verified in the AppEEARS layer list)
NDVI_ACCEPT_RELIABILITY = (0, 1)


def _find_col(cols: list[str], pattern: str, required: bool = True) -> str | None:
    hit = [c for c in cols if re.search(pattern, c, re.I)]
    if hit:
        return hit[0]
    if required:
        raise ValueError(f"column matching /{pattern}/ not found; columns are: {cols}")
    return None


def _select_point(df: pd.DataFrame, lat: float, lon: float) -> pd.DataFrame:
    lat_c, lon_c = _find_col(list(df.columns), r"^latitude$"), _find_col(list(df.columns), r"^longitude$")
    d = np.hypot(df[lat_c] - lat, df[lon_c] - lon)
    if d.min() > MAX_DEG:
        raise ValueError(f"no point within {MAX_DEG} deg of ({lat}, {lon}); nearest is {d.min():.2f} deg away")
    best = df.loc[d.idxmin(), [lat_c, lon_c]]
    return df[(df[lat_c] == best[lat_c]) & (df[lon_c] == best[lon_c])]


def parse_ndvi(path: Path, lat: float, lon: float, accept: tuple[int, ...] = NDVI_ACCEPT_RELIABILITY) -> pd.DataFrame:
    """Return a frame indexed by date with `ndvi` (QA-filtered, NaN where rejected) and `ndvi_raw_ok`."""
    raw = pd.read_csv(path)
    df = _select_point(raw, lat, lon)
    cols = list(df.columns)
    nd = _find_col(cols, r"250m_16_days_NDVI$")
    rel = _find_col(cols, r"250m_16_days_pixel_reliability$")
    out = pd.DataFrame({"ndvi": df[nd].astype(float).values * NDVI_SCALE,
                        "reliability": df[rel].astype(float).values},
                       index=pd.to_datetime(df[_find_col(cols, r"^date$")]).values)
    ok = out["reliability"].isin(accept) & (df[nd].values != NDVI_FILL) & df[nd].between(-2000, 10000).values
    out.loc[~ok.values if hasattr(ok, "values") else ~ok, "ndvi"] = np.nan
    out.index.name = "date"
    return out.sort_index()


def parse_smap(path: Path, lat: float, lon: float) -> pd.DataFrame:
    """Return a frame indexed by date with `soil_moisture` (m3/m3, QA-filtered, AM/PM mean)."""
    raw = pd.read_csv(path)
    df = _select_point(raw, lat, lon)
    cols = list(df.columns)
    parts = []
    for sm_pat, q_pat in ((r"_AM_soil_moisture$", r"AM_retrieval_qual_flag$|retrieval_qual_flag$"),
                          (r"_PM_soil_moisture_pm$", r"PM_retrieval_qual_flag_pm$|retrieval_qual_flag_pm$")):
        sm = _find_col(cols, sm_pat, required=False)
        if sm is None:
            continue
        q = _find_col([c for c in cols if (c.lower().endswith("_pm") == sm.lower().endswith("_pm"))], q_pat)
        v = df[sm].astype(float)
        flag = df[q].astype(float).fillna(65535).astype(int)
        good = (v != SMAP_FILL) & (v > 0) & ((flag & 1) == 0) & (flag < QUAL_FILL)   # 65534 (fill) has bit 0 clear: reject explicitly
        parts.append(v.where(good))
    if not parts:
        raise ValueError(f"no AM/PM soil_moisture columns found; columns are: {cols}")
    out = pd.DataFrame({"soil_moisture": pd.concat(parts, axis=1).mean(axis=1).values},
                       index=pd.to_datetime(df[_find_col(cols, r"^date$")]).values)
    out.index.name = "date"
    return out.sort_index()


def _files(pattern: str) -> list[Path]:
    return sorted(Path(RAW_DIR).glob(f"*{pattern}*.csv")) if Path(RAW_DIR).exists() else []


def _load(source: str, patterns: list[str], parser, lat: float, lon: float, res: str) -> FetchResult:
    files = [f for p in patterns for f in _files(p)]
    if not files:
        return FetchResult.failed(source, f"no file matching {patterns} in data/raw/ (download from AppEEARS)")
    errors = []
    for f in files:
        try:
            df = parser(f, lat, lon)
            n_ok = int(df.iloc[:, 0].notna().sum())
            if n_ok == 0:
                raise ValueError("all observations rejected by QA")
            return FetchResult(source, df, True, res, f"{df.index.min():%Y-%m-%d} to {df.index.max():%Y-%m-%d}",
                               f"{f.name}: {n_ok}/{len(df)} observations pass QA",
                               {"file": f.name, "n_total": len(df), "n_valid": n_ok})
        except Exception as e:  # noqa: BLE001
            errors.append(f"{f.name}: {e}")
    return FetchResult.failed(source, "; ".join(errors)[:400])


def load_ndvi(lat: float, lon: float) -> FetchResult:
    return _load("MODIS NDVI (MOD13Q1.061, AppEEARS CSV)", ["MOD13Q1"], parse_ndvi, lat, lon, "250 m, 16-day")


def load_smap(lat: float, lon: float) -> FetchResult:
    return _load("SMAP soil moisture (SPL3SMP_E, AppEEARS CSV)", ["SPL3SMP"], parse_smap, lat, lon, "9 km, daily")
