"""ISRIC SoilGrids point values (0-30 cm), three tiers: REST -> COG/VRT via rasterio -> manual JSON.

Output units: clay/sand/silt %, soc g/kg, phh2o pH, bdod kg/dm3. Depth-weighted over 0-5/5-15/15-30 cm.
Manual file: data/manual/soil_<field>.json with keys clay_pct, sand_pct, silt_pct, soc_g_kg, phh2o, bdod_kg_dm3.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

from ..config import MANUAL_DIR
from .base import FetchResult, cache_key, read_json_cache, write_json_cache

REST_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
COG_URL = "https://files.isric.org/soilgrids/latest/data/{p}/{p}_{d}_mean.vrt"
PROPS = ["clay", "sand", "silt", "soc", "phh2o", "bdod"]
DEPTHS = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}      # label -> thickness (cm) for weighting
D_FACTOR = {"clay": 10, "sand": 10, "silt": 10, "soc": 10, "phh2o": 10, "bdod": 100}
OUT_NAME = {"clay": "clay_pct", "sand": "sand_pct", "silt": "silt_pct", "soc": "soc_g_kg",
            "phh2o": "phh2o", "bdod": "bdod_kg_dm3"}
TIMEOUT_S = 10


def _weighted(values: dict[str, float]) -> float:
    tot = sum(DEPTHS[d] for d in values)
    return sum(v * DEPTHS[d] for d, v in values.items()) / tot


def parse_rest(payload: dict) -> dict[str, float]:
    """SoilGrids REST JSON -> {clay_pct: ..}, converting mapped units with each layer's d_factor."""
    out: dict[str, float] = {}
    for layer in payload["properties"]["layers"]:
        name, d = layer["name"], layer["unit_measure"]["d_factor"]
        vals = {x["label"]: x["values"]["mean"] / d for x in layer["depths"]
                if x["label"] in DEPTHS and x["values"].get("mean") is not None}
        if vals:
            out[OUT_NAME[name]] = _weighted(vals)
    return out


def _via_rest(lat: float, lon: float) -> dict[str, float]:
    q = [("lon", lon), ("lat", lat), ("value", "mean")]
    q += [("property", p) for p in PROPS] + [("depth", d) for d in DEPTHS]
    r = requests.get(REST_URL, params=q, timeout=TIMEOUT_S)
    r.raise_for_status()
    return parse_rest(r.json())


def _via_cog(lat: float, lon: float) -> dict[str, float]:
    import rasterio  # lazy: heavy optional dependency
    from rasterio.warp import transform
    out: dict[str, float] = {}
    with rasterio.Env(GDAL_HTTP_TIMEOUT=str(TIMEOUT_S), GDAL_HTTP_MAX_RETRY="1",
                      GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".vrt,.tif"):
        vals: dict[str, dict[str, float]] = {p: {} for p in PROPS}
        for p in PROPS:
            for d in DEPTHS:
                with rasterio.open(COG_URL.format(p=p, d=d)) as ds:
                    x, y = transform("EPSG:4326", ds.crs, [lon], [lat])
                    v = next(ds.sample([(x[0], y[0])]))[0]
                    if ds.nodata is None or v != ds.nodata:
                        vals[p][d] = float(v) / D_FACTOR[p]
    for p, v in vals.items():
        if v:
            out[OUT_NAME[p]] = _weighted(v)
    return out


def _via_manual(field_key: str | None) -> dict[str, float]:
    if not field_key:
        raise FileNotFoundError("no field key for manual soil file")
    f = Path(MANUAL_DIR) / f"soil_{field_key}.json"
    d = json.loads(f.read_text())
    return {k: float(d[k]) for k in OUT_NAME.values() if k in d}


def texture_class(clay: float, sand: float, silt: float) -> str:
    """Coarse USDA-style texture label from percentages."""
    if clay >= 40:
        return "clay"
    if sand >= 70 and clay < 15:
        return "sandy"
    if silt >= 50 and clay < 27:
        return "silty (loam)"
    if clay >= 27:
        return "clay loam"
    return "loam"


def fetch_soil(lat: float, lon: float, field_key: str | None = None) -> FetchResult:
    key = cache_key("soil", lat, lon)
    cached = read_json_cache(key)
    if cached is not None:
        c = cached
        return _result(c["values"], c["tier"], "from cache")
    errors: list[str] = []
    for tier, fn in (("SoilGrids REST", lambda: _via_rest(lat, lon)),
                     ("SoilGrids COG", lambda: _via_cog(lat, lon)),
                     ("manual estimate", lambda: _via_manual(field_key))):
        try:
            vals = fn()
            if vals:
                if tier != "manual estimate":   # never cache a hand-entered file; it is read live
                    write_json_cache(key, {"values": vals, "tier": tier})
                return _result(vals, tier, "; ".join(errors) or "live")
            errors.append(f"{tier} returned no data")
        except Exception as e:  # noqa: BLE001
            errors.append(f"{tier} failed ({type(e).__name__})")
    return FetchResult.failed("SoilGrids", "; ".join(errors))


def _result(vals: dict[str, float], tier: str, msg: str) -> FetchResult:
    df = pd.DataFrame([vals])
    if {"clay_pct", "sand_pct", "silt_pct"} <= set(vals):
        df["texture"] = texture_class(vals["clay_pct"], vals["sand_pct"], vals["silt_pct"])
    res = "250 m, 0-30 cm weighted" if tier.startswith("SoilGrids") else "manual point estimate"
    return FetchResult(f"Soil: {tier}", df, True, res, "static", msg, {"tier": tier})
