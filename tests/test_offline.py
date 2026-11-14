"""A fresh clone must run the two demo fields with no network and an empty live cache."""
import pytest

from fieldshift.config import DEMO_END_YEAR, DEMO_FIELDS, end_year_for


def test_end_year_pinned_for_demo_fields_only():
    f = DEMO_FIELDS["fergana"]
    assert end_year_for(f.lat, f.lon, today_year=2031) == DEMO_END_YEAR
    assert end_year_for(10.0, 10.0, today_year=2031) == 2030


def test_demo_fields_load_from_committed_cache_without_network(tmp_path, monkeypatch):
    import requests
    from fieldshift.fetch import base, soil
    from fieldshift.pipeline import build_context

    monkeypatch.setattr(base, "CACHE_DIR", tmp_path)            # empty live cache, like a fresh clone

    def no_network(*a, **k):
        raise AssertionError("network was used")
    monkeypatch.setattr(requests, "get", no_network)
    for f in DEMO_FIELDS.values():
        ctx = build_context(f.lat, f.lon)                       # raises if POWER had to be downloaded
        assert ctx.annual.index.min() == 2001 and ctx.annual.index.max() == DEMO_END_YEAR
    assert soil.fetch_soil(38.50, -98.50, "kansas").ok          # SoilGrids REST value stored in the demo cache


def test_filled_manual_soil_file_overrides_cache(tmp_path, monkeypatch):
    import json
    from fieldshift.fetch import soil
    (tmp_path / "soil_kansas.json").write_text(json.dumps({"clay_pct": 20, "sand_pct": 40, "silt_pct": 40, "soc_g_kg": 9}))
    monkeypatch.setattr(soil, "MANUAL_DIR", tmp_path)
    r = soil.fetch_soil(38.50, -98.50, "kansas")
    assert r.ok and r.meta["tier"] == "manual estimate" and "read manually" in r.source
