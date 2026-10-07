# Condition-dependent phase reversal hypothesis — 2026-10-07

## Working ecological question

> **Can the same high body-state phenotype that facilitates entry into migration become more selective once a risky or restrictive passage decision is encountered?**

This is a cross-dataset hypothesis, not yet a demonstrated within-individual sign reversal.

## 1. Developmental Europe-wide evidence: body state promotes migration entry

Across the six-project public European-eel cohort, capture weight-for-length state retains predictive information after adjustment for ordinal Durif stage, body length, release timing and project-year context.

### Migration activation

Primary stage-adjusted allometric condition metric:

- n = **525**
- OR per 1 SD condition = **1.460**
- 95% CI **1.164–1.832**
- p = **0.00105**

### Migration onset

- n = **570**
- onset events = **418**
- HR per 1 SD condition = **1.149**
- 95% CI **1.029–1.284**
- p = **0.0139**

The condition effect remains positive in every leave-one-project-out fit for both endpoints.

### Metric robustness

The positive pattern is not tied to one condition formula.

Across three definitions:

1. stage-adjusted allometric residual;
2. project-adjusted allometric residual without stage in residualization;
3. Fulton log K;

the full-cohort effects are:

- activation OR range: **1.438–1.460** per SD;
- onset HR range: **1.148–1.153** per SD.

All three definitions retain positive direction in all leave-one-project-out fits for both activation and onset.

Status:

> **ROBUST_TO_CONDITION_METRIC_DEFINITION**

This supports a narrow empirical statement:

> **continuous capture body-state information predicts whether and when classified downstream migration activates beyond the ordinal Durif label.**

It does not establish an independent energetic axis because body weight and length also contribute to Durif silvering classification.

## 2. Independent barrier evidence points in the opposite performance direction

### Nieuwe Statenzijl tidal sluice — Huisman et al. 2023

Among 26 eels that reached and passed the sluice:

- higher body weight predicted more missed sluicing events;
- higher Fulton condition predicted more missed sluicing events;
- standardized published IRR for weight = **2.99**, p < **0.001**;
- standardized published IRR for condition = **1.87**, p = **0.043**.

The authors explicitly discussed two candidate explanations:

- phenotype-dependent stimulus thresholds;
- the asset-protection principle, under which individuals with greater current assets can be more risk-averse.

The published condition IRR interval and Wald p are not numerically concordant, so this project uses the direction and the source authors' interpretation as contextual evidence rather than as a meta-analytic coefficient.

### Consecutive Dutch pump -> tidal sluice — van Rijn et al. 2026

Among 35 pumping-station passers:

- better-conditioned eels accumulated more missed passage opportunities before passage;
- published condition IRR = **1.66**, p = **0.016**;
- faster canal migrants accumulated fewer missed opportunities.

The source authors again interpret better-condition delay as compatible with stronger required flow stimuli or greater risk aversion / asset protection.

As above, the published condition IRR interval and Wald p are not numerically concordant, so no pooled effect size is calculated.

### Rozema pumping station accelerometry — van der Knaap et al. 2025

In an independent 40-eel pumping-station study:

- individual K-factor significantly predicted routine acceleration;
- better-conditioned eels had lower mean acceleration;
- p = **0.001**.

This is not a passage-delay endpoint, but it is a mechanistic boundary consistent with body condition altering movement intensity around engineered passage systems.

## 3. Candidate synthesis

The current evidence is compatible with a phase-dependent change in the behavioral value of body state:

~~~text
before directed migration
    better body state
        -> higher probability of activation
        -> earlier activation
                    |
                    v
after arrival at a risky/restrictive barrier
    better body state
        -> can afford to wait
        -> stronger opportunity threshold / greater selectivity
        -> more missed opportunities before passage
~~~

The key idea is **not** that good condition universally increases or decreases movement.

It is:

> **body state may change which decision is optimal across the movement sequence.**

At entry, adequate state can make migration feasible.

