# Analysis programme

## Publication target

This repository does **not** aim to publish a re-analysis of the Flores eel paper.

The primary ecological programme is **state-dependent mobility gating**:

> internal migratory readiness may change how strongly landscape resistance constrains realised movement.

See [general-principle programme](../docs/general_principle_program.md) and [independent test protocol](../docs/independent_test_protocol.md).

## Phase 0 — Flores seed diagnosis only

~~~bash
python analysis/01_receiver_state_diagnostic.py
~~~

Flores is the extreme resident anchor. It is not the evidence base for the general claim.

## Phase 1 — lightweight independent preflight

Do **not** download 1.1 GB first.

Run:

~~~bash
python analysis/03_stage_landscape_preflight.py
~~~

This audits the public processed Europe-wide eel products and tests whether exact capture-time Durif stages have enough cross-project/WRS overlap.

Current design target:

~~~text
FIII / FIV / FV × landscape resistance
~~~

FII and MII remain boundary groups.

## Phase 2 — standardized individual table

~~~bash
python analysis/04_build_stage_landscape_table.py
~~~

This creates:

~~~text
analysis/derived/eel_stage_landscape.csv
~~~

from public upstream metadata, WRS data and the published successful-migrant endpoint.

**Boundary:** aggregate outcome counts were already inspected during development. This panel is developmental independent evidence, not outcome-blind confirmation.

## Phase 2b — behavioural initiation result

Run the complete upstream reconstruction:

~~~bash
python analysis/09_durif_migration_initiation.py
~~~

This streams the public migration tables for six compatible projects and reproduces:

- expert-corrected stage-specific migration initiation;
- algorithm-only sensitivity before the upstream expert correction;
- project-year + body-length + release-timing adjusted stage effect;
- leave-one-project-out stability.

For censored onset timing, use:

~~~bash
python analysis/10_migration_onset_cox.py
~~~

`life4fish` is excluded from this onset reconstruction because the upstream repository contains no compatible distance/residency/speed/migration project products for the classifier. Excluding that entire project, stage-specific table coverage is approximately 95–97%.

The source paper used movement to classify migrant behaviour and then analysed phenology/speed; this phase instead asks whether **capture-time Durif readiness predicts later movement-state expression**.

## Phase 3 — model

Primary ecological test:

~~~text
later movement ~ capture Durif stage
               + landscape resistance
               + stage × landscape resistance
               + project/design covariates
~~~

Project-level leave-one-project-out stability is mandatory.

Only reconstruct the 1.1 GB raw detections if onset/progression metrics unavailable in the public processed migration/speed products require it.

## Phase 4 — replication

Use Wolastoq or another independently accessible eel system to test whether state-dependent landscape resistance transfers across water bodies/species.


## Interpretation correction — stage effect is a positive control

Durif FIII is a pre-migrant female stage and FIV/FV are migrating female stages. Therefore the strong FIII -> FIV -> FV association with later movement is expected biology and serves as a **positive control** for the readiness axis.

Implemented developmental checks:

~~~bash
python analysis/05_project_stratified_stage_effect.py
python analysis/06_project_fixed_ordinal_stage.py
python analysis/07_stage_effect_body_timing_robustness.py
~~~

These establish that the readiness variable behaves coherently and survives body-size/release-timing adjustment.

They do **not** constitute the paper's novelty.

## Active confirmation target

The novel target is:

~~~text
realised movement
  ~ internal readiness
  × barrier / hydrological opportunity
~~~

For the Dutch consecutive-barrier system, after obtaining DANS DOI 10.17026/LS/WTSUNG:

~~~bash
python analysis/08_dutch_barrier_confirmation_gate.py   --data-dir <downloaded_DANS_directory>
~~~

If stage and body mass/opportunity cannot be separated, return NON-IDENTIFIABLE rather than rescuing the interaction.

## Phase 2d — project-context gate audit

Run:

~~~bash
python analysis/11_project_context_gate.py
~~~

This compares median project WRS impact with two sequential outcomes:

1. migration initiation rate;
2. successful completion conditional on initiation.

The script uses all **6! = 720** project permutations for exact Spearman p-values and reports leave-one-project-out completion gradients.

**Boundary:** this is project-level bridge evidence, not causal WRS inference. The Dutch within-route system remains the progression-stage confirmation.


## Canonical two-stage pipeline

Use only these files for the current paper mainline:

~~~text
Gate 1 binary initiation:
  analysis/09_durif_migration_initiation.py

Gate 1 timing:
  analysis/10_migration_onset_cox.py

Gate 1 versus Gate 2 direct interaction:
  analysis/11_phase_stage_interaction.py

Gate 2 completion:
  analysis/10_two_stage_mobility.py

External-context bridge:
  analysis/11_project_context_gate.py
~~~

Older parallel 09/10 scripts that omitted the nine 2015 source expert corrections
are deprecated and intentionally terminate if executed.


## Phase 3 — departure gate versus completion filter

Run:

~~~bash
python analysis/09_departure_gate_completion_filter.py
~~~

This reconstructs the published behavioural migration flag from all six primary-stage projects, including the large migration tables pinned by Git blob SHA.

Current developmental result:

- initiation OR per Durif stage: **1.99** (95% CI **1.49–2.66**);
- completion among initiators OR: **1.29** (95% CI **0.94–1.77**).

Interpretation:

> internal readiness is concentrated at the departure transition; successful post-departure progression is more weakly related to the same readiness measure.

This phase decomposition supersedes treating the successful-migrant endpoint as one indivisible movement outcome.

## Phase 4 — external progression filter

Use the Dutch consecutive-barrier system to test the second phase inside one shared movement landscape.

See [Dutch confirmation protocol](../docs/dutch_barrier_confirmation_protocol.md).
