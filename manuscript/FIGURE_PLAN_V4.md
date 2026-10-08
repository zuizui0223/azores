# Figure plan V4 — multivariate entry-state manuscript

Canonical manuscript:
- `manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md`

Canonical numeric contract:
- `manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json`

## Figure 1 — Migratory commitment and progression are different prediction targets

**Purpose:** introduce the biological sequence and avoid treating “migration
performance” as one phenotype.

Panel A — capture state:
- ordinal Durif stage FIII → FIV → FV;
- continuous weight-for-length condition.

Panel B — sequential responses:
- migration activation;
- threshold-defined behavioral onset;
- whole-route speed after activation;
- positive inter-station transit speed after activation.

Panel C — analysis universe:
- 575 evaluable stage-coded tracks;
- 525 animals in informative multivariate activation strata;
- 570 animals / 418 events in the onset analysis;
- 418 animals in whole-route speed;
- 411 animals in frozen segment-speed analysis.

Message:

> capture phenotype is measured before movement and its information is tested
> for transfer across successive phases rather than assumed to be universal.

Do not depict terminal non-detection as failure.

## Figure 2 — Migration entry is multivariate

Panel A — raw activation fraction by Durif stage:
- FIII: 154/261 = 59.0%;
- FIV: 53/68 = 77.9%;
- FV: 215/246 = 87.4%.

Panel B — multivariate activation effects:
- Durif: OR **2.130/stage**, 95% CI **1.596–2.842**;
- condition: OR **1.460/SD**, 95% CI **1.164–1.832**.

Panel C — activation-trained score definition:
- stage coefficient **0.756**;
- condition coefficient **0.379**;
- joint LR χ²(2) **39.01**, p **3.39×10⁻9**.

Message:

> the ordinal silvering label does not exhaust capture-state information; stage
> and continuous body state contribute additively to the entry gate.

Boundary:
- condition is a biometric weight-for-length proxy, not an independent
  physiological reserve measurement.

## Figure 3 — Entry-state information transfers to onset, not realized transit speed

Plot the multiplicative effect per 1 SD activation-trained score on a log ratio
axis centered at 1. The four rows use different response links and must be
labelled explicitly; the plot is a **transferability display**, not a claim that
OR, HR and speed ratios are identical effect-size scales.

Rows:
- activation OR **2.230**, 95% CI **1.704–2.918**;
- onset HR **1.317**, 95% CI **1.168–1.485**;
- whole-route speed ratio **0.946**, 95% CI **0.832–1.076**;
- frozen positive inter-station speed ratio **1.028**, 95% CI **0.869–1.215**.

Annotate:
- whole-route speed partial R² **0.18%**;
- segment-speed partial R² **0.026%**.

### Panel A — cross-phase transferability

Plot the four canonical score effects listed above.

### Panel B — exact-link realized transit-speed test

Show the frozen exact-link estimate:
- **17,792** positive segment rows;
- **418** eels;
- **244** directed station pairs;
- project-held-out score ratio **0.962/SD**;
- 95% CI **0.883–1.048**;
- p **0.372**;
- weighted partial R² **0.0382%**.

Add three small sensitivity points:
- <=2.5 m s⁻¹: **0.942**;
- <=5 m s⁻¹: **0.944**;
- <=10 m s⁻¹: **0.941**.

Annotate that the external-plausibility screens are post-hoc and that they
remove **53.0–63.1%** of candidate raw segment rows because the source
last-to-first speed field contains grossly implausible values.

Message:

> a capture-state vector trained on migratory commitment still ranks when
> migration starts, but provides essentially no ranking of realized transit
> speed even within identical route links.


The current numerical results exclude the nine fixed expert-classified 2015 non-migrants. Corrected pair-support ratios are **0.956** (>=3 fish) and **0.999** (>=10 fish); leave-one-project-out ratios range **0.933–1.013**. The 2.5/5/10 m s⁻¹ screens are post-hoc and yield weak negative point estimates (p≈0.07–0.08), not an established speed effect.

## Figure 4 — Independent arrival-defined barrier test does not support a simple selectivity mechanism

Panel A — risk-set construction:
```
barrier arrival (SewerArrival)
      ↓
opening starts after arrival (Firstquarter)
      ↓
missed openings … chosen passage event
      ↓
confirmed PassageTime
```

Primary row inclusion:
```
SewerArrival <= Firstquarter <= PassageTime
```

Event duration and the source duration-dependent `valid` flag are not used for
primary inclusion.

