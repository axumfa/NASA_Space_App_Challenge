import pytest

from fieldshift.config import DEMO_FIELDS, field_at
from fieldshift.pipeline import build_context

PRESETS = [k for k, f in DEMO_FIELDS.items() if f.preset]


def test_three_regional_presets_exist_and_only_karakalpakstan_has_satellite_data():
    assert set(PRESETS) == {"karakalpakstan", "bukhara", "samarkand"}
    assert all(DEMO_FIELDS[k].country == "UZ" for k in PRESETS)
    assert [k for k in PRESETS if DEMO_FIELDS[k].satellite] == ["karakalpakstan"]    # its AppEEARS point returned cropland NDVI and SMAP
    assert DEMO_FIELDS["fergana"].satellite and DEMO_FIELDS["kansas"].satellite


@pytest.mark.parametrize("key", ["bukhara", "samarkand"])
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


def test_karakalpakstan_gap_note_says_rice_is_common_and_not_modelled():
    f = DEMO_FIELDS["karakalpakstan"]
    ctx = build_context(f.lat, f.lon)
    assert any("Rice is a common crop in Karakalpakstan and is not modelled" in g for g in ctx.gaps)
    other = DEMO_FIELDS["bukhara"]
    assert not any("Rice" in g for g in build_context(other.lat, other.lon).gaps)


def test_karakalpakstan_uses_the_committed_satellite_subset_offline(tmp_path, monkeypatch):
    import requests
    from fieldshift.fetch import base
    monkeypatch.setattr(base, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(requests, "get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network used")))
    f = DEMO_FIELDS["karakalpakstan"]
    ctx = build_context(f.lat, f.lon)
    assert ctx.ndvi.ok and ctx.smap.ok and ctx.ndvi_curve is not None and ctx.smap_anomaly is not None
    assert ctx.ndvi.meta["n_valid"] > 100 and not any("not been requested" in g for g in ctx.gaps)


def test_non_cropland_ndvi_is_rejected_with_a_gap_message(monkeypatch):
    import numpy as np
    import pandas as pd
    from fieldshift import pipeline
    from fieldshift.fetch.base import FetchResult
    idx = pd.date_range("2019-01-01", "2025-12-31", freq="16D")
    low = pd.DataFrame({"ndvi": 0.1 + 0.15 * np.sin(np.arange(len(idx)) / 5) ** 2}, index=idx)      # peaks ~0.25: bare ground / town edge
    res = FetchResult(source="MODIS NDVI", data=low, ok=True, message="", meta={"n_valid": len(idx), "n_total": len(idx)})
    monkeypatch.setattr(pipeline, "load_ndvi", lambda *a: res)
    assert pipeline.ndvi_cropland_peak(low["ndvi"]) < 0.3
    f = DEMO_FIELDS["fergana"]                                                                       # committed POWER cache: runs offline
    ctx = build_context(f.lat, f.lon)
    assert ctx.ndvi is not None and not ctx.ndvi.ok and ctx.ndvi_curve is None
    assert any("not clearly cropland" in g for g in ctx.gaps)
    high = low.assign(ndvi=0.2 + 0.7 * np.sin(np.arange(len(idx)) / 5) ** 2)
    assert pipeline.ndvi_cropland_peak(high["ndvi"]) > 0.6
    assert pipeline.ndvi_cropland_peak(low["ndvi"].iloc[:10]) is None                                 # one partial year: no verdict
