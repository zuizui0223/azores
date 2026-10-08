# Observation gate in eel migration initiation — 2026-10-08

**Evidence class:** post-hoc observation-process falsification. The negative-control run is not yet promoted as a result until its CI calculation and checks complete.

## Why this matters

The V4 paper asks whether a capture-time phenotype distinguishes *entering migration* from *moving faster after entry*. That question depends on a reliable distinction between source-classified initiators and source noninitiators. But the source is telemetry, not continuous physical observation.

The six-project activation panel contains **575** stage-eligible European eels: **422** source-classified initiation cases, **153** source noninitiation records. The fixed **90-day eligibility** selection used in the temporal audit retains **475** fish. Crucially, **all 422 initiators remain**, while just **53 of 153 source noninitiators remain**. A total of **100 records**, all belonging to the source noninitiation class, are omitted for insufficient follow-up.

The original held-out activation-discrimination AUC increment from condition was **+0.03356** in all 575. The separate 90-day-eligible cohort gives **+0.08068** for *the same eventual source initiation label* and the *same fitted held-out score model*. The raw contrast is **+0.04713**, but its reason has not yet been distinguished.

**This does not imply physiological time gating.** Both outcome groups and their project-year weights change when the 100 negative-class records are removed; AUC can change even though it is insensitive to *overall* class prevalence under unselected case/control sampling.

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

The selection-null holds **every source-classified initiator** and each project-year's exact **negative retention quota** constant, randomizing only *which source noninitiation records* remain. The 20,000 random-retention replicates preserve the outcome model and do not re-estimate weights or physiologic state.

## Interpretation boundaries

1. A fish lacking day-90 records is **not** known to be dead, stationary or nonmigratory.
2. The last receiver arrival is not proof that monitoring was uninterrupted until that point.
3. The permutation compares a specific null of conditional random negative retention; it cannot prove observation caused the condition-AUC gain or correct informative censoring.
4. Observability prediction is a negative-control *association*, not an independent ecological mechanism.
5. Receiver coverage and discharge/sluice time series, ideally alongside direct passage and survival records, are required to identify environmental control of actual migration.

## Implication for conservation monitoring

Silvering stage, conditional body-state readiness, telemetry-defined initiation, and genuine escapement success are distinct quantities. Selection of fish by duration of detectable telemetry can distort the apparent performance of readiness biomarkers. A biologically interpretable monitoring index requires explicit observation opportunity or independent passage outcomes, not an AUC score alone.
