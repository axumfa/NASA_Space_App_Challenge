"""UI strings in English and Uzbek (Latin script). `tr(key, lang, **fmt)` falls back to English.

Uzbek strings that the author is not sure about are listed in docs/uzbek_review.md for a native speaker to check.
Crop names come from `crop_name`; dataset and product names (NASA POWER, MODIS, SMAP, SoilGrids) are never translated.
"""
from __future__ import annotations

LANGS = {"en": "English", "uz": "O'zbekcha"}

S: dict[str, dict[str, str]] = {}


def add(key: str, en: str, uz: str | None = None) -> None:
    S[key] = {"en": en, **({"uz": uz} if uz else {})}


def tr(key: str, lang: str = "en", **fmt) -> str:
    entry = S[key]
    text = entry.get(lang) or entry["en"]
    return text.format(**fmt) if fmt else text


# ---- plain-language summary box (rotation tab)
add("sum.title", "In plain words")
add("sum.best", "**Best fit for your priorities:** {crops} (fit {fit:.0f}; your current rotation {cur:.0f}).")
add("sum.best_is_current", "**Your current rotation fits your priorities best** among these options (fit {fit:.0f}; next best {other:.0f}).")
add("sum.reason", "**Why:** {reasons}.")
add("sum.reason_none", "**Why:** it is ahead on the combination of your priorities, but by no single large margin.")
add("sum.tradeoff", "**Main trade-off:** {tradeoff}.")
add("sum.tradeoff_none", "**Main trade-off:** none of your priorities gets clearly worse than in your current rotation.")
add("sum.check", "**Check with a local agronomist:** {check}")
add("sum.caveat", "This summary is built only from the numbers on this page. It compares the options shown; it is not a forecast.")
add("r.water", "irrigation need {new:.0f} mm/yr instead of {old:.0f} mm ({pct:+.0f}%)")
add("r.nitrogen", "legumes add about {new:.0f} kg N/ha per year (now {old:.0f})")
add("r.erosion", "bare soil falls to {new:.0f} days a year (now {old:.0f})")
add("r.soil_om", "more organic matter returns to the soil (index {new:.0f} vs {old:.0f} of 100)")
add("r.forage", "more feed value (index {new:.0f} vs {old:.0f} of 100)")
add("r.income", "higher expected market income (index {new:.0f} vs {old:.0f} of 100)")
add("t.water", "it needs more water: {new:.0f} mm/yr instead of {old:.0f} mm ({pct:+.0f}%)")
add("t.nitrogen", "less nitrogen from legumes ({new:.0f} kg N/ha per year instead of {old:.0f})")
add("t.erosion", "more bare soil ({new:.0f} days a year instead of {old:.0f})")
add("t.soil_om", "less organic matter returns to the soil (index {new:.0f} vs {old:.0f} of 100)")
add("t.forage", "less feed value (index {new:.0f} vs {old:.0f} of 100)")
add("t.income", "lower expected market income (index {new:.0f} vs {old:.0f} of 100)")
add("t.shortage", "in a water-short year (1 in 10) yield at risk from shortage is {new:.0f}% instead of {old:.0f}%")
add("c.salinity", "{crop} is sensitive to salt; check soil and irrigation-water salinity before sowing it.")
add("c.newcrop", "{crop} is new for you; confirm seed, machinery and a buyer or market before committing.")
add("c.water", "confirm that irrigation water will really be available ({irr:.0f} mm/yr is needed).")
add("c.dates", "check that the sowing and harvest dates in this calendar fit your local weather and farm work.")
add("c.cycle", "this rotation takes {years} years to complete; check that it fits your land and contracts.")
