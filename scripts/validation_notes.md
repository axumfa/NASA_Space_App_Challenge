## Reading the results honestly

Some checks only **partly pass**; none was tuned to pass.

- **A (cotton needs more irrigation than winter wheat and the grain legumes; alfalfa and sugar beet higher): PARTIAL in Fergana, PASS in Kansas.**
  Cotton is above winter wheat and every feasible grain legume in both fields. In Kansas alfalfa and sugar beet are both above cotton. In Fergana sugar beet
  is above cotton, but **alfalfa is not on irrigation need (930 mm vs 977 mm)**. Alfalfa's *crop water use* (ETc 1,108 mm) is above cotton's (1,034 mm), as expected; its
  330-day season also catches more effective rain (autumn to spring), which lowers the irrigation it needs. The expectation therefore holds for water use, not for irrigation need.
  (The first version of this check asked for cotton to be the highest of all crops; that wording was wrong and was replaced by this one.)
- **B (legume insertion raises the soil subscores): PARTIAL.** Nitrogen rises in every legume option. Organic matter and erosion cover rise only when the added
  legume fits inside the existing calendar (for example mung bean after wheat harvest). Every option where they fall lengthens the rotation from 2 to 3 years. The worked example
  above shows by hand that this is **not an averaging artefact**: over an equal horizon the longer rotation also returns less organic-matter input and less cover (the new crop
  occupies ~110 days of an extra 365, and the main crops are grown less often), and it leaves more bare soil. A sensitivity that credits 60 days of post-harvest residue cover does
  not remove the difference. **The model was not changed, so no rankings changed.** One limitation remains: the soil subscores credit a crop only for its days in the field
  (not for residue or roots after harvest), which may understate short crops.
- **C (water-first prefers lower-ETc rotations): PASS** in both fields (rank correlation +0.72 and +0.90; the winners need markedly less water than the current rotation).
- **D (reduced supply hurts high-Ky crops most): PARTIAL.** The identity yield loss = Ky × relative ET deficit holds exactly, but the *ranking* of crops by loss follows how
  irrigation-dependent the crop is (the deficit) more than Ky, so crops with Ky ≥ 1.05 do not lose more than crops with Ky ≤ 0.90. The expectation as worded mixes Ky with total
  exposure; the conditional statement (for equal deficit, higher Ky loses more) is true by construction and therefore not an independent test.
- **E (bare window after harvest): PASS.** The first version of this check required a bare window after every harvest and failed Fergana because wheat is sown straight after cotton.
  The rule was corrected to the stated expectation (a window follows a harvest when the next sowing is at least 45 days away, and not otherwise); the model output is unchanged.

**What this does not show.** No measured yields, water use or soil data were available, so none of this validates absolute numbers. These checks only show that the model behaves in the
directions that agronomic reasoning predicts (A, C, E, most of B) and expose where its structure produces results a reader might not expect (alfalfa's irrigation need, the cycle-length
effect in B, the Ky ranking in D).
