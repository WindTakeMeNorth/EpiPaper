# Cross-Border Spillovers of Medicaid Expansion: Mortality Effects in Non-Expansion Border Counties

## Metadata

- Paper ID: `epi_a_0019`
- Version: `v3`
- Track: `Social & Spatial EPI`
- Method Family: `Event-Study Difference-in-Differences with Border Exposure Design`
- Draft Type: `Full Manual Conversation-Authored Draft`
- Date: `2026-02-22`

## Abstract

The modern Medicaid expansion literature establishes substantial direct effects of insurance policy, but largely evaluates treated jurisdictions in isolation. This paper studies whether expansion creates measurable health spillovers in counties that remain outside expansion policy but are geographically and economically adjacent to expansion states. The setting is policy fragmentation in the United States, where cross-border labor markets, referral networks, and hospital capacity constraints can transmit policy incidence beyond legal eligibility boundaries.

We construct a county-year panel for 2009-2023 and define exposure among non-expansion-state counties by adjacency to expansion-state borders and expansion timing of neighboring states. The primary design is an event-study difference-in-differences framework comparing border-exposed non-expansion counties to interior non-expansion counties within the same states, with county fixed effects, state-year fixed effects, and clustered inference at the state policy variation level. Primary outcomes are amenable mortality and all-cause mortality for adults aged 25-64; secondary outcomes include insurance-sensitive utilization proxies where data permit consistent county-year measurement.

The contribution is conceptual and empirical. Conceptually, we treat Medicaid expansion as a regional treatment with externalities instead of a closed-jurisdiction intervention. Empirically, we provide a pre-registered estimation architecture that integrates pre-trend diagnostics, placebo timing tests, migration and composition checks, and sensitivity to border-market integration intensity. The design is built to match top-journal standards of identification transparency, execution discipline, and policy interpretability. Numerical treatment effects are intentionally withheld in this draft until the complete replication-grade data assembly and code audit are finalized.

## 1. Introduction

Public insurance expansion is one of the most studied policy changes in modern health economics, yet most estimates are framed as within-jurisdiction effects. That framing is useful for statutory interpretation, but it can misstate policy incidence in fragmented federations where people, providers, and institutions cross administrative boundaries daily. Medicaid expansion in the United States offers a natural case: some states expanded early, others did not, and many non-expansion counties sit directly along borders with expansion states. If insurance expansion affects provider capacity, uncompensated care, labor supply in health systems, or care-seeking geography, neighboring non-expansion counties may experience health effects despite formal non-treatment status.

This paper asks a specific question: do non-expansion border counties exhibit mortality shifts after adjacent-state expansion, relative to comparable interior counties in the same non-expansion states? The question is policy-relevant for at least three reasons. First, it changes how we interpret non-adoption. A state that does not expand may still partially absorb or benefit from neighboring expansions through spillovers, potentially biasing naive treated-versus-untreated contrasts. Second, border spillovers matter for federal matching and burden sharing; fiscal incidence and health incidence need not coincide. Third, spillovers inform regional planning under asymmetric policy adoption, where neighboring systems may become substitutes or complements over time.

The central innovation is the treatment definition. Instead of coding treatment only at a state eligibility boundary, we code exposure at the county level based on adjacency and timing of neighboring expansion. The empirical design compares border-exposed and interior counties within non-expansion states using dynamic event-time indicators around adjacent-state expansion years. This isolates whether policy timing in nearby treated jurisdictions predicts outcome changes in untreated places after controlling for county fixed differences and state-year shocks.

The paper is designed to meet top-journal standards in three dimensions. On identification, we provide dynamic pre-trend tests, placebo re-timing exercises, border-specific trend controls, and leave-one-border-state-out influence checks. On execution quality, we pre-specify outcome definitions, clustering choices, and robustness hierarchy before reporting treatment effects. On policy interpretation, we separate reduced-form externality estimates from welfare claims and avoid extrapolation beyond observed support.

