"""Project paths and demo field definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "data" / "cache"                 # live downloads (git-ignored)
DEMO_CACHE_DIR = ROOT / "data" / "demo_cache"       # committed copies for the two demo fields (read first)
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


# The demo caches hold 2001-2025. Pin the end year for the demo fields so a fresh clone made in any later
# year still finds its cache key (the key includes the end year) and works with no network.
DEMO_END_YEAR = 2025


def end_year_for(lat: float, lon: float, today_year: int | None = None) -> int:
    """Last year of POWER data to request: pinned for the demo fields, else the last full calendar year."""
    import datetime as dt
    if any(abs(f.lat - lat) < 0.005 and abs(f.lon - lon) < 0.005 for f in DEMO_FIELDS.values()):
        return DEMO_END_YEAR
    return (today_year or dt.date.today().year) - 1
