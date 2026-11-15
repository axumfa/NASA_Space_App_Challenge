# Field Shift — Developer & Agent Instructions

## Overview
Field Shift is a crop-rotation decision support system developed for the NASA Space Apps Challenge 2026. It combines NASA satellite/climate data (NASA POWER, MODIS NDVI, SMAP, GIBS) with FAO agronomic models (FAO-56 Penman-Monteith ET0, FAO-33 Ky yield response) to evaluate climate-resilient crop rotations.

## Tech Stack
- **Language**: Python 3.12 (compatible with 3.11+)
- **App Framework**: Streamlit 1.67.0
- **Math & Data**: NumPy 2.5.4, pandas 3.1.1
- **Visualization & Maps**: Plotly 7.1.0, Folium 0.20.0, vendored Leaflet
- **Testing**: pytest 9.2.0, Streamlit `AppTest`

## Build, Run & Test Commands
```bash
# Run local Streamlit app
uv run streamlit run app.py

# Run unit tests
PYTHONPATH=src uv run pytest -q

# Run agronomic models audit and smoke tests
PYTHONPATH=src uv run python scripts/checks.py
PYTHONPATH=src uv run python scripts/app_smoke.py
```

## Core Architecture & Conventions
1. **Offline Independence**: Demo fields (`fergana`, `kansas`, `karakalpakstan`, `bukhara`, `samarkand`) MUST work offline using committed data in `data/demo_cache/`. Never break cache keys or force external network requests for demo points.
2. **Data & Calculation Integrity**:
   - Every number presented in the UI or in explanations MUST originate from computed features, scores, or `crops.json`. Zero fabricated metrics.
   - Quality control: AppEEARS MODIS NDVI points require peak NDVI >= 0.6 to confirm cropland.
3. **Localization (i18n)**:
   - Full dual-language support: English (`en`) and Uzbek (`uz`).
   - Bullet points, explanations, and gap messages use `Msg` objects (`src/fieldshift/i18n.py`) so computation remains language-neutral and values render dynamically in the user's chosen language.
4. **UI Design System**:
   - Adhere to the Field Shift earthy palette (`#2F6B45` forest, `#B9731F` et0, `#3F78A5` rain, `#B04A35` heat).
   - Use `pchart()` instead of raw `st.plotly_chart()` to respect toolbar visibility rules across languages.