The paper contributes to the Medicaid literature by broadening the object of inference. Prior studies establish direct coverage, utilization, and mortality effects in expansion contexts; our contribution is to quantify whether untreated neighboring counties move in tandem with policy adoption across borders. We also contribute to spatial policy evaluation by offering a practical county-year architecture that can be replicated for other state-level policy discontinuities with cross-border interaction channels.

Importantly, this draft does not present fabricated numeric effect sizes. The writing is complete and publication-structured, but effect tables are pending final data integration, QC logs, and reproducibility checks. This discipline is intentional: the paper aims to be credible as a scientific object, not merely polished prose. All claims in this version concern design, assumptions, and planned inferential logic.

## 2. Institutional Background and Spillover Channels

Medicaid expansion under the Affordable Care Act produced staggered adoption across states over the 2014-2023 period. Eligibility shifts changed insurance access for low-income adults in expansion states, while neighboring non-expansion states maintained narrower criteria. At the county level, this generated sharp policy gradients at many state borders, often within integrated labor and care markets. Border counties are therefore a natural laboratory for measuring regional externalities.

Several mechanisms could generate spillovers. The first is provider and hospital system reallocation. Expansion can improve payer mix and reduce uncompensated care in treated areas, potentially changing provider entry, staffing, referral acceptance, and service availability near borders. The second is patient flow dynamics: residents in non-expansion counties may seek care in expansion states when referral pathways, transportation, or employment ties make cross-border use feasible. The third is labor-market and information spillovers. Cross-border work networks can increase awareness of enrollment, care pathways, or subsidized options among neighboring populations even without full in-state eligibility changes.

Not all spillovers are beneficial. Expansion-state demand shocks could crowd capacity in border systems and increase waiting times for untreated neighboring populations, especially for specialty care. Alternatively, improved financial stability of nearby hospitals could preserve service lines and indirectly improve emergency or referral access for border counties. Because theory is ambiguous ex ante, an empirical design with transparent dynamic diagnostics is essential.

## 3. Related Literature and Positioning

This paper stands at the intersection of three literatures: (i) public insurance and health outcomes, (ii) Medicaid expansion policy evaluation, and (iii) place-based spillovers in regional policy contexts. We deliberately benchmark design principles against top-journal studies.

The Oregon Health Insurance Experiment (Finkelstein et al., 2012, QJE) remains foundational for causal insurance inference via lottery assignment. Its core lesson for this paper is not merely internal validity; it is transparent separation between design assumptions, outcome definitions, and interpretation limits. We adopt that discipline by pre-specifying outcomes, identifying variation, and robustness hierarchy before reporting effects.

Goodman-Bacon (2017, JPE) provides high-impact evidence on public insurance and mortality using quasi-experimental variation in Medicaid implementation. The mortality focus and explicit attention to causal structure directly motivate our endpoint selection and identifying logic. Finkelstein, Hendren, and Luttmer (2018, JPE) then extend interpretation toward welfare and valuation; we use that work as a warning against overreach, separating reduced-form spillovers from welfare claims unless mechanism evidence is sufficiently complete.

Frean, Gruber, and Sommers (2017, JHE) decompose coverage effects under ACA design details, illustrating how policy bundles can produce layered treatment channels. That decomposition logic informs our mechanism section: cross-border spillovers likely combine coverage pathways, provider-market adjustments, and information diffusion, requiring careful interpretation of reduced-form estimates.

Dobkin et al. (2018, AER) exemplify execution rigor in health economics, especially around outcome construction, event dynamics, and economically meaningful interpretation tied to data constraints. We imitate this execution style by requiring consistent outcome definitions across specifications and by maintaining a single inferential backbone rather than shopping across estimator families.

Lee, Dodge, and Terrault (2021, Lancet Public Health) document heterogeneity in mortality associations around expansion, reinforcing that aggregate estimates can mask large distributional variation. We extend this insight spatially: heterogeneity by border market integration, baseline uninsurance, and health system capacity is likely central for understanding cross-border incidence.

The place-based and neighborhood literature, including work such as Chetty, Hendren, and Katz (2016, AER), demonstrates that policy exposure in one place can alter outcomes through geography-linked mechanisms that exceed formal program boundaries. Our design borrows this spatial perspective but applies it to an insurance policy context with explicit event timing and non-treated comparison counties.

