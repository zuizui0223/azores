# Post-activation speed reproducibility and novelty audit — 2026-10-05

## Final reproducibility resolution

The canonical post-activation speed result is reproducible from the pinned upstream source.

Repository: `PieterjanVerhelst/eel-meta-analysis`  
Pinned commit: `59578cb622dddbbba5174b4c51bff0807787385a`

The earlier audit temporarily treated three large migration CSVs as empty because the GitHub contents wrapper returned zero text for oversized files. Direct Git blob retrieval showed that this was a connector-size/display limitation, not missing upstream data.

Blob sizes recovered:

- 2012 Leopold Canal: ~5.47 million characters;
- 2013 Albert Canal: ~29.0 million characters;
- 2015 Scheldt: ~2.94 million characters.

The earlier zero-byte interpretation is withdrawn.

## Exact independent replay

Using the same six-project universe, expert nonmigrant corrections, speed definition, project-year eligibility rule, within-stratum body-length centering, within-stratum release-timing centering and ordinal FIII/FIV/FV stage coding as `analysis/12_post_initiation_speed.py`:

- stage-coded metadata records: **603**;
- expert-corrected speed-bearing initiators before stratum filtering: **422**;
- informative project-year strata: **13**;
- modelled individuals: **418**.

Stage counts among the 418 modelled individuals:

- FIII: **154**;
- FIV: **53**;
- FV: **211**.

Median migration speeds:

- FIII: **0.0228976 m/s**;
- FIV: **0.0232434 m/s**;
- FV: **0.0244765 m/s**.

Adjusted ordinal Durif effect:

- beta: **-0.01703547**;
- speed ratio per stage: **0.98310882**;
- 95% CI: **0.85240163–1.13385863**.

These match the canonical manuscript values to numerical precision.

## Reproducibility status

**PASS_POST_ACTIVATION_SPEED_REPRO**

The canonical n=418 / ratio=0.983 result is submission-reproducible from the pinned source.

## New project-level heterogeneity audit

The same speed-bearing cohort was then split by source project and the same within-project model form was fitted, retaining project-year fixed effects where multiple informative years occurred.

Adjusted speed ratio per FIII -> FIV -> FV increment:

| Project | n | Speed ratio | 95% CI |
|---|---:|---:|---:|
| 2011 Warnow | 107 | 0.915 | 0.682–1.228 |
| 2012 Leopold Canal | 52 | 0.981 | 0.678–1.420 |
| 2013 Albert Canal | 128 | 1.272 | 0.899–1.799 |
| 2015 Scheldt | 86 | 1.011 | 0.856–1.193 |
| 2019 Grote Nete | 33 | 1.035 | 0.731–1.465 |
| ESGL | 12 | 1.219 | 0.675–2.201 |

Inverse-variance heterogeneity audit:

- Cochran Q = **2.469**;
- df = **5**;
- p ≈ **0.781**.

Thus the pooled near-null result is **not** readily explained by strong opposing project-specific stage effects cancelling one another. Within these six projects, the available stage-speed effects are statistically compatible with a shared weak average effect.

This is a developmental heterogeneity audit, not a preregistered confirmatory test.

## Important new external result

A newly published River Test study (Moyo et al., 2026, *Hydrobiologia*, DOI 10.1007/s10750-026-06406-6) tracked 25 silver European eels. The tagged fish had already initiated downstream movement before capture. In a reach-level mixed model of downstream progression rate, silvering stage remained in the selected model together with temperature, barriers, flow and lunar illumination; removing silvering stage worsened model fit.

This provides a useful external boundary condition:

> a weak Europe-wide individual-level stage gradient in overall post-activation speed does **not** imply that silvering state is irrelevant to progression at finer reach/time scales or under a particular hydrological context.

## Revised ecological hypothesis

Do **not** frame the result as:

> internal state controls activation, then stops mattering after activation.

The stronger and safer formulation is:

> **Migratory readiness has a strong and transferable association with activation, whereas its contribution to progression is scale- and context-sensitive: it is weak in the pooled whole-migration speed metric but can reappear in finer-grained reach-level progression under particular environmental conditions.**

This changes the next question from a pooled-null question to a mechanistic scale question:

> **At what spatial and temporal scale does internal migratory state remain visible once movement has begun, and when is its signal masked by route opportunity and environmental forcing?**

## Next valid analysis

Priority order:

1. keep the canonical pooled overall-speed analysis as the broad-scale progression result;
2. retain the six-project heterogeneity audit as evidence that the pooled null is not simple cancellation;
3. compare whole-route speed with finer reach/barrier progression metrics where open data permit;
4. test stage × independently defined hydrological/opportunity variables only where the measurement structure supports it;
5. do not tune route classes or temporal windows against stage-effect estimates.

## Status

The reproducibility stop is cleared.

The scientific programme is **reopened only for scale/context decomposition**, because new external evidence reveals that "no general post-activation stage gradient" and "stage can matter for reach-level progression" can both be true.
