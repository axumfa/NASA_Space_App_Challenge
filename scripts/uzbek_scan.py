"""Render the Uzbek UI in many states and list English fragments that code (not the translation table) put on screen.

Method: collect every visible string (markdown, captions, alerts, widget labels and options, tables, plotly titles/axes/legends,
map legend text), then flag words that occur in English UI strings but in no Uzbek string and are not product/proper names.
Usage: python scripts/uzbek_scan.py            (prints the findings; exit 1 if any)
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from streamlit.testing.v1 import AppTest  # noqa: E402

from fieldshift import i18n  # noqa: E402

WORD = re.compile(r"[A-Za-z][A-Za-z'’]+")
PROPER = {w.lower() for w in """NASA POWER MODIS NDVI SMAP SoilGrids ISRIC IMERG GIBS AppEEARS EOSDIS Esri Maxar Earthstar OpenStreetMap OpenTopoMap SRTM
CC BY SA GPM Terra MERRA CERES FAO Leaflet Field Shift GWETROOT ET0 GDD Ky REST MOD13Q1 SPL3SMP USD OSM QA UZ US N Sh Shq J G""".split()}
UNITS = {"mm", "kg", "ha", "km", "mi", "m", "sm", "yr", "h", "c", "csv", "ws", "deg"}
_en_words, _uz_words = set(), set()
for k, v in i18n.S.items():
    _en_words |= {w.lower() for w in WORD.findall(re.sub(r"\{[^}]*\}", " ", v["en"]))}
    _uz_words |= {w.lower() for w in WORD.findall(re.sub(r"\{[^}]*\}", " ", v.get("uz", "")))}
for cid, (nm, _) in i18n.CROP_UZ.items():
    _uz_words |= {w.lower() for w in WORD.findall(nm)}
for names in i18n.MONTHS.values():
    _uz_words |= {w.lower() for w in names}
ENGLISH = _en_words - _uz_words - PROPER - UNITS          # words that exist only in English strings
ENGLISH |= {"to", "from", "and", "the", "of", "for", "with", "not", "no", "is", "are", "was", "were", "in", "on", "at", "by", "or", "all", "this", "that"}
ENGLISH -= {"v", "a", "i", "bu", "on", "no", "at"}      # collide with Uzbek words / letters


def strip_html(t: str) -> str:
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"&#?\w+;", "'", t)                 # &#x27; etc.: an apostrophe, not a word break
    return re.sub(r"<[^>]+>", " ", t)


def texts_of_element(el) -> list[str]:
    out = []
    for attr in ("value", "label", "body", "help", "placeholder"):
        v = getattr(el, attr, None)
        if isinstance(v, str):
            out.append(v)
    opts = getattr(el, "options", None)
    if isinstance(opts, (list, tuple)):
        out += [o for o in opts if isinstance(o, str)]
    return out


def walk(node):
    yield node
    for c in getattr(node, "children", {}).values() if isinstance(getattr(node, "children", None), dict) else []:
        yield from walk(c)


def figure_texts(fig: dict) -> list[str]:
    out = []
    lay = fig.get("layout", {})

    def title(t):
        return t.get("text", "") if isinstance(t, dict) else (t or "")
    out.append(title(lay.get("title")))
    for ax in [k for k in lay if k.startswith(("xaxis", "yaxis"))]:
        out.append(title(lay[ax].get("title")))
        out += [str(x) for x in (lay[ax].get("ticktext") or [])]
    for a in lay.get("annotations", []) or []:
        out.append(a.get("text", ""))
    for tr in fig.get("data", []):
        if tr.get("name"):
            out.append(tr["name"])
        if tr.get("type") == "bar" and tr.get("x") is not None and any(isinstance(x, str) for x in tr["x"]):
            out += [x for x in tr["x"] if isinstance(x, str)]
        out += [x for x in (tr.get("theta") or []) if isinstance(x, str)]
    return [x for x in out if isinstance(x, str) and x.strip()]


def collect(at) -> list[str]:
    out = []
    for blk in (at.main, at.sidebar):
        for el in walk(blk):
            out += texts_of_element(el)
    for pc in at.get("plotly_chart"):
        try:
            out += figure_texts(json.loads(pc.proto.spec))
        except Exception:  # noqa: BLE001
            pass
    for df in at.dataframe:
        v = df.value
        out += [str(c) for c in v.columns] + [str(x) for x in v.to_numpy().ravel() if isinstance(x, str)]
    return out


def scan(texts: list[str], where: str, found: dict):
    for t in texts:
        clean = strip_html(t)
        for w in WORD.findall(clean):
            if w.lower() in ENGLISH:
                found[w.lower()].append((where, clean.strip()[:110]))


def run(fields=None, extras=True) -> dict:
    """Render the Uzbek UI and return {english_word: [(where, text), ...]}; `fields` limits the field list (default: all)."""
    found: dict = defaultdict(list)
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=300)
    at.run()
    at.session_state["lang_label"] = "O'zbekcha"
    at.run()
    fields = fields or [v["en"] for k, v in i18n.S.items() if k.startswith("field.")] + ["My own location"]
    for fld in fields:
        at.session_state["field_choice"] = fld
        for view in ("field", "options", "glossary"):
            at.session_state["view"] = view
            at.run()
            if at.exception:
                raise RuntimeError(f"exception rendering {fld}/{view}: {[e.value for e in at.exception]}")
            scan(collect(at), f"{fld[:22]}/{view}", found)
    if not extras:
        return found
    # what-if banner, other profiles
    at.session_state["field_choice"] = "Fergana Valley, Uzbekistan"
    for prof in ("water-first", "income-first", "soil-first"):
        at.session_state["profile"] = prof; at.session_state["view"] = "options"; at.run()
        scan(collect(at), f"profile {prof}", found)
    at.session_state["rain"], at.session_state["temp"], at.session_state["supply"] = -20, 2.0, 60
    for view in ("field", "options"):
        at.session_state["view"] = view; at.run(); scan(collect(at), f"what-if/{view}", found)
    # error states
    at.session_state["rain"], at.session_state["temp"], at.session_state["supply"] = 0, 0.0, 100
    at.session_state["crop1"] = at.session_state["crop0"]; at.session_state["view"] = "field"; at.run()
    scan(collect(at), "duplicate crop", found)
    # map: legend and control texts produced in Python
    from fieldshift import mapview
    from fieldshift.fetch import gibs
    layers = gibs.load_cached()
    html = mapview.build_map(40.4, 71.7, layers, "uz").get_root().render()
    scan(re.findall(r'"(?:title|lo|hi|src|note|asof|date)": "([^"]+)"', html) + [mapview.tr(f"map.{k}", "uz") for k in ("loading", "loaded", "tile_error", "source", "date")], "map", found)
    for name, txt, tip, ok in mapview.layer_status(layers, "uz"):
        scan([name, txt], "map layer line", found)
    return found


def main() -> int:
    found = run()
    if not found:
        print("no English-only words found in the rendered Uzbek UI")
        return 0
    print(f"{len(found)} English-only words found in rendered Uzbek text:\n")
    for w, hits in sorted(found.items()):
        print(f"- {w!r}  ({len(hits)}x)  e.g. [{hits[0][0]}] {hits[0][1]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