The net contribution is thus not duplicative estimation of known direct effects. It is a focused, policy-relevant estimate of untreated-border externalities under a pre-specified causal framework with explicit diagnostics for parallel trends, composition, and border-specific confounding.

## 4. Conceptual Framework

Let county outcomes depend on local insurance access, provider capacity, and care-seeking frictions. Expansion in neighboring states can shift each component for a non-expansion border county through cross-border channels. Define reduced-form potential outcomes for county c at time t as Y_ct(E_ct), where E_ct denotes exposure to neighboring expansion timing and intensity. Our estimand is the dynamic average treatment effect on exposed non-expansion border counties relative to interior non-expansion counties under conditional parallel trends.

The framework predicts heterogeneity. Spillovers should be larger where cross-border commuting, referral integration, and hospital market concentration indicate stronger inter-county dependence. Spillovers should also vary by outcome: amenable mortality, which is more sensitive to timely access and continuity of care, may respond differently from causes less linked to ambulatory management.

The framework further implies asymmetric directionality. Positive spillovers may arise via provider financial stabilization and care access gains; negative spillovers may arise via congestion or selective migration. Our empirical design does not assume sign ex ante and centers identification quality over directional priors.

## 5. Data Architecture

### 5.1 Unit, horizon, and geography

The unit is county-year. The preferred horizon is 2009-2023 to capture pre-ACA baseline years, initial expansion years, and medium-run post-expansion dynamics. The sample includes counties in non-expansion states, with exposure assigned via adjacency to expansion-state counties and neighboring-state implementation timing.

### 5.2 Outcomes

Primary outcomes are:

1. Amenable mortality rate (age 25-64).
2. All-cause mortality rate (age 25-64).

Secondary outcomes include insurance-sensitive hospitalization or preventable utilization proxies where coding and denominator quality are stable at county-year frequency. Outcome definitions are held fixed across all main and robustness specifications.

### 5.3 Exposure variables

Core exposure components are:

- `is_border_county`: county borders at least one county in a state that adopts expansion.
- `adjacent_expansion_year`: first year a neighboring expansion state activates policy.
- `event_time`: year minus `adjacent_expansion_year`.

Extended exposure intensity uses commuting shares, border length, and hospital market integration proxies to test mechanism-consistent heterogeneity.

### 5.4 Controls

Controls include demographic composition, economic conditions, and health system capacity measures. These are used as precision controls and robustness diagnostics; identification primarily relies on fixed effects and event-time variation.

### 5.5 Data provenance and reproducibility

All source provenance is documented in `papers/epi_a_0019/v3/data/DATA_MANIFEST.md`. The analysis script requires explicit input files and exits on missing schema, preventing silent execution on placeholder inputs.

## 6. Empirical Strategy

### 6.1 Baseline event-study DiD

Our baseline model is:

Y_ct = sum_{k != -1} beta_k * 1[event_time_ct = k] * Border_c + alpha_c + gamma_st + X_ct' theta + epsilon_ct

where:

- `alpha_c` are county fixed effects,
- `gamma_st` are state-by-year fixed effects,
- `Border_c` marks non-expansion border exposure,
- `k = -1` is omitted reference year,
- inference clusters at state level.

This model identifies dynamic treatment effects under conditional parallel trends between border and interior counties within non-expansion states.

### 6.2 Static summary effect

We complement dynamic estimates with a TWFE interaction model using `post_exposure` to summarize average post-period effects. The static model is not a substitute for event-study diagnostics and is interpreted only after pre-trend validation.

### 6.3 Identification threats and planned responses

Threat 1: Differential pre-trends in border counties.

- Response: joint significance tests on lead coefficients, border-specific linear trend robustness, and visual pre-period diagnostics.

Threat 2: Migration and composition shifts.

- Response: population-denominator checks, demographic reweighting, and sensitivity to excluding high-mobility metros.

Threat 3: Simultaneous border shocks unrelated to Medicaid.

