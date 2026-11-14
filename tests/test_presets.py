import pytest

from fieldshift.config import DEMO_FIELDS, field_at
from fieldshift.pipeline import build_context

PRESETS = [k for k, f in DEMO_FIELDS.items() if f.preset]


def test_three_regional_presets_exist_without_satellite_data():
    assert set(PRESETS) == {"karakalpakstan", "bukhara", "samarkand"}
    assert all(not DEMO_FIELDS[k].satellite and DEMO_FIELDS[k].country == "UZ" for k in PRESETS)
    assert DEMO_FIELDS["fergana"].satellite and DEMO_FIELDS["kansas"].satellite


@pytest.mark.parametrize("key", PRESETS)
def test_preset_runs_offline_and_gaps_say_no_satellite_requested(key, tmp_path, monkeypatch):
    import requests
    from fieldshift.fetch import base
    monkeypatch.setattr(base, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(requests, "get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network used")))
    f = DEMO_FIELDS[key]
    ctx = build_context(f.lat, f.lon)
    assert ctx.annual.index.max() == 2025 and ctx.ndvi is not None and not ctx.ndvi.ok and not ctx.smap.ok
    gaps = " ".join(ctx.gaps)
    assert "no satellite NDVI/SMAP point has been requested for this preset" in gaps and ctx.ndvi_curve is None
    assert ctx.root_wetness is not None                         # POWER root-zone wetness stands in for SMAP


def test_field_at_matches_only_exact_demo_points():
    f = DEMO_FIELDS["bukhara"]
    assert field_at(f.lat, f.lon).key == "bukhara" and field_at(f.lat + 0.2, f.lon) is None
