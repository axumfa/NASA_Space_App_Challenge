"""Field Shift - crop-rotation decision support with NASA data (Streamlit UI, English / Uzbek)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

# First paint: set_page_config and a light splash come BEFORE the heavy imports and the first computation, so a cold load never shows an
# empty page. Shown once per browser session (reruns on a click must not flash it); a CSS timer hides it by itself if the script dies.
st.set_page_config(page_title="Field Shift", page_icon="🌾", layout="wide", initial_sidebar_state="auto")
boot = st.empty()
if "booted" not in st.session_state:
    st.session_state["booted"] = True
    _uz = st.session_state.get("lang_label", "").startswith("O")
    boot.markdown(
        "<style>[data-testid=\"stToolbar\"],[data-testid=\"stDecoration\"]{visibility:hidden}.fs-boot{position:fixed;inset:0;z-index:99999;background:#FAF8F3;display:flex;flex-direction:column;align-items:center;"
        "justify-content:center;gap:14px;font-family:Inter,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#232623;"
        "animation:fsboothide 0s linear 12s forwards}@keyframes fsboothide{to{opacity:0;visibility:hidden}}"
        ".fs-boot b{font-size:1.25rem;letter-spacing:-.02em}.fs-boot span{font-size:.85rem;color:#6B6F66}"
        ".fs-boot i{display:block;width:150px;height:4px;border-radius:3px;background:#E3DFD3;overflow:hidden;position:relative}"
        ".fs-boot i::after{content:'';position:absolute;inset:0;width:45%;background:#2F6B45;border-radius:3px;animation:fsbootbar 1.2s ease-in-out infinite}"
        "@keyframes fsbootbar{0%{left:-45%}100%{left:100%}}</style>"
        '<div class="fs-boot"><svg viewBox="0 0 32 32" width="40" height="40" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#2F6B45"/>'
        '<path d="M6 12.5 L26 7.5" stroke="#CFE0C8" stroke-width="3" stroke-linecap="round"/><path d="M6 19 L26 14" stroke="#EAF1E4" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M6 25.5 L26 20.5" stroke="#B9C48A" stroke-width="3" stroke-linecap="round"/></svg>'
        f"<b>Field Shift</b><span>{'Yuklanmoqda…' if _uz else 'Loading…'}</span><i></i></div>", unsafe_allow_html=True)

import pandas as pd  # noqa: E402  (heavy imports after the splash on purpose)

from fieldshift import features as F  # noqa: E402
from fieldshift import viz  # noqa: E402
from fieldshift.config import DEMO_FIELDS, field_at  # noqa: E402
from fieldshift.crops import load_crops  # noqa: E402
from fieldshift.explain import explain, is_arid, summary_box  # noqa: E402
from fieldshift.fetch.soil import fetch_soil  # noqa: E402
from fieldshift import i18n, ui  # noqa: E402
from fieldshift import mapview  # noqa: E402
from fieldshift.fetch import gibs  # noqa: E402
from fieldshift.i18n import GLOSSARY, LANGS, crop_name, tr  # noqa: E402
from fieldshift.pipeline import build_context, choose, run  # noqa: E402
from fieldshift.rotations import schedule  # noqa: E402
from fieldshift.scoring import PRIORITIES, PROFILES, DailyClimate, Weights, planting_table  # noqa: E402

DB = load_crops()
CROP_IDS = list(DB)
S = st.session_state
S.setdefault("lang_label", LANGS["en"])
S["lang"] = {v: k for k, v in LANGS.items()}[S["lang_label"]]     # a click on the language control reruns with the new value
OWN = "My own location"          # option value (not displayed as is)
ui.inject_css()


def pchart(fig, **kw):
    """Plotly chart; the toolbar's tooltips are English-only in plotly.js, so it is hidden in Uzbek mode (drag to zoom still works)."""
    kw.setdefault("width", "stretch")
    st.plotly_chart(fig, config={"displayModeBar": S.get("lang", "en") == "en"}, **kw)


def t(key: str, **kw) -> str:
    return tr(key, S.lang, **kw)


def cname(cid: str) -> str:
    return crop_name(cid, S.lang, DB[cid]["name"])


