"""Download and cache everything the demo needs (run once with internet; afterwards the demo works offline).

Usage: python scripts/prewarm.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.fetch.appeears import load_ndvi, load_smap  # noqa: E402
from fieldshift.fetch.power import fetch_power  # noqa: E402
from fieldshift.fetch.soil import fetch_soil  # noqa: E402


def main() -> None:
    end = dt.date.today().year - 1
    for key, f in DEMO_FIELDS.items():
        print(f"== {f.name}")
        for r in (fetch_power(f.lat, f.lon, 2001, end), fetch_soil(f.lat, f.lon, key),
                  load_ndvi(f.lat, f.lon), load_smap(f.lat, f.lon)):
            print(f"  {'OK  ' if r.ok else 'MISS'} {r.source}: {r.message[:110]}")


if __name__ == "__main__":
    main()
