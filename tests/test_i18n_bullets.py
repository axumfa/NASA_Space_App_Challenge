"""Every bullet shown in a field's gaps list and in the option cards must be translatable (no English left in Uzbek mode)."""
import re

import pytest

from fieldshift import i18n
from fieldshift.config import DEMO_FIELDS
from fieldshift.explain import explain
from fieldshift.i18n import Msg, render
from fieldshift.pipeline import build_context, run
from fieldshift.scoring import Weights

ENGLISH_WORDS = re.compile(r"\b(the|and|not|your|this|for|with|from|are|is|of|days|year|crop|field|soil)\b", re.I)


@pytest.fixture(scope="module")
def parts():
    f = DEMO_FIELDS["fergana"]
    ctx = build_context(f.lat, f.lon)
    res = run(ctx, f.rotation, Weights(), n_alternatives=500, n_per_rule=500)
    return ctx, res


def test_gaps_and_card_bullets_are_msgs_and_render_in_uzbek(parts):
    ctx, res = parts
    texts = list(ctx.gaps)
    for r in res:
        e = explain(r, res[0], ctx)
        texts += e.why + e.evidence + e.benefits + e.tradeoffs + e.gaps + e.risks
    assert texts and all(isinstance(t, Msg) for t in texts), [t for t in texts if not isinstance(t, Msg)]
    for t in texts:
        en, uz = render(t, "en"), render(t, "uz")
        assert en == str(t)                       # English output unchanged by the mechanism
        assert uz != en and not ENGLISH_WORDS.search(re.sub(r"\([^)]*\.csv[^)]*\)", "", uz)), (t.key, uz)


def test_no_point_message_is_translated_with_numbers_kept():
    ctx = build_context(39.98, 64.33)
    uz = " ".join(render(g, "uz") for g in ctx.gaps)
    assert "0.228" in uz and "no point within" not in uz


def test_every_msg_key_exists_with_uzbek_and_same_placeholders():
    for k, v in i18n.S.items():
        if k.startswith(("x.", "g.", "d.", "f.", "mk.", "ap.")):
            assert "uz" in v, k
            assert sorted(re.findall(r"\{(\w+)", v["en"])) == sorted(re.findall(r"\{(\w+)", v["uz"])), k


def test_msg_survives_pickle_and_copy():
    import copy
    import pickle
    from fieldshift.i18n import CropRef
    m = Msg("d.adds", crop=CropRef("chickpea", "Chickpea (spring-sown)"))
    for m2 in (pickle.loads(pickle.dumps(m)), copy.deepcopy(m)):
        assert isinstance(m2, Msg) and str(m2) == str(m) and render(m2, "uz") == render(m, "uz")