def pick(widget, label: str, values: list, canon: str, fmt, **kw):
    """Selectbox/radio whose displayed text depends on the language, without `format_func`.

    The choice lives in plain session state `canon` (a raw value). The widget is keyed per language, so changing the
    language rebuilds it from `canon` and keeps the selection; programmatic changes to `canon` (made after the widget
    was created in an earlier run, e.g. a map click) are synced into the widget BEFORE it is created, because Streamlit
    forbids writing a widget's state after it exists. Returns (value, changed_by_user).
    """
    if canon not in S or S[canon] not in values:
        S[canon] = values[0]
    labels = [fmt(v) for v in values]
    wk, seen = f"{canon}__{S.lang}", f"{canon}__seen"
    if wk not in S or S[wk] not in labels or S.get(seen) != S[canon]:
        S[wk] = fmt(S[canon])
    value = values[labels.index(widget(label, labels, key=wk, **kw))]
    changed = seen in S and value != S[seen]
    S[canon] = S[seen] = value
    return value, changed


# ------------------------------------------------------------------ cached heavy work
# st.cache_data keys: field (lat, lon), current rotation, what-if values (and priority weights for the display choice).
@st.cache_data(show_spinner=False, max_entries=16)
def get_context(lat: float, lon: float, rain_pct: int, temp_c: float):
    return build_context(lat, lon, rain_factor=1 + rain_pct / 100, temp_delta=temp_c)


@st.cache_data(show_spinner=False, max_entries=16)
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
    return r.ok, r.data.to_dict("records"), r.message, r.source


# ------------------------------------------------------------------ state and callbacks
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


def field_label(name: str) -> str:
    return t("side.own") if name == OWN else t(f"field.{names[name]}")


# ------------------------------------------------------------------ header: brand, navigation, language
VIEWS = ["field", "options", "glossary"]
h1, h2, h3 = st.columns([3, 5, 2.4], vertical_alignment="center")
with h1:
    st.markdown(ui.brand(t("ui.tagline")), unsafe_allow_html=True)
with h2:
    # A keyed radio styled as tabs (not st.tabs): st.tabs jumps back to the first tab on every rerun, e.g. when a what-if slider moves.
    with st.container(key="nav"):
        view, _ = pick(st.radio, t("ui.view_label"), VIEWS, "view", lambda v: t(f"view.{v}"), horizontal=True, label_visibility="collapsed")
with h3:
    with st.container(key="langbox"):
        st.radio(t("ui.lang"), list(LANGS.values()), key="lang_label", horizontal=True, label_visibility="collapsed")
