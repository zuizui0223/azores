# Dutch consecutive-barrier confirmation protocol v3

## Current decision — arrival-defined risk sets

The earlier v2 protocol used the source study's passage-opportunity table and proposed discharge duration as the primary opportunity-strength axis.

That design is **not primary anymore**.

The source paper defines a passage opportunity partly from whether an eel could physically reach the barrier during a discharge event, and event duration contributes directly to that eligibility calculation. Therefore using the same duration variable as the primary exposure inside that preselected opportunity table creates a definitional dependence between:

- whether a row enters the risk set; and
- the exposure whose effect is being estimated.

This does not make the source analysis invalid for its published purpose, but it weakens a new `readiness × discharge-duration` mechanism test.

The revised primary design reconstructs the risk set from telemetry **before** using discharge duration as a predictor.

## Ecological question

> **After an eel has actually reached a barrier, does capture-time migratory readiness modify how strongly passage depends on the strength of the next discharge opportunity?**

The target is post-activation progression, not migration initiation.

## Source

- van Rijn et al. 2026
- DOI: 10.1139/cjfas-2025-0359
- DANS dataset: 10.17026/LS/WTSUNG

Published cohort:

- 40 tagged FIII–FV eels;
- FIII = **11**;
- FIV = **6**;
- FV = **23**;
- 35 passed the pumping station (PS);
- 27 completed seaward passage through the tidal sluice (TS).

## Important release-cohort confounding

The published stage counts by release group are:

| release date | FIII | FIV | FV |
|---|---:|---:|---:|
| 11 Oct 2021 | 9 | 3 | 8 |
| 18 Oct 2021 | 1 | 1 | 7 |
| 26 Oct 2021 | 1 | 2 | 8 |

Thus **9/11 FIII fish (82%)** came from the earliest release, whereas FIV/FV were distributed much more broadly across all three releases.

The source paper also reports that release group 3 had substantially higher migration speeds and coincided with an exceptionally long approximately 2.5-day discharge event.

Therefore release cohort / calendar hydrology is not an optional nuisance term. It is a mandatory confounding check for any readiness × opportunity interaction.

## Frozen readiness definition

~~~text
pre-migrant = FIII
migrant-ready = FIV or FV
~~~

Do not split FIV and FV after outcome inspection.

## Primary risk-set reconstruction

For each eel and barrier:

1. identify the eel's **first direct detection at the barrier receiver/receiver array**;
2. define that timestamp as barrier arrival;
3. include discharge events that begin after barrier arrival and before confirmed downstream passage;
4. classify the discharge event containing confirmed passage as the chosen event;
5. classify earlier included discharge events as missed events.

Thus:

~~~text
arrival at barrier
    -> discharge event 1 : missed
    -> discharge event 2 : missed
    -> ...
    -> discharge event k : passage
~~~

A discharge event is **not** included merely because its duration was long enough for the eel to reach the barrier from an upstream position.

This is the critical v3 change.

## Why this fixes the duration problem

Under the source-defined opportunity rule, discharge duration helps determine whether a discharge event is labelled an opportunity for that eel.

Under the arrival-defined risk set, membership is instead determined from:

- observed barrier arrival;
- event timing;
- whether confirmed passage has already occurred.

Discharge duration is then an exposure rather than part of the inclusion rule.

## Primary exposure

### Discharge-event duration

Primary matched interaction, separately for PS and TS:

~~~text
chosen_event
  ~ log(discharge_duration)
  + migrant_ready × log(discharge_duration)
  | eel
~~~

Interpretation:

- positive duration coefficient: passage is concentrated in longer events;
- negative readiness × duration interaction: FIV/FV are less dependent than FIII on long discharge windows;
- positive interaction: FIV/FV are more selective for long windows.

Do not force a directional conclusion.

## Mandatory release-cohort sensitivity

Because stage and release date are associated, the primary physiological interpretation requires:

~~~text
chosen_event
  ~ log(duration)
  + migrant_ready × log(duration)
  + release_group × log(duration)
  | eel
~~~

