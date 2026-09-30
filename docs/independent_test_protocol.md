# Independent test protocol: state-dependent landscape resistance

## Scientific target

The Europe-wide eel panel is used to develop and stress-test a biological interaction, not to repeat the published migration-speed analysis.

> **Does independently measured migratory readiness change how landscape resistance is translated into realised movement?**

The key ecological claim is that a barrier or hydrological corridor has no single biological effect. Its realised effect may depend on the animal's internal movement state.

## Independent state variable

Use capture-time life_stage from the public eel metadata.

Exact Durif-coded individuals:

- FII: 17
- FIII: 303
- FIV: 98
- FV: 336
- MII: 12

Total exact Durif-coded: **766**.

Primary female cohort:

~~~text
FIII -> FIV -> FV
~~~

FII is a sparse resident boundary case; MII is a sparse male boundary case. Neither is pooled into the primary cohort.

## Identifiability boundary discovered in preflight

The panel is strong for testing **stage effects within projects**, but weaker for a universal stage × landscape interaction.

Why:

- FIII/FIV/FV occur across seven projects;
- all exact-stage animals have WRS records;
- but WRS impact is largely a project/system property;
- only a small subset of projects contain meaningful within-project WRS variation.

Therefore:

### GO — internal-state effect

Estimate whether capture-time Durif stage predicts later migration initiation/progression within project.

### GO, developmental — state × resistance

Estimate the interaction with project-aware models and leave-one-project-out diagnostics.

### HOLD — general confirmation of state-dependent resistance

Do not treat this panel alone as confirmation of a general state × landscape law. A second dataset/system with stronger within-system resistance contrast is required.

## Outcomes

State is defined independently of movement.

### O1 — migration initiation

Time from release to first later event meeting the frozen published migration criterion, with non-initiators censored.

### O2 — progression after initiation

Among initiators:
- downstream progression;
- migration speed;
- interruption/delay;
- successful escapement where estimable.

### O3 — landscape resistance

Use response-independent:
- barrier_number;
- wrs_impact_score;
- water_body_class;
- station habitat type.

## Model ladder

### A0 — project/design baseline

~~~text
outcome ~ project + release timing + body size + design covariates
~~~

### A1 — internal state

~~~text
outcome ~ A0 + Durif stage
~~~

### A2 — landscape resistance

~~~text
outcome ~ A1 + WRS
~~~

### A3 — state-dependent resistance

~~~text
outcome ~ A2 + Durif stage × WRS
~~~

A3 is exploratory/developmental in this panel because WRS is substantially system-confounded.

## Interpretation

- **A1 robust:** internal readiness predicts later movement expression.
- **A3 stable across project deletion:** state-dependent resistance becomes a strong candidate general mechanism.
- **A3 unstable to one project:** interaction remains system-specific/underidentified.
- **no A1:** mobility-gating interpretation is weakened.

## Existing outcome access

Aggregate successful-migrant counts were inspected before this protocol was frozen. This is not outcome-blind/preregistered evidence.

## Anti-circularity and no-rescue rules

1. Movement-derived migration flags are outcomes, never the internal-state predictor.
2. Capture-time Durif stage is fixed before modelling.
3. Do not regroup FII/FIII/FIV/FV/MII after seeing model results.
4. Do not tune WRS categories to maximise interaction.
5. Report leave-one-project-out sign and magnitude changes.
6. Distinguish within-project stage information from between-project resistance information.

## Confirmation requirement

A general statement that landscape resistance is state dependent requires at least one additional independent system where internal state and landscape opportunity vary with less confounding than in the Europe-wide panel.
