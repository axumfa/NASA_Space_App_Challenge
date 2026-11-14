"""Project paths and demo field definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "data" / "cache"
RAW_DIR = ROOT / "data" / "raw"
MANUAL_DIR = ROOT / "data" / "manual"


@dataclass(frozen=True)
class Field:
    key: str
    name: str
    lat: float
    lon: float
    rotation: tuple[str, ...]  # current rotation, crop ids in sequence (one per season slot)
    country: str = ""


DEMO_FIELDS: dict[str, Field] = {
    "fergana": Field("fergana", "Fergana Valley, Uzbekistan", 40.40, 71.78,
                     ("winter_wheat", "cotton"), "UZ"),
    "kansas": Field("kansas", "Central Kansas, USA", 38.50, -98.50,
                    ("maize", "soybean"), "US"),
}
