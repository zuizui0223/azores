#!/usr/bin/env python3
"""Network-free synthetic checks for selection null denominator and score locking."""
import importlib.util
from pathlib import Path

m=Path("analysis/45_observability_selection_gate.py")
spec=importlib.util.spec_from_file_location("observation_gate",m)
audit=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit)


def fish(tag,y,base,plus,project="P",stratum="P::2020"):
    return {"fish":tag,"initiated":y,"score_base":base,"score_plus":plus,
            "project":project,"stratum":stratum,"stage":"FIII"}


def test_selected_pair_conservation():
    scored=[
      fish("p1",1,.9,.9),fish("p2",1,.5,.7),
      fish("n1",0,.8,.6),fish("n2",0,.6,.2),fish("n3",0,.1,.8),
      fish("n4",0,.1,.9,project="Q",stratum="Q::2021"),
    ]
    included={"p1","p2","n1","n3"}
    cells=audit.build_selection_cells(scored,included)
    assert len(cells)==1
    first=cells[0]
    assert first["n_positive"]==2
    assert first["n_selected_noninitiators"]==2
    out=audit.stratified_retention_null(cells,n_perm=1500,seed=8)
    assert out["selected_positive_negative_pairs"]==4
    assert abs(out["observed_selected_auc_base"]-.75)<1e-12
    assert abs(out["observed_selected_auc_plus"]-.75)<1e-12
    assert abs(out["observed_selected_delta"])<1e-12
    assert out["conditional_random_retention"]["mean_delta"]>0
    assert out["conditional_random_retention"]["upper_tail_probability"]>.5


def test_no_positive_leakage():
    scored=[fish("p",1,.2,.5),fish("n",0,.1,.3)]
    try:
        audit.build_selection_cells(scored,{"n"})
    except AssertionError as e:
        assert "positive excluded" in str(e)
    else:
        raise AssertionError("Excluded initiator did not fail closed")


if __name__=="__main__":
    test_selected_pair_conservation()
    test_no_positive_leakage()
    print("PASS observation-gate synthetic tests")
