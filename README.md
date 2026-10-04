# azores

## Main ecological question

> **Does control of movement shift from internal migratory readiness at initiation to external ecological opportunity during progression?**

This project began from an extreme Azores yellow-eel system in which 36 tagged individuals showed very strong pool fidelity and zero valid receiver-to-receiver movement.

The goal is **not** to rediscover site fidelity.

The ecological hypothesis is now two-stage:

> **internal life-history state regulates the release of migration; after migration begins, route-specific ecological opportunity and prior route experience increasingly govern progression.**

The Europe-wide panel supports the initiation clause. The independent Dutch consecutive-barrier study provides compatible external evidence for the progression clause: Durif stage did not persist as a generic barrier predictor, whereas discharge, wind, moon and prior passage experience did.

Azores is the deep-residence anchor.

The main developmental test uses the open Europe-wide European eel panel, where capture-time Durif stage is independent of later telemetry movement.

The focal analysis is now phase-specific:

~~~text
Gate 1 — activation
migration initiation / onset
  ~ Durif stage
  + project × release-year
  + body length
  + release timing

Gate 2 — progression
speed / passage / completion
  ~ route opportunity
  + barrier / hydrology
  + route history
  + residual Durif effect
~~~

The paper target is the **change in dominant control across phases**, not one pooled stage × landscape coefficient.

See:

- [Azores-specific ecological principle](docs/specific_general_principle.md)
- [stay in place versus stay in state](docs/azores_louisiana_contrast.md)
- [independent test protocol](docs/independent_test_protocol.md)
- [data feasibility audit](docs/data_feasibility_audit.md)
- [analysis programme](analysis/README.md)

## Two-stage mobility result

The Europe-wide panel now separates two sequential movement stages.

### Migration initiation

After source-study expert exclusions and adjustment for project × release year, body length and release timing:

- Durif FIII -> FIV -> FV: OR **2.08** per stage increment;
- 95% CI **1.56–2.76**;
- p ≈ **4.2e-7**.

### Progression after initiation

Among 422 classified initiators:

- completion model: adjusted Durif OR **1.15** per stage increment;
- 95% CI **0.83–1.59**;
- p = **0.41**.

Using the source paper's overall migration-speed definition on 418 initiated eels:

- Durif speed ratio per stage increment: **0.983**;
- 95% CI **0.852–1.134**;
- p = **0.815**.

A direct stacked two-phase model confirms that the stage effect itself attenuates after initiation:

- OR(initiation) / OR(completion) = **1.81**;
- cluster-robust 95% CI **1.15–2.84**;
- phase interaction **p = 0.0099**.

Current biological interpretation:

> **internal readiness strongly regulates whether/when migration is expressed, but does not provide a general advantage for speed or completion once movement has begun.**

The downstream filter remains mechanistically unresolved. Barrier/hydrological opportunity is now the direct confirmation target, not an assumed explanation.

See:
- [migration-initiation result](docs/durif_migration_initiation_result.md)
- [two-stage mobility decomposition](docs/two_stage_mobility_result.md)
- [direct phase-interaction result](docs/phase_stage_interaction_result.md)
- [post-initiation speed result](docs/post_initiation_speed_result.md)

## Current developmental result

Project-fixed ordinal analysis of the Europe-wide panel shows a strong stage signal, used here as a **positive control rather than the novelty claim**:

- FIII -> FIV -> FV: OR **1.89** per stage increment;
- 95% CI **1.49–2.38**;
- body-size and release-timing robustness: OR **1.74**, 95% CI **1.37–2.22**.

Project heterogeneity is strong. Because FIII is biologically pre-migrant and FIV/FV are migratory stages by the Durif framework, this result validates the readiness axis but does not itself constitute the novel ecological finding. The paper target is **why readiness is translated into movement differently among external contexts**.

See:
- [project-fixed stage result](docs/project_fixed_stage_result.md)
- [body/timing robustness](docs/stage_effect_body_timing_robustness.md)

