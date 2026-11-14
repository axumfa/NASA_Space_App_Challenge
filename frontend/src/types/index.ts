export interface DemoFieldItem {
  key: string;
  name: string;
  lat: number;
  lon: number;
  rotation: string[];
  country: string;
  preset: boolean;
  satellite: boolean;
}

export interface CropStage {
  ini: number;
  dev: number;
  mid: number;
  late: number;
}

export interface CropInfo {
  name: string;
  family: string;
  season: string;
  stages: [number, number, number, number];
  kc: { ini: number; mid: number; end: number };
  gdd_base_c: number;
  gdd_total: number;
  ky: number;
  heat_thr_c: number;
  frost_thr_c: number;
  n_credit: number;
  om_score: number;
  erosion_cover: number;
  forage_value: number;
  economic_tier: number;
  traits: string[];
}

export interface ConfigResponse {
  demo_fields: Record<string, DemoFieldItem>;
  crops: Record<string, CropInfo>;
  profiles: Record<string, Record<string, number>>;
  priorities: string[];
  translations: Record<string, { en: string; uz?: string }>;
  glossary: [string, string, string][];
}

export interface AnnualKpis {
  rain_median: number;
  rain_p10: number;
  rain_p90: number;
  et0_median: number;
  gap_mm: number;
  is_deficit: boolean;
  temp_median: number;
  temp_trend_slope: number;
  temp_trend_significant: boolean;
  precip_trend_slope: number;
  precip_trend_significant: boolean;
  last_spring_frost_median: string;
  last_spring_frost_p10: string;
  last_spring_frost_p90: string;
  first_autumn_frost_median: string;
  first_autumn_frost_p10: string;
  first_autumn_frost_p90: string;
  frost_free_days_median: number;
  frost_free_days_p10: number;
  frost_free_days_p90: number;
  frost_days_median: number;
  frost_days_p10: number;
  frost_days_p90: number;
  heat_days_median: number;
  heat_days_p10: number;
  heat_days_p90: number;
}

export interface ClimatologyPoint {
  month: number;
  month_name: string;
  rain_mm: number;
  et0_mm: number;
  t_mean: number;
  t_max: number;
  t_min: number;
}

export interface FrostWeekPoint {
  week: number;
  frost_prob: number;
}

export interface HeatMonthPoint {
  month: number;
  heat_days: number;
}

export interface SoilData {
  ok: boolean;
  source: string;
  records: Record<string, string | number>[];
  message: string;
}

export interface SatelliteData {
  has_ndvi: boolean;
  ndvi_curve: { doy: number; median: number; p25: number; p75: number }[] | null;
  bare_windows: { start_doy: number; days: number }[];
  observed_bare_days: number | null;
  observed_unobservable_days: number | null;
  unobservable_months: number[];
  ndvi_curve_min: number | null;
  has_smap: boolean;
  smap_anomaly: { month: number; median: number; p10: number; p90: number }[] | null;
  root_wetness: { month: number; median: number; p10: number; p90: number }[] | null;
}

export interface DataSourceStatus {
  name: string;
  status: "ok" | "miss" | "na";
  label: string;
  date_range: string;
  tooltip: string;
}

export interface ContextResponse {
  lat: number;
  lon: number;
  elevation_m: number;
  field_key: string | null;
  field_name: string;
  sources: DataSourceStatus[];
  gaps: { en: string; uz: string }[];
  kpis: AnnualKpis;
  monthly_climatology: ClimatologyPoint[];
  frost_probability: FrostWeekPoint[];
  heat_days: HeatMonthPoint[];
  soil: SoilData;
  satellite: SatelliteData;
}

export interface VulnerabilityRow {
  crop_id: string;
  crop_name_en: string;
  crop_name_uz: string;
  frost_days: number;
  heat_days: number;
  heat_thr_c: number;
  irrigation_mm: number;
  suitability: number;
}

export interface PlantingPeriod {
  crop_id: string;
  crop_name_en: string;
  crop_name_uz: string;
  start_doy: number;
  end_doy: number;
  start_date_en: string;
  start_date_uz: string;
  end_date_en: string;
  end_date_uz: string;
  duration_days: number;
}

export interface RotationOption {
  index: number;
  is_current: boolean;
  is_best_fit: boolean;
  crops: string[];
  crop_names_en: string[];
  crop_names_uz: string[];
  rule: string;
  rule_desc_en: string;
  rule_desc_uz: string;
  fit_score: number;
  fit_dry: number;
  fit_normal: number;
  fit_wet: number;
  fit_p10: number;
  fit_p90: number;
  irrigation_demand_mm: number;
  irrigation_delta_pct: number | null;
  yield_loss_median_pct: number;
  yield_loss_p90_pct: number;
  bare_days_per_year: number;
  nitrogen_kg_median: number;
  heat_stress: {
    crop_id: string;
    crop_name_en: string;
    crop_name_uz: string;
    median_days: number;
    p90_days: number;
    threshold_c: number;
  }[];
  radar_scores: Record<string, number>;
  explanations: Record<string, { en: string; uz: string }[]>;
  plantings: PlantingPeriod[];
  bare_windows: { start_doy: number; days: number }[];
  vuln_rows: VulnerabilityRow[];
}

export interface EvaluateResponse {
  options: RotationOption[];
  best_fit_index: number;
  tied: Record<string, boolean>;
  summary_box: {
    title_en: string;
    title_uz: string;
    best_en: string;
    best_uz: string;
    reason_en: string;
    reason_uz: string;
    tradeoff_en: string;
    tradeoff_uz: string;
    check_en: string;
    check_uz: string;
    caveat_en: string;
    caveat_uz: string;
  };
}

export interface GibsLayerItem {
  key: string;
  layer_id: string;
  date: string;
  tms: string;
  tile_template: string;
  css_gradient: string;
  vmin: number | null;
  vmax: number | null;
  unit: string;
  max_zoom: number;
  ok: boolean;
  message: string;
}
