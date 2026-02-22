# Cross-Border Spillovers of Medicaid Expansion: Mortality Effects in Non-Expansion Border Counties

## Metadata

- Paper ID: `epi_a_0019`
- Version: `v2`
- Track: `Social & Spatial EPI`
- Method: `Event Study Difference-in-Differences`
- Round: `Manual Mode Round 1`
- Draft date: `2026-02-22`

## Abstract

Most evidence on Medicaid expansion focuses on direct effects inside expansion states. This paper studies a different margin: whether expansion policies generate cross-border spillovers in neighboring non-expansion counties. The setting is policy-fragmented US geography, where residents can work, seek care, and interact across state lines, potentially transmitting health system effects beyond treated jurisdictions.

We build a county-year panel and estimate event-study difference-in-differences models that compare non-expansion border counties with interior non-expansion counties in the same states. The primary estimands are changes in amenable mortality and all-cause mortality among adults aged 25-64. Identification relies on staggered exposure to adjacent-state expansion timing, with county fixed effects, state-by-year fixed effects, and clustered inference.

The contribution is conceptual and empirical. Conceptually, we reframe Medicaid expansion as a regional policy shock with potential externalities, not only a within-state treatment. Empirically, we provide a transparent design that tests pre-trends, migration-based compositional concerns, and border-specific confounding, while preserving policy relevance for federal-state coordination.

## 1. Contribution and Novelty

This paper targets a gap between two literatures: causal estimates of Medicaid expansion and place-based spillover effects. Prior top-journal work has established important direct effects of public insurance on outcomes and mortality, but evidence on untreated neighboring counties remains limited. Our design isolates whether proximity to expansion itself produces measurable health effects outside formal treatment boundaries.

The novelty is not a new estimator for its own sake. The novelty is the treatment definition and comparison architecture. We treat policy adjacency as exposure intensity and estimate event-time responses among counties that remain in non-expansion states, which allows policy-relevant inference for jurisdictions that did not adopt expansion.

## 2. Positioning Against Benchmark Literature

We explicitly emulate the empirical discipline of leading papers in economics and health policy while extending scope to cross-border spillovers.

- Finkelstein et al. (2012, QJE) for transparent outcome architecture and design logic.
- Goodman-Bacon (2017, JPE) for mortality-focused public insurance identification.
- Finkelstein, Hendren, and Luttmer (2018, JPE) for welfare interpretation discipline.
- Dobkin et al. (2018, AER) for high-quality health economics execution standards.
- Frean, Gruber, and Sommers (2017, JHE) for ACA policy decomposition.
- Lee, Dodge, and Terrault (2021, Lancet Public Health) for mortality heterogeneity framing.

## 3. Institutional Setting and Hypotheses

After 2014, Medicaid expansion adoption varied across states and years. Non-expansion states often border expansion states, creating plausible exposure channels for untreated counties: cross-border hospital utilization, provider labor reallocation, uncompensated care spillovers, and informal network diffusion regarding insurance take-up behavior.

Hypotheses:

1. Border counties in non-expansion states experience mortality changes after adjacent-state expansion, relative to interior counties in the same non-expansion states.
2. Effects are larger where baseline hospital market integration across the border is higher.
3. Effects are stronger for amenable causes than for external causes of death.

## 4. Data and Sample Construction

Unit of observation is county-year for contiguous US counties. Core study period is 2009-2023, providing a balanced pre-period and post-period around staggered expansion timing.

Data blocks:

- Mortality outcomes from CDC WONDER county-year files.
- Policy timing from KFF Medicaid expansion tracker.
- Demographic controls from ACS and intercensal population estimates.
- Health system covariates from AHRF and hospital market files.
- Geographic adjacency from Census TIGER/Line county boundary products.

Sample rules:

- Keep counties in non-expansion states.
- Define treated exposure as county bordering at least one expansion state.
- Interior controls are non-border counties in the same non-expansion states.
- Exclude counties with unstable boundary coding over sample.

## 5. Estimands and Empirical Strategy

Primary estimand is dynamic ATT in event time relative to adjacent-state expansion year.

Baseline equation (conceptual):

