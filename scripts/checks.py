"""Pre-Phase-3 checks: scoring balance, irrigation-supply scenarios, ET0 audit."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import warnings; warnings.filterwarnings("ignore")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.crops import kc_curve, load_crops  # noqa: E402
from fieldshift.pipeline import build_context, run  # noqa: E402
from fieldshift.rotations import schedule  # noqa: E402
from fieldshift.scoring import PRIORITIES, PROFILES, DailyClimate, Weights, score_planting  # noqa: E402

pd.set_option("display.width", 200)
SUB = [*PRIORITIES, "pest_break", "suitability"]
MUNG = ("winter_wheat", "mung_bean", "cotton")
DB = load_crops()


def short(r) -> str:
    return " > ".join(c.replace("winter_", "w.").replace("_cover", "") for c in r.rotation.crops)


def table(results) -> pd.DataFrame:
    rows = {short(r) + f" [{r.rotation.rule}]": {**{m: r.summary[m]["median"] for m in SUB},
            "FIT": r.summary["fit"]["median"], "irr_mm": r.summary["irrigation_mm_per_year"]["median"],
            "bare_d": r.rotation.bare_days_per_year()} for r in results}
    return pd.DataFrame(rows).T


def check1(key: str) -> None:
    f = DEMO_FIELDS[key]
    ctx = build_context(f.lat, f.lon)
    pinned = (MUNG,) if key == "fergana" else ()
    res = run(ctx, f.rotation, pinned=pinned)
    t = table(res)
    print(f"\n##### CHECK 1 [{f.name}] subscores (median over years, 0-100)")
    print(t.round(0).astype(int).to_string())
    print("\nChange vs current (points; irr/bare in raw units):")
    print((t - t.iloc[0]).iloc[1:].round(0).astype(int).to_string())
    # cover crops: income sign and own water need
    dc = DailyClimate(ctx.daily)
    print("\nCover-crop planting audit (median over years):")
    for r in res:
        for p in r.rotation.plantings:
            c = DB[p.crop_id]
            if c["season"] == "cover":
                rows = [score_planting(p, c, dc, dc.window(y, p.start, p.days)) for y in range(2003, 2020)]
                d = pd.DataFrame(rows).median()
                print(f"  {c['name']}: income index {c['income']:+.2f}; days {p.days}; ETc {d.etc_mm:.0f} mm, "
                      f"rain {d.rain_mm:.0f} mm, irrigation {d.irrigation_mm:.0f} mm; first 30 days Kc={kc_curve(c, p.days)[0]:.2f}")
    # weight profiles over ALL feasible candidates
    print(f"\nWeight profiles [{f.name}] (all feasible candidates):")
    winners = {}
    for name, w in PROFILES.items():
        allr = run(ctx, f.rotation, w, n_alternatives=500, n_per_rule=500, pinned=pinned)
        allr.sort(key=lambda r: -r.summary["fit"]["median"])
        winners[name] = short(allr[0]) + f" [{allr[0].rotation.rule}]"
        cur = next(r for r in allr if r.rotation.rule == "current")
        print(f"  {name:13s} n={len(allr)}  winner: {winners[name]} ({allr[0].summary["fit"]['median']:.0f}) "
              f"| runner-up: {short(allr[1])} ({allr[1].summary["fit"]['median']:.0f}) | current {cur.summary["fit"]['median']:.0f}")
    print("  => same winner under all three!" if len(set(winners.values())) == 1 else "  => winners differ across profiles")


def check2() -> None:
    f = DEMO_FIELDS["fergana"]
    ctx = build_context(f.lat, f.lon)
    print("\n##### CHECK 2 [Fergana] irrigation supply (fraction of design demand = P90 of each crop-season)")
    for s in (1.0, 0.8, 0.6):
        res = run(ctx, f.rotation, pinned=(MUNG,), irrigation_supply=s)
        print(f"\n-- supply {s:.1f}")
        print(f"{'rotation':46s} {'score':>5s} {'p10-p90':>8s} {'dry/norm/wet':>13s} {'irr mm':>6s} {'water yield-at-risk med/p90':>18s}")
        for r in res:
            t, yl = r.summary["fit"], r.summary["yield_loss"]
            print(f"{short(r)[:45]:46s} {t['median']:5.0f} {t['p10']:3.0f}-{t['p90']:<4.0f} "
                  f"{t['median_dry']:4.0f}/{t['median_normal']:3.0f}/{t['median_wet']:3.0f} "
                  f"{r.summary['irrigation_mm_per_year']['median']:6.0f} {yl['median']*100:8.0f}%/{yl['p90']*100:.0f}%")


def check3() -> None:
    f = DEMO_FIELDS["fergana"]
    ctx = build_context(f.lat, f.lon)
    d = ctx.daily
    print("\n##### CHECK 3 ET0 audit (after eq.19 fix)")
    print(f"elevation used {ctx.elevation_m:.0f} m (MERRA-2 grid-cell value)")
    m = d.groupby([d.index.year, d.index.month])["ET0"].sum().groupby(level=1).mean()
    print("Monthly ET0 (mm):", m.round(0).astype(int).to_dict(), f"| annual {m.sum():.0f}")
    dc = DailyClimate(d)
    for cid in ("cotton", "winter_wheat"):
        p = schedule(("winter_wheat", "cotton"), DB).plantings[[p.crop_id for p in schedule(("winter_wheat", "cotton"), DB).plantings].index(cid)]
        rows = pd.DataFrame([score_planting(p, DB[cid], dc, dc.window(y, p.start, p.days)) for y in range(2001, 2024)])
        print(f"{cid}: season day {p.start % 365}-{p.end % 365}, ETc median {rows.etc_mm.median():.0f} mm "
              f"(p10-p90 {rows.etc_mm.quantile(.1):.0f}-{rows.etc_mm.quantile(.9):.0f}), rain {rows.rain_mm.median():.0f}, "
              f"irrigation {rows.irrigation_mm.median():.0f}; seasonal ET0 {np.mean([dc.et0[dc.window(y,p.start,p.days)].sum() for y in range(2001,2024)]):.0f}")


if __name__ == "__main__":
    for k in ("fergana", "kansas"):
        check1(k)
    check2()
    check3()
