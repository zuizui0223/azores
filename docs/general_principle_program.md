# General ecological programme: initiation–progression control handoff

## Publication target

This project is not a re-analysis of the Flores yellow-eel study and is not a general paper about predictive memory.

The target is a movement-ecology question:

> **Does the dominant controller of realised movement change across phases—from internal life-history state at migration initiation to external opportunity during migration progression?**

## Literature boundary

Several component ideas are already established:

- site fidelity can arise from stable/predictable resources, familiarity and movement costs;
- movement ecology already treats movement as the interaction of internal state, motion capacity, navigation and external environment;
- yellow-stage anguillid eels often show high site fidelity;
- silver-stage eels initiate directed seaward migration;
- landscape barriers and hydrodynamics can delay or alter eel migration.

Therefore none of those statements is the novelty claim.

The specific empirical target is their interaction within one unusually plastic movement architecture:

> **the same catadromous lineage can express resident and migratory movement regimes, and the magnitude/timing of that switch should depend on both internal migratory state and landscape opportunity.**

## Core hypothesis

### Two-stage mobility hypothesis

Realised migration is decomposed into two biologically distinct control stages.

**Stage 1 — activation**

Internal silvering/readiness regulates whether and when directed migration is expressed.

**Stage 2 — progression**

Once active migration is underway, local hydrological opportunity, barrier operation, route geometry and prior passage experience increasingly govern whether movement proceeds efficiently.

Thus the key prediction is not a universal Durif × barrier interaction. It is a **change in the dominant source of control across movement phases**.

For anguillid eels:

- yellow/pre-migrant state -> movement often remains latent;
- advanced silvering -> migration is more likely to activate;
- after activation -> progression can still be slowed or filtered by route-specific external conditions.

## Primary quantities

For individual i in system j:

- M_yellow: yellow-stage movement scale before migratory transition;
- M_silver: movement rate after migratory transition;
- T_release: timing of abrupt transition from resident to directional movement;
- L_access: accessible network length;
- B: barrier/resistance structure;
- Q: hydrological connectivity/flow opportunity;
- R_refuge: local refuge/resource stability.

A useful within-individual contrast is the mobility-release ratio:

R_stage = log((M_silver + epsilon) / (M_yellow + epsilon)).

Movement metrics must be harmonised within each telemetry design before cross-system comparison.

## Falsifiable predictions

### A1 — state release

Within individuals observed across the transition, movement should increase sharply after migratory state onset even though taxonomy and much of the landscape are unchanged.

### A2 — control handoff after activation

Once migration has activated, the marginal effect of Durif stage should weaken relative to hydrological opportunity, barrier operation, route geometry and prior passage experience.

### A3 — local refuge value matters mainly before release

During the yellow stage, stable/high-value refuges should suppress exploratory movement. After silvering, the effect of local refuge quality should weaken relative to directional connectivity toward the sea.

### A4 — phase-specific models beat one movement rule

A model that allows different predictors for activation and progression should outperform a single pooled movement rule that assumes internal state and external opportunity act identically throughout migration.

## What would falsify the programme

The mobility-gating interpretation is weakened if:

- apparent stage effects disappear after controlling body size, season and tracking design;
- individuals do not show a strong increase in movement around migratory transition;
- the same landscape variables have indistinguishable effects in yellow and silver stages;
- landscape opportunity does not modify migration timing/speed across independent systems;
- system-specific idiosyncrasy dominates any transferable stage × landscape relationship.

## Why Azores matters

Flores is an extreme yellow-stage endpoint: 36 yellow eels, one year of tracking, no valid receiver-to-receiver movement, a highly constrained pool–riffle–waterfall stream, and seasonal drying risk.

It supplies the **deep-residence anchor**, not the general test.

## Independent empirical route

Priority comparison systems:

1. **Wolastoq / Saint John River American eel** — 72 tagged yellow eels; most resident, several large seasonal movements; 16 individuals apparently transitioned to silver-stage outmigration. This is especially valuable because it contains a within-study life-history switch.
2. **Europe-wide European eel biotelemetry panel** — 2,306 eels across 18 water bodies; migration timing and speed vary with latitude, tidal setting, hydrodynamics and water-regulating structures. Raw individual access must be verified before treating it as executable evidence.
3. **Japanese yellow-eel telemetry systems** — useful as independent yellow-stage residence/movement contrasts.
4. **Additional small-stream European eel studies** — useful for separating small-system size from Azores-specific ecology.

## Main paper-level model

At minimum:

movement ~ life_history_state * landscape_opportunity + refuge_stability + body_size + season + tracking_design + (1 | study/system)

Where data permit within-individual stage transition:

movement_it ~ pre/post_migratory_state * hydrological_opportunity_t + individual random effects

## Strong ecological conclusion if supported

> **Realised migration is controlled sequentially: internal state governs activation, then external opportunity and route history increasingly govern progression.**

This is the ecological endpoint. EOG is only the route that exposed the extreme resident anchor.