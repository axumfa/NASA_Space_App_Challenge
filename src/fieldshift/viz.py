"""Plotly figures for the Streamlit app (consistent farmer-friendly palette)."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .compare import FIT_SHORT
from .crops import load_crops
from .scoring import PRIORITIES

C = {"rain": "#2b7bba", "et0": "#e07b00", "frost": "#5b8bd6", "heat": "#d64545", "current": "#7a6a53",
     "alt": ["#2e8b57", "#1b9aaa", "#8e6bbf", "#c28f2c"], "bare": "rgba(214,69,69,0.18)", "ink": "#2b2b2b"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LAYOUT = dict(font=dict(size=15, color=C["ink"]), margin=dict(l=10, r=10, t=50, b=10),
              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=-0.2))
LABEL = {"water_saving": "Water saving", "soil_om": "Soil organic matter", "nitrogen": "Nitrogen fixing",
         "erosion": "Erosion reduction", "forage": "Forage value", "income": "Market / income"}


def color_for(i: int) -> str:
    return C["current"] if i == 0 else C["alt"][(i - 1) % len(C["alt"])]


def doy_to_date(doy: float) -> str:
    return "n/a" if pd.isna(doy) else (dt.date(2001, 1, 1) + dt.timedelta(days=int(doy) - 1)).strftime("%b %d")


def fig_water_balance(clim: pd.DataFrame) -> go.Figure:
    f = go.Figure()
    f.add_bar(x=MONTHS, y=clim["PRECTOTCORR"], name="Rain (mm)", marker_color=C["rain"])
    f.add_scatter(x=MONTHS, y=clim["ET0"], name="Water the air can take (ET0, mm)", mode="lines+markers",
                  line=dict(color=C["et0"], width=4))
    f.update_layout(title="Rain vs. water demand, average month", yaxis_title="mm per month", **LAYOUT)
    return f


def fig_frost_heat(week_prob: pd.Series, heat_by_month: pd.Series, heat_thr: float = 35.0) -> go.Figure:
    f = make_subplots(rows=2, cols=1, vertical_spacing=0.22,
                      subplot_titles=("Chance of a frost (≤ 0 °C) in each week, share of years",
                                      f"Hot days (max ≥ {heat_thr:.0f} °C) per month, average year"))
    wk = week_prob.reindex(range(1, 53), fill_value=0)
    f.add_bar(x=wk.index, y=wk.values * 100, marker_color=C["frost"], showlegend=False, row=1, col=1)
    f.update_xaxes(title_text="week of year", row=1, col=1)
    f.update_yaxes(title_text="% of years", row=1, col=1, range=[0, 100])
    f.add_bar(x=MONTHS, y=heat_by_month.reindex(range(1, 13), fill_value=0).values, marker_color=C["heat"],
              showlegend=False, row=2, col=1)
    f.update_yaxes(title_text="days", row=2, col=1)
    f.update_layout(height=520, **{**LAYOUT, "margin": dict(l=10, r=10, t=60, b=10)})
    return f


def fig_calendar(rotation, title: str = "Crop calendar: green = crop in the field, red = bare soil") -> go.Figure:
    db = load_crops()
    total = 365 * rotation.cycle_years
    f = go.Figure()
    for s, n in rotation.bare_windows():
        for a, b in ((s, min(s + n, total)), (0, s + n - total) if s + n > total else (0, 0)):
            if b > a:
                f.add_vrect(x0=a, x1=b, fillcolor=C["bare"], line_width=0, layer="below")
    for i, p in enumerate(rotation.plantings):
        c = db[p.crop_id]
        for a, b in ((p.start % total, min(p.start % total + p.days, total)),
                     (0, p.start % total + p.days - total) if p.start % total + p.days > total else (0, 0)):
            if b > a:
                f.add_bar(y=[c["name"]], x=[b - a], base=[a], orientation="h", marker_color=C["alt"][0],
                          opacity=0.85, showlegend=False, hovertemplate=f"{c['name']}<extra></extra>")
    ticks = [m * 30.4 + y * 365 for y in range(rotation.cycle_years) for m in (0, 3, 6, 9)]
    f.update_xaxes(tickvals=ticks, ticktext=[f"{MONTHS[m]} Y{y + 1}" for y in range(rotation.cycle_years) for m in (0, 3, 6, 9)],
                   range=[0, total])
    f.update_layout(title=title, height=170 + 50 * len(rotation.plantings), barmode="overlay", **LAYOUT)
    return f


def fig_radar(res, current, color: str) -> go.Figure:
    keys = [m for m in PRIORITIES]
    short = {"water_saving": "Water", "soil_om": "Soil humus", "nitrogen": "Nitrogen", "erosion": "Erosion", "forage": "Forage", "income": "Income"}
    labels = [short[m] for m in keys]
    f = go.Figure()
    cur = [current.summary[f"norm_{m}"]["median"] for m in keys]
    f.add_scatterpolar(r=cur + cur[:1], theta=labels + labels[:1], name="Current", line=dict(color=C["current"], dash="dot"))
    if res is not current:
        v = [res.summary[f"norm_{m}"]["median"] for m in keys]
        f.add_scatterpolar(r=v + v[:1], theta=labels + labels[:1], name="This option", fill="toself",
                           line=dict(color=color), opacity=0.8)
    f.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="rgba(128,128,128,0.35)"),
                               angularaxis=dict(tickfont=dict(size=12), gridcolor="rgba(128,128,128,0.35)")), height=300,
                    **{**LAYOUT, "margin": dict(l=55, r=55, t=20, b=30), "legend": dict(orientation="h", y=-0.15)})
    return f


def fig_fit_by_year_type(display: list) -> go.Figure:
    f = go.Figure()
    for i, r in enumerate(display):
        sc = r.scores
        med, lo, hi = [], [], []
        for cls in ("dry", "normal", "wet"):
            g = sc.loc[sc["year_class"] == cls, "fit"]
            med.append(g.median()); lo.append(g.median() - g.quantile(.1)); hi.append(g.quantile(.9) - g.median())
        f.add_bar(x=["Dry years (high water need)", "Normal years", "Wet years (low water need)"], y=med,
                  name=r.rotation.key.replace("_", " "), marker_color=color_for(i),
                  error_y=dict(type="data", symmetric=False, array=hi, arrayminus=lo))
    f.update_layout(title=f"{FIT_SHORT} by type of year (bars = typical, whiskers = 10th–90th percentile)",
                    yaxis=dict(title="relative score", range=[0, 105]), barmode="group", height=380, **LAYOUT)
    return f


def fig_ndvi(curve: pd.DataFrame, windows: list, threshold: float) -> go.Figure:
    f = go.Figure()
    for st_, n in windows:
        f.add_vrect(x0=st_, x1=min(st_ + n, 366), fillcolor=C["bare"], line_width=0, layer="below")
        if st_ + n > 366:
            f.add_vrect(x0=0, x1=st_ + n - 366, fillcolor=C["bare"], line_width=0, layer="below")
    f.add_scatter(x=curve["doy"], y=curve["p75"], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip")
    f.add_scatter(x=curve["doy"], y=curve["p25"], mode="lines", line=dict(width=0), fill="tonexty",
                  fillcolor="rgba(46,139,87,0.25)", name="typical spread (25–75%)")
    f.add_scatter(x=curve["doy"], y=curve["median"], mode="lines+markers", line=dict(color="#2e8b57", width=4), name="greenness (NDVI), median year")
    f.add_hline(y=threshold, line_dash="dot", line_color=C["heat"], annotation_text="bare soil below this")
    f.update_xaxes(tickvals=[m * 30.4 + 15 for m in range(12)], ticktext=MONTHS, range=[0, 366])
    f.update_layout(title="Satellite greenness through the year (red = typically bare)", yaxis_title="NDVI (0 bare – 0.8 dense crop)", **LAYOUT)
    return f


def fig_soil_anomaly(z: pd.DataFrame) -> go.Figure:
    m = z["z"].groupby(level="month").mean()
    f = go.Figure(go.Bar(x=[MONTHS[i - 1] for i in m.index], y=m.values, marker_color=[C["heat"] if v < 0 else C["rain"] for v in m.values]))
    f.update_layout(title="Satellite soil moisture: wetter (+) or drier (−) than normal, average by month", yaxis_title="z-score", **LAYOUT)
    return f
