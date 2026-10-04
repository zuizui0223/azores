# Dutch consecutive-barrier confirmation protocol v2

## Role

The Europe-wide eel panel now supports two developmental internal-state signals:

- later successful migration;
- earlier detected migration onset.

The unresolved question is no longer whether Durif stage matters on average.

It is:

> **Does internal migratory readiness alter which passage opportunities an eel can exploit?**

Source:
- van Rijn et al. 2026
- DOI 10.1139/cjfas-2025-0359
- DANS data DOI 10.17026/LS/WTSUNG

## Why the original paper does not already answer this question

The source paper followed 40 eels through a pumping station (PS) and a tidal sluice (TS).

Durif composition was approximately:

- FIII pre-migrant: **11**
- FIV: **6**
- FV: **23**

The source analysis:

- included Durif stage as a candidate individual predictor at the PS, where it was dropped during model selection;
- excluded Durif stage from the TS individual model because FIV body mass and stage could not be separated adequately;
- modelled event-level population passage probabilities after aggregating individual attempts.

Therefore a simple re-test of the Durif main effect would be redundant.

## New ecological estimand: opportunity exploitation

For every eel that eventually passes a barrier, reconstruct its **choice set**:

~~~text
missed opportunity 1
missed opportunity 2
...
successful opportunity
~~~

The individual eel is its own matched stratum.

The question is:

> **does FIII versus FIV/FV readiness change the environmental strength of the opportunity that is sufficient to trigger passage?**

This is a case-crossover / conditional-choice question.

## Primary readiness definition

Freeze:

~~~text
pre-migrant = FIII
migrant-ready = FIV or FV
~~~

This grouping follows the biological interpretation in the source paper and is fixed before opening the DANS attempt-level data.

Do not split FIV/FV after seeing results.

## Primary opportunity variable

### Discharge-event duration

Use the source-defined duration of each passage opportunity as the primary continuous opportunity-strength axis.

Reason:

- a passage opportunity only exists during an operational discharge/opening window;
- duration is defined independently of whether a specific eel uses it;
- it is available at both barriers;
- it has direct biological meaning as the length of time an eel has to exploit a passage window.

Primary interaction:

~~~text
passage_this_opportunity
  ~ log(discharge_duration)
  + migrant_ready × log(discharge_duration)
  | matched within eel
~~~

Because readiness is constant within eel, its main effect is conditioned out. The estimand is the **difference in opportunity-response slope** between FIII and FIV/FV.

## Biological prediction

The directional hypothesis is:

> **migrant-ready FIV/FV eels should require less extreme/long passage windows than FIII pre-migrants.**

Under the conditional-logit parameterization above, this predicts a weaker positive dependence on long duration for FIV/FV than for FIII.

If advanced fish instead wait for stronger opportunities, the interaction will point in the opposite direction and the gating hypothesis must be revised.

## Barrier-specific analysis

Fit the matched model separately at:

1. pumping station;
2. tidal sluice.

Do not pool barriers as interchangeable.

The ecological test is whether the readiness × opportunity relationship itself changes between the two barrier mechanisms.

## Secondary event variables

Only after the primary duration interaction is reported:

### Pumping station
- wind speed in the frozen source window;
- discharge volume.

### Tidal sluice
- moon illumination;
- discharge volume.

These are secondary because the original paper identified barrier-specific associations after outcome modelling.

They cannot rescue a null primary duration interaction.

## Body-size confounding

The source paper found stage/body-mass confounding at the tidal sluice.

A matched choice model removes the constant main effects of both stage and body mass, but it does **not** automatically remove confounding of:

~~~text
stage × opportunity
versus
body mass × opportunity.
~~~

Therefore freeze one sensitivity model:

~~~text
passage
  ~ duration
  + migrant_ready × duration
  + body_mass × duration
  | eel
~~~

If the readiness interaction becomes unidentified or unstable, report **non-identifiable** rather than dropping body mass.

## Why matched choice sets help

This design avoids treating hundreds of attempts as independent animals.

Each eel contributes one matched choice set, and the inference asks which event within that individual's available set was used.

Fish with only one available opportunity contain no within-eel choice information and do not contribute to the primary conditional likelihood.

Fish that never pass have no chosen event and are reported separately; they do not enter the primary matched-choice model.

## Primary support rule

For each barrier report:

- number of informative eel choice sets;
- FIII versus FIV/FV representation;
- coefficient and interval for log duration;
- coefficient and interval for readiness × log duration;
- fish-level leave-one-out stability.

The readiness interaction is considered supported only if:

1. its two-sided 95% interval excludes zero;
2. its sign is stable under fish-level leave-one-out;
3. it remains directionally stable in the body-mass × duration sensitivity where estimable.

## Cross-barrier interpretation

The strongest result is not necessarily the same interaction at both barriers.

A biologically interesting outcome is:

> **internal readiness changes opportunity exploitation at one barrier type but not the other.**

That would directly support the emerging hypothesis that landscape infrastructure changes how internal migratory state is translated into realized movement.

## Failure condition

If readiness × opportunity is unsupported at both barriers under adequate information, the Europe-wide stage effect remains real as a predictor but the proposed **passage-opportunity gating mechanism** is weakened.

## Evidence boundary

This is an independent dataset, but the source paper and its published results were read before this v2 protocol.

The new **matched within-eel interaction estimand** is frozen before opening the DANS attempt-level data in this project.
