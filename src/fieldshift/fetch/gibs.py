"""NASA GIBS (Global Imagery Browse Services) map layers: metadata only (the browser fetches the tiles itself).

For each layer we need, from the live WMTS capabilities document: the newest observation date, the tile matrix set (max zoom)
and the image format; and from NASA's published colormap XML: the legend colours and value range. Nothing is invented: if the
capabilities cannot be read (offline, server down) and no cached copy exists, the layer is reported as *unavailable* with a reason
and the map simply does not offer it.

Layers (all global coverage; the date is the newest GIBS offers, not a seasonal mean):
  ndvi    MODIS Terra NDVI, rolling 8-day, 250 m
  precip  GPM IMERG precipitation rate, ~10 km
  temp    MODIS Terra land surface temperature, 8-day daytime, 1 km (surface, not air, temperature)
  soil    SMAP L4 surface soil moisture, ~9 km (model analysis that assimilates SMAP data)
"""
from __future__ import annotations

import html
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests

from .base import CACHE_DIR

CAPS_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml"
TILE_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/{layer}/default/{date}/{tms}/{{z}}/{{y}}/{{x}}.{ext}"
TIMEOUT_S = 25
CACHE_TTL_S = 12 * 3600
LAYERS = {"ndvi": "MODIS_Terra_NDVI_8Day", "precip": "IMERG_Precipitation_Rate",
          "temp": "MODIS_Terra_L3_Land_Surface_Temp_8Day_Day", "soil": "SMAP_L4_Analyzed_Surface_Soil_Moisture"}
KELVIN_KEYS = {"temp"}          # legend values are in kelvin; shown in °C


@dataclass
class Legend:
    stops: list[tuple[int, int, int]]
    vmin: float | None
    vmax: float | None

    def css_gradient(self, n: int = 18) -> str:
        if not self.stops:
            return "none"
        idx = sorted({round(i * (len(self.stops) - 1) / (n - 1)) for i in range(n)}) if len(self.stops) > n else range(len(self.stops))
        pts = [self.stops[i] for i in idx]
        return "linear-gradient(to right," + ",".join(f"rgb{c} {100 * k / max(1, len(pts) - 1):.0f}%" for k, c in enumerate(pts)) + ")"


@dataclass
class GibsLayer:
    key: str
    layer_id: str
    date: str = ""
    tms: str = ""
    ext: str = "png"
    legend: Legend | None = None
    ok: bool = False
    reason: str = ""
    stale: bool = False

    @property
    def max_zoom(self) -> int:
        m = re.search(r"Level(\d+)", self.tms)
        return int(m.group(1)) if m else 6

    def tile_url(self) -> str:
        return TILE_URL.format(layer=self.layer_id, date=self.date, tms=self.tms, ext=self.ext)


# ---------------------------------------------------------------- parsing
def parse_capabilities(xml: str, layer_id: str) -> dict | None:
    """Pull date / tile matrix set / format / colormap URL for one layer out of the (large) capabilities text."""
    i = xml.find(f"<ows:Identifier>{layer_id}</ows:Identifier>")
    if i < 0:
        return None
    j, k = xml.rfind("<Layer>", 0, i), xml.find("</Layer>", i)
    block = xml[j:k]
    default = re.search(r"<Dimension>.*?<Default>([^<]*)</Default>", block, re.S)
    tms = re.search(r"<TileMatrixSet>([^<]*)</TileMatrixSet>", block)
    fmt = re.search(r"<Format>image/(png|jpeg)</Format>", block)
    cmap = None
    for tag in re.findall(r"<ows:Metadata\b[^>]*>", block):          # attribute order varies between server responses
        if "colormap/1.3" in tag:
            cmap = re.search(r"""xlink:href=["']([^"']*)["']""", tag)
            break
    if not (default and tms):
        return None
    return {"date": default.group(1), "tms": tms.group(1), "ext": "jpg" if fmt and fmt.group(1) == "jpeg" else "png",
            "colormap": cmap.group(1) if cmap else ""}


_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def parse_colormap(xml: str, kelvin: bool = False) -> Legend:
    """Legend colours and range from a GIBS colormap XML. Entries without a number in the tooltip (Fill, No Data) are skipped."""
    stops: list[tuple[int, int, int]] = []
    nums: list[float] = []
    for r, g, b, tip in re.findall(r'<LegendEntry rgb="(\d+),(\d+),(\d+)" tooltip="([^"]*)"', xml):
        found = _NUM.findall(html.unescape(tip))
        if not found:
            continue
        stops.append((int(r), int(g), int(b)))
        nums += [float(v) for v in found]
    if kelvin:
        nums = [v - 273.15 for v in nums]
    return Legend(stops, min(nums) if nums else None, max(nums) if nums else None)


# ---------------------------------------------------------------- fetching with a small disk cache
def _cache_path() -> Path:
    return Path(CACHE_DIR) / "gibs_layers.json"


def _read_cache() -> dict | None:
    try:
        return json.loads(_cache_path().read_text())
    except Exception:  # noqa: BLE001
        return None


def _from_record(key: str, rec: dict, stale: bool) -> GibsLayer:
    lg = rec.get("legend")
    return GibsLayer(key, LAYERS[key], rec["date"], rec["tms"], rec["ext"],
                     Legend([tuple(c) for c in lg["stops"]], lg["vmin"], lg["vmax"]) if lg else None, True, "", stale)


def load_layers(session=None, now: float | None = None) -> dict[str, GibsLayer]:
    """All four layers. Fresh cache (<12 h) -> used; otherwise fetch; fetch failure -> older cache marked stale, else unavailable."""
    now = time.time() if now is None else now
    cache = _read_cache()
    if cache and now - cache.get("fetched", 0) < CACHE_TTL_S and all(k in cache.get("layers", {}) for k in LAYERS):
        return {k: _from_record(k, cache["layers"][k], False) for k in LAYERS}
    get = (session or requests).get
    try:
        r = get(CAPS_URL, timeout=TIMEOUT_S)
        r.raise_for_status()
        xml = r.text
        recs: dict[str, dict] = {}
        for key, lid in LAYERS.items():
            info = parse_capabilities(xml, lid)
            if info is None:
                continue
            legend = None
            if info["colormap"]:
                try:
                    cr = get(info["colormap"], timeout=TIMEOUT_S)
                    cr.raise_for_status()
                    lg = parse_colormap(cr.text, key in KELVIN_KEYS)
                    legend = {"stops": lg.stops, "vmin": lg.vmin, "vmax": lg.vmax}
                except Exception:  # noqa: BLE001
                    legend = None
            recs[key] = {"date": info["date"], "tms": info["tms"], "ext": info["ext"], "legend": legend}
        out = {}
        for key in LAYERS:
            out[key] = _from_record(key, recs[key], False) if key in recs else GibsLayer(key, LAYERS[key], reason="not listed by NASA GIBS")
        try:
            _cache_path().parent.mkdir(parents=True, exist_ok=True)
            _cache_path().write_text(json.dumps({"fetched": now, "layers": recs}))
        except OSError:
            pass
        return out
    except Exception as e:  # noqa: BLE001
        reason = f"NASA GIBS could not be reached ({type(e).__name__})"
        if cache and cache.get("layers"):
            return {k: _from_record(k, cache["layers"][k], True) if k in cache["layers"] else GibsLayer(k, LAYERS[k], reason=reason) for k in LAYERS}
        return {k: GibsLayer(k, LAYERS[k], reason=reason) for k in LAYERS}
