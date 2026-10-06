# Post-activation speed reproducibility and novelty audit — resolved 2026-10-06

## Status

**REPRODUCIBILITY RESOLVED. NOVELTY/GENERALITY REMAINS OPEN.**

The earlier apparent discrepancy in the post-activation speed endpoint was caused by the GitHub connector omitting the contents of several very large CSV files when they were fetched through the repository-contents route. Direct blob retrieval shows that the files are present and large, not zero-byte.

The previously added STOP based on apparent missing input files is therefore withdrawn.

## Frozen source

Repository: `PieterjanVerhelst/eel-meta-analysis`  
Pinned commit: `59578cb622dddbbba5174b4c51bff0807787385a`

Current analysis:
- `analysis/12_post_initiation_speed.py`

Large source blobs confirmed directly:
- `migration_2012_leopoldkanaal.csv`: 5,469,591 characters retrieved
- `migration_2013_albertkanaal.csv`: 29,015,367 characters retrieved
- `migration_2015_phd_verhelst_eel.csv`: 2,941,361 characters retrieved

## Exact independent reproduction

The six source migration files plus metadata were re-read from the pinned commit and the committed Python logic was independently reimplemented.

Stage-coded expert-corrected `migration == TRUE` individuals by project:

- 2011 Warnow: 107
- 2012 Leopoldkanaal: 52
- 2013 Albertkanaal: 132
- 2015 phd_verhelst_eel: 86
- 2019 Grotenete: 33
- ESGL: 12

Total expert-corrected initiators represented before project-year eligibility filtering: **422**.

The committed project-year eligibility rule retains 13 informative strata and **418** individuals.

Independent reproduction:

- n = **418**
- Durif log-speed coefficient = **-0.0170354672**
- speed ratio per stage = **0.9831088159**
- 95% CI = **0.8524016314–1.1338586275**

These match the canonical result to numerical precision.

Stage-specific medians also reproduce:

- FIII n=154, median **0.0228976 m/s**
- FIV n=53, median **0.0232434 m/s**
- FV n=211, median **0.0244765 m/s**

Therefore the canonical pooled speed endpoint is reproducible and submission-safe with respect to the pinned source.

## Project-specific stage effects

A follow-up decomposition fit the same adjusted log-speed structure separately within each project where estimable.

Speed ratio per FIII -> FIV -> FV increment:

- Warnow: **0.915** (95% CI 0.682–1.228; n=107)
- Leopoldkanaal: **0.981** (0.678–1.420; n=52)
- Albertkanaal: **1.272** (0.899–1.799; n=128)
- Scheldt: **1.011** (0.856–1.193; n=86)
- Grotenete: **1.035** (0.731–1.465; n=33)
- ESGL: **1.219** (0.675–2.201; n=12)

Inverse-variance heterogeneity audit:

- Q = **2.47**
- df = **5**
- p = **0.781**
- I2 = **0%**

Thus the present six-project dataset does **not** support detectable between-project heterogeneity in the Durif-stage effect on post-activation speed.

The visually different point estimates should not be promoted into a context-dependent interaction claim.

## External 2026 River Test result

Moyo et al. (2026, Hydrobiologia; DOI 10.1007/s10750-026-06406-6) analysed 25 silver eels in the River Test and retained silvering stage in a mixed-effects model of downstream progression rate together with temperature, barriers, flow and moon illumination.

This is useful external evidence that a silvering-stage contribution to progression can be detectable in a specific river context.

However:

- the River Test sample is small;
- its progression metric and design differ from the pooled Europe-wide speed endpoint;
- the current six-project reanalysis does not show significant stage-effect heterogeneity.

Therefore the River Test should be treated as an external boundary case, not as proof of a stage × route-context interaction.

## Revised ecological interpretation

The strongest supported statement remains:

> **Capture-time Durif readiness strongly predicts migration activation and onset, whereas no general transferable Durif-stage gradient is detectable in pooled post-activation migration speed across the six-project dataset.**

Do not strengthen this to:

> silvering stage ceases to matter after activation.

A better boundary is:

> **The transferable effect of silvering stage is concentrated at activation; stage effects on subsequent progression may occur in particular systems but are not a consistent cross-system gradient in the present dataset.**

## Novelty consequence

The two-phase idea itself is not novel enough to carry the paper alone.

The potentially distinctive empirical contribution is narrower:

1. the same independently measured readiness axis is evaluated against activation, onset and progression;
2. the activation effect is strong and project-robust;
3. the same ordinal gradient is not transferable to pooled post-activation speed;
4. an external River Test study shows that local progression effects can still exist.

This shifts the paper from a universal "control handoff" claim to a **transferability boundary**:

> **internal readiness is a general predictor of entering migration, but not a universally portable predictor of how migration proceeds once active.**

That is the formulation to test against the broader migration literature.
