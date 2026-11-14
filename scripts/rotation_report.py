"""Phase 2 CLI: score and explain rotations for a demo field.

Usage: python scripts/rotation_report.py fergana|kansas [--rain -20] [--temp 2] [--w nitrogen=3 water_saving=2]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.explain import explain  # noqa: E402
from fieldshift.pipeline import build_context, run  # noqa: E402
from fieldshift.scoring import Weights  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("field", choices=list(DEMO_FIELDS))
    ap.add_argument("--rain", type=float, default=0, help="rainfall change in percent")
    ap.add_argument("--temp", type=float, default=0, help="temperature change in C")
    ap.add_argument("--w", nargs="*", default=[], help="priority weights, e.g. nitrogen=3")
    ap.add_argument("--full", action="store_true", help="print full explanations")
    a = ap.parse_args()
    f = DEMO_FIELDS[a.field]
    w = Weights(**{k: float(v) for k, v in (x.split("=") for x in a.w)})
    ctx = build_context(f.lat, f.lon, rain_factor=1 + a.rain / 100, temp_delta=a.temp)
    results = run(ctx, f.rotation, w)
    print(f"\n=== {f.name}: current {' → '.join(f.rotation)} | rain {a.rain:+.0f}% temp {a.temp:+.1f}C ===")
    print(f"{'rotation':58s} {'rule':13s} {'fit':>5s} {'p10-p90':>9s} {'dry/norm/wet':>14s} {'irr mm':>6s} {'bare d':>6s}")
    for r in results:
        t = r.summary["fit"]
        print(f"{r.rotation.key[:57]:58s} {r.rotation.rule:13s} {t['median']:5.0f} {t['p10']:4.0f}-{t['p90']:<4.0f} "
              f"{t['median_dry']:4.0f}/{t['median_normal']:3.0f}/{t['median_wet']:3.0f}   "
              f"{r.summary['irrigation_demand_mm']['median']:6.0f} {r.rotation.bare_days_per_year():6.0f}")
    for r in (results if a.full else results[:2]):
        e = explain(r, results[0], ctx)
        print(f"\n--- {e.title} ---")
        for name in ("why", "evidence", "benefits", "tradeoffs", "gaps", "risks"):
            items = getattr(e, name)
            if items:
                print(f"{name.upper()}:")
                for i in items:
                    print("  -", i)


if __name__ == "__main__":
    main()