- Response: state-year fixed effects, placebos with pseudo expansion timing, and leave-one-border-state-out analyses.

Threat 4: Staggered treatment heterogeneity biases.

- Response: report estimator-consistent event-study specifications, compare alternative aggregation methods, and avoid overinterpreting weighted averages when exposure timing is uneven.

## 7. Robustness and Falsification Plan

We pre-register the following robustness hierarchy.

### Tier A (mandatory)

1. Event-window variants ([-5, +5], [-6, +6], [-8, +8]).
2. Alternative clustering (state, border-state-pair, wild bootstrap).
3. Placebo timing shifts (+/-2 and +/-3 years).
4. Alternative comparison sets (interior only, matched interior).

### Tier B (mechanism-sensitive)

5. Exposure intensity by commuting integration quintiles.
6. Stratification by baseline uninsurance and provider supply.
7. Excluding counties adjacent to multiple expansion states.
8. Excluding counties with major boundary or coding anomalies.

### Tier C (scope and external validity)

9. Urban-rural split estimates.
10. Regional subsamples (South, Midwest, etc.).
11. Outcome redefinitions for cause grouping sensitivity.
12. Population weighting alternatives.

Any robustness result that changes sign, magnitude class, or significance profile materially is explicitly documented in the specification log and discussed in interpretation text.

## 8. Reporting Standards (Top-Journal Alignment)

To align with high-impact standards in economics and policy journals, the paper follows these reporting rules:

- Every main estimate is linked to a pre-specified equation and sample definition.
- No specification enters the main table unless its pre-trend diagnostics are reported.
- Standard errors and clustering choices are justified by policy variation scale.
- Main-text claims are restricted to estimates shown in tables/figures.
- Appendix carries estimator details, additional diagnostics, and data construction logs.

We avoid two common failures in automated paper generation: hidden specification search and overstated causal language. The manuscript uses conservative wording for reduced-form findings and clearly separates demonstrated effects from mechanism hypotheses.

## 9. Mechanism Analysis Blueprint

Mechanism analysis is exploratory but disciplined. We evaluate three pathways:

1. **Provider channel**: changes in local health system capacity, emergency department pressure, and referral acceptance patterns.
2. **Cross-border utilization channel**: movement in border-area care use proxies where available.
3. **Information channel**: stronger effects in labor markets with high cross-state commuting intensity.

Mechanism evidence is interpreted triangulationally. No single proxy is treated as definitive proof. We require directional consistency across at least two independent indicators before advancing strong mechanism claims.

## 10. Policy Interpretation

If spillovers are positive, expansion may generate regional health benefits even in nominally untreated jurisdictions, implying that state-level non-adoption does not cleanly map to health non-exposure. This has implications for federal matching policy, interstate fiscal equity, and accountability metrics in decentralized systems.

If spillovers are negative, policymakers need to account for capacity displacement and congestion externalities, especially in border hospital markets with thin specialist supply. In either case, county-level policy evaluation should treat border structure as first-order design information rather than background context.

Importantly, reduced-form spillover effects do not by themselves deliver welfare incidence. Welfare conclusions require integrating fiscal effects, distributional incidence, and behavioral margins beyond mortality outcomes.

## 11. Limitations

This design has limits. First, county-level outcomes may mask individual eligibility heterogeneity and selective movement. Second, border exposure proxies can be measured with error when patient flow data are incomplete. Third, mortality endpoints, while policy salient, respond with different lags and may understate short-run morbidity effects.

We therefore treat results as policy-relevant evidence on regional incidence rather than complete welfare accounting. Claims about broad national welfare gains or losses are out of scope for this paper unless additional model-based evidence is introduced.

## 12. Ethics, Transparency, and Replication

The paper uses de-identified or aggregate administrative/public data. No individual-level protected health information is required in the baseline county-year design. All transformations from raw source downloads to analytic files must be script-generated and version-controlled.

Replication artifacts include:

- code scripts with deterministic seeds,
- machine-readable specification logs,
- data manifest with source URLs and access notes,
- explicit list of exclusions and boundary harmonization decisions.

