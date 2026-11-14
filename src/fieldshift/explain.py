"""Structured, templated explanations. Every number comes from features/scores/crop data.

(An optional LLM may later rephrase these strings, never add numbers.)
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .crops import load_crops
from .pipeline import FieldContext, RotationResult
from .compare import FIT_LABEL
from .scoring import PRIORITIES

LABEL = {"water_saving": "Water saving", "soil_om": "Soil organic matter", "nitrogen": "Nitrogen fixing",
         "erosion": "Erosion reduction", "forage": "Forage value", "income": "Market/income"}


@dataclass
class Explanation:
    title: str
    why: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


def _names(crops: tuple[str, ...]) -> str:
    db = load_crops()
    return " → ".join(db[c]["name"] for c in crops)


def explain(res: RotationResult, current: RotationResult, ctx: FieldContext) -> Explanation:
    db = load_crops()
    r, cur = res.rotation, current.rotation
    s, cs = res.summary, current.summary
    ann = ctx.annual
    e = Explanation(title=_names(r.crops) + ("  (your current rotation)" if r.rule == "current" else ""))

    bare_now, bare_new = cur.bare_days_per_year(), r.bare_days_per_year()
    frost_med, heat_med = ann["frost_days"].median(), ann["heat_days"].median()
    first = ann["first_autumn_frost_doy"].median()
    last = ann["last_spring_frost_doy"].median()

    # ---- why
    if r.rule == "current":
        e.why.append("This is what you grow now. It is the baseline every other option is compared against.")
    elif r.rule == "legume":
        c = db[r.added[0]]
        e.why.append(f"{r.detail}: a nitrogen-fixing legume (about {c['n_credit']} kg N/ha credit for the next crop, approximate) "
                     f"that also breaks the pest and disease cycle.")
    elif r.rule == "cover":
        e.why.append(f"{r.detail}. Your current rotation leaves the field bare about {bare_now:.0f} days a year; "
                     f"this brings it to about {bare_new:.0f}.")
    elif r.rule == "swap_drought":
        d = s["irrigation_demand_mm"]["median"] - cs["irrigation_demand_mm"]["median"]
        eff = (f"Estimated irrigation need falls by {-d:.0f} mm/year." if d < -5 else
               f"Note: estimated irrigation need is NOT lower here ({d:+.0f} mm/year vs today), "
               f"because the cycle fits more crop-days per year; the benefit is a more drought-tolerant crop.")
        e.why.append(f"{r.detail}, aimed at water scarcity. {eff}")
    elif r.rule == "perennial":
        e.why.append(f"{r.detail}: a deep-rooted perennial legume that builds organic matter, fixes nitrogen and covers the soil.")
    elif r.rule == "winter_crop":
        e.why.append(f"{r.detail}: a winter crop that uses the cool, wetter months and changes the crop family sequence.")

    # ---- evidence (numbers)
    e.evidence.append(f"Calendar: field is bare about {bare_new:.0f} days/year in this rotation "
                      f"(current: {bare_now:.0f}); cycle length {r.cycle_years} year(s).")
    if r.rule == "current" and ctx.observed_bare_days is not None:
        e.evidence.append(f"Satellite check (MODIS NDVI below 0.2): about {ctx.observed_bare_days:.0f} bare days/year observed, "
                          f"against {bare_now:.0f} from the crop calendar.")
    e.evidence.append(f"Climate at the field ({ctx.annual.index.min()}–{ctx.annual.index.max()}, NASA POWER): "
                      f"median {frost_med:.0f} frost days/year (last spring frost ~day {last:.0f}, first autumn frost ~day {first:.0f}), "
                      f"{heat_med:.0f} days/year with Tmax ≥ 35 °C, rainfall {ann['precip'].median():.0f} mm vs reference ET0 {ann['et0'].median():.0f} mm.")
    t, ct = s["fit"], cs["fit"]
    e.evidence.append(f"{FIT_LABEL}: {t['median']:.0f} (typical range {t['p10']:.0f}–{t['p90']:.0f}); "
                      f"dry years {t['median_dry']:.0f}, normal {t['median_normal']:.0f}, wet {t['median_wet']:.0f}. "
                      f"Current rotation: {ct['median']:.0f}. This is a relative score among the options shown, not an absolute grade.")
    irr, cirr = s["irrigation_demand_mm"], cs["irrigation_demand_mm"]
    pct = 100 * (irr["median"] - cirr["median"]) / cirr["median"] if cirr["median"] else 0.0
    e.evidence.append(f"Estimated irrigation need: {irr['median']:.0f} mm/year" +
                      ("" if r.rule == "current" else f" ({pct:+.0f}% vs current {cirr['median']:.0f} mm)") +
                      f"; dry years {irr['median_dry']:.0f}, wet years {irr['median_wet']:.0f}.")
    if s["n_kg"]["median"] > 0:
        e.evidence.append(f"Nitrogen credit from legumes: about {s['n_kg']['median']:.0f} kg N/ha per year (approximate).")
    yl = s["yield_loss"]
    e.evidence.append(f"Yield at risk from water shortage (FAO yield-response): {yl['median']*100:.0f}% typical, "
                      f"{yl['p90']*100:.0f}% in the worst 1 year in 10 (irrigation supply set to the slider value).")
    for i, pl in enumerate(r.plantings):
        c = db[pl.crop_id]
        hd = s[f"heat_days_{i}"]
        if c["gdd_req"] > 0 or hd["median"] > 0:
            e.evidence.append(f"Heat exposure, {c['name']}: {hd['median']:.0f} days above {c['heat_thr_c']:.0f} °C in season "
                              f"(worst 1 in 10: {hd['p90']:.0f}); not converted to yield loss.")
    e.evidence.append(f"Climate fit {s['suitability']['median']:.0f}/100; pest-cycle break {s['pest_break']['median']:.0f}/100.")

    # ---- benefits / trade-offs vs current
    if r.rule != "current":
        for m in PRIORITIES:
            if res.tied.get(m):
                continue
            d = s[f"norm_{m}"]["median"] - cs[f"norm_{m}"]["median"]
            if d >= 10:
                e.benefits.append(f"{LABEL[m]}: better than your current rotation (relative score {s[f'norm_{m}']['median']:.0f} vs {cs[f'norm_{m}']['median']:.0f}).")
            elif d <= -10:
                e.tradeoffs.append(f"{LABEL[m]}: worse than your current rotation (relative score {s[f'norm_{m}']['median']:.0f} vs {cs[f'norm_{m}']['median']:.0f}).")
        if bare_new < bare_now - 5:
            e.benefits.append(f"Bare soil reduced from ~{bare_now:.0f} to ~{bare_new:.0f} days/year.")
        if not e.benefits:
            e.benefits.append("No priority improves by 5+ points over the current rotation with your weights.")
    else:
        e.benefits.append("Known to you; no new equipment, seed or market arrangements needed.")
        weak = [LABEL[m] for m in PRIORITIES if not res.tied.get(m) and s[f"norm_{m}"]["median"] < 30]
        if weak:
            e.tradeoffs.append("Lowest among the options on: " + ", ".join(weak) + ".")
    ties = [LABEL[m] for m, v in res.tied.items() if v]
    if ties:
        e.evidence.append("No real difference between these options for: " + ", ".join(ties) + " (treated as a tie).")

    # ---- gaps
    e.gaps.extend(ctx.gaps)
    approx = sorted({a for c in r.crops for a in db[c]["approx"]})
    e.gaps.append(f"Crop values marked approximate for: {', '.join(approx)}.")
    if r.feasibility_notes:
        e.gaps.extend(r.feasibility_notes)

    # ---- risks needing local expert review
    for cid in r.crops:
        c = db[cid]
        if c["salinity_tol"] < 0.5:
            e.risks.append(f"{c['name']} is salt-sensitive; check soil/irrigation-water salinity locally.")
        if cid not in cur.crops:
            e.risks.append(f"New crop {c['name']}: confirm seed availability, machinery, and local agronomy advice.")
        e.risks.append(f"Market ({c['name']}): {c['market_note']}")
    e.risks.append("Irrigation water supply and timing were not modelled; confirm with your water-user association.")
    return e


# ---------------------------------------------------------------- plain-language summary box
CRITERION_KEYS = {"water_saving": "water", "soil_om": "soil_om", "nitrogen": "nitrogen", "erosion": "erosion",
                  "forage": "forage", "income": "income"}


def _natural(res, m: str) -> float:
    """The number shown to the farmer for criterion m (mm, kg N, bare days, or a 0-100 index)."""
    s = res.summary
    return {"water_saving": s["irrigation_demand_mm"]["median"], "nitrogen": s["n_kg"]["median"],
            "erosion": res.rotation.bare_days_per_year()}.get(m, s[m]["median"])


def summary_box(display: list, weights, lang: str = "en", arid: bool = False) -> dict[str, str]:
    """Four plain sentences (best option, why, main trade-off, one check) built only from computed results.

    `display` is current first, then alternatives, already normalised by compare.apply (norm_* columns present).
    `arid` (annual rain / ET0 below 0.3, i.e. irrigated drylands where salt build-up is a real concern) switches on the salinity check.
    Returns {'best', 'reason', 'tradeoff', 'check', 'caveat', 'title'} plus 'facts' (the numbers used), for testing.
    """
    from .i18n import crop_name, tr
    db = load_crops()
    w = weights.normalized()

    def nm(c: str) -> str:
        return crop_name(c, lang, db[c]["name"])

    cur = display[0]
    best = max(display, key=lambda r: r.summary["fit"]["median"])
    facts: dict[str, float] = {}

    def norm(res, m: str) -> float:
        return res.summary[f"norm_{m}"]["median"]

    if best is cur:
        others = display[1:]
        runner = max(others, key=lambda r: r.summary["fit"]["median"]) if others else cur
        out_best = tr("sum.best_is_current", lang, fit=cur.summary["fit"]["median"], other=runner.summary["fit"]["median"])
        ref = runner
    else:
        crops = " → ".join(nm(c) for c in best.rotation.crops)
        out_best = tr("sum.best", lang, crops=crops, fit=best.summary["fit"]["median"], cur=cur.summary["fit"]["median"])
        ref = cur
    facts["fit_best"] = best.summary["fit"]["median"]

    # criteria ranked by weighted advantage of `best` over `ref` (ties excluded)
    gains = []
    for m in CRITERION_KEYS:
        if display[0].tied.get(m):
            continue
        gains.append((w[m] * (norm(best, m) - norm(ref, m)), m))
    gains.sort(reverse=True)
    reasons = []
    for g, m in gains[:2]:
        if g <= 0.5 or best is ref:
            continue
        new, old = _natural(best, m), _natural(ref, m)
        pct = 100 * (new - old) / old if old else 0.0
        reasons.append(tr(f"r.{CRITERION_KEYS[m]}", lang, new=new, old=old, pct=pct))
        facts[f"{m}_new"], facts[f"{m}_old"] = new, old
    if best is cur:       # the current rotation leads: explain by what it does better than the runner-up
        for g, m in sorted(((w[m] * (norm(cur, m) - norm(runner, m)), m) for m in CRITERION_KEYS if not cur.tied.get(m)), reverse=True)[:2]:
            if g > 0.5:
                new, old = _natural(cur, m), _natural(runner, m)
                reasons.append(tr(f"r.{CRITERION_KEYS[m]}", lang, new=new, old=old, pct=100 * (new - old) / old if old else 0.0))
                facts[f"{m}_new"], facts[f"{m}_old"] = new, old
    out_reason = tr("sum.reason", lang, reasons="; ".join(reasons)) if reasons else tr("sum.reason_none", lang)

    # main trade-off of `best` relative to `ref`: largest weighted loss, or a worse water-shortage tail
    losses = sorted(((w[m] * (norm(best, m) - norm(ref, m)), m) for m in CRITERION_KEYS if not best.tied.get(m)))
    tradeoff = None
    if best is not ref and losses and losses[0][0] < -0.5:
        m = losses[0][1]
        new, old = _natural(best, m), _natural(ref, m)
        tradeoff = tr(f"t.{CRITERION_KEYS[m]}", lang, new=new, old=old, pct=100 * (new - old) / old if old else 0.0)
        facts[f"trade_{m}_new"], facts[f"trade_{m}_old"] = new, old
    elif best is ref:     # current rotation is best: name its weakest weighted criterion against the strongest alternative
        weakest = sorted(((w[m] * (norm(cur, m) - norm(runner, m)), m) for m in CRITERION_KEYS if not cur.tied.get(m)))
        if weakest and weakest[0][0] < -0.5:
            m = weakest[0][1]
            new, old = _natural(cur, m), _natural(runner, m)
            tradeoff = tr(f"t.{CRITERION_KEYS[m]}", lang, new=new, old=old, pct=100 * (new - old) / old if old else 0.0)
            facts[f"trade_{m}_new"], facts[f"trade_{m}_old"] = new, old
    if tradeoff is None and best is not ref:
        a, b = best.summary["yield_loss"]["p90"] * 100, ref.summary["yield_loss"]["p90"] * 100
        if a - b >= 5:
            tradeoff = tr("t.shortage", lang, new=a, old=b)
            facts["shortage_new"], facts["shortage_old"] = a, b
    out_trade = tr("sum.tradeoff", lang, tradeoff=tradeoff) if tradeoff else tr("sum.tradeoff_none", lang)

    # one thing to check, in priority order: salinity, a new crop's seed/market, water availability, cycle length, dates
    new_crops = [c for c in best.rotation.crops if c not in cur.rotation.crops]
    salt = [c for c in new_crops if arid and db[c]["salinity_tol"] < 0.5]
    irr_new, irr_old = _natural(best, "water_saving"), _natural(cur, "water_saving")
    if salt:
        check = tr("c.salinity", lang, crop=nm(salt[0]))
    elif new_crops:
        check = tr("c.newcrop", lang, crop=nm(new_crops[0]))
    elif irr_new >= 1.1 * irr_old and best is not cur:
        check = tr("c.water", lang, irr=irr_new)
    elif best.rotation.cycle_years > 1 and best is not cur:
        check = tr("c.cycle", lang, years=best.rotation.cycle_years)
    else:
        check = tr("c.dates", lang)
    return {"title": tr("sum.title", lang), "best": out_best, "reason": out_reason, "tradeoff": out_trade,
            "check": tr("sum.check", lang, check=check), "caveat": tr("sum.caveat", lang), "facts": facts,
            "best_is_current": best is cur}


def is_arid(ctx) -> bool:
    """True where median annual rain is under 30% of reference ET0 (irrigation is essential, salts accumulate)."""
    return float((ctx.annual["precip"] / ctx.annual["et0"]).median()) < 0.3