st.markdown('<div class="fs-rule"></div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ field bar (location selection)
with st.container(border=True, key="bar_field"):
    b1, b2, b3 = st.columns([5, 1.4, 1.4])
    with b1:
        first_run = "crop0" not in S
        _, field_changed = pick(st.selectbox, t("ui.field_label"), [*names, OWN], "field_choice", field_label, help=t("ui.field_help"))
        if field_changed or first_run:
            on_field_change()
    k = names.get(S.field_choice)
    S.lat = b2.number_input(t("side.lat"), -60.0, 70.0, float(S.lat), 0.01, format="%.2f")
    S.lon = b3.number_input(t("side.lon"), -180.0, 180.0, float(S.lon), 0.01, format="%.2f")

# ------------------------------------------------------------------ sidebar: rotation, priorities, scenario
with st.sidebar:
    ui.side_heading(t("ui.sidebar_rot"))
    with st.container(key="sidecrops"):                  # the crops you grow are the most important input: shown first, in a card
        st.caption(t("ui.step_rot"))
        opts = ["—", *CROP_IDS]
        picks = [pick(st.selectbox, t("side.crop_opt", n=i + 1) if i == 2 else t("side.crop", n=i + 1), opts if i else CROP_IDS,
                      f"crop{i}", lambda c: cname(c) if c in DB else t("side.none"))[0] for i in range(3)]
        current = tuple(c for c in picks if c != "—")
        if current:
            ui.rotation_preview([cname(c) for c in current])
    st.write("")
    with st.expander(t("ui.sidebar_prio"), expanded=True):
        _, profile_changed = pick(st.selectbox, t("side.quick"), ["Balanced", *PROFILES], "profile", lambda p: t(f"profile.{p}"),
                                  help=t("side.quick_help"))
        if profile_changed:
            on_profile()
        st.caption(t("ui.prio_hint"))
        wv = {}
        ui.group_label(t("ui.grp_env"))
        for m in ("water_saving", "soil_om", "nitrogen", "erosion"):
            wv[m] = float(st.slider(t(f"p.{m}"), 0, 10, key=f"w_{m}", help=t(f"ph.{m}")))
        ui.group_label(t("ui.grp_econ"))
        for m in ("forage", "income"):
            wv[m] = float(st.slider(t(f"p.{m}"), 0, 10, key=f"w_{m}", help=t(f"ph.{m}")))
        w = Weights(**{m: wv[m] for m in PRIORITIES})
    ui.side_heading(t("ui.sidebar_what"))
    with st.expander(t("side.whatif"), expanded=bool(S.rain or S.temp or S.supply < 100)):
        with st.form("whatif"):   # one recompute per click, not one per slider move
            rain_pct = st.slider(t("side.rain"), -30, 20, step=5, key="rain", help=t("side.rain_help"))
            temp_c = st.slider(t("side.temp"), 0.0, 3.0, step=0.5, key="temp")
            supply = st.slider(t("side.supply"), 40, 100, step=5, key="supply", help=t("side.supply_help"))
            st.form_submit_button(t("side.apply"), type="primary")
    supply = supply / 100

boot.empty()                       # header and field bar are on screen: reveal them
lat, lon = float(S.lat), float(S.lon)
if not current:
    st.error(t("err.pick")); st.stop()
if len(set(current)) != len(current):
    st.warning(t("err.dup")); st.stop()
if schedule(current, DB) is None:
    st.error(t("err.cal")); st.stop()

try:
    with st.spinner(t("spin.climate")):
        ctx = get_context(lat, lon, rain_pct, temp_c)
except Exception as e:  # noqa: BLE001
    st.error(t("err.power", e=e))
    st.stop()


def load_display():
    """Rotation options are needed only below the map (field view) or in the options view, so they are computed lazily:
    the map and the climate indicators appear first on a cold start."""
    with st.spinner(t("spin.pool")):
        return get_display(lat, lon, rain_pct, temp_c, current, supply, tuple(w.as_dict().values()),
                           (("winter_wheat", "mung_bean", "cotton"),) if current == ("winter_wheat", "cotton") else ())


soil_ok, soil_recs, _soil_msg, soil_src = get_soil(lat, lon, k)
ui.notice(t("ui.notice"))
if rain_pct or temp_c or supply < 1:
    st.info(t("whatif.active", rain=rain_pct, temp=temp_c, supply=supply * 100))

# ------------------------------------------------------------------ view 1: your field
if view == "field":
    d, ann = ctx.daily, ctx.annual
    clim = F.monthly_climatology(d)
    nd_ok = ctx.ndvi is not None and ctx.ndvi.ok
    sm_ok = ctx.smap is not None and ctx.smap.ok
    title = t("side.own") if S.field_choice == OWN else field_label(S.field_choice)
    fld = field_at(lat, lon)
    def state(ok: bool, applicable: bool = True) -> str:
        return "ok" if ok else ("miss" if applicable else "na")
    sat_applicable = not (fld is not None and not fld.satellite)       # presets never had a satellite point requested
    rows = [
        (t("ui.ds_power"), "ok", t("ui.st_ok"), t("ui.tip_power", rng=ctx.sources[0].date_range)),
        (t("ui.ds_ndvi"), state(nd_ok, sat_applicable), t("ui.st_ok") if nd_ok else t("ui.st_miss" if sat_applicable else "ui.st_na"),
         t("ui.tip_ndvi_ok") if nd_ok else t("ui.tip_ndvi_miss" if sat_applicable else "ui.tip_na")),
        (t("ui.ds_smap"), state(sm_ok, sat_applicable), t("ui.st_ok") if sm_ok else t("ui.st_miss" if sat_applicable else "ui.st_na"),
         t("ui.tip_smap_ok") if sm_ok else t("ui.tip_smap_miss" if sat_applicable else "ui.tip_na")),
        (t("ui.ds_soil"), state(soil_ok), t("ui.st_ok") if soil_ok else t("ui.st_miss"),
         t("ui.tip_soil_ok") if soil_ok else t("ui.tip_soil_miss")),
    ]
    coords = (f"{abs(lat):.2f}° {t('ui.hemi_n' if lat >= 0 else 'ui.hemi_s')}  ·  {abs(lon):.2f}° {t('ui.hemi_e' if lon >= 0 else 'ui.hemi_w')}")
    with st.container(border=True, key="hero"):
        hl, hr = st.columns([3, 2], gap="large")
        with hl:
            st.markdown(ui.hero_left(t("ui.selected"), title, coords, [(t("ui.elev", m=ctx.elevation_m), t("ui.elev_tip"))], t("ui.grows"),
                                     [cname(c) for c in current], t("ui.hero")), unsafe_allow_html=True)
            if st.button(t("ui.cta") + "  →", type="primary", key="cta"):
                S["view"] = "options"
                st.rerun()
        with hr:
            st.markdown(ui.data_status(t("ui.data_h"), rows, t("ui.data_note") if any(r_[1] != "ok" for r_ in rows) else ""),
                        unsafe_allow_html=True)

    ui.section(t("ui.sec_overview"), t("ui.sec_overview_sub"))
    c1, c2 = st.columns([6, 6], gap="medium")
    with c1:
        with st.container(border=True, key="panel_map"):
            try:
                from streamlit_folium import st_folium
                layers = gibs.load_cached()          # instant: live copy or the committed snapshot, never the network
                gibs.refresh_in_background()          # at most one daemon thread, only when the copy is older than 12 h
                m = mapview.build_map(lat, lon, layers, S.lang, tooltip=f"{t('map.marker')}: {lat:.2f}, {lon:.2f}",
                                      local_assets=mapview.local_assets_available())
                out = st_folium(m, height=345, width=None, returned_objects=["last_clicked"], key="map")
                if out and out.get("last_clicked"):
                    lc = out["last_clicked"]
                    if abs(lc["lat"] - lat) > 1e-3 or abs(lc["lng"] - lon) > 1e-3:
                        S.lat, S.lon, S.field_choice = round(lc["lat"], 2), round(lc["lng"], 2), OWN   # plain state: pick() syncs the widget
                        st.rerun()
                st.caption(t("map.help"))
                st.markdown(ui.layer_line(t("map.layers_h"), mapview.layer_status(layers, S.lang)), unsafe_allow_html=True)
                stale = [l for l in layers.values() if l.ok and l.stale]
                if stale:
                    st.caption(t("map.stale_note", d=stale[0].as_of or "?"))
            except Exception:  # noqa: BLE001  - the map must never take the dashboard down; plain map as a fallback
                import traceback
                traceback.print_exc()
                st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))
    with c2:
        def rng(series, unit="", fmt=None):
            lo, hi = series.quantile(.1), series.quantile(.9)
            return lo, hi
        def dates(col):
            return t("ui.kpi_dates", a=viz.doy_to_date(ann[col].quantile(.1), S.lang), b=viz.doy_to_date(ann[col].quantile(.9), S.lang))
        rain_m, et0_m = ann["precip"].median(), ann["et0"].median()
        rlo, rhi = rng(ann["precip"])
        gap = et0_m - rain_m
        et_ctx = t("ui.kpi_et0_gap", gap=gap, pct=100 * rain_m / et0_m) if gap > 0 else t("ui.kpi_et0_ok", gap=-gap)
        t_t, p_t = F.theil_sen_trend(ann["t_mean"]), F.theil_sen_trend(ann["precip"])
        free = ann["first_autumn_frost_doy"] - ann["last_spring_frost_doy"]
        hlo, hhi = rng(ann["heat_days"])
        flo, fhi = rng(ann["frost_days"])
        ui.kpi_grid([
            ui.kpi(t("ui.kpi_rain"), f"{rain_m:.0f}", t("ui.unit_mm"), t("ui.kpi_rain_d"), t("ui.kpi_range", lo=rlo, hi=rhi, unit="mm")),
            ui.kpi(t("ui.kpi_et0"), f"{et0_m:.0f}", t("ui.unit_mm"), t("ui.kpi_et0_d"), et_ctx, warn=gap > 0),
            ui.kpi(t("ui.kpi_temp"), f"{ann['t_mean'].median():.1f}", t("ui.unit_c"), t("ui.kpi_temp_d"),
                   t("ui.kpi_temp_ctx", dt=t_t.slope_per_decade, clear=t("f.clear") if t_t.significant else t("f.notclear"))),
            ui.kpi(t("ui.kpi_last"), viz.doy_to_date(ann["last_spring_frost_doy"].median(), S.lang), "", t("ui.kpi_last_d"), dates("last_spring_frost_doy")),
            ui.kpi(t("ui.kpi_first"), viz.doy_to_date(ann["first_autumn_frost_doy"].median(), S.lang), "", t("ui.kpi_first_d"), dates("first_autumn_frost_doy")),
            ui.kpi(t("ui.kpi_free"), f"{free.median():.0f}", t("ui.unit_days"), t("ui.kpi_free_d"),
                   t("ui.kpi_free_ctx", lo=free.quantile(.1), hi=free.quantile(.9))),
        ], cols=3)
    st.write("")
    ui.kpi_grid([
        ui.kpi(t("ui.kpi_frost"), f"{ann['frost_days'].median():.0f}", t("ui.unit_days"), t("ui.kpi_frost_d"),
               t("ui.kpi_range", lo=flo, hi=fhi, unit=t("ui.unit_days"))),
        ui.kpi(t("ui.kpi_hot"), f"{ann['heat_days'].median():.0f}", t("ui.unit_days"), t("ui.kpi_hot_d"),
               t("ui.kpi_hot_ctx", lo=hlo, hi=hhi), warn=True),
        ui.kpi(t("ui.kpi_rtrend"), f"{p_t.slope_per_decade:+.0f}", t("ui.unit_mm_dec"), t("ui.kpi_rtrend_d", y0=ann.index.min(), y1=ann.index.max()),
               t("f.clear") if p_t.significant else t("f.notclear")),
    ])
    st.caption(t("f.trend", y0=ann.index.min(), y1=ann.index.max(), dt=t_t.slope_per_decade, dp=p_t.slope_per_decade,
                 tclear=t("f.clear") if t_t.significant else t("f.notclear"), pclear=t("f.clear") if p_t.significant else t("f.notclear")))

    ui.section(t("ui.sec_history"))
    wk = F.frost_probability_by_week(d)
    heat = (d["T2M_MAX"] >= 35).groupby(d.index.month).sum() / ann.shape[0]
    ca, cb = st.columns(2)
    with ca, st.container(border=True, key="panel_wb"):
        pchart(viz.fig_water_balance(clim, S.lang), width="stretch")
    with cb, st.container(border=True, key="panel_temp"):
        pchart(viz.fig_temperature(clim, S.lang), width="stretch")
    cc, cd = st.columns(2)
    with cc, st.container(border=True, key="panel_frost"):
        pchart(viz.fig_frost(wk, S.lang), width="stretch")
    with cd, st.container(border=True, key="panel_heat"):
        pchart(viz.fig_heat(heat, lang=S.lang), width="stretch")

    display, tied = load_display()
    cur = display[0]
    ui.section(t("ui.sec_season"), t("f.bare_h"))
    with st.container(border=True, key="panel_cal"):
        pchart(viz.fig_calendar(cur.rotation, lang=S.lang), width="stretch")
        bw = cur.rotation.bare_windows()
        wins = (": " + ", ".join(t("f.bare_win", start=viz.doy_to_date(s % 365 + 1, S.lang), n=n) for s, n in bw)) if bw else ""
        st.write(t("f.bare_text", days=cur.rotation.bare_days_per_year(), wins=wins))
    if ctx.ndvi_curve is not None:
        with st.container(border=True, key="panel_ndvi"):
            pchart(viz.fig_ndvi(ctx.ndvi_curve, ctx.ndvi_bare_windows, 0.2, S.lang), width="stretch")
            if ctx.observed_bare_days is not None:
                cal_bare = cur.rotation.bare_days_per_year()
                txt = t("f.ndvi_text", obs=ctx.observed_bare_days, cal=cal_bare)
                if (ctx.observed_unobservable_days or 0) >= 15:
                    months = ", ".join(i18n.MONTHS[S.lang][m - 1] for m in ctx.unobservable_months) or t("f.ndvi_anytime")
                    txt += t("f.ndvi_unobs", unobs=ctx.observed_unobservable_days, months=months)
                stays_green = ctx.observed_bare_days < cal_bare / 4 and ctx.ndvi_curve_min is not None and ctx.ndvi_curve_min >= 0.2
                txt += t("f.ndvi_green", low=ctx.ndvi_curve_min, thr=0.2) if stays_green else (t("f.ndvi_diff") if abs(ctx.observed_bare_days - cal_bare) > 15 else "")
                st.write(txt)
    tbl = planting_table(cur.rotation, DB, DailyClimate(d))
    rows = []
    for i, p in enumerate(cur.rotation.plantings):
        vals = pd.DataFrame([rows_[i] for rows_ in tbl.values()]).median()
        rows.append({t("col.crop"): cname(p.crop_id), t("col.frost"): f"{vals.frost_days:.0f}",
                     t("col.hot2"): f"{vals.heat_days:.0f} (≥ {DB[p.crop_id]['heat_thr_c']:.0f} °C)",
                     t("col.irr"): f"{vals.irrigation_mm:.0f}", t("col.fit"): f"{vals.suitability:.0f}"})
    st.markdown(t("f.vuln"))
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

    ui.section(t("ui.sec_soil"))
    sa, sb_ = st.columns(2)
    with sa, st.container(border=True, key="panel_sm"):
        if ctx.smap_anomaly is not None:
            pchart(viz.fig_soil_anomaly(ctx.smap_anomaly, S.lang), width="stretch")
        else:
            pchart(viz.fig_root_wetness(ctx.root_wetness, S.lang), width="stretch")
            st.caption(t("f.smap_missing"))
    with sb_, st.container(border=True, key="panel_soil"):
        st.markdown(f"**{t('f.soil')}**")
        if soil_ok:
            r = soil_recs[0]
            def soil_label(key: str) -> str:
                return t(f"soil.{key}") if f"soil.{key}" in i18n.S else key
            TEX = {"clay": "clay", "sandy": "sandy", "silty (loam)": "silty", "clay loam": "clay_loam", "loam": "loam"}
            def soil_value(kk, vv) -> str:
                if isinstance(vv, float):
                    return f"{vv:.1f}"
                return t(f"soil.tex.{TEX[vv]}") if kk == "texture" and vv in TEX else str(vv)
            ui.kpi_grid([ui.kpi(soil_label(kk), soil_value(kk, vv), "", "") for kk, vv in r.items()])
            src_key = "soil.src_manual" if "manual" in soil_src.lower() else "soil.src_rest"
            st.caption(f"{t('f.soil')}: {t(src_key)}")
        else:
            st.info(t("f.soil_na"))
    with st.expander(t("f.gaps")):
        for g in ctx.gaps:
            st.write("• " + i18n.render(g, S.lang))
        st.write("• " + t("g.contracts"))

    st.write("")
    with st.container(border=True, key="panel_next"):
        nl, nr = st.columns([4, 1.4], vertical_alignment="center")
        nl.markdown(f'<div class="fs-next"><div><b>{t("ui.next_h")}</b><br><span>{t("ui.next_t")}</span></div></div>', unsafe_allow_html=True)
        if nr.button(t("ui.cta") + "  →", type="primary", key="cta2"):
            S["view"] = "options"
            st.rerun()

