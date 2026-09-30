# From the EOG result to the next ecological tests

## 1. Result that needs a biological explanation

The EOG fresh-data experiment used **receiver-week observed detection** for European yellow eel (*Anguilla anguilla*) at 10 receivers.

The conventional arm already contained:

- season/week terms;
- receiver position and active days;
- receiver-network degree at three spatial scales;
- release-anchor abundance, distance and exposure;
- previous-week detection;
- weeks since last detection;
- cumulative previous detections;
- previous-week detected-receiver count;
- neighbouring previous-source counts/exposures;
- cumulative prior global detections.

The frozen EOG support-summary block still improved held-out macro log loss from **0.1422727 to 0.1322871** and won **5/5** held-out blocks.

The ecological object to explain is therefore **not ordinary site fidelity by itself**. Much of simple local detection history was already present in the baseline.

The result says only:

> A system-level, time-updated spatial/history state carried information about future receiver-week detections that was not fully redundant with the measured local history, season, release geometry and receiver geometry.

This is an association. It is not evidence that an EOG world was the true movement process.

## 2. Published boundary

The source study already established that yellow eels in this Azorean stream had a restricted movement range and mostly remained in a given pool. It already discussed strong habitat limitation in the small island stream and possible adaptation to limited food/high competition.

Therefore this repository should **not** use "eels show site fidelity in a small island stream" as its new main result.

The EOG result points to the next question:

> **What generates the residual temporal-spatial memory beyond ordinary pool fidelity?**

## 3. Ecological interpretation ladder

### Interpretation A — individual residence creates latent state memory

Receiver-week aggregation may hide strong individual-specific residence states.

If each eel occupies a preferred pool for long intervals, the whole array has a persistent latent configuration. A receiver-level lag variable is only a coarse proxy for that individual-level configuration.

**Prediction A1:** an individual-level state model should explain a large fraction of the residual temporal dependence.

**Prediction A2:** after individual identity and latent pool state are represented, the extra value of coarse global-history summaries should shrink strongly.

### Interpretation B — hydrological disturbance resets the residence state

The stream can become seasonally dry in places. A disturbance may alter connectivity, water depth, refugia and detectability, causing a sudden reconfiguration of otherwise persistent residence states.

This produces a natural "memory-reset" mechanism:

```text
stable hydrology -> persistent local state
disturbance       -> state transition / temporary loss of predictability
stable hydrology -> new persistent local state
```

**Prediction B1:** inter-pool transitions or abrupt detection-state changes should cluster around hydrological disturbance windows.

**Prediction B2:** temporal dependence should be stronger during stable periods and weaken immediately after disturbance.

**Prediction B3:** adding a frozen hydrological-state variable should reduce the residual history effect.

### Interpretation C — a small mobile subset drives the system-level signal

Most individuals may be resident while a minority is mobile. Aggregated receiver-week predictions can then depend on the current distribution of those few mobile individuals.

**Prediction C1:** movement propensity is strongly heterogeneous among individuals rather than unimodal.

**Prediction C2:** the global spatial-state signal is disproportionately associated with weeks containing movements by the mobile subset.

### Interpretation D — observation memory rather than biological memory

Persistent receiver performance, tag detectability, water conditions or deployment geometry can create temporal correlation in observed detections.

**Prediction D1:** receiver/tag random effects explain the residual dependence without requiring biological state transitions.

**Prediction D2:** apparent state changes align with changes in effort/detection conditions rather than movement events.

This is the essential competing explanation and must be tested before a biological-memory claim.

## 4. Primary next validation target

The first new analysis should be **individual-level state reconstruction with an explicit observation layer**.

For eel (i), week (t), and pool/receiver state (S_{it}):

```text
latent state:
S(i,t+1) ~ transition(S(i,t), hydrology(t), season(t), individual(i))

observation:
Y(i,t,r) ~ detection(S(i,t), receiver(r), effort(r,t), tag(i))
```

The first decision is not whether a complex model fits best. It is:

> **Does the EOG-derived residual history signal survive after individual identity, latent local state and observation heterogeneity are represented?**

### Outcome classes

1. **individual-state explanation supported**  
   Residual history dependence collapses after individual states are represented.

2. **disturbance-reset explanation supported**  
   State-transition hazard rises during hydrological disturbance and memory weakens around those events.

3. **mobile-subset explanation supported**  
   Strong between-individual heterogeneity explains the array-level signal.

4. **observation explanation supported**  
   Receiver/tag/detection effects explain the signal with little evidence for state change.

5. **unresolved**  
   The data do not contain enough transitions or hydrological contrast to distinguish these explanations.

## 5. First executable tests

### T1 — transition inventory

Reconstruct, for every tagged eel:

- first/last detection;
- receivers/pools used;
- number of receiver changes;
- transition dates;
- residence-run lengths;
- gaps in detection;
- tag-specific detection frequency.

**Gate:** if there are too few inter-pool transitions, do not fit a high-dimensional transition model. Treat movement-reset inference as non-estimable and focus on residence/detection decomposition.

### T2 — residence versus observation model

Compare:

- receiver-week aggregate lag model;
- individual + receiver random-effects model;
- individual latent-state / observation model.

Primary target: change in out-of-time predictive loss and residual temporal autocorrelation.

### T3 — disturbance test

Only after an external hydrology/rainfall source is frozen without reference to the movement outcome:

- define disturbance windows;
- test transition/gap hazard around disturbance;
- test whether state-memory strength changes across disturbance versus stable periods.

### T4 — movement-compression extension

Only after the within-Azores mechanism is resolved, compare the estimated local movement scale with independent yellow-eel telemetry systems spanning larger rivers, lakes and estuaries.

That comparative analysis tests the broader hypothesis:

> **realised yellow-stage movement is compressed by available habitat-network geometry.**

The current Azores dataset alone cannot establish that general cross-system relationship.

## 6. Claim rules

- Do not call receiver-week non-detection absence.
- Do not infer a unique movement path from receiver-level support.
- Do not call the EOG improvement a causal effect.
- Do not present restricted movement as a new result if it duplicates the source paper.
- The new contribution must explain **why the temporal-spatial state is persistent or reset**, or establish the comparative movement-compression relationship with independent systems.
