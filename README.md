# azores

## Main ecological question

> **Does internal migratory readiness change how strongly landscape resistance constrains realised movement?**

This project began from an extreme Azores yellow-eel system in which 36 tagged individuals showed very strong pool fidelity and zero valid receiver-to-receiver movement.

The goal is **not** to rediscover site fidelity.

The ecological hypothesis is:

> **movement capacity is gated by internal life-history state, and the same landscape barrier can have different realised effects depending on how ready the animal is to move.**

Azores is the deep-residence anchor.

The main independent test now uses the open Europe-wide European eel panel, where capture-time Durif stages are available independently of later telemetry movement. The primary cohort is FIII/FIV/FV; the focal test is:

~~~text
later movement ~ Durif stage
               + landscape resistance
               + Durif stage × landscape resistance
               + project/design covariates
~~~

See:

- [Azores-specific ecological principle](docs/specific_general_principle.md)
- [stay in place versus stay in state](docs/azores_louisiana_contrast.md)
- [independent test protocol](docs/independent_test_protocol.md)
- [data feasibility audit](docs/data_feasibility_audit.md)
- [analysis programme](analysis/README.md)

## Current developmental result

Project-fixed ordinal analysis of the Europe-wide panel shows a strong stage signal, used here as a **positive control rather than the novelty claim**:

- FIII -> FIV -> FV: OR **1.89** per stage increment;
- 95% CI **1.49–2.38**;
- body-size and release-timing robustness: OR **1.74**, 95% CI **1.37–2.22**.

Project heterogeneity is strong. Because FIII is biologically pre-migrant and FIV/FV are migratory stages by the Durif framework, this result validates the readiness axis but does not itself constitute the novel ecological finding. The paper target is **why readiness is translated into movement differently among external contexts**.

See:
- [project-fixed stage result](docs/project_fixed_stage_result.md)
- [body/timing robustness](docs/stage_effect_body_timing_robustness.md)

## Movement initiation result

The public migration classifier separates movement initiation from final successful migration.

Across six projects and **575** tracked FIII/FIV/FV eels:

- descriptive classified-migration initiation: FIII **61.7%**, FIV **79.4%**, FV **87.8%**;
- after project×release-year, body length and release timing adjustment:
  - OR **1.99** per Durif-stage increment;
  - 95% CI **1.49–2.66**;
- among 382 initiators, each Durif-stage increment was associated with a **0.72×** factor in `1 + days to detected migration` (95% CI **0.57–0.91**).

Thus the developmental evidence now supports **state-dependent movement initiation**, not only a final successful-migrant endpoint.

See [migration initiation result](docs/migration_initiation_result.md).

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
