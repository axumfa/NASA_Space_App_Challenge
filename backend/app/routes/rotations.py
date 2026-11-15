"""Crop rotation generator, scoring, and explanation endpoints."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fastapi import APIRouter, HTTPException
import pandas as pd

from fieldshift import i18n, viz
from fieldshift.crops import load_crops
from fieldshift.explain import explain, is_arid, summary_box
from fieldshift.i18n import crop_name, tr
from fieldshift.pipeline import build_context, choose, run
from fieldshift.rotations import schedule
from fieldshift.scoring import PRIORITIES, DailyClimate, Weights, planting_table

from ..schemas import (
    EvaluateResponse,
    PlantingPeriod,
    RotationEvaluateRequest,
    RotationOption,
    VulnerabilityRow,
)

router = APIRouter(prefix="/api/rotations", tags=["rotations"])
DB = load_crops()


def cname(cid: str, lang: str = "en") -> str:
    return crop_name(cid, lang, DB[cid]["name"]) if cid in DB else cid


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_rotations(req: RotationEvaluateRequest):
    lat, lon = req.lat, req.lon
    current = tuple(c for c in req.current_crops if c and c in DB)
    if not current:
        raise HTTPException(status_code=400, detail="At least one valid crop must be selected.")
    if len(set(current)) != len(current):
        raise HTTPException(status_code=400, detail="Duplicate crops are not allowed in the rotation.")
    if schedule(current, DB) is None:
        raise HTTPException(status_code=400, detail="The selected crops overlap in the calendar.")

    try:
        ctx = build_context(
            lat,
            lon,
            rain_factor=1.0 + req.rain_pct / 100.0,
            temp_delta=req.temp_c,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build climate context: {e}")

    # Build weights from request
    weights_dict = {m: req.weights.get(m, 5.0) for m in PRIORITIES}
    w = Weights(**weights_dict)

    # Run pool and select top display candidates
    try:
        pool = run(
            ctx,
            current,
            Weights(),
            n_alternatives=500,
            n_per_rule=500,
            irrigation_supply=req.irrigation_supply,
        )
        force = (("winter_wheat", "mung_bean", "cotton"),) if current == ("winter_wheat", "cotton") else ()
        display, tied = choose(pool, w, n=4, force=force)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to score rotations: {e}")

    cur = display[0]
    ci = cur.summary
    cirr = ci["irrigation_demand_mm"]["median"]

    best_idx = 0
    fits = [r.summary["fit"]["median"] for r in display]
    if len({round(v) for v in fits}) > 1:
        best_idx = int(max(range(len(display)), key=lambda i: fits[i]))

    # Summary box in both English and Uzbek
    arid = is_arid(ctx)
    sb_en = summary_box(display, w, "en", arid=arid)
    sb_uz = summary_box(display, w, "uz", arid=arid)

    summary_box_data = {
        "title_en": sb_en["title"],
        "title_uz": sb_uz["title"],
        "best_en": sb_en["best"],
        "best_uz": sb_uz["best"],
        "reason_en": sb_en["reason"],
        "reason_uz": sb_uz["reason"],
        "tradeoff_en": sb_en["tradeoff"],
        "tradeoff_uz": sb_uz["tradeoff"],
        "check_en": sb_en["check"],
        "check_uz": sb_uz["check"],
        "caveat_en": sb_en["caveat"],
        "caveat_uz": sb_uz["caveat"],
    }

    # Format each option
    options: list[RotationOption] = []
    dc = DailyClimate(ctx.daily)

    for i, r in enumerate(display):
        s = r.summary
        rot = r.rotation
        e = explain(r, cur, ctx)
        fit = s["fit"]
        irr = s["irrigation_demand_mm"]["median"]
        irr_pct = round(100.0 * (irr - cirr) / cirr, 1) if (i > 0 and cirr > 0) else None

        # Rule descriptions
        rule_desc_en = ""
        rule_desc_uz = ""
        if i == 0:
            rule_desc_en = "Current rotation"
            rule_desc_uz = "Hozirgi almashlab ekish"
        else:
            added_en = cname(rot.added[0], "en") if rot.added else " → ".join(cname(c, "en") for c in rot.crops)
            added_uz = cname(rot.added[0], "uz") if rot.added else " → ".join(cname(c, "uz") for c in rot.crops)
            old_en = cname(rot.removed[0], "en") if rot.removed else ""
            old_uz = cname(rot.removed[0], "uz") if rot.removed else ""
            rule_desc_en = tr(f"rule.{rot.rule}", "en", crop=added_en, old=old_en)
            rule_desc_uz = tr(f"rule.{rot.rule}", "uz", crop=added_uz, old=old_uz)

        # Plantings
        plantings: list[PlantingPeriod] = []
        for pl in rot.plantings:
            start_doy = int(pl.start)
            duration = int(pl.days)
            end_doy = int((pl.start + pl.days - 1) % 365 + 1)
            plantings.append(
                PlantingPeriod(
                    crop_id=pl.crop_id,
                    crop_name_en=cname(pl.crop_id, "en"),
                    crop_name_uz=cname(pl.crop_id, "uz"),
                    start_doy=start_doy,
                    end_doy=end_doy,
                    start_date_en=viz.doy_to_date(start_doy, "en"),
                    start_date_uz=viz.doy_to_date(start_doy, "uz"),
                    end_date_en=viz.doy_to_date(end_doy, "en"),
                    end_date_uz=viz.doy_to_date(end_doy, "uz"),
                    duration_days=duration,
                )
            )

        # Vulnerability rows
        tbl = planting_table(rot, DB, dc)
        vuln_rows: list[VulnerabilityRow] = []
        for j, pl in enumerate(rot.plantings):
            vals = pd.DataFrame([rows_[j] for rows_ in tbl.values()]).median()
            vuln_rows.append(
                VulnerabilityRow(
                    crop_id=pl.crop_id,
                    crop_name_en=cname(pl.crop_id, "en"),
                    crop_name_uz=cname(pl.crop_id, "uz"),
                    frost_days=round(float(vals.frost_days), 0),
                    heat_days=round(float(vals.heat_days), 0),
                    heat_thr_c=float(DB[pl.crop_id]["heat_thr_c"]),
                    irrigation_mm=round(float(vals.irrigation_mm), 0),
                    suitability=round(float(vals.suitability), 0),
                )
            )

        # Heat stress lines
        heat_stress = []
        for j, pl in enumerate(rot.plantings):
            if DB[pl.crop_id]["season"] != "cover":
                heat_stress.append({
                    "crop_id": pl.crop_id,
                    "crop_name_en": cname(pl.crop_id, "en"),
                    "crop_name_uz": cname(pl.crop_id, "uz"),
                    "median_days": round(float(s[f"heat_days_{j}"]["median"]), 0),
                    "p90_days": round(float(s[f"heat_days_{j}"]["p90"]), 0),
                    "threshold_c": float(DB[pl.crop_id]["heat_thr_c"]),
                })

        # Radar scores
        radar_scores = {m: round(float(s[f"norm_{m}"]["median"]), 1) for m in PRIORITIES}

        # Explanations
        def render_bullets(items):
            return [{"en": i18n.render(it, "en"), "uz": i18n.render(it, "uz")} for it in items]

        tradeoffs = e.tradeoffs
        rendered_tradeoffs = [tr("ex.tradeoff", "en", t=i18n.render(x, "en")) for x in tradeoffs]
        rendered_tradeoffs_uz = [tr("ex.tradeoff", "uz", t=i18n.render(x, "uz")) for x in tradeoffs]

        explanations = {
            "why": render_bullets(e.why),
            "evidence": render_bullets(e.evidence),
            "benefits": render_bullets(e.benefits) + [{"en": en, "uz": uz} for en, uz in zip(rendered_tradeoffs, rendered_tradeoffs_uz)],
            "gaps": render_bullets(e.gaps),
            "risks": render_bullets(e.risks),
        }

        bare_windows = [{"start_doy": int(s_doy), "days": int(days)} for s_doy, days in rot.bare_windows()]

        options.append(
            RotationOption(
                index=i,
                is_current=(i == 0),
                is_best_fit=(i == best_idx),
                crops=list(rot.crops),
                crop_names_en=[cname(c, "en") for c in rot.crops],
                crop_names_uz=[cname(c, "uz") for c in rot.crops],
                rule=rot.rule,
                rule_desc_en=rule_desc_en,
                rule_desc_uz=rule_desc_uz,
                fit_score=round(float(fit["median"]), 1),
                fit_dry=round(float(fit["median_dry"]), 1),
                fit_normal=round(float(fit["median_normal"]), 1),
                fit_wet=round(float(fit["median_wet"]), 1),
                fit_p10=round(float(fit["p10"]), 1),
                fit_p90=round(float(fit["p90"]), 1),
                irrigation_demand_mm=round(float(irr), 1),
                irrigation_delta_pct=irr_pct,
                yield_loss_median_pct=round(float(s["yield_loss"]["median"]) * 100, 1),
                yield_loss_p90_pct=round(float(s["yield_loss"]["p90"]) * 100, 1),
                bare_days_per_year=round(float(rot.bare_days_per_year()), 0),
                nitrogen_kg_median=round(float(s["n_kg"]["median"]), 1),
                heat_stress=heat_stress,
                radar_scores=radar_scores,
                explanations=explanations,
                plantings=plantings,
                bare_windows=bare_windows,
                vuln_rows=vuln_rows,
            )
        )

    return EvaluateResponse(
        options=options,
        best_fit_index=best_idx,
        tied=tied,
        summary_box=summary_box_data,
    )
