"""The Uzbek UI must not show English produced by code (dates, units, reasons, bullets, soil terms)."""
import importlib.util
import re
from pathlib import Path

import pytest

from fieldshift import i18n
from fieldshift.i18n import render
from fieldshift.pipeline import build_context

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def scan():
    spec = importlib.util.spec_from_file_location("uzbek_scan", ROOT / "scripts" / "uzbek_scan.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rendered_uzbek_ui_has_no_english_only_words(scan):
    found = scan.run(["Fergana Valley, Uzbekistan", "Karakalpakstan farmland (near Nukus), Uzbekistan"], extras=False)
    assert not found, {w: h[0] for w, h in found.items()}


def test_failure_reasons_and_date_ranges_are_language_neutral_or_translated():
    from fieldshift.config import DEMO_FIELDS
    f = DEMO_FIELDS["fergana"]
    ctx = build_context(f.lat, f.lon)                                   # NDVI loads, SMAP is rejected by QA at this point
    uz = " ".join(render(g, "uz") for g in ctx.gaps)
    assert "barcha kuzatuvlar sifat tekshiruvidan o'tmadi" in uz
    assert ".csv" not in uz and "rejected by QA" not in uz and " to " not in uz
    rng = ctx.ndvi.date_range
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} – \d{4}-\d{2}-\d{2}", rng), rng


def test_no_point_reason_has_no_file_name_in_either_language():
    ctx = build_context(39.98, 64.33)                                    # no satellite point near here
    for lang in ("en", "uz"):
        txt = " ".join(render(g, lang) for g in ctx.gaps)
        assert ".csv" not in txt and "0.228" in txt


def test_year_class_wording():
    s = i18n.S
    assert "qurg'oqchil/me'yoriy/seryog'in yil" in s["g.classes"]["uz"].lower() and "hisobga olinmaydi" in s["g.classes"]["uz"]
    assert "quruq yil" not in " ".join(v.get("uz", "").lower() for v in s.values())
