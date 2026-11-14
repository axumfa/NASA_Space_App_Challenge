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
    monkeypatch.setattr(appeears, "DEMO_CACHE_DIR", tmp_path)
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


# ---- real NASA AppEEARS output (subsets of a downloaded bundle), checked against NASA's own decoded QA columns
P = "MOD13Q1_061__250m_16_days_"
SP = "SPL3SMP_E_006_Soil_Moisture_Retrieval_Data_AM_"
REAL_NDVI = FIX / "real_appeears_MOD13Q1_subset.csv"
REAL_SMAP = FIX / "real_appeears_SPL3SMP_E_subset.csv"
FERGANA_CITY, SAMARKAND_CITY, NUKUS_CITY = (40.3842, 71.7843), (39.6542, 66.9597), (42.4602, 59.6166)


def _ndvi_truth(raw: pd.DataFrame) -> pd.Series:
    """QA truth from NASA's decoded description columns (independent of the bit decoding in the parser)."""
    return (raw[P + "VI_Quality_MODLAND_Description"].isin(["VI produced with good quality", "VI produced, but check other QA"])
            & (raw[P + "VI_Quality_Mixed_Clouds_Description"] == "No")
            & (raw[P + "VI_Quality_Possible_snow/ice_Description"] == "No")
            & (raw[P + "VI_Quality_Possible_shadow_Description"] == "No")
            & ~raw[P + "VI_Quality_VI_Usefulness_Description"].str.contains("not useful|Lowest|faulty", case=False))


@pytest.mark.parametrize("pid,pt", [("Fergana", FERGANA_CITY), ("Samarkand", SAMARKAND_CITY)])
def test_real_ndvi_no_reliability_layer_scaled_values_and_qa_matches_nasa_columns(pid, pt):
    raw = pd.read_csv(REAL_NDVI).query("ID == @pid")
    assert not any("pixel_reliability" in c for c in raw.columns)                      # the real download has none
    d = appeears.parse_ndvi(REAL_NDVI, *pt)
    assert len(d) == len(raw) and (d["qa"] == "VI_Quality bits").all()
    truth = _ndvi_truth(raw.sort_values("Date")).to_numpy()
    assert (d["ndvi"].notna().to_numpy() == truth).all()                               # QA agrees with NASA's decoded flags
    assert d["ndvi"].max() <= 0.5 and d["ndvi"].max() > 0.05                           # delivered scaled: not 0.00003, not 3000
    assert d["ndvi"].notna().sum() < len(d)                                            # cloudy/mixed pixels were removed


def test_real_ndvi_point_tolerance_is_strict():
    with pytest.raises(ValueError, match="no point within"):                           # demo field 40.43,71.70 is ~9 km from this town pixel
        appeears.parse_ndvi(REAL_NDVI, 40.43, 71.70)
    assert len(appeears.parse_ndvi(REAL_NDVI, 40.3842 + 0.004, 71.7843)) == 43         # within ~0.4 km still matches


def test_real_smap_qa_matches_nasa_recommended_quality_description():
    raw = pd.read_csv(REAL_SMAP)
    d = appeears.parse_smap(REAL_SMAP, *NUKUS_CITY)
    r = raw.query("ID == 'Nukus'").sort_values("Date")
    truth = (r[SP + "retrieval_qual_flag_Recommended_Quality_Description"].str.contains("has recommended")
             & (r[SP + "soil_moisture"] != -9999)).to_numpy()
    assert (d["soil_moisture"].notna().to_numpy() == truth).all() and truth.sum() > 0
    assert 0 < d["soil_moisture"].max() < 0.6


def test_real_smap_point_with_no_recommended_quality_retrievals_fails_cleanly(tmp_path, monkeypatch):
    raw = pd.read_csv(REAL_SMAP).query("ID == 'Fergana'")
    assert (raw[SP + "soil_moisture"] != -9999).sum() > 50                              # valid values exist ...
    assert not raw[SP + "retrieval_qual_flag_Recommended_Quality_Description"].str.contains("has recommended").any()   # ... none is recommended
    (tmp_path / "x-SPL3SMP-E-006-results.csv").write_bytes(REAL_SMAP.read_bytes())
    monkeypatch.setattr(appeears, "RAW_DIR", tmp_path / "raw")                          # loader also scans RAW_DIR.parent = tmp_path
    r = appeears.load_smap(*FERGANA_CITY)
    assert not r.ok and "rejected by QA" in r.message


def test_ndvi_requires_both_qa_layers_when_both_present(tmp_path):
    raw = pd.read_csv(REAL_NDVI).query("ID == 'Samarkand'").copy()
    raw["MOD13Q1_061__250m_16_days_pixel_reliability"] = 0
    raw.loc[raw.index[:5], "MOD13Q1_061__250m_16_days_pixel_reliability"] = 3          # cloudy by reliability layer only
    f = tmp_path / "both.csv"; raw.to_csv(f, index=False)
    d = appeears.parse_ndvi(f, *SAMARKAND_CITY)
    only_bits = appeears.parse_ndvi(REAL_NDVI, *SAMARKAND_CITY)
    assert d["qa"].iloc[0] == "VI_Quality bits + pixel_reliability"
    assert d["ndvi"].notna().sum() <= only_bits["ndvi"].notna().sum()
    assert d["ndvi"].iloc[:5].isna().all()


def test_one_fill_value_does_not_rescale_an_already_scaled_ndvi_column(tmp_path):
    """Regression from the real Karakalpakstan file: a single -3000 fill made the 'raw integers' branch fire and the whole series read ~0."""
    import pandas as pd

    from fieldshift.fetch.appeears import parse_ndvi
    rows = [("2024-01-01", -3000.0), ("2024-01-17", 0.20), ("2024-02-02", 0.45), ("2024-02-18", 0.70)]
    df = pd.DataFrame({"Latitude": 42.4128, "Longitude": 59.5159, "Date": [d for d, _ in rows],
                       "MOD13Q1_061__250m_16_days_NDVI": [v for _, v in rows], "MOD13Q1_061__250m_16_days_VI_Quality": 0})
    f = tmp_path / "x-MOD13Q1-061-results.csv"
    df.to_csv(f, index=False)
    out = parse_ndvi(f, 42.4128, 59.5159)
    assert out["ndvi"].dropna().round(2).tolist() == [0.20, 0.45, 0.70]
