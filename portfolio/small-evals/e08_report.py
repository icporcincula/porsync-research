"""Post-freeze aggregation, reproducibility validation and audit sampling."""
import json
import random
import re
from collections import Counter
import numpy as np
from e08_summaries.prepare import ROOT
from e08_summaries.numbers import verify
from e08_summaries.runtime import BASE, sha, write
from e08_summaries.run import prompt, fallback


def direction(task, text):
    findings = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        for indicator, series in task["values"].items():
            fuel = indicator.split()[0].lower()
            if fuel not in sentence.lower():
                continue
            # Heuristic only: endpoint direction, excludes sentences referring to interior dates.
            dates = set(map(int, re.findall(r"\b(?:19|20)\d{2}\b", sentence)))
            if dates and dates != {task["years"][0], task["years"][-1]}:
                continue
            signs = []
            if re.search(r"\b(rose|increased|grew|rising|increase)\b", sentence, re.I):
                signs.append(1)
            if re.search(r"\b(fell|declined|decreased|falling|decrease)\b", sentence, re.I):
                signs.append(-1)
            expected = (series[-1] > series[0]) - (series[-1] < series[0])
            if len(signs) == 1 and signs[0] != expected:
                findings.append({"indicator": indicator, "sentence": sentence, "endpoint_sign": expected})
    return findings


def cluster_ci(tasks, values):
    countries = sorted({t["country"] for t in tasks})
    buckets = [[v for t, v in zip(tasks, values) if t["country"] == c] for c in countries]
    sums = np.array([sum(b) for b in buckets])
    counts = np.array([len(b) for b in buckets])
    idx = np.random.default_rng(0).integers(0, len(countries), (10000, len(countries)))
    means = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
    return {"difference": float(np.mean(values)), "ci95": np.quantile(means, [.025,.975]).tolist(), "method": "paired country-cluster bootstrap, 10000 draws, seed 0"}


def main():
    frozen = json.loads((ROOT / "run-v1/freeze.json").read_text("utf-8"))
    for name, digest in frozen["files"].items():
        assert sha(BASE / name) == digest, name
    tasks = json.loads((ROOT / "tasks.json").read_text("utf-8"))
    traces = {p.stem: json.loads(p.read_text("utf-8")) for p in (ROOT / "run-v1/test").glob("*.json")}
    assert set(traces) == {t["id"] for t in tasks}
    summary = {"n": len(tasks), "countries": len({t['country'] for t in tasks}), "arms": {}, "finish_reasons": Counter(), "generation_seconds": 0, "model_calls": 0}
    flags, passed, directions = [], [], []
    for arm in ("N0", "N1", "N2", "N3"):
        rows = []
        for task in tasks:
            trace = traces[task["id"]]
            row = trace[arm]
            check = verify(task, row["text"])
            assert check == row["check"]
            rows.append(check)
            if arm in ("N0", "N1"):
                assert row["request"]["messages"] == prompt(task,arm)
                for call in [row] + ([trace["repair"]] if arm == "N1" and "repair" in trace else []):
                    assert call["text"] == call["response"]["choices"][0]["message"]["content"]
                    summary["finish_reasons"][call["response"]["choices"][0]["finish_reason"]] += 1
                    summary["generation_seconds"] += call["seconds"]
                    summary["model_calls"] += 1
                flags.extend({"id": task["id"], "arm": arm, "number": n, "text": row["text"], "task": task} for n in check["unsupported"])
                if not check["flagged"]:
                    passed.append({"id": task["id"], "arm": arm, "text": row["text"], "task": task})
                directions.extend({"id": task["id"], "arm": arm, "task": task, **d} for d in direction(task, row["text"]))
            else:
                initial = trace["N1"]
                if arm == "N2":
                    expected = fallback(task) if initial["check"]["flagged"] else initial["text"]
                else:
                    assert ("repair" in trace) == initial["check"]["flagged"]
                    revised = trace.get("repair",initial)
                    expected = fallback(task) if revised["check"]["flagged"] else revised["text"]
                assert row["text"] == expected
        summary["arms"][arm] = {"flagged_summaries": sum(r["flagged"] for r in rows), "numbers": sum(len(r["numbers"]) for r in rows), "unsupported_numbers": sum(len(r["unsupported"]) for r in rows), "fallbacks": sum(traces[t["id"]][arm].get("fallback", False) for t in tasks)}
    summary["N1_minus_N0_flag_rate"] = cluster_ci(tasks, [int(traces[t["id"]]["N1"]["check"]["flagged"]) - int(traces[t["id"]]["N0"]["check"]["flagged"]) for t in tasks])
    rng = random.Random(1808)
    write(ROOT / "audit-sample.json", {"flagged_numbers": rng.sample(flags, min(50,len(flags))), "passed_summaries": rng.sample(passed, min(50,len(passed))), "direction_flags": directions})
    write(ROOT / "summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
