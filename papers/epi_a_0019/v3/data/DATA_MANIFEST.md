# Data Manifest - epi_a_0019 v3

## Raw source datasets

| Dataset | Source | Unit | Years | Access |
|---|---|---|---|---|
| CDC WONDER Multiple Cause of Death | `https://wonder.cdc.gov/mcd-icd10-expanded.html` | county-year | 2009-2023 | public query portal |
| KFF Medicaid Expansion Tracker | `https://www.kff.org/medicaid/issue-brief/status-of-state-medicaid-expansion-decisions-interactive-map/` | state-year | 2010-2023 | public |
| ACS 5-year estimates | `https://www.census.gov/programs-surveys/acs` | county-year | 2009-2023 | public |
| AHRF | `https://data.hrsa.gov/topics/health-workforce/ahrf` | county-year | 2009-2023 | public |
| Census TIGER/Line counties | `https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html` | polygon/county | reference vintages | public |
| BEA regional economic data | `https://www.bea.gov/data/income-saving/personal-income-county-metro-and-other-areas` | county-year | 2009-2023 | public |

## Derived analytic files and schemas

| File | Required Fields |
|---|---|
| `data/panel.csv` | `county_fips,state_fips,year,amenable_mortality_25_64,allcause_mortality_25_64,population_25_64,nonexp_state` |
| `data/border_exposure.csv` | `county_fips,adjacent_expansion_year,is_border_county,commuting_share_crossborder` |

## Validation checklist

1. FIPS harmonization log complete.
2. Missingness rates documented by variable-year.
3. Expansion timing source cross-verified against archived snapshots.
4. Border adjacency matrix checksum stored.