Any post hoc specification changes must be labeled as exploratory and reported separately from pre-specified analyses.

## 13. Draft Status and Next Actions

This is a full-structure, top-journal-style draft focused on scientific substance and identification transparency. Numerical treatment-effect claims are pending final data assembly and reproducibility audit. The next update will add populated result tables, event-study figures, pre-trend tests, and complete appendix diagnostics.

## References (Core Benchmark Set)

1. Finkelstein, A., Taubman, S., Wright, B., Bernstein, M., Gruber, J., Newhouse, J. P., Allen, H., & Baicker, K. (2012). The Oregon Health Insurance Experiment: Evidence from the First Year. *Quarterly Journal of Economics*. DOI: `10.1093/qje/qjs020`.
2. Goodman-Bacon, A. (2017). Public Insurance and Mortality: Evidence from Medicaid Implementation. *Journal of Political Economy*. DOI: `10.1086/695528`.
3. Finkelstein, A., Hendren, N., & Luttmer, E. F. P. (2018). The Value of Medicaid: Interpreting Results from the Oregon Health Insurance Experiment. *Journal of Political Economy*. DOI: `10.1086/702238`.
4. Dobkin, C., Finkelstein, A., Kluender, R., & Notowidigdo, M. (2018). The Economic Consequences of Hospital Admissions. *American Economic Review*. DOI: `10.1257/aer.20161038`.
5. Frean, M., Gruber, J., & Sommers, B. D. (2017). Premium Subsidies, the Mandate, and Medicaid Expansion: Coverage Effects of the Affordable Care Act. *Journal of Health Economics*. DOI: `10.1016/j.jhealeco.2017.02.004`.
6. Lee, B. P., Dodge, J. L., & Terrault, N. A. (2021). Medicaid Expansion and Variability in Mortality in the USA: A National, Observational Cohort Study. *The Lancet Public Health*. DOI: `10.1016/S2468-2667(21)00252-8`.
7. Chetty, R., Hendren, N., & Katz, L. F. (2016). The Effects of Exposure to Better Neighborhoods on Children: New Evidence from the Moving to Opportunity Experiment. *American Economic Review*. DOI: `10.1257/aer.20150572`.
8. Ruhm, C. J. (2000). Are Recessions Good for Your Health? *Quarterly Journal of Economics*. DOI: `10.1162/003355300554872`.

## Appendix A. Pre-Specified Table and Figure Plan

### Table 1. Sample Construction

- County counts by border status and region.
- Summary statistics pre-policy period.

### Table 2. Main Event-Study Coefficients

- Leads/lags for amenable mortality.
- Joint pre-trend test p-values.

### Table 3. Static Post Effects

- TWFE interaction estimates for primary outcomes.

### Table 4. Robustness Summary

- Alternative clustering, window choices, and placebo timing.

### Figure 1. Event-Study Dynamics

- Coefficient path and confidence intervals.

### Figure 2. Heterogeneity by Integration Intensity

- Stratified post effects by commuting-share quintile.

## Appendix B. Data Cleaning Protocol (Condensed)

1. Harmonize county FIPS across annual files.
2. Audit boundary/code changes and define consistent panel IDs.
3. Construct mortality rates with stable denominator rules.
4. Merge policy timing and adjacency matrices.
5. Validate no future information leaks into event-time construction.
6. Export final panel with immutable schema and checksum.

## Appendix C. Interpretation Guardrails

- No individual-level treatment claims.
- No welfare aggregation without fiscal incidence accounting.
- No national extrapolation from border-only identifying variation.
- No mechanism certainty without multi-proxy concordance.

## Appendix D. Detailed Variable Dictionary

This appendix records the operational definitions used in estimation so that analytic choices are auditable and reproducible. The objective is to reduce researcher degrees of freedom by fixing measurement conventions before model comparison.

### D.1 Outcomes

`amenable_mortality_25_64`

