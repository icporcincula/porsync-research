"""Compare E03 profiles with contract-clustered intervals and quote diagnostics."""

from collections import Counter
import json

import numpy as np

from e03_replicate import OUTPUT, PROFILES, key, rows, run, score


def cluster_ci(delta, titles):
    _, groups = np.unique(titles, return_inverse=True)
    count = np.bincount(groups)
    total = np.bincount(groups, weights=delta)
    draws = np.random.default_rng(0).integers(len(count), size=(10_000, len(count)))
    estimates = total[draws].sum(axis=1) / count[draws].sum(axis=1)
    return [float(np.mean(delta)), *np.quantile(estimates, [0.025, 0.975]).tolist()]


def evaluate(directory, sample, chunks):
    score.OUT = directory
    raw = {arm: score.load(arm) for arm in run.P.ARMS}
    keys = [key(row) for row in sample]
    if any(list(data) != keys for data in raw.values()):
        raise ValueError(f"Incomplete or reordered generations: {directory}")
    answers = {arm: score.answers(arm, raw["F2" if arm == "F3" else arm], chunks)
               for arm in (*run.P.ARMS, "F3")}
    gold = {key(row): row["gold"] for row in sample}
    absent = [key(row) for row in sample if not row["present"]]
    present = [key(row) for row in sample if row["present"]]
    metrics = {}
    for arm, data in answers.items():
        invented = [data[k]["value"] is not None for k in absent]
        recalled = [data[k]["value"] is not None and score.overlap(data[k]["value"], gold[k]) for k in present]
        metrics[arm] = (np.array(invented, dtype=int), np.array(recalled, dtype=int))
    comparisons = {}
    for arm, reference in (("F1", "F0"), ("F2", "F0"), ("F3", "F0"), ("F3", "F2")):
        comparisons[f"{arm}_vs_{reference}"] = {
            metric: cluster_ci(metrics[arm][i] - metrics[reference][i], [chunks[k[1]]["title"] for k in cohort])
            for i, (metric, cohort) in enumerate((("invention", absent), ("recall", present)))
        }

    quote_counts = Counter()
    surviving = []
    for k, reply in raw["F2"].items():
        parsed = run.P.parse("F2", reply["raw"])
        if run.P.is_null(parsed["value"]):
            continue
        cohort = "present" if gold[k] else "absent"
        quote_counts[f"{cohort}_non_null"] += 1
        if answers["F3"][k]["value"] is None:
            continue
        quote_counts[f"{cohort}_quote_pass"] += 1
        quote = score.norm(parsed["evidence"])
        if gold[k] and any(score.norm(span) in quote for span in gold[k]):
            quote_counts["present_quote_contains_gold_span"] += 1
        if not gold[k]:
            surviving.append({"field": k[0], "chunk": k[1], "value": parsed["value"],
                              "evidence": parsed["evidence"]})

    return {
        "clustered_deltas": comparisons,
        "quote_counts": dict(quote_counts),
        "absent_non_null_with_valid_quote": surviving,
        "finish_reasons": {arm: dict(Counter(row["finish"] for row in data.values())) for arm, data in raw.items()},
        "max_prompt_tokens": {arm: max(row["prompt_tokens"] or 0 for row in data.values())
                              for arm, data in raw.items()},
        "total_generation_seconds": {arm: round(sum(row["total_s"] for row in data.values()), 1)
                                     for arm, data in raw.items()},
    }


def main():
    sample = rows(run.OUT / "sample.jsonl")
    chunks = rows(run.CHUNKS)
    directories = {"qwen35-9b-original": run.OUT, **{p: OUTPUT / p for p in PROFILES}}
    result = {profile: evaluate(directory, sample, chunks) for profile, directory in directories.items()}
    (OUTPUT / "diagnostics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
