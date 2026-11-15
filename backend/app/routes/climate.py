"""Climate, field context, and soil endpoints."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fastapi import APIRouter, HTTPException
import pandas as pd

from fieldshift import features as F
from fieldshift import i18n
from fieldshift import viz
from fieldshift.config import DEMO_FIELDS, field_at
from fieldshift.fetch.soil import fetch_soil
from fieldshift.pipeline import build_context

from ..schemas import (
    AnnualKpis,
    ClimatologyPoint,
    ContextRequest,
    ContextResponse,
    DataSourceStatus,
    FrostWeekPoint,
    HeatMonthPoint,
    SatelliteData,
    SoilData,
)

router = APIRouter(prefix="/api", tags=["climate"])


@router.post("/context", response_model=ContextResponse)
def get_field_context(req: ContextRequest):
    lat, lon = req.lat, req.lon
    try:
        ctx = build_context(
            lat,
            lon,
            rain_factor=1.0 + req.rain_pct / 100.0,
            temp_delta=req.temp_c,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build field context: {e}")

    d, ann = ctx.daily, ctx.annual
    fld = field_at(lat, lon)
    field_key = fld.key if fld else None
    field_name = fld.name if fld else f"{abs(lat):.2f}° {'N' if lat >= 0 else 'S'}, {abs(lon):.2f}° {'E' if lon >= 0 else 'W'}"

    # KPIs
    rain_m = float(ann["precip"].median())
    et0_m = float(ann["et0"].median())
    gap = et0_m - rain_m
    t_t = F.theil_sen_trend(ann["t_mean"])
    p_t = F.theil_sen_trend(ann["precip"])
    free = ann["first_autumn_frost_doy"] - ann["last_spring_frost_doy"]

    kpis = AnnualKpis(
        rain_median=round(rain_m, 1),
        rain_p10=round(float(ann["precip"].quantile(0.1)), 1),
        rain_p90=round(float(ann["precip"].quantile(0.9)), 1),
        et0_median=round(et0_m, 1),
        gap_mm=round(gap, 1),
        is_deficit=gap > 0,
        temp_median=round(float(ann["t_mean"].median()), 1),
        temp_trend_slope=round(float(t_t.slope_per_decade), 2),
        temp_trend_significant=bool(t_t.significant),
        precip_trend_slope=round(float(p_t.slope_per_decade), 1),
        precip_trend_significant=bool(p_t.significant),
        last_spring_frost_median=viz.doy_to_date(ann["last_spring_frost_doy"].median(), "en"),
        last_spring_frost_p10=viz.doy_to_date(ann["last_spring_frost_doy"].quantile(0.1), "en"),
        last_spring_frost_p90=viz.doy_to_date(ann["last_spring_frost_doy"].quantile(0.9), "en"),
        first_autumn_frost_median=viz.doy_to_date(ann["first_autumn_frost_doy"].median(), "en"),
        first_autumn_frost_p10=viz.doy_to_date(ann["first_autumn_frost_doy"].quantile(0.1), "en"),
        first_autumn_frost_p90=viz.doy_to_date(ann["first_autumn_frost_doy"].quantile(0.9), "en"),
        frost_free_days_median=round(float(free.median()), 0),
        frost_free_days_p10=round(float(free.quantile(0.1)), 0),
        frost_free_days_p90=round(float(free.quantile(0.9)), 0),
        frost_days_median=round(float(ann["frost_days"].median()), 0),
        frost_days_p10=round(float(ann["frost_days"].quantile(0.1)), 0),
        frost_days_p90=round(float(ann["frost_days"].quantile(0.9)), 0),
        heat_days_median=round(float(ann["heat_days"].median()), 0),
        heat_days_p10=round(float(ann["heat_days"].quantile(0.1)), 0),
        heat_days_p90=round(float(ann["heat_days"].quantile(0.9)), 0),
    )

    # Monthly Climatology
    clim = F.monthly_climatology(d)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_pts = []
    for m in range(1, 13):
        row = clim.loc[m]
        monthly_pts.append(
            ClimatologyPoint(
                month=m,
                month_name=month_names[m - 1],
                rain_mm=round(float(row["PRECTOTCORR"]), 1),
                et0_mm=round(float(row["ET0"]), 1),
                t_mean=round(float(row["T2M"]), 1),
                t_max=round(float(row["T2M_MAX"]), 1),
                t_min=round(float(row["T2M_MIN"]), 1),
            )
        )

    # Frost probability by week
    wk = F.frost_probability_by_week(d)
    frost_pts = [FrostWeekPoint(week=int(w), frost_prob=round(float(p), 3)) for w, p in wk.items()]

    # Heat days by month
    heat = (d["T2M_MAX"] >= 35).groupby(d.index.month).sum() / ann.shape[0]
    heat_pts = [HeatMonthPoint(month=int(m), heat_days=round(float(v), 1)) for m, v in heat.items()]

    # Soil
    soil_res = fetch_soil(lat, lon, field_key)
    soil_recs = soil_res.data.to_dict("records") if soil_res.ok and hasattr(soil_res.data, "to_dict") else []
    soil_data = SoilData(
        ok=bool(soil_res.ok),
        source=str(soil_res.source),
        records=soil_recs,
        message=str(soil_res.message or ""),
    )

    # Satellite data
    nd_ok = ctx.ndvi is not None and ctx.ndvi.ok
    sm_ok = ctx.smap is not None and ctx.smap.ok
    sat_applicable = not (fld is not None and not fld.satellite)

    sources = [
        DataSourceStatus(
            name="NASA POWER",
            status="ok",
            label="NASA POWER (MERRA-2, CERES)",
            date_range=ctx.sources[0].date_range if ctx.sources else "2001–2025",
            tooltip="Daily solar radiation, precipitation, air temperature, relative humidity, wind speed",
        ),
        DataSourceStatus(
            name="MODIS NDVI",
            status="ok" if nd_ok else ("miss" if sat_applicable else "na"),
            label="MODIS NDVI (MOD13Q1)",
            date_range=ctx.ndvi.date_range if nd_ok and ctx.ndvi else "–",
            tooltip="250 m 16-day vegetation index for greenness and bare period estimation",
        ),
        DataSourceStatus(
            name="SMAP",
            status="ok" if sm_ok else ("miss" if sat_applicable else "na"),
            label="SMAP Soil Moisture",
            date_range=ctx.smap.date_range if sm_ok and ctx.smap else "–",
            tooltip="Surface soil moisture active/passive radiometer",
        ),
        DataSourceStatus(
            name="SoilGrids",
            status="ok" if soil_res.ok else "miss",
            label="ISRIC SoilGrids",
            date_range="Static 250 m",
            tooltip="Global gridded soil information (texture, pH, organic carbon)",
        ),
    ]

    gaps = [{"en": i18n.render(g, "en"), "uz": i18n.render(g, "uz")} for g in ctx.gaps]

    # NDVI curve serialization
    ndvi_curve_pts = None
    if ctx.ndvi_curve is not None:
        ndvi_curve_pts = [
            {
                "doy": int(r.get("doy", doy)),
                "median": round(float(r["median"]), 3),
                "p25": round(float(r.get("p25", r["median"])), 3),
                "p75": round(float(r.get("p75", r["median"])), 3),
            }
            for doy, r in ctx.ndvi_curve.iterrows()
        ]

    # Root wetness serialization
    root_w_pts = None
    if ctx.root_wetness is not None:
        root_w_pts = [
            {"month": int(m), "median": round(float(r["median"]), 3), "p10": round(float(r["p10"]), 3), "p90": round(float(r["p90"]), 3)}
            for m, r in ctx.root_wetness.iterrows()
        ]

    # SMAP anomaly serialization
    smap_anom_pts = None
    if ctx.smap_anomaly is not None:
        smap_anom_pts = [
            {"month": int(m), "median": round(float(r["median"]), 3), "p10": round(float(r["p10"]), 3), "p90": round(float(r["p90"]), 3)}
            for m, r in ctx.smap_anomaly.iterrows()
        ]

    satellite = SatelliteData(
        has_ndvi=bool(nd_ok),
        ndvi_curve=ndvi_curve_pts,
        bare_windows=[{"start_doy": int(s), "days": int(n)} for s, n in ctx.ndvi_bare_windows],
        observed_bare_days=round(float(ctx.observed_bare_days), 1) if ctx.observed_bare_days is not None else None,
        observed_unobservable_days=round(float(ctx.observed_unobservable_days), 1) if ctx.observed_unobservable_days is not None else None,
        unobservable_months=list(ctx.unobservable_months or []),
        ndvi_curve_min=round(float(ctx.ndvi_curve_min), 3) if ctx.ndvi_curve_min is not None else None,
        has_smap=bool(sm_ok),
        smap_anomaly=smap_anom_pts,
        root_wetness=root_w_pts,
    )

    return ContextResponse(
        lat=lat,
        lon=lon,
        elevation_m=round(float(ctx.elevation_m), 1),
        field_key=field_key,
        field_name=field_name,
        sources=sources,
        gaps=gaps,
        kpis=kpis,
        monthly_climatology=monthly_pts,
        frost_probability=frost_pts,
        heat_days=heat_pts,
        soil=soil_data,
        satellite=satellite,
    )