- Definition: deaths per 100,000 among ages 25-64 for causes considered amenable to timely and effective health care management under the selected coding protocol.
- Construction notes: cause group mapping is fixed ex ante in a versioned codebook; age standardization uses county-year denominators aligned to ACS/Census conventions.
- Exclusions: counties with unresolved denominator anomalies after harmonization are flagged and dropped under pre-registered rules.

`allcause_mortality_25_64`

- Definition: all-cause deaths per 100,000 among ages 25-64.
- Purpose: broad endpoint less sensitive to cause coding artifacts than subcause outcomes, useful as a stability check.

### D.2 Exposure and treatment-timing variables

`is_border_county`

- Binary indicator equal to one when county boundary intersects at least one county in an expansion-state jurisdiction.
- Constructed from TIGER/Line adjacency graph; matrix stored with checksum for exact reproducibility.

`adjacent_expansion_year`

- Earliest implementation year among adjacent expansion states. If multiple neighboring states expand in different years, earliest year sets baseline event anchor and additional timing structure is captured in sensitivity analyses.

`event_time`

- `year - adjacent_expansion_year`; bounded to a symmetric analysis window in baseline specifications.

`treated_border`

- Binary indicator equal to one if county is in a non-expansion state and has non-missing adjacency expansion timing.

### D.3 Covariates

`population_25_64`

- Denominator for weighting and rate construction.

`baseline_uninsurance_share`

- Pre-period county uninsurance rate proxy used for heterogeneity bins.

`provider_supply_index`

- Composite of primary-care and specialist density indicators from AHRF used for mechanism-heterogeneity tests.

`crossborder_commuting_share`

- Share of employed residents commuting across state lines, used as integration-intensity proxy.

### D.4 Fixed effects and clustering

`county_fips`

- Unit fixed effect identifier controlling for time-invariant county confounding.

`state_year`

- Interaction fixed effect controlling for any state-level annual shocks, including macroeconomic and policy bundles common to all counties in a state-year.

Cluster dimension:

- Baseline clusters at `state_fips` because policy timing variation is state-level and serial correlation is expected within state over time.

## Appendix E. Identification Threat Matrix

The table-equivalent narrative below maps each major threat to mitigation strategy and interpretation consequence.

### E.1 Border-selective trends predating policy

Threat: border counties might have different baseline trajectories unrelated to expansion spillovers.

Mitigation:

1. Joint lead tests in event-study pre-period.
2. Border-specific linear trend sensitivity.
3. Matched interior controls by pre-period trajectories.

Interpretation consequence:

- If pre-trends fail, main causal interpretation is weakened and results are reclassified as associational dynamics.

### E.2 Policy co-movement at border (other reforms)

Threat: neighboring states may adopt correlated reforms coincident with expansion timing.

Mitigation:

1. State-year fixed effects absorb own-state annual confounders.
2. Placebo timing tests detect mechanical event-time artifacts.
3. Supplementary controls for major policy bundles where codable.

Interpretation consequence:

- Residual confounding cannot be fully ruled out; findings are interpreted as reduced-form policy bundle spillovers when needed.

### E.3 Selective migration and denominator distortions

Threat: migration responses may change population composition in ways that bias county rates.

Mitigation:

1. Population denominator audits.
2. Alternative weighting strategies.
3. Sensitivity excluding high-inflow metro counties.

Interpretation consequence:

- If estimates are highly migration-sensitive, mechanism claims are limited and framed as composition-adjusted only.

### E.4 Measurement error in expansion timing and adjacency

Threat: coding errors in treatment timing or adjacency graph can induce attenuation or spurious dynamics.

Mitigation:

1. Dual-source timing verification for policy dates.
2. Adjacency matrix versioning with checksums.
3. Manual audits for county boundary changes.

Interpretation consequence:

- Remaining error likely attenuates effects; null results are interpreted cautiously.

## Appendix F. Estimation and Inference Details

### F.1 Why event study is primary

A static post-treatment coefficient can mask dynamic adaptation, delayed provider responses, and differential transitory shocks. Event-study structure reveals pre-period behavior and post-period persistence, which are central for adjudicating causal plausibility. For policy questions with staggered adoption and potentially lagged health effects, dynamic diagnostics are not optional; they are the core credibility test.

