# European eel silvering-stage ordering under imperfect telemetry observation

**Evidence class:** mathematical scenario-conditioned bounds using source-verified stage counts and receiver-followup groups; developmental, not biological migration-rate estimation.

**Independent rerun:** [stage-entry-observability-bounds workflow](../.github/workflows/stage-entry-observability-bounds.yml). Source files:
- `results/stage_specific_condition_gate_v1.json`;
- `results/receiver_witness_observability_v1.json`;
- `analysis/contracts/stage_entry_observability_bounds_v1.json`;
- `analysis/50_stage_entry_observability_bounds.py`.

## The specific uncertainty set

575 eels: 422 source-classified initiators and 153 source negatives.
- **100** negatives lack the 90-day receiver-followup criterion and are *allowed* to be reclassified as hypothetical unobserved initiators.
- The other **53** negatives are *fixed* under the first scenario because their last observed arrival passes 90 days. This **does not prove biological nonmovement or continuous observation**.
- All 422 positives are fixed, respecting the original telemetry classification.

Within each stage, the exact interval under these assumptions is

\[
p_s \in \left[\frac{I_s}{N_s},\ \frac{I_s+A_s}{N_s}\right],
\]

where `I` is source-classified initiation, `N` the tracked fish, and `A` the subset of short-followup source negatives.

| Stage | Tracked | Classified initiators | Hypothetically ambiguous negatives | Conditional initiation-rate interval |
|---|---:|---:|---:|---|
| FIII | 261 | 154 | 70 | **59.0–85.8%** |
| FIV | 68 | 53 | 13 | **77.9–97.1%** |
| FV | 246 | 215 | 17 | **87.4–94.3%** |

**An informative asymmetry:** even the upper FIII rate (224/261 = 85.82%) is below the lower FV rate (215/246 = 87.40%). Hence the pooled **FV−FIII difference is between +1.57 and +35.31 percentage points** under this *specific* limited uncertainty set. It does not require assuming that all short negatives truly started: the upper/lower assignments only describe logically permissible possibilities.

But neither the FIV-vs-FIII nor FV-vs-FIV ordering is strictly protected by this uncertainty set. These are deterministic identification regions, not sampling confidence intervals.

## Sharpness does not imply universality across waterways

Project-specific FV−FIII bounds from exactly the same assumptions:

| Project | Lower bound | Upper bound | Sign constrained? |
|---|---:|---:|---|
| 2011 Warnow | −16.7 pp | +29.1 pp | No |
| 2012 Leopoldkanaal | +25.7 pp | +42.6 pp | **FV greater** |
| 2013 Albertkanaal | −10.3 pp | −8.5 pp | **FV lower** |
| 2015 Verhelst | +18.5 pp | +46.5 pp | **FV greater** |
| 2019 Grotenete | 0 pp | +45.5 pp | Strict difference not established |
| ESGL | −58.3 pp | +76.9 pp | No |

Two of six projects have a positive strict sign, one has a **negative strict sign**, and three are unresolved. Albertkanaal is not evidence of a causal reversal: all **26 sampled FIII** in that project were classified initiators, while FV contains source negatives; composition, selection and tracking opportunity are not controlled by these simple proportions.

Equal-project averaging instead of pooling individual eels produces an FV−FIII identification interval of **−6.84 to +38.67 pp**, including zero. Weighting projects by the *minimum* of the FIII and FV sample sizes gives approximately **−0.33 to +34.62 pp**, also including zero. The robust **pooled** ordering is therefore not a transportable universal river effect. These weights were chosen only to illustrate aggregation; they do not estimate a superpopulation effect.

## How fragile is the conditional lower bound?

The 70 short-followup FIII negatives are all hypothetically promoted to initiation in the worst case. That creates 224 FIII starts / 261 fish (85.82%), narrowly below 215 / 246 (87.40%) for the *original* FV observed initiation rate.

There are also **37 FIII source negatives with later/longer receiver observations**. If only **five of those 37** were hypothetical hidden starts too, then FIII would have 229/261 = 87.74%, exceeding the original FV rate.

This is an **exact arithmetic fragility threshold under an enlarged uncertainty set**, not a finding that any of those five fish did initiate or that the later receivers missed them. Receiver contacts are discrete sightings rather than a denominator of valid nonmigration observation time.

## Ecological interpretation

The strongest supported claim is asymmetrical:

- The silvering-stage FIII versus FV *pooled source-label* contrast survives the specifically defined 100 ambiguous short-followup negatives.
- The more subtle body-condition incremental ranking (+0.0336 AUC) is much more sensitive to which ambiguous fish are relabelled: an independently validated adversarial construction erased it with **11** hypothetical changes; the distribution of true hidden initiations is unknown.
- Neither result identifies a mechanistic energetic threshold or the transition from a physiological decision into external control.
- A small, bounded within-sample stage contrast can coexist with real or observationally induced project variation; the all-project positive sign does not generalize to every river.

For conservation, this argues for distinguishing **production of silver-morphology eels**, **actual initiation**, **observability**, **barrier passage**, and **escapement**. It does not convert a telemetry-derived initiation fraction into escapement probability.

## What would actually resolve the mechanism?

Receiver deployment/recovery timestamps and fish-specific detection opportunity, independently timed downstream passage events, river flow/tide and animal energy measurements are needed. The pinned sources do not provide a uniform record of those for all six projects. No quantitative physiological threshold or receiver failure rate is identified here.
