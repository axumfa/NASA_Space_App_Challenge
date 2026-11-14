"""Phase 1 CLI: fetch POWER for a demo field (or lat/lon) and print key features.

Usage: python scripts/field_report.py fergana | kansas | --lat 40.4 --lon 71.78
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402

from fieldshift import features as F  # noqa: E402
from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.fetch.power import fetch_power  # noqa: E402


def _ranges(weeks: list[int]) -> str:
    out, i = [], 0
    while i < len(weeks):
        j = i
        while j + 1 < len(weeks) and weeks[j + 1] == weeks[j] + 1:
            j += 1
        out.append(str(weeks[i]) if i == j else f"{weeks[i]}-{weeks[j]}")
        i = j + 1
    return ", ".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("field", nargs="?", choices=list(DEMO_FIELDS))
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    a = ap.parse_args()
    if a.field:
        f = DEMO_FIELDS[a.field]
        lat, lon, name = f.lat, f.lon, f.name
    else:
        lat, lon, name = a.lat, a.lon, f"({a.lat}, {a.lon})"
    end_year = dt.date.today().year - 1
    res = fetch_power(lat, lon, 2001, end_year)
    if not res.ok:
        sys.exit(f"POWER failed: {res.message}")
    elev = res.meta.get("elevation_m") or 0.0
    df = F.add_et0(res.data, lat, elev)
    ann = F.annual_features(df, lat)
    ann["class"] = F.classify_years(ann)
    pd.set_option("display.width", 160)

    print(f"\n=== {name} | lat {lat}, lon {lon}, elev {elev:.0f} m | POWER {res.date_range} ({res.message}) ===")
    print("Missing fraction:", {k: v for k, v in F.completeness(df).items() if v > 0} or "none")
    print("\nMonthly climatology (mean over years):")
    print(F.monthly_climatology(df).round(1).to_string())
    print("\nAnnual headline numbers (median over years):")
    print(ann.drop(columns="class").median().round(1).to_string())
    for col, label in [("t_mean", "Mean temp"), ("precip", "Precipitation")]:
        t = F.theil_sen_trend(ann[col])
        print(f"{label} trend: {t.slope_per_decade:+.2f}/decade "
              f"(95% CI {t.ci_low:+.2f}..{t.ci_high:+.2f}, {'significant' if t.significant else 'not significant'})")
    wk = F.frost_probability_by_week(df)
    risky = [int(w) for w in wk[wk >= 0.5].index]
    print("\nFrost-risk weeks (>=50% of years have a Tmin<=0C day):", _ranges(risky) or "none")
    print("Heat-stress days (Tmax>=35C) by month, mean/yr:",
          (df["T2M_MAX"] >= 35).groupby(df.index.month).sum().div(len(ann)).round(1).to_dict())
    print("\nYear classes:", ann["class"].value_counts().to_dict())
    print("Water balance by class (mm):", ann.groupby("class")["water_balance"].median().round(0).to_dict())
    sm = F.soil_moisture_anomaly(df)
    print("Latest-year root-zone soil-moisture z by month:",
          sm.xs(ann.index.max(), level="year")["z"].round(2).to_dict())


if __name__ == "__main__":
    main()
