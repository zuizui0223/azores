#!/usr/bin/env python3
"""Synthetic tests for exact release-year nuisance-baseline conditioning."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location(
    "silvering_year",
    Path("analysis/54_silvering_stage_project_year_heterogeneity_exact.py")
)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

# For a project comprising two informative release years with 1 FIII and
# 1 FV individual and one start per year, the year-stratified combinatorial
# coefficients convolve from [1,1] twice to [1,2,1].
b1=m.M.Block("A::2018",1,1,1,0)
b2=m.M.Block("A::2019",1,0,1,1)
a=m.YearAdjustedProject("A",[b1,b2])
assert a.values==[0,1,2]
assert a.y1==1
assert abs(a.lcombs[0])<1e-12
assert abs(a.lcombs[1]-m.math.log(2))<1e-12
assert abs(a.lcombs[2])<1e-12
assert abs(a.expectation(0)-1)<1e-12
assert abs(sum(a.probs(0)[0])-1)<1e-12

# Two projects with the same year-fixed margins and identical outcome,
# no heterogeneity; exact enumeration includes exactly three joint vectors.
c=m.YearAdjustedProject("B",[b1,b2])
th,result,loo=m.exact_all_and_leave_one([a,c])
assert abs(th)<1e-10
assert abs(result["observed_lr"])<1e-9
assert result["admissible_joint_vectors"]==3
assert abs(result["exact_conditional_p"]-1)<1e-10
assert len(loo)==2

# One project with stage entirely absent in one year gives no information
# about odds in that year and must be harmless, not divided by zero.
fixed=m.M.Block("A::2020",0,0,3,3)
add=m.YearAdjustedProject("A",[b1,b2,fixed])
assert add.lo==3 and add.hi==5 and add.y1==4
assert abs(add.expectation(0)-4)<1e-12
print("PASS year-conditioned exact homogeneity synthetic tests")
