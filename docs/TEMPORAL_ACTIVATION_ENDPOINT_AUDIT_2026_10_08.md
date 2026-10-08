# Entry-state predictive information depends on the observed activation endpoint and time horizon

**2026-10-08 — exploratory post-hoc audits, not proof of an ecological timing mechanism.**

Frozen sources:
- `results/cross_project_condition_increment_v1.json` — eventual observed migration-activation ranking, six held-out projects.
- `results/fixed_followup_condition_increment_v1.json` — source 7/30/60/90-day eligibility and models re-trained separately on each endpoint.
- `results/paired_temporal_endpoint_condition_v1.json` — **same 475 eels and same activation-trained held-out scores**, evaluating cumulative early/late and eventual endpoints.
- `analysis/contracts/fixed_followup_condition_increment_v1.json` and `analysis/contracts/paired_temporal_endpoint_condition_v1.json` — registered rules before inspecting their respective outputs.

## The apparent sign reversal is a prediction-target issue

In the original 575-fish study population, a continuous weight-for-length condition residual improved held-out within-project-year onset-*classification* ranking above Durif stage, length and release timing by **+0.0336 AUC**.

We then fixed common post-release observation horizons. A positive onset event could count before that horizon; an apparent non-event required at least one later receiver arrival documenting potential observation through that duration. Four separate nested logistic models were **re-trained** per horizon. These changed both the case mix and the fitted score:

| Endpoint | Eligible eels | Observed events | Body-condition AUC increment, retrained |
|---|---:|---:|---:|
| By day 7 | 496 | 239 | **−0.0263** |
| By day 30 | 484 | 299 | **−0.0291** |
| By day 60 | 478 | 331 | **−0.0226** |
| By day 90 | 475 | 351 | **+0.0021** |

For the 30-day endpoint all five informative held-out projects gave negative increments; the six-project/bootstrap over informative contexts gave **−0.0613 to −0.0042**, but the exact five-project two-sided sign flip was **p=0.0625**. This is **not** evidence that a higher condition is physiologically harmful for early migration. Different eligibility and training weights make that inference invalid.

## Same-fish, same-model falsification

The decisive diagnostic kept the **475 eels eligible at day 90** and froze **one pair of project-held-out models trained for eventual initiation on all 575 eels**. No early-outcome label entered model training. Only the outcome horizon was relabelled:

| Endpoint on 475 fixed eels | Events | Base AUC | + Condition AUC | Added condition information |
|---|---:|---:|---:|---:|
| By day 7 | 239 | 0.5877 | 0.5954 | **+0.0077** |
| By day 30 | 299 | 0.5171 | 0.5500 | **+0.0329** |
| By day 60 | 331 | 0.5409 | 0.5869 | **+0.0460** |
| By day 90 | 351 | 0.5770 | 0.6319 | **+0.0549** |
| Eventually classified as initiator | 422 | 0.6665 | 0.7472 | **+0.0807** |

Thus the earlier negative *re-trained* AUC increments do not persist when scores are held fixed. They arise from changed targets, case mix and model estimation, not a demonstrated biologically negative influence on short-term decisions.

Four projects had both day-30 and eventual positive–negative comparison groups. The equal-project mean of the **eventual-minus-30-day condition increment** was **+0.0431**, and all four project differences were positive. A project bootstrap gave **+0.0164–+0.0697**; the exact paired sign-flip is **p=0.125** with four independent projects. Treat this as exploratory, not conclusive external replication.

## Three biological/observation states, not a single binary transition

The fixed 475-fish set consists of:

- 299 with onset detected by day 30;
- 123 with onset detected only after day 30;
- 53 with no source-classified initiation over their observed record.

Using the **same fixed predictor scores** and evaluating within project-year positive–negative pairs:

| Contrast | Condition information increment |
|---|---:|
| Early onset versus no detected initiation | **+0.0832** |
| Late onset versus no detected initiation | **+0.0756** |
| Early onset versus late onset | **+0.0089** |

An entry-state score appears to rank **initiation participation** more reliably than the early-versus-late order among detected initiators. The larger cumulative AUC increment is therefore compatible with a changing composition of the apparent noninitiator class; it is **not** yet evidence that well-conditioned fish deliberately wait longer before migrating.

## Follow-up selection explains inflated eventual AUC in the restricted cohort

A second, now completed post-hoc falsification specifically interrogated why the eventual-source-initiation increment rises from **+0.0336** in all 575 to **+0.0807** in the day-90-eligible 475 fish. That selection retains all 422 source initiators but only 53/153 source noninitiators.

The exact project-pair decomposition assigned **+0.0515** of the **+0.0471** change to altered project weights and **−0.0044** to changes inside the projects. A project-year-matched random-control retention simulation (20,000 repeats) produced mean AUC gain **+0.0844**, interval **+0.0606–+0.1083**; observed **+0.0807** is typical (two-sided **p=0.764**). Thus the larger AUC gain in the 90-day subset does **not** independently support stronger biological readiness effects at long follow-up.

The excluded 100 source noninitiation records had a median last receiver arrival **0.515 days** after release, making source-classified noninitiation a particularly incomplete biological category. This finding reinforces the need to distinguish observation opportunity, departure, migration initiation, subsequent passage and verified escapement.

Canonical independent outputs:
- `results/observability_project_composition_v1.json`
- `results/observability_selection_gate_v1.json`
- `docs/OBSERVATION_GATE_2026_10_08.md`

## What remains unresolved

1. **Informative detection/selection.** Last receiver arrival after the horizon is not continuous receiver coverage; early events and non-events have asymmetric eligibility. One hundred source tracks lack day-90 eligibility. The 53 eventual noninitiators are an observed telemetry category, not proven failures, deaths or residents.
2. **Shared measurement.** Durif classification partly uses morphology and mass; the extra weight-for-length score is not an experimentally independent energy reserve.
3. **Only four matched independent projects** permit the primary paired 30-day/eventual gain contrast. The apparent strong bootstrap interval comes from very few projects.
4. **Conditional onset timing completed.** Cox onset hazard can mix the propensity to enter migration and its timing conditional on entry. With **422 source initiators and 10,756 onset-order pairs**, fixed project-held-out score concordance changed from **0.5446** to **0.5461** after adding condition (Δ **+0.0015**, project bootstrap CI **−0.0237–+0.0202**, exact project sign-flip p=**0.9375**). Excluding onset within day 1 left 291 eels and Δ **−0.0086**. This supports the prediction-target distinction but is not an identification of the underlying hazard components. Source: `results/entrant_onset_latency_discrimination_v1.json`, verified GitHub Actions run 37754405283.

## Conservation consequence if replicated

Do not equate the number of silver eels in a sample, the proportion detected entering downstream migration by an arbitrary 30-day tracking horizon, and the number actually reaching the sea. Phenotype-based readiness indicators may be useful for monitoring **potential migrators**, but neither source classifications nor AUC changes estimate effective escapement or the benefit of a barrier intervention.

A prospective study needs repeated physiological measurements, noninformative follow-up, environmental opening/discharge data, and independent passage/survival endpoints to identify the true mechanism.
