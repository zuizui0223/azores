# Finer-scale progression audit: silvering predicts activation, not a general transit-speed advantage

## Why this test was added

The canonical Azores analysis defines post-activation progression using one overall migration-speed value per eel.

A newly published 2026 River Test study retained silvering stage in a repeated reach-level downstream-progression model. That external result raises a legitimate scale question:

> **Does the weak Durif effect in the six-project analysis arise because overall trajectory speed is too coarse, while finer inter-station transit still carries a silvering-stage signal?**

Before inspecting the stage result, this repository froze one alternative progression endpoint in 'results/segment_progression_scale_audit_v1_contract.json'.

No alternative endpoint or trimming threshold is authorized as a rescue.

## Endpoint

For each expert-corrected activated eel:

1. keep upstream rows with 'migration == TRUE';
2. retain finite positive 'speed_m_s', generated upstream from consecutive-station movementSpeeds(..., 'last to first', distance_matrix);
3. require at least two positive segment speeds;
4. use the **individual median positive segment speed** as the eel-level response.

The individual eel, not the segment row, is the biological replicate.

Primary model:

    log(individual median positive segment speed)
      ~ project x release-year fixed effects
      + within-stratum body length
      + within-stratum release timing
      + ordinal Durif stage

## Result

The primary model retained **411 eels** across the same 13 informative project-year strata.

Pooled descriptive medians appear strongly stage ordered:

- FIII: **0.404 m/s** (n=152)
- FIV: **0.518 m/s** (n=53)
- FV: **0.897 m/s** (n=206)

However, after project-year context, body length and release timing were represented, the Durif effect was essentially zero:

- speed ratio per FIII -> FIV -> FV increment: **1.0006**
- 95% CI: **0.831–1.204**

Thus the strong-looking pooled descriptive stage gradient is not a transferable within-context stage effect under the frozen model.

## Project-specific scope

| Project | n | speed ratio/stage | 95% CI |
|---|---:|---:|---:|
| Warnow | 106 | 1.045 | 0.732–1.492 |
| Leopold Canal | 52 | 1.293 | 0.721–2.321 |
| Albert Canal | 123 | 0.882 | 0.580–1.341 |
| Scheldt | 85 | 1.082 | 0.889–1.316 |
| Grote Nete | 33 | 0.962 | 0.838–1.104 |
| ESGL | 12 | 0.722 | 0.201–2.593 |

Between-project heterogeneity is weak:

- Cochran Q = **2.32**
- df = **5**
- p = **0.804**
- tau² = **0**

The fixed-effect project-specific ratio is approximately **1.002**.

So the near-null adjusted result is not hiding obvious strong positive effects in some projects and strong negative effects in others.

## Agreement with the canonical overall-speed endpoint

Canonical overall trajectory speed:

- ratio/stage = **0.983**
- 95% CI **0.852–1.134**

Finer inter-station transit endpoint:

- ratio/stage = **1.001**
- 95% CI **0.831–1.204**

The two independently defined progression scales therefore tell the same qualitative story.

## Biological interpretation

This makes the phase contrast more specific.

The data do **not** support a simple performance model in which more advanced silvering produces a general transferable increase in movement pace after migration has activated.

> **Silvering readiness is strongly associated with entering the migratory state and with earlier activation, but it does not translate into a general speed advantage either for overall migration progress or for median positive inter-station transit within the six-project cohort.**

This is not equivalent to saying physiology becomes irrelevant after departure.

Stage may still affect particular reaches, burst performance, barrier-specific decisions, energetics, persistence, or endpoints defined differently from the two speed metrics tested here.

## Relation to Moyo et al. 2026

The River Test study and this audit use different progression estimands.

The River Test analysis uses repeated reach-level progression rates and models eel ID as a random effect. The present audit deliberately avoids row-level pseudo-replication and asks whether each eel's median positive inter-station transit speed carries a transferable stage effect across six systems.

Therefore the external study is best treated as a scope boundary:

> **some local progression responses can retain stage information, but the six-project data provide no evidence for a general stage-dependent increase in post-activation movement pace.**

## Novelty consequence

The paper should not claim that the two-phase idea itself is novel.

The stronger empirical contribution is:

> **the same independently measured readiness axis is strongly informative for activation across heterogeneous telemetry systems, yet fails to provide a transferable advantage for two distinct post-activation speed estimands after ecological context is represented.**

This is a phase-specific predictive asymmetry, not an exclusive internal-to-external switch.