# Project-fixed Durif-stage result

## Developmental independent result

Using the public Europe-wide eel processed data, capture-time Durif stage was tested against the published successful-migrant endpoint with project fixed effects.

Only projects containing both successes and failures contribute to the fixed-effect logistic model.

Primary female stages:

~~~text
FIII = 0
FIV  = 1
FV   = 2
~~~

### Ordinal effect

Project-fixed logistic regression:

- beta per one-stage increment: **0.635**
- SE: **0.119**
- odds ratio per stage increment: **1.89**
- 95% CI: **1.49–2.38**
- Wald p: **1.1e-7**

Thus, moving one Durif category from FIII -> FIV -> FV was associated with approximately **89% higher odds** of the later successful-migrant endpoint after controlling for project.

### Categorical contrasts

Relative to FIII:

- FIV: OR **2.69**, 95% CI **1.51–4.80**, p = **0.00083**
- FV: OR **3.35**, 95% CI **2.09–5.37**, p = **4.7e-7**

This supports a graded internal-readiness signal rather than only an arbitrary FIII versus advanced-stage split.

## Strong project heterogeneity

Advanced (FIV/FV) versus FIII odds ratios by informative project:

| project | OR advanced vs FIII |
|---|---:|
| 2011 Warnow | 2.07 |
| 2012 Leopoldkanaal | 4.53 |
| 2013 Albertkanaal | 0.58 |
| 2015 phd_verhelst_eel | 6.47 |
| 2019 Grotenete | 46.54 |
| ESGL | 0.90 |

Approximate heterogeneity:

- Q = **21.55**
- df = **5**
- p ≈ **0.0007**

Therefore the correct ecological reading is two-part:

1. **internal state effect is strong on average after project control;**
2. **the strength and even direction of that advantage varies strongly among landscapes/systems.**

The second point is not noise to hide. It is the biological reason to test state-dependent landscape resistance.

## Claim boundary

This result does **not** show that WRS causes the heterogeneity.

Landscape resistance, tracking design, hydrology and project identity are strongly entangled.

The next question is therefore not:

> is advanced Durif stage always better?

It is:

> **which landscape or hydrological contexts permit advanced migratory readiness to be translated into successful movement, and which contexts suppress it?**

That interaction requires an independent system with better within-system contrast.

## Evidence class

Developmental independent evidence only.

The published endpoint was inspected during hypothesis refinement, so this is not preregistered/outcome-blind confirmation.