# ------------------------------------------------------------------ view 2: rotation options
if view == "options":
    display, tied = load_display()
    cur = display[0]
    st.caption(t("ui.step_trail"))
    ui.section(t("fit.label"), t("o.caption"))
    sb = summary_box(display, w, S.lang, arid=is_arid(ctx))
    with st.container(border=True, key="panel_summary"):
        st.markdown(f"#### {sb['title']}")
        st.markdown(sb["best"]); st.markdown(sb["reason"]); st.markdown(sb["tradeoff"]); st.markdown(sb["check"])
        st.caption(sb["caveat"])
    ties = [t(f"p.{m}") for m, v in tied.items() if v]
    if ties:
        st.info(t("o.ties", list=", ".join(ties)))

    # ---- at-a-glance comparison table (all numbers come from the same summaries as the cards)
    ui.section(t("ui.sec_compare"))
    def best_idx(vals: list[float], high: bool) -> set[int]:
        if len({round(v) for v in vals}) < 2:
            return set()
        tgt = max(vals) if high else min(vals)
        return {i for i, v in enumerate(vals) if abs(v - tgt) < 1e-9}
    sm = [r.summary for r in display]
    yield_low = supply >= 1.0 and all(max(x["yield_loss"]["median"], x["yield_loss"]["p90"]) * 100 < 3 for x in sm)
    head = [(" → ".join(cname(c) for c in r.rotation.crops), t("o.current") if i == 0 else t("ui.opt_n", n=i), i == 0) for i, r in enumerate(display)]
    fits = [x["fit"]["median"] for x in sm]
    irrs = [x["irrigation_demand_mm"]["median"] for x in sm]
    bares = [r.rotation.bare_days_per_year() for r in display]
    nitro = [x["n_kg"]["median"] for x in sm]
    ylds = [x["yield_loss"]["median"] * 100 for x in sm]
    best_fit = max(range(len(display)), key=lambda i: fits[i]) if len({round(v) for v in fits}) > 1 else None
    prio_rows = [(t(f"p.{m}"), [f"{x[f'norm_{m}']['median']:.0f}" for x in sm],
                  set() if tied.get(m) else best_idx([x[f"norm_{m}"]["median"] for x in sm], True)) for m in PRIORITIES]
    ui.compare_table(head, [
        ("__group__", t("ui.g_main")),
        (t("ui.tbl_fit"), [f"{v:.0f}" for v in fits], best_idx(fits, True)),
        (t("ui.tbl_dry"), [f"{x['fit']['median_dry']:.0f} / {x['fit']['median_normal']:.0f} / {x['fit']['median_wet']:.0f}" for x in sm], set()),
        ("__group__", t("ui.g_water")),
        (t("ui.tbl_irr"), [f"{v:.0f}" for v in irrs], best_idx(irrs, False)),
        (t("ui.tbl_yield"), [f"{x['yield_loss']['median'] * 100:.0f}% / {x['yield_loss']['p90'] * 100:.0f}%" for x in sm], best_idx(ylds, False)),
        *([("__note__", t("o.yield_low", sec=t("ui.sidebar_what")))] if yield_low else []),
        ("__group__", t("ui.g_soil")),
        (t("ui.tbl_bare"), [f"{v:.0f}" for v in bares], best_idx(bares, False)),
        (t("ui.tbl_n"), [f"{v:.0f}" for v in nitro], best_idx(nitro, True)),
        ("__group__", t("ui.g_prio")),
        *prio_rows,
    ], t("ui.tbl_metric"), top=best_fit, top_tag=t("ui.best_fit"))
    st.caption(t("ui.best_note"))
    with st.container(border=True, key="panel_fit"):
        pchart(viz.fig_fit_by_year_type(display, S.lang), width="stretch")

    ui.section(t("ui.sec_cards"))
    ci = cur.summary
    PER_ROW = 3
    cols = [c for j in range(0, len(display), PER_ROW) for c in st.columns(PER_ROW)][:len(display)]
    for i, (col, r) in enumerate(zip(cols, display)):
        s, e = r.summary, explain(r, cur, ctx)
        with col, st.container(border=True, key=("panel_cardtop" if i == best_fit else f"panel_card{i}")):
            names_ = " → ".join(cname(c) for c in r.rotation.crops)
            st.markdown(f'<div class="fs-opt-h">{names_}</div>', unsafe_allow_html=True)
            top_tag = f' <span class="fs-tag top">{t("ui.best_fit")}</span>' if i == best_fit else ""
            if i == 0:
                st.markdown(f'<span class="fs-tag">{t("o.current")}</span>{top_tag}', unsafe_allow_html=True)
            else:
                rot = r.rotation
                st.markdown(f'<span class="fs-tag new">{t("ui.opt_n", n=i)}</span>{top_tag}', unsafe_allow_html=True)
                st.caption(t(f"rule.{rot.rule}", crop=cname(rot.added[0]) if rot.added else " → ".join(cname(c) for c in rot.crops),
                             old=cname(rot.removed[0]) if rot.removed else ""))
            fit = s["fit"]
            st.markdown(ui.score_block(fit["median"], t("o.fit_cap", short=t("fit.short"), lo=fit["p10"], hi=fit["p90"], d=fit["median_dry"],
                                                         n=fit["median_normal"], w=fit["median_wet"])), unsafe_allow_html=True)
            irr, cirr = s["irrigation_demand_mm"]["median"], ci["irrigation_demand_mm"]["median"]
            pct = t("o.vs_now", pct=100 * (irr - cirr) / cirr) if i and cirr else ""
            yl = s["yield_loss"]
            heat_lines = "".join(
                f'<div class="fs-line">{t("o.heat", crop=cname(pl.crop_id), n=s[f"heat_days_{j}"]["median"], thr=DB[pl.crop_id]["heat_thr_c"], p=s[f"heat_days_{j}"]["p90"])}</div>'
                for j, pl in enumerate(r.rotation.plantings) if DB[pl.crop_id]["season"] != "cover")
            st.markdown(f'<div class="fs-line">{t("o.irr", irr=irr, pct=pct)}</div>'
                        f'<div class="fs-line">{t("o.bare", d=r.rotation.bare_days_per_year())}</div>'
                        f'<div class="fs-line">{t("o.nitrogen", n=s["n_kg"]["median"])}</div>'
                        f'<div class="fs-line">{t("o.yield", m=yl["median"] * 100, p=yl["p90"] * 100)}</div>'
                        + (f'<div class="fs-line" style="color:var(--fs-muted);font-size:.78rem">{t("o.yield_low", sec=t("ui.sidebar_what"))}</div>' if yield_low else "") +
                        f'<div class="fs-side-h" style="margin-top:.8rem">{t("ui.heat_h")}</div>' + heat_lines, unsafe_allow_html=True)
            st.caption(t("o.heat_cap"))
            pchart(viz.fig_radar(r, cur, viz.color_for(i), S.lang), width="stretch", key=f"radar{i}")
            for key, items in (("ex.why", e.why), ("ex.evidence", e.evidence), ("ex.benefits", e.benefits + [t("ex.tradeoff", t=i18n.render(x, S.lang)) for x in e.tradeoffs]),
                               ("ex.gaps", e.gaps), ("ex.risks", e.risks)):
                with st.expander(t(key), expanded=(key == "ex.why")):
                    for it in items:
                        st.write("• " + i18n.render(it, S.lang))
    st.caption(t("o.radar_cap"))

