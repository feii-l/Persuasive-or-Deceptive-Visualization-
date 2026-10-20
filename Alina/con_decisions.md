# Con visualization — caption and design decisions

Chart file: `con_1_hero.png` · Script: `make_con_chart.py`

## Caption

> **Most American women live in a county that has a clinic.** Among U.S. women aged
> 15–44, 62.5% live in a county with at least one abortion clinic, weighted by each
> state's female population across the 50 states and DC. Below, of the people who
> obtained an abortion in 2020, 88% did so without leaving their state.
> Source: Guttmacher Institute, 2020.

## Design decisions

Scored from **−2 (fully deceptive)** to **+2 (fully earnest)**.

### 1. Counting women rather than counties — **−1.5**

The same dataset gives two very different answers: 77.9% of counties have no clinic,
but only 37.5% of women live in such a county. Counties are a unit of land and most of
them are rural and nearly empty, so the women-based measure is arguably the more
relevant one when the proposition is about people. We chose it because it produced the
number we wanted, not because we settled the measurement question first — the pro side
made the opposite choice from the same two columns. We considered showing both measures
side by side (we built a connected dot plot that did exactly that) and rejected it
because disclosing the gap undercut our own argument.

### 2. Stating the share who *have* access rather than who do not — **−1**

The chart leads with "62.5% live in a county with a clinic" instead of "37.5% do not."
The arithmetic is identical and nothing is hidden, but readers anchor on the headline
number, and a figure above half reads as reassuring. We tried the inverse headline and
the same chart felt like an argument for the other side, which is how we knew the
framing rather than the data was doing the work.

### 3. Leaving the absolute number out — **−1.5**

37.5% of 64.5 million women is roughly **24 million people** without a clinic in their
county. The figure never says so. A percentage below half feels tolerable; "24 million
women" does not, and we expect this omission persuades more than any visual choice on
the page. We discussed adding it as a footnote and decided against it, which is the
single least honest decision in this figure.

### 4. Weighting by population instead of averaging the states — **+2**

A plain mean of the 51 state values treats Wyoming and California as equal and returns
45.7%. We recovered each state's number of women aged 15–44 from two columns
(abortions ÷ abortion rate × 1,000; the national total comes to 64.5 million against
roughly 65 million actual) and weighted by it, giving 37.5% — the population-weighted
national figure. This is the more defensible method and it also happens to favour our
side, which is worth saying out loud rather than quietly banking.

### 5. Dropping "within reach" and adding a travel measure — **+2**

The first version was headlined "Most American women live **within reach** of a clinic"
and the legend read "no clinic **nearby**." Feedback pointed out that both words imply
travel distance, which this dataset does not measure at all — a county can be larger
than a small state, so "a clinic somewhere in my county" is not the same as "a clinic
close to me." We rewrote the headline to say literally what the data says, and rather
than drop the question we answered it with the one behavioural column available: 88% of
people who obtained an abortion in 2020 did so without crossing a state line. We also
flag in the figure that the two measures cover different groups — all women aged 15–44
for the 62.5%, only those who obtained an abortion for the 88% — because sliding
between two populations inside one figure would otherwise be a fourth deceptive move.

### Unit chart form — *(supporting note, not a separate decision)*

100 equal squares, one per percent, with a legend naming both colours. No truncated
axis, no area encoding. The squares round 62.5 up to 63; the exact figure is printed
beside them, so the rounding is visible rather than concealed.
