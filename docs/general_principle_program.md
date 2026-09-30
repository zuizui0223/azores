# General ecological programme: state-dependent mobility gating

## Publication target

This project is not a re-analysis of the Flores yellow-eel study and is not a general paper about predictive memory.

The target is a movement-ecology question:

> **How does a high-mobility organism switch between local residence and long-distance movement as internal life-history state changes, and how strongly can landscape opportunity constrain that switch?**

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

### Mobility-gating hypothesis

Realised mobility is a behavioural phenotype produced by internal movement state × landscape opportunity × local refuge value, not a fixed species-level property.

For anguillid eels, the strongest state contrast is:

- yellow/growth phase: local growth, refuge use and optional exploration;
- silver/migratory phase: directed seaward movement.

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

### A2 — landscape gating of the state switch

The magnitude and timing of mobility release should interact with landscape opportunity. Barriers should delay or compress the realised silver-stage response, while high-flow/connectivity windows should permit stronger expression of the migratory state.

### A3 — local refuge value matters mainly before release

During the yellow stage, stable/high-value refuges should suppress exploratory movement. After silvering, the effect of local refuge quality should weaken relative to directional connectivity toward the sea.

### A4 — stage × landscape interaction beats a single movement rule

A model with stage-specific landscape effects should predict movement better across systems than a taxon-only mobility score, system size alone, barrier count alone, or a single landscape effect assumed constant across life stages.

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

> **Mobility is a gated phenotype: internal life-history state determines the motivation to move, while landscape opportunity determines how completely that latent mobility can be expressed.**

This is the ecological endpoint. EOG is only the route that exposed the extreme resident anchor.