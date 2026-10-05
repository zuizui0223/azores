# Novelty boundary — Azores / eel programme

## Already established

This project does **not** claim novelty for:

- internal state and external environment jointly shaping movement;
- physiology contributing to the decision to move and later movement;
- European eel silvering and FIII/FIV/FV biology;
- discharge, darkness, lunar phase or other cues affecting downstream migration;
- barriers lowering passage or increasing delay;
- phenotype-dependent fishway passage;
- barriers acting as selective filters;
- cumulative effects of multiple barriers;
- decomposing migration into sequential stages.

Mechanistic migration frameworks already distinguish an early decision-to-move phase from later realized movement. Fish-passage work already shows that barriers can filter morphology, timing and behavior and can create contemporary selection.

Therefore neither "two-stage migration" nor "selective barrier passage" is a sufficient novelty claim.

## Developmental result motivating a narrower question

The current canonical Europe-wide result is phase dependent.

### Activation

- Durif OR per FIII -> FIV -> FV increment: **2.08**
- cluster 95% CI: **1.55–2.77**

### Completion conditional on activation

- Durif OR per stage: **1.15**
- cluster 95% CI: **0.81–1.62**
- p ≈ **0.41**

### Direct phase difference

- activation/completion OR-ratio: **1.81**
- 95% CI: **1.15–2.84**
- p = **0.0099**
- leave-one-project-out direction: **6/6** OR-ratios > 1.

The phenotype-performance association therefore weakens after migration activation.

At project level, median WRS is almost unrelated to activation but strongly negatively aligned with completion after activation. That alignment is contextual only because route, hydrology, telemetry geometry and system identity are confounded.

## Refined novelty candidate

> **Do fragmented migration routes decouple an organism's pre-movement migratory phenotype from realized migration performance?**

The focal object is the **change in the same trait-performance relationship across sequential movement gates**.

Let beta_g be the effect of response-independent migratory readiness at gate g:

~~~text
beta_activation
beta_barrier_1
beta_barrier_2
beta_completion
~~~

Define the gate-to-gate change:

~~~text
Delta_beta(g1,g2) = beta_g1 - beta_g2
~~~

The target is not the name "selection-gradient turnover". The target is an empirical, replicated change in beta.

## Fragmentation-decoupling prediction

### Permeable route

~~~text
beta_activation ~= beta_completion
~~~

More-ready animals should be able to translate readiness into route completion.

### Resistant route

~~~text
beta_activation > beta_completion
~~~

After movement activation, hydrological opportunity and barrier performance increasingly determine fate.

The stronger comparative prediction is:

~~~text
phase attenuation
  increases with
route resistance
~~~

## Evolutionary meaning if supported

Anthropogenic fragmentation would not simply lower migration success.

It could alter the mapping:

~~~text
natural migratory phenotype
        ->
successful downstream / spawning contribution
~~~

A barrier can therefore impose a filter that differs from the natural filter governing migration activation.

Possible consequences include:

- attenuation of naturally adaptive readiness-performance coupling;
- enrichment of different morphological or behavioral traits downstream of barriers;
- sequential change in phenotype composition along a route;
- altered contemporary selection on migratory phenotypes.

These are future-test hypotheses, not conclusions from the current continental panel.

## Required independent evidence

A decisive study requires the same individuals to be observed across ordered gates with traits measured before movement outcome.

Required:

1. pre-movement readiness phenotype;
2. explicit activation/departure state;
3. independently characterized barrier/opportunity states;
4. final route completion;
5. enough readiness variation at each gate.

Preferred:

- permeable and fragmented routes;
- multiple barrier types;
- multiple route-years;
- hydrology measured independently of animal passage outcome.

## Primary future model

Long-form individual × gate data:

~~~text
passed_gate
  ~ readiness
  * gate
  * route_resistance
  + body_size
  + season
  + route/year effects
~~~

Primary evidence:

1. readiness × gate interaction;
2. readiness × gate × resistance interaction;
3. gate-specific readiness coefficients.

## Falsification

The refined hypothesis fails if:

- readiness effects remain constant across gates;
- route resistance does not predict attenuation;
- permeable and fragmented routes show the same gate-specific trait slopes;
- phase differences vanish after body size, timing and observability controls;
- gate-specific slopes do not replicate across route-years.

## Evidence boundary

The Europe-wide open panel is developmental and outcome-opened. It motivates this independent study but cannot confirm fragmentation-induced phenotype-performance decoupling.
