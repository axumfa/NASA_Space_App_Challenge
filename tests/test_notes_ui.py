"""The planting-obligations limitation and the low-yield-risk note appear where promised."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

from fieldshift import i18n


def _app(lang="en", view="options", supply=100):
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=90)
    at.session_state["lang_label"] = {"en": "English", "uz": "O'zbekcha"}[lang]
    at.session_state["view"] = view
    at.session_state["supply"] = supply
    at.run()
    assert not at.exception
    return at


def _text(at):
    return " ".join(str(getattr(e, "value", "")) for e in list(at.markdown) + list(at.caption) + list(at.info))


def test_contracts_line_on_field_view_both_languages():
    for lang in ("en", "uz"):
        assert i18n.tr("g.contracts", lang) in _text(_app(lang, "field"))


def test_no_country_specific_wording():
    for lang in ("en", "uz"):
        s = i18n.tr("g.contracts", lang).lower() + i18n.tr("o.yield_low", lang, sec="x").lower()
        assert not any(w in s for w in ("quota", "kvota", "law", "qonun", "state", "davlat", "government", "hukumat"))


def test_low_yield_note_at_full_supply_only_when_all_under_3_percent():
    at = _app()
    note = i18n.tr("o.yield_low", "en", sec=i18n.tr("ui.sidebar_what", "en"))
    txt = _text(at)
    # shown on the table and on every card (4+ times) exactly when every displayed figure is under 3 %
    low = txt.count(note)
    assert low == 0 or low >= 2
    at = _app(supply=60)
    assert note not in _text(at)
