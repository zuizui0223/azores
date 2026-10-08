# Observation gate in eel migration initiation — 2026-10-08

**Evidence class:** verified post-hoc observation-process falsification. Source-matched permutation and synthetic validations **PASS** in GitHub Actions run [37755617841](https://github.com/zuizui0223/azores/actions/runs/37755617841). Numerical results are in `results/observability_selection_gate_v1.json` and `results/observability_project_composition_v1.json`.

## Why this matters

The V4 paper asks whether a capture-time phenotype distinguishes *entering migration* from *moving faster after entry*. That question depends on a reliable distinction between source-classified initiators and source noninitiators. But the source is telemetry, not continuous physical observation.

The six-project activation panel contains **575** stage-eligible European eels: **422** source-classified initiation cases, **153** source noninitiation records. The fixed **90-day eligibility** selection used in the temporal audit retains **475** fish. Crucially, **all 422 initiators remain**, while just **53 of 153 source noninitiators remain**. A total of **100 records**, all belonging to the source noninitiation class, are omitted for insufficient follow-up.

The original held-out activation-discrimination AUC increment from condition was **+0.03356** in all 575. The separate 90-day-eligible cohort gives **+0.08068** for *the same eventual source initiation label* and the *same fitted held-out score model*. The raw contrast is **+0.04713**, but its reason has not yet been distinguished.

**This does not imply physiological time gating.** Both outcome groups and their project-year weights change when the 100 negative-class records are removed; AUC can change even though it is insensitive to *overall* class prevalence under unselected case/control sampling.

## Verified result: apparent later-horizon gain is sampling composition, not evidence of a stronger gate

The original 575-eel eventual-classification AUC gain from condition is **+0.03356** over the base model. The 90-day-eligible cohort (475 eels) gives **+0.08068** with the **same** outcome definition and **same** project-held-out score weights, an increase of **+0.04713**.

The exact project-pair-weight identity attributes:
- **+0.05153** to changing how informative project pairs are weighted after follow-up selection;
- **−0.00440** to within-project changes (also including within-project-year mix);
- sum **+0.04713**, with numerical identity residual essentially zero.

The Warnow project contributes 52.6% of full comparison pairs but only 5.2% of selected pairs, while Leopoldkanaal grows from 21.1% to 53.4%. The apparent stronger benefit in the selected cohort can therefore occur without any new physiological response to elapsed time.

A second check holds all 422 initiators and the exact number of retained noninitiators per project-year, randomly choosing **which** noninitiators survive the screen in **20,000** permutations. The expected condition AUC gain is **+0.08444** (95% permutation interval **+0.06064 to +0.10831**), compared with observed **+0.08068**. The two-sided deviation from the random-retention mean is **p=0.764**. Thus specific retained-fish phenotype selection is **not needed** to explain the observed gain once project-year quotas are fixed.

The source-label negative-control question is whether condition-trained initiation scores also rank which **noninitiator** has a final receiver detection after day 90. Across 326 within-project-year pairs, adding condition improved AUC by just **+0.0092**; signs differ among projects, and the four informative projects do not establish a general observability gradient.

Among the 153 source noninitiators, the 100 excluded individuals have a median time from release to last receiver arrival of **0.515 days**, while the 53 day90-retained individuals have a median **549 days**. These are *last recorded detections*, not continuous monitored exposure; the contrast warns against equating source noninitiation with confirmed biological failure to move.

This is an unusually useful negative result: **the selected-cohort AUC amplification has an identified accounting explanation, without requiring an adaptive physiological timing mechanism**. This does not prove the original activation association is entirely artifactual or that all pathways of detection bias are absent.

## Exact ambiguity tipping: the in-panel condition gain is vulnerable to a few hypothetical missed initiations

A follow-up **post-hoc sensitivity**, independently validated by exhaustive synthetic combination tests, held the **original two project-held-out model scores fixed** and allowed hypothetical relabelling of only the 100 source noninitiation records lacking 90-day observation support. All 422 source initiators and the 53 longer-observed source noninitiators were fixed.

The exact rank-pair optimization over possible relabellings found:
- unchanged classification: condition adds **+0.03356 AUC**;
- best-case *against* condition at 5 relabelled fish: **+0.01296**;
- at 10 fish: minimum **+0.00191**;
- **first nonpositive gain at 11 fish: −0.00016**;
- at 15 fish: minimum **−0.00784**.

The eleven-fish worst-case allocation assigned eight hypothetical hidden starts to Warnow and one each to Leopoldkanaal, Albertkanaal and Verhelst. Other legal assignments could strengthen rather than weaken the apparent condition signal.

**This does not show that 11 actual fish started migration undetected.** It is a mathematically exact *adversarial sensitivity bound* conditional on frozen fitted scores and one source-definition of inadequate receiver follow-up. Score retraining under alternative labels was not performed; receiver dropout and genuine nonmigration remain unidentifiable. Its scientific contribution is to quantify **how little source-label ambiguity may be sufficient to remove the added ranking advantage** in one allowed worst-case scenario.

Reproduction:
- `analysis/contracts/observability_label_ambiguity_tipping_v1.json`;
- `analysis/46_observability_label_ambiguity_tipping.py`;
- `analysis/tests/test_observability_label_ambiguity_tipping.py`;
- `results/observability_label_ambiguity_tipping_v1.json`;
- [CI run 37763360099](https://github.com/zuizui0223/azores/actions/runs/37763360099) — PASS.

## Competing explanations

- **Random loss from the noninitiation class.** Narrowing the control pool, with differing project-year support, could alter ranking metrics simply by chance and reweighting. Diagnostic: randomly retain the same number of negative records within every project-year; repeat with the fixed scores.
- **Phenotype-related observation.** Noninitiation fish whose last receiver record exceeds day 90 may differ systematically in morphology, condition, tagging location, route or detection opportunity. Diagnostic: among the 153 noninitiation records, test held-out-score ranking of >=90-day observability *without retraining on observation outcome*.
- **True ecological initiation differences.** Some fish may not enter downstream movement despite full opportunity to be observed. This requires independent tracking/censoring information to disentangle from telemetry dropout and cannot be established by the existing label.
- **Protocol and project composition.** Receiver coverage, monitoring endpoints and hydrological conditions differ among waterways, so project-year stratification and between-project support must accompany any result.

## Fixed test

See:
- `analysis/contracts/observability_selection_gate_v1.json` — rule frozen before the selection-null result;
- `analysis/45_observability_selection_gate.py` — frozen-score, within-project-year stratified negative-retention null;
- `analysis/tests/test_observability_selection_gate.py` — synthetic paired-AUC and fail-closed positive-retention tests;
- `.github/workflows/observability-selection-gate.yml` — reproducible CI job.

The completed selection-null holds **every source-classified initiator** and each project-year's exact **negative retention quota** constant, randomizing only *which source noninitiation records* remain. The 20,000 random-retention replicates preserve the outcome model and do not re-estimate weights or physiologic state.

## Interpretation boundaries

1. A fish lacking day-90 records is **not** known to be dead, stationary or nonmigratory.
2. The last receiver arrival is not proof that monitoring was uninterrupted until that point.
3. The permutation compares a specific null of conditional random negative retention; it cannot prove observation caused the condition-AUC gain or correct informative censoring.
4. Observability prediction is a negative-control *association*, not an independent ecological mechanism.
5. Receiver coverage and discharge/sluice time series, ideally alongside direct passage and survival records, are required to identify environmental control of actual migration.

## Implication for conservation monitoring

Silvering stage, conditional body-state readiness, telemetry-defined initiation, and genuine escapement success are distinct quantities. Selection of fish by duration of detectable telemetry can distort the apparent performance of readiness biomarkers. A biologically interpretable monitoring index requires explicit observation opportunity or independent passage outcomes, not an AUC score alone.
