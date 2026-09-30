# Exploratory stage × landscape signal

## Status

This note records a **developmental diagnostic**, not confirmatory evidence.

The Europe-wide processed files were inspected while the hypothesis was being refined.

## Question

Does the apparent advantage of more advanced Durif stage depend on landscape resistance?

For a simple exploratory contrast, FIV and FV were combined as "advanced" and compared with FIII **within each project** using the published successful-migrant endpoint.

Approximate Haldane-corrected odds ratios for advanced stage versus FIII:

| project | representative WRS impact | OR advanced vs FIII |
|---|---:|---:|
| 2015_phd_verhelst_eel | 0 | 6.47 |
| 2019_Grotenete | 0 | 46.54 |
| 2011_Warnow | 1 | 2.07 |
| ESGL | 3 | 0.90 |
| 2012_leopoldkanaal | 5 | 5.31 |
| 2013_albertkanaal | ~14 | 0.61 |

These values are highly heterogeneous.

A crude inverse-variance weighted regression of project log(OR) on representative WRS impact across only six project contexts gave an exploratory negative slope of about **-0.129 log-odds per WRS unit**, but with very large uncertainty (p approximately 0.16).

## What this means

The diagnostic is **compatible with** the state-dependent resistance hypothesis:

> advanced migratory readiness may translate into successful movement more strongly in low-resistance systems than in high-resistance systems.

But this is not evidence sufficient for the paper claim because:

1. WRS exposure is largely project-level;
2. only a handful of independent project contexts contribute;
3. tracking geometry and endpoint observability differ among projects;
4. the outcome was inspected before this diagnostic was formalized;
5. FIV is sparse in some high-resistance systems.

## Required next analysis

Do not report the crude cross-project slope as a result.

The next analysis must use the individual-level table and explicitly separate:

- within-project stage contrasts;
- between-project landscape contrasts;
- stage × WRS interaction;
- body size / release timing where available;
- project-level leave-one-out stability.

The hypothesis is considered fragile if removing one project changes the sign of the interaction.

## Why it is still useful

The diagnostic shows that the general ecological question is not empty: **stage effects are not obviously constant across landscape contexts**.

That is exactly the pattern the state-dependent landscape-resistance hypothesis predicts, but it remains to be tested with a model that respects project structure.
