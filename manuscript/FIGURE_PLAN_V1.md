# Final figure plan — Azores phase-control manuscript

## Figure 1 — Biological hypothesis and study design

**Purpose:** establish the question without showing a result twice.

Panel A:
- FIII → FIV → FV internal-readiness axis.

Panel B:
- sequential gates:
  readiness → migration activation → progression → escapement.

Panel C:
- six-project analysis universe as a compact schematic/table, not necessarily a geographic map.

Message:
> the same internal-state predictor is evaluated before and after activation.

## Figure 2 — Gate 1: internal state predicts activation

### Panel A
Stage-specific initiation fractions:
- FIII 154/261;
- FIV 53/68;
- FV 215/246.

### Panel B
Cox Durif HR:
- primary HR 1.28, CI 1.12–1.45;
- show six leave-one-project-out HRs as robustness points.

Avoid plotting raw onset time by stage without project/year context as the primary result.

## Figure 3 — Primary novel result: attenuation across phases

### Panel A
Forest plot of the same ordinal Durif coefficient:
- initiation OR 2.08, cluster-robust CI 1.55–2.77;
- completion OR 1.15, CI 0.81–1.62.

### Panel B
Direct OR-ratio:
- 1.81, CI 1.15–2.84;
- include six leave-one-project-out ratios.

This is the manuscript's primary figure.

### Panel C
Optional/Supplement:
- median post-initiation speed by stage;
- adjusted stage speed ratio 0.983, CI 0.852–1.134.

## Figure 4 — External context aligns with progression

Two aligned panels using the same six projects:

A. median WRS impact vs initiation rate;
B. median WRS impact vs completion conditional on initiation.

Required annotation:
> n = 6 project contexts; WRS is project-confounded; descriptive/bridge evidence only.

Do not draw a causal regression line as if project points were experimental WRS treatments. A rank-order visualization or labelled scatter is preferable.

## Figure 5 — Independent Dutch route constraint

Schematic:
pump → lake → tidal sluice → sea

Annotate:
- tagged 40;
- pump passage 35;
- seaward completion 27;
- mean cumulative barrier delay ~34 d.

List published barrier-specific drivers beside the relevant structure.

This can move to the Supplement if the target journal limits main figures.

## Figure data rule

All numeric plotting inputs come from:

- `manuscript/FIGURE_DATA_CONTRACT_V1.json`

Generate CSVs with:

~~~bash
python analysis/14_build_manuscript_figure_data.py
~~~

Do not type manuscript values directly into plotting code.
