# Two-stage migration decomposition

## Developmental independent result

The Europe-wide eel panel was re-analysed as a **sequential biological process** rather than as a single migration-success endpoint.

Primary female Durif stages:

~~~text
FIII = premigrant
FIV  = migrant
FV   = advanced migrant
~~~

The analysis used six projects with public per-project migration files and excluded `life4fish` because no corresponding public migration file is present in the processed migration directory.

## Stage 1 — migration initiation

Migration onset was defined exactly from the published classifier as the **first row with `downstream_migration == TRUE`**.

The classifier requires:
- >4 km downstream progression available for the speed calculation;
- migration speed >=0.01 m/s;
- the published stationary-range smoothing rule.

Project × release-year fixed effects were used, with within-stratum adjustment for:
- body length;
- release timing.

Primary ordinal result:

- n = **525**
- 11 informative project-year strata
- OR per FIII -> FIV -> FV increment = **1.99**
- 95% CI = **1.49–2.66**
- p = **3.2e-6**

Raw initiation rates in the model cohort:

- FIII: **60.8%**
- FIV: **79.1%**
- FV: **85.7%**

Among initiators, one Durif-stage increment was associated with a shorter onset latency:

- multiplicative effect on `latency + 1 day`: **0.71**
- 95% CI **0.56–0.90**
- p = **0.004**

### Leave-one-project-out stability

Removing each project in turn:

- stage OR for initiation ranged **1.67–2.26**;
- every 95% interval remained above 1.

The initiation signal is therefore not carried by one project.

## Stage 2 — successful escapement after initiation

The source repository defines `successful_migrants_final_detection.csv` as **successful escapement to the sea**, using water-body-specific final-station/distance rules.

Among individuals that had already initiated migration:

- n = **394**
- 11 informative project-year strata
- OR per Durif-stage increment = **1.29**
- 95% CI = **0.94–1.77**
- p = **0.12**

Leave-one-project-out:

- OR range **1.07–1.37**;
- every 95% interval overlapped 1.

Thus the strong stage effect seen before departure is substantially attenuated after migration has begun.

## Ecological interpretation

The current pattern is compatible with a **two-filter migration process**:

### Filter 1 — physiological departure gate

> internal silvering/readiness strongly controls whether and how rapidly downstream migration begins.

### Filter 2 — landscape completion filter

> once migration has begun, advanced silvering stage alone does not reliably determine successful escapement to sea.

Completion then depends more strongly on the landscape and hydrological route traversed after departure.

This interpretation is stronger than the earlier generic "state × landscape resistance" framing because it identifies **where in the movement sequence internal state appears to act**.

## WRS exploratory diagnostic

With project-year fixed effects, within-stratum WRS variation is sparse.

Among initiators:

- WRS impact OR for successful escapement ≈ **0.61 per unit**
- 95% CI ≈ **0.36–1.05**
- p ≈ **0.074**

This direction is compatible with stronger resistance reducing completion, but the estimate is dominated by the few strata with within-project WRS variation and is not confirmatory.

WRS should not be interpreted causally from this panel.

## Literature boundary

Durif FIII/FIV/FV stages are already defined biologically as premigrant/migrant states, and prior studies have reported that many FIII individuals fail to migrate while some FIV/FV individuals also remain stationary.

The new target is therefore **not** "silver eels migrate."

The Europe-wide source meta-analysis used movement to identify migratory tracks and then focused on arrival timing, migration speed, latitude and WRS. It did not make this cross-project decomposition of:

~~~text
physiological state -> initiation
versus
physiological state -> escapement | initiation
~~~

## Evidence boundary

This is developmental independent evidence, not preregistered confirmation.

The successful-escapement endpoint and aggregate stage patterns were inspected while the hypothesis was being refined.

A stronger causal/general claim requires an external system where:
- internal stage is measured independently;
- departure can be separated from passage/completion;
- landscape opportunity is measured at the transition where completion is decided.
