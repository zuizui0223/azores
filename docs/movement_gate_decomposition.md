# Movement-gate decomposition: initiation versus completion

## Ecological question

The Europe-wide eel result can now be decomposed into two distinct stages:

1. **movement initiation** — does the eel begin directed migration?
2. **movement completion** — once migration has begun, does it reach the published successful-migrant endpoint?

This distinction matters biologically because an internal migratory state could act primarily on the **decision/motivation to move**, while subsequent success could depend more strongly on landscape opportunity, barriers and hydrology.

## 1. Durif stage predicts initiation

Across the six primary-stage projects with public migration tables, after respecting the source study's expert exclusions:

- FIII: 154/254 initiated migration = **60.6%**
- FIV: 53/67 = **79.1%**
- FV: 215/245 = **87.8%**

Fixed-window initiation models controlled:

- project × release year;
- body length within project-year;
- release timing within project-year.

Durif stage effect per FIII -> FIV -> FV increment:

| Window after release | OR | 95% CI | p |
|---|---:|---:|---:|
| 7 d | **1.51** | 1.16–1.97 | 0.0025 |
| 30 d | **1.50** | 1.14–1.99 | 0.0043 |
| 60 d | **1.70** | 1.28–2.24 | 0.00021 |
| 90 d | **1.89** | 1.39–2.57 | 0.000050 |

The direction is stable from the first week through three months.

## 2. After initiation, the stage association largely disappears

Among eels that had initiated migration, success at the published final-migrant endpoint was modelled with:

- project × release-year fixed effects;
- body length;
- release timing;
- ordinal Durif stage.

Result:

- OR per Durif-stage increment = **1.15**
- 95% CI = **0.83–1.59**
- p = **0.41**

The corresponding project-only version was similarly weak:

- OR = **1.19**
- 95% CI = **0.87–1.62**
- p = **0.28**

## Biological interpretation

The cleanest current interpretation is:

> **Migratory readiness is associated primarily with release of movement, not with a uniform increase in post-initiation success across landscapes.**

In other words:

~~~text
internal state
    ↓
opens / closes movement gate
    ↓
migration begins
    ↓
landscape + barriers + hydrology
    ↓
progression / completion
~~~

This is more specific than saying "silver eels move more."

It suggests two ecological controls at different stages of the process:

- **internal-state control** over whether/when movement is expressed;
- **external landscape control** over what happens after that movement is expressed.

## Why this matters for the Azores programme

The Flores yellow-eel anchor represents the closed-gate end:

> high movement capacity, but no observed receiver-to-receiver movement during the growth phase.

The Europe-wide panel shows that more advanced Durif state is associated with opening that movement gate.

The unresolved question is then exactly the independent confirmation target:

> **once the gate is open, which landscape opportunities or barriers determine whether movement can be completed?**

That is why the Dutch consecutive-barrier system is valuable.

## Important causal boundary

The conditional-on-initiation analysis is **not a formal mediation analysis**.

Initiation is itself affected by stage and potentially by landscape context, so conditioning on initiation can introduce selection/collider bias.

Therefore do not claim:

> stage has no causal effect after initiation.

The supported descriptive statement is narrower:

> **the strong marginal stage association seen for eventual success is substantially attenuated among the subset that has already initiated migration.**

This pattern is consistent with a movement-gating interpretation and motivates direct barrier/opportunity tests.

## Evidence class

Developmental independent evidence.

The outcome had already been opened during hypothesis refinement, and the fixed-window series is exploratory sensitivity rather than preregistered confirmation.
