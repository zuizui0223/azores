# V5 paper spine to frozen evidence and supplement map

**Scope:** companion to AZORES_PHASE_TRANSFER_MAIN_V5_DRAFT.md. The V5 text is a shorter **author-review manuscript**, not a new biological analysis or a claim that supplementary tables have already been typeset. No source model, cohort, estimator, confidence interval or significance rule has changed.

## Main biological arguments and canonical evidence

| Main claim | Source/phase | Mandatory numbers and risk set | Manuscript position |
|---|---|---|---|
| More advanced silvering ranks classified initiation | Six-project cleaned source, expert-corrected | FIII 154/261; FIV 53/68; FV 215/246; 575 stage-coded tracks, Durif OR/stage 2.08 (1.56–2.76) | V5 Results 1, Figure 2 |
| Continuous condition contributes to observed activation after stage | Multivariate activation model | Stage OR 2.13 (1.60–2.84); condition OR 1.46 (1.16–1.83); n=525 score fit | V5 Methods/Results 1, Figure 2 |
| Entry-trained score transfers to onset but not two speeds | Frozen relative stage/condition weights from activation | Activation OR 2.23 (1.70–2.92); onset HR 1.32 (1.17–1.49, n=570, 418 events); whole speed 0.946 (0.832–1.076, n=418); station speed 1.028 (0.869–1.215, n=411) | V5 Results 2, Figure 3 |
| Source-project held-out robustness | Six withheld training folds; predictor preprocessing partly shared | Activation OR 1.97, onset HR 1.26, whole speed ratio 0.948, station speed 1.013 | V5 Results 2; supplement |
| Same-route physical progression falsification | Directed receiver links fixed; fish-equal weighting | 17,792 source-positive rows, 418 eels, 244 directed links; ratio 0.962 (0.883–1.048), post-hoc gross-speed screens all 95% intervals contain 1 | V5 Results 2, supplement |
| Silvering/initiation association differs among projects | FV vs FIII exact conditional test with project × release-year fixed margins | n=507; 14 source project-year margins, 11 informative; LR 19.087; exact p=0.003142; no Albertkanaal p=0.05310 | V5 Results 3, supplement |
| Added condition discrimination not universally portable | Stratified held-out positive-negative pairs | AUC 0.610 vs 0.643; 4/6 positive projects, cluster interval [-0.0007,0.0918]; score-blind negative follow-up sensitivity | V5 Results 3, supplement |
| Proposed barrier opening/waiting pathway not supported | Independent Dutch DANS archive, arrival-defined | CL choice n=15, beta=-0.095, permutation p=0.849; EZ near-separated not interpreted | V5 Results 4, Figure 4 |

Primary scientific statement: **Capture phenotype predicts entry and onset, not a general ranking of realized movement speed.** It does not say that internal physiology ceases to matter after migration, that noninitiation is biological failure or that any of these estimates prove escapement.

## Source V4 items to allocate to supplement, not delete or silently hide

**S1 — Source cohort and observational risk sets.** Map the 603 metadata candidate records to 575 cleaned stage-coded tracks; document 28 unmatched entries and the source expert correction of nine algorithm-positive eels. Distinguish 525 multivariate activation observations, 570 onset records/418 events and 418/411 progression observations. Canonical provenance is the unchanged source-manuscript Methods and sample-flow files.

**S2 — Multivariate measurement dependence.** Show Durif × condition/length interaction tests, three weight-for-length sensitivity definitions, five-project measured eye/fin subset (429 fish, condition-after-morphology AUC +0.0244, project CI spanning zero), and stage-specific Durif class analyses. Weight-for-length is not direct lipid, endocrine or energy measurement and is partly mechanically related to Durif's morphology.

**S3 — Incomplete observation and false source noninitiation.** The key issue is telemetry **observability**, not proof of actual unrecorded behavioral departure. Retain the 90-day source-positive/censored-negative risk-set discrepancies, stage-specific and river-specific logical nonidentification bounds, worst-case 11 hypothetical false negatives sufficient to remove +0.0336 AUC, and non-adversarial random-label sensitivity. None reports eleven observed misclassified fish. Include the project-level and individual sampling-uncertainty caveat on the positive pooled FV-FIII logical bound.

