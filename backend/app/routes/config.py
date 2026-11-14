"""Configuration and catalog endpoints."""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is on path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fastapi import APIRouter
from fieldshift.config import DEMO_FIELDS
from fieldshift.crops import load_crops
from fieldshift.i18n import GLOSSARY, S as TRANSLATIONS
from fieldshift.scoring import PRIORITIES, PROFILES

from ..schemas import ConfigResponse, DemoFieldItem

router = APIRouter(prefix="/api", tags=["config"])


@router.get("/config", response_model=ConfigResponse)
def get_config():
    demo_dict = {
        k: DemoFieldItem(
            key=f.key,
            name=f.name,
            lat=f.lat,
            lon=f.lon,
            rotation=list(f.rotation),
            country=f.country,
            preset=f.preset,
            satellite=f.satellite,
        )
        for k, f in DEMO_FIELDS.items()
    }
    prof_dict = {k: v.as_dict() for k, v in PROFILES.items()}
    return ConfigResponse(
        demo_fields=demo_dict,
        crops=load_crops(),
        profiles=prof_dict,
        priorities=list(PRIORITIES),
        translations=TRANSLATIONS,
        glossary=[list(g) for g in GLOSSARY],
    )


@router.get("/presets", response_model=list[DemoFieldItem])
def get_presets():
    return [
        DemoFieldItem(
            key=f.key,
            name=f.name,
            lat=f.lat,
            lon=f.lon,
            rotation=list(f.rotation),
            country=f.country,
            preset=f.preset,
            satellite=f.satellite,
        )
        for f in DEMO_FIELDS.values()
    ]
