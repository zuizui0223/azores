# Physical receiver evidence behind 100 ambiguous eel noninitiation labels — 2026-10-08

**Evidence class:** retrospective source-event inventory, not survival, continuous listening effort or a physiological response. GitHub Actions [37765219057](https://github.com/zuizui0223/azores/actions/runs/37765219057) passed both the source-pinned inventory and synthetic real-receiver timing tests.

Canonical result: `results/receiver_witness_observability_v1.json`; reproducible implementation: `analysis/48_receiver_witness_observability.py`. The original repository was pinned at PieterjanVerhelst/eel-meta-analysis commit `59578cb622dddbbba5174b4c51bff0807787385a`.

## The first split was not simply a short versus long follow-up time

Source panel: 575 FIII/FIV/FV eels, 422 algorithmically classified initiators, 153 classified noninitiators.

The 90-day receiver-follow-up eligibility gate separates noninitiators into:
- **100 short-follow-up source noninitiators**;
- **53 day-90-supported source noninitiators**.

Source migration CSV files contain both **synthetic release pseudo-station rows** (e.g., `rel_warnow` with `receiver_id=none`) and events with physical `receiver_id`. We excluded pseudo-stations from evidence of actual receiver activity.

| Evidence | Short-follow-up negatives | Day-90-supported negatives | Source initiators |
|---|---:|---:|---:|
| Fish | 100 | 53 | 422 |
| Had at least one physical-receiver row | **76** | **53** | **422** |
| Had only synthetic release / no physical-receiver row | **24** | **0** | **0** |
| Median count of physical-receiver rows | **1** | **260** | **50** |
| Median number of unique real receivers | **1** | **2** | **12** |
| Median time from release to last real receiver event, *among those with one* | **0.680 d** | **549.11 d** | **72.93 d** |

The numbers demonstrate an enormous **observation-data-depth disparity** between source noninitiators. They do *not* show whether animals stayed, migrated, died, or were lost from the network.

## Additional observation witness: another tagged fish at the same receiver

For each of the **76 short-follow-up source negatives with at least one physical receiver contact**, we identified the exact last physical station/receiver, its last observed arrival/departure event, and searched *all source study fish* for a distinct tag at that same receiver **strictly later**, before focal release + 90 days.

- Another fish detected **within 1 day**: **58/76**.
- Another fish detected **within 7 days**: **66/76**.
- Another fish detected **within 30 days**: **68/76**.
- Another fish detected **within 90 days**: **70/76**.

Such records are a *point-in-time witness* that the receiver could detect another fish at that later event. They **do not establish uninterrupted receiver operation** in the intervening period, tag functionality, fish residence, range coverage, or failure/success of migration.

The simplest explanation that *every* early final detection was caused by that particular receiver permanently turning off at that instant is inconsistent with these later event witnesses. But a range of other explanations (fish movement away from coverage, insufficient downstream array geometry, tag loss, or mortality) remain indistinguishable without independent data.

## Stage and project support

Within the 100 short-follow-up negative labels:
- FIII: **70**, including **20** with no physical receiver evidence;
- FIV: **13**, including **3** with no physical receiver evidence;
- FV: **17**, including **1** with no physical receiver evidence.

By project, virtual-only counts among short-follow-up negatives were:
- Warnow **2/33**;
- Leopoldkanaal **6/7**;
- Albertkanaal **0/2**;
- Verhelst **2/19**;
- Grotenete **3/5**;
- ESGL **11/34**.

This demonstrates substantial **uneven observability across river projects and silvering classes**. It is not proof of differential receiver efficiency or stage-dependent movement; actual aquatic space use and receiver layout could generate the same pattern.

## Receiver operation periods were not identified

The pinned repository does contain `data/interim/deployments.csv` and `data/raw/deployments.csv` as well as station network files, but the relevant files provide **station coordinates** and not complete deploy/recovery dates for the six focal projects. Some non-focal Nedap data include receiver-time metadata; those cannot simply be transferred to these projects.

Therefore the real receiver contact data **cannot create a 90-day biological nonmovement label** or a quantitative detector uptime / detection probability estimate.

## Ecological conclusion and conservation boundary

An apparently clean binary migration-entry response is a compound of:
1. fish physiology and commitment, potentially varying within silvering stage;
2. exposure to environmental cues and routes;
3. tagging and receiver exposure/detection;
4. the source threshold for *classified* migration.

The present public telemetry panel contains signal about source-classified entry but does not uniquely identify those components. Genuine physiological initiation, safe barrier passage and eventual escapement remain separate endpoints. For management, recording **active receiver deployment periods**, fish-specific exposure and independent downstream witnesses is necessary before using non-detection to infer migration failure.

## Follow-up mathematical sensitivity

The constrained exact-label audit passed independent GitHub Actions [37765521770](https://github.com/zuizui0223/azores/actions/runs/37765521770). Canonical result: `results/receiver_stratified_label_tipping_v1.json`.

**The counterintuitive result:** the exact original worst-case eleven-label assignment included **9 fish with physical receiver contact** and **only 2 with no physical receiver contact**. Constraining the worst-case hypothetical misclassification to each observational group gives:

| Only hypothetical hidden starts drawn from… | Eligible source negatives | Minimum k to erase +0.03356 condition AUC |
|---|---:|---:|
| No real receiver contact | 24 | **Impossible even if all 24 switched** |
| Had at least one real receiver contact | 76 | **13** |
| Other fish later recorded at that same receiver within 90 days | 70 | **13** |
| Other fish later recorded at the same receiver within 1 day | 58 | **17** |
| No subsequent same-receiver witness within 90 days (includes no contacts) | 30 | **Impossible even if all 30 switched** |
| Unrestricted union of 100 | 100 | **11** |

The exact minimum at **11** changes is **+0.02081** if relabeling is constrained to the **24 virtual-only** fish, **+0.00288** for the 76 with any real contact, and **+0.00748** for the 58 whose last receiver later recorded another fish within a day. All are still positive.

This shows that the worst-case rank sensitivity is **not solely produced by those eels with no real receiver observations**. The most influential hypothetical relabelings include already-detected fish whose subsequent fates are unresolved. It does **not** show that such fish truly initiated, nor that receiver hardware worked continuously, nor that tag loss rather than habitat behavior caused the final detection. The result is a stronger *observation-process identifiability boundary*, not a newly identified physiological migration mechanism.
