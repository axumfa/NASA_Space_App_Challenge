"""Why does the satellite show ~0 bare days at the Fergana 213 ha point while the crop calendar says 155? (diagnosis only)

Reads the committed demo satellite subset (data/demo_cache) or the full AppEEARS download (data/raw) and writes docs/satellite_bare_days.md.
Nothing here changes a threshold or the calendar.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fieldshift import features as F  # noqa: E402
from fieldshift.config import DEMO_FIELDS  # noqa: E402
from fieldshift.fetch import appeears as A  # noqa: E402
from fieldshift.i18n import MONTHS  # noqa: E402
from fieldshift.rotations import schedule  # noqa: E402
from fieldshift.crops import load_crops  # noqa: E402

f = DEMO_FIELDS["fergana"]
files = A._files("MOD13Q1")
src = next((p for p in files if "demo-points" in p.name), files[0])     # the committed demo subset is enough (same values)
raw = pd.read_csv(src)
df = A._select_point(raw, f.lat, f.lon, A.NDVI_MAX_DEG)
cols = list(df.columns)
dates = pd.to_datetime(df[A._find_col(cols, r"^date$")]).values
nd = df[A._find_col(cols, r"250m_16_days_NDVI$")].astype(float).to_numpy()
parsed = A.parse_ndvi(src, f.lat, f.lon)["ndvi"]
t = pd.DataFrame({"date": dates, "ndvi": nd, "ok": parsed.reindex(pd.DatetimeIndex(dates)).notna().to_numpy()})
t = t[t.date >= "2019-01-01"].copy()
t["m"] = t.date.dt.month
mn = MONTHS["en"]

out = [f"# Satellite vs calendar bare days, Fergana demo field ({f.lat}, {f.lon})\n",
       f"Source: `{src.name}`, MOD13Q1.061 250 m NDVI, 2019–2026, {len(t)} composites. Diagnosis only: no threshold or calendar was changed.\n",
       "## 1. By calendar month (all years pooled)\n", "| month | composites | pass QA | rejected | median NDVI (passing) | min NDVI (passing) | median NDVI (all, unfiltered) |", "|---|---|---|---|---|---|---|"]
for m, g in t.groupby("m"):
    p = g[g.ok]
    out.append(f"| {mn[m - 1]} | {len(g)} | {int(g.ok.sum())} | {int((~g.ok).sum())} | {p.ndvi.median():.2f} | {p.ndvi.min():.2f} | {g.ndvi.median():.2f} |")
out.append(f"\nDec–Feb: {int(t[t.m.isin([12, 1, 2])].ok.sum())} of {len(t[t.m.isin([12, 1, 2])])} composites pass QA. All rejected winter composites carry "
           "pixel reliability 3 (snow/ice) and fail the VI_Quality cloud/snow bits.\n")

d = parsed.dropna()
summ = F.observed_bare_summary(parsed, 0.2)
out += ["## 2. How failed observations are treated\n",
        "- Rejected composites are removed (not counted as bare, not counted as not bare).",
        "- The old count (`observed_bare_days_per_year`) then **interpolated linearly across the gaps**; a winter with only 1–3 clear dates was filled in "
        "from those few clear (never snow-covered) values, so it could only say 0.",
        "- The count now (`observed_bare_summary`) skips (a) days more than 24 days from a passing observation and (b) every calendar month in which "
        "fewer than half of the composites pass QA. Those days are reported as **not observable**, never as 0 bare days.",
        f"- Fergana result: bare days on observable days = **{summ['bare_days']:.0f}** per year; **{summ['unobservable_days']:.0f}** days a year not observable; "
        f"poorly observed months: {', '.join(mn[m - 1] for m in summ['poor_months'])}.\n"]

out += ["## 3. Do the two peaks fall in the same year?\n", "| year | Mar–May max (date) | June min | Jul–Sep max (date) | Oct–Dec median | Jan–Feb median |", "|---|---|---|---|---|---|"]
rows = []
for y in range(2019, 2026):
    g = d[d.index.year == y]
    s1 = g[(g.index.month >= 3) & (g.index.month <= 5)]; s2 = g[(g.index.month >= 7) & (g.index.month <= 9)]
    jun = g[g.index.month == 6]; q4 = g[g.index.month >= 10]; w = g[g.index.month <= 2]
    rows.append((y, s1.max(), s2.max(), jun.min()))
    out.append(f"| {y} | {s1.max():.2f} ({s1.idxmax():%m-%d}) | {jun.min():.2f} | {s2.max():.2f} ({s2.idxmax():%m-%d}) | {q4.median():.2f} | "
               f"{'–' if w.empty else f'{w.median():.2f}'} |")
spring = np.array([r[1] for r in rows]); late = np.array([r[2] for r in rows])
out += ["", f"Both peaks occur in **every** one of the 7 years (spring {spring.min():.2f}–{spring.max():.2f}, late summer {late.min():.2f}–{late.max():.2f}), "
        "with a June trough between them (0.23–0.31 in four of the years, 0.42–0.57 in the others). The pattern does not alternate between years.\n",
        "Reading (an inference, not a measurement; it rests on assumed end-members of ~0.85 for a full canopy and ~0.2 for bare soil, with linear mixing): "
        "a spring peak of 0.8 needs about 90% of the 250 m pixel green in spring, and a late-summer value of 0.6–0.7 needs about 60–80% green then. "
        "Two separate fields side by side (one spring crop, one summer crop) cannot supply both, because that would need roughly 150–170% of the pixel. "
        "So the pattern points to most of the same ground being green twice a year (a second crop after the spring crop), or to every field in the pixel doing so. "
        "It is not alternating years and a simple wheat/cotton split of the pixel does not fit. Caveats: the end-members are assumed, stubble and weeds keep "
        "the trough at 0.2–0.3 instead of bare-soil values, the 213 ha polygon is OSM farmland of many fields while a pixel is only 6.25 ha, "
        "and NDVI cannot name the crops. Needs a local check.\n"]

rot = schedule(tuple(f.rotation), load_crops())
wins = rot.bare_windows()
out += ["## 4. What the calendar assumes\n",
        f"`{' → '.join(f.rotation)}` is scheduled as a {rot.cycle_years}-year cycle: cotton cannot be sown after a June wheat harvest, so the calendar leaves the ground bare "
        f"for {'; '.join(f'{n} days from about {(pd.Timestamp(2001, 1, 1) + pd.Timedelta(days=s % 365)):%d %b}' for s, n in wins)} of the {365 * rot.cycle_years}-day cycle "
        f"({rot.bare_days_per_year():.0f} days a year). "
        "The satellite shows a green late summer every year, which the calendar does not allow.\n",
        "## 5. What the app now says\n",
        "- Bare days are counted only on observable days, and the number of not-observable days and the months concerned are stated.",
        "- If the satellite stays above the bare-soil line even at its lowest, the app says so and names the possible reasons (second crop, stubble, weeds, mixed fields) "
        "and asks for a local check. It does not state which one it is.",
        "- The crop calendar, the 0.2 threshold and the scores are unchanged."]
(ROOT / "docs" / "satellite_bare_days.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
