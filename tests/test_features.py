import numpy as np
import pandas as pd
import pytest

from fieldshift import features as F


def test_ra_fao56_example():
    # FAO-56 Example 8: lat 20°S, 3 Sept (doy 246) -> Ra = 32.2 MJ/m2/day
    assert F.extraterrestrial_radiation(-20, 246) == pytest.approx(32.2, abs=0.2)


def test_et0_fao56_example17_brussels():
    # FAO-56 Example 18: Brussels 6 July, 100 m, 50.8N. Tmax 21.5, Tmin 12.3, ea 1.409 kPa,
    # u2 2.78 m/s, Rs 22.07 MJ/m2/day -> ET0 = 3.9 mm/day
    et0 = F.et0_penman_monteith(21.5, 12.3, 22.07, 1.409, 2.78, 100, 50.8, 187)
    assert float(et0) == pytest.approx(3.9, abs=0.15)


def test_gdd_daily_clipping():
    # base 10, cap 30: (min 5->10, max 35->30) -> 20-10 = 10
    assert float(F.gdd_daily(5, 35, 10, 30)) == pytest.approx(10.0)
    assert float(F.gdd_daily(0, 8, 10, 30)) == 0.0


def _daily(years, fn):
    idx = pd.date_range(f"{years[0]}-01-01", f"{years[-1]}-12-31")
    return pd.DataFrame(fn(idx), index=idx)


