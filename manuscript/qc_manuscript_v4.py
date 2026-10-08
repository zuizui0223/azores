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
L = Path("results/within_link_entry_state_speed_v1.json")
Q = Path("results/within_link_speed_quality_sensitivity_v1.json")
F = Path("results/within_link_fwl_numerical_audit_v1.json")
FD = Path("manuscript/FIGURE_DATA_CONTRACT_V4.json")
I = Path("results/cross_project_condition_increment_v1.json")
J = Path("results/cross_project_condition_increment_project_robustness_v1.json")
G = Path("results/stage_specific_condition_gate_v1.json")
H = Path("results/stage_gate_context_matched_robustness_v1.json")
CM = Path("results/continuous_morphology_condition_increment_v1.json")
PENALTY = Path("results/continuous_morphology_penalty_sensitivity_v1.json")

text = M.read_text(encoding="utf-8")
contract = json.loads(C.read_text())
score = json.loads(R.read_text())
dutch = json.loads(D.read_text())
waiting = json.loads(W.read_text())
cross = json.loads(X.read_text())
link = json.loads(L.read_text())
quality = json.loads(Q.read_text())
fwl = json.loads(F.read_text())
figure = json.loads(FD.read_text())
increment = json.loads(I.read_text())
project_robustness = json.loads(J.read_text())
stage_gate = json.loads(G.read_text())
stage_matched = json.loads(H.read_text())
morphology = json.loads(CM.read_text())
penalty = json.loads(PENALTY.read_text())

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
checks["within_link_ratio_0_962"] = has(r"0\.962")
checks["within_link_ci_0_883_1_048"] = has(r"0\.883") and has(r"1\.048")
checks["within_link_n_segments_17792"] = has(r"17,792")
checks["within_link_n_fish_418"] = has(r"17,792.{0,120}418")
checks["within_link_n_pairs_244"] = has(r"244")
checks["quality_ratios_present"] = has(r"0\.942") and has(r"0\.944") and has(r"0\.941")
checks["quality_boundary_present"] = has(r"3752") and has(r"53\.0") and has(r"63\.1")
checks["within_link_no_superseded_numbers"] = not has(r"18,012|0\.995|0\.00052%")
checks["within_link_weak_negative_quality_boundary"] = has(r"0\.07.{0,8}0\.08")

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
checks["within_link_schema"] = link.get("schema") == "azores.within_link_entry_state_speed.v1"
checks["within_link_ratio_exact"] = abs(link["primary"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["primary"]["ratio_per_sd"]) < 1e-9
checks["within_link_ci_exact"] = all(abs(a-b) < 1e-9 for a,b in zip(link["primary"]["entry_state_effect"]["ci95"], contract["within_link_entry_state"]["primary"]["ci95"]))
checks["within_link_sample_exact"] = link["primary"]["n_segment_rows"] == contract["within_link_entry_state"]["primary"]["n_segment_rows"] and link["primary"]["n_fish"] == contract["within_link_entry_state"]["primary"]["n_fish"] and link["primary"]["n_pairs"] == contract["within_link_entry_state"]["primary"]["n_directed_pairs"]
checks["within_link_status_null"] = link.get("status") == "NO_SUPPORTED_WITHIN_LINK_ENTRY_STATE_SPEED_GRADIENT"
checks["within_link_expert_correction"] = link.get("expert_non_migrant_segment_rows") == 0 and link.get("canonical_expert_non_migrant_count") == 9
checks["within_link_canonical_initiator_universe"] = link.get("raw_candidate_fish") == 422
checks["quality_uses_corrected_primary"] = quality.get("frozen_primary_reference", {}).get("n_fish") == link.get("primary", {}).get("n_fish") and abs(quality.get("frozen_primary_reference", {}).get("ratio", 0) - link.get("primary", {}).get("entry_state_effect", {}).get("speed_ratio_per_1sd_score", 999)) < 1e-9
checks["quality_schema"] = quality.get("schema") == "azores.within_link_speed_quality_sensitivity.v1"
checks["quality_status_robust"] = quality.get("status") == "WITHIN_LINK_NULL_ROBUST_TO_GROSS_SPEED_ARTIFACT_SCREEN"
checks["quality_2_5_exact"] = abs(quality["threshold_results"]["2.5"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["2.5"]["ratio_per_sd"]) < 1e-9
checks["quality_5_exact"] = abs(quality["threshold_results"]["5.0"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["5.0"]["ratio_per_sd"]) < 1e-9
checks["quality_10_exact"] = abs(quality["threshold_results"]["10.0"]["primary_model_after_quality_cut"]["entry_state_effect"]["speed_ratio_per_1sd_score"] - contract["within_link_entry_state"]["source_speed_quality_boundary"]["posthoc_upper_screen_results"]["10.0"]["ratio_per_sd"]) < 1e-9
checks["fwl_equivalence_pass"] = fwl.get("status") == "PASS_FWL_NUMERICAL_EQUIVALENCE"
checks["fwl_primary_agreement"] = fwl["primary_all_positive_source_speeds"]["absolute_beta_difference"] < 1e-8 and fwl["primary_all_positive_source_speeds"]["absolute_se_difference"] < 5e-4
checks["fwl_primary_sample_match"] = fwl["primary_all_positive_source_speeds"]["n_rows"] == link["primary"]["n_segment_rows"] and fwl["primary_all_positive_source_speeds"]["n_fish"] == link["primary"]["n_fish"]
checks["figure3_corrected_link"] = figure["main_figures"]["figure3"]["exact_link_transit"]["n_segment_rows"] == link["primary"]["n_segment_rows"] and abs(figure["main_figures"]["figure3"]["exact_link_transit"]["ratio_per_sd"] - link["primary"]["entry_state_effect"]["speed_ratio_per_1sd_score"]) < 1e-9
checks["figure3_quality_sensitivity"] = figure["main_figures"]["figure3"]["speed_quality_sensitivity"]["all_intervals_include_one"] is True

# Project-held-out AUC increment and project-level uncertainty.
delta = increment["primary_pairwise_auc"]["delta_auc_condition_above_stage_length_timing"]
incr_contract = contract["heldout_condition_increment"]
checks["condition_increment_schema"] = increment.get("schema") == "azores.cross_project_condition_increment.v1"
checks["condition_increment_n_projects"] = increment["n_projects"] == 6 and increment["n_source_evaluable"] == 575
checks["condition_increment_auc_exact"] = abs(delta - incr_contract["incremental_auc"]) < 1e-10
checks["condition_increment_auc_baseline_exact"] = abs(increment["primary_pairwise_auc"]["auc"]["score_base"] - incr_contract["base_auc"]) < 1e-10
checks["condition_increment_auc_plus_exact"] = abs(increment["primary_pairwise_auc"]["auc"]["score_plus"] - incr_contract["expanded_auc"]) < 1e-10
checks["condition_increment_pairs_exact"] = increment["primary_pairwise_auc"]["n_positive_negative_pairs"] == incr_contract["initiator_noninitiator_pairs"] == 6914
checks["condition_increment_stage_control"] = increment["secondary_same_stage_pairwise_auc"]["n_positive_negative_pairs"] == incr_contract["same_stage_pairs"] == 3199
checks["condition_increment_4_of_6"] = increment["primary_pairwise_auc"]["project_deltas_positive"] == incr_contract["n_projects_positive"] == 4
checks["condition_project_robustness_schema"] = project_robustness.get("schema") == "azores.cross_project_condition_increment_project_robustness.v1"
checks["condition_project_ci_includes_zero"] = project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"][0] < 0 < project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"][1]
checks["condition_project_ci_exact"] = all(abs(x-y)<1e-10 for x,y in zip(project_robustness["project_cluster_bootstrap"]["pair_weighted_gain_ci95"], incr_contract["project_cluster_bootstrap_ci95"]))
checks["condition_project_leave_one_out"] = min(p["delta_auc"] for p in project_robustness["leave_one_project_out"]) > 0
checks["condition_project_signed_test"] = abs(project_robustness["exploratory_exact_sign_flip"]["weighted"]["two_sided"] - 0.1875) < 1e-10
checks["condition_figure_contract_matches"] = abs(figure["supplementary"]["heldout_condition_increment"]["delta_auc"] - delta) < 1e-10
checks["condition_auc_reported"] = has(r"0\.610") and has(r"0\.643") and has(r"0\.0336")
checks["condition_project_uncertainty_reported"] = has(r"0\.0007") and has(r"0\.0918") and has(r"four of six") and has(r"p=0\.1875")

# Complete-morphology replication of the condition increment.
mc = contract["continuous_morphology_condition_increment"]
fig_m = figure["supplementary"]["continuous_silvering_morphology"]
checks["continuous_morphology_schema"] = morphology.get("schema") == "azores.continuous_morphology_condition_increment.v1"
checks["continuous_morphology_n"] = morphology["n_complete_morphology_evaluable"] == mc["n_morphology_complete"] == 429
checks["continuous_morphology_projects"] = morphology["n_eligible_projects"] == mc["n_projects"] == 5 and "2011_Warnow" not in morphology["eligible_projects"]
checks["continuous_morphology_n_pairs"] = morphology["primary"]["n_pairs"] == mc["n_positive_negative_pairs"] == 3272
checks["continuous_morphology_auc_identity"] = all(abs(morphology["primary"]["auc"][key] - mc["auc"][key]) < 1e-10 for key in ("base","morph","condition","full"))
checks["continuous_morphology_condition_increment"] = abs(morphology["primary"]["deltas"]["condition_after_morph"] - mc["delta_auc"]["condition_after_morph"]) < 1e-10
checks["continuous_morphology_ci_spans_zero"] = morphology["project_uncertainty"]["project_bootstrap"]["ci95"][0] < 0 < morphology["project_uncertainty"]["project_bootstrap"]["ci95"][1]
checks["continuous_morphology_project_signs"] = morphology["project_uncertainty"]["n_positive_project_deltas"] == mc["n_project_delta_positive"] == 3
checks["continuous_morphology_figure"] = abs(fig_m["delta_auc"]["condition_after_morph"]-mc["delta_auc"]["condition_after_morph"]) < 1e-10
checks["continuous_morphology_manuscript"] = has(r"429") and has(r"3,272") and has(r"0\.0244") and has(r"0\.0003") and has(r"0\.0659")
checks["continuous_morphology_no_energy_proof"] = has(r"cannot isolate fat reserves") and has(r"not justify interpreting condition as an independent energy-reserve trait")
checks["stage_schema"] = stage_gate.get("schema") == "azores.stage_specific_condition_gate.v1"
checks["stage_n_fish"] = stage_gate["n_evaluable_fish"] == 575 and stage_gate["n_informative_same_stage_pairs"] == 3199
checks["stage_FV_FIII_finite"] = stage_gate["stage"]["FV"]["delta_auc"] > stage_gate["stage"]["FIII"]["delta_auc"]
checks["stage_matched_schema"] = stage_matched.get("schema") == "azores.stage_gate_context_matched_robustness.v1"
checks["stage_matched_contexts"] = stage_matched["full"]["n_contexts"] == 5 and stage_matched["full"]["n_projects"] == 4
checks["stage_matched_uncertainty"] = stage_matched["exploratory_exact_project_signflip_two_sided_p"] == 0.25
checks["penalty_schema"] = penalty.get("schema") == "azores.continuous_morphology_penalty_sensitivity.v1"
checks["penalty_three_strengths"] = sorted(penalty.get("sweep",{}).keys()) == ["0.1","1.0","10.0"]
checks["penalty_frozen_lambda_exact"] = abs(penalty["sweep"]["1.0"]["delta_auc"]["condition_after_morph"] - morphology["primary"]["deltas"]["condition_after_morph"]) < 1e-10
checks["penalty_all_positive"] = penalty["all_increment_signs_positive"] is True and all(x["delta_auc"]["condition_after_morph"]>0 for x in penalty["sweep"].values())
checks["penalty_all_project_ci_overlap_zero"] = penalty["all_project_resample_cis_include_zero"] is True and all(x["project_ci95"][0] < 0 < x["project_ci95"][1] for x in penalty["sweep"].values())
checks["penalty_contract_consistency"] = all(abs(penalty["sweep"][k]["delta_auc"]["condition_after_morph"]-contract["continuous_morphology_penalty_sensitivity"]["condition_after_morph_delta_by_lambda"][k]) < 1e-10 for k in ("0.1","1.0","10.0"))
checks["penalty_manuscript_reporting"] = has(r"0\.0269") and has(r"0\.0244") and has(r"0\.0214")




checks["title_realized_transit_speed"] = text.startswith("# A multivariate entry state predicts migration activation but not realized transit speed in European eel")
checks["new_refs_present"] = "Tudorache, C." in text and "Katopodis, C." in text

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