or an equivalent calendar/hydrology adjustment.

If readiness × duration becomes non-identifiable or materially changes sign after representing release cohort, report the readiness mechanism as **confounded**, not supported.

## Active-migration window

Very long residence near a barrier can blur active passage attempts with temporary stopping.

Freeze a sensitivity using the source study's published recent-attempt windows:

- PS: retain the most recent **8** post-arrival discharge events, including passage;
- TS: retain the most recent **7** post-arrival discharge events, including passage.

Report the full arrival-to-passage risk set first. The recent-event window is sensitivity only.

## Barrier-specific secondary cues

Only after the primary duration interaction is reported:

### Pumping station
- wind speed during the frozen source window.

### Tidal sluice
- moon illumination.

These variables do not define arrival-risk-set membership.

Because the source publication already identified these event-level associations, they are explanatory secondary analyses rather than untouched confirmatory tests.

## Body-mass confounding

The source study reported that Durif stage and body mass could not be separated adequately at the TS.

A fish-stratified matched model conditions out constant main effects, but it does **not** remove confounding between:

~~~text
readiness × duration
and
body mass × duration
~~~

Freeze the sensitivity:

~~~text
chosen_event
  ~ log(duration)
  + migrant_ready × log(duration)
  + body_mass_z × log(duration)
  | eel
~~~

If these interaction terms are non-identifiable or unstable, report:

~~~text
NON_IDENTIFIABLE_STAGE_VS_MASS_INTERACTION
~~~

Do not drop body mass to rescue a readiness interaction.

## Replication unit

The replication unit is the eel.

Opportunity rows are repeated observations within eel and are not independent animals.

Primary support must therefore use:

- eel-stratified conditional likelihood or an equivalent matched event model;
- fish-level leave-one-out stability.

## Primary support rule

For each barrier report:

- number of eels reaching the barrier;
- number of passing eels with informative post-arrival event sets;
- FIII versus FIV/FV representation;
- number of included discharge events;
- duration interaction coefficient and 95% interval;
- fish-level leave-one-out sign stability;
- release-cohort interaction sensitivity;
- body-mass interaction sensitivity;
- recent-attempt-window sensitivity.

A readiness × duration interaction is supported only if:

1. the 95% interval excludes zero;
2. the sign is stable under fish-level leave-one-out;
3. the direction remains compatible after release-cohort adjustment;
4. the direction remains compatible after body-mass adjustment where identifiable;
5. the conclusion is not created solely by the recent-attempt filter.

## Non-passing individuals

The matched chosen-event analysis requires a passage event and therefore estimates the opportunity-response relationship **among eventual passers**.

Non-passing eels must be reported separately.

A secondary discrete-time survival analysis may include censored non-passers, but it must not replace the matched analysis after seeing the result.

## Cross-barrier interpretation

Do not require the same readiness interaction at both barriers.

Biologically informative outcomes include:

- readiness modifies opportunity dependence at PS but not TS;
- readiness modifies opportunity dependence at TS but not PS;
- neither barrier shows residual readiness modulation despite strong activation effects in the Europe-wide cohort.

The last outcome would support a narrow phase boundary without implying that physiology is irrelevant after departure.

## Failure condition

The external mechanism is weakened if:

- arrival-defined risk sets cannot be reconstructed from the archive;
- stage/release or stage/body-mass interactions are non-identifiable;
- informative FIII choice sets are too few;
- readiness × opportunity interactions are unsupported at both barriers.

That failure does **not** invalidate the Europe-wide activation/onset result.

## Evidence boundary

This is an independent dataset, but the published paper and its outcomes were read before this protocol revision.

Therefore this is **developmental independent evidence**, not outcome-blind confirmation.

The novelty comes from the new arrival-defined, within-eel phase-resolved estimand, not from relabelling the published passage model.

## Superseded v2 design

The earlier protocol used the source-defined opportunity rows directly with discharge duration as the primary exposure.

Retain that design only as provenance/sensitivity. It must not be used as the main mechanism test because duration contributes to source-defined opportunity eligibility.
