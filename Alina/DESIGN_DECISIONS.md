# Design decisions log

Fill this in **as you build**, not afterwards. The final submission needs 3–5
decisions per visualization, each scored from **−2 (fully deceptive)** to
**+2 (fully earnest)** in 0.5 steps, with a couple of sentences on rationale,
what worked, and what else you considered. Use 0 only if genuinely undecided.

Proposition: **"Access to abortion care in the United States is severely restricted."**

---

## CON side — Alina — Viz 1: `con_1_hero.png`

Claim: *Most American women live within reach of a clinic (62.5%).*

| # | Decision | Score | Notes |
|---|---|---|---|
| 1 | **Counted women, not counties.** Used `pct_women_no_clinic_2020` rather than `pct_counties_no_clinic_2020`. | **−1.5** | Both are in the dataset and both are true, but they answer different questions. Counties are a land unit; the proposition is about people, so the women denominator is arguably the more relevant one — which is what makes the choice defensible rather than a lie. Still deceptive on balance, because it was picked for the number it produced (45.7% vs 77.9%), not on principle. Alternative considered: showing both, which is what Viz 2 does. |
| 2 | **Weighted by state population instead of averaging the 51 rows.** | **+2** | An unweighted `.mean()` treats Wyoming and California as equal and gives 45.7%. Weighting by women aged 15–44 gives 37.5%, the real national figure. This is strictly the more correct method — and it happens to favour our side, which is worth stating plainly in the reflection. |
| 3 | **Flipped the polarity: "62.5% live WITH a clinic" rather than "37.5% live without."** | **−1** | Identical arithmetic, opposite emotional weight. Readers anchor on the number in the headline. Nothing is hidden, but the framing does the persuading. |
| 4 | **Omitted the absolute count.** 37.5% of 64.5M is roughly 24 million women. | **−1.5** | A percentage feels small; "24 million women" does not. Leaving it out is the single most persuasive choice in this figure. Considered adding it as a footnote and chose not to. |
| 5 | **Unit chart where one square = 1% of women.** Rounded 62.5 to 63 filled squares. | **+1.5** | Makes the majority tangible without distorting the scale: 100 equal squares, no truncated axis, no area encoding. The 0.5-square rounding is visible in the printed figure (62.5%) so nothing is concealed. |

## CON side — Alina — Viz 2: `con_2_gap.png`

Claim: *Counting counties overstates how many women lack access.*

| # | Decision | Score | Notes |
|---|---|---|---|
| 1 | **Showed both measures side by side as a connected dot plot.** | **+2** | This is the honest version of Viz 1's decision 1 — it discloses the county/women gap instead of exploiting it. The dumbbell form makes the size of the gap the visual subject. |
| 2 | **Selected the 10 states where the gap is largest.** | **−1.5** | Cherry-picking. The national gap is 77.9 vs 45.7 (32 points); these ten run up to 79 points (Nevada 88% vs 9%). The pattern is real everywhere, but this selection makes it look more extreme than typical. Alternative considered: all 51 states, which is unreadable at this size, or a random sample, which is weaker. |
| 3 | **x-axis runs the full 0–100%.** | **+2** | No truncation. The gap is large enough to carry itself. |
| 4 | **Blue for women, orange for counties.** | **+1** | Two hues validated for colorblind separation, plus a direct value label on every dot, so identity never depends on colour alone. |

---

## PRO side — Fei — Viz 1: *(fill in)*

Claim: …

| # | Decision | Score | Notes |
|---|---|---|---|
| 1 | **Counted counties, not women** (77.9%). | | |
| 2 | Choropleth — colour scale choice, bin cut points | | |
| 3 | | | |

## PRO side — Fei — Viz 2: *(fill in)*

Claim: …

| # | Decision | Score | Notes |
|---|---|---|---|
| 1 | **Kept only the 17 states where clinics declined**, dropping the 17 flat and 17 that grew. | | |
| 2 | **y-axis set to [−70, 0]** so every bar reads as a drop. | | |
| 3 | | | |

---

## Shared cleaning decisions (both sides)

| # | Decision | Score | Notes |
|---|---|---|---|
| 1 | Dropped `<1,000` suppressed cells rather than imputing a value. | **+2** | We do not know the value; inventing one would fabricate data. |
| 2 | Both sides computed from the same `abortion_clean.csv`. | **+2** | Guarantees the two arguments disagree about framing, not about arithmetic. |

## Note for the reflection

The 17 states that lost clinics between 2017 and 2020 include New York,
Massachusetts, New Jersey, Connecticut, Rhode Island, Maryland and Washington —
so "clinics are closing" is not simply a red-state story. Worth a sentence when
we say which side we lean toward.
