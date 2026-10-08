#!/usr/bin/env python3
"""Six-project conditional exact test of FIII versus FV initiation heterogeneity.

The source counts are already expert-corrected in the frozen stage-specific
result. The test conditions on each project's two stage denominators and its
total initiators, so separate project intercepts disappear.

Under a COMMON stage odds ratio theta, K_i (FV initiators) follows Fisher's
noncentral hypergeometric distribution. A parametric bootstrap calibrates the
common-vs-project-specific likelihood ratio, including separated cells.

The SECONDARY finite-sample exact calculation additionally conditions on
sum(K_i). This cancels the nuisance common odds ratio identically and permits
enumeration of every admissible table. No asymptotic chi-square p-value is
needed. Neither test identifies physiology or observation probability.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

SOURCE = Path("results/stage_specific_condition_gate_v1.json")
CONTRACT = Path("analysis/contracts/silvering_stage_project_heterogeneity_exact_v1.json")
OUTPUT = Path("analysis/results/silvering_stage_project_heterogeneity_exact.json")
SEED = 20261008
REPS = 10000


def logadd(a, b):
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def log_choose(n, k):
    if k < 0 or k > n:
        return -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


class Block:
    def __init__(self, project, fiii_n, fiii_yes, fv_n, fv_yes):
        self.project = project
        self.n0 = int(fiii_n)
        self.y0 = int(fiii_yes)
        self.n1 = int(fv_n)
        self.y1 = int(fv_yes)
        self.total = self.y0 + self.y1
        self.lo = max(0, self.total - self.n0)
        self.hi = min(self.n1, self.total)
        self.values = list(range(self.lo, self.hi + 1))
        self.lcombs = [
            log_choose(self.n1, k) + log_choose(self.n0, self.total-k)
            for k in self.values
        ]
        self.sup_logp = {k: self._sup_log_prob(k) for k in self.values}

    def probs(self, theta):
        z = [a + theta * k for a, k in zip(self.lcombs, self.values)]
        largest = max(z)
        x = [math.exp(a-largest) for a in z]
        denom = sum(x)
        p = [v/denom for v in x]
        return p, largest + math.log(denom)

    def expectation(self, theta):
        p, _ = self.probs(theta)
        return sum(x * k for k, x in zip(p, self.values))

    def root_for_k(self, k):
        if k == self.lo:
            return -math.inf
        if k == self.hi:
            return math.inf
        a, b = -50.0, 50.0
        for _ in range(55):
            t = (a+b)/2
            if self.expectation(t) < k:
                a = t
            else:
                b = t
        return (a+b)/2

    def _sup_log_prob(self, k):
        if len(self.values) == 1 or k in (self.lo, self.hi):
            return 0.0  # supremum at log-odds +/- infinity
        t = self.root_for_k(k)
        _, logz = self.probs(t)
        return self.lcombs[k-self.lo] + t*k - logz

    def log_prob(self, k, theta, logz=None):
        if logz is None:
            _, logz = self.probs(theta)
        return self.lcombs[k-self.lo]+theta*k-logz

    def draw(self, theta, rng):
        p, _ = self.probs(theta)
        r = rng.random()
        for k, q in zip(self.values, p):
            r -= q
            if r <= 0:
                return k
        return self.values[-1]

    def summary(self):
        corr_or = ((self.y1+0.5)*(self.n0-self.y0+0.5) /
                   ((self.n1-self.y1+0.5)*(self.y0+0.5)))
        return {
            "project":self.project,
            "FIII":{"n":self.n0,"starts":self.y0,"rate":self.y0/self.n0},
            "FV":{"n":self.n1,"starts":self.y1,"rate":self.y1/self.n1},
            "fv_success_support":[self.lo,self.hi],
            "observed_fv_success_at_boundary":self.y1 in (self.lo,self.hi),
            "haldane_or_fv_vs_fiii_descriptive":corr_or
        }


def fit_common(blocks, counts):
    if len(blocks) != len(counts):
        raise ValueError("count mismatch")
    total = sum(counts)
    if total <= sum(b.lo for b in blocks):
        return -math.inf
    if total >= sum(b.hi for b in blocks):
        return math.inf
    low, high = -50.0, 50.0
    for _ in range(48):
        theta=(low+high)/2
        expected = sum(b.expectation(theta) for b in blocks)
        if expected < total:
            low=theta
        else:
            high=theta
    return (low+high)/2


def deviance(blocks, counts, theta=None):
    if theta is None:
        theta=fit_common(blocks,counts)
    if not math.isfinite(theta):
        raise ValueError("common null MLE separated")
    terms=[]
    for b,k in zip(blocks,counts):
        terms.append(b.sup_logp[k]-b.log_prob(k,theta))
    result=2*sum(terms)
    return max(0.0,result)


def parametric_bootstrap(blocks, obs, theta, n, seed):
    rng=random.Random(seed)
    obs_stat=deviance(blocks,obs,theta)
    more=0
    vals=[]
    for _ in range(n):
        x=[b.draw(theta,rng) for b in blocks]
        stat=deviance(blocks,x)
        vals.append(stat)
        if stat >= obs_stat-1e-10:
            more+=1
    vals.sort()
    return {
        "replicates":n,
        "seed":seed,
        "observed_lr":obs_stat,
        "extreme_replicates":more,
        "p_plus_one":(more+1)/(n+1),
        "null_quantiles":{"50":vals[int(.5*(n-1))],
                          "95":vals[int(.95*(n-1))],
                          "99":vals[int(.99*(n-1))]},
    }


def exact_conditional(blocks, obs, theta):
    """Under common log OR and conditioning on sum FV successes, theta cancels."""
    target=sum(obs)
    lo_suffix=[0]*(len(blocks)+1)
    hi_suffix=[0]*(len(blocks)+1)
    for i in range(len(blocks)-1,-1,-1):
        lo_suffix[i]=lo_suffix[i+1]+blocks[i].lo
        hi_suffix[i]=hi_suffix[i+1]+blocks[i].hi
    obs_stat=deviance(blocks,obs,theta)
    # theta is fixed over *all* joint vectors with the same total FV starts.
    logz=[b.probs(theta)[1] for b in blocks]
    denom=-math.inf
    extreme=-math.inf
    count=0
    extreme_count=0
    witness_max=-math.inf

    def walk(i, subtotal, log_weight, log_alt, log_null):
        nonlocal denom, extreme, count, extreme_count, witness_max
        if i == len(blocks):
            if subtotal != target:
                return
            stat=max(0.0,2*(log_alt-log_null))
            count+=1
            denom=logadd(denom,log_weight)
            witness_max=max(witness_max,stat)
            if stat >= obs_stat-1e-10:
                extreme_count+=1
                extreme=logadd(extreme,log_weight)
            return
        b=blocks[i]
        for k in b.values:
            z=subtotal+k
            if z+lo_suffix[i+1] > target or z+hi_suffix[i+1] < target:
                continue
            weight=b.lcombs[k-b.lo]
            walk(i+1,z,log_weight+weight,log_alt+b.sup_logp[k],
                 log_null+weight+theta*k-logz[i])

    walk(0,0,0.0,0.0,0.0)
    if count==0:
        raise ValueError("conditioning support empty")
    return {
        "total_FV_classified_starts_fixed":target,
        "admissible_joint_vectors":count,
        "extreme_joint_vectors":extreme_count,
        "exact_conditional_p":math.exp(extreme-denom),
        "observed_lr":obs_stat,
        "max_lr_in_support":witness_max,
        "algorithm":"full enumeration, probability-weighted hypergeometric, fixed project margins and fixed grand FV initiators",
        "common_odds_nuisance_cancelled":True
    }


def source_blocks():
    obj=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert obj["n_evaluable_fish"]==575
    one=obj["stage"]["FIII"]["project_details"]
    two=obj["stage"]["FV"]["project_details"]
    if set(one)!=set(two):
        raise ValueError("project lists differ")
    return [
        Block(p,one[p]["fish"],one[p]["initiators"],
              two[p]["fish"],two[p]["initiators"])
        for p in sorted(one)
    ]


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    blocks=source_blocks()
    obs=[b.y1 for b in blocks]
    theta=fit_common(blocks,obs)
    if not math.isfinite(theta):
        raise ValueError("null score model unestimable")
    pb=parametric_bootstrap(blocks,obs,theta,REPS,SEED)
    exact=exact_conditional(blocks,obs,theta)
    if exact["admissible_joint_vectors"]!=156690:
        raise ValueError("expected frozen support changed")
    leave=[]
    for i,b in enumerate(blocks):
        bs=[u for j,u in enumerate(blocks) if j!=i]
        ys=[u.y1 for u in bs]
        t=fit_common(bs,ys)
        exact_minus_one = exact_conditional(bs,ys,t) if math.isfinite(t) else None
        leave.append({
            "excluded":b.project,
            "conditional_common_or":math.exp(t) if math.isfinite(t) else None,
            "heterogeneity_lr":deviance(bs,ys,t) if math.isfinite(t) else None,
            "exact_conditional_p": (
                exact_minus_one["exact_conditional_p"]
                if exact_minus_one is not None else None
            ),
            "admissible_joint_vectors": (
                exact_minus_one["admissible_joint_vectors"]
                if exact_minus_one is not None else None
            )
        })
    result={
        "schema":"azores.silvering_stage_project_heterogeneity_exact.v1",
        "evidence_class":contract["evidence_class"],
        "source":str(SOURCE),
        "contract":str(CONTRACT),
        "stage_contrast":"FV vs FIII telemetry-classified initiation",
        "n_projects":len(blocks),
        "n_FIII":sum(b.n0 for b in blocks),
        "n_FV":sum(b.n1 for b in blocks),
        "common_or_fv_vs_fiii":math.exp(theta),
        "common_log_or":theta,
        "observed_lr":deviance(blocks,obs,theta),
        "project_stage_counts":[b.summary() for b in blocks],
        "parametric_bootstrap":pb,
        "exact_conditioned_on_total_FV_starts":exact,
        "leave_one_project_out":leave,
        "inferential_boundaries":contract["inferential_boundary"]
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
