#!/usr/bin/env python3
"""Build a per-eel state/landscape table from source-study processed outputs.

Requires GO_STATE_LANDSCAPE_AUDIT. Uses source migration flags as fixed labels
and does not refit the source migration classifier.

Outputs descriptive pre/post movement quantities for yellow-at-tagging eels
that later enter migration, plus WRS/water-body covariates. No inferential model
is fit here.
"""
from __future__ import annotations
import argparse,csv,json,math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

TRUE={"true","1","t","yes","y"}

def read(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def b(x):return (x or "").strip().lower() in TRUE
def n(x):
    try:return float(str(x).strip())
    except:return None
def t(x):
    v=(x or "").strip().replace("Z","+00:00")
    if not v:return None
    for fmt in (None,"%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try:return datetime.fromisoformat(v) if fmt is None else datetime.strptime(v,fmt)
        except:pass
    return None
def norm(x):return (x or "").strip().lower()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-repo",default="external/eel-meta-analysis")
    ap.add_argument("--gate",default="analysis/results/processed_panel_transition_audit.json")
    ap.add_argument("--out",default="analysis/results/yellow_to_migration_landscape_panel.csv")
    args=ap.parse_args()
    gate=json.loads(Path(args.gate).read_text(encoding="utf-8"))
    if gate.get("status")!="GO_STATE_LANDSCAPE_AUDIT":
        print(json.dumps({"status":"STOP","reason":"transition audit did not pass","gate_status":gate.get("status")},indent=2));return

    root=Path(args.source_repo)
    meta_rows=read(root/"data/interim/eel_meta_data.csv")
    wrs_rows=read(root/"data/external/eels_wrs.csv")
    meta_by_tag=defaultdict(list);wrs_by_tag=defaultdict(list)
    for r in meta_rows: meta_by_tag[(r.get("acoustic_tag_id") or "").strip()].append(r)
    for r in wrs_rows: wrs_by_tag[(r.get("acoustic_tag_id") or "").strip()].append(r)

    tracks=defaultdict(list)
    for p in sorted((root/"data/interim/migration").glob("migration_*.csv")):
        for r in read(p):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag: tracks[tag].append(r)

    outrows=[]
    for tag, rows in tracks.items():
        ms=meta_by_tag.get(tag,[])
        if len(ms)!=1: continue
        meta=ms[0]
        if norm(meta.get("life_stage"))!="yellow": continue
        rows=sorted(rows,key=lambda r:t(r.get("arrival")) or datetime.max)
        mig_idx=[i for i,r in enumerate(rows) if b(r.get("migration"))]
        if not mig_idx: continue
        i0=min(mig_idx)
        pre=rows[:i0];post=rows[i0:]
        def vals(part,key):
            return [v for v in (n(r.get(key)) for r in part) if v is not None]
        pre_dist=vals(pre,"distance_to_source_m")
        post_dist=vals(post,"distance_to_source_m")
        pre_speed=vals(pre,"speed")
        post_speed=vals(post,"speed")
        first=t(rows[0].get("arrival")); onset=t(rows[i0].get("arrival")); last=t(rows[-1].get("arrival"))
        wrs=wrs_by_tag.get(tag,[{}])
        w=wrs[0] if len(wrs)==1 else {}
        pre_range=(max(pre_dist)-min(pre_dist)) if pre_dist else None
        post_range=(max(post_dist)-min(post_dist)) if post_dist else None
        ratio=None
        if pre_range is not None and post_range is not None:
            ratio=math.log((post_range+1.0)/(pre_range+1.0))
        outrows.append({
            "tag":tag,
            "project_at_tagging":meta.get("animal_project_code"),
            "sex":meta.get("sex"),
            "length1":meta.get("length1"),
            "weight":meta.get("weight"),
            "life_stage_at_tagging":"yellow",
            "pre_rows":len(pre),"post_rows":len(post),
            "pre_days":((onset-first).total_seconds()/86400 if first and onset else None),
            "post_days":((last-onset).total_seconds()/86400 if onset and last else None),
            "pre_distance_range_m":pre_range,
            "post_distance_range_m":post_range,
            "mobility_release_log_ratio":ratio,
            "pre_speed_median_raw":(sorted(pre_speed)[len(pre_speed)//2] if pre_speed else None),
            "post_speed_median_raw":(sorted(post_speed)[len(post_speed)//2] if post_speed else None),
            "barrier_number":w.get("barrier_number"),
            "wrs_impact_score":w.get("wrs_impact_score"),
            "wrs_types":w.get("wrs_types"),
            "water_body_class":w.get("water_body_class"),
        })

    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    if outrows:
        with out.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(outrows[0]));w.writeheader();w.writerows(outrows)
    summary={
        "schema":"azores.yellow_to_migration_landscape_panel.v1",
        "status":"BUILT" if outrows else "EMPTY",
        "individuals":len(outrows),
        "projects":len({r["project_at_tagging"] for r in outrows}),
        "water_body_classes":sorted({str(r["water_body_class"]) for r in outrows if r["water_body_class"] not in (None,"")}),
        "with_pre3_post3":sum(r["pre_rows"]>=3 and r["post_rows"]>=3 for r in outrows),
        "with_wrs":sum(r["wrs_impact_score"] not in (None,"") for r in outrows),
        "boundary":"Descriptive panel only. State labels come from source study; no state effect or causal landscape interaction is inferred here."
    }
    Path(str(out)+".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
