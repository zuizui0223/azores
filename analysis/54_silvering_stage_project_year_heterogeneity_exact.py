#!/usr/bin/env python3
"""Release-year-stratified *exact* FV/FIII initiation heterogeneity audit.

The original six-project stage contrast is potentially confounded by release
year. Year-specific totals, stage frequencies and event totals are conditioned
upon here, so every project × year has a separate nuisance baseline.

Year-wise Fisher noncentral hypergeom polynomials are convolved within each
project. The resulting project sufficient count distributions support exactly
the same likelihood-ratio homogeneity test as analysis/53, while conditioning
on the pooled number of FV starts removes the shared odds-ratio nuisance.

Post-hoc observational diagnostic, not a causal hydraulic test.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

MODEL = Path("analysis/53_silvering_stage_project_heterogeneity_exact.py")
BASE = Path("analysis/31_entry_state_score_transferability.py")
CONTRACT = Path("analysis/contracts/silvering_stage_project_year_heterogeneity_exact_v1.json")
OUTPUT = Path("analysis/results/silvering_stage_project_year_heterogeneity_exact.json")


def import_module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


M=import_module(MODEL,"silvering_conditional_test")
B=import_module(BASE,"eel_analysis_base")


class YearAdjustedProject(M.Block):
    def __init__(self,project,blocks):
        """Convolve within-year nuisance-free combinatorial coefficients."""
        if not blocks:
            raise ValueError("Empty project blocks")
        self.project=project
        self.blocks=blocks
        self.n0=sum(b.n0 for b in blocks)
        self.n1=sum(b.n1 for b in blocks)
        self.y0=sum(b.y0 for b in blocks)
        self.y1=sum(b.y1 for b in blocks)
        self.total=self.y0+self.y1
        coeff={0:0.0}
        for b in blocks:
            nxt={}
            for subtotal,logw in coeff.items():
                for i,k in enumerate(b.values):
                    pos=subtotal+k
                    proposal=logw+b.lcombs[i]
                    nxt[pos]=M.logadd(nxt.get(pos,-math.inf),proposal)
            coeff=nxt
        self.lo=min(coeff)
        self.hi=max(coeff)
        self.values=list(range(self.lo,self.hi+1))
        self.lcombs=[coeff.get(k,-math.inf) for k in self.values]
        if any(not math.isfinite(v) for v in self.lcombs):
            raise ValueError("Convolved support has gap")
        if not self.lo <= self.y1 <= self.hi:
            raise ValueError("Observed total outside project-year support")
        self.sup_logp={k:self._sup_log_prob(k) for k in self.values}


def build_blocks(rows):
    project_year=defaultdict(list)
    projects=sorted({r["project"] for r in rows})
    for r in rows:
        if r["stage"] not in {"FIII","FV"}:
            continue
        project_year[(r["project"],r["release"].year)].append(r)
    year_rows=[]
    groups=defaultdict(list)
    for (project,year),rs in sorted(project_year.items()):
        first=[r for r in rs if r["stage"]=="FIII"]
        last=[r for r in rs if r["stage"]=="FV"]
        block=M.Block(f"{project}::{year}",len(first),sum(bool(r["initiated"]) for r in first),
                      len(last),sum(bool(r["initiated"]) for r in last))
        groups[project].append(block)
        year_rows.append({
            "project":project,"year":year,
            "FIII":{"n":block.n0,"starts":block.y0},
            "FV":{"n":block.n1,"starts":block.y1},
            "within_year_stage_odd_information":block.hi>block.lo,
            "fv_start_support":[block.lo,block.hi]
        })
    project_blocks=[YearAdjustedProject(p,groups[p]) for p in projects]
    return project_blocks,year_rows


def exact_all_and_leave_one(blocks):
    ks=[b.y1 for b in blocks]
    theta=M.fit_common(blocks,ks)
    full=M.exact_conditional(blocks,ks,theta)
    leave=[]
    for i,block in enumerate(blocks):
        others=[b for j,b in enumerate(blocks) if i!=j]
        ys=[b.y1 for b in others]
        other_theta=M.fit_common(others,ys)
        exact=M.exact_conditional(others,ys,other_theta)
        leave.append({
            "excluded":block.project,
            "n_projects":len(others),
            "pooled_common_or":math.exp(other_theta),
            "exact_conditional_p":exact["exact_conditional_p"],
            "observed_lr":exact["observed_lr"],
            "admissible_joint_vectors":exact["admissible_joint_vectors"]
        })
    return theta,full,leave


def main():
    frozen=json.loads(CONTRACT.read_text(encoding="utf-8"))
    rows=B.load()
    if len(rows)!=575:
        raise ValueError(f"Expected source cohort 575; found {len(rows)}")
    blocks,years=build_blocks(rows)
    assert len(blocks)==6
    assert sum(b.n0 for b in blocks)==261
    assert sum(b.n1 for b in blocks)==246
    assert sum(b.y0 for b in blocks)==154
    assert sum(b.y1 for b in blocks)==215
    theta,exact,leave=exact_all_and_leave_one(blocks)
    primary={
        "common_or_FV_vs_FIII":math.exp(theta),
        "common_log_or":theta,
        "lr":exact["observed_lr"],
        "exact_p":exact["exact_conditional_p"],
        "joint_configurations":exact["admissible_joint_vectors"],
        "finite_sample_nuisance_cancelled":exact["common_odds_nuisance_cancelled"],
    }
    summary={
        "schema":"azores.silvering_stage_project_year_heterogeneity_exact.v1",
        "evidence_class":frozen["evidence_class"],
        "contract":str(CONTRACT),
        "source":"analysis/31_entry_state_score_transferability.py::load; pinned 575-fish six-project panel",
        "n_projects":len(blocks),
        "n_fish_all_stages":len(rows),
        "n_fish_FIII_FV":sum(b.n0+b.n1 for b in blocks),
        "n_project_year_stage_cells":len(years),
        "n_year_cells_with_estimable_stage_contrast":sum(x["within_year_stage_odd_information"] for x in years),
        "year_cells":years,
        "project_margins":[{
            "project":b.project,"n_release_years":len(b.blocks),
            "FIII":{"n":b.n0,"starts":b.y0},
            "FV":{"n":b.n1,"starts":b.y1},
            "fv_starts_support":[b.lo,b.hi]
        } for b in blocks],
        "year_baseline_adjusted_exact_test":primary,
        "leave_one_project_out":leave,
        "claim_boundaries":frozen["caveats"]
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