At an anthropogenic passage bottleneck, a high-asset individual may have more to lose and may wait for a stronger or safer passage opportunity.

This is consistent with the general asset-protection principle, which predicts greater caution as current reproductive assets increase.

## 4. Why this is more specific than a generic state-dependent movement claim

Movement ecology already expects internal state and external context to interact.

The sharper hypothesis here is a **sign change in phenotype-performance coupling across sequential ecological decisions**:

- positive coupling with migration entry;
- negative coupling with rapid barrier passage.

That predicts that the same phenotype can be favoured by one transition and filtered against by the next.

If true, migration corridors do not merely reduce total passage.

They can change the **phenotypic composition and timing** of successful migrants.

## 5. Conservation implication

A barrier can be numerically efficient yet still impose phenotype-dependent delay.

Under the working hypothesis, high-condition eels — potentially individuals carrying larger reproductive assets — may be disproportionately delayed while waiting for acceptable hydraulic opportunities.

Management should therefore evaluate not only:

> what fraction of eels pass?

but also:

> **which phenotypes pass promptly, and under what operating windows?**

The relevant mitigation target becomes preservation of both:

- total passage;
- phenotype-neutral passage timing.

## 6. Decisive test in the 2026 Dutch archive

The current source-defined passage-opportunity table cannot be used as the primary duration test because event duration contributes to the source eligibility rule.

The frozen primary extension therefore uses **arrival-defined risk sets**:

1. first direct detection at the barrier = arrival;
2. include discharge events after arrival and before confirmed downstream passage;
3. classify the passage event as chosen;
4. classify prior post-arrival events as missed.

Primary models should test, separately by barrier:

~~~text
chosen_event
  ~ log(discharge_duration)
  + body_condition × log(discharge_duration)
  + readiness × log(discharge_duration)
  + release_group × log(discharge_duration)
  | eel
~~~

with body mass / stage identifiability checks retained.

### Prediction under the phase-reversal / asset-protection hypothesis

Among eels already at a barrier:

> **better-conditioned individuals should show stronger dependence on high-quality passage windows.**

The exact sign depends on how opportunity quality is coded.

For discharge duration as a positive opportunity-strength axis, this predicts a positive condition × duration interaction if high-condition fish preferentially use longer windows.

For stronger flow or other barrier-specific positive opportunity axes, the same logic predicts steeper positive opportunity-response slopes at high condition.

## 7. Strong falsifiers

The hypothesis is weakened if:

- the Europe-wide body-state effect disappears under independent physiology or repeated-stage measurement;
- arrival-defined Dutch risk sets show no condition-dependent opportunity response despite adequate information;
- high-condition eels pass equally or more readily under weak opportunities;
- the apparent barrier pattern vanishes after release cohort, size and stage are represented;
- similar negative condition effects occur in unobstructed/permeable reaches, implying a general locomotor effect rather than barrier selectivity.

## 8. Important evidence boundaries

This is **not yet a demonstrated within-individual sign reversal**.

The positive pre-migration and negative barrier associations come from different datasets and use related but not identical condition metrics.

Durif stage already incorporates body morphometrics, so the Europe-wide condition term is not independent physiology.

The Dutch barrier studies are observational with respect to individual condition.

The 2023 and 2026 papers also contain reported condition-effect confidence intervals that are not numerically concordant with their Wald p-values; therefore the present synthesis uses their published direction, not a formal pooled magnitude.

## 9. External experimental boundary

Leandersson et al. 2026 showed in large-scale flume trials that individual behavioral phenotype influenced downstream passage more strongly than rack design: more active eels passed sooner/more readily, and passage structures could therefore impose phenotype-dependent filtering.

Its public Figshare dataset is a useful next external test of **phenotype-dependent barrier filtering**, although the published focal phenotype is open-field activity rather than body condition.

## Current status

**CANDIDATE_CONDITION_PHASE_REVERSAL_HYPOTHESIS**

