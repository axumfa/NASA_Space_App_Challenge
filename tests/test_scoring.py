import numpy as np
import pandas as pd
import pytest

from fieldshift.crops import kc_curve, load_crops
from fieldshift.rotations import schedule
from fieldshift.scoring import DailyClimate, Weights, score_rotation, static_subscores, summarize

DB = load_crops()


def _clim(tmean=20.0, p=1.0, et0=4.0, years=(2001, 2008)):
    idx = pd.date_range(f"{years[0]}-01-01", f"{years[1]}-12-31")
    n = len(idx)
    df = pd.DataFrame({"T2M": np.full(n, tmean), "T2M_MAX": np.full(n, tmean + 6),
                       "T2M_MIN": np.full(n, tmean - 6), "PRECTOTCORR": np.full(n, p),
                       "ET0": np.full(n, et0)}, index=idx)
    return DailyClimate(df)


def test_kc_curve_length_and_bounds():
    c = DB["cotton"]
    k = kc_curve(c, 180)
    assert len(k) == 180 and k[0] == pytest.approx(0.36, abs=0.05) and max(k) == pytest.approx(1.18)


def test_irrigation_is_etc_minus_effective_rain():
    clim = _clim()
    rot = schedule(("maize",), DB)
    cls = pd.Series("normal", index=range(2001, 2009))
    s = score_rotation(rot, DB, clim, Weights(), cls)
    r = s.iloc[0]
    assert r["irrigation_mm_per_year"] > 0
    # rain 1 mm/day over 125 days = 125 mm, eff 100 mm, ETc ~ mean(kc)*4*125 -> irrigation = ETc - 100
    assert r["irrigation_mm_per_year"] == pytest.approx(
        float(np.sum(kc_curve(DB["maize"], 125)) * 4) - 100, rel=0.01)


def test_legume_rotation_scores_higher_nitrogen_and_pest_break():
    base = static_subscores(schedule(("winter_wheat", "cotton"), DB), DB)
    vetch = static_subscores(schedule(("winter_wheat", "hairy_vetch", "cotton"), DB), DB)
    assert vetch["nitrogen"] > base["nitrogen"] == 0
    assert vetch["bare_days"] < base["bare_days"]
    assert vetch["erosion"] > base["erosion"]


def test_monoculture_penalised_by_pest_break():
    st = static_subscores(schedule(("maize", "sorghum"), DB), DB)  # same family back-to-back
    assert st["pest_break"] == 0
    assert static_subscores(schedule(("maize", "soybean"), DB), DB)["pest_break"] == 100


def test_hot_climate_lowers_suitability_of_cool_crop():
    cls = pd.Series("normal", index=range(2001, 2009))
    rot = schedule(("potato", "maize"), DB)
    hot = score_rotation(rot, DB, _clim(tmean=34), Weights(), cls)["suitability"].median()
    mild = score_rotation(rot, DB, _clim(tmean=20), Weights(), cls)["suitability"].median()
    assert hot < mild


def test_weights_change_total_and_summary_has_classes():
    cls = pd.Series(["dry", "normal", "wet", "normal"] * 2, index=range(2001, 2009))
    rot = schedule(("winter_wheat", "hairy_vetch", "cotton"), DB)
    a = score_rotation(rot, DB, _clim(), Weights(nitrogen=5), cls)
    b = score_rotation(rot, DB, _clim(), Weights(water_saving=5), cls)
    assert a["total"].median() != b["total"].median()
    s = summarize(a)
    assert {"median", "p10", "p90", "median_dry", "median_wet"} <= set(s["total"])
