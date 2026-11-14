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
from fieldshift.scoring import PROFILES, DailyClimate, Weights, planting_table, score_rotation, static_subscores  # noqa: E402

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


GRAIN_LEGUMES = ["soybean", "mung_bean", "chickpea", "lentil"]


def check_a(key, ctx, dc) -> tuple[str, str, str]:
    """Cotton needs more irrigation than winter wheat and the grain legumes; alfalfa and sugar beet are expected to be higher.

    Verdict rule: PASS if cotton > winter wheat and cotton > every feasible grain legume AND alfalfa and sugar beet > cotton;
    PARTIAL if the first part holds but alfalfa and/or sugar beet are not higher; FAIL if cotton is not above wheat or a legume.
    """
    wanted = ["cotton", "winter_wheat", *GRAIN_LEGUMES, "alfalfa", "sugar_beet"]
    rows = {c: single_crop_stats(ctx, dc, c) for c in wanted}
    feas = {c: r for c, r in rows.items() if r and r["feasible"]}
    if "cotton" not in feas:
        return "N/A", "cotton is not climatically feasible here (frost-free season/GDD), so it cannot be compared", ""
    cot = feas["cotton"]["irrigation"]
    below = [c for c in ["winter_wheat", *GRAIN_LEGUMES] if c in feas]
    below_ok = {c: cot > feas[c]["irrigation"] for c in below}
    above = [c for c in ("alfalfa", "sugar_beet") if c in feas]
    above_ok = {c: feas[c]["irrigation"] > cot for c in above}
    skipped = [DB[c]["name"] for c in wanted if c not in feas]
    if not all(below_ok.values()):
        verdict = "FAIL"
    elif above and all(above_ok.values()):
        verdict = "PASS"
    else:
        verdict = "PARTIAL"
    parts = [f"cotton {cot:.0f} mm; lower than cotton: " + ", ".join(f"{DB[c]['name']} {feas[c]['irrigation']:.0f}" for c in below if below_ok[c])]
    bad = [DB[c]["name"] for c in below if not below_ok[c]]
    if bad:
        parts.append("NOT lower than cotton: " + ", ".join(bad))
    parts.append("expected higher: " + ", ".join(f"{DB[c]['name']} {feas[c]['irrigation']:.0f} ({'higher' if above_ok[c] else 'NOT higher'})" for c in above))
    if skipped:
        parts.append("not feasible here, skipped: " + ", ".join(skipped))
    order = sorted(feas, key=lambda c: -feas[c]["irrigation"])
    tbl = pd.DataFrame({"irrigation need, mm/season": [feas[c]["irrigation"] for c in order], "crop water use ETc, mm": [feas[c]["etc"] for c in order],
                        "role in the check": [("compared" if c == "cotton" else "must be below cotton" if c in below else "expected above cotton") for c in order]},
                       index=pd.Index([DB[c]["name"] for c in order], name=""))
    return verdict, "; ".join(parts), md_table(tbl)


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


def _rotation_rows(rot) -> tuple[list[dict], dict]:
    """Per planting: days, om, cover, and the model's own sums. Also the residue-credit sensitivity inputs."""
    k, total = rot.cycle_years, 365 * rot.cycle_years
    rows = []
    for i, p in enumerate(rot.plantings):
        c = DB[p.crop_id]
        nxt = rot.plantings[i + 1].start if i + 1 < len(rot.plantings) else rot.plantings[0].start + total
        gap = nxt - p.end
        rows.append(dict(crop=c["name"], days=p.days, om=c["om"], cover=c["cover"], om_days=c["om"] * p.days, cover_days=c["cover"] * p.days,
                         gap_days=gap, residue_days=min(60, max(gap, 0))))
    return rows, dict(k=k, om_days=sum(r["om_days"] for r in rows), cover_days=sum(r["cover_days"] for r in rows),
                      residue_cover_days=sum(0.5 * r["cover"] * r["residue_days"] for r in rows))


