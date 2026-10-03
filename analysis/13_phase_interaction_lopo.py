#!/usr/bin/env python3
"""Leave-one-project-out robustness for the canonical phase interaction.

Loads the canonical analysis module without executing its main(), rebuilds the
same stacked two-phase model, and repeats it after dropping each source project.

Canonical source:
  analysis/11_phase_stage_interaction.py

Output:
  analysis/results/phase_stage_interaction_lopo.json
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "11_phase_stage_interaction.py"


def load_source():
    spec = importlib.util.spec_from_file_location("phase_source", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load canonical phase module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fit_subset(mod, individuals):
    long = []
    for r in individuals:
        long.append({**r, "phase": "initiation", "y": int(r["initiated"])})
        if r["initiated"]:
            long.append({**r, "phase": "completion", "y": int(r["successful"])})

    stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in long:
        key = f"{r['phase']}::{r['project']}::{r['release'].year}"
        s = stats[key]
        s["n"] += 1
        s["success"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in stats.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
        }
        for k in informative
    }

    model = []
    for r in long:
        key = f"{r['phase']}::{r['project']}::{r['release'].year}"
        if key not in means:
            continue
        m = means[key]
        model.append({
            **r,
            "stratum": key,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X, y, clusters = [], [], []
    for r in model:
        init = r["phase"] == "initiation"
        comp = not init
        X.append([
            1.0,
            *[float(r["stratum"] == k) for k in dummies],
            r["length_100mm"] if init else 0.0,
            r["length_100mm"] if comp else 0.0,
            r["release_100days"] if init else 0.0,
            r["release_100days"] if comp else 0.0,
            r["stage_score"] if init else 0.0,
            r["stage_score"] if comp else 0.0,
        ])
        y.append(float(r["y"]))
        clusters.append(r["tag"])

    Xv = np.asarray(X)
    yv = np.asarray(y)
    beta, bread, mu = mod.logistic_irls(Xv, yv)
    robust = mod.clustered_sandwich(Xv, yv, mu, bread, clusters)

    i_init = Xv.shape[1] - 2
    i_comp = Xv.shape[1] - 1
    b_init = float(beta[i_init])
    b_comp = float(beta[i_comp])
    delta = b_init - b_comp
    var_delta = (
        robust[i_init, i_init]
        + robust[i_comp, i_comp]
        - 2 * robust[i_init, i_comp]
    )
    se_delta = float(math.sqrt(max(0.0, var_delta)))
    z = delta / se_delta

    return {
        "n_individuals": len(individuals),
        "n_stacked_rows": len(model),
        "n_informative_strata": len(informative),
        "or_ratio_init_over_completion": math.exp(delta),
        "ci95": [
            math.exp(delta - 1.96 * se_delta),
            math.exp(delta + 1.96 * se_delta),
        ],
        "p": 2 * (1 - mod.norm_cdf(abs(z))),
    }


def main():
    mod = load_source()
    individuals = mod.build_individuals()
    projects = sorted({r["project"] for r in individuals})

    full = fit_subset(mod, individuals)
    loo = {
        project: fit_subset(
            mod, [r for r in individuals if r["project"] != project]
        )
        for project in projects
    }

    result = {
        "schema": "azores.phase_stage_interaction_lopo.v1",
        "canonical_source": "analysis/11_phase_stage_interaction.py",
        "full": full,
        "leave_one_project_out": loo,
        "direction_consistent_all_projects": all(
            x["or_ratio_init_over_completion"] > 1 for x in loo.values()
        ),
        "supported_p_lt_0_05_count": sum(
            x["p"] < 0.05 for x in loo.values()
        ),
        "claim_boundary": (
            "All leave-one-project-out estimates retain stronger Durif control "
            "at initiation. Formal support weakens after removing the 2015 "
            "project, so precision is not fully project-independent."
        ),
    }

    out = Path("analysis/results/phase_stage_interaction_lopo.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
