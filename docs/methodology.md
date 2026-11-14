# Field Shift: methodology

Each feature and score is explained in 1–3 sentences, in the order the pipeline computes them. Formulas live in
`src/fieldshift/`; the file is named next to each item. Everything here is **decision support**: it compares
options and shows its uncertainty, and it does not replace a farmer's or agronomist's judgment.

## 1. Data and status

| Source | Used for | Status |
|---|---|---|
| NASA POWER daily (MERRA-2 / CERES-SYN), ~0.5° grid, 2001–last full year | all climate features, ET0, frost, heat, year classes | **required**, cached on disk |
| ISRIC SoilGrids (REST, 10 s timeout) → manual JSON read from the SoilGrids web map | soil texture, organic carbon, pH (shown, **not in the scores**) | optional; REST returns nothing for masked (urban, water) pixels and takes 6–10 s per point, so the demo values are cached; the Fergana demo point sits on farmland just outside the urban mask |
| MODIS MOD13Q1.061 NDVI via AppEEARS CSV in `data/raw/` | observed greenness and bare-soil windows (shown and compared, **not in the scores**) | optional; parser tested on a synthetic fixture only |
| SMAP SPL3SMP_E via AppEEARS CSV in `data/raw/` | soil-moisture anomaly (shown) | optional; same caveat |
| NASA GIBS map tiles (MODIS NDVI 8-day, GPM IMERG rate, MODIS land surface temperature 8-day, SMAP L4 surface soil moisture) | **map layers only**: shown as images with their NASA colour legend, source and observation date; never used in scores or numbers | optional; global coverage; the browser fetches the tiles; if GIBS cannot be reached the layers are listed as unavailable |
| GPM IMERG / SRTM slope as model inputs | – | **not implemented** |

Every source except POWER fails gracefully: the app runs and the "information gaps" section names what is missing and why.
POWER values equal to −999 are converted to NaN. NDVI and SMAP files are quality-filtered before use (section 8).

## 2. Climate features (`features.py`)

- **Reference ET0.** FAO-56 Penman–Monteith (eq. 6) with G = 0, computed daily from POWER Tmax/Tmin/Tmean, RH2M, WS2M (already at 2 m), solar radiation (MJ/m²/day) and the grid-cell elevation. Actual vapour pressure follows eq. 19 (mean RH × mean of es(Tmax), es(Tmin)). Validated against the FAO-56 Brussels worked example (3.9 mm/day).
- **Monthly climatology and trend.** Monthly means/totals across years; trends are Theil–Sen slopes per decade with a bootstrap 95% interval, reported as "clear" only if the interval excludes zero.
- **Growing degree days.** Modified method, daily temperatures clipped to [base, 30 °C], summed over each planting window.
- **Frost.** Last spring / first autumn day with Tmin ≤ 0 °C per year (medians reported), and the share of years with a frost in each week.
- **Heat stress.** Days with Tmax ≥ a crop-specific threshold (default 35 °C; 32–40 °C by crop). Heat is reported as a **count of days**, never converted to yield loss.
- **Water balance.** Monthly P − ET0. **Soil-moisture anomaly:** z-score of a month's mean wetness against the same calendar month in other years.
- **Year classes.** Years are sorted into dry / normal / wet by terciles of the *current rotation's irrigation demand* (high demand = "dry"), shared by all options so columns are comparable.
- **Satellite bare soil.** Median NDVI by 16-day period; windows where it is below 0.2 (configurable) are "bare"; observed bare days per year come from linearly interpolated NDVI.

## 3. Crop knowledge base (`crops.json`, built by `scripts/build_crops.py`)

