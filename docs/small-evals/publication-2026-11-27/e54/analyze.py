"""E54 offline analyzer (standard library plus the pinned E52 helpers). Private.

Arms: C = production Inkling (control), CB = Inkling with the E53 per-request reasoning budget, B = Bonsai (candidate).
The frozen decision compares B with C only. CB comparisons are reported as labelled supplements and never change the decision.
Usage: python scripts/e54_analyze.py [--rows-dir tmp/e54] [--out tmp/e54/summary.json]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
_spec = importlib.util.spec_from_file_location("e52_analyze", Path(__file__).resolve().parent.parent / "e52" / "analyze.py")
A52 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A52)

SEED = 5252
RESAMPLES = 10000
EXPECTED_PER_ARM = 72
MARGIN = -0.10
BUDGET_CODES = {"truncation", "output_budget", "timeout"}
SERVING_CODES = {"server_error", "oom"}
ARMS = ("C", "CB", "B")


def pair_bootstrap(rows, cand, ctrl, seed=SEED, resamples=RESAMPLES):
    tasks = sorted({r["task_id"] for r in rows})
    by = {t: {cand: [], ctrl: []} for t in tasks}
    for r in rows:
        if r["arm"] in (cand, ctrl):
            by[r["task_id"]][r["arm"]].append((1 if r["success"] else 0, r["task_seconds"]))
    rng = random.Random(seed)
    diffs, ratios, skipped = [], [], 0
    for _ in range(resamples):
        pick = [tasks[rng.randrange(len(tasks))] for _ in tasks]
        sums = {}
        for arm in (cand, ctrl):
            ok = n = 0
            secs = 0.0
            for t in pick:
                for s, sec in by[t][arm]:
                    ok += s
                    n += 1
                    secs += sec
            sums[arm] = (ok, n, secs)
        if sums[cand][1] == 0 or sums[ctrl][1] == 0:
            skipped += 1
            continue
        diffs.append(sums[cand][0] / sums[cand][1] - sums[ctrl][0] / sums[ctrl][1])
        tp = {a: (3600 * sums[a][0] / sums[a][2]) if sums[a][2] > 0 else 0.0 for a in sums}
        if tp[ctrl] > 0 and tp[cand] > 0:
            ratios.append(tp[cand] / tp[ctrl])
        else:
            skipped += 1
    return {"accuracy_diff_ci95": A52.percentile_ci(diffs), "ratio_ci95": A52.percentile_ci(ratios), "resamples": resamples,
            "undefined_ratio_resamples": skipped, "seed": seed}


def compare(rows, cand, ctrl, stats):
    sc, sk = stats[ctrl], stats[cand]
    boot = pair_bootstrap([r for r in rows if r["arm"] in (cand, ctrl)], cand, ctrl)
    ratio = (sk["verified_per_hour"] / sc["verified_per_hour"]) if sc["verified_per_hour"] and sk["verified_per_hour"] else None
    return {"accuracy_diff": round(sk["rate"] - sc["rate"], 4), "throughput_ratio": ratio, "ratio_defined": ratio is not None, "bootstrap": boot}


def analyze(rows, stops=None):
    by_arm = {a: [r for r in rows if r["arm"] == a] for a in ARMS}
    stats = {a: A52.arm_stats(by_arm[a]) for a in ARMS}
    out = {"arms": stats}
    stops = stops or {}
    stopped_early = [b for b, s in stops.items() if s != "completed"]
    primary_complete = len(by_arm["C"]) == EXPECTED_PER_ARM and len(by_arm["B"]) == EXPECTED_PER_ARM and not stopped_early
    out["complete"] = primary_complete
    out["budget_arm_complete"] = len(by_arm["CB"]) == EXPECTED_PER_ARM
    out["stopped_blocks"] = stopped_early
    out["comparison_B_vs_C"] = None
    out["supplement_CB_vs_C"] = None
    out["supplement_B_vs_CB"] = None
    out["decision"] = "incomplete"
    if not primary_complete:
        return out
    cmp_bc = compare(rows, "B", "C", stats)
    out["comparison_B_vs_C"] = cmp_bc
    if out["budget_arm_complete"]:
        out["supplement_CB_vs_C"] = compare(rows, "CB", "C", stats)
        out["supplement_B_vs_CB"] = compare(rows, "B", "CB", stats)
    sc, sb = stats["C"], stats["B"]
    boot = cmp_bc["bootstrap"]
    d_lo = (boot["accuracy_diff_ci95"] or [None])[0]
    r_lo = (boot["ratio_ci95"] or [None])[0]
    acc_ok = d_lo is not None and d_lo > MARGIN
    speed_ok = r_lo is not None and r_lo > 1.0
    violations = sum(stats[a]["boundary_violations"] for a in ARMS)
    serving = sum(stats[a]["failure_codes"].get(c, 0) for a in ARMS for c in SERVING_CODES)
    attempts = sum(stats[a]["n"] for a in ARMS)
    b_fail = sb["n"] - sb["success"]
    budget_share = (sum(sb["failure_codes"].get(c, 0) for c in BUDGET_CODES) / b_fail) if b_fail else 0.0
    ceiling = (sc["rate"] >= 0.95 and sb["rate"] >= 0.95) or (sc["rate"] <= 0.05 and sb["rate"] <= 0.05)
    out["checks"] = {"accuracy_diff_lower_above_minus_0.10": bool(acc_ok), "ratio_lower_above_1": bool(speed_ok),
                     "no_boundary_violation": violations == 0, "serving_error_attempts": serving, "both_at_ceiling_or_floor": ceiling,
                     "B_budget_failure_share": round(budget_share, 4)}
    if violations:
        out["decision"] = "blocked_by_boundary_violation"
    elif serving > 0.10 * attempts:
        out["decision"] = "serving_failure"
    elif ceiling:
        out["decision"] = "inconclusive"
    elif acc_ok and speed_ok:
        out["decision"] = "advance"
    elif acc_ok and not speed_ok:
        out["decision"] = "inconclusive"
    elif budget_share >= 0.5:
        out["decision"] = "budget_failed"
    else:
        out["decision"] = "not_advance"
    return out


def load_rows(rows_dir: Path):
    rows = []
    for p in sorted(rows_dir.glob("rows-b*-*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    stops = {}
    for p in sorted(rows_dir.glob("stop-b*.json")):
        stops[p.stem.replace("stop-", "")] = json.loads(p.read_text()).get("reason")
    return rows, stops


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-dir", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rows, stops = load_rows(Path(a.rows_dir))
    res = analyze(rows, stops)
    text = json.dumps(res, indent=2)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(text)
