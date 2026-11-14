"""Field Shift - crop-rotation decision support with NASA data (Streamlit UI)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd
import streamlit as st

from fieldshift import features as F
from fieldshift import viz
from fieldshift.compare import FIT_LABEL, FIT_SHORT
from fieldshift.config import DEMO_FIELDS
from fieldshift.crops import load_crops
from fieldshift.explain import explain
from fieldshift.fetch.soil import fetch_soil
from fieldshift.pipeline import build_context, choose, run
from fieldshift.rotations import schedule
from fieldshift.scoring import PRIORITIES, PROFILES, DailyClimate, Weights, planting_table

st.set_page_config(page_title="Field Shift", page_icon="🌾", layout="wide")
DB = load_crops()
CROP_IDS = list(DB)
LABEL = viz.LABEL

st.markdown("""<style>
html, body, [class*="css"] { font-size: 18px; }
h1, h2, h3 { color: #2f5d3a; }
.card-title { font-size: 1.15rem; font-weight: 700; line-height: 1.3; }
.badge { background:#7a6a53; color:#ffffff; padding:2px 10px; border-radius:12px; font-size:.8rem; }
.fit { font-size: 2.4rem; font-weight: 800; color:#2f5d3a; line-height:1; }
.metric-row { font-size: 1rem; margin: .2rem 0; }
.disclaimer { color:#2b2b2b; background:#fff4d6; border-left:6px solid #e0a800; padding:.7rem 1rem; border-radius:6px; font-size:1rem;}
</style>""", unsafe_allow_html=True)
st.title("🌾 Field Shift")
st.caption("Explore crop-rotation options for your field using NASA satellite and climate data.")
st.markdown('<div class="disclaimer"><b>This tool supports, and does not replace, your own judgment and that of a local '
            'agronomist.</b> Results are estimates from regional data; check them with local experts before changing what you grow.</div>',
            unsafe_allow_html=True)


# ------------------------------------------------------------------ cached heavy work
# st.cache_data keys: field (lat, lon), current rotation, what-if values (and priority weights for the display choice).
@st.cache_data(show_spinner="Getting NASA climate data for this field…", max_entries=16)
def get_context(lat: float, lon: float, rain_pct: int, temp_c: float):
    return build_context(lat, lon, rain_factor=1 + rain_pct / 100, temp_delta=temp_c)


@st.cache_data(show_spinner="Comparing rotation options…", max_entries=16)
def get_pool(lat: float, lon: float, rain_pct: int, temp_c: float, current: tuple[str, ...], supply: float):
    ctx = get_context(lat, lon, rain_pct, temp_c)
    return run(ctx, current, Weights(), n_alternatives=500, n_per_rule=500, irrigation_supply=supply)


@st.cache_data(show_spinner=False, max_entries=64)
def get_display(lat: float, lon: float, rain_pct: int, temp_c: float, current: tuple[str, ...], supply: float,
                weights: tuple[float, ...], force: tuple[tuple[str, ...], ...]):
    return choose(get_pool(lat, lon, rain_pct, temp_c, current, supply), Weights(*weights), n=4, force=force)


@st.cache_data(show_spinner=False)
def get_soil(lat: float, lon: float, key: str | None):
    r = fetch_soil(lat, lon, key)
    return r.ok, r.name if hasattr(r, "name") else r.source, r.data.to_dict("records"), r.message, r.source


# ------------------------------------------------------------------ sidebar
S = st.session_state
S.setdefault("field_choice", "Fergana Valley, Uzbekistan")
S.setdefault("lat", DEMO_FIELDS["fergana"].lat)
S.setdefault("lon", DEMO_FIELDS["fergana"].lon)
names = {f.name: k for k, f in DEMO_FIELDS.items()}


def on_field_change() -> None:
    k = names.get(S.field_choice)
    if k:
        f = DEMO_FIELDS[k]
        S.lat, S.lon = f.lat, f.lon
        for i in range(3):
            S[f"crop{i}"] = f.rotation[i] if i < len(f.rotation) else "—"


def on_profile() -> None:
    """Quick settings: same ratios as the profiles used in the scoring checks (primary 8:1, soil 4:1)."""
    w = PROFILES.get(S.profile)
    for m in PRIORITIES:
        S[f"w_{m}"] = int(getattr(w, m)) if w else 5


for _m in PRIORITIES:
    S.setdefault(f"w_{_m}", 5)
S.setdefault("rain", 0); S.setdefault("temp", 0.0); S.setdefault("supply", 100)


with st.sidebar:
    st.header("Your field")
    st.radio("Choose a field", [*names, "My own location"], key="field_choice", on_change=on_field_change)
    k = names.get(S.field_choice)
    if "crop0" not in S:
        on_field_change()
    S.lat = st.number_input("Latitude", -60.0, 70.0, float(S.lat), 0.01, format="%.2f")
    S.lon = st.number_input("Longitude", -180.0, 180.0, float(S.lon), 0.01, format="%.2f")
    st.subheader("What you grow now")
    st.caption("Crops in the order you grow them (one per season/year).")
    opts = ["—", *CROP_IDS]
    picks = [st.selectbox(f"Crop {i + 1}" + (" (optional)" if i == 2 else ""), opts if i else CROP_IDS,
                          key=f"crop{i}", format_func=lambda c: DB[c]["name"] if c in DB else "— none —") for i in range(3)]
    current = tuple(c for c in picks if c != "—")
    st.subheader("What matters to you")
    st.selectbox("Quick settings", ["Balanced", *PROFILES], key="profile", on_change=on_profile,
                 help="Pre-sets the sliders; you can still change them.")
    helps = {"water_saving": "Needing less irrigation water.", "soil_om": "Building organic matter (soil 'humus') that holds water and nutrients.",
             "nitrogen": "Legumes put nitrogen into the soil, saving fertiliser.", "erosion": "Keeping the soil covered so wind and rain do not carry it away.",
             "forage": "Feed for animals (hay, grazing).", "income": "Expected market income from the crops."}
    w = Weights(**{m: float(st.slider(LABEL[m], 0, 10, key=f"w_{m}", help=helps[m])) for m in PRIORITIES})
    st.subheader("What if…?")
    with st.form("whatif"):   # one recompute per click, not one per slider move
        rain_pct = st.slider("Rainfall change (%)", -30, 20, step=5, key="rain", help="Applied to every day of the climate record.")
        temp_c = st.slider("Temperature rise (°C)", 0.0, 3.0, step=0.5, key="temp")
        supply = st.slider("Irrigation water available (% of what crops need)", 40, 100, step=5, key="supply",
                           help="100% = enough water in almost every year. Lower values show how much yield is put at risk by a shortage.")
        st.form_submit_button("Apply what-if", type="primary")
    supply = supply / 100

lat, lon = float(S.lat), float(S.lon)
if not current:
    st.error("Pick at least one crop you grow now."); st.stop()
if len(set(current)) != len(current):
    st.warning("The same crop is listed twice; each crop should appear once in your rotation."); st.stop()
if schedule(current, DB) is None:
    st.error("This crop order does not fit a repeating calendar of 1–3 years (the crops overlap in time or the cycle is too long). Try another order."); st.stop()

try:
    ctx = get_context(lat, lon, rain_pct, temp_c)
except Exception as e:  # noqa: BLE001
    st.error(f"Could not get NASA POWER climate data for this place ({e}). Check your connection; demo fields work offline once downloaded.")
    st.stop()
display, tied = get_display(lat, lon, rain_pct, temp_c, current, supply, tuple(w.as_dict().values()),
                            (("winter_wheat", "mung_bean", "cotton"),) if current == ("winter_wheat", "cotton") else ())
cur = display[0]
if rain_pct or temp_c or supply < 1:
    st.info(f"What-if active: rainfall {rain_pct:+d}%, temperature +{temp_c:.1f} °C, irrigation water {supply*100:.0f}%.")

VIEWS = ["📍 Your field", "🔀 Rotation options", "📖 Glossary & data"]
# A keyed radio (not st.tabs): st.tabs jumps back to the first tab on every rerun, e.g. when a what-if slider moves.
view = st.radio("View", VIEWS, horizontal=True, key="view", label_visibility="collapsed")

# ------------------------------------------------------------------ tab 1
if view == VIEWS[0]:
    d, ann = ctx.daily, ctx.annual
    clim = F.monthly_climatology(d)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Where is your field?")
        try:
            import folium
            from streamlit_folium import st_folium
            m = folium.Map(location=[lat, lon], zoom_start=7, tiles="OpenStreetMap")
            folium.Marker([lat, lon], tooltip="Your field").add_to(m)
            out = st_folium(m, height=300, width=None, returned_objects=["last_clicked"], key="map")
            if out and out.get("last_clicked"):
                lc = out["last_clicked"]
                if abs(lc["lat"] - lat) > 1e-3 or abs(lc["lng"] - lon) > 1e-3:
                    S.lat, S.lon, S.field_choice = round(lc["lat"], 2), round(lc["lng"], 2), "My own location"
                    st.rerun()
            st.caption("Click the map to move the field. Climate data is for a ~50 km area around the point.")
        except Exception:  # noqa: BLE001
            st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))
    with c2:
        st.subheader("Key numbers (typical year)")
        a, b = st.columns(2)
        a.metric("Rain per year", f"{ann['precip'].median():.0f} mm")
        b.metric("Water the air can take (ET0)", f"{ann['et0'].median():.0f} mm", help="Evapotranspiration: water lost from soil and plants to the air.")
        a.metric("Last spring frost", viz.doy_to_date(ann["last_spring_frost_doy"].median()))
        b.metric("First autumn frost", viz.doy_to_date(ann["first_autumn_frost_doy"].median()))
        a.metric("Frost days per year", f"{ann['frost_days'].median():.0f}")
        b.metric("Very hot days (≥ 35 °C)", f"{ann['heat_days'].median():.0f}")
        t_t, p_t = F.theil_sen_trend(ann["t_mean"]), F.theil_sen_trend(ann["precip"])
        st.markdown(f"**Trend {ann.index.min()}–{ann.index.max()}:** temperature {t_t.slope_per_decade:+.2f} °C per decade "
                    f"({'clear' if t_t.significant else 'not clear'} trend); rain {p_t.slope_per_decade:+.0f} mm per decade "
                    f"({'clear' if p_t.significant else 'not clear'} trend).")
    st.plotly_chart(viz.fig_water_balance(clim), width="stretch")
    wk = F.frost_probability_by_week(d)
    heat = (d["T2M_MAX"] >= 35).groupby(d.index.month).sum() / ann.shape[0]
    st.plotly_chart(viz.fig_frost_heat(wk, heat), width="stretch")

    st.subheader("Bare soil and vulnerable seasons for what you grow now")
    st.plotly_chart(viz.fig_calendar(cur.rotation), width="stretch")
    bw = cur.rotation.bare_windows()
    st.write(f"Your field is bare about **{cur.rotation.bare_days_per_year():.0f} days a year** according to the crop calendar"
             + (": " + ", ".join(f"{viz.doy_to_date(s % 365 + 1)} for {n} days" for s, n in bw) if bw else "") + ".")
    if ctx.ndvi_curve is not None:
        st.plotly_chart(viz.fig_ndvi(ctx.ndvi_curve, ctx.ndvi_bare_windows, 0.2), width="stretch")
        if ctx.observed_bare_days is not None:
            st.write(f"Satellite view: the field is below the bare-soil greenness level about **{ctx.observed_bare_days:.0f} days a year**"
                     f" (the crop calendar above says {cur.rotation.bare_days_per_year():.0f}). Differences usually mean sowing dates, weeds or cloud gaps differ from the typical calendar.")
    else:
        st.caption("Satellite vegetation (MODIS NDVI) is not loaded for this field, so bare periods come from typical sowing and harvest dates, not from observed greenness. "
                   "Put the AppEEARS CSV in data/raw/ to add it.")
    if ctx.smap_anomaly is not None:
        st.plotly_chart(viz.fig_soil_anomaly(ctx.smap_anomaly), width="stretch")
    else:
        st.plotly_chart(viz.fig_root_wetness(ctx.root_wetness), width="stretch")
        st.caption("Satellite soil moisture (SMAP) is not usable for this field, so this is NASA POWER's model estimate of root-zone wetness "
                   "(~50 km grid), not a satellite measurement. See the information gaps for the reason.")
    tbl = planting_table(cur.rotation, DB, DailyClimate(d))
    rows = []
    for i, p in enumerate(cur.rotation.plantings):
        vals = pd.DataFrame([rows_[i] for rows_ in tbl.values()]).median()
        rows.append({"Crop": DB[p.crop_id]["name"], "Frost days in season": f"{vals.frost_days:.0f}",
                     f"Hot days (≥ {DB[p.crop_id]['heat_thr_c']:.0f} °C)": f"{vals.heat_days:.0f}",
                     "Water to add by irrigation (mm)": f"{vals.irrigation_mm:.0f}", "Climate fit (0-100)": f"{vals.suitability:.0f}"})
    st.markdown("**When your current crops are most vulnerable** (typical year, from the daily weather record):")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.subheader("Soil")
    ok, name, recs, msg, src = get_soil(lat, lon, k)
    if ok:
        r = recs[0]
        st.write(f"{src}: " + ", ".join(f"{kk} {vv:.1f}" if isinstance(vv, float) else f"{kk} {vv}" for kk, vv in r.items()))
    else:
        st.info("Soil data is not available for this field yet (SoilGrids could not be reached and no manual reading was found). "
                "It is listed as an information gap and is not used in the scores.")
    with st.expander("What data is missing for this field?"):
        for g in ctx.gaps:
            st.write("• " + g)

# ------------------------------------------------------------------ tab 2
if view == VIEWS[1]:
    st.subheader(FIT_LABEL)
    st.caption("A relative score from 0 to 100 that compares the options shown here, using the priorities you set. "
               "It is not a grade or a yield forecast. Real units (mm of water, days, % yield at risk) are shown on every card.")
    ties = [LABEL[m] for m, v in tied.items() if v]
    if ties:
        st.info("These options do not differ meaningfully on: " + ", ".join(ties) + ". That priority does not change the ranking.")
    st.plotly_chart(viz.fig_fit_by_year_type(display), width="stretch")
    cols = st.columns(len(display))
    ci = cur.summary
    for i, (col, r) in enumerate(zip(cols, display)):
        s, e = r.summary, explain(r, cur, ctx)
        with col:
            names_ = " → ".join(DB[c]["name"] for c in r.rotation.crops)
            st.markdown(f'<div class="card-title">{names_}</div>', unsafe_allow_html=True)
            if i == 0:
                st.markdown('<span class="badge">Your current rotation</span>', unsafe_allow_html=True)
            else:
                st.caption(r.rotation.detail.capitalize())
            fit = s["fit"]
            st.markdown(f'<div class="fit">{fit["median"]:.0f}</div>', unsafe_allow_html=True)
            st.caption(f"{FIT_SHORT} · typical range {fit['p10']:.0f}–{fit['p90']:.0f} · dry {fit['median_dry']:.0f} / normal {fit['median_normal']:.0f} / wet {fit['median_wet']:.0f}")
            irr, cirr = s["irrigation_demand_mm"]["median"], ci["irrigation_demand_mm"]["median"]
            pct = f" ({100 * (irr - cirr) / cirr:+.0f}% vs now)" if i and cirr else ""
            yl = s["yield_loss"]
            heat_lines = "".join(
                f'<div class="metric-row">🔥 {DB[pl.crop_id]["name"]}: <b>{s[f"heat_days_{j}"]["median"]:.0f}</b> days above '
                f'{DB[pl.crop_id]["heat_thr_c"]:.0f} °C in season (bad year: {s[f"heat_days_{j}"]["p90"]:.0f})</div>'
                for j, pl in enumerate(r.rotation.plantings) if DB[pl.crop_id]["season"] != "cover")
            st.markdown(f'<div class="metric-row">💧 Irrigation need: <b>{irr:.0f} mm/yr</b>{pct}</div>'
                        f'<div class="metric-row">🟤 Bare soil: <b>{r.rotation.bare_days_per_year():.0f} days/yr</b></div>'
                        f'<div class="metric-row">🌱 Nitrogen from legumes: <b>{s["n_kg"]["median"]:.0f} kg N/ha/yr</b></div>'
                        f'<div class="metric-row">⚠️ Yield at risk from water shortage: <b>{yl["median"]*100:.0f}%</b> typical, '
                        f'<b>{yl["p90"]*100:.0f}%</b> in a bad year (1 in 10)</div>' + heat_lines, unsafe_allow_html=True)
            st.caption("Heat exposure is a count of hot days, not a yield forecast. Temperatures come from ~50 km reanalysis that runs hot over irrigated land.")
            st.plotly_chart(viz.fig_radar(r, cur, viz.color_for(i)), width="stretch", key=f"radar{i}")
            for title, items in (("Why this option", e.why), ("Evidence (numbers)", e.evidence), ("Benefits", e.benefits + [f"Trade-off: {t}" for t in e.tradeoffs]),
                                 ("Information gaps", e.gaps), ("Risks to check with a local expert", e.risks)):
                with st.expander(title, expanded=(title == "Why this option")):
                    for it in items:
                        st.write("• " + it)
    st.caption("Shaded radar = this option, dotted = your current rotation. Each axis compares options with each other (outer edge = best of those shown).")

# ------------------------------------------------------------------ tab 3
if view == VIEWS[2]:
    st.subheader("What the words mean")
    gl = {
        "Evapotranspiration (ET0)": "Water that leaves the field as vapour: from the soil and through plant leaves. ET0 is how much a well-watered reference grass would lose on a given day. Crops use a share of it (the 'crop coefficient', Kc).",
        "Water balance": "Rain minus ET0 for a month. Negative means the air can take more water than rain provides, so plants need irrigation or stored soil water.",
        "Irrigation need": "Crop water use over the season minus the rain that actually reaches the roots. Shown in mm; 100 mm = 1,000 m³ per hectare.",
        "NDVI": "A 'greenness' number from satellites (0 = bare, 0.8 = dense crop). Low values show when the field is bare.",
        "Soil-moisture anomaly": "How much wetter or drier the soil is than normal for the time of year. Negative = drier than usual.",
        "Frost risk": "Chance that the night minimum drops to 0 °C or lower. Late spring and early autumn frosts can kill young or ripening crops.",
        "Heat stress": "Days when the daytime high goes above a crop's tolerance (for example 35–38 °C). Flowers and grain can fail.",
        "Growing degree days": "A running total of useful warmth. A crop needs a certain amount to reach maturity.",
        "Yield at risk": "How much of a normal harvest may be lost because the crop gets less water than it needs (FAO yield-response factors). It is 0 when irrigation water is plentiful. Heat is shown separately, as a count of very hot days.",
        "Dry / normal / wet year": "Years sorted into thirds by how much irrigation water crops needed: dry = highest need.",
        "Fit to your priorities": "A relative 0–100 comparison among the options shown, based on the sliders. It changes when you change the options or sliders.",
    }
    for t, text in gl.items():
        with st.expander(t):
            st.write(text)
    st.subheader("NASA and other data used")
    srcs = pd.DataFrame([
        ["NASA POWER (MERRA-2, CERES-SYN)", "Daily temperature, rain, humidity, wind, sunshine, soil wetness", "~50 km grid, daily", "2001–2025", "Used"],
        ["ISRIC SoilGrids", "Soil texture, organic carbon, pH", "250 m", "static", "Used only if reachable or entered by hand"],
        ["MODIS NDVI (MOD13Q1)", "Greenness, bare-soil periods", "250 m, 16-day", ctx.ndvi.date_range if ctx.ndvi and ctx.ndvi.ok else "–",
         "Used for display and comparison" if ctx.ndvi and ctx.ndvi.ok else "Not loaded for this field"],
        ["SMAP soil moisture", "Soil moisture anomaly", "~9 km", ctx.smap.date_range if ctx.smap and ctx.smap.ok else "–",
         "Used for display" if ctx.smap and ctx.smap.ok else "Not loaded; POWER soil wetness is the model-based stand-in"],
        ["GPM IMERG / SRTM", "Rain cross-check; slope", "10 km / 30 m", "–", "Not yet loaded"],
    ], columns=["Source", "What for", "Resolution", "Period", "Status"])
    st.dataframe(srcs, hide_index=True, width="stretch")
    st.subheader("Satellite and model data versus your ground")
    st.write("• Climate values come from a ~50 km model/satellite blend, not from a weather station at your field. Over irrigated land it tends to run hotter and drier than the ground.\n"
             "• Irrigation need and ET0 are computed (FAO-56 Penman–Monteith), not measured.\n"
             "• Crop values (water use, heat limits, nitrogen credit) are regional approximations; check them with local advisers.\n"
             "• Water supply from rivers or canals is not observed; use the irrigation-water slider to test shortages.")
st.divider()
st.caption("Decision support only. Validate with local agronomists. Data: NASA POWER, ISRIC SoilGrids. Method notes: docs/methodology.md.")
