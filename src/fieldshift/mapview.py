"""Agricultural map (Leaflet through folium): basemaps + NASA GIBS data layers + a legend / source panel.

Design choices
- Layer switching is done in the browser (Leaflet layer control + a few lines of JS), so changing a layer never reruns the Streamlit
  script and pan/zoom stay smooth. The user's basemap / data-layer choice is remembered in the browser (localStorage, best effort).
- Tiles are requested by the browser straight from the providers; this module only builds URLs from verified metadata.
- Data layers shown: only those GIBS reports. Unavailable layers are not drawn; the caller lists them with the reason.
- No field boundary is drawn: the project has no real boundary geometry for any field (only points).
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

import folium
from branca.element import MacroElement, Template

from .fetch.gibs import GibsLayer
from .i18n import tr

FOREST = "#2F6B45"
BASEMAPS = {
    "sat": dict(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", native=18,
                attr="Imagery © Esri, Maxar, Earthstar Geographics and the GIS User Community"),
    "street": dict(url="https://tile.openstreetmap.org/{z}/{x}/{y}.png", native=19, attr="© OpenStreetMap contributors"),
    "terrain": dict(url="https://tile.opentopomap.org/{z}/{x}/{y}.png", native=17,
                    attr="Map data © OpenStreetMap contributors, SRTM | Style © OpenTopoMap (CC-BY-SA)"),
}
GIBS_ATTR = "NASA GIBS / EOSDIS"
UNITS = {"ndvi": "", "precip": "mm/h", "temp": "°C", "soil": "m³/m³"}

CSS = """<style>
.leaflet-container{font-family:Inter,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;}
.leaflet-control-attribution{font-size:10px !important; background:rgba(255,255,255,.8) !important;}
.leaflet-control-scale-line{font-size:10px;}
.leaflet-control-layers{border:1px solid #E3DFD3 !important; border-radius:8px !important; box-shadow:none !important;}
.leaflet-control-layers-expanded{padding:8px 12px !important; font-size:13px; color:#232623;}
.leaflet-control-layers-separator{margin:6px 0 !important;}
.fs-maplegend{background:rgba(255,255,255,.94); border:1px solid #E3DFD3; border-radius:8px; padding:8px 11px; width:225px; font-size:11.5px; line-height:1.35; color:#232623;}
.fs-maplegend b{font-size:12.5px;}
.fs-maplegend .bar{height:9px; border-radius:3px; margin:6px 0 2px; border:1px solid rgba(0,0,0,.08);}
.fs-maplegend .rng{display:flex; justify-content:space-between; color:#4a4e46; font-variant-numeric:tabular-nums;}
.fs-maplegend .src{color:#6B6F66; margin-top:5px;}
.fs-maplegend .st{margin-top:4px; font-weight:600;}
.fs-maplegend .st.err{color:#8A5313;} .fs-maplegend .st.ok{color:#234E35;}
.fs-maplegend .note{color:#6B6F66; margin-top:3px;}
.leaflet-top{z-index:1001 !important;}
@media (max-width: 480px){.fs-maplegend{width:185px; padding:6px 8px;} .fs-maplegend .note{display:none;} .fs-maplegend .src{font-size:10.5px;}}
</style>"""


class _Behaviour(MacroElement):
    """Exclusive data layers, legend / source panel, loading and error states, remembered choices."""
    _template = Template("{% macro script(this, kwargs) %}{{ this.js }}{% endmacro %}")

    def __init__(self, js: str):
        super().__init__()
        self._name = "FieldShiftBehaviour"
        self.js = js


def _legend_html(layer: GibsLayer, key: str, labels: dict) -> dict:
    lg = layer.legend
    unit = UNITS.get(key, "")
    if lg and lg.vmin is not None and lg.vmax is not None:
        fmt = (lambda v: f"{v:.2f}") if key in ("ndvi", "soil") else (lambda v: f"{v:.0f}" if abs(v) >= 10 else f"{v:.1f}")
        lo, hi = f"{fmt(lg.vmin)}", f"{fmt(lg.vmax)} {unit}".strip()
        bar = lg.css_gradient()
    else:
        lo = hi = ""
        bar = "none"
    return {"title": labels["title"], "bar": bar, "lo": lo, "hi": hi, "src": labels["src"], "date": layer.date + (" *" if layer.stale else ""),
            "note": labels["note"], "asof": labels.get("asof", "") if layer.stale else ""}


LEAFLET_VERSION = "1.9.3"
LEAFLET_CDN = f"https://cdn.jsdelivr.net/npm/leaflet@{LEAFLET_VERSION}/dist"
LEAFLET_LOCAL = "/app/static/leaflet"        # served by Streamlit when `server.enableStaticServing` is on (see .streamlit/config.toml)
STATIC_DIR = Path(__file__).resolve().parents[2] / "static" / "leaflet"


def local_assets_available() -> bool:
    """True if the vendored Leaflet exists and Streamlit serves ./static; otherwise the map falls back to the CDN."""
    try:
        import streamlit as st
        return (STATIC_DIR / "leaflet.js").exists() and bool(st.get_option("server.enableStaticServing"))
    except Exception:  # noqa: BLE001
        return False


def resources(local: bool) -> tuple[list, list]:
    """(default_js, default_css) for the map. streamlit-folium loads exactly these, one after another, before drawing the map.
    The stock bundle also fetches jQuery, Bootstrap, Font Awesome and awesome-markers from CDNs; none is used here and they were
    most of the time between "page ready" and "map visible"."""
    base = LEAFLET_LOCAL if local else LEAFLET_CDN
    return [("leaflet", f"{base}/leaflet.js")], [("leaflet_css", f"{base}/leaflet.css")]


def build_map(lat: float, lon: float, layers: dict[str, GibsLayer], lang: str = "en", zoom: int = 7, tooltip: str = "",
              local_assets: bool = False) -> folium.Map:
    m = folium.Map(location=[lat, lon], zoom_start=zoom, tiles=None, control_scale=True, max_zoom=13, prefer_canvas=True)
    m.default_js, m.default_css = resources(local_assets)
    m.get_root().header.add_child(folium.Element(CSS))

    base_names, base_vars = {}, {}
    for i, (key, b) in enumerate(BASEMAPS.items()):
        name = tr(f"map.base_{key}", lang)
        tl = folium.TileLayer(tiles=b["url"], attr=b["attr"], name=name, overlay=False, control=True, show=(i == 0),
                              max_native_zoom=b["native"], max_zoom=13)
        tl.add_to(m)
        base_names[key], base_vars[name] = name, tl.get_name()

    data_vars, info = {}, {}
    for key, layer in layers.items():
        if not layer.ok:
            continue
        name = tr(f"map.layer_{key}", lang)
        tl = folium.TileLayer(tiles=layer.tile_url(), attr=GIBS_ATTR, name=name, overlay=True, control=True, show=False, opacity=0.78,
                              max_native_zoom=layer.max_zoom, max_zoom=13)
        tl.add_to(m)
        data_vars[name] = tl.get_name()
        info[name] = _legend_html(layer, key, {"title": tr(f"map.title_{key}", lang), "src": tr(f"map.src_{key}", lang),
                                               "note": tr(f"map.note_{key}", lang),
                                               "asof": tr("map.asof", lang, d=layer.as_of or "?")})

    folium.CircleMarker([lat, lon], radius=8, color="#FFFFFF", weight=3, fill=True, fill_color=FOREST, fill_opacity=1,
                        tooltip=tooltip or None).add_to(m)
    lc = folium.LayerControl(collapsed=True, position="topright")
    lc.add_to(m)

    text = {k: tr(f"map.{k}", lang) for k in ("loading", "loaded", "tile_error", "source", "date", "stale")}
    js = f"""
(function() {{
  var map = {m.get_name()};
  var lc = window["{lc.get_name()}"];
  var bases = {json.dumps(base_vars)};   // display name -> layer variable name (resolved below)
  var data = {json.dumps(data_vars)};
  var info = {json.dumps(info)};
  var T = {json.dumps(text)};
  var resolve = function(o) {{ var r = {{}}; Object.keys(o).forEach(function(k) {{ r[k] = window[o[k]]; }}); return r; }};
  var B = resolve(bases), D = resolve(data);
  window.__fs = {{B: B, D: D, map: map}};
  var panel = L.control({{position: 'bottomleft'}});
  panel.onAdd = function() {{ this._d = L.DomUtil.create('div', 'fs-maplegend'); this._d.style.display = 'none'; return this._d; }};
  panel.addTo(map);
  var store = {{ get: function(k) {{ try {{ return window.localStorage.getItem(k); }} catch (e) {{ return null; }} }},
                set: function(k, v) {{ try {{ if (v === null) window.localStorage.removeItem(k); else window.localStorage.setItem(k, v); }} catch (e) {{}} }} }};
  var active = null, errs = 0;
  function esc(s) {{ var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }}
  function render(name, status, cls) {{
    var i = info[name]; var d = panel._d;
    if (!i) {{ d.style.display = 'none'; return; }}
    var rng = i.bar !== 'none' ? '<div class="bar" style="background:' + i.bar + '"></div><div class="rng"><span>' + esc(i.lo) + '</span><span>' + esc(i.hi) + '</span></div>' : '';
    d.innerHTML = '<b>' + esc(i.title) + '</b>' + rng + '<div class="src">' + esc(T.source) + ': ' + esc(i.src) + '<br>' + esc(T.date) + ': ' + esc(i.date) + '</div>' +
      '<div class="note">' + esc(i.note) + '</div>' + (i.asof ? '<div class="note">' + esc(i.asof) + '</div>' : '') + (status ? '<div class="st ' + (cls || '') + '">' + esc(status) + '</div>' : '');
    d.style.display = 'block';
  }}
  function activate(name) {{
    active = name; errs = 0; var l = D[name];
    render(name, T.loading, '');
    if (l._fsLoad) {{ l.off('load', l._fsLoad); l.off('tileerror', l._fsErr); }}
    l._fsLoad = function() {{ if (active === name) render(name, errs ? T.tile_error : T.loaded, errs ? 'err' : 'ok'); }};
    l._fsErr = function() {{ errs += 1; if (active === name) render(name, T.tile_error, 'err'); }};
    l.on('load', l._fsLoad); l.on('tileerror', l._fsErr);
  }}
  L.DomEvent.disableClickPropagation(panel._d);
  // Leaflet re-adds a layer removed during the same click (its checkbox is still ticked), so the exclusive switch runs after the click,
  // keeping the layer the user actually clicked.
  var lastClick = null;
  if (lc && lc._container) lc._container.addEventListener('click', function(ev) {{
    var lab = ev.target.closest && ev.target.closest('label'); if (lab) lastClick = lab.textContent.trim();
  }}, true);
  map.on('overlayadd', function(e) {{
    if (!D[e.name]) return;
    setTimeout(function() {{
      var keep = (lastClick && D[lastClick] && map.hasLayer(D[lastClick])) ? lastClick : e.name;
      Object.keys(D).forEach(function(k) {{ if (k !== keep && map.hasLayer(D[k])) map.removeLayer(D[k]); }});
      activate(keep); store.set('fs_data', keep);
    }}, 0);
  }});
  map.on('overlayremove', function(e) {{
    if (!D[e.name]) return;
    if (active === e.name) {{ active = null; panel._d.style.display = 'none'; }}
    var any = Object.keys(D).some(function(k) {{ return map.hasLayer(D[k]); }});
    if (!any) store.set('fs_data', null);
  }});
  map.on('baselayerchange', function(e) {{ store.set('fs_base', e.name); }});
  // restore the remembered choices (the page reruns, e.g. when the field is moved, and rebuilds the map)
  var b = store.get('fs_base'); if (b && B[b] && !map.hasLayer(B[b])) {{ Object.keys(B).forEach(function(k) {{ if (map.hasLayer(B[k])) map.removeLayer(B[k]); }}); B[b].addTo(map); }}
  var dname = store.get('fs_data'); if (dname && D[dname]) {{ D[dname].addTo(map); }}
}})();
"""
    m.add_child(_Behaviour(js))
    return m


def layer_status(layers: dict[str, GibsLayer], lang: str = "en") -> list[tuple[str, str, str, bool]]:
    """(name, date text, tooltip, available) per layer for the caption under the map."""
    out = []
    for key, layer in layers.items():
        name = tr(f"map.short_{key}", lang)
        if layer.ok:
            out.append((name, layer.date + (" *" if layer.stale else ""), tr(f"map.title_{key}", lang), True))
        else:
            out.append((name, tr("map.unavailable", lang), escape(layer.reason), False))
    return out