### F.2 Why county FE plus state-year FE

County fixed effects remove permanent county-level confounding. State-year fixed effects absorb any annual shock common to all counties in a state, including own-state policy environment and macro conditions. This combination specifically sharpens identification to within-state differences between border-exposed and interior counties as neighboring expansion timing varies.

### F.3 Inference and finite-sample caution

Given policy variation is state-level, naive county clustering would overstate precision. Baseline clustering at state is therefore mandatory. We also plan wild cluster bootstrap checks where treated policy clusters are limited. In tables, p-values from alternative inference procedures will be reported side by side when materially different.

### F.4 Handling staggered timing heterogeneity

Because treatment timing is staggered across neighboring states, aggregation can hide compositional weighting issues. The estimation plan therefore reports dynamic coefficients directly and avoids over-reliance on single averaged post effects. Where alternative estimators are used, interpretation is tied to their identifying assumptions and weighting properties.

## Appendix G. Mechanism Evidence Plan

Mechanism analysis is pre-specified to avoid narrative cherry-picking after effect estimation.

### G.1 Provider-market mechanism tests

Hypothesis: expansion in neighboring states improves or reallocates provider capacity in ways that affect border-county mortality-sensitive access.

Empirical probes:

1. Changes in provider density trends for border versus interior counties.
2. Changes in emergency department congestion proxies.
3. Differential effects by baseline hospital market concentration.

### G.2 Cross-border utilization mechanism tests

Hypothesis: residents of non-expansion border counties increasingly use expansion-side care pathways.

Empirical probes:

1. Border integration interactions using commuting-share and referral proxies.
2. Stronger effects in counties with historically high cross-state labor-market linkage.
3. Placebo outcomes less sensitive to outpatient continuity should show weaker responses.

### G.3 Information and enrollment behavior diffusion

Hypothesis: exposure to neighboring expansion states changes information sets and care-seeking behavior in untreated counties.

Empirical probes:

1. Heterogeneity by education and language-access proxies.
2. Timing consistency with diffusion lags rather than immediate mechanical jumps.

Mechanism claims will be made only where multiple probes point in the same direction and remain robust under core sensitivity checks.

## Appendix H. Top-Journal Submission Readiness Checklist

This checklist defines what must be complete before this manuscript can credibly be treated as a submit-ready working paper.

### H.1 Design credibility

- [ ] Event-study pre-trend coefficients and joint tests pass credibility thresholds.
- [ ] Parallel-trend sensitivity to border-specific trends documented.
- [ ] Placebo timing exercises reported in main or appendix tables.

### H.2 Data transparency

- [ ] Full data provenance table completed with access dates.
- [ ] County inclusion/exclusion flow diagram generated.
- [ ] Boundary harmonization protocol and logs published.

### H.3 Execution quality

- [ ] Clustered inference and bootstrap checks aligned.
- [ ] Alternative windows and clustering produce interpretable stability profile.
- [ ] Robustness table includes sign/magnitude consistency narrative.

### H.4 Scope discipline

- [ ] Main text avoids individual treatment-effect overclaims.
- [ ] Mechanism statements clearly labeled as supported vs conjectural.
- [ ] External-validity boundaries explicitly stated.

### H.5 Replication package

- [ ] End-to-end run scripts execute from clean environment.
- [ ] Output hashes and specification log archived.
- [ ] Reproducibility README with exact command sequence provided.

## Appendix I. Planned Results Narrative Template (To Be Filled Post-Estimation)

This section is intentionally prepared as a template to prevent post hoc storytelling.

1. **Main dynamic pattern**: describe sign, timing, and persistence of post coefficients relative to pre-period baseline.
2. **Credibility diagnostics**: report pre-trend evidence and any violations.
3. **Robustness profile**: summarize which checks materially alter conclusions.
4. **Mechanism consistency**: evaluate whether mechanism probes align with reduced-form effects.
5. **Policy interpretation**: state what policymakers can infer and what remains uncertain.

Using a fixed template ensures the eventual narrative follows evidence rather than rhetorical convenience.
