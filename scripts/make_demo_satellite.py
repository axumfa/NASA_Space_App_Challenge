"""Trim the downloaded AppEEARS CSVs to the columns the parser reads and the demo points, for the committed demo cache.

Input : data/raw/fieldshift-points-2019-{MOD13Q1-061,SPL3SMP-E-006}-results.csv  (public NASA data, see scripts/appeears_fetch.py)
Output: data/demo_cache/demo-points-{MOD13Q1-061,SPL3SMP-E-006}-results.csv      (same format; read by fetch/appeears.py)
Values are copied unchanged; only columns and points are dropped. Run again after a new AppEEARS download.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fieldshift.config import DEMO_CACHE_DIR, DEMO_FIELDS, RAW_DIR  # noqa: E402

KEEP = {"MOD13Q1-061": (r"^(Latitude|Longitude|Date)$", r"250m_16_days_(NDVI|VI_Quality|pixel_reliability)$"),
        "SPL3SMP-E-006": (r"^(Latitude|Longitude|Date)$", r"(AM|PM)_(soil_moisture|retrieval_qual_flag)(_pm)?$")}
POINTS = [(f.lat, f.lon) for k, f in DEMO_FIELDS.items() if f.satellite]
TOL = 0.0005

for prod, pats in KEEP.items():
    src = Path(RAW_DIR) / f"fieldshift-points-2019-{prod}-results.csv"
    df = pd.read_csv(src)
    cols = [c for c in df.columns if any(__import__("re").search(p, c) for p in pats)]
    keep = pd.Series(False, index=df.index)
    for la, lo in POINTS:
        keep |= ((df["Latitude"] - la).abs() < TOL) & ((df["Longitude"] - lo).abs() < TOL)
    out = df.loc[keep, cols]
    dst = Path(DEMO_CACHE_DIR) / f"demo-points-{prod}-results.csv"
    out.to_csv(dst, index=False)
    print(f"{dst.name}: {len(out)} rows, {len(cols)} columns, {dst.stat().st_size / 1e6:.2f} MB; points {sorted(set(zip(out.Latitude.round(4), out.Longitude.round(4))))}")
