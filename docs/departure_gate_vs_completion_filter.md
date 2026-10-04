# Departure gate versus completion filter

## Main result

The public Europe-wide eel migration tables were read for all six projects that contain the primary Durif stages FIII/FIV/FV.

The large Leopoldkanaal, Albertkanaal and 2015 telemetry tables were retrieved through their pinned Git blobs rather than the GitHub Contents endpoint.

Upstream repository:
- `PieterjanVerhelst/eel-meta-analysis`
- pinned commit: `59578cb622dddbbba5174b4c51bff0807787385a`

## Stage flow

| Capture-time stage | tracked n | initiated migration | initiation rate | successful endpoint | completion among initiators |
|---|---:|---:|---:|---:|---:|
| FIII | 261 | 161 | **61.7%** | 106 | **65.8%** |
| FIV | 68 | 54 | **79.4%** | 45 | **83.3%** |
| FV | 246 | 216 | **87.8%** | 116 | **53.7%** |

Raw initiation probability rises strongly with advanced silvering state.

Completion after initiation does not show the same simple monotonic pattern.

## Adjusted initiation model

Model:

~~~text
migration initiated
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

Eleven informative project-year strata contributed 525 individuals.

Durif stage:

- OR per FIII -> FIV -> FV increment: **1.99**
- 95% CI: **1.49–2.66**
- p ≈ **3.2e-6**

Leave-one-project-out stage ORs remain above 1:

- minimum ≈ **1.67**
- maximum ≈ **2.26**

The initiation result is therefore not driven by one project.

## Adjusted completion model conditional on initiation

The same model was fitted only to individuals that initiated migration.

Eleven informative project-year strata contributed 394 initiators.

Durif stage:

- OR per stage increment: **1.29**
- 95% CI: **0.94–1.77**
- p = **0.12**

This does not support a strong monotonic stage effect on successful completion once migration has begun.

## Ecological interpretation

The data support a more specific mechanism than the broad phrase “mobility gating”:

> **Internal migratory state primarily opens the departure gate. After departure, realised fate becomes much more dependent on the external movement landscape.**

Conceptually:

~~~text
growth / pre-migrant state
        |
        | silvering readiness
        v
  DEPARTURE GATE
        |
        | movement begins
        v
  LANDSCAPE FILTER
  barriers / flow / route
  tracking opportunity
        |
        v
  successful progression
~~~

This makes the Dutch consecutive-barrier test much more targeted.

The external confirmation question is no longer merely:

> does Durif stage predict passage?

It is:

> **after the departure gate has opened, which barrier and hydrological conditions determine whether latent migratory motivation can be converted into successful progression?**

## Important nuance

This is not proof that landscape resistance causes the weaker completion-stage association.

The post-initiation filter may contain:

- barrier configuration;
- hydrological opportunity;
- route structure;
- tracking geometry;
- unmeasured physiological state;
- project-specific handling or release context.

The result tells us **where in the movement sequence internal state is most strongly expressed**, not yet which external factor controls the remaining fate.

## Paper consequence

Azores now has a clearer biological spine:

1. a highly mobile species can remain locally resident during growth;
2. advancing migratory readiness strongly increases the probability that movement begins;
3. the same readiness is not enough to guarantee successful completion;
4. therefore migration is naturally decomposed into **internal departure gating** and **external progression filtering**.

The next paper-level confirmation should directly manipulate or observe the second stage inside one shared landscape, rather than continuing to compare broad project averages.
