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

## Figure 3 — Entry-state information transfers to onset, not generic speed

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

Message:

> a capture-state vector trained on migratory commitment still ranks when
> migration starts, but provides essentially no general ranking of post-
> activation progression speed.

## Figure 4 — Independent arrival-defined barrier test falsifies a simple selectivity mechanism

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

## Figure boundary

Do not:
- compare OR and HR numerically as if they share the same effect-size scale;
- call the entry-state score a physiological latent variable;
- plot the unstable EZ matched-choice coefficient as reliable evidence;
- present Dutch results as confirmation of an internal-to-external handoff;
- use terminal non-membership as failure.
