# Post-initiation speed heterogeneity audit

## Question

The pooled post-initiation speed model gives a near-null Durif-stage effect, but a newly published 2026 River Test study retained silvering stage in a reach-level downstream-progression model. This follow-up asks a narrower question:

> **Is the weak pooled Durif effect in the six-project analysis hiding strong between-project heterogeneity?**

This is a post-hoc scope/novelty audit, not a preregistered confirmation test.

## Canonical population

The direct-blob reproducibility audit restored the full pinned upstream inputs and exactly reproduced the canonical speed analysis:

- n = **418** activated eels;
- six projects;
- pooled speed ratio per FIII -> FIV -> FV increment = **0.983**;
- 95% CI **0.852–1.134**.

## Project-specific stage effects

Each project was fit separately using the same basic adjustment logic as the pooled analysis: release-year fixed effects where multiple informative years were available, within-stratum body length and release timing, and ordinal Durif stage.

| Project | n | FIII / FIV / FV | speed ratio per stage | 95% CI |
|---|---:|---:|---:|---:|
| Warnow | 107 | 61 / 23 / 23 | **0.915** | 0.682–1.228 |
| Leopold Canal | 52 | 21 / 7 / 24 | **0.981** | 0.678–1.420 |
| Albert Canal | 128 | 26 / 1 / 101 | **1.272** | 0.899–1.799 |
| Scheldt | 86 | 34 / 19 / 33 | **1.011** | 0.856–1.193 |
| Grote Nete | 33 | 6 / 2 / 25 | **1.035** | 0.731–1.465 |
| ESGL | 12 | 6 / 1 / 5 | **1.219** | 0.675–2.201 |

The Albert Canal and ESGL point estimates are positive, but precision is limited and stage balance is poor in those systems.

## Formal heterogeneity

Inverse-variance Cochran heterogeneity test on project-specific log-speed coefficients:

- Q = **2.47**
- df = **5**
- p = **0.781**
- DerSimonian-Laird tau² = **0**

The fixed/random pooled project-specific ratio is approximately **1.028**.

Thus the six-project data do **not** support a strong project-by-stage heterogeneity explanation for the pooled near-null speed effect.

## What the 2026 River Test paper changes

Moyo et al. (2026; DOI 10.1007/s10750-026-06406-6) analysed 25 silver eels in the River Test. Their reach-level mixed-effects progression analysis retained silvering stage along with temperature, barriers, flow and moon illumination after model selection.

That result should not be described as a direct contradiction because the estimands differ:

- Tampa/Azores repository endpoint here: one overall migration-speed value per activated eel across its classified migration trajectory;
- River Test: repeated reach-level progression rates with eel ID as a random effect;
- stage coding and environmental covariates also differ.

The external paper nevertheless sets an important scope boundary:

> **silvering stage can remain informative for some post-activation progression responses in some systems.**

## Updated biological conclusion

The strongest supported statement is therefore narrower than a universal control handoff:

> **Capture-time silvering readiness is a strong and transferable predictor of migration activation and onset across the six-project cohort, whereas it provides little general predictive information for the pooled overall post-activation speed endpoint.**

Do not strengthen this to:

> internal state stops mattering after activation.

Nor do the six projects support:

> the stage effect changes strongly among projects.

The unresolved general question is now about **which post-activation response definition and environmental scale expose residual internal-state effects**.

That is a better next question than searching for another pooled stage p-value.
