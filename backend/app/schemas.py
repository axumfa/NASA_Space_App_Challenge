"""Pydantic schemas for Field Shift API."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


# ------------------------------------------------------------------ Config & Metadata
class DemoFieldItem(BaseModel):
    key: str
    name: str
    lat: float
    lon: float
    rotation: list[str]
    country: str = ""
    preset: bool = False
    satellite: bool = True


class ConfigResponse(BaseModel):
    demo_fields: dict[str, DemoFieldItem]
    crops: dict[str, Any]
    profiles: dict[str, dict[str, float]]
    priorities: list[str]
    translations: dict[str, dict[str, str]]
    glossary: list[list[str]]


# ------------------------------------------------------------------ Context & Climate
class ContextRequest(BaseModel):
    lat: float = Field(..., ge=-60.0, le=70.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    rain_pct: int = Field(0, ge=-30, le=20)
    temp_c: float = Field(0.0, ge=0.0, le=3.0)


class AnnualKpis(BaseModel):
    rain_median: float
    rain_p10: float
    rain_p90: float
    et0_median: float
    gap_mm: float
    is_deficit: bool
    temp_median: float
    temp_trend_slope: float
    temp_trend_significant: bool
    precip_trend_slope: float
    precip_trend_significant: bool
    last_spring_frost_median: str
    last_spring_frost_p10: str
    last_spring_frost_p90: str
    first_autumn_frost_median: str
    first_autumn_frost_p10: str
    first_autumn_frost_p90: str
    frost_free_days_median: float
    frost_free_days_p10: float
    frost_free_days_p90: float
    frost_days_median: float
    frost_days_p10: float
    frost_days_p90: float
    heat_days_median: float
    heat_days_p10: float
    heat_days_p90: float


class ClimatologyPoint(BaseModel):
    month: int
    month_name: str
    rain_mm: float
    et0_mm: float
    t_mean: float
    t_max: float
    t_min: float


class FrostWeekPoint(BaseModel):
    week: int
    frost_prob: float


class HeatMonthPoint(BaseModel):
    month: int
    heat_days: float


class SoilData(BaseModel):
    ok: bool
    source: str
    records: list[dict[str, Any]]
    message: str = ""


class SatelliteData(BaseModel):
    has_ndvi: bool
    ndvi_curve: list[dict[str, Any]] | None = None
    bare_windows: list[dict[str, Any]] = []
    observed_bare_days: float | None = None
    observed_unobservable_days: float | None = None
    unobservable_months: list[int] = []
    ndvi_curve_min: float | None = None
    has_smap: bool
    smap_anomaly: list[dict[str, Any]] | None = None
    root_wetness: list[dict[str, Any]] | None = None


class DataSourceStatus(BaseModel):
    name: str
    status: str  # "ok", "miss", "na"
    label: str
    date_range: str = ""
    tooltip: str = ""


class ContextResponse(BaseModel):
    lat: float
    lon: float
    elevation_m: float
    field_key: str | None = None
    field_name: str
    sources: list[DataSourceStatus]
    gaps: list[dict[str, str]]
    kpis: AnnualKpis
    monthly_climatology: list[ClimatologyPoint]
    frost_probability: list[FrostWeekPoint]
    heat_days: list[HeatMonthPoint]
    soil: SoilData
    satellite: SatelliteData


# ------------------------------------------------------------------ Rotations Evaluation
class RotationEvaluateRequest(BaseModel):
    lat: float
    lon: float
    rain_pct: int = Field(0, ge=-30, le=20)
    temp_c: float = Field(0.0, ge=0.0, le=3.0)
    current_crops: list[str]
    irrigation_supply: float = Field(1.0, ge=0.4, le=1.0)
    weights: dict[str, float] = Field(default_factory=dict)


class VulnerabilityRow(BaseModel):
    crop_id: str
    crop_name_en: str
    crop_name_uz: str
    frost_days: float
    heat_days: float
    heat_thr_c: float
    irrigation_mm: float
    suitability: float


class PlantingPeriod(BaseModel):
    crop_id: str
    crop_name_en: str
    crop_name_uz: str
    start_doy: int
    end_doy: int
    start_date_en: str
    start_date_uz: str
    end_date_en: str
    end_date_uz: str
    duration_days: int


class RotationOption(BaseModel):
    index: int
    is_current: bool
    is_best_fit: bool
    crops: list[str]
    crop_names_en: list[str]
    crop_names_uz: list[str]
    rule: str
    rule_desc_en: str
    rule_desc_uz: str
    fit_score: float
    fit_dry: float
    fit_normal: float
    fit_wet: float
    fit_p10: float
    fit_p90: float
    irrigation_demand_mm: float
    irrigation_delta_pct: float | None = None
    yield_loss_median_pct: float
    yield_loss_p90_pct: float
    bare_days_per_year: float
    nitrogen_kg_median: float
    heat_stress: list[dict[str, Any]]
    radar_scores: dict[str, float]
    explanations: dict[str, list[dict[str, str]]]
    plantings: list[PlantingPeriod]
    bare_windows: list[dict[str, Any]]
    vuln_rows: list[VulnerabilityRow]


class EvaluateResponse(BaseModel):
    options: list[RotationOption]
    best_fit_index: int
    tied: dict[str, bool]
    summary_box: dict[str, Any]


# ------------------------------------------------------------------ GIBS Layers
class GibsLayerItem(BaseModel):
    key: str
    layer_id: str
    date: str
    tms: str
    tile_template: str
    css_gradient: str
    vmin: float | None = None
    vmax: float | None = None
    unit: str
    max_zoom: int
    ok: bool
    message: str = ""
