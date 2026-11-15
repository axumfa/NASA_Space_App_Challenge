"""NASA GIBS satellite layers endpoint."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fastapi import APIRouter
from fieldshift.fetch import gibs

from ..schemas import GibsLayerItem

router = APIRouter(prefix="/api/layers", tags=["layers"])
UNITS = {"ndvi": "", "precip": "mm/h", "temp": "°C", "soil": "m³/m³"}


@router.get("/gibs", response_model=list[GibsLayerItem])
def get_gibs_layers():
    layers = gibs.load_cached()
    gibs.refresh_in_background()

    out: list[GibsLayerItem] = []
    for key, l in layers.items():
        grad = l.legend.css_gradient() if (l.ok and l.legend) else "none"
        vmin = l.legend.vmin if (l.ok and l.legend) else None
        vmax = l.legend.vmax if (l.ok and l.legend) else None
        template = (
            gibs.TILE_URL.format(layer=l.layer_id, date=l.date, tms=l.tms, ext=l.ext)
            if l.ok
            else ""
        )
        out.append(
            GibsLayerItem(
                key=key,
                layer_id=l.layer_id,
                date=l.date or "",
                tms=l.tms or "",
                tile_template=template,
                css_gradient=grad,
                vmin=vmin,
                vmax=vmax,
                unit=UNITS.get(key, ""),
                max_zoom=l.max_zoom,
                ok=bool(l.ok),
                message=str(l.reason or ""),
            )
        )
    return out
