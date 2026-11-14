import pytest

from fieldshift.fetch.soil import parse_rest, texture_class


def _layer(name, d_factor, means):
    return {"name": name, "unit_measure": {"d_factor": d_factor},
            "depths": [{"label": l, "values": {"mean": m}} for l, m in zip(["0-5cm", "5-15cm", "15-30cm"], means)]}


def test_parse_rest_converts_units_and_weights_depths():
    payload = {"properties": {"layers": [_layer("clay", 10, [200, 250, 300]), _layer("soc", 10, [150, 100, 50]),
                                         _layer("phh2o", 10, [80, 80, 80]), _layer("bdod", 100, [130, 140, 150])]}}
    v = parse_rest(payload)
    assert v["clay_pct"] == pytest.approx((20 * 5 + 25 * 10 + 30 * 15) / 30)
    assert v["soc_g_kg"] == pytest.approx((15 * 5 + 10 * 10 + 5 * 15) / 30)
    assert v["phh2o"] == pytest.approx(8.0) and v["bdod_kg_dm3"] == pytest.approx((1.3 * 5 + 1.4 * 10 + 1.5 * 15) / 30)


def test_parse_rest_skips_missing_values():
    payload = {"properties": {"layers": [{"name": "clay", "unit_measure": {"d_factor": 10},
               "depths": [{"label": "0-5cm", "values": {"mean": None}}]}]}}
    assert parse_rest(payload) == {}


def test_texture_class():
    assert texture_class(45, 20, 35) == "clay" and texture_class(8, 80, 12) == "sandy"
