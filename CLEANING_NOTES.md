# Data cleaning notes — Project 2

Source: `GuttmacherInstituteAbortionDataByState.xlsx`, sheet `Guttmacher`.
Output: `abortion_clean.csv` (51 rows = 50 states + DC, 33 columns).
Reproduce with: `python clean_data.py`

**Everyone must use `abortion_clean.csv`, not the raw xlsx**, so both sides of the
argument are computed from identical numbers.

## What the script does

1. **Renamed columns** to short snake_case names. The year is kept in every name
   (e.g. `pct_counties_no_clinic_2020`) because this dataset is cross-sectional —
   there is no time column, and different columns are from different years
   (2010, 2014, 2015, 2017, 2020). Do not plot two different years as a trend.
2. **Converted every value column to a number.** The raw file mixes text markers
   into numeric columns: `unavailable`, `u`, `nr` (no response), `n/a`, and
   `<1,000` (suppressed because the cell size was small). All become `NaN`.
   `<1,000` is dropped rather than treated as e.g. 500 — we do not know the value.
3. **Added `state_abbr`** (two-letter codes) for choropleth maps.
4. **Added `women_15_44_2020`**, back-derived as
   `abortions_residence_2020 / rate_residence_2020 * 1000`.
   The rate is per 1,000 women aged 15–44, so this recovers the denominator.
   Validation: the national total comes to 64.5M against roughly 65M actual, so
   the derivation is sound.

## Why `women_15_44_2020` matters

A plain `.mean()` across the 51 rows treats Wyoming and California as equally
important. Weighting by women aged 15–44 gives the real national figure:

| Measure | Value |
|---|---|
| % of women in a county with no clinic — unweighted state mean | 45.7% |
| % of women in a county with no clinic — **population-weighted** | **37.5%** |
| % of women in a county **with** a clinic — population-weighted | **62.5%** |
| % of **counties** with no clinic — unweighted mean | 77.9% |

Weighted figures:
```python
w = df.women_15_44_2020
(df.pct_women_no_clinic_2020 * w).sum() / w.sum()
```

## Data completeness

Every column either side of the argument needs is **100% complete** (0 missing):
`pct_counties_no_clinic_2020`, `pct_women_no_clinic_2020`,
`pct_chg_clinics_2017_2020`, `clinics_2020`, `rate_occurrence_2020`,
`rate_residence_2020`, `pct_traveled_out_of_state_2020`, `women_15_44_2020`.

Columns with heavy missingness — avoid these:
`rate_15_17_2017` (15), `rate_18_19_2017` (15), `abortions_15_17_2017` (15),
`abortions_18_19_2017` (15), `abortions_under_15_2017` (14),
`total_public_exp_2015_k` (14), `state_funded_abortions_2010` (9),
`public_exp_state_2015_k` (9).

## For the write-up

Two cleaning choices are themselves design decisions worth scoring:

- **Dropping `<1,000` instead of imputing a value.** Earnest (+2) — inventing a
  number would fabricate data.
- **Weighting by population instead of averaging states.** Earnest (+2) — the
  unweighted mean over-represents small states. Note that here the more rigorous
  method also happens to produce the number that favours the "access is not that
  restricted" side, which is worth saying out loud in the reflection.
