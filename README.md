# azores

## Main ecological question

> **What controls the two distinct gates of migration: the decision/readiness to initiate movement, and the ability to complete movement through a resistant landscape?**

This project began from an extreme Azores yellow-eel system in which 36 tagged individuals showed very strong pool fidelity and zero valid receiver-to-receiver movement.

The goal is **not** to rediscover site fidelity.

The current ecological hypothesis is a **two-gate movement model**:

1. **internal migratory state opens the initiation gate;**
2. **landscape/barrier/hydrological context filters movement after initiation.**

The Europe-wide public eel panel now supports the first gate developmentally.

Among FIII/FIV/FV eels represented in processed migration tracks:

- initiation rates: **59.0% / 77.9% / 87.4%**;
- adjusted initiation OR: **2.08 per Durif-stage increment** (95% CI 1.56–2.76);
- after conditioning on initiation, the stage effect on the published successful-migrant endpoint weakens to **OR 1.15** (95% CI 0.83–1.59).

The direct phase test is stronger than comparing separate p-values:

- initiation/completion stage-OR ratio: **1.81**
- 95% CI: **1.15–2.84**
- p = **0.0099**
- LOPO direction: **6/6** projects.

Thus the strongest current result is:

> **the predictive association of internal migratory readiness is significantly attenuated after migration activation.**

The source inputs are pinned to upstream commit `59578cb622dddbbba5174b4c51bff0807787385a`.

See:

- [two-gate movement hypothesis](docs/two_gate_movement_hypothesis.md)
- [canonical phase-control result](results/phase_control_canonical_v1.json)
- [direct phase interaction](docs/phase_stage_interaction_result.md)
- [canonical developmental result](results/two_gate_movement_developmental_v1.json)
- [migration initiation analysis](analysis/09_migration_initiation_by_durif.py)
- [post-initiation analysis](analysis/10_post_initiation_success_by_durif.py)
- [Dutch barrier confirmation protocol](docs/dutch_barrier_confirmation_protocol.md)
- [data feasibility audit](docs/data_feasibility_audit.md)
- [analysis programme](analysis/README.md)

## Migration-classification and direct-detection result

Using all six public migration tables:

- FIII/FIV/FV metadata individuals: **603**
- represented in migration tables: **575**
- adjusted odds of a trajectory meeting the published migration criterion: **OR 1.99 per Durif stage** (95% CI 1.49–2.66, p≈3.2×10⁻⁶)
- adversarial missingness bound: **OR 1.74** (95% CI 1.32–2.28)
- among 418 individuals with a direct non-release downstream-movement detection, each Durif-stage increment shortened `1+latency` to **0.696×** (95% CI 0.562–0.863, p≈9.3×10⁻⁴).

Important correction: the first `migration=TRUE` row is **not** treated as natural migration onset, because the published classifier can classify the release row itself as migratory. The timing endpoint is therefore the first directly detected downstream-migration row away from the release station.

See [migration classification and direct-detection result](docs/migration_initiation_latency_result.md).

## Evidence boundary

These are developmental independent results, not outcome-blind confirmation.

The Europe-wide panel strongly supports an internal-state association but cannot establish that WRS causes post-initiation heterogeneity because landscape resistance is strongly entangled with project/system identity.

The next confirmation target is a within-landscape system where the same FIII–FV animals encounter measured barrier/opportunity variation.

## Role of EOG

EOG is only the discovery route. It exposed temporal structure in a system with no observed receiver-to-receiver propagation, motivating the question of when latent mobility is actually expressed and what happens after it is released.

## Three separate EOG-derived ecology programmes

Azores is one of three independent ecological projects:

- **Azores:** state-dependent mobility gating;
- **Louisiana:** within-home-range micro-niche tracking;
- **Tampa:** buffered persistence under quantitative degradation.

These are not intended as one umbrella analysis or one shared endpoint.

See [three independent ecology programmes](docs/three_ecology_programs.md).


- [three-programme current status](docs/three_ecology_programs_status.md)