# ------------------------------------------------------------------ view 3: glossary and data
if view == "glossary":
    ui.section(t("g.title"))
    for gid, *_ in GLOSSARY:
        with st.expander(t(f"gl.{gid}.t")):
            st.write(t(f"gl.{gid}.d"))
    ui.section(t("g.data"))
    nd_ok = ctx.ndvi is not None and ctx.ndvi.ok
    sm_ok = ctx.smap is not None and ctx.smap.ok
    srcs = pd.DataFrame([
        ["NASA POWER (MERRA-2, CERES-SYN)", t("g.power_for"), t("g.power_res"), "2001–2025", t("g.used")],
        ["ISRIC SoilGrids", t("g.soil_for"), "250 m", t("g.static"), t("g.soil_status")],
        ["MODIS NDVI (MOD13Q1)", t("g.ndvi_for"), t("g.res_ndvi"), ctx.ndvi.date_range if nd_ok else "–", t("g.ndvi_used") if nd_ok else t("g.ndvi_not")],
        ["SMAP", t("g.smap_for"), "~9 km", ctx.smap.date_range if sm_ok else "–", t("g.smap_used") if sm_ok else t("g.smap_not")],
        ["GPM IMERG / SRTM", t("g.other_for"), "10 km / 30 m", "–", t("g.not_yet")],
    ], columns=[t("g.col_source"), t("g.col_for"), t("g.col_res"), t("g.col_period"), t("g.col_status")])
    st.dataframe(srcs, hide_index=True, width="stretch")
    ui.section(t("g.versus"))
    st.write(t("g.versus_text"))
st.divider()
st.caption(t("footer"))
