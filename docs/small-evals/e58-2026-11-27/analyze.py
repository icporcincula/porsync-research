#!/usr/bin/env python3
"""Public, offline E58x analysis (reads only files in this directory). Original: scripts/e58x_analyze.py.
E58x analysis: task-cluster bootstrap (10,000 resamples, both repeats of a task kept together).

Unit = task; per-task score = mean success over its repeats. Contrasts are computed ONLY on tasks present in both arms:
  P1-A and P2-A on each planner's accepted set; P2-P1 (primary planner comparison) on the intersection of accepted briefs.
Labels: helps (CI lower > 0), hurts (CI upper < 0), else no_detectable_effect.
Also: discordant-task table, cost per verified task (Bonsai task seconds + planner seconds), and validity checks.
Planner token counts are not recorded by the brief generators; only planner wall seconds are available.
"""
from __future__ import annotations

import json, random, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ARMS = ["A", "P1", "P2"]
B = 10000


def load() -> list[dict]:
    rows = []
    for p in sorted(OUT.glob("rows-b*-*.jsonl")):
        rows += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def per_task(rows, arm):
    d = {}
    for r in rows:
        if r["arm"] == arm:
            d.setdefault(r["task_id"], []).append(1.0 if r["success"] else 0.0)
    return {t: sum(v) / len(v) for t, v in d.items()}


def boot(diffs: list[float], seed: int):
    rng, n = random.Random(seed), len(diffs)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return means[int(0.025 * B)], means[int(0.975 * B) - 1]


def label(lo, hi):
    return "helps" if lo > 0 else "hurts" if hi < 0 else "no_detectable_effect"


def contrast(a, b, tasks, seed):
    ids = sorted(t for t in tasks if t in a and t in b)
    diffs = [b[t] - a[t] for t in ids]
    if not ids:
        return None
    lo, hi = boot(diffs, seed)
    return {"n_tasks": len(ids), "mean_a": sum(a[t] for t in ids) / len(ids), "mean_b": sum(b[t] for t in ids) / len(ids),
            "diff": sum(diffs) / len(ids), "ci95": [round(lo, 4), round(hi, 4)], "label": label(lo, hi),
            "b_better": sum(d > 0 for d in diffs), "a_better": sum(d < 0 for d in diffs), "tied": sum(d == 0 for d in diffs),
            "discordant_tasks": {t: [a[t], b[t]] for t in ids if a[t] != b[t]}}


def main() -> int:
    rows = load()
    proto = json.loads((OUT / "configuration.json").read_text())
    man = json.loads((OUT / "briefs-summary.json").read_text())
    pt = {a: per_task(rows, a) for a in ARMS}
    sets = proto["task_sets"]
    inter = sorted(set(sets["P1"]) & set(sets["P2"]))
    res = {"contrasts": {
        "P1_vs_A": contrast(pt["A"], pt["P1"], sets["P1"], 1),
        "P2_vs_A": contrast(pt["A"], pt["P2"], sets["P2"], 2),
        "P2_vs_P1_intersection": contrast(pt["P1"], pt["P2"], inter, 3),
        "P1_vs_A_intersection": contrast(pt["A"], pt["P1"], inter, 4),
        "P2_vs_A_intersection": contrast(pt["A"], pt["P2"], inter, 5)}}
    cost = {}
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a]
        succ = sum(r["success"] for r in rs)
        planner = 0.0 if a == "A" else sum(man[a]["tasks"][t]["accepted"]["seconds"] for t in sets[a])
        secs = sum(r["task_seconds"] for r in rs)
        cost[a] = {"attempts": len(rs), "successes": succ, "bonsai_seconds": round(secs, 1), "planner_seconds_once": round(planner, 1),
                   "sec_per_verified": round((secs + planner) / succ, 1) if succ else None}
    res["cost"] = cost
    exp = {a: len(sets[a]) * 2 for a in ARMS}
    got = {a: sum(1 for r in rows if r["arm"] == a) for a in ARMS}
    srv = {a: sum(1 for r in rows if r["arm"] == a and r["failure_code"] in ("server_error", "oom")) for a in ARMS}
    res["validity"] = {"expected_attempts": exp, "got_attempts": got, "all_complete": exp == got,
                       "boundary_violations": sum(1 for r in rows if r["failure_code"] == "boundary_violation"),
                       "server_error_rate": {a: round(srv[a] / got[a], 3) if got[a] else None for a in ARMS},
                       "server_errors_le_10pct": all(got[a] == 0 or srv[a] / got[a] <= 0.10 for a in ARMS),
                       "failure_codes": {a: {} for a in ARMS}}
    for r in rows:
        fc = res["validity"]["failure_codes"][r["arm"]]
        fc[r["failure_code"]] = fc.get(r["failure_code"], 0) + 1
    (OUT / "summary.json").write_bytes((json.dumps(res, indent=2) + "\n").encode("utf-8"))
    for k, c in res["contrasts"].items():
        if c:
            print(f"{k}: n={c['n_tasks']} {c['mean_a']:.3f} -> {c['mean_b']:.3f} diff {c['diff']:+.3f} CI {c['ci95']} {c['label']} "
                  f"(better {c['b_better']} / worse {c['a_better']} / tied {c['tied']})")
    print(json.dumps(res["cost"]), json.dumps({k: v for k, v in res["validity"].items() if k != "failure_codes"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