def test_frost_dates_and_probability():
    def tmin(idx):
        t = np.full(len(idx), 5.0)
        t[(idx.month == 3) & (idx.day == 10)] = -2.0   # last spring frost doy 69/70
        t[(idx.month == 11) & (idx.day == 5)] = -1.0   # first autumn frost
        return {"T2M_MIN": t}
    df = _daily([2020, 2021], tmin)
    ft = F.frost_table(df, 40.0)
    assert ft.loc[2021, "last_spring_frost_doy"] == 69
    assert ft.loc[2021, "first_autumn_frost_doy"] == pd.Timestamp("2021-11-05").day_of_year
    assert ft.loc[2021, "frost_days"] == 2
    p = F.frost_probability_by_week(df)
    assert p.loc[(69 - 1) // 7 + 1] == 1.0 and p.loc[20] == 0.0


def test_heat_stress_days():
    df = _daily([2020], lambda i: {"T2M_MAX": np.where(i.month == 7, 36.0, 25.0)})
    assert F.heat_stress_days(df, 35)[2020] == 31


def test_water_balance_and_class():
    df = _daily([2019, 2020, 2021], lambda i: {
        "PRECTOTCORR": np.full(len(i), 1.0) * np.where(i.year == 2020, 2, 1), "ET0": np.full(len(i), 3.0)})
    wb = F.monthly_water_balance(df)
    assert wb.loc[(2019, 1), "WB"] == pytest.approx(31 * (1 - 3))
    ann = pd.DataFrame({"precip": [100, 200, 300]}, index=[1, 2, 3])
    assert list(F.classify_years(ann)) == ["dry", "normal", "wet"]


def test_soil_moisture_anomaly_zero_mean():
    df = _daily([2018, 2019, 2020], lambda i: {"GWETROOT": np.where(i.year == 2019, 0.6, 0.4)})
    z = F.soil_moisture_anomaly(df)
    assert z.loc[(2019, 5), "z"] > 0 > z.loc[(2018, 5), "z"]


def test_theil_sen_trend():
    s = pd.Series(np.arange(20) * 0.05 + 10, index=range(2000, 2020))
    tr = F.theil_sen_trend(s)
    assert tr.slope_per_decade == pytest.approx(0.5) and tr.significant


def test_add_et0_uses_fao56_eq19_for_actual_vapour_pressure():
    # With RH=50% the ET0 must match the explicit eq.19 calculation (ea from mean of es(Tmax), es(Tmin)).
    idx = pd.date_range("2020-07-01", periods=3)
    df = pd.DataFrame({"T2M": 30.0, "T2M_MAX": 38.0, "T2M_MIN": 22.0, "RH2M": 50.0, "WS2M": 2.0,
                       "ALLSKY_SFC_SW_DWN": 27.0}, index=idx)
    es = (F.sat_vp(38.0) + F.sat_vp(22.0)) / 2
    expected = F.et0_penman_monteith(38.0, 22.0, 27.0, 0.5 * es, 2.0, 500, 40.0, idx.day_of_year.values)
    got = F.add_et0(df, 40.0, 500)["ET0"].values
    assert got == pytest.approx(expected)


def test_cache_keys_distinct_for_decimal_lon_and_different_requests(tmp_path, monkeypatch):
    from fieldshift.fetch import base
    monkeypatch.setattr(base, "CACHE_DIR", tmp_path)
    a = base._json_path(base.cache_key("power", 40.4, 71.78, "2001", "2025", "T2M"))
    b = base._json_path(base.cache_key("power", 40.4, 71.78, "2001", "2010", "T2M"))
    c = base._json_path(base.cache_key("power", 40.4, 71.98, "2001", "2025", "T2M"))
    assert len({a, b, c}) == 3 and a.name.endswith(".json") and "71.78" in a.name
    base.write_json_cache(base.cache_key("power", 40.4, 71.78, "2001", "2025", "T2M"), {"x": 1})
    assert base.read_json_cache(base.cache_key("power", 40.4, 71.78, "2001", "2010", "T2M")) is None


def test_root_wetness_summary_months_and_latest_year():
    idx = pd.date_range("2018-01-01", "2021-12-31")
    df = pd.DataFrame({"GWETROOT": np.where(idx.year == 2021, 0.7, 0.4) + 0.0 * np.arange(len(idx))}, index=idx)
    rw = F.root_wetness_summary(df)
    assert list(rw.index) == list(range(1, 13)) and rw.attrs["latest_year"] == 2021
    assert rw["latest"].to_numpy() == pytest.approx(0.7) and (rw["latest_z"] > 0).all() and (rw["p10"] <= rw["median"]).all()


# ---------------------------------------------------------------- satellite bare days: not observable vs not bare
def _years(winter_ok: bool, trough: float, years=(2019, 2020, 2021)):
    """16-day composites: green April-May, low June trough, otherwise 0.45; winter either observed or rejected (NaN) like snow dates."""
    import numpy as np
    import pandas as pd
    parts = []
    for y in years:
        idx = pd.date_range(f"{y}-01-01", f"{y}-12-31", freq="16D")
        v = np.where((idx.month >= 4) & (idx.month <= 5), 0.7, 0.45)
        v = np.where(idx.month == 6, trough, v)
        s = pd.Series(v, index=idx)
        if not winter_ok:
            s[(idx.month <= 2) | (idx.month == 12)] = np.nan
        parts.append(s)
    return pd.concat(parts)


def test_rejected_winter_is_not_observable_never_zero_bare_days():
    r = F.observed_bare_summary(_years(False, trough=0.15), 0.2)
    assert {12, 1, 2} <= set(r["poor_months"])
    assert r["unobservable_days"] >= 31 + 28 + 31 - 5                      # winter days are reported as not observable
    assert r["bare_days"] > 0                                               # the observed June trough (0.15 < 0.2) is still counted


def test_green_pixel_with_clear_winter_has_no_bare_days_and_nothing_unobservable():
    r = F.observed_bare_summary(_years(True, trough=0.35), 0.2)
    assert r["bare_days"] == 0 and r["poor_months"] == [] and r["unobservable_days"] < 20


def test_too_few_observations_gives_no_verdict():
    import pandas as pd
    s = pd.Series([0.5] * 5, index=pd.date_range("2022-03-01", periods=5, freq="16D"))
    assert F.observed_bare_summary(s, 0.2) is None