**S4 — Entry-state discriminative portability.** Preserve stratified AUC estimation within held-out project-year, fish/bootstrap vs six-project bootstrap interpretation, same-stage positive-negative pairs, project heterogeneity (4/6 positive), five-project morphology-controlled comparison and sample-composition shifts under the horizon-specific onset/cohort analyses. A pooled score AUC does not imply a universally portable river-level classifier.

**S5 — Speed and transit reliability.** Retain whole-route and per-eel median station-speed samples, within-link FWL numerical equivalence, eel-balanced weights, source ground-speed values reaching 3,752 m s−1 and post-hoc exclusion of >2.5, >5 and >10 m s−1. These quality checks are not evidence for a negative physiological speed effect. Keep activation-selection, inverse-propensity and elapsed-time/predictor-aging diagnostics separately rather than treating a non-significant p-value as evidence of zero effect.

**S6 — River-level environmental opportunity.** Retain conditional FV/FIII odds ratio heterogeneity and its Albertkanaal sensitivity. The source environmental forcing is not time-aligned to individual migration events, so no discharge-by-stage causal modifier is estimated. Project-context WRS/terminal-positive-set correlations (n=6) are observational and **not biological survival or escapement effects**.

**S7 — Independent Dutch arrival-to-barrier window tests.** Document observed arrival, opening start and observed passage eligibility, rather than source event-duration-dependent valid flags; include opening-duration choice, missing opening events and hours to passage by barrier. The EZ fitted choice is near-separated and should never be plotted as a precise signed biological effect. This archive is not direct validation of the European activation model.

**S8 — Documentation and reproducibility.** Retain all frozen numerical contracts, result JSON provenance, source file links, original protocol limitations, figure-data V4 contract, and validated SVGs. V5 has no new estimated number. V4 full-length text is archived as an evidence ledger, not an independently verified journal supplement ready for submission.

## Current populated supplementary draft

The [S1–S8 supplementary Methods and Results manuscript](AZORES_V5_SUPPLEMENT_METHODS_RESULTS_DRAFT.md) now contains 35 verbatim source sections extracted from the V4 Methods, Results and source-limitations passages. This is a **populated evidence draft**, not yet a journal-style Supplement with independently typeset tables or bibliography. Its [exact source-integrity verifier](../validation/verify_v5_supplement_source_integrity.py) compares each full section with the unchanged original V4 to prevent truncated or reinterpreted evidence.

## Current canonical file references

- Full source evidence manuscript: [AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md](AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md).
- Numeric source of truth: [MANUSCRIPT_NUMERIC_CONTRACT_V4.json](MANUSCRIPT_NUMERIC_CONTRACT_V4.json).
- Figure data source: [FIGURE_DATA_CONTRACT_V4.json](FIGURE_DATA_CONTRACT_V4.json).
- Four verified V4 figures: [Figure 1](rendered_figures_v4/Figure1.svg), [Figure 2](rendered_figures_v4/Figure2.svg), [Figure 3](rendered_figures_v4/Figure3.svg), [Figure 4](rendered_figures_v4/Figure4.svg).
- Recorded V4 author/figure/source QC: [MANUSCRIPT_QC_V4.json](MANUSCRIPT_QC_V4.json).

## Submission stop list (independent of scientific QC)

1. Verify actual authors, institutional affiliations, contributions and acknowledgements from contributors.
2. Select a target journal and split S1–S8 into its required supplementary format/length. This map is an allocation proposal, not the completed supplement.
3. Replace the abbreviated Verhelst author listing with journal-compliant verified source bibliography.
4. Confirm source-project animal-handling ethics approvals from original telemetry publications.
5. Ensure final V5 text, references and four SVGs are proofread by a human and match a submission archive/release.
6. Do not announce submission or peer-review status before a genuine journal acknowledgement.
