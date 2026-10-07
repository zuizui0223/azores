#!/usr/bin/env python3
"""Schema/provenance audit for the downloaded Dutch DANS archive.

This script does not fit ecological effects. It inspects only the information
needed to reconstruct an arrival-defined risk set:
- codebook definitions for event/time/duration/passage fields;
- row counts and small structural summaries of passage tables;
- source-code lines that construct event IDs, validity and passage fields.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

TERMS = [
    "OutletID","OutletTimeTotal","valid","last_detection_time","Passage",
    "MaxOpenGates","Debietsom","MaxDischarge","distance_station",
    "distance_max","distance_1","SewerArrival","SewerDeparture"
]
FILES = [
    "biometrics_cl.tab","biometrics_ez.tab","durif_21.tab",
    "passage_cl.tab","passage_ez.tab","station_info.tab"
]
RFILES = [
    "calculate_distance_validity.R","mpo_model_cl.R","mpo_model_ez.R",
    "passage_glmm_cl.R","passage_glmm_ez.R"
]

def read_tab(path: Path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))

def compact_row(row):
    return {k:v for k,v in row.items() if v not in (None,"")}

def source_hits(path: Path):
    lines=path.read_text(encoding="utf-8-sig",errors="replace").splitlines()
    hits=[]
    for i,line in enumerate(lines):
        if any(t.lower() in line.lower() for t in TERMS):
            lo=max(0,i-1);hi=min(len(lines),i+2)
            hits.append({"line":i+1,"context":"\n".join(lines[lo:hi])})
    return hits[:80]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",default="external/dutch_dans")
    ap.add_argument("--out",default="analysis/results/dutch_schema_provenance_audit.json")
    a=ap.parse_args()
    root=Path(a.data_dir)

    codebook=read_tab(root/"codebook.tab")
    cb=[
        r for r in codebook
        if any(t.lower() in (r.get("variable_file") or "").lower() for t in TERMS)
        or any(t.lower() in (r.get("variable_manuscript") or "").lower() for t in TERMS)
        or any(x in (r.get("description") or "").lower()
               for x in ("outlet","duration","passage","discharge","detection","valid"))
    ]

    tables={}
    for name in FILES:
        p=root/name
        rows=read_tab(p)
        header=list(rows[0].keys()) if rows else []
        summary={"n_rows":len(rows),"header":header,"first_rows":[compact_row(x) for x in rows[:3]]}
        if name.startswith("passage_") and rows:
            for col in ("valid","Passage","Group","OutletID","OutletTimeTotal","LastStation"):
                if col in header:
                    vals=[r.get(col,"") for r in rows]
                    uniq=sorted(set(vals))
                    summary[col]={
                        "n_nonempty":sum(v!="" for v in vals),
                        "n_unique":len(uniq),
                        "sample_unique":uniq[:20]
                    }
        tables[name]=summary

    r_sources={}
    for name in RFILES:
        p=root/name
        if p.exists():
            r_sources[name]=source_hits(p)

    result={
        "schema":"azores.dutch_schema_provenance_audit.v1",
        "codebook_relevant_rows":cb,
        "tables":tables,
        "r_source_hits":r_sources,
        "questions":[
            "Does OutletID encode discharge-event timing or a stable event key?",
            "Does OutletTimeTotal represent event duration independently of eel validity?",
            "Do passage tables retain invalid/unreachable events that can be re-filtered after observed barrier arrival?",
            "Can first barrier arrival and confirmed passage be joined from detections/biometrics without using duration?"
        ]
    }
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
