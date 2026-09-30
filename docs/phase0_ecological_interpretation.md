# Phase 0 ecological interpretation

## Bottom line

The original EOG result should **not** be described as evidence for yellow-eel
movement or propagation.

The correct ecological translation is:

> **EOG detected predictive memory in a system with no valid observed
> between-receiver movement. Part of the EOG heldout period is contaminated by
> a documented receiver-operability failure, but an independent pre-failure
> screen still shows that weekly detection states are more similar among
> co-resident eels sharing a receiver than among eels at different receivers.**

The next biological target is therefore the source of **local state memory**,
not movement between pools.

## 1. What EOG contributed

For the receiver-week endpoint, adding the frozen EOG world-support summary to
an already history-rich conventional predictor changed heldout macro log loss
from 0.1422727 to 0.1322871 and improved all 5 heldout blocks.

That result is retained only as the anomaly that generated the question.

It does not identify the source of the memory.

## 2. Why the EOG effect size cannot be interpreted directly as eel ecology

The source paper documents that station 4 / `151 FLO CRUZ` ceased producing
detections after 2022-07-24 because sediment burial prevented data retrieval.

The post-EOG operability audit found that the deployment metadata nevertheless
continued to classify that station as active under the EOG effort rule.

Consequently:

- all 49 scored weeks were deployment-eligible at station 151;
- **9 EOG heldout weeks** were fully after the documented receiver failure;
- affected weeks began 2022-07-25 and continued through 2022-09-19;
- none of the calibration weeks were affected.

Therefore late receiver-week zeroes at this station are potentially observation
failures. The frozen EOG result remains historically valid as the result of its
predeclared contract, but its ~7% predictive improvement is **not a clean
biological effect size**.

This is not a reason to repair EOG retrospectively. It is a reason to change
what the ecological follow-up asks.

## 3. What survives the receiver-failure problem

A separate sensitivity restricted the cleaned residency data to timestamps no
later than 2022-07-24.

Within that clean window:

- 26 retained yellow eels were detected;
- no retained eel used more than one study receiver;
- same-receiver eel pairs had mean weekly detection correlation **0.1227**;
- different-receiver pairs had mean correlation **-0.0206**;
- same-minus-different difference = **0.1433**;
- receiver-label permutation screen: **p = 0.0118**.

Thus the local clustering of detection memory predates the known late receiver
failure. The failure cannot by itself create this locality pattern.

## 4. What this means biologically

The combined evidence rules out one tempting explanation:

> the predictive memory is not evidence of observed receiver-to-receiver
> propagation.

It leaves two primary explanations that are still confounded.

### H-A1 — local biological state

Eels sharing a pool respond to a common local state such as refuge use, local
activity, food, depth, flow or another pool-level condition.

### H-A2 — local observation state

Eels sharing a receiver covary because receiver performance, acoustic
propagation or other observation conditions affect all tags at that receiver.

The pre-failure locality result says there is **locality**. It does not yet say
whether that locality belongs to the animals or the receiver.

## 5. Next validation target

The next analysis must discriminate H-A1 from H-A2.

Primary target:

> **Does a receiver/pool-level temporal effect remain after explicitly modelling
> individual tag history and receiver-operability state, and can an independent
> environmental covariate explain that shared local effect?**

Useful discriminating evidence, in order:

1. receiver replacements / operability changes at a fixed pool;
2. independently measured local hydrology or water state;
3. sub-weekly co-activity timing among co-resident eels;
4. independent telemetry in another stream.

A purely receiver-specific discontinuity supports H-A2. A shared local effect
that persists across hardware changes and tracks environmental state supports
H-A1.

## 6. Stop rule

Do not fit a more elaborate movement model to this Azores dataset.

The source study already established restricted movement, and the retained
cohort has zero valid between-receiver movement. Complexity cannot manufacture
movement information that the observations do not contain.

The Azores role in the broader programme is therefore:

> **an anchor system demonstrating predictive/local memory without observed
> propagation, with a known observation-process perturbation that makes the
> biological-versus-observation distinction directly testable.**
