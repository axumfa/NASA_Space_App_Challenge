# Satellite vs calendar bare days, Fergana demo field (40.4229, 71.7576)

Source: `demo-points-MOD13Q1-061-results.csv`, MOD13Q1.061 250 m NDVI, 2019–2026, 180 composites. Diagnosis only: no threshold or calendar was changed.

## 1. By calendar month (all years pooled)

| month | composites | pass QA | rejected | median NDVI (passing) | min NDVI (passing) | median NDVI (all, unfiltered) |
|---|---|---|---|---|---|---|
| Jan | 16 | 3 | 13 | 0.29 | 0.27 | 0.23 |
| Feb | 16 | 5 | 11 | 0.33 | 0.26 | 0.26 |
| Mar | 16 | 11 | 5 | 0.50 | 0.30 | 0.47 |
| Apr | 16 | 15 | 1 | 0.71 | 0.50 | 0.68 |
| May | 16 | 16 | 0 | 0.56 | 0.39 | 0.56 |
| Jun | 16 | 14 | 2 | 0.33 | 0.23 | 0.36 |
| Jul | 16 | 16 | 0 | 0.46 | 0.38 | 0.46 |
| Aug | 16 | 16 | 0 | 0.61 | 0.43 | 0.61 |
| Sep | 16 | 15 | 1 | 0.53 | 0.33 | 0.53 |
| Oct | 10 | 8 | 2 | 0.33 | 0.23 | 0.35 |
| Nov | 12 | 8 | 4 | 0.30 | 0.14 | 0.29 |
| Dec | 14 | 7 | 7 | 0.35 | 0.20 | 0.26 |

Dec–Feb: 15 of 46 composites pass QA. All rejected winter composites carry pixel reliability 3 (snow/ice) and fail the VI_Quality cloud/snow bits.

## 2. How failed observations are treated

- Rejected composites are removed (not counted as bare, not counted as not bare).
- The old count (`observed_bare_days_per_year`) then **interpolated linearly across the gaps**; a winter with only 1–3 clear dates was filled in from those few clear (never snow-covered) values, so it could only say 0.
- The count now (`observed_bare_summary`) skips (a) days more than 24 days from a passing observation and (b) every calendar month in which fewer than half of the composites pass QA. Those days are reported as **not observable**, never as 0 bare days.
- Fergana result: bare days on observable days = **0** per year; **90** days a year not observable; poorly observed months: Jan, Feb, Dec.

## 3. Do the two peaks fall in the same year?

| year | Mar–May max (date) | June min | Jul–Sep max (date) | Oct–Dec median | Jan–Feb median |
|---|---|---|---|---|---|
| 2019 | 0.83 (04-23) | 0.42 | 0.54 (09-30) | 0.24 | – |
| 2020 | 0.82 (04-22) | 0.31 | 0.71 (08-12) | 0.24 | 0.33 |
| 2021 | 0.81 (05-09) | 0.28 | 0.61 (08-29) | 0.23 | – |
| 2022 | 0.75 (04-23) | 0.23 | 0.63 (08-13) | 0.39 | 0.29 |
| 2023 | 0.60 (05-25) | 0.47 | 0.72 (09-14) | 0.40 | 0.29 |
| 2024 | 0.83 (04-22) | 0.30 | 0.63 (08-28) | 0.31 | 0.32 |
| 2025 | 0.65 (04-07) | 0.57 | 0.62 (08-29) | 0.35 | 0.32 |

Both peaks occur in **every** one of the 7 years (spring 0.60–0.83, late summer 0.54–0.72), with a June trough between them (0.23–0.31 in four of the years, 0.42–0.57 in the others). The pattern does not alternate between years.

Reading (an inference, not a measurement; it rests on assumed end-members of ~0.85 for a full canopy and ~0.2 for bare soil, with linear mixing): a spring peak of 0.8 needs about 90% of the 250 m pixel green in spring, and a late-summer value of 0.6–0.7 needs about 60–80% green then. Two separate fields side by side (one spring crop, one summer crop) cannot supply both, because that would need roughly 150–170% of the pixel. So the pattern points to most of the same ground being green twice a year (a second crop after the spring crop), or to every field in the pixel doing so. It is not alternating years and a simple wheat/cotton split of the pixel does not fit. Caveats: the end-members are assumed, stubble and weeds keep the trough at 0.2–0.3 instead of bare-soil values, the 213 ha polygon is OSM farmland of many fields while a pixel is only 6.25 ha, and NDVI cannot name the crops. Needs a local check.

## 4. What the calendar assumes

`winter_wheat → cotton` is scheduled as a 2-year cycle: cotton cannot be sown after a June wheat harvest, so the calendar leaves the ground bare for 300 days from about 15 Jun of the 730-day cycle (155 days a year). The satellite shows a green late summer every year, which the calendar does not allow.

## 5. What the app now says

- Bare days are counted only on observable days, and the number of not-observable days and the months concerned are stated.
- If the satellite stays above the bare-soil line even at its lowest, the app says so and names the possible reasons (second crop, stubble, weeds, mixed fields) and asks for a local check. It does not state which one it is.
- The crop calendar, the 0.2 threshold and the scores are unchanged.
