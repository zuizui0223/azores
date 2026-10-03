# Developmental result: Durif stage predicts migration initiation and timing

## Why this analysis matters

The earlier Azores programme used the published **successful-migrant endpoint**.

That endpoint mixes at least two biological processes:

1. whether an eel expresses downstream migration at all;
2. whether that movement ultimately succeeds through the monitored landscape.

The public upstream repository also provides the movement classifier itself, allowing the first process to be isolated.

## Classifier semantics

The source algorithm does not simply label an animal migratory from release.

A downstream migration starts at the first telemetry row satisfying the frozen source rules:

- a future detection at least 4 km farther downstream;
- implied speed at least 0.01 m/s;
- an additional 1005-m smoothing criterion to avoid starting in a stationary phase.

The `migration` state then runs from that first downstream-migration row to the maximum-distance row.

Thus the first `migration=TRUE` row is a defensible algorithmic movement-onset marker.

## Coverage

Six projects contain both exact FIII/FIV/FV metadata and public migration trajectories.

Tracked stage-tagged individuals:

- FIII: **261**
- FIV: **68**
- FV: **246**
- total: **575**

Tracking coverage relative to stage-tagged metadata is approximately 95% or higher for each stage.

## Descriptive initiation pattern

Among tracked individuals:

- FIII: **161/261 = 61.7%** initiated classified migration;
- FIV: **54/68 = 79.4%**;
- FV: **216/246 = 87.8%**.

This is descriptive only because projects, years and release timing differ.

## Adjusted migration-initiation model

Model:

```text
initiation
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
```

Eleven informative project-year strata and 525 individuals contributed.

### Durif stage

Per FIII -> FIV -> FV increment:

- OR = **1.99**
- 95% CI = **1.49–2.66**
- p ≈ **3.2e-6**

### Body length

Per 100 mm:

- OR = **1.37**
- 95% CI = **1.00–1.89**
- p ≈ **0.053**

### Release timing

Per 100 days later within project-year:

- OR = **1.30**
- 95% CI = **0.68–2.50**
- p ≈ **0.43**

The stage effect therefore persists after the two obvious individual/timing confounders.

## Delay to detected migration among initiators

Among 382 initiators in informative strata, the response was:

```text
log(1 + days from release to first migration=True row)
```

Per one-stage Durif increment:

- multiplicative factor on `1 + onset days` = **0.72**
- 95% CI = **0.57–0.91**
- p ≈ **0.0065**

Thus more advanced Durif stage is associated not only with a higher probability of expressing migration, but—conditional on detected initiation—with **shorter delay to movement**.

Release timing also mattered strongly for delay:

- 100 days later -> factor **0.39**
- 95% CI **0.21–0.72**
- p ≈ **0.0026**

Later-season fish began detected migration sooner after release.

## Ecological interpretation

This is a stronger result than the successful-migrant endpoint alone.

It supports:

> **internal migratory readiness gates the expression of downstream movement itself.**

The two components are now separable:

```text
internal state
   -> probability / timing of movement initiation
   -> landscape/barrier interaction
   -> eventual migration success
```

The first arrow has developmental support.

The second arrow remains the central unresolved landscape-gating question.

## Important limitations

1. The classifier is algorithmic, not a physiological measurement of migration.
2. Delay analysis conditions on initiators and is not a full censored survival model.
3. Outcome data were inspected during hypothesis development.
4. Project heterogeneity remains strong.
5. These results do not establish a causal effect of Durif stage.
6. They do not establish stage × landscape resistance.

## Next decisive analysis

Use the independent Dutch consecutive-barrier system to test whether the **translation from readiness into realised passage** depends on barrier type and hydrological opportunity.
