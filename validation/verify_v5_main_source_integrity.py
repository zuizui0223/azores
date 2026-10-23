#!/usr/bin/env python3
"""Source-linked ecological integrity review of condensed V5 European eel text.

The checker verifies that no figures or numerical claims drifted from the
existing V4 evidence contract. It cannot certify author metadata, ethics
permissions, literature completeness, typesetting or journal acceptance.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
V5=ROOT/"manuscript/AZORES_PHASE_TRANSFER_MAIN_V5_DRAFT.md"
SUP=ROOT/"manuscript/AZORES_V5_SUPPLEMENT_EVIDENCE_MAP.md"
V4=ROOT/"manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md"
DATA=ROOT/"manuscript/FIGURE_DATA_CONTRACT_V4.json"
QC_V4=ROOT/"manuscript/MANUSCRIPT_QC_V4.json"
OUT=ROOT/"manuscript/V5_SCIENTIFIC_REVIEW_QC.json"

def verify():
    m=V5.read_text(encoding="utf-8")
    supplement=SUP.read_text(encoding="utf-8")
    full=V4.read_text(encoding="utf-8")
    c=json.loads(DATA.read_text(encoding="utf-8"))
    q=json.loads(QC_V4.read_text(encoding="utf-8"))
    if q.get("status")!="PASS":raise ValueError("STOP_V4_CANONICAL_QC_NOT_PASS")
    figures=c["main_figures"]
    words=len(re.findall(r"\b[\w'-]+\b",m))
    checks={}
    checks["compact_main_2300_5000_words"]=2300<=words<=5000
    checks["evidence_and_word_count_reduced"]=len(m)<len(full)*.50
    headings=("## Abstract","## Introduction","## Methods","## Results",
              "## Discussion","## Conclusions","## Figures","## Data, code and ethics",
              "## References")
    checks["all_scientific_sections"]=all(x in m for x in headings)
    checks["source_separated_from_paper"]=all(x in m for x in (
        "secondary analyses","not a direct replication",
        "not a verified failure","does not prove", "source-classified"))
    checks["six_projects_and_575"]=("six European projects" in m and "575 stage-coded" in m)
    checks["canonical_stage_counts"]=all(
        f"{row['initiated']}/{row['tracked']}" in m
        for row in figures["figure2"]["activation_by_stage"]
    )
    main=figures["figure3"]["entry_state_transfer"]
    checks["phase_score_point_values"]=all(
        f"{x['estimate']:.3f}" in m for x in main
    )
    checks["phase_score_interval_values"]=all(
        f"{x['lo']:.3f}" in m and f"{x['hi']:.3f}" in m for x in main
    )
    checks["coefficient_source"]=(
        f"{figures['figure2']['multivariate_activation'][0]['estimate']:.2f}" in m
        and f"{figures['figure2']['multivariate_activation'][1]['estimate']:.2f}" in m
    )
    checks["crossproject_effect_values"]=all(
        x in m for x in ("OR 1.97","hazard ratio 1.26","ratio 0.948","1.013")
    )
    link=figures["figure3"]["exact_link_transit"]
    checks["within_link_sample"]=all(str(x) in m for x in
             (link["n_segment_rows"],link["n_fish"],link["n_directed_links"]))
    checks["within_link_ratio"]=f"{link['ratio_per_sd']:.3f}" in m
    checks["river_year_exact"]=all(
        v in m for v in ("507","14 project × release-year","19.087",
                        "0.003142","46,116","0.05310","Albertkanaal"))
    checks["dutch_negative_mechanism"]=all(
        v in m for v in ("permutation p=0.849","n=15","near","unsupported")
    )
    checks["all_four_source_matched_figures"]=all(
        (ROOT/f"manuscript/rendered_figures_v4/Figure{i}.svg").is_file()
        and f"rendered_figures_v4/Figure{i}.svg" in m for i in range(1,5)
    )
    checks["no_completion_failure_claim"]=not bool(
        re.search(r"\b(estimated escapement probability|failure to escape|proved no physiological effect|universally absent speed effect)\b",m,re.I))
    checks["supplement_all_caveat_sections"]=all(
        f"**S{i} " in supplement for i in range(1,9))
    checks["supplement_preserves_v4"]=(
        "AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md" in supplement and
        "11 hypothetical false negatives" in supplement and
        "observability" in supplement and
        "not biological survival or escapement" in supplement
    )
    checks["reference_names_in_source_v4"]=all(
        key in m and key in full for key in
        ("Verhelst","Durif","van Rijn","Tudorache","Nathan","Winkler")
    )
    failed=sorted(k for k,v in checks.items() if not v)
    status="PASS_SCIENTIFIC_SOURCE_CONSISTENCY_AUTHOR_INPUT_PENDING" if not failed else "FAIL_SCIENTIFIC_SOURCE_CONSISTENCY"
    pending=["author names and affiliations", "author contributions and acknowledgements",
             "final source-study ethics approval citation", "journal format, target, and length",
             "complete, verified journal bibliography", "real typeset supplement and author figure review"]
    return {
        "schema":"azores.v5_condensed_main_source_qc.v1",
        "status":status, "main_file":str(V5.relative_to(ROOT)),
        "source_v4_qc":"PASS", "v5_wordcount_approx":words,
        "source_v4_characters":len(full),"v5_characters":len(m),
        "checks":checks,"failed":failed,"human_submission_blocks":pending,
        "certification_scope":"Scientific text/source numeric consistency only. No journal submission, statistical refitting or human author approval."
    }

if __name__=="__main__":
    result=verify()
    OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    sys.exit(0 if result["status"].startswith("PASS") else 2)
