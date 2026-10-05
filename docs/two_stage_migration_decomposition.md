# Two-stage movement decomposition: readiness versus completion

## Why this matters

The Europe-wide eel panel suggests that "migration success" is not one biological process.

It can be decomposed into at least two sequential components:

1. **entry into a migratory movement mode**;
2. **successful progression/completion after that mode is expressed**.

Capture-time Durif stage is independently measured before the telemetry outcome, so it can be used to ask where along this sequence internal state carries information.

## Stage 1 — entry into migratory mode

Outcome:

> whether the later telemetry trajectory satisfies the published migration classification.

Adjusted for project × release year, within-stratum body length and release timing:

- OR per FIII -> FIV -> FV increment = **1.99**
- 95% CI = **1.49–2.66**
- p = **3.2e-6**

Interpretation:

> **advanced internal migratory readiness strongly predicts whether a later trajectory expresses migratory movement.**

## Stage 2 — completion conditional on a migratory trajectory

Restrict to individuals whose trajectory was classified as migratory.

Outcome:

> published successful-migrant endpoint.

Adjusted with the same project-year/body-size/release-timing structure:

- OR per Durif stage = **1.29**
- 95% CI = **0.94–1.77**
- p = **0.12**

Thus, once an eel is already in the migratory-trajectory set, there is no robust evidence in this panel for a large additional stage advantage in final completion.

## Raw conditional rates

Among migratory trajectories:

| Stage | Successful / migratory | Completion rate |
|---|---:|---:|
| FIII | 106 / 161 | 0.658 |
| FIV | 45 / 54 | 0.833 |
| FV | 116 / 216 | 0.537 |

The non-monotonic FV rate is another reason not to treat silvering stage as a universal determinant of completion.

## Strong project heterogeneity after migration entry

Completion among migratory trajectories varies dramatically among systems:

| Project | Representative resistance context | Completion rate |
|---|---|---:|
| 2019 Grotenete | WRS 0 / class A | **1.00** |
| 2015 phd_verhelst_eel | WRS 0 / class A | **0.80** |
| 2011 Warnow | WRS 1 / class B | **0.81** |
| ESGL | WRS 3 / class B | **0.83** |
| 2012 Leopoldkanaal | mostly WRS 5 / class E | **0.69** |
| 2013 Albertkanaal | mostly WRS 14 / class D | **0.19** |

These project values are descriptive. Tracking design, geography, hydrology, route length and barrier configuration are confounded with project.

Within Albertkanaal, the small lower-WRS cells are sparse and non-monotonic, so the dataset does **not** identify a clean within-project WRS dose response.

## Ecological hypothesis generated from the decomposition

The most useful biological hypothesis is no longer merely "advanced silvering means more movement."

It is:

> **Internal state governs readiness to enter a migratory mode; once movement is initiated, successful realization becomes increasingly contingent on external opportunity and landscape resistance.**

This predicts a transition in the dominant control of movement:

~~~text
before migration expression:
    internal state / readiness dominates

after migration expression:
    external passage opportunity, barriers and hydrology become more important
~~~

## Why this is more general than eel stage

The same two-stage logic can apply to:

- amphibian breeding migrations;
- salmonid smolt migration;
- ungulate seasonal migration;
- insect dispersal morphs;
- bird migratory restlessness versus realized departure;
- seed dispersal where release and establishment are distinct stages.

The general question is:

> **When does movement limitation shift from organismal motivation/capacity to landscape opportunity?**

## Causal boundary

This analysis is not a causal mediation analysis.

Conditioning on a migratory trajectory is conditioning on a post-state outcome and can induce selection.

Therefore the supported statement is predictive/sequential:

> the Durif signal is strong for migratory-trajectory membership, while evidence for an additional Durif signal among migratory individuals is weak.

Do not claim that landscape resistance causally mediates the stage effect from these data.

## Novelty boundary

The source meta-analysis already analysed water-body context, barriers, migration speed and arrival timing, but the public analysis code does not use life_stage as a main predictor in the principal models inspected here.

Nevertheless, this Europe-wide panel remains a **hypothesis-generating developmental analysis**, not the final publication endpoint.

A paper-level claim requires an independent system where:

- internal movement state is measured before movement;
- transition into movement can be distinguished from completion;
- external passage opportunity varies independently enough to test the predicted control shift.