Supported now:
- robust positive condition signal for activation and onset in the Europe-wide cohort;
- two independent Dutch barrier studies with better-condition -> more missed opportunities;
- one independent pumping-station study with better-condition -> lower routine acceleration;
- general theory predicts condition-dependent risk aversion when reproductive assets are high.

Not yet supported:
- a formal condition × migration-phase interaction in the same individuals;
- a causal asset-protection mechanism;
- generality beyond engineered barriers.

Canonical evidence ledger:
- `results/condition_phase_sign_audit_v1.json`

Primary next test:
- `analysis/13_dutch_arrival_riskset_gate.py`


## 10. Same-cohort progression update — locomotion versus elapsed time

A new same-cohort diagnostic sharpens the candidate mechanism.

### Whole-route speed

Among the canonical **418** activated eels, the capture-condition coefficient on whole-route speed is negative under all three frozen condition definitions:

- stage-adjusted allometric residual: speed ratio **0.925** per SD, 95% CI **0.820–1.044**, p = **0.205**;
- project-adjusted allometric residual: **0.898**, 95% CI **0.797–1.012**, p = **0.078**;
- Fulton log K: **0.896**, 95% CI **0.792–1.013**, p = **0.078**.

All six leave-one-project-out estimates are below one under all three definitions.

The intervals nevertheless include one, so this is a **consistent negative point-estimate pattern**, not a supported negative whole-route-speed effect.

### Frozen positive inter-station speed

The result does **not** reproduce for the previously frozen per-eel median positive inter-station speed endpoint.

Across the same three condition definitions:

- adjusted condition ratios are approximately **1.049–1.050** per SD;
- all 95% intervals include one;
- leave-one-project-out directions are not uniformly negative.

Thus better-conditioned eels are not detectably slower while making positive inter-station movements.

### Algebraic decomposition of whole-route speed

Because:

```
whole-route speed = distance range / elapsed migration time
```

the whole-route association was decomposed using the exact same 418-eel cohort and covariate model.

Across the three condition definitions:

- route-distance ratio per SD condition: **1.019–1.025**;
- elapsed-time ratio per SD condition: **1.108–1.138**;
- whole-route speed ratio per SD condition: **0.896–0.925**.

The elapsed-time point estimate is above one in every leave-one-project-out fit under every condition definition.

The distance effect is small and unsupported.

Therefore the negative whole-route-speed pattern is algebraically carried mainly by **longer elapsed migration time**, not by shorter route distance or slower positive inter-station transit.

### Revised ecological interpretation

The strongest current working model is no longer:

> high body state reduces movement performance after activation.

It is:

> **high body state facilitates entry into migration, but after entry it is associated with more elapsed time that is not explained by slower positive transit speed.**

This pattern is compatible with additional waiting, delay, staging, or selective use of movement opportunities.

It does **not** identify which of those processes generated the elapsed time.

This distinction makes the independent Dutch barrier results more relevant: those studies directly observe more missed passage opportunities in better-conditioned eels, offering an external candidate mechanism for a same-cohort elapsed-time pattern that is not visible in positive transit speed.

### Current status after this update

**CANDIDATE_ACTIVATION_TO_DELAY_BODY_STATE_TURNOVER**

What is now supported developmentally:

- better capture body state predicts higher activation probability;
- better capture body state predicts earlier onset;
- the positive effect is robust to three condition definitions;
- positive inter-station transit speed does not show a negative condition gradient;
- whole-route speed has a consistent negative point estimate;
- that whole-route pattern is carried primarily by longer elapsed time.

What remains unproven:

- that the extra elapsed time is specifically barrier waiting;
- a causal within-individual sign reversal;
- an asset-protection mechanism;
- generality beyond the available telemetry systems.

Canonical new results:
- `results/body_condition_post_activation_speed_v1.json`
- `results/body_condition_segment_progression_v1.json`
- `results/body_condition_whole_route_decomposition_v1.json`
