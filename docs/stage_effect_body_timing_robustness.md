# Robustness: Durif stage survives body-size and release-timing control

## Model

The public Europe-wide eel panel was restricted to primary female stages FIII/FIV/FV.

To reduce confounding by multi-year projects and seasonal tagging, the model used **project × release year fixed effects**.

Within those strata, it additionally controlled:

- body length, centered within stratum and scaled per 100 mm;
- release timing, centered within stratum and scaled per 100 days.

Primary ordinal coding:

```text
FIII = 0
FIV  = 1
FV   = 2
```

Thirteen project-year strata contained both outcome variation and at least two Durif stages, contributing 598 individuals.

## Result

### Durif stage

Per one-stage increment:

- OR = **1.74**
- 95% CI = **1.37–2.22**
- p = **7.2e-6**

### Body length

Per 100 mm within project-year:

- OR = **1.15**
- 95% CI = **0.89–1.50**
- p = **0.277**

### Release timing

Per 100 days later within project-year:

- OR = **1.73**
- 95% CI = **1.01–2.97**
- p = **0.047**

## Interpretation

The stage signal is attenuated from the simpler project-fixed estimate but remains strong.

Therefore:

> **the Durif-stage association with later successful migration is not explained only by body size or broad release timing.**

Release timing itself carries information, which is biologically sensible and should remain in later movement-onset/progression models.

## What this still does not prove

This result establishes a robust **internal-state association**.

It does not identify the mechanism linking silvering state to movement, and it does not establish the stronger state × landscape-resistance interaction.

Project/system heterogeneity remains substantial and is part of the biological problem rather than a nuisance to average away.

## Evidence boundary

The successful-migrant endpoint had already been inspected during hypothesis development.

This remains developmental independent evidence, not preregistered confirmation.
