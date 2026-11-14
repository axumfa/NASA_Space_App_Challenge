from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from fieldshift import features as F
from fieldshift.fetch import appeears

FIX = Path(__file__).parent / "fixtures"


def test_ndvi_qa_rejects_snow_cloud_fill_and_scales():
    d = appeears.parse_ndvi(FIX / "appeears_MOD13Q1_fixture.csv", 40.40, 71.78)
    raw = pd.read_csv(FIX / "appeears_MOD13Q1_fixture.csv").query("ID == 'fergana'")
    assert len(d) == len(raw)                                        # point selection: only the Fergana rows
    bad = raw["MOD13Q1_061__250m_16_days_pixel_reliability"].isin([2, 3, -1]).values
    assert d["ndvi"].isna().values[bad].all() and d["ndvi"].notna().values[~bad].all()
    assert 0 < d["ndvi"].max() < 1                                   # scale factor 0.0001 applied


def test_ndvi_selects_other_point_and_rejects_far_point():
    k = appeears.parse_ndvi(FIX / "appeears_MOD13Q1_fixture.csv", 38.5, -98.5)
    raw = pd.read_csv(FIX / "appeears_MOD13Q1_fixture.csv").query("ID == 'kansas'")
    assert len(k) == len(raw) and k["ndvi"].notna().sum() > 0.9 * len(k)   # only cloud/fill rows rejected
    with pytest.raises(ValueError, match="no point within"):
        appeears.parse_ndvi(FIX / "appeears_MOD13Q1_fixture.csv", 10.0, 10.0)


def test_smap_qa_flag_and_fill():
    d = appeears.parse_smap(FIX / "appeears_SPL3SMP_E_fixture.csv", 40.40, 71.78)
    assert d.loc["2018-03-05", "soil_moisture"] == pytest.approx(0.19)      # AM flagged -> PM only
    assert np.isnan(d.loc["2018-03-06", "soil_moisture"])                   # both fill -> NaN
    assert d.loc["2018-03-07", "soil_moisture"] == pytest.approx(0.195, abs=0.02)


def test_missing_columns_raise_with_column_list(tmp_path):
    f = tmp_path / "x_MOD13Q1.csv"
    pd.DataFrame({"Latitude": [1.0], "Longitude": [1.0], "Date": ["2020-01-01"], "foo": [1]}).to_csv(f, index=False)
    with pytest.raises(ValueError, match="columns are"):
        appeears.parse_ndvi(f, 1.0, 1.0)


def test_loader_absent_files_is_a_clean_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(appeears, "RAW_DIR", tmp_path)
    r = appeears.load_ndvi(40.4, 71.78)
    assert not r.ok and "data/raw" in r.message
    assert not appeears.load_smap(40.4, 71.78).ok


def test_loader_picks_up_file_and_reports_qa_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(appeears, "RAW_DIR", tmp_path)
    (tmp_path / "req-MOD13Q1-061-results.csv").write_bytes((FIX / "appeears_MOD13Q1_fixture.csv").read_bytes())
    r = appeears.load_ndvi(40.40, 71.78)
    assert r.ok and r.meta["n_valid"] < r.meta["n_total"]


def test_bare_windows_and_observed_bare_days():
    idx = pd.date_range("2015-01-01", "2020-12-31", freq="16D")
    nd = pd.Series(np.where((idx.day_of_year > 120) & (idx.day_of_year < 250), 0.6, 0.1), index=idx)
    curve = F.ndvi_seasonal_curve(nd)
    wins = F.bare_windows_from_ndvi(curve, 0.2)
    assert len(wins) == 1 and wins[0][1] > 200                        # one long bare window wrapping the year end
    assert 150 < F.observed_bare_days_per_year(nd, 0.2).median() < 260


def test_smap_rejects_quality_flag_fill_value(tmp_path):
    f = tmp_path / "x_SPL3SMP.csv"
    pre = "SPL3SMP_E_006_Soil_Moisture_Retrieval_Data_AM_"
    pd.DataFrame({"Latitude": [1.0] * 3, "Longitude": [1.0] * 3, "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                  pre + "soil_moisture": [0.3, 0.3, 0.3], pre + "retrieval_qual_flag": [0, 1, 65534]}).to_csv(f, index=False)
    d = appeears.parse_smap(f, 1.0, 1.0)
    assert d["soil_moisture"].notna().tolist() == [True, False, False]      # recommended / not recommended / fill
