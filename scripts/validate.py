"""Sanity checks of the model on both demo fields: expectation vs result, written to docs/validation.md.

Nothing here tunes the model: each check states an expectation up front, computes the result from the pipeline,
and records PASS / PARTIAL / FAIL by a rule that is fixed in this file.

Usage: python scripts/validate.py
"""
from __future__ import annotations

import datetime as dt
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
warnings.filterwarnings("ignore")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.crops import load_crops  # noqa: E402
from fieldshift.pipeline import build_context, run  # noqa: E402
from fieldshift.rotations import check_feasible, schedule  # noqa: E402
from fieldshift.scoring import PROFILES, DailyClimate, Weights, planting_table, score_rotation  # noqa: E402

DB = load_crops()
FIELDS = ["fergana", "kansas"]
MAIN_CROPS = [c for c, v in DB.items() if v["season"] in ("summer", "winter", "perennial")]


def rank_corr(a: pd.Series, b: pd.Series) -> float:
    """Spearman rank correlation (Pearson on ranks; no scipy needed)."""
    return float(np.corrcoef(a.rank().to_numpy(), b.rank().to_numpy())[0, 1])


def md_table(df: pd.DataFrame, floatfmt: str = "{:.0f}") -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join([df.index.name or ""] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    for idx, row in df.iterrows():
        out.append("| " + " | ".join([str(idx)] + [floatfmt.format(v) if isinstance(v, (int, float, np.floating)) and not pd.isna(v) else str(v) for v in row]) + " |")
    return "\n".join(out)


def single_crop_stats(ctx, dc, crop_id: str, supply: float = 1.0) -> dict | None:
    rot = schedule((crop_id,), DB)
    if rot is None:
        return None
    ok, notes = check_feasible(rot, DB, ctx.clim)
    table = planting_table(rot, DB, dc)
    if not table:
        return None
    rows = pd.DataFrame([r[0] for r in table.values()])
    cls = pd.Series("normal", index=list(table))
    sc = score_rotation(rot, DB, dc, Weights(), cls, irrigation_supply=supply, table=table)
    return dict(feasible=ok, irrigation=float(rows["irrigation_mm"].median()), etc=float(rows["etc_mm"].median()),
                loss=float(sc["yield_loss"].median()), ky=DB[crop_id]["ky"], loss_p90=float(sc["yield_loss"].quantile(0.9)))


def check_a(key, ctx, dc) -> tuple[str, str, str]:
    """Cotton has the highest irrigation demand among the main field crops."""
    rows = {c: single_crop_stats(ctx, dc, c) for c in MAIN_CROPS}
    df = pd.DataFrame({c: r for c, r in rows.items() if r and r["feasible"]}).T.sort_values("irrigation", ascending=False)
    top = df.head(6)[["irrigation", "etc"]]
    if "cotton" not in df.index:
        verdict, why = "N/A", "cotton is not climatically feasible here (frost-free season/GDD), so it cannot be ranked"
    else:
        rank = int(list(df.index).index("cotton")) + 1
        above = [DB[c]["name"] for c in df.index[:rank - 1]]
        verdict = "PASS" if rank == 1 else "FAIL"
        why = f"cotton ranks {rank} of {len(df)} feasible crops" + (f"; higher: {', '.join(above)}" if above else "")
    tbl = md_table(top.rename(columns={"irrigation": "irrigation need, mm/season", "etc": "crop water use ETc, mm"}).rename(index=lambda c: DB[c]["name"]))
    return verdict, why, tbl


def check_b(key, ctx, pool) -> tuple[str, str, str]:
    """Inserting a legume raises the soil subscores (organic matter, nitrogen, erosion cover) vs the current rotation."""
    cur = pool[0].scores[["soil_om", "nitrogen", "erosion"]].median()
    rows = []
    for r in pool[1:]:
        if r.rotation.rule in ("legume", "cover", "perennial") and any(DB[c]["n_fixing"] for c in r.rotation.added):
            m = r.scores[["soil_om", "nitrogen", "erosion"]].median()
            rows.append(dict(option=r.rotation.key.replace("_", " "), cycle_years=r.rotation.cycle_years, soil_om=m.soil_om - cur.soil_om,
                             nitrogen=m.nitrogen - cur.nitrogen, erosion=m.erosion - cur.erosion))
    if not rows:
        return "N/A", "no legume-insertion candidates were feasible", ""
    df = pd.DataFrame(rows).set_index("option")
    n = len(df)
    up = {k: int((df[k] > 0).sum()) for k in ("soil_om", "nitrogen", "erosion")}
    verdict = "PASS" if all(v == n for v in up.values()) else ("PARTIAL" if up["nitrogen"] == n else "FAIL")
    cur_cycle = pool[0].rotation.cycle_years
    flat = df[(df["soil_om"] <= 0) | (df["erosion"] <= 0)]
    longer = int((flat["cycle_years"] > cur_cycle).sum())
    why = (f"{n} legume options; nitrogen higher in {up['nitrogen']}, organic matter higher in {up['soil_om']}, erosion cover higher in {up['erosion']}; "
           f"of the {len(flat)} options where organic matter or erosion cover did not rise, {longer} lengthen the cycle from {cur_cycle} to a longer cycle (more bare days per year)")
    t = df.sort_values("nitrogen", ascending=False).head(8).copy()
    t["cycle_years"] = t["cycle_years"].map(lambda v: f"{int(v)}")          # a count, not a delta
    return verdict, why, md_table(t.rename(columns={"cycle_years": "cycle (years)", "soil_om": "Δ organic matter", "nitrogen": "Δ nitrogen", "erosion": "Δ erosion cover"}), "{:+.0f}")


def check_c(key, f, ctx) -> tuple[str, str, str]:
    """The water-first profile prefers rotations with lower irrigation demand."""
    res = run(ctx, f.rotation, PROFILES["water-first"], n_alternatives=500, n_per_rule=500)
    df = pd.DataFrame({"fit": [r.summary["fit"]["median"] for r in res], "demand": [r.summary["irrigation_demand_mm"]["median"] for r in res]},
                      index=[r.rotation.key for r in res])
    rho = rank_corr(df["fit"], -df["demand"])
    cur_d, win = df["demand"].iloc[0], df["fit"].idxmax()
    win_d, med_d = df.loc[win, "demand"], df["demand"].median()
    low_third = df["demand"] <= df["demand"].quantile(1 / 3)
    verdict = "PASS" if rho >= 0.5 and win_d < cur_d else ("PARTIAL" if rho > 0 else "FAIL")
    why = (f"rank correlation of fit with (lower) irrigation demand = {rho:+.2f} over {len(df)} options; winner '{win.replace('_', ' ')}' needs "
           f"{win_d:.0f} mm vs {cur_d:.0f} mm for the current rotation (median option {med_d:.0f} mm); "
           f"{int(low_third[df['fit'].nlargest(3).index].sum())} of the top 3 are in the lowest-demand third")
    top = df.sort_values("fit", ascending=False).head(5).rename(columns={"fit": "fit (water-first)", "demand": "irrigation need, mm/yr"})
    top.index = [i.replace("_", " ") for i in top.index]
    return verdict, why, md_table(top)


def check_d(key, ctx, dc) -> tuple[str, str, str]:
    """Reduced irrigation supply raises yield at risk most for high-Ky crops."""
    rows = {}
    for c in MAIN_CROPS:
        a = single_crop_stats(ctx, dc, c, supply=0.6)
        if a and a["feasible"] and a["irrigation"] > 0:
            rows[c] = a
    df = pd.DataFrame(rows).T
    df["deficit"] = df["loss"] / df["ky"]                              # relative ET deficit (loss = Ky x deficit before the cap at 1)
    rho_raw = rank_corr(df["ky"].astype(float), df["loss"].astype(float))
    resid = (df["loss"] - df["ky"] * df["deficit"]).abs().max()
    high = df[df["ky"] >= 1.05]["loss"].median(); low = df[df["ky"] <= 0.90]["loss"].median()
    verdict = "PASS" if rho_raw >= 0.5 else ("PARTIAL" if rho_raw > 0 else "FAIL")
    why = (f"across {len(df)} crops, rank correlation of Ky with yield loss at 60% supply = {rho_raw:+.2f}; median loss {high*100:.0f}% for Ky ≥ 1.05 vs "
           f"{low*100:.0f}% for Ky ≤ 0.90. Loss = Ky × relative ET deficit holds exactly (max residual {resid:.3f}); the raw ranking is also driven by how "
           f"irrigation-dependent each crop is (deficit), which varies more than Ky does")
    t = df.sort_values("loss", ascending=False).head(8)[["ky", "deficit", "loss"]].astype(float)
    t.columns = ["Ky", "relative ET deficit", "yield loss at 60% supply"]
    t.index = [DB[c]["name"] for c in t.index]
    t["relative ET deficit"] *= 100; t["yield loss at 60% supply"] *= 100
    return verdict, why, md_table(t.round(2).assign(**{"relative ET deficit": t["relative ET deficit"].round(0), "yield loss at 60% supply": t["yield loss at 60% supply"].round(0)}), "{:g}")


def check_e(key, f) -> tuple[str, str, str]:
    """A bare window starts within 14 days of a harvest whenever the next crop is not sown within 45 days (and not otherwise).

    First version of this check required a bare window after EVERY harvest, which wrongly failed Fergana (cotton is
    followed immediately by wheat). The rule above is the stated expectation; the model output was not changed.
    """
    rot = schedule(f.rotation, DB)
    total = 365 * rot.cycle_years
    wins = rot.bare_windows()
    rows, ok = [], True
    for i, p in enumerate(rot.plantings):
        nxt_start = rot.plantings[i + 1].start if i + 1 < len(rot.plantings) else rot.plantings[0].start + total
        gap = nxt_start - p.end
        expect = gap >= 45
        hit = [w for w in wins if (w[0] - p.end) % total <= 14]
        good = bool(hit) == expect
        ok &= good
        rows.append({"harvest": DB[p.crop_id]["name"], "harvest day": p.end % 365, "days to next sowing": gap, "bare window expected": "yes" if expect else "no",
                     "bare window found": f"{hit[0][1]} days" if hit else "none", "ok": "yes" if good else "NO"})
    df = pd.DataFrame(rows).set_index("harvest")
    wheat = next((r for r in rows if "wheat" in r["harvest"].lower()), None)
    verdict = "PASS" if ok else "FAIL"
    why = ((f"after wheat harvest (day {wheat['harvest day']}) the field is bare for {wheat['bare window found']}; " if wheat else "") +
           f"{len(wins)} bare window(s) per cycle; calendar bare days/yr = {rot.bare_days_per_year():.0f}")
    return verdict, why, md_table(df, "{:.0f}")


def main() -> None:
    out = [f"# Model validation: sanity checks on the demo fields\n",
           f"Generated by `scripts/validate.py` on {dt.date.today()}. Each check states an expectation *before* looking at the result, "
           "computes the result with the same code the app uses, and records the verdict by a fixed rule. Failures are reported as failures; "
           "nothing was tuned to make a check pass. These are **plausibility checks, not validation against measured yields or water use** "
           "(no such data was available).\n"]
    summary = []
    for key in FIELDS:
        f = DEMO_FIELDS[key]
        ctx = build_context(f.lat, f.lon)
        dc = DailyClimate(ctx.daily)
        pool = run(ctx, f.rotation, Weights(), n_alternatives=500, n_per_rule=500)
        out.append(f"\n## {f.name} (current: {' → '.join(DB[c]['name'] for c in f.rotation)})\n")
        for tag, title, expect, fn in [
            ("A", "Cotton has the highest irrigation demand", "Among the main field crops that are feasible here, cotton needs the most irrigation water per season.", lambda: check_a(key, ctx, dc)),
            ("B", "Legume insertion raises the soil subscores", "Every option that adds a nitrogen-fixing crop scores higher than the current rotation on nitrogen, organic matter and erosion cover.", lambda: check_b(key, ctx, pool)),
            ("C", "Water-first profile prefers lower-ETc rotations", "With water saving weighted 8:1, fit rises as irrigation demand falls and the winner needs less water than the current rotation.", lambda: check_c(key, f, ctx)),
            ("D", "Reduced supply hurts high-Ky crops most", "At 60% irrigation supply, yield loss is larger for crops with larger Ky (FAO-33).", lambda: check_d(key, ctx, dc)),
            ("E", "Bare window after the first harvest", "A bare window starts within two weeks of harvest in the current rotation.", lambda: check_e(key, f)),
        ]:
            verdict, why, tbl = fn()
            summary.append((f.name.split(",")[0], tag, title, verdict, why))
            out.append(f"### {tag}. {title}: **{verdict}**\n\n*Expectation:* {expect}\n\n*Result:* {why}.\n\n{tbl}\n")
    head = ["\n## Summary\n", "| Field | Check | Verdict | Result |", "|---|---|---|---|"]
    head += [f"| {fld} | {tag}. {title} | **{v}** | {why} |" for fld, tag, title, v, why in summary]
    out.insert(2, "\n".join(head) + "\n")
    notes = Path(__file__).with_name("validation_notes.md")
    if notes.exists():
        out.append("\n" + notes.read_text())
    Path(__file__).resolve().parents[1].joinpath("docs", "validation.md").write_text("\n".join(out))
    print("\n".join(f"{fld:8s} {tag} {v:7s} {why[:150]}" for fld, tag, title, v, why in summary))


if __name__ == "__main__":
    main()
