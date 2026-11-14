## Reading the results honestly

Two checks **fail** or only **partly pass**, and one initial failure was a flaw in the check, not in the model.

- **A (cotton highest irrigation demand): FAIL in both fields.** Cotton is second in Fergana (sugar beet is higher) and third in Kansas
  (sugar beet and the 330-day alfalfa stand are higher). The model multiplies FAO-56 Kc by reanalysis ET0 over each crop's season, and
  sugar beet (Kc mid 1.20, 180 days) and a near-year-round alfalfa stand simply use more water than a 180-day cotton crop on that arithmetic.
  I did not change any crop value to rescue the expectation. The expectation itself may have been too strong; what the check cannot
  tell us is whether cotton's absolute demand (about 1,000 mm in Fergana) is realistic: reanalysis ET0 likely runs high there.
- **B (legume insertion raises soil subscores): PARTIAL.** Nitrogen rises in every legume option. Organic matter and erosion cover rise
  only in some, and **every** option where they do not rise is one that lengthens the rotation cycle from 2 to 3 years: a crop that cannot
  be sown in the same year pushes the cycle out, and the extra months are bare, which dilutes the per-year subscores. That is a property of
  how the model normalises per year of cycle, and it may over-penalise such options; it is not a data error, and I have not changed it.
- **C (water-first prefers lower-ETc rotations): PASS** in both fields (rank correlation +0.72 and +0.90; the winners need markedly less water than the current rotation).
- **D (reduced supply hurts high-Ky crops most): PARTIAL.** The identity yield loss = Ky × relative ET deficit holds exactly, but the
  *ranking* of crops by loss follows how irrigation-dependent the crop is (the deficit) more than Ky, so crops with Ky ≥ 1.05 do not lose
  more than crops with Ky ≤ 0.90 (30% vs 30% in Fergana, 4% vs 5% in Kansas). The expectation as worded mixes Ky with total exposure; the conditional
  statement (for equal deficit, higher Ky loses more) is true by construction and therefore not an independent test.
- **E (bare window after harvest): PASS.** The first version of this check required a bare window after every harvest and failed Fergana
  because wheat is sown straight after cotton. The rule was corrected to the stated expectation (a window follows a harvest when the next sowing is
  at least 45 days away, and not otherwise); the model output is unchanged.

**What this does not show.** No measured yields, water use or soil data were available, so none of this validates absolute numbers. These checks
only show that the model behaves in the directions that agronomic reasoning predicts (C, E, most of B) and expose where its structure produces
results a reader might not expect (A, the cycle-length effect in B, the Ky ranking in D).