## Canonical migration-initiation result

The expert-corrected six-project reconstruction gives:

- FIII: **154/261 = 59.0%** initiated;
- FIV: **53/68 = 77.9%**;
- FV: **215/246 = 87.4%**;
- adjusted initiation OR per FIII -> FIV -> FV increment: **2.08**;
- 95% CI **1.56–2.76**;
- p ≈ **4.2e-7**.

The older 161/54/216 counts are retained only as an explicitly labelled
**algorithm-only sensitivity** before the nine upstream expert corrections.

See:
- [expert-corrected initiation result](docs/durif_migration_initiation_result.md)
- [direct phase-interaction result](docs/phase_stage_interaction_result.md)

## Migration-onset result

The internal-state signal also appears in **movement onset itself**, not only in final migration success.

A stratified Cox analysis of 570 exact-stage individuals and 418 migration-onset events used project × release-year strata and adjusted for body length and release timing.

Per FIII -> FIV -> FV stage increment:

- threshold-defined migration-onset hazard ratio: **1.29**
- 95% CI: **1.13–1.47**
- p = **0.00016**

Leave-one-project-out stage HRs remained positive (**1.09–1.52**), although removing the 2015 project gave HR **1.09 [0.94–1.27]** and therefore crossed 1.

This is the cleanest current developmental evidence that internal silvering state is associated with earlier expression of the movement phenotype.

See:
- [migration-onset Cox result](docs/migration_onset_cox_result.md)
- [reproducible Cox analysis](analysis/10_migration_onset_cox.py)

## Independent Dutch control-handoff result

The 2026 Dutch consecutive-barrier study provides an external progression-stage constraint:

- 40 eels, all Durif FIII-FV;
- 35 passed the pumping station;
- 27 completed the tidal-sluice passage;
- mean cumulative barrier delay about 34 days;
- Durif was dropped from the pumping-station individual model;
- Durif was non-identifiable at the tidal sluice because stage and body mass were confounded;
- passage instead depended on barrier-specific opportunity, including discharge duration, wind, lunar condition and prior barrier experience.

This is compatible with a **control handoff** from internal readiness at migration activation to external opportunity during migration progression.

See [independent Dutch control-handoff result](docs/dutch_control_handoff_result.md).


## Gate-specific project-context bridge

Across the six Europe-wide projects with compatible migration tables, median WRS impact behaves differently across the two sequential gates:

- WRS vs migration initiation: Spearman rho **+0.029**, exact 6-project permutation p **0.983**;
- WRS vs completion after initiation: rho **-0.928**, exact p **0.022**;
- leave-one-project-out completion rho remains approximately **-0.97 to -0.87**.

The same pattern survives standardization to a common FIII/FIV/FV composition.

This is **not causal WRS evidence** because resistance is strongly project-confounded. Its role is bridge evidence: the external context descriptor aligns with Gate 2 but not Gate 1, matching the initiation–progression control-handoff hypothesis.

See [project-context gate result](docs/project_context_gate_result.md).

## Evidence boundary

The Europe-wide outcome was partially inspected while refining the hypothesis, so it is independent-data developmental evidence rather than an outcome-blind validation.

Project-level leave-one-project-out stability is mandatory, and a later external eel system is required for stronger confirmation.

## Role of EOG

EOG is only the discovery route. It exposed temporal structure in a system with no observed receiver-to-receiver propagation, motivating the question of when latent mobility is actually expressed.


## Three separate EOG-derived ecology programmes

Azores is one of three independent ecological projects:

- **Azores:** state-dependent mobility gating;
- **Louisiana:** within-home-range micro-niche tracking;
- **Tampa:** buffered persistence under quantitative degradation.

These are not intended as one umbrella analysis or one shared endpoint.

See [three independent ecology programmes](docs/three_ecology_programs.md).


- [three-programme current status](docs/three_ecology_programs_status.md)
