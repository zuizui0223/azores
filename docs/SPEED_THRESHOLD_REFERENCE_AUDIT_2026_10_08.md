# Speed-screen reference evidence audit — 2026-10-08

## Trigger

The frozen post-hoc speed-quality sensitivity in `analysis/contracts/within_link_speed_quality_sensitivity_v1.json` described **2.26 m/s** as a published upper swimming speed for European eel and placed the 2.5 m/s screen just above it.

This was subsequently checked against accessible primary sources.

## Confirmed

Tudorache et al. (2015), `https://doi.org/10.3389/fphys.2015.00256`, Table 1, measured seven migratory European female silver eels with:
- mean critical sustained speed, Ucrit = **0.94 ± 0.02 m/s**;
- mean optimal speed, Uopt = **0.64 ± 0.03 m/s**.

These are lab performance measurements under specific conditions. The study warns that Ucrit cannot simply be extrapolated to freely swimming fish in nature.

The government report exists:
- Katopodis & Gervais (2016), *Fish swimming performance database and analyses*, Canadian Science Advisory Secretariat Research Document 2016/002.

## Not established

A **2.26 m/s universal or species-level maximum** for European eel was not independently verified from an accessible primary source/table.

Even if a record-level maximum were substantiated, it would not form a hard upper bound on telemetry-derived *ground speed*, which differs from swimming speed relative to water and can be distorted by short detection intervals, route distances and hydraulic advection.

## Fixed sensitivity retained

The speed screens remain **2.5, 5 and 10 m/s** because they were registered before their results were inspected. They are explicitly *heuristic gross-artifact screens*, not biologically measured censoring thresholds.

Corrected expert-eligible results:
- unfiltered source-speed ratio **0.9616** (95% CI 0.8825–1.0478);
- <=2.5 m/s ratio **0.9421** (0.8822–1.0061);
- <=5 m/s ratio **0.9437** (0.8842–1.0071);
- <=10 m/s ratio **0.9411** (0.8810–1.0054).

All intervals span 1; none establishes a negative gradient, although the filtered estimates are weakly negative.

## Manuscript wording rule

The manuscript must not claim a verified 2.26 m/s species maximum. Explain the speed screens as post-hoc heuristic sensitivity to evidently impossible source speeds (e.g. recorded >3,700 m/s), not as estimates of intrinsic eel locomotor limits.

This audit corrects interpretation without altering the historical contract, the thresholds, or the analysis output.
