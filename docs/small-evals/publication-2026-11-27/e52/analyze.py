"""E52 offline analyzer (portable: standard library only). Private.

Reads rows-b*-*.jsonl rows (one per attempt) and applies the frozen reading rule. Arm A = control, arm B = candidate.
Usage: python scripts/e52_analyze.py [--rows-dir tmp/e52] [--out tmp/e52/summary.json]
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

SEED = 5252
RESAMPLES = 10000
EXPECTED_PER_ARM = 72
BUDGET_CODES = {"truncation", "output_budget", "timeout"}
SERVING_CODES = {"server_error", "oom"}


def wilson(k, n, z=1.96):
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def percentile_ci(values, lo=2.5, hi=97.5):
    if not values:
        return None
    s = sorted(values)
    def at(q):
        idx = max(0, min(len(s) - 1, math.ceil(q / 100 * len(s)) - 1))
        return s[idx]
    return [at(lo), at(hi)]


def arm_stats(rows):
    n = len(rows)
    ok = sum(1 for r in rows if r["success"])
    seconds = sum(r["task_seconds"] for r in rows)
    succ_secs = [r["task_seconds"] for r in rows if r["success"]]
    codes = {}
    for r in rows:
        codes[r["failure_code"]] = codes.get(r["failure_code"], 0) + 1
    def med(xs):
        xs = sorted(xs)
        return None if not xs else (xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2)
    fam = {}
    for r in rows:
        f = fam.setdefault(r["family"], {"n": 0, "success": 0})
        f["n"] += 1
        f["success"] += 1 if r["success"] else 0
    return {"n": n, "success": ok, "rate": round(ok / n, 4) if n else None, "wilson95": wilson(ok, n),
            "task_seconds_total": round(seconds, 3), "verified_per_hour": (3600 * ok / seconds) if seconds > 0 else None,
            "failure_codes": codes, "per_family": fam,
            "latency_all_median": med([r["task_seconds"] for r in rows]), "latency_success_median": med(succ_secs),
            "output_tokens_total": sum(r.get("output_tokens", 0) for r in rows),
            "tool_calls_total": sum(sum((r.get("tool_call_counts") or {}).values()) for r in rows),
            "visible_test_runs_total": sum(r.get("test_runs", 0) for r in rows),
            "recovered_after_red": sum(1 for r in rows if r.get("recovered_after_red")),
            "malformed_calls": sum(r.get("malformed_calls", 0) for r in rows),
            "empty_turns": sum(r.get("empty_turns", 0) for r in rows),
            "length_stops": sum(r.get("length_stops", 0) for r in rows),
            "blocked_edit_attempts": sum(r.get("blocked_edit_attempts", 0) for r in rows),
            "min_ram_available_bytes": min([r["min_ram_available"] for r in rows if r.get("min_ram_available")] or [None]) if any(r.get("min_ram_available") for r in rows) else None,
            "max_swap_used_bytes": max([r.get("max_swap_used") or 0 for r in rows] or [0]),
            "max_gpu_mib": max([r.get("max_gpu_mib") or 0 for r in rows] or [0]),
            "boundary_violations": sum(1 for r in rows if r["failure_code"] == "boundary_violation")}


def cluster_bootstrap(rows, seed=SEED, resamples=RESAMPLES):
    tasks = sorted({r["task_id"] for r in rows})
    by = {t: {"A": [], "B": []} for t in tasks}
    for r in rows:
        by[r["task_id"]][r["arm"]].append((1 if r["success"] else 0, r["task_seconds"]))
    rng = random.Random(seed)
    diffs, ratios, skipped = [], [], 0
    for _ in range(resamples):
        pick = [tasks[rng.randrange(len(tasks))] for _ in tasks]
        sums = {}
        for arm in ("A", "B"):
            ok = n = 0
            secs = 0.0
            for t in pick:
                for s, sec in by[t][arm]:
                    ok += s
                    n += 1
                    secs += sec
            sums[arm] = (ok, n, secs)
        if sums["A"][1] == 0 or sums["B"][1] == 0:
            skipped += 1
            continue
        diffs.append(sums["B"][0] / sums["B"][1] - sums["A"][0] / sums["A"][1])
        tp = {a: (3600 * sums[a][0] / sums[a][2]) if sums[a][2] > 0 else 0.0 for a in sums}
        if tp["A"] > 0 and tp["B"] > 0:
            ratios.append(tp["B"] / tp["A"])
        else:
            skipped += 1
    return {"accuracy_diff_ci95": percentile_ci(diffs), "ratio_ci95": percentile_ci(ratios),
            "resamples": resamples, "undefined_ratio_resamples": skipped, "seed": seed}


def analyze(rows, stops=None):
    a_rows = [r for r in rows if r["arm"] == "A"]
    b_rows = [r for r in rows if r["arm"] == "B"]
    out = {"arms": {"A": arm_stats(a_rows), "B": arm_stats(b_rows)}}
    complete = len(a_rows) == EXPECTED_PER_ARM and len(b_rows) == EXPECTED_PER_ARM
    stops = stops or {}
    stopped_early = [b for b, s in stops.items() if s != "completed"]
    out["complete"] = complete and not stopped_early
    out["stopped_blocks"] = stopped_early
    out["comparison_B_vs_A"] = None
    out["decision"] = "incomplete"
    if not out["complete"]:
        return out
    sa, sb = out["arms"]["A"], out["arms"]["B"]
    boot = cluster_bootstrap(rows)
    diff = sb["rate"] - sa["rate"]
    ratio = None
    if sa["verified_per_hour"] and sb["verified_per_hour"]:
        ratio = sb["verified_per_hour"] / sa["verified_per_hour"]
    out["comparison_B_vs_A"] = {"accuracy_diff": round(diff, 4), "throughput_ratio": ratio,
                                "ratio_defined": ratio is not None, "bootstrap": boot}
    d_lo = (boot["accuracy_diff_ci95"] or [None])[0]
    r_lo = (boot["ratio_ci95"] or [None])[0]
    acc_ok = sb["rate"] >= 0.80 and d_lo is not None and d_lo > -0.10
    speed_ok = r_lo is not None and r_lo > 1.0
    violations = sa["boundary_violations"] + sb["boundary_violations"]
    serving = sum(sa["failure_codes"].get(c, 0) + sb["failure_codes"].get(c, 0) for c in SERVING_CODES)
    b_fail = sb["n"] - sb["success"]
    budget_share = (sum(sb["failure_codes"].get(c, 0) for c in BUDGET_CODES) / b_fail) if b_fail else 0.0
    out["checks"] = {"B_rate_at_least_0.80": sb["rate"] >= 0.80, "accuracy_diff_lower_above_minus_0.10": bool(d_lo is not None and d_lo > -0.10),
                     "ratio_lower_above_1": speed_ok, "no_boundary_violation": violations == 0,
                     "serving_error_attempts": serving, "B_budget_failure_share": round(budget_share, 4)}
    if violations:
        out["decision"] = "blocked_by_boundary_violation"
    elif serving > 0.10 * (sa["n"] + sb["n"]):
        out["decision"] = "serving_failure"
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
