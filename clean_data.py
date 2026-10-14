"""Clean the Guttmacher state-level abortion dataset for DSC106 Project 2."""
import pandas as pd
import numpy as np

SRC = "GuttmacherInstituteAbortionDataByState.xlsx"
OUT = "abortion_clean.csv"

RENAME = {
    "U.S. State": "state",
    "% change in abortion rate, 2017-2020": "pct_chg_abortion_rate_2017_2020",
    "% change in the no. of abortion clinics, 2017-2020": "pct_chg_clinics_2017_2020",
    "% change in the no. of abortion providers, 2014-2017": "pct_chg_providers_2014_2017",
    "% of all U.S. abortions, by state of occurrence, 2020": "pct_us_abortions_occurrence_2020",
    "% of counties without a known abortion provider, 2014": "pct_counties_no_provider_2014",
    "% of counties without a known clinic, 2020": "pct_counties_no_clinic_2020",
    "% of residents obtaining abortions who traveled out of state for care, 2020": "pct_traveled_out_of_state_2020",
    "% of women aged 15-44 living in a county without a clinic, 2020": "pct_women_no_clinic_2020",
    "% of women aged 15-44 living in a county without an abortion provider, 2014": "pct_women_no_provider_2014",
    "Abortion rate (the no. of abortions per 1,000 women aged 15-17), by state of residence, 2017": "rate_15_17_2017",
    "Abortion rate (the no. of abortions per 1,000 women aged 15-19), by state of residence, 2017": "rate_15_19_2017",
    "Abortion rate (the no. of abortions per 1,000 women aged 18-19), by state of residence, 2017": "rate_18_19_2017",
    "Change in the no. of abortion clinics, 2017-2020": "chg_clinics_2017_2020",
    "Change in the no. of abortion providers, 2014-2017": "chg_providers_2014_2017",
    "No. of abortion clinics, 2020": "clinics_2020",
    "No. of abortion providers, 2017": "providers_2017",
    "No. of abortions among women aged 15-17, by state of residence, 2017": "abortions_15_17_2017",
    "No. of abortions among women aged 15-19, by state of residence, 2017": "abortions_15_19_2017",
    "No. of abortions among women aged 18-19, by state of residence, 2017": "abortions_18_19_2017",
    "No. of abortions among women younger than 15, by state of residence, 2017": "abortions_under_15_2017",
    "No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020": "rate_occurrence_2020",
    "No. of abortions per 1,000 women aged 15–44, by state of residence, 2020": "rate_residence_2020",
    "No. of abortions, by state of occurrence, 2020": "abortions_occurrence_2020",
    "No. of abortions, by state of residence, 2020": "abortions_residence_2020",
    "No. of federally funded abortions, 2010": "federally_funded_abortions_2010",
    "No. of state funded abortions, 2010": "state_funded_abortions_2010",
    "Reported public expenditures for abortions (in 000s of dollars), federal, 2015": "public_exp_federal_2015_k",
    "Reported public expenditures for abortions (in 000s of dollars), state, 2015": "public_exp_state_2015_k",
    "Total no. of publicly funded abortions , 2010": "total_publicly_funded_abortions_2010",
    "Total reported public expenditures for abortions (in 000s of dollars), 2015": "total_public_exp_2015_k",
}

ABBR = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO",
    "Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL","Georgia":"GA",
    "Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY",
    "Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN",
    "Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH",
    "New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND",
    "Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI",
    "South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
    "Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY",
}

# Strings Guttmacher uses for missing/suppressed values (see the metadata sheet).
MISSING = {"unavailable", "u", "nr", "n/a", "na", "", "-", "--", "*"}


def to_number(v):
    """Return a float, or NaN for any of Guttmacher's missing/suppressed markers."""
    if pd.isna(v):
        return np.nan
    if isinstance(v, (int, float, np.number)):
        return float(v)
    s = str(v).strip().replace(",", "")
    if s.lower() in MISSING:
        return np.nan
    if s.startswith("<"):      # "<1,000" = suppressed small cell, not a usable number
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


df = pd.read_excel(SRC, sheet_name="Guttmacher", header=0)
df.columns = [str(c).strip() for c in df.columns]

unmapped = [c for c in df.columns if c not in RENAME]
if unmapped:
    raise SystemExit(f"Unmapped columns, update RENAME: {unmapped}")

df = df.rename(columns=RENAME)
df["state"] = df["state"].astype(str).str.strip()

for c in df.columns:
    if c != "state":
        df[c] = df[c].map(to_number)

df.insert(1, "state_abbr", df["state"].map(ABBR))
if df["state_abbr"].isna().any():
    raise SystemExit(f"No abbreviation for: {df.loc[df.state_abbr.isna(),'state'].tolist()}")

# Women aged 15-44 per state, back-derived from the two 2020 residence columns:
#   rate = abortions per 1,000 women  ->  women = abortions / rate * 1000
# Needed for population-weighted national figures (an unweighted mean across 51
# states over-weights small states). National total validates at ~64.5M vs ~65M actual.
df["women_15_44_2020"] = (
    df["abortions_residence_2020"] / df["rate_residence_2020"] * 1000
).round(0)

df = df.sort_values("state").reset_index(drop=True)
df.to_csv(OUT, index=False)

print(f"wrote {OUT}: {df.shape[0]} rows x {df.shape[1]} cols")
print(f"derived women 15-44 national total: {df.women_15_44_2020.sum()/1e6:.1f}M")
print("\nmissing values per column (blank = complete):")
miss = df.drop(columns=["state", "state_abbr"]).isna().sum()
for c, n in miss.items():
    print(f"  {c:40s} {n:2d}" + ("   <-- unusable" if n > 15 else ""))
