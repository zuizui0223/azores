# Independent-data feasibility audit

## Current decision

The project is no longer blocked on finding an independent eel dataset.

### GO — Europe-wide European eel biotelemetry dataset

**Paper**
- Verhelst et al. 2025, *Fish and Fisheries*
- DOI: 10.1111/faf.12904

**Open data**
- Verhelst 2025, *Detection data for silver eel meta-analysis*
- Zenodo: 10.5281/zenodo.15260539
- public file: `raw_detection_data.csv`
- size: about 1.1 GB
- MD5: `b4528016678b0bec8948265a7c285fab`

The dataset covers 16 ETN projects / 17 ETN locations; the associated analysis also includes two non-ETN projects from the code repository. The published study combines 18 water bodies and 2,306 tagged eels. Importantly, some animals were tagged in the yellow phase and later began seaward migration during tracking.

This is the strongest currently executable independent dataset for the **mobility-gating** programme.

## Why this dataset can test more than the published paper

The original meta-analysis focused on migration classification, arrival at sea, migration speed, tidal/non-tidal differences, geography and water-regulating structures.

Our question is different:

> **Does the effect of landscape opportunity change when an individual switches from a resident/growth movement state into a directed migratory state?**

The published method already provides a reproducible movement-state classifier. Their general rule using at least 4 km of movement at at least 0.01 m/s agreed with expert classification about 95% of the time.

The first analysis can therefore use the published state-classification machinery as provenance, then test a different estimand: **within-individual and cross-system change in movement expression around state transition**.

## Primary executable test

For individuals with sufficient pre-migration observations:

1. reconstruct detection sequence;
2. identify migration onset with the published classifier;
3. estimate pre-onset movement scale / station use;
4. estimate post-onset movement speed / directionality;
5. compute within-individual mobility-release contrast;
6. test whether the contrast differs among:
   - free-flowing versus regulated systems;
   - tidal versus non-tidal reaches;
   - water-body types;
   - hydrological opportunity where external flow data can be joined without outcome-driven selection.

### Gate A — pre-transition information

The mobility-gating hypothesis requires enough individuals with detections before classified migration onset.

If most animals enter the dataset only after migratory behaviour has started, **do not** claim a within-individual state switch from this panel. In that case use it only for the landscape-gating component and seek another stage-transition dataset.

### Gate B — landscape interaction

A stage effect alone is already expected biologically. The new target requires:

```text
movement_state × landscape_opportunity
```

If stage-specific landscape effects cannot be estimated across independent systems, the programme collapses to a known ontogenetic movement result.

## Secondary candidate — Wolastoq / Saint John River

Eissenhauer et al. 2026 tracked 72 American eels. Sixteen were classified as apparent silver-stage outmigrants, with rapid freshwater downstream movement after onset. This is an excellent biological replication because resident yellow-stage and migratory behaviour occur in the same river study.

Current status: **paper verified; public raw telemetry not located in the present audit**.

Use as:
- independent published contrast now;
- direct validation dataset if raw data become openly accessible.

## HOLD candidates

The Tone River, Mehaigne, Poole Harbour and other yellow-eel studies remain useful comparative systems, but raw individual telemetry access has not yet been verified here. Do not build the main analysis around them until access is confirmed.

## Immediate implementation target

The next executable object is the Europe-wide raw detection panel, not the Flores response.

Use `analysis/02_fetch_public_comparative_data.py` to audit/download the Zenodo record.
