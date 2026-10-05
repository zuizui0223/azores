# azores

## Main ecological question

> **How strongly does internal migratory readiness control activation of seaward movement, and how much of that stage signal remains once migration is already progressing?**

This project began from an extreme Azores yellow-eel system in which 36 tagged individuals showed very strong pool fidelity and zero valid receiver-to-receiver movement.

The goal is **not** to rediscover site fidelity.

The current ecological result is phase specific:

1. **capture-time Durif stage strongly predicts migration activation;**
2. **advanced stage predicts earlier behavioral onset;**
3. **after activation, there is no general Durif-stage gradient in migration speed.**

Canonical developmental results:

- initiation rates FIII / FIV / FV: **59.0% / 77.9% / 87.4%**
- adjusted initiation OR: **2.08 per stage** (95% CI **1.56–2.76**)
- onset Cox HR: **1.29 per stage** (95% CI **1.13–1.47**)
- post-activation migration-speed ratio: **0.983 per stage** (95% CI **0.852–1.134**, p = **0.815**)

Thus the strongest current statement is:

> **silvering readiness strongly predicts whether and when migration becomes behaviorally expressed, but does not provide a transferable general speed advantage once migration is active.**

A direct reproducibility audit now exactly reproduces the canonical post-activation result (n = 418; speed ratio = 0.983). Project-specific adjusted speed ratios range from 0.915 to 1.272, with weak evidence for between-project coefficient heterogeneity (Cochran Q = 2.469, df = 5, p ≈ 0.781). A 2026 River Test study nevertheless retained silvering stage in a progression-rate model, so the pooled null is not interpreted as biological irrelevance of silvering after activation.

See:
- [post-activation speed reproducibility audit](docs/POST_ACTIVATION_SPEED_REPRO_AUDIT_2026_10_05.md)
- [project-level speed diagnostic](results/post_activation_speed_project_heterogeneity_v1.json)

## Important endpoint correction

The upstream file `successful_migrants_final_detection.csv` identifies positive terminal/sea-endpoint records.

The source Europe-wide paper explicitly did **not** estimate escapement success rate because non-detection at the terminal endpoint can reflect fishing, detection loss, release geometry and other study-specific assumptions.

Therefore:

- terminal-endpoint membership is retained only as a **secondary sensitivity endpoint**;
- its complement is **not** called biological failure;
- the former initiation/completion OR-ratio is no longer the primary manuscript evidence.

See:
- [escapement endpoint audit](docs/escapement_endpoint_audit.md)
- [canonical phase-control v2](results/phase_control_canonical_v2.json)

## Primary post-activation question

The open biological question is now:

> **once migration is active, which barrier, hydrological and route conditions determine progression?**

The Dutch pump -> lake -> tidal-sluice system is the active within-route confirmation target.

See:
- [submission-canonical manuscript V3](manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md)
- [V3 numeric contract](manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V2.json)
- [V3 QC PASS](manuscript/MANUSCRIPT_QC_V2.json)
- [canonical activation/onset/progression evidence](results/phase_control_canonical_v2.json)
- [post-initiation speed result](docs/post_initiation_speed_result.md)
- [Dutch barrier confirmation protocol](docs/dutch_barrier_confirmation_protocol.md)
- [data feasibility audit](docs/data_feasibility_audit.md)
- [analysis programme](analysis/README.md)

## Additional movement-onset result

The same internal-state signal appears before the final successful-migrant endpoint.

Across six upstream migration projects, a project-year stratified Cox model of **time to first classified migration episode** included body length and within-year release timing.

- n = **570**
- classified migration episodes = **418**
- Durif FIII -> FIV -> FV: hazard ratio **1.28** per stage
- 95% CI **1.12–1.45**
- p ≈ **2.2×10⁻⁴**

Thus capture-time Durif readiness predicts both **whether downstream movement is ultimately realized** and **how rapidly the published classifier identifies a migration episode**.

See [first migration episode result](docs/first_migration_episode_result.md).

## Post-activation project heterogeneity audit

The pooled near-null Durif effect on post-activation speed is not explained by obvious cancellation of strong opposing project effects.

Using the same speed definition and covariate structure within each of the six projects, stage-specific speed ratios ranged from approximately **0.915 to 1.272**. A Cochran heterogeneity audit gave **Q = 2.47**, **df = 5**, **p = 0.781**.

Thus the current data do not support a strong Durif-stage × water-body interaction in overall migration speed.

The supported interpretation is narrower:

> **silvering readiness has a strong general predictive signal for activation/onset, whereas its general predictive signal for already-active overall migration speed is weak.**

This does not imply that internal state becomes biologically irrelevant after activation, and it does not demonstrate that route opportunity causally replaces internal control. A recent River Test study uses a different reach-level progression endpoint and shows that silvering stage can still contribute within a particular route context.

See [post-activation project heterogeneity audit](docs/post_activation_speed_project_heterogeneity.md).

## Evidence boundary

These are developmental independent results, not outcome-blind confirmation.

Durif stages already encode migratory readiness, so the initiation association is biologically expected and is not novelty by itself. The stronger contribution is the **phase-resolved decomposition** showing that the same stage gradient that predicts activation is absent from the generic post-activation speed response.

## Role of EOG

EOG is only the discovery route. It exposed temporal structure in a system with no observed receiver-to-receiver propagation, motivating the question of when latent mobility is actually expressed and what controls movement after activation.

## Three separate EOG-derived ecology programmes

Azores is one of three independent ecological projects:

- **Azores:** state-dependent mobility gating;
- **Louisiana:** within-home-range micro-niche tracking;
- **Tampa:** buffered persistence under quantitative degradation.

These are not intended as one umbrella analysis or one shared endpoint.

See [three independent ecology programmes](docs/three_ecology_programs.md).


- [three-programme current status](docs/three_ecology_programs_status.md)


## Submission figures

Endpoint-audited reference renders are now committed:

- `manuscript/rendered_figures_v2/Figure1.svg`
- `manuscript/rendered_figures_v2/Figure2.svg`
- `manuscript/rendered_figures_v2/Figure3.svg`
- `manuscript/rendered_figures_v2/Figure4.svg`

Render QC:
- `manuscript/RENDERED_FIGURE_QC_V2.json` — **PASS_REFERENCE_RENDER**

Numeric content is locked to `FIGURE_DATA_CONTRACT_V2.json`; terminal positive-set sensitivity remains supplementary only.
