# Mobile Vaccine Campaign and Outbreak Response Delay in Border Municipalities

## Metadata

- Paper ID: `epi_a_0018`
- Version: `v1`
- Track: `Health Equity & Policy`
- Method: `Synthetic Control`
- Generated at: `2026-02-22T16:18:56+00:00`

## Abstract

This paper evaluates a policy intervention in an epidemiology setting using a pre-registered quasi-experimental design.
The objective is to estimate causal impacts on health outcomes and quantify distributional effects across vulnerable groups.
The manuscript follows a reproducibility-first workflow with explicit assumptions, falsification tests, and policy-relevant heterogeneity analysis.

## Policy Question

How does the intervention affect the selected health outcome, and through which equity channels are effects distributed?

## Identification Strategy

Primary design: **Synthetic Control**.

Planned checks:

1. Event-time dynamics
2. Placebo or falsification tests
3. Heterogeneity by socioeconomic vulnerability
4. Sensitivity to alternative clustering levels

## Data Sources

- Public health surveillance source (declared in `data/DATA_MANIFEST.md`)
- Policy implementation registry and treatment timing records
- Geospatial and demographic covariates for confounding control

## Main Specification

The baseline model estimates policy effects with fixed effects and clustered standard errors at the treatment-assignment unit.
The design includes pre-trend diagnostics and event-time coefficients to assess parallel trends.

## Robustness Plan

1. Alternative treatment timing windows.
2. Alternative clustering levels and wild bootstrap checks.
3. Placebo intervention dates.
4. Alternative sample restrictions and outlier handling.

## Limitations (Preliminary)

- Potential measurement error in administrative coding.
- Potential spillovers across geographic boundaries.
- External validity may be limited outside observed settings.

## Reproducibility

Run analysis script:

```bash
Rscript scripts/analysis.R
```

Artifacts expected after successful run:

- `outputs/main_estimates.csv`
- `outputs/event_study.csv`
- `outputs/specification_log.json`
