# Post-activation Durif-speed heterogeneity audit

## Question

The pooled Europe-wide model gives a post-activation Durif speed ratio of **0.983 per stage**. A possible explanation was that strong but opposing stage effects in different routes cancelled in the pooled mean.

This audit tests that explanation directly using the same pinned upstream source, speed definition, project-year eligibility rule, body-length adjustment and release-timing adjustment as the canonical speed analysis.

## Project-specific effects

| Project | n | FIII/FIV/FV | speed ratio per stage | 95% CI |
|---|---:|---:|---:|---:|
| 2011 Warnow | 107 | 61/23/23 | **0.915** | 0.682–1.228 |
| 2012 Leopoldkanaal | 52 | 21/7/24 | **0.981** | 0.678–1.420 |
| 2013 Albertkanaal | 128 | 26/1/101 | **1.272** | 0.899–1.799 |
| 2015 Scheldt | 86 | 34/19/33 | **1.011** | 0.856–1.193 |
| 2019 Grote Nete | 33 | 6/2/25 | **1.035** | 0.731–1.465 |
| ESGL | 12 | 6/1/5 | **1.219** | 0.675–2.201 |

Cochran heterogeneity test:

- Q = **2.469**
- df = **5**
- p = **0.781**
- I² = **0%**

## Result

There is no detectable project-level heterogeneity in the Durif-stage effect on the canonical post-activation speed endpoint.

Thus the pooled near-null result is **not** readily explained by strong positive effects in some routes being cancelled by strong negative effects in others.

The best-supported statement within this six-project dataset remains:

> **capture-time Durif readiness has a strong and transferable association with migration activation and onset, but it does not show a comparable general association with the canonical post-activation speed endpoint.**

## What this changes

The external-context explanation should be narrowed.

Do **not** claim that the present six-project data demonstrate a stage × route-context interaction. They do not.

A separate 2026 river study can still show a stage contribution to a different progression-rate endpoint in its own system. That is evidence that a post-activation stage effect can exist, not evidence that the current Europe-wide dataset contains detectable project heterogeneity.

## Important limitation

Stage balance is poor in several systems, most notably Albertkanaal (only one FIV individual), and the smallest projects have wide intervals. Therefore I²=0% is a failure to detect heterogeneity, not proof of universal equality.

## Evidence status

Post-hoc novelty/generalization audit, triggered by external 2026 evidence. It does not replace the canonical pooled speed analysis.


## 2026 River Test comparison

Moyo et al. (2026, Hydrobiologia; DOI 10.1007/s10750-026-06406-6) does not estimate the same progression endpoint as the present Europe-wide speed analysis.

Their primary progression model is reach-level:

- progression rate is calculated within river reaches;
- each eel contributes repeated reach observations;
- eel ID is a random effect;
- fixed effects include silvering stage, temperature, barriers, flow and moon illumination;
- silvering stage is retained by AICc model selection.

By contrast, the present canonical Europe-wide endpoint is one overall migration-speed value per eel, calculated across all migration==TRUE rows before fitting project-year-adjusted stage effects.

Therefore the two results are compatible:

> **silvering stage need not produce a transferable effect on whole-route average speed even if it influences local progression rate within a particular river and environmental context.**

This shifts the ecological interpretation away from "stage stops mattering after activation" and toward a scale-specific statement:

> **the strong cross-system signal of readiness is concentrated at activation; after activation, any remaining readiness effect is more local/process-specific and does not appear as a general whole-route speed gradient across the six-project dataset.**

This is a stronger and safer boundary than claiming a complete internal-to-external control switch.
