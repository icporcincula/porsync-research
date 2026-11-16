"""Derive E09 tables from immutable raw attempts; no model calls."""

import argparse
import json
import math
from collections import Counter
from itertools import combinations

from e09_tools.catalogue import ROOT, execute, prepare, sha
from e09_tools.score import score as frozen_score
from e09_audit import score


def wilson(k, n):
    if not n:
        return None
    z = 1.95996398454
    centre = (k / n + z * z / (2 * n)) / (1 + z * z / n)
    half = (
        z * math.sqrt(k / n * (1 - k / n) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    )
    return [centre - half, centre + half]


def paired(left, right):
    assert left.keys() == right.keys()
    b = sum(left[k] and not right[k] for k in left)
    c = sum(right[k] and not left[k] for k in left)
    n = b + c
    return dict(
        left_only=b,
        right_only=c,
        p=min(1, 2 * sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2**n)
        if n
        else 1,
    )


def failure_format(row):
    content = row["responses"][-1]["choices"][0]["message"].get("content") or ""
    if "<tool_call>" in content:
        return "tool_call_as_text"
    for offset, char in enumerate(content):
        if char != "{":
            continue
        try:
            obj, end = json.JSONDecoder().raw_decode(content[offset:])
        except ValueError:
            continue
        if isinstance(obj, dict) and "answer" in obj and "items" in obj:
            return (
                "json_with_extra_text"
                if content[:offset].strip() or content[offset + end :].strip()
                else "schema_violation"
            )
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="run-20261108-v1")
    args = ap.parse_args()
    dest = ROOT / args.run
    db = prepare()
    tasks = {
        t["id"]: t for t in json.loads((ROOT / "requests.json").read_text("utf-8"))
    }
    rows = [
        json.loads(p.read_text("utf-8")) for p in (dest / "test").glob("*.trace.json")
    ]
    assert len(rows) == 600, f"incomplete: {len(rows)}/600"
    assert {(r["id"], r["arm"]) for r in rows} == {
        (key, arm) for key in tasks for arm in ("T0", "T1", "T2", "T3")
    }
    frozen = json.loads((dest / "test/freeze.json").read_text("utf-8"))
    for key, expected in frozen["files"].items():
        assert sha(ROOT.parents[1] / key) == expected, (
            f"frozen input/source changed: {key}"
        )
    for row in rows:
        assert len(row["calls"]) <= 4 and len(row["responses"]) <= 5
        assert row["messages"][:2] == [
            {"role": "system", "content": frozen["system"]},
            {"role": "user", "content": tasks[row["id"]]["text"]},
        ]
        for call in row["calls"]:
            assert call["result"] == execute(
                db, call["name"], call["arguments"], strict=row["arm"] == "T3"
            ), "tool replay differs"
        try:
            decoded = json.loads(
                row["responses"][-1]["choices"][0]["message"].get("content") or ""
            )
        except ValueError:
            decoded = None
        assert decoded == row["final"], "recorded final differs from raw response"
        assert row["scores"] == frozen_score(tasks[row["id"]], row), (
            "saved scores drifted"
        )
        row["legacy_scores"] = dict(row["scores"])
        row["scores"] = score(tasks[row["id"]], row)
        row["group"] = tasks[row["id"]]["group"]
        s = row["scores"]
        s["claim_or_drop"] = s["false_claim"] or s["silent_drop"]
        s["claim_drop_or_protocol"] = s["claim_or_drop"] or s["protocol_failure"]
    metrics = [
        "valid_final",
        "invented_parameter",
        "false_claim",
        "silent_drop",
        "claim_or_drop",
        "claim_drop_or_protocol",
        "postfilter_correct",
        "task_success",
        "protocol_failure",
    ]
    aggregate = {}
    lines = [
        "# E09 — local tool-filter results",
        "",
        "600 frozen test attempts: 150 requests × four arms, Qwen3.5-9B Q4_K_M, local llama.cpp, one slot, thinking off. No frontier model or subscription. One synthetic catalogue, one deterministic run per arm.",
        "",
        "| Arm | Supported success /50 | Unobservable success /50 | Post-filter success /50 | Invented argument /150 | Invalid final /150 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm in ("T0", "T1", "T2", "T3"):
        selected = [r for r in rows if r["arm"] == arm]
        aggregate[arm] = {}
        for group in ("all", "supported", "unobservable", "postfilter", "unsupported"):
            group_rows = [
                r
                for r in selected
                if group == "all"
                or r["group"] == group
                or (group == "unsupported" and r["group"] != "supported")
            ]
            valid = [r for r in group_rows if r["scores"]["valid_final"]]
            aggregate[arm][group] = dict(
                n=len(group_rows),
                valid_n=len(valid),
                counts={m: sum(r["scores"][m] for r in group_rows) for m in metrics},
                wilson95={
                    m: wilson(sum(r["scores"][m] for r in group_rows), len(group_rows))
                    for m in metrics
                },
                valid_only={
                    m: dict(k=sum(r["scores"][m] for r in valid), n=len(valid))
                    for m in ("false_claim", "silent_drop", "claim_or_drop")
                },
            )
        a = aggregate[arm]
        lines.append(
            f"| {arm} | {a['supported']['counts']['task_success']} | {a['unobservable']['counts']['task_success']} | {a['postfilter']['counts']['postfilter_correct']} | {a['all']['counts']['invented_parameter']} | {a['all']['counts']['protocol_failure']} |"
        )
        a["calls"] = dict(
            total=sum(r["scores"]["tool_calls"] for r in selected),
            invented=sum(r["scores"]["invented_calls"] for r in selected),
            accepted_unknown=sum(
                bool(
                    isinstance(c["arguments"], dict)
                    and set(c["arguments"])
                    - (
                        {"category", "max_price", "min_price", "brand", "in_stock"}
                        if c["name"] == "search_products"
                        else {"id"}
                    )
                )
                and "error" not in c["result"]
                for r in selected
                for c in r["calls"]
            ),
        )
        a["seconds"] = sum(r["seconds"] for r in selected)
        a["protocol_failure_formats"] = dict(
            Counter(
                failure_format(r) for r in selected if r["scores"]["protocol_failure"]
            )
        )
    lines += [
        "",
        "Unsupported requests combine 50 unobservable and 50 post-filterable cases. Claim/drop flags can overlap. Rates below use all 100 requests; invalid finals are listed separately and count in conservative error.",
        "",
        "| Arm | False claim /100 | Silent drop /100 | Claim or drop /100 | Claim/drop/invalid /100 | Valid finals /100 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm, a in aggregate.items():
        c = a["unsupported"]["counts"]
        lines.append(
            f"| {arm} | {c['false_claim']} | {c['silent_drop']} | {c['claim_or_drop']} | {c['claim_drop_or_protocol']} | {a['unsupported']['valid_n']} |"
        )
    comparisons = {}
    for left, right in combinations(("T0", "T1", "T2", "T3"), 2):
        comparisons[f"{left}-{right}"] = {}
        for metric in (
            "invented_parameter",
            "silent_drop",
            "false_claim",
            "task_success",
        ):
            group = "supported" if metric == "task_success" else "unsupported"
            maps = [
                {
                    r["id"]: r["scores"][metric]
                    for r in rows
                    if r["arm"] == arm
                    and (
                        r["group"] == "supported"
                        if group == "supported"
                        else r["group"] != "supported"
                    )
                }
                for arm in (left, right)
            ]
            comparisons[f"{left}-{right}"][metric] = paired(*maps)
    format_comparisons = {
        f"{left}-{right}": paired(
            *[
                {
                    r["id"]: r["scores"]["protocol_failure"]
                    for r in rows
                    if r["arm"] == arm
                }
                for arm in (left, right)
            ]
        )
        for left, right in combinations(("T0", "T1", "T2", "T3"), 2)
    }
    lines += [
        "",
        "| Arm | Tool calls | Calls with invented arguments | Accepted invented arguments | Model-loop seconds |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm, a in aggregate.items():
        c = a["calls"]
        lines.append(
            f"| {arm} | {c['total']} | {c['invented']} | {c['accepted_unknown']} | {a['seconds']:.1f} |"
        )
    baseline = aggregate["T0"]["unsupported"]["counts"]
    h3_base = baseline["silent_drop"]
    hypotheses = dict(
        H1=dict(
            prediction="T0 claim/drop union >=25/100",
            observed=baseline["claim_or_drop"],
            status="met"
            if baseline["claim_or_drop"] >= 25
            else "refuted in this study",
        ),
        H2=dict(
            prediction="T1 reduces invention without reducing drops",
            status="uninformative at zero baseline invention"
            if aggregate["T0"]["unsupported"]["counts"]["invented_parameter"] == 0
            else "see paired exploratory comparisons",
        ),
        H3=dict(
            prediction="T2 halves silent drops",
            status="uninformative at zero baseline drops"
            if h3_base == 0
            else (
                "met"
                if aggregate["T2"]["unsupported"]["counts"]["silent_drop"]
                <= h3_base / 2
                else "refuted in this study"
            ),
        ),
        H4=dict(
            prediction="T3 eliminates invention without changing claims",
            status="report attempted and accepted separately; no equivalence inference",
            comparison=comparisons["T2-T3"],
        ),
        H5=dict(
            prediction="supported success equivalent across arms",
            status="not an equivalence design; report Wilson intervals and all six paired comparisons",
        ),
    )
    lines += [
        "",
        "Wilson 95% intervals, exact paired McNemar comparisons (exploratory, unadjusted), valid-final-only rates, per-call invention, acceptance and runtime are in `summary.json`. No equivalence follows from a non-significant difference. Shared output instructions already tell every arm to acknowledge unverifiable properties; this can make T0 strong. Prose claims are outside the mechanical scorer. T3 rejects unknown parameters but does not constrain model decoding. Generated request templates and a single catalogue limit generalisation.",
        "",
        "Protocol and reproduction: [runner README](../../../e09_tools/README.md). Raw traces and frozen code/input/runtime hashes are in this run directory.",
    ]
    lines += [
        "",
        "Reporting amendment: after the first 34 test traces, an empty-item refusal exposed a false-claim scorer defect. The original metric requires both lack of tool application and lack of satisfying items; the frozen scorer checked only items. `e09_audit.py` restores the tool-evidence branch, with regression tests. Raw stored scores are untouched; `summary.json` preserves the original counts alongside corrected counts. No prompt, request, sampling or tool behaviour changed. This correction was made after seeing an early outcome and is not claimed as preregistered.",
    ]
    summary = dict(
        arms=aggregate,
        comparisons=comparisons,
        posthoc_format_comparisons_all_150=format_comparisons,
        hypotheses=hypotheses,
        traces=600,
        legacy_false_claim={
            a: sum(r["legacy_scores"]["false_claim"] for r in rows if r["arm"] == a)
            for a in aggregate
        },
        audit_sha256=sha(__file__.replace("e09_report.py", "e09_audit.py")),
        reporter_sha256=sha(__file__),
        stop_reasons=dict(Counter(r.get("stop", "normal") for r in rows)),
    )
    (dest / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (dest / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
