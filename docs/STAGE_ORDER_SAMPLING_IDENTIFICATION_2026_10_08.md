# Stage-specific initiation: three different statements, not one

**Status (2026-10-08):** observational label bounds completed; resampling sensitivity computed and committed; CI reproduction gate may still be queued. Evidence is developmental and observational.

Sources:
- `results/stage_entry_observability_bounds_v1.json`
- `results/stage_order_dual_uncertainty_v1.json`
- `analysis/52_stage_order_dual_uncertainty.py`
- `analysis/contracts/stage_order_dual_uncertainty_v1.json`

## 1. What source telemetry classified in these 575 fish

| Durif class | Source-classified starts | Evaluated fish | Observed rate |
|---|---:|---:|---:|
| FIII | 154 | 261 | 59.0% |
| FIV | 53 | 68 | 77.9% |
| FV | 215 | 246 | 87.4% |

A source non-initiation is **not** an independently observed decision to remain in place. The 153 original negatives comprise 100 short-followup and 53 day-90-observable individuals. Receiver activity on other fish is evidence of an observation process, not continuous coverage or focal fish inactivity.

## 2. Finite-sample identification conditional on one error class

If all 422 classified initiators and all 53 day-90-supported negative labels are retained as correct, and only the 100 short-followup negatives can hypothetically represent missed initiation, the **exact sharp finite-sample bounds** are:

- FIII initiation 59.0–85.8%;
- FIV initiation 77.9–97.1%;
- FV initiation 87.4–94.3%;
- FV minus FIII **+1.57 to +35.31 percentage points**.

This is an arithmetic identification interval for **the current tracked individuals under stated admissible label changes**, not a probability interval for a wild eel population.

Only **2/6 projects** have a strictly positive FV–FIII lower bound. **1/6** has a strictly negative upper bound (Albertkanaal: 26/26 FIII initiated versus 105/117 FV); **3/6** are unresolved. The equal-project mean sharp bounds are **−6.84 to +38.67 points**. If even five of the 37 longer-observed FIII negatives are hypothesized as unseen starts, the pooled strict ordering can disappear. None of these hypothetical changes was observed.

## 3. Additional sampling/context uncertainty

The positive **+1.57-point lower endpoint** is itself estimated from a finite, heterogeneous collection of tagged eels. Two *distinct exploratory resampling diagnostics* were therefore computed, holding the hypothetical label-set rule fixed.

| Process resampled | Exploratory 95% percentile variation of the **lower-bound endpoint** | Fraction of simulated endpoints above zero |
|---|---:|---:|
| Fish within each project × stage, keeping sample sizes fixed | −3.91 to +6.87 points | 71.8% |
| All six projects as independent context clusters, with replacement | −16.65 to +17.96 points | 53.3% |

The first assumes exchangeable independent fish and the second has only six clusters. Neither is a valid sampling confidence interval for *true* biological initiation or a causal effect; these specifically describe the **stability of the finite-sample logical bound** under two assumed sampling mechanisms.

The project-balanced lower endpoint is already negative for the observed project set (−6.84 points), further demonstrating that pooled fish weighting and between-river generality are different targets.

## 4. What ecological mechanism remains unknown

**Supported:** silvering-stage labels strongly track observed classification of downstream migration in the pooled data; the pooled stage gradient is robust to a restricted hypothetical short-followup label class in the *observed sample*. The result varies greatly across waterway contexts.

**Not identified:** a universal biological FIII→FV departure threshold; an energy-reserve gate; a river-discharge or tidal-cue interaction; the fraction that reached the sea; or actual receiver uptime/tag loss/detection probability.

A falsifiable next ecological test needs jointly measured physiological state and environmental opportunities with fish-specific detector uptime or downstream independent witnesses. Its critical outcome is *true exposure-corrected onset*, not simply a better classifier of the existing telemetry label.

## 5. Operational conservation consequence

Separate at least four quantities:
1. potential migrants classified by silvering morphology;
2. detection-supported initiation into downstream migration;
3. passage, delay and mortality at route barriers;
4. actual escapement.

An apparent cohort enrichment in FV does not itself quantify any later endpoint. For future monitoring, prioritize timed deployment metadata, full receiver-array geometry, individual tag retention and independent downstream detections before estimating the latent initiation-to-escapement transition.

The public six-project analysis is a decision about **identifiable evidence and monitoring gaps**, not a validated conservation intervention.
