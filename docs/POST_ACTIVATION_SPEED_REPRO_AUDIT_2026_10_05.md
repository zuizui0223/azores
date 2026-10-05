# Post-activation speed reproducibility and novelty audit — 2026-10-05

## Status

**RESOLVED_REPRODUCIBLE**

The apparent discrepancy reported earlier in this audit was caused by the GitHub connector omitting the body of very large CSV files in normal file-content retrieval. Direct blob retrieval confirmed that the three apparently blank migration files are large, non-empty source files:

- `migration_2012_leopoldkanaal.csv`: about 5.5 MB
- `migration_2013_albertkanaal.csv`: about 29 MB
- `migration_2015_phd_verhelst_eel.csv`: about 2.9 MB

The pinned upstream source itself is not missing these inputs.

## Exact reproduction

Repository: `PieterjanVerhelst/eel-meta-analysis`  
Pinned commit: `59578cb622dddbbba5174b4c51bff0807787385a`

Using the six migration files named in `analysis/12_post_initiation_speed.py`, direct blob retrieval, the source expert-nonmigrant exclusions, the same project-year eligibility rule, and the same regression specification reproduces the canonical result exactly:

- valid speed-bearing stage-coded initiators before project-year eligibility: **422**
- informative project-year strata: **13**
- modelled eels: **418**
- Durif coefficient on log migration speed: **-0.01703547**
- speed ratio per FIII -> FIV -> FV increment: **0.98310882**
- 95% CI: **0.85240163–1.13385863**

Thus the canonical n=418 / ratio=0.983 result is submission-reproducible from the pinned upstream source.

## Project-level diagnostic

The same model was fitted separately within each project, preserving release-year fixed effects and within-stratum body length/release-timing adjustment.

| Project | n | speed ratio / stage | 95% CI |
|---|---:|---:|---:|
| 2011 Warnow | 107 | 0.915 | 0.682–1.228 |
| 2012 Leopold Canal | 52 | 0.981 | 0.678–1.420 |
| 2013 Albert Canal | 128 | 1.272 | 0.899–1.799 |
| 2015 Scheldt | 86 | 1.011 | 0.856–1.193 |
| 2019 Grote Nete | 33 | 1.035 | 0.731–1.465 |
| ESGL | 12 | 1.219 | 0.675–2.201 |

A fixed-effect heterogeneity diagnostic gives:

- Cochran Q = **2.469**
- df = **5**
- p ≈ **0.781**

Therefore the six-project dataset does not support strong between-project heterogeneity in the post-activation Durif coefficient.

Leave-one-project-out pooled ratios remain close to one (**0.953–1.029**).

## Novelty update from 2026 external evidence

Moyo et al. (2026, *Hydrobiologia*, DOI 10.1007/s10750-026-06406-6) reported a detectable silvering-stage contribution to downstream progression rate in the River Test.

That result should not be described as contradicting the present six-project analysis. A stage effect may be detectable in a particular system even when there is no transferable pooled effect across multiple systems.

The safe ecological interpretation is:

> **Silvering readiness has a strong and transferable association with migration activation, but it does not provide a general Europe-wide post-activation speed advantage. Context-specific post-activation effects remain biologically possible.**

Do not strengthen this to:

- silvering is irrelevant after activation;
- all route systems erase internal-state effects;
- post-activation control is purely external;
- project heterogeneity has been demonstrated in the present six-project data.

## Consequence for the paper

The speed endpoint can remain primary progression evidence.

The paper should frame the contribution as **phase-specific transferability of an internal-state signal**, not a universal switch from internal to external control.

## Audit resolution

The temporary `STOP_POST_ACTIVATION_SPEED_REPRO_AUDIT` is lifted.