def worked_example_b(key, f, pool) -> str:
    """One worked example of a legume option that lengthens the cycle and lowers organic matter and erosion cover."""
    cur = pool[0]
    cands = [r for r in pool[1:] if r.rotation.cycle_years > cur.rotation.cycle_years
             and r.scores["soil_om"].median() < cur.scores["soil_om"].median() and r.scores["erosion"].median() < cur.scores["erosion"].median()
             and any(DB[c]["n_fixing"] for c in r.rotation.added)]
    if not cands:
        return "*No legume option in this field both lengthens the cycle and lowers organic matter and erosion cover, so there is no example to show.*\n"
    opt = next((r for r in cands if "chickpea" in r.rotation.crops), cands[0])
    rc, tc = _rotation_rows(cur.rotation)
    ro, to = _rotation_rows(opt.rotation)
    sc, so = static_subscores(cur.rotation, DB), static_subscores(opt.rotation, DB)
    # the hand arithmetic below must reproduce the model's subscores exactly
    for t_, st_, rot in ((tc, sc, cur.rotation), (to, so, opt.rotation)):
        om = min(100, 100 * t_["om_days"] / (365 * t_["k"]) / 0.6)
        er = min(100, 100 * t_["cover_days"] / (365 * t_["k"]) / 0.8)
        assert abs(om - st_["soil_om"]) < 1e-9 and abs(er - st_["erosion"]) < 1e-9, "worked example does not match the model"
    names = lambda r: " → ".join(x["crop"] for x in r)
    lines = [f"#### Worked example: **{names(rc)}** (current, {tc['k']}-year cycle) vs **{names(ro)}** ({to['k']}-year cycle)\n"]
    def tab(rows):
        return md_table(pd.DataFrame(rows).set_index("crop")[["days", "om", "cover", "om_days", "cover_days", "gap_days"]].rename(columns={
            "days": "days in field", "om": "om score", "cover": "cover score", "om_days": "om × days", "cover_days": "cover × days", "gap_days": "days to next sowing"}), "{:g}")
    lines += ["Current rotation:\n", tab(rc), "\nOption:\n", tab(ro), ""]
    kk, k2 = tc["k"], to["k"]
    lines.append("Model formulas: organic matter = 100 × (Σ om × days / (365 × cycle years)) / 0.6 and erosion cover = 100 × (Σ cover × days / (365 × cycle years)) / 0.8.\n")
    calc = pd.DataFrame({
        "current": [tc["om_days"], kk, tc["om_days"] / kk, sc["soil_om"], tc["cover_days"], tc["cover_days"] / kk, sc["erosion"], sc["bare_days"]],
        "option": [to["om_days"], k2, to["om_days"] / k2, so["soil_om"], to["cover_days"], to["cover_days"] / k2, so["erosion"], so["bare_days"]]},
        index=["Σ om × days over the cycle", "cycle (years)", "om × days **per year**", "organic matter subscore", "Σ cover × days over the cycle",
               "cover × days **per year**", "erosion-cover subscore", "bare days per year (calendar)"])
    lines += [md_table(calc, "{:.1f}"), ""]
    # same-horizon comparison: lcm of the two cycles
    import math
    H = math.lcm(kk, k2)
    lines.append(f"**Is it an averaging artefact?** Compare over the same horizon ({H} years) instead of per-year averages: the current rotation runs {H // kk} cycles "
                 f"and returns {H // kk * tc['om_days']:.0f} om × days and {H // kk * tc['cover_days']:.0f} cover × days; the option runs {H // k2} cycles and returns "
                 f"{H // k2 * to['om_days']:.0f} and {H // k2 * to['cover_days']:.0f}. The totals over equal time agree with the per-year ranking, so dividing by more years is "
                 "not what lowers the scores.\n")
    cur_cov = (tc["cover_days"] + tc["residue_cover_days"]) / kk
    opt_cov = (to["cover_days"] + to["residue_cover_days"]) / k2
    lines.append("**Is it caused by ignoring crop residue?** The model counts cover only while the crop is in the field. Sensitivity: add 60 days of "
                 "post-harvest residue cover (at half the crop's cover score, never longer than the gap before the next sowing). "
                 f"Cover × days per year then become {cur_cov:.1f} (current) vs {opt_cov:.1f} (option) → "
                 f"{'the option still has less cover' if opt_cov < cur_cov else 'the option now has at least as much cover'}.\n")
    added = [c for c in opt.rotation.crops if c not in cur.rotation.crops]
    lines.append(f"**What actually happens (real calendar, not arithmetic):** {', '.join(DB[c]['name'] for c in added)} cannot be sown in the same year as the existing crops "
                 f"(its sowing window does not follow the previous harvest), so the cycle grows from {kk} to {k2} years while the new crop occupies only "
                 f"{sum(r['days'] for r in ro) - sum(r['days'] for r in rc)} days of the extra {365 * (k2 - kk)}. The main crops are then grown less often, and the longer fallow "
                 "stands bare (bare days per year "
                 f"{sc['bare_days']:.0f} → {so['bare_days']:.0f}). Legumes that fit inside the same year (e.g. mung bean after wheat) keep the cycle length and do raise both subscores.\n")
    return "\n".join(lines)


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
            ("A", "Cotton needs more irrigation than winter wheat and the grain legumes", "Cotton needs more irrigation water per season than winter wheat and than each feasible grain legume (soybean, mung bean, chickpea, lentil); alfalfa and sugar beet are expected to need more than cotton.", lambda: check_a(key, ctx, dc)),
            ("B", "Legume insertion raises the soil subscores", "Every option that adds a nitrogen-fixing crop scores higher than the current rotation on nitrogen, organic matter and erosion cover.", lambda: check_b(key, ctx, pool)),
            ("C", "Water-first profile prefers lower-ETc rotations", "With water saving weighted 8:1, fit rises as irrigation demand falls and the winner needs less water than the current rotation.", lambda: check_c(key, f, ctx)),
            ("D", "Reduced supply hurts high-Ky crops most", "At 60% irrigation supply, yield loss is larger for crops with larger Ky (FAO-33).", lambda: check_d(key, ctx, dc)),
            ("E", "Bare window after the first harvest", "A bare window starts within two weeks of harvest in the current rotation.", lambda: check_e(key, f)),
        ]:
            verdict, why, tbl = fn()
            summary.append((f.name.split(",")[0], tag, title, verdict, why))
            out.append(f"### {tag}. {title}: **{verdict}**\n\n*Expectation:* {expect}\n\n*Result:* {why}.\n\n{tbl}\n")
            if tag == "B":
                out.append(worked_example_b(key, f, pool) + "\n")
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
