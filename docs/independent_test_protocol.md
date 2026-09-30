# Independent test protocol: state-dependent landscape resistance

## Scientific target

The independent Europe-wide eel panel is used to test a biological interaction, not to repeat the published migration-speed analysis.

> **Does independently measured migratory readiness change how landscape resistance is translated into realised movement?**

The key ecological claim is that a barrier or hydrological corridor has no single biological effect. Its realised effect depends on the animal's internal movement state.

## Independent state variable

Use capture-time life_stage from the public eel metadata.

Exact Durif-coded individuals currently present in the public processed metadata:

- FII: 17
- FIII: 303
- FIV: 98
- FV: 336
- MII: 12

Total exact Durif-coded: **766**.

There are also 396 animals recorded only as silver and 1,522 with NA stage.

### Primary cohort

Use female stages with enough replication and cross-project overlap:

~~~text
FIII -> FIV -> FV
~~~

These stages occur across multiple independent projects and multiple WRS classes.

FII is retained as an ecological boundary case but is not the primary contrast because n=17 and 16/17 individuals come from one project/WRS context.

MII is analysed separately because n=12 and sex/stage are confounded.

The coarse silver group is not mixed into the ordinal Durif analysis.

## Outcomes

State is defined independently of movement. Movement outcomes can therefore be evaluated without circularity.

### O1 — migration initiation

For each tagged individual, determine whether/when the published movement classifier first identifies directed downstream migration.

Primary response:
- time from release to first classified migration event;
- censor individuals with no detected migration onset.

### O2 — migration progression after initiation

Among initiators:
- downstream progression rate;
- migration speed;
- distance progressed before long interruption;
- successful arrival/escapement where the published endpoint is available.

### O3 — barrier sensitivity

Use response-independent landscape descriptors already published with the dataset:
- barrier_number;
- wrs_impact_score;
- water_body_class;
- station-level habitat type.

The target is the interaction:

~~~text
Durif stage × landscape resistance
~~~

not the marginal WRS effect already analysed in the source paper.

## Model ladder

### A0 — project/design baseline

~~~text
outcome ~ project + release date + body size + sex where estimable
~~~

### A1 — internal state

~~~text
outcome ~ A0 + Durif stage
~~~

Question: does independently measured readiness predict later movement expression?

### A2 — landscape resistance

~~~text
outcome ~ A1 + WRS / water-body context
~~~

### A3 — state-dependent resistance

~~~text
outcome ~ A2 + Durif stage × WRS
~~~

This is the main ecological test.

## Interpretation

- **A1 only:** movement is state dependent, but state-dependent landscape resistance is not established.
- **A3 supported:** the same landscape resistance has different realised effects depending on internal migratory readiness.
- **no robust A1/A3:** mobility-gating programme is not supported by this panel.

## Existing outcome access

The public processed files have already been inspected during development. Aggregate successful-migrant counts by stage were seen before this protocol was frozen. Therefore this Europe-wide analysis is **not outcome-blind/preregistered**.

It is a developmental independent test. Confirmation must use another system or a held-out project not used for specification.

## Anti-circularity rules

1. Never use the movement-derived migration flag as the predictor of movement.
2. Capture-time Durif stage is the primary internal-state predictor.
3. Do not redefine stages after seeing movement outcomes.
4. Do not tune WRS categories to maximise a stage interaction.
5. Do not pool FII into FIII or MII into female stages to improve significance.
6. Project-level leave-one-project-out stability is mandatory because stage composition differs among projects.

## Strong ecological conclusion if supported

> **Landscape resistance is state dependent: internal migratory readiness determines not only whether an animal moves, but how strongly barriers and hydrological opportunity constrain that movement.**
