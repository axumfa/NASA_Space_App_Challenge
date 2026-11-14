import re

import pytest

from fieldshift.config import DEMO_FIELDS
from fieldshift.explain import is_arid, summary_box
from fieldshift.pipeline import build_context, choose, run
from fieldshift.scoring import PROFILES, Weights


@pytest.fixture(scope="module")
def fergana():
    f = DEMO_FIELDS["fergana"]
    ctx = build_context(f.lat, f.lon)
    return ctx, run(ctx, f.rotation, Weights(), n_alternatives=500, n_per_rule=500)


def _numbers(text: str) -> set[int]:
    return {int(round(float(x))) for x in re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))}


def test_summary_has_four_parts_and_uses_only_computed_numbers(fergana):
    ctx, pool = fergana
    for w in (Weights(), PROFILES["water-first"], PROFILES["income-first"]):
        display, _ = choose(pool, w, 4)
        sb = summary_box(display, w, "en", arid=is_arid(ctx))
        assert all(sb[k] for k in ("best", "reason", "tradeoff", "check", "caveat"))
        allowed = {int(round(v)) for v in sb["facts"].values()}
        allowed |= {int(round(r.summary["fit"]["median"])) for r in display}
        for pre in ("", "trade_"):                                   # percentage change shown next to the water figures
            k = f"{pre}water_saving"
            if f"{k}_new" in sb["facts"] and sb["facts"][f"{k}_old"]:
                allowed.add(int(round(abs(100 * (sb["facts"][f"{k}_new"] - sb["facts"][f"{k}_old"]) / sb["facts"][f"{k}_old"]))))
        allowed |= {r.rotation.cycle_years for r in display}
        text = " ".join(sb[k] for k in ("best", "reason", "tradeoff"))
        extra = _numbers(text) - allowed - {0, 100}                  # '100' = the index scale, 0 = formatting
        assert not extra, f"numbers not traceable to computed results: {extra} in: {text}"


def test_summary_names_the_best_option_by_fit(fergana):
    ctx, pool = fergana
    w = Weights()
    display, _ = choose(pool, w, 4)
    best = max(display, key=lambda r: r.summary["fit"]["median"])
    sb = summary_box(display, w)
    if best is display[0]:
        assert sb["best_is_current"] and "current rotation fits" in sb["best"]
    else:
        assert f"fit {best.summary['fit']['median']:.0f}" in sb["best"] and not sb["best_is_current"]


def test_salinity_check_only_when_arid(fergana):
    ctx, pool = fergana
    assert is_arid(ctx)                                             # Fergana: ~190 mm rain vs ~1500 mm ET0
    w = PROFILES["income-first"]
    display, _ = choose(pool, w, 4)
    assert "salt" in summary_box(display, w, arid=True)["check"] or "new for you" in summary_box(display, w, arid=True)["check"]
    assert "salt" not in summary_box(display, w, arid=False)["check"]


def test_kansas_is_not_arid():
    f = DEMO_FIELDS["kansas"]
    assert not is_arid(build_context(f.lat, f.lon))
