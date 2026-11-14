"""Write docs/uzbek_review.md: every Uzbek string in the app, with the ones the author is unsure about listed first.

Usage: python scripts/uzbek_review.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fieldshift import i18n  # noqa: E402
from fieldshift.crops import load_crops  # noqa: E402


def esc(t: str) -> str:
    return t.replace("|", "\\|").replace("\n", "<br>")


def main() -> None:
    sure = [k for k in i18n.S if k not in i18n.UNSURE and i18n.S[k].get("uz") and i18n.S[k]["en"]]
    out = ["# Uzbek text for native-speaker review\n",
           "All Uzbek text (Latin script) was written by the AI assistant and has **not** been checked by a native speaker. "
           "Please correct anything that is wrong, unnatural, or not the term farmers actually use. Placeholders in `{braces}` "
           "(numbers, crop names) must stay exactly as they are. Dataset and product names (NASA POWER, MODIS, SMAP, SoilGrids, FAO) are "
           "intentionally not translated.\n",
           "To change a string, edit `src/fieldshift/i18n.py` (key shown below); `scripts/uzbek_review.py` regenerates this file.\n",
           f"\n## 1. Strings I am unsure about ({len(i18n.UNSURE)})\n", "| key | English | Uzbek | why unsure |", "|---|---|---|---|"]
    for k, why in sorted(i18n.UNSURE.items()):
        out.append(f"| `{k}` | {esc(i18n.S[k]['en'])} | {esc(i18n.S[k]['uz'])} | {esc(why)} |")
    db = load_crops()
    out += ["\n## 2. Crop names\n", "| crop | English | Uzbek | note |", "|---|---|---|---|"]
    for cid, c in db.items():
        uz, note = i18n.CROP_UZ[cid]
        out.append(f"| `{cid}` | {esc(c['name'])} | {esc(uz)} | {esc(note) if note else ''} |")
    out += [f"\n## 3. All other strings ({len(sure)}), please still skim\n", "| key | English | Uzbek |", "|---|---|---|"]
    for k in sure:
        out.append(f"| `{k}` | {esc(i18n.S[k]['en'])} | {esc(i18n.S[k]['uz'])} |")
    out += ["\n## 4. What is NOT translated (stays English in Uzbek mode)\n",
            "- The long bullets inside each option card: *Why this option*, *Evidence (numbers)*, *Benefits*, *Information gaps*, *Risks to check with a local expert*. "
            "The section titles are translated; the bullet sentences are templated English built from the numbers. The app shows a note about this in Uzbek mode.",
            "- The *What data is missing for this field?* list on the field view (same reason).",
            "- Texts inside the downloaded documents (`README.md`, `docs/`).",
            "- Soil texture class names (`clay loam`, `loam`, ...) and the data-source names."]
    Path(__file__).resolve().parents[1].joinpath("docs", "uzbek_review.md").write_text("\n".join(out) + "\n")
    print(f"unsure: {len(i18n.UNSURE)}, other strings: {len(sure)}, crops: {len(db)}")


if __name__ == "__main__":
    main()