outcome_ct = sum_{k != -1} beta_k * 1[event_time_ct = k] * exposed_c + alpha_c + gamma_st + X_ct' theta + eps_ct

where:

- c indexes counties, t indexes years, s indexes states.
- alpha_c are county fixed effects.
- gamma_st are state-by-year fixed effects.
- exposed_c identifies non-expansion border counties.
- standard errors clustered at state level, with alternative clustering checks.

## 6. Identification Assumptions and Diagnostics

Key identifying condition is that, absent adjacent-state expansion, outcome trends in border and interior counties within the same non-expansion states would have evolved in parallel after conditioning on fixed effects and controls.

We pre-register diagnostics:

1. Joint pre-trend tests in event-study leads.
2. Border-specific linear trend adjustments.
3. Placebo event years assigned to pre-period.
4. Leave-one-border-state-out sensitivity.

## 7. Execution Standards

To align with top-journal expectations:

- Inference uses clustered standard errors at policy variation level.
- We report coefficient paths with confidence intervals, not only post averages.
- Main and robustness estimates use identical outcome definitions.
- Data construction and exclusions are logged in machine-readable metadata.

## 8. Robustness and Falsification Suite

Mandatory checks in this draft:

1. Alternative treated definitions by border length and commuting intensity.
2. Alternative control sets (interior-only, matched interior, synthetic interior).
3. Wild cluster bootstrap p-values for small treated-state counts.
4. Exposure timing perturbation (+/-1 year).
5. Negative-control outcomes with weaker insurance sensitivity.
6. County population re-weighting sensitivity.
7. Exclusion of major metro outliers.
8. Border discontinuity variant for near-border pairs.

## 9. Heterogeneity and Mechanisms

We plan stratified estimates by baseline uninsurance, hospital bed supply, and provider density. Mechanism analysis focuses on preventable hospitalization and insurance-sensitive mortality categories where coding allows consistent county-year panels.

## 10. Scope and Interpretation Discipline

This paper estimates reduced-form policy adjacency effects, not individual treatment effects of insurance enrollment. We avoid claims about welfare magnitudes unless mechanism evidence is coherent and exposure channels are empirically supported. External validity is limited to the observed policy period and border structure.

## 11. Policy Relevance

Results inform intergovernmental design questions: if expansion creates cross-border benefits, then state-level non-adoption can still be partially affected by neighboring policy choices. This matters for federal matching design, interstate compacts, and regional health planning where fiscal incidence and health incidence may diverge.

## 12. Reproducibility

Run baseline pipeline:

```bash
Rscript scripts/analysis.R
```

Expected artifacts:

- `outputs/main_event_study.csv`
- `outputs/main_twfe.csv`
- `outputs/robust_placebo.csv`
- `outputs/specification_log.json`

## References (Benchmark Set)

1. Finkelstein, A., Taubman, S., Wright, B., et al. (2012). *The Oregon Health Insurance Experiment: Evidence from the First Year*. QJE. DOI: `10.1093/qje/qjs020`
2. Goodman-Bacon, A. (2017). *Public Insurance and Mortality: Evidence from Medicaid Implementation*. JPE. DOI: `10.1086/695528`
3. Finkelstein, A., Hendren, N., Luttmer, E. (2018). *The Value of Medicaid*. JPE. DOI: `10.1086/702238`
4. Dobkin, C., Finkelstein, A., Kluender, R., Notowidigdo, M. (2018). *The Economic Consequences of Hospital Admissions*. AER. DOI: `10.1257/aer.20161038`
5. Frean, M., Gruber, J., Sommers, B. (2017). *Premium subsidies, the mandate, and Medicaid expansion*. JHE. DOI: `10.1016/j.jhealeco.2017.02.004`
6. Lee, B., Dodge, J., Terrault, N. (2021). *Medicaid expansion and variability in mortality in the USA*. Lancet Public Health. DOI: `10.1016/S2468-2667(21)00252-8`
7. Chetty, R., Hendren, N., Katz, L. (2016). *The Effects of Exposure to Better Neighborhoods on Children*. AER. DOI: `10.1257/aer.20150572`
8. Ruhm, C. (2000). *Are Recessions Good for Your Health?* QJE. DOI: `10.1162/003355300554872`