20 crops for Central Asia and the US. Kc ini/mid/end were **checked against FAO-56 Table 12** (fetched from fao.org); three were corrected (alfalfa, berseem clover, dry beans/pulses). Seasonal **Ky** is the FAO-33 value (Table 1, as reproduced in FAO paper 66) for 10 crops; four use a stand-in species (flagged), the rest a fallback formula `0.6 + 0.9·(1 − drought tolerance)` (flagged approximate). Stage lengths were **checked against FAO-56 Table 11**: cotton, winter wheat, maize, soybean, sorghum, millet, sunflower, potato, sugar beet and melon match a published row (each crop's `stages_source` names the row; the US maize and winter-wheat rows are longer than the Mediterranean/Nigeria rows used, so seasons may be short for the US); alfalfa publishes only the initial and development stages; barley, mung bean, lentil, chickpea, safflower, rapeseed and the cover crops are the author's estimates. GDD bases and requirements, temperature limits, heat thresholds, and all 0–1 trait scores (cover, organic matter, forage, income, drought and salinity tolerance, nitrogen credit) are the author's estimates; each crop lists them in its `approx` key and the UI repeats them in the gaps section. The cotton base temperature (15.5 °C) is the common DD60 convention and is not stated in the FAO documents consulted. Alfalfa is modelled as a **1-year stand**, a simplification.

## 4. Rotations (`rotations.py`)

A rotation is an ordered crop sequence that repeats. Each crop is placed at the earliest day in its sowing window after the previous harvest (plus 7 days), counting from 1 January of cycle year 0; the cycle is the smallest whole number of years (≤ 3) after which the first crop can be sown again, so overlaps cannot occur. A rotation is *feasible* only if every planting passes a frost-free-season check (for frost-sensitive crops) and has at least 85% of its GDD requirement in median climate.
Candidates are generated by rules and the best of each rule family (by an absolute score) is kept: **legume** insertion, **cover crop** in a bare window (cycle length unchanged), **drought-tolerant swap**, **income swap**, **perennial** (alfalfa), **winter crop** to break the cycle. The farmer's current rotation is always included.

## 5. Per-planting scoring (`scoring.py`)

For each planting in each historical year:

- **Climate suitability** = 100 × temperature fit × (1 − 0.5·frost penalty) × (1 − 0.5·heat penalty) × GDD sufficiency. Temperature fit is a trapezoid on daily mean temperature; the frost penalty saturates at 3 killing-frost days; the heat penalty saturates when 40% of season days exceed the crop's heat threshold.
- **Crop water use** ETc = Σ Kc(day) × ET0(day); **effective rain** = min(0.8·P, ETc); **irrigation demand** = ETc − effective rain.
- **Irrigation supply** (slider, default 100%). Water available to a planting = supply × the 90th-percentile demand of that crop-season over the record. If demand exceeds supply, the relative ET deficit is (demand − supply)/ETc and **yield loss = min(1, Ky × deficit)** (FAO-33). This is the "yield at risk" shown on cards; it is 0 when water is plentiful. Suitability is multiplied by (1 − loss), so shortages also lower income and forage.

## 6. Rotation subscores (0–100, per year of the cycle)

| Priority | Natural quantity | Subscore |
|---|---|---|
| Water saving | irrigation demand, mm/yr | 100·(1 − demand/1200) (full demand, so a shortage never "saves" water) |
| Soil organic matter | Σ om·days / (365·years) | scaled so 0.6 = 100 |
| Nitrogen fixing | Σ N credit / years, kg N/ha/yr | scaled so 50 kg = 100 |
| Erosion reduction | Σ cover·days / (365·years); bare days/yr | scaled so 0.8 = 100 |
| Forage value | Σ forage·yield factor / years | scaled so 0.6 = 100 |
| Market / income | Σ income index·yield factor / years | scaled so 0.9 = 100; cover crops are negative (seed + termination) |

Also computed: **pest-cycle break** = 100 × (1 − share of cyclic neighbours from the same crop family) and **bare days/year** from the crop calendar.

## 7. "Fit to your priorities (compared among these options)" (`compare.py`)

1. For each priority, the median natural value of every option is min-max scaled to 0–100 **across the options shown** (for water, lower is better). If the options differ by less than a floor (30 mm irrigation; 10 bare days for erosion; 5 score points otherwise) the priority is a **tie** and every option gets 50.
2. Slider weights are rescaled to sum to 1; fit = Σ weight × scaled score × (0.6 + 0.4·climate suitability/100) × (0.85 + 0.15·pest break/100).
3. The result is a **relative** ranking, not a grade or a yield forecast; adding or removing an option changes the numbers. Natural units (mm, days, kg N, % yield at risk, hot days) are always shown next to it.

**Three of the six priorities are soil criteria** (organic matter, nitrogen fixing, erosion reduction). With equal sliders, soil therefore carries half of the weight, and options that add cover crops or legumes tend to win. That is a modelling choice, not a finding; use the sliders (or the water-first and income-first quick settings) to see how the ranking depends on it. Soil data (SoilGrids texture, carbon, pH) is displayed but does not enter these subscores.

## 8. Quality control of satellite files (`fetch/appeears.py`)

- **MOD13Q1 NDVI:** every QA layer present must pass. `VI_Quality` is decoded bit by bit (MODLAND QA ≤ 1 so not cloudy; no mixed clouds,
  possible snow/ice or possible shadow; usefulness code ≤ 11), checked against NASA's own decoded columns in a real download;
  `pixel_reliability` 0 or 1 is also required when that layer is present. AppEEARS delivers NDVI already scaled (values are used as
  delivered; raw integers are multiplied by 0.0001); valid range −0.2 to 1.
- **SMAP SPL3SMP_E.006:** retrieval-quality flag bit 0 must be 0 ("recommended quality", which matches NASA's decoded description), the
  flag's fill value 65534 is rejected explicitly, soil-moisture fill −9999 is rejected; AM and PM are averaged. Version .005 does not exist
  in AppEEARS; layer names were verified against its product API. Over some places no retrieval is ever "recommended quality" (none
  was at the Fergana, Bukhara or Samarkand town points in 2025–26), so SMAP can legitimately be empty.
- **Point matching:** the CSV may hold several points; NDVI needs one within 0.01° (~1 km) of the field and SMAP within 0.06° (~6 km).
- **Short records:** a seasonal NDVI curve from fewer than 5 years is labelled a rough picture; a soil-moisture anomaly needs ≥ 4 years
  of the same calendar month, otherwise none is shown. Observed bare days need a year with at least 12 good observations.
- The column names are matched by pattern; if required columns are missing, an error lists the real ones and the gap is reported.

## 9. Uncertainty

Scores are computed for every historical start year, then summarised as the median and 10th–90th percentile, and separately for dry, normal and wet years. "Worst 1 year in 10" on the cards is the 90th percentile. These ranges reflect **weather variability only**, not errors in crop parameters, reanalysis bias, or water supply (use the supply slider for the latter).

## 10. Explanations (`explain.py`)

Templated text built only from computed features, scores and crop data: why the option was suggested, evidence (numbers), benefits and trade-offs versus the current rotation, information gaps, and risks for local expert review (salinity, market, new-crop equipment and seed, irrigation timing). An optional LLM rewording step is **not implemented**.

## 11. Known limitations

- POWER is a ~50 km reanalysis blend; over irrigated land it runs hot and dry, so hot-day counts and ET0 are probably overstated (an unverified expectation, not measured against stations).
- Irrigation supply, soil salinity, slope, labour, machinery and prices are not observed.
- Crop parameters are regional approximations; stage lengths, GDD, heat thresholds and trait scores are unverified estimates.
- Year classes come from model-estimated irrigation demand, not from river flow or snowpack.

## 12. The map (`mapview.py`, `fetch/gibs.py`)

- **Library:** Leaflet through folium and streamlit-folium, which the app already used. MapLibre GL JS and PyDeck would add a build step or a WebGL dependency without a feature we need (all data layers are ready-made raster tiles). Layer switching happens inside the browser, so the Streamlit script does not rerun and panning stays smooth.
- **Basemaps:** Esri World Imagery (satellite, default), OpenStreetMap (street), OpenTopoMap (terrain). Each shows its provider attribution on the map. These are third-party services with their own terms (Esri's imagery terms, OSM tile usage policy, OpenTopoMap CC-BY-SA); check them before any commercial deployment.
- **Data layers (NASA GIBS, public):** NDVI, rainfall rate, land surface temperature, surface soil moisture. For each, the newest observation date and tile pyramid come from the live GIBS capabilities document, and the legend colours and range from NASA's published colormap, so nothing on the map is generated by this project. Differences to keep in mind: temperature is *land surface* (not air) temperature; the soil-moisture layer is the SMAP L4 *model analysis* that assimilates SMAP data, not a direct retrieval; the rainfall layer is a rate (mm/h) for one day, not a seasonal total. A cached copy of the metadata (12 h) is used and marked with `*` when GIBS cannot be reached; with no cache the layers are offered as unavailable.
- **Not drawn:** a field boundary. The project has coordinates only, no real boundary geometry for any field.
- **Not connected to the scores:** the map layers are for orientation; the climate indicators, scores and charts still come from NASA POWER (and the optional AppEEARS files).
