# Dual-gate decomposition of eel migration

## Biological question

The current programme asked whether internal migratory readiness and landscape opportunity jointly determine realised movement.

The Europe-wide panel now suggests a more specific process structure.

> **Internal readiness primarily determines whether migration is initiated; after initiation, completion is much less stage-dependent.**

This motivates a working **dual-gate** model:

1. **readiness gate** — does the eel initiate downstream migration?
2. **route gate** — once migration starts, can it progress through the water body and reach the terminal successful endpoint?

The phrase "dual-gate" is descriptive working terminology, not a novelty claim.

## Matched-cohort decomposition

To make the three stage effects directly comparable, all models were restricted to the same project × release-year strata that contained information for:

- migration initiation;
- overall successful-migrant endpoint;
- successful endpoint conditional on initiation.

Common strata: **9**  
All individuals in those strata: **487**  
Initiators in those strata: **340**

Every model used the same adjustment structure:

~~~text
endpoint
  ~ project × release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage
~~~

Ordinal coding:

~~~text
FIII = 0
FIV  = 1
FV   = 2
~~~

## Result

### Gate 1 — migration initiation

Per Durif stage increment:

- OR = **1.92**
- 95% CI = **1.44–2.56**
- p = **9.8e-6**

### Overall successful endpoint

Per stage increment:

- OR = **1.64**
- 95% CI = **1.27–2.11**
- p = **1.5e-4**

### Gate 2 — successful endpoint among initiators

Per stage increment:

- OR = **1.07**
- 95% CI = **0.75–1.52**
- p = **0.704**

## Ecological interpretation

The stage gradient is strongest before or at the transition into behavioural migration.

Once an eel has crossed the frozen migration-initiation criterion, advanced Durif stage provides little additional information about whether it later reaches the successful-migrant endpoint.

Therefore the cleanest current interpretation is:

> **internal readiness strongly gates movement initiation, whereas post-initiation completion is dominated by other sources of variation.**

The source Europe-wide meta-analysis independently reports that water-regulating structures, tidal context and local hydrology can alter migration timing and speed. This makes external route conditions a biologically plausible explanation for the second gate, but the conditional-stage result alone does not prove that WRS causes post-initiation failure.

## Why this is stronger than the earlier single-endpoint result

The earlier successful-endpoint analysis could be read in two ways:

1. advanced-stage eels start migration more often;
2. advanced-stage eels are better at completing an already initiated migration.

The matched decomposition distinguishes them.

The current evidence supports **(1)** much more strongly than **(2)**.

That is a more specific biological result.

## Candidate mechanism hierarchy

### Internal readiness gate

Measured by:

- capture-time Durif stage;
- migration initiation probability;
- threshold-crossing latency.

Current support:
- robust initiation effect;
- timing effect present on average but system-dependent.

### External route gate

Candidate state variables:

- WRS/barrier configuration;
- discharge/passable flow windows;
- tidal opportunity;
- local route geometry;
- tracking coverage / terminal detectability.

Current support:
- stage effect disappears conditional on initiation;
- source literature supports WRS/hydrological effects on timing and speed.

Still unresolved:
- which external variable explains between-system completion differences.

## Independent confirmation target

The Dutch pump -> lake -> tidal-sluice system is now especially useful because it can test the two gates in one shared route.

Primary questions:

1. Does Durif stage predict whether/when migration is initiated?
2. Among initiators, do passage opportunity and barrier identity explain delay/success?
3. Does Durif stage add little after route opportunity is represented?
4. Is there any true stage × opportunity interaction, or are readiness and route constraints approximately sequential?

## Falsification

The dual-gate interpretation weakens if:

- an independent system shows no internal-state effect on initiation;
- Durif stage strongly predicts post-initiation completion after route conditions are controlled;
- the apparent initiation effect is entirely explained by body size, release timing or tagging design;
- post-initiation outcomes cannot be linked to independently measured route conditions.

## Evidence boundary

This is developmental independent analysis.

It is a process decomposition of already public telemetry outcomes, not a preregistered test and not causal mediation analysis.