Panel B — post-arrival condition versus missed opening events:
- EZ n=35: r **0.009**, permutation p **0.960**;
- CL n=27: r **−0.104**, permutation p **0.592**.

Use fish-level points from
`results/dutch_arrival_waiting_diagnostic_v1.json`.

Panel C — post-arrival condition versus barrier delay:
- EZ: r **0.072**, p **0.677**;
- CL: r **−0.182**, p **0.350**.

Panel D — matched duration-choice test:
- CL condition × duration β **−0.095**, p **0.841**,
  permutation p **0.849**;
- EZ model is near-separated/non-converged and should be marked
  **unstable / not interpretable**, not plotted as a reliable huge negative
  effect.

Message:

> the phase boundary is not rescued by a universal high-condition
> “wait for a stronger passage window” mechanism.

## Supplementary Figure S1 — Stage-only benchmark

Show the original Durif-only phase boundary:
- activation OR **2.08**, CI **1.56–2.77**;
- onset HR **1.29**, CI **1.13–1.47**;
- whole-route speed ratio **0.983**, CI **0.852–1.134**;
- frozen segment speed ratio **1.001**, CI **0.831–1.204**.

## Supplementary Figure S2 — Progression falsification audits

Include:
- whole-route project heterogeneity Q **2.47**, p **0.781**;
- segment project heterogeneity Q **2.32**, p **0.804**;
- capture-stage staleness interaction ratio **1.036**, p **0.382**;
- stage-speed selection diagnostic **1.042 → 1.062** after IPW;
- condition-speed selection diagnostic **0.907 → 0.920** after IPW.

Message:
> project cancellation, simple stage ageing and measured activation selection do
> not restore a transferable positive generic speed gradient.

## Supplementary Figure S3 — Terminal positive-set sensitivity

- terminal positive-set OR/stage **1.15**, CI **0.83–1.59**;
- stacked activation/terminal OR ratio **1.81**, CI **1.15–2.84**.

Required annotation:

> terminal non-membership is not a validated biological failure state; no
> escapement probability is estimated.

## Supplementary Figure S4 — Entry participation versus timing among initiators

**All analyses in this figure are exploratory and conducted after inspection of the first multivariate entry-score results.**

Panel A — **Frozen project-held-out prediction across observed time horizons**:
- exactly **475** day-90-eligible eels in every comparison;
- the same event-training coefficients are used in all five endpoints;
- report added condition stratified AUC by 7/30/60/90-day onset and eventual initiation:
  **+0.0077 / +0.0329 / +0.0460 / +0.0549 / +0.0807**;
- label each endpoint event count **239 / 299 / 331 / 351 / 422**;
- avoid a linear/physiological-time interpretation of the event labels; pair sets change as the event definition changes.

Panel B — **Three observed migration-onset categories**:
- ≤30-day onset: **299** eels;
- >30-day onset: **123** eels;
- no source-classified initiation: **53** eels.
- conditional AUC increments, same fixed scores: early versus never **+0.0832**, late versus never **+0.0756**, early versus late **+0.0089**.
- the 53 are not verified true nonmigrants or failed escapements.

Panel C — **Direct onset-order ranking among detected entrants**:
- 422 initiated eels, **10,756** within-project-year onset-order pairs;
- baseline concordance **0.5446**, condition-expanded **0.5461**, gain **+0.0015**;
- project-resampling CI for gain **−0.0237–+0.0202** and exact project sign-flip **p=0.9375**;
- onset after day 1 only: 291 eels, gain **−0.0086**.

Panel D — **Selection and inferential boundaries**:
- 100 of 575 eels lack day-90 eligibility;
- unequal event/control followup and latent non-detection limit any survival inference;
- eventual-vs-day30 added AUC contrast: four matched projects, mean **+0.0431**, project-bootstrap CI **+0.0164–+0.0697**, exact sign-flip **p=0.125**.
- explicitly distinguish from separately re-trained 7/30/60/90-day models, which changed training population and had different effect directions.

Data sources: `results/paired_temporal_endpoint_condition_v1.json`,
`results/fixed_followup_condition_increment_v1.json`,
`results/entrant_onset_latency_discrimination_v1.json`.

## Figure boundary

Do not:
- compare OR and HR numerically as if they share the same effect-size scale;
- call the entry-state score a physiological latent variable;
- plot the unstable EZ matched-choice coefficient as reliable evidence;
- present Dutch results as confirmation of an internal-to-external handoff;
- hide the source segment-speed data-quality problem or present post-hoc speed screens as preregistered;
- use terminal non-membership as failure.
