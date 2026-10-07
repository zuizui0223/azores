# Capture-stage staleness diagnostic — 2026-10-07

## Biological alternative

The canonical six-project result shows:

- strong capture-time Durif association with migration activation and onset;
- no general Durif gradient in post-activation whole-migration speed.

A biologically plausible alternative to a phase-specific interpretation is **state convergence**.

Durif stage is a developmental state, not a permanent trait. Palstra et al. (2011; DOI 10.1007/s10695-011-9496-x) showed strong temporal progression in migratory/maturation status during the downstream migration season, with stage-3 and stage-4 eels declining and stage-5 becoming increasingly dominant.

Because capture-time FIII eels also take longer to activate migration in the present panel, initially less advanced individuals could theoretically progress physiologically before post-activation speed is measured.

## Frozen diagnostic

Before running the diagnostic, two checks were fixed:

1. continuous interaction:
   `capture Durif × log(1 + release-to-activation latency)`;
2. stage-speed models restricted to eels activating within:
   - <=1 day;
   - <=3 days;
   - <=7 days.

Prediction under a simple staleness explanation:

- advanced capture stage should show a positive speed advantage among the fastest activators, where little time has elapsed for convergence;
- that advantage should weaken as activation latency increases, giving a negative stage × latency interaction.

## Reproducible result

The GitHub Actions independent-data audit completed successfully on 2026-10-07.

Joined records with both threshold latency and speed:
- **422**

Canonical informative speed model:
- n = **418**
- ratio per stage = **0.983**
- 95% CI = **0.852–1.134**
- p = **0.815**

### Continuous stage × latency interaction

- beta = **+0.0358**
- 95% CI = **−0.0444 to +0.1159**
- p = **0.382**
- multiplicative interaction = **1.036** per unit increase in centered log latency

The point estimate is positive, not the negative direction predicted by simple decay of a positive stage-speed advantage.

### Rapid activators

| Maximum release-to-activation latency | Model n | FIII / FIV / FV | speed ratio per capture-stage increment | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| <=1 day | 120 | 33 / 15 / 72 | **0.942** | 0.772–1.150 | 0.559 |
| <=3 days | 189 | 55 / 29 / 105 | **0.953** | 0.782–1.161 | 0.634 |
| <=7 days | 231 | 75 / 34 / 122 | **0.963** | 0.798–1.162 | 0.693 |

There is no positive stage-speed point estimate even among eels activating within one day.

## Interpretation

> **The data do not support the simple explanation that the pooled post-activation null is produced because initially less advanced eels merely have time to physiologically catch up before movement speed is measured.**

The result is useful because the <=1-day subset still contains 33 FIII eels, so the diagnostic is not based on an almost empty premigrant group.

However, this is not evidence that physiological convergence never occurs.

The intervals remain compatible with moderate positive or negative stage effects, and no eel was repeatedly assigned a Durif stage after release. Activation latency is also itself a post-capture outcome.

Therefore the correct status is:

**NO_SUPPORT_FOR_SIMPLE_STATE_STALENESS_PATTERN**

not:

**STATE_CONVERGENCE_FALSIFIED**

## Consequence for the main ecological interpretation

This diagnostic strengthens the narrower phase/scale interpretation:

> **capture-time silvering readiness is highly informative for whether and when migration becomes expressed, but it does not behave as a general locomotor-speed ranking once migration is active.**

The River Test result remains important because it shows that silvering stage can contribute to finer reach-level progression. Thus the current synthesis is not "internal state matters only before departure".

It is:

> **the ecological information carried by silvering state changes across response scales: strong for activation, weak for generic whole-route speed, but potentially detectable again for finer route-specific progression.**

## Evidence boundary

This is a post-hoc developmental diagnostic.

It was motivated after the canonical activation/speed contrast was known.

Use it to constrain alternative explanations, not as independent confirmation.

Canonical machine-readable result:
- `results/stage_staleness_diagnostic_v1.json`

Executable analysis:
- `analysis/14_stage_staleness_diagnostic.py`
