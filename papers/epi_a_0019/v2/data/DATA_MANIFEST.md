# Data Manifest - epi_a_0019 v2

## Primary datasets

| Dataset | Source URL | Unit | Coverage | License / Access | Role in Analysis |
|---|---|---|---|---|---|
| CDC WONDER Multiple Cause of Death | `https://wonder.cdc.gov/mcd-icd10-expanded.html` | County-year | 2009-2023 | Public query system (terms apply) | Mortality outcomes (amenable and all-cause, age 25-64) |
| KFF Medicaid Expansion Tracker | `https://www.kff.org/medicaid/issue-brief/status-of-state-medicaid-expansion-decisions-interactive-map/` | State-year | 2010-2023 | Public | Expansion timing and treatment exposure anchor |
| ACS 5-year County Tables | `https://www.census.gov/programs-surveys/acs` | County-year | 2009-2023 | Public | Demographic and socioeconomic controls |
| AHRF (Area Health Resources Files) | `https://data.hrsa.gov/topics/health-workforce/ahrf` | County-year | 2009-2023 | Public download with attribution | Health system capacity covariates |
| Census TIGER/Line Counties | `https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html` | County polygons | Reference vintages | Public | Border adjacency construction |
| BEA Regional Income and Employment | `https://www.bea.gov/data/income-saving/personal-income-county-metro-and-other-areas` | County-year | 2009-2023 | Public | Income controls and macro confounding checks |

## Constructed analytic files

| File | Created by | Description | Required Columns |
|---|---|---|---|
| `data/panel.csv` | `scripts/build_panel.R` (to be maintained) | County-year analytic panel in non-expansion and comparison states | `county_fips,state_fips,year,amenable_mortality_25_64,allcause_mortality_25_64,population_25_64,nonexp_state` |
| `data/border_exposure.csv` | `scripts/build_border_exposure.R` (to be maintained) | County exposure to adjacent expansion timing | `county_fips,adjacent_expansion_year,is_border_county,commuting_share_crossborder` |

## Data quality checks

1. County FIPS harmonization across boundary changes.
2. Year-over-year continuity checks for mortality coding revisions.
3. Missingness report for outcome and population denominators.
4. Verification that treatment timing uses policy implementation year, not announcement year.

## Reproducibility note

All transformations that produce `panel.csv` and `border_exposure.csv` must be script-generated and committed with deterministic seeds where relevant.
