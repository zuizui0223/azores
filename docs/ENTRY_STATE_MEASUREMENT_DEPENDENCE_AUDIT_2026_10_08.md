# Measurement dependence audit: Durif stage vs weight-for-length condition

**Correction 2026-10-08:** An earlier version incorrectly claimed raw eye and fin measurements were unavailable. This document now records the actual `length2/3/4` measurements and the five-project coverage, verified at the pinned source commit.

**2026-10-08 — interpretive and provenance audit**

## Confirmed source facts

The public source archive pinned to
`PieterjanVerhelst/eel-meta-analysis@59578cb622dddbbba5174b4c51bff0807787385a`
contains `data/interim/eel_meta_data.csv`. Its header contains `length1`, `weight`, `sex`, `life_stage`, collection metadata and locations, **as well as `length2/3/4`, their recorded measurement types and units**. The first header-only audit incorrectly treated those generically named length fields as absent morphometrics.

**Correction based on parsing actual pinned source rows:** Horizontal and vertical eye diameters and pectoral fin length are present, though their assignment to `length2`, `length3` and `length4` **differs by project**. Of the six focal projects, five include morphometrics for at least some FIII–FV individuals: Leopoldkanaal (80/80 raw stage-coded fish), Albertkanaal (152/157), Verhelst 2015 cohort (135/135), Grotenete (38/38) and ESGL (47/47). Warnow (0/146) does not. These counts are from the broader metadata and must not be confused with the 575 movement-evaluable sample. The source still does **not** expose a ready-made continuous Durif discriminant score, but a continuous eye index and relative pectoral fin length can be constructed for the available subset.

The current Azores score defines capture condition as a standardized residual
from a regression of log body weight on log length, project and the three
ordinal Durif classes. That makes it distinct from the *class label* by
construction, but **does not make it physiologically independent** of Durif.

Published source context:
- Durif, Dufour & Elie (2005), *The silvering process of Anguilla anguilla: a new classification from the yellow resident to the silver migrating stage*. J Fish Biol 66, 1025–1043.
  DOI: https://doi.org/10.1111/j.0022-1112.2005.00662.x.
  Their stage III is described as premigrant; IV/V as migrating female stages.
- Sundin et al. (2022), *Evaluation of Sampling Methods for Maturation Stage Determination in the European Eel Anguilla anguilla*, Marine and Coastal Fisheries 14, e10219.
  DOI: https://doi.org/10.1002/mcf2.10219.
  The Durif silvering index uses body length, mass, eye diameter and pectoral fin length; between-observer and measurement effects can alter classification.

Thus an extra weight-for-length term can recover **continuous morphometric
variation discarded when a multidimensional silvering phenotype is compressed
to the ordinal FIII/FIV/FV class**, even without uncovering a distinct
physiological reserve axis.

## The ecological interpretation ladder

1. **Supported for this study panel:** the body-mass residual contains some
   additional predictive information for telemetry-classified initiation
   relative to the ordinal class and basic morphometrics. The gain is
   heterogeneous among six held-out projects; project-level uncertainty crosses
   zero in the pooled analysis.
2. **Plausible, untested:** the residual is a proxy for energetic stores,
   endocrine readiness, or terminal physiological competence.
3. **Not supported by available data:** a causal energetic threshold within
   silvering stage; physiologically independent inputs to entry-state control;
   measured fat content or swimming capacity; conservation-benefit magnitude.

To distinguish explanation (1), due only to ordinal coarsening, from a more independent condition contribution, we **can now reconstruct a subset of the underlying continuous morphology**: normalized eye diameter/eye index and relative pectoral fin length, together with body length and mass. The pinned public metadata contain those observations for five focal projects; the remaining challenge is valid type/units harmonization, eligible-fish intersection and project-held-out testing. Direct lipid measurements and prospective validation are still unavailable, and even an additional weight residual after eye/fin adjustment does not prove energetic causation.

## Consequences for the stage decomposition

FIII is a morphology-defined **premigrant** category; FIV and FV are
morphology-defined **migrating female** categories in the classification,
not guaranteed behavioral outcomes after telemetry release.

This matters for interpreting the observed 2015-corrected activation rates:
FIII 154/261 classified as initiating, FIV 53/68, FV 215/246.
The remaining animals are algorithmic non-initiation/undetected within the
monitoring window, **not validated biological failure or loss of escapement**.

Do not interpret a stronger AUC increment in FV as evidence for a *final
energetic checkpoint* unless it remains stable in same-project-year
comparisons and direct measurements (or appropriate physiological natural
experiments) are added.

## Falsifiable follow-up with better data

Within future matched captures, collect eye and fin morphometrics, weight,
length, directly measured body composition (fat/lipid) and local hydrological
time series, then test:

- **Coarse-class-information explanation:** a continuous Durif discriminant
  score removes condition's incremental predictive gain.
- **Independent readiness explanation:** body composition improves held-out
  migration initiation prediction even after the *continuous* Durif features.
- **Cue-dependent readiness explanation:** condition effects interact with
  observed discharge/tide opportunity at onset, and this interaction
  replicates between waterways.

No causal or conservation claim is made by the current dataset alone.
