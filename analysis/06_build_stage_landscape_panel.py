#!/usr/bin/env python3
"""Build a descriptive growth/premigrant -> behavioral-migration landscape panel."""
from __future__ import annotations
import argparse,csv,json,math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
TRUE={"true","1","t","yes","y"}; PRE={"i":"growth","fi":"growth","fii":"growth","fiii":"premigrant"}
def read(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def norm(x):return (x or "").strip().lower()
def pb(x):return norm(x) in TRUE
def num(x):
    try:return float(str(x).strip())
    except:return None
def tm(x):
    v=(x or "").strip().replace("Z","+00:00")
    if not v:return None
    for fmt in (None,"%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try:return datetime.fromisoformat(v) if fmt is None else datetime.strptime(v,fmt)
        except:pass
    return None
def median(v):
    v=sorted(v)
    if not v:return None
    n=len(v);return v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source-repo",default="external/eel-meta-analysis");ap.add_argument("--gate",default="analysis/results/processed_panel_transition_audit.json");ap.add_argument("--out",default="analysis/results/state_landscape_panel.csv");args=ap.parse_args()
    gate=json.loads(Path(args.gate).read_text(encoding="utf-8"))
    if gate.get("status")!="GO_STATE_LANDSCAPE_AUDIT":print(json.dumps({"status":"STOP","gate_status":gate.get("status")},indent=2));return
    root=Path(args.source_repo);meta=defaultdict(list);wrs=defaultdict(list);tracks=defaultdict(list)
    for r in read(root/"data/interim/eel_meta_data.csv"):
        tag=(r.get("acoustic_tag_id") or "").strip()
        if tag:meta[tag].append(r)
    for r in read(root/"data/external/eels_wrs.csv"):
        tag=(r.get("acoustic_tag_id") or "").strip()
        if tag:wrs[tag].append(r)
    for p in sorted((root/"data/interim/migration").glob("migration_*.csv")):
        for r in read(p):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag:tracks[tag].append(r)
    outrows=[]
    for tag,tr in tracks.items():
        if len(meta[tag])!=1:continue
        m=meta[tag][0];stage=norm(m.get("life_stage"))
        if stage not in PRE:continue
        tr=sorted(tr,key=lambda r:tm(r.get("arrival")) or datetime.max);mig=[i for i,r in enumerate(tr) if pb(r.get("migration"))]
        if not mig:continue
        i0=min(mig);pre=tr[:i0];post=tr[i0:]
        def vals(part,key):return [z for z in (num(r.get(key)) for r in part) if z is not None]
        pre_dist=vals(pre,"distance_to_source_m");post_dist=vals(post,"distance_to_source_m");pre_speed=vals(pre,"speed_m_s");post_speed=vals(post,"speed_m_s")
        pre_range=(max(pre_dist)-min(pre_dist)) if pre_dist else None;post_range=(max(post_dist)-min(post_dist)) if post_dist else None
        ratio=math.log((post_range+1)/(pre_range+1)) if pre_range is not None and post_range is not None else None
        first=tm(tr[0].get("arrival"));onset=tm(tr[i0].get("arrival"));last=tm(tr[-1].get("arrival"));w=wrs[tag][0] if len(wrs[tag])==1 else {}
        outrows.append({"tag":tag,"initial_stage":stage.upper(),"initial_stage_group":PRE[stage],"project":m.get("animal_project_code"),"sex":m.get("sex"),"length1":m.get("length1"),"weight":m.get("weight"),"pre_rows":len(pre),"post_rows":len(post),"pre_days":((onset-first).total_seconds()/86400 if onset and first else None),"post_days":((last-onset).total_seconds()/86400 if onset and last else None),"pre_distance_range_m":pre_range,"post_distance_range_m":post_range,"mobility_release_log_ratio":ratio,"pre_speed_median_m_s":median(pre_speed),"post_speed_median_m_s":median(post_speed),"barrier_number":w.get("barrier_number"),"wrs_impact_score":w.get("wrs_impact_score"),"wrs_types":w.get("wrs_types"),"water_body_class":w.get("water_body_class")})
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    if outrows:
        with out.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=list(outrows[0]));w.writeheader();w.writerows(outrows)
    summary={"schema":"azores.state_landscape_panel.v2","status":"BUILT" if outrows else "EMPTY","individuals":len(outrows),"projects":len({r["project"] for r in outrows}),"growth_initial":sum(r["initial_stage_group"]=="growth" for r in outrows),"premigrant_initial":sum(r["initial_stage_group"]=="premigrant" for r in outrows),"with_pre3_post3":sum(r["pre_rows"]>=3 and r["post_rows"]>=3 for r in outrows),"with_mobility_release_ratio":sum(r["mobility_release_log_ratio"] is not None for r in outrows),"with_wrs":sum(r["wrs_impact_score"] not in (None,"") for r in outrows),"boundary":"Descriptive analysis table only; no fitted state or landscape effect."}
    Path(str(out)+".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
