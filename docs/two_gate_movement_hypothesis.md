# Two-gate movement hypothesis — expert-corrected v2

## Result

The Europe-wide eel panel separates two biological phases:

1. **migration initiation** — whether a tracked eel enters the published migratory movement state;
2. **sea escapement after initiation** — whether an initiator reaches the project-specific successful-sea-escapement endpoint.

The source definition now exactly follows the upstream processing code, including nine 2015 individuals that the authors removed from the migratory set by expert judgement.

## Gate 1 — silvering readiness strongly structures departure

Among FIII/FIV/FV individuals represented in the processed migration tables:

- FIII: **154/261 = 59.0%**
- FIV: **53/68 = 77.9%**
- FV: **215/246 = 87.4%**

Project × release-year fixed effects plus within-stratum body length and release timing:

> **OR = 2.08 per FIII -> FIV -> FV increment**  
> 95% CI **1.56–2.76**  
> p ≈ **4.2e-7**

A deliberately harsh sensitivity that counts all 28 stage-coded individuals missing from the migration tables as non-initiators still gives:

> **OR = 1.92**  
> 95% CI **1.47–2.52**

Leave-one-project-out estimates remain positive in all six deletions:

> **OR range 1.67–2.35**, with every 95% CI above 1.

### Timing among initiators

Among observed initiators, advanced stage is also associated with shorter release-to-first-migration delay.

After the same project-year/body-size/release-timing adjustment:

> multiplicative effect on (1 + delay) = **0.73 per stage**  
> 95% CI **0.58–0.91**  
> p ≈ **0.0048**

This timing analysis conditions on initiation and is therefore secondary.

## Gate 2 — stage gradient largely disappears after departure

The upstream code defines successful migration as **successful escapement to the sea**, using project-specific terminal station/distance rules.

Among expert-corrected initiators:

- FIII: **106/154 = 68.8%**
- FIV: **45/53 = 84.9%**
- FV: **116/215 = 54.0%**

With project × release-year fixed effects, body length and release timing:

> **OR = 1.15 per Durif stage**  
> 95% CI **0.83–1.59**  
> p ≈ **0.41**

Thus the strong stage gradient at departure is not retained clearly for sea escapement after departure.

## Ecological interpretation

The supported developmental pattern is:

> **internal migratory readiness strongly structures whether and how quickly movement begins; after movement has begun, the fate of that migration becomes much more context dependent.**

This does not prove that barriers or WRS cause Gate 2. Project-specific receiver geometry, hydrology, route length and barrier configuration remain entangled.

## What is already known

The components are established:

- FIII is premigrant and FIV/FV are migrant silvering stages;
- external cues such as discharge and lunar conditions trigger downstream movement;
- barriers can delay, redirect or prevent sea escapement.

The novelty candidate is therefore not the existence of two influences.

It is the **continental-scale empirical partition of the same individuals' movement process**, showing a strong morphological-stage gradient for initiation but a much weaker one for conditional sea escapement.

## Next confirmation

The Dutch pump -> tidal-sluice dataset should test Gate 2 within one shared route:

> once eels are ready and moving, do barrier-specific passage opportunities explain progression better than residual Durif-stage differences?

## Claim boundary

These results are developmental rather than preregistered confirmation. Do not claim a universal two-gate law until the phase-specific pattern is reproduced independently.
