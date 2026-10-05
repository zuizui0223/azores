# Prospective programme: sequential filters on migratory phenotype

## Main question

> **Does the phenotype that predicts entry into migration remain the phenotype that predicts successful route completion?**

## Core design

Track the same animals through ordered gates:

~~~text
pre-movement phenotype
        |
        v
activation
        |
        v
barrier/opportunity 1
        |
        v
barrier/opportunity 2
        |
        v
route completion
~~~

The response is the change in phenotype-performance coupling across gates.

## Pre-outcome phenotype

For European eel:

- primary: Durif stage measured at tagging;
- secondary prespecified: body condition and body size;
- optional physiological marker only if measured before movement.

No stage regrouping after outcomes.

## Gate definitions

Gates must be ecological/physical events rather than receiver-density artifacts, for example:

- departure from residence/release reach;
- pump/weir/lock passage;
- tidal sluice passage;
- lagoon/estuary exit;
- sea escapement.

## Environmental opportunity

Freeze before outcome analysis:

- discharge/flow;
- opening duration;
- water-level difference;
- tide;
- temperature;
- other barrier-operating state.

Opportunity variables describe the environment independently of eel success.

## Main estimands

- beta_activation: readiness effect on activation;
- beta_gate_k: readiness effect on gate-k passage;
- beta_completion: readiness effect on final completion;
- attenuation_k = beta_activation - beta_gate_k;
- readiness × gate × resistance interaction.

## Key predictions

1. readiness strongly predicts activation;
2. readiness-performance coupling is better preserved in permeable routes;
3. coupling attenuates more in resistant/sequentially fragmented routes;
4. gate-specific opportunity explains additional post-activation performance.

## Candidate route classes

### Permeable route

Free-flowing/natural route with little engineered resistance.

Prediction: high completion and small attenuation.

### Moderate route

One or few passable structures.

Prediction: intermediate attenuation.

### Strong/sequential resistance

Multiple or restrictive barriers.

Prediction: activation remains readiness-dependent but later performance is increasingly filtered by passage opportunity.

## Current candidate systems

### Dutch pump -> tidal sluice

- 40 European eels;
- FIII–FV;
- two structurally different consecutive barriers;
- discharge/weather opportunities measured.

Role: developmental within-route test.

Boundary: n is small and stage/body mass are partly confounded.

### Lithuanian free-flowing rivers -> Curonian Lagoon

Published 2026:
- 50 tagged silver eels;
- source-river migration success 72–92%;
- 76% overall riverine success;
- major loss appears later in the Curonian Lagoon.

Role: candidate permeable river / downstream-bottleneck contrast.

Need: verify individual readiness/stage data access before selection-gradient analysis.

### River Test, England

Published 2026:
- 25 tagged silver eels;
- 24 detected migrating downstream;
- 19 reached the tidal area;
- in-river barriers did not measurably delay emigration;
- Durif silvering stage measured.

Role: candidate permeable-route control.

Need: individual data and sufficient stage variation.

## Strong final design

At least:

- one permeable route;
- one fragmented route;
- same readiness definition;
- gate-resolved outcomes;
- route/year replication.

The final endpoint is the change in readiness coefficient, not raw passage rate.

## Conservation implication if supported

Fish-passage mitigation should ask not only:

> what fraction passes?

but also:

> **does passage preserve the natural phenotype distribution of successful migrants?**

A structure could have acceptable total efficiency yet alter which phenotypes reach downstream or spawning habitat.
