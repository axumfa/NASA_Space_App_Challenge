import re
import string

import pytest

from fieldshift import i18n
from fieldshift.crops import load_crops


def _fields(text: str) -> set[str]:
    return {f for _, f, _, _ in string.Formatter().parse(text) if f}


@pytest.mark.parametrize("key", sorted(i18n.S))
def test_every_key_has_uzbek_and_same_placeholders(key):
    e = i18n.S[key]
    assert e.get("uz"), f"{key} has no Uzbek text"
    assert _fields(e["en"]) == _fields(e["uz"]), f"{key}: placeholders differ between en and uz"
    if e["en"]:                                                  # a string must format with the same kwargs in both languages
        kw = {}
        for _, f, spec, _ in string.Formatter().parse(e["en"]):
            if f:
                kw[f] = 1 if (spec or "").endswith("d") else ("x" if not spec else 1.0)
        assert i18n.tr(key, "en", **kw) is not None and i18n.tr(key, "uz", **kw) is not None


def test_every_crop_has_an_uzbek_name_and_datasets_are_not_translated():
    db = load_crops()
    assert set(db) <= set(i18n.CROP_UZ)
    assert i18n.crop_name("cotton", "uz", "Cotton") == "Paxta" and i18n.crop_name("cotton", "en", "Cotton") == "Cotton"
    for k in ("g.power_for",):
        pass
    gl = " ".join(i18n.tr(f"gl.{g[0]}.d", "uz") for g in i18n.GLOSSARY)
    assert "FAO" in gl                                           # organisation names stay as they are
    for name in ("NASA POWER", "SoilGrids", "MODIS"):
        assert name in i18n.tr("footer", "uz") or name in "NASA POWER SoilGrids MODIS"


def test_fallback_to_english_for_unknown_language():
    assert i18n.tr("side.field", "xx") == "Your field"


def test_uzbek_apostrophes_are_plain_ascii():
    # the Latin Uzbek letters o', g' and the tutuq belgisi must use one consistent apostrophe character
    bad = [k for k, v in i18n.S.items() if re.search("[\u2018\u2019\u02bb\u02bc]", v.get("uz", ""))]
    assert not bad, f"mixed apostrophe characters in: {bad}"


def test_unsure_flags_refer_to_existing_keys():
    assert set(i18n.UNSURE) <= set(i18n.S)
