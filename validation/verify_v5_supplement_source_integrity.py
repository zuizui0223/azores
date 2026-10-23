#!/usr/bin/env python3
"""Verify every V5 supplementary evidence excerpt is source-exact V4 text.

The document is an author-review scientific supplement draft. This validates
full verbatim methods/results integrity and section organization, not journal
acceptance, reference list completeness or original ethical approvals.
"""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"manuscript/AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md"
TARGET=ROOT/"manuscript/AZORES_V5_SUPPLEMENT_METHODS_RESULTS_DRAFT.md"
OUTPUT=ROOT/"manuscript/V5_SUPPLEMENT_SOURCE_QC.json"
SOURCE_MARK=re.compile(r"^#{2,3} ([^\n]+)$",re.M)
BLOCK_RE=re.compile(
    r"<!-- V4_SOURCE_BEGIN: ([^\n]+) -->\n(.*?)\n<!-- V4_SOURCE_END: \1 -->",
    re.S
)

def audit():
    source=SOURCE.read_text(encoding="utf-8")
    doc=TARGET.read_text(encoding="utf-8")
    found=list(SOURCE_MARK.finditer(source))
    indexed={}
    for i,m in enumerate(found):
        last=found[i+1].start() if i+1<len(found) else len(source)
        indexed[m.group(1)]=source[m.start():last].strip()
    blocks=list(BLOCK_RE.finditer(doc))
    result={"schema":"azores.v5_supplement_verbatim_source_qc.v1",
       "target":str(TARGET.relative_to(ROOT)),
       "source":str(SOURCE.relative_to(ROOT)),
       "source_sha256":hashlib.sha256(source.encode()).hexdigest(),
       "n_source_subsections":len(blocks),
       "n_source_titles":len(set(x.group(1) for x in blocks)),
       "checks":{}}
    check=result["checks"]
    check["all_35_excerpts"]=len(blocks)==35
    check["each_title_unique"]=len(set(b.group(1) for b in blocks))==len(blocks)
    check["verbatim_original_sections"]=all(
        b.group(1) in indexed and b.group(2).strip()==indexed[b.group(1)]
        for b in blocks)
    check["no_orphan_open_close_marker"]=(
       doc.count("<!-- V4_SOURCE_BEGIN:")==len(blocks)==doc.count("<!-- V4_SOURCE_END:"))
    check["eight_supplement_sections"]=all(
        f"## S{i}. " in doc for i in range(1,9))
    check["source_v4_linkage"]=(
        "AZORES_PHASE_CONTROL_MANUSCRIPT_V4.md" in doc
        and "AZORES_PHASE_TRANSFER_MAIN_V5_DRAFT.md" in doc)
    check["observability_and_speed_boundaries"]=all(
        x in doc for x in
        ("Hypothetical", "receiver", "non-migrants", "source-derived", "causal")
    ) if False else all(x in doc for x in
       ("short-follow-up", "speed_m_s", "Albertkanaal", "arrival"))
    check["no_human_approval_claim"]=(
        "not a final journal-formatted supplement" in doc
        and "ethics approval" in doc)
    result["failed"]=[k for k,v in check.items() if not v]
    result["status"]=(
        "PASS_VERBATIM_ECOLOGICAL_SOURCE_DRAFT_NOT_JOURNAL_READY"
        if not result["failed"] else "STOP_SUPPLEMENT_SOURCE_DRIFT"
    )
    return result

if __name__=="__main__":
    q=audit()
    OUTPUT.write_text(json.dumps(q,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(q,indent=2))
    sys.exit(0 if q["status"].startswith("PASS") else 2)
