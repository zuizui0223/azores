#!/usr/bin/env python3
"""Fail-closed manuscript QC for Azores V4."""
from __future__ import annotations

import json
import re
from pathlib import Path

M = Path("manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md")
C = Path("manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V4.json")
R = Path("results/entry_state_score_transferability_v1.json")
D = Path("results/dutch_condition_choice_test_v1.json")
W = Path("results/dutch_arrival_waiting_diagnostic_v1.json")
X = Path("results/cross_project_entry_state_score_v1.json")

text = M.read_text(encoding="utf-8")
contract = json.loads(C.read_text())
score = json.loads(R.read_text())
dutch = json.loads(D.read_text())
waiting = json.loads(W.read_text())
cross = json.loads(X.read_text())

checks = {}

def has(pattern: str) -> bool:
    return re.search(pattern, text, flags=re.I | re.M) is not None

def count_line(line: str) -> int:
    return sum(1 for x in text.splitlines() if x.strip() == line)

# Structure
checks["single_discussion_heading"] = count_line("## Discussion") == 1
checks["single_phase_question_heading"] = count_line("### Why phase-specific analysis changes the ecological question") == 1
checks["single_data_availability_heading"] = count_line("## Data availability") == 1
checks["no_stale_V3_label"] = not has(r"\bV3\b|MANUSCRIPT_V3")
checks["no_pending_dutch_gate"] = not has(r"Until that gate passes|Current gate:\s*|retrieve the public DANS files")

# Correct canonical event count: explicitly prevent old 427 bug.
checks["onset_418"] = has(r"418 onset events|onset events\s*=\s*\*\*418\*\*|418\s+onset events")
checks["no_onset_427"] = not has(r"427 onset events|onset events\s*=\s*427")

# Multivariate score numbers as displayed in V4.
checks["score_activation_OR_2_23"] = has(r"2\.23")
checks["score_onset_HR_1_32"] = has(r"1\.32")
checks["score_whole_speed_0_946"] = has(r"0\.946")
checks["score_segment_speed_1_028"] = has(r"1\.028")
checks["score_partial_r2_whole_018pct"] = has(r"0\.18%")
checks["score_partial_r2_segment_0026pct"] = has(r"0\.026%")
checks["cross_activation_OR_1_97"] = has(r"1\.97")
checks["cross_onset_HR_1_26"] = has(r"1\.26")
checks["cross_whole_speed_0_948"] = has(r"0\.948")
checks["cross_segment_speed_1_013"] = has(r"1\.013")

# Contract/result identity.
checks["score_schema"] = score.get("schema") == "azores.entry_state_score_transferability.v1"
checks["score_onset_events_result_418"] = score["score_transfer"]["onset"]["events"] == 418
checks["score_activation_exact"] = abs(score["score_transfer"]["activation"]["effect"]["odds_ratio"] - contract["entry_state_score"]["activation"]["or_per_sd"]) < 1e-9
checks["score_onset_exact"] = abs(score["score_transfer"]["onset"]["effect"]["hazard_ratio"] - contract["entry_state_score"]["onset"]["hr_per_sd"]) < 1e-9
checks["score_whole_speed_exact"] = abs(score["score_transfer"]["whole_route_speed"]["effect"]["ratio"] - contract["entry_state_score"]["whole_route_speed"]["ratio_per_sd"]) < 1e-9
checks["score_segment_speed_exact"] = abs(score["score_transfer"]["frozen_median_positive_interstation_speed"]["effect"]["ratio"] - contract["entry_state_score"]["frozen_segment_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_schema"] = cross.get("schema") == "azores.cross_project_entry_state_score.v1"
checks["cross_activation_exact"] = abs(cross["crossfitted_transfer"]["activation"]["effect"]["odds_ratio"] - contract["cross_project_entry_state"]["activation"]["or_per_sd"]) < 1e-9
checks["cross_onset_exact"] = abs(cross["crossfitted_transfer"]["onset"]["effect"]["hazard_ratio"] - contract["cross_project_entry_state"]["onset"]["hr_per_sd"]) < 1e-9
checks["cross_whole_speed_exact"] = abs(cross["crossfitted_transfer"]["whole_route_speed"]["effect"]["ratio"] - contract["cross_project_entry_state"]["whole_route_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_segment_speed_exact"] = abs(cross["crossfitted_transfer"]["frozen_median_positive_interstation_speed"]["effect"]["ratio"] - contract["cross_project_entry_state"]["frozen_segment_speed"]["ratio_per_sd"]) < 1e-9
checks["cross_weight_signs_positive"] = bool(cross["weight_stability"]["stage_beta_all_positive"] and cross["weight_stability"]["condition_beta_all_positive"])

# Dutch falsification language and numbers.
checks["dutch_falsification_heading"] = has(r"did not support condition-dependent barrier selectivity|falsified the specific prediction")
checks["dutch_CL_beta"] = has(r"β\s*=\s*[−-]0\.095")
checks["dutch_CL_p"] = has(r"p\s*=\s*0\.841")
checks["dutch_CL_perm_p"] = has(r"permutation p\s*=\s*0\.849")
checks["dutch_EZ_missed_null"] = has(r"r\s*=\s*0\.009.*p\s*=\s*0\.960")
checks["dutch_CL_missed_null"] = has(r"r\s*=\s*[−-]0\.104.*p\s*=\s*0\.592")
checks["dutch_choice_schema"] = dutch.get("schema") == "azores.dutch_condition_choice_test.v1"
checks["dutch_waiting_schema"] = waiting.get("schema") == "azores.dutch_arrival_waiting_diagnostic.v1"

# Interpretation boundaries.
checks["terminal_sensitivity_only"] = has(r"terminal.*sensitivity")
checks["nonmembership_not_failure"] = has(r"non-membership.*not.*(?:biological )?failure|complement.*not.*validated.*failure")
checks["no_escapement_claim"] = not has(r"we estimate(?:d)? escapement probability|escapement probability was")
checks["entry_not_progression_speed_claim"] = has(r"entry-state indicator.*not.*(?:transferable )?general progression-speed score|entry state is not a progression-speed score")
checks["no_asset_protection_support"] = not has(r"(support(?:s|ed)?|confirm(?:s|ed)?)\s+(?:a\s+)?(?:general\s+)?asset[- ]protection")
checks["no_dutch_handoff_confirmation"] = not has(r"Dutch.{0,100}(confirm(?:s|ed|ation)|support(?:s|ed)).{0,100}(handoff|internal-to-external)")

# Reference requirements.
for key in ["Durif, C.", "Nathan, R.", "Verhelst, P.", "Huisman, J. B. J.", "van Rijn, J.", "Lennox, R. J.", "Moyo, S."]:
    checks[f"ref::{key}"] = key in text

failed = [k for k,v in checks.items() if not v]
result = {
    "schema":"azores.manuscript_qc.v4",
    "manuscript":str(M),
    "contract":str(C),
    "status":"PASS" if not failed else "FAIL",
    "checks":checks,
    "failed":failed,
}
Path("manuscript/MANUSCRIPT_QC_V4.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
raise SystemExit(0 if not failed else 1)
