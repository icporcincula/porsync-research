"""Offline E41 n09-n16 audit; standard library only, never executes trials."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import median

MODELS = ("gptoss", "qwen3coder", "qwen36", "edge0")
ARMS = ("v5", "v6", "aider")
FIXTURES = (
    "n09_rle",
    "n10_ranges",
    "n11_csv",
    "n12_pager",
    "n13_roman",
    "n14_window",
    "n15_suggest",
    "n16_dictdiff",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(root):
    trials, sources = [], {}
    for model in MODELS:
        for arm in ARMS:
            relative = (
                f"{model}/aider/results.jsonl" if arm == "aider" else f"{model}/{arm}"
            )
            path = root / relative
            sources[relative] = digest(path)
            text = path.read_text(encoding="utf-8-sig")
            rows = (
                [json.loads(line) for line in text.splitlines() if line.strip()]
                if arm == "aider"
                else json.loads(text)["rows"]
            )
            for row in rows:
                green = row["green"]
                assert type(green) is bool
                if arm != "aider":
                    assert green == (row["independent_tests"]["returncode"] == 0)
                    assert row["baseline_tests"]["returncode"] != 0
                    # Saved diffs are checked without executing any generated code.
                    assert not any(
                        Path(p).name.startswith("test_") for p in row["files_changed"]
                    )
                else:
                    assert row["test_loop"] is True
                    assert green == ("\nOK\n" in row["test_tail"])
                trials.append(
                    {
                        "model": model,
                        "arm": arm,
                        "fixture": row["fixture"],
                        "repeat": row["run"] + (1 if arm == "aider" else 0),
                        "green": green,
                        "secs": row["secs"],
                        "turns": row.get("turns"),
                        "reason": row.get("reason")
                        or (
                            "passed"
                            if green
                            else "timeout"
                            if row.get("aider_rc") == "timeout"
                            else "unsuccessful_edit"
                        ),
                        "source": relative,
                        "source_sha256": sources[relative],
                    }
                )
    return trials, sources


def analyze(trials):
    expected = {
        (m, a, f, r) for m in MODELS for a in ARMS for f in FIXTURES for r in (1, 2, 3)
    }
    keys = [(r["model"], r["arm"], r["fixture"], r["repeat"]) for r in trials]
    assert len(keys) == len(set(keys)) == len(expected)
    assert set(keys) == expected
    cells = {}
    for model in MODELS:
        for arm in ARMS:
            rows = [r for r in trials if r["model"] == model and r["arm"] == arm]
            assert all(type(r["green"]) is bool and r["secs"] >= 0 for r in rows)
            cells[f"{model}/{arm}"] = {
                "passed": sum(r["green"] for r in rows),
                "total": len(rows),
                "per_fixture": {
                    f: sum(r["green"] for r in rows if r["fixture"] == f)
                    for f in FIXTURES
                },
                "failed_reasons": dict(
                    sorted(Counter(r["reason"] for r in rows if not r["green"]).items())
                ),
                "median_attempt_seconds": round(median(r["secs"] for r in rows), 3),
                "total_attempt_seconds": round(sum(r["secs"] for r in rows), 3),
                "failed_trials": [
                    {k: r[k] for k in ("fixture", "repeat", "reason", "turns")}
                    for r in rows
                    if not r["green"]
                ],
            }
    return {
        "cohort": "E41 blind set 2, n09-n16 only",
        "trials": len(expected),
        "cells": cells,
        "excluded": {},
        "limits": [
            "Eight distinct synthetic tasks, three attempts each",
            "Repeated attempts are not independent task samples",
            "Fixed v5 then v6 then Aider order, no counterbalancing",
            "Whole harness comparison, unequal budgets, no causal format ablation",
            "No model ranking or router promotion; no pooling with n01-n08",
            "Edge0 v5b and gpt-oss recovery were tuned on earlier evidence, not blind",
            "Edge0 completed in a separate post-reboot rerun at unchanged 32768 context",
        ],
    }


def audit_edge0(root):
    """Reconcile saved evidence only; retain hashes, never copy raw content."""
    directory = root / "edge0"
    records = {
        p: json.loads(p.read_text(encoding="utf-8"))
        for p in (directory / "data/runs").glob("*.json")
    }
    used, failures, encodings = [], [], {}
    for arm in ("v5", "v6"):
        out = directory / f"{arm}.out"
        encoding = (
            "utf-16"
            if out.read_bytes()[:2] in (b"\xff\xfe", b"\xfe\xff")
            else "utf-8-sig"
        )
        console = out.read_text(encoding=encoding)
        encodings[f"{arm}.out"] = encoding
        table = (directory / f"{arm}.table.md").read_text(encoding="utf-8-sig")
        rows = json.loads((directory / arm).read_text(encoding="utf-8-sig"))["rows"]
        assert not any(row["reason"] == "execution_error" for row in rows)
        for fixture in FIXTURES:
            cells = next(
                line for line in table.splitlines() if line.startswith(f"| {fixture} |")
            )
            assert cells in console
            assert (
                cells.split("|")[6].strip()
                == f"{sum(r['green'] for r in rows if r['fixture'] == fixture)}/3"
            )
        for row in rows:
            transcript = (
                directory
                / f"{arm}.transcripts"
                / f"{row['fixture']}-{row['run']}.jsonl"
            )
            events = [
                json.loads(line)
                for line in transcript.read_text(encoding="utf-8").splitlines()
            ]
            result = events[-1]
            assert result["event"] == "result"
            matches = [
                (p, record)
                for p, record in records.items()
                if record["transcript_path"] == result["transcript_path"]
            ]
            assert len(matches) == 1
            path, record = matches[0]
            used.append(path)
            assert record["turns"] == row["turns"]
            assert record["status"] == row["status"]
            assert record["reason"] == row["reason"]
            if not row["green"]:
                assert result["applied"] is False
                assert row["attempt_history"][-1]["test_output"].startswith("exit 1")
                tools = [
                    event.get("content", "")
                    for event in events
                    if event.get("role") == "tool"
                ]
                failures.append(
                    {
                        "arm": arm,
                        "fixture": row["fixture"],
                        "repeat": row["run"],
                        "terminal_reason": row["reason"],
                        "stop_warning_events": sum(
                            t.startswith("STOP:") for t in tools
                        ),
                        "tool_error_events": sum(t.startswith("ERROR:") for t in tools),
                        "applied": result["applied"],
                        "independent_test_returncode": row["independent_tests"][
                            "returncode"
                        ],
                    }
                )
    assert len(used) == len(set(used)) == len(records) == 48
    aider = [
        json.loads(line)
        for line in (directory / "aider/results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    failed = [row for row in aider if not row["green"]]
    assert len(failed) == 1
    assert (failed[0]["fixture"], failed[0]["run"], failed[0]["aider_rc"]) == (
        "n14_window",
        1,
        0,
    )
    log = (directory / "aider/logs/n14_window-1.txt").read_text(encoding="utf-8")
    assert "has hit a token limit" in log
    assert "Applied edit" not in log
    evidence = sorted(p for p in directory.rglob("*") if p.is_file())
    return {
        "model": "edge0",
        "expected_attempts": 72,
        "missing": [],
        "duplicates": [],
        "reconciled_patchsmith_records": len(used),
        "console_encodings": encodings,
        "terminal_execution_errors": 0,
        "terminal_request_timeouts": 0,
        "patchsmith_failures": failures,
        "aider_failure": {
            "fixture": "n14_window",
            "repeat": 2,
            "original_repeat": 1,
            "process_returncode": 0,
            "classification": "generation_limit_empty_answer",
            "diagnostic": "Long reasoning, empty answer, token-limit warning; no applied edit marker",
            "limit_caveat": "Aider reports unknown limit 0; not proof of server context exhaustion",
        },
        "source_hashes": {p.relative_to(root).as_posix(): digest(p) for p in evidence},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--root", type=Path, help="Private blind2 input directory")
    mode.add_argument("--trials", type=Path, help="Curated portable trial JSON")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.root:
        trials, sources = extract(args.root)
    else:
        trials = json.loads(args.trials.read_text(encoding="utf-8"))
        sources = None
    summary = analyze(trials)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    if sources is not None:
        (args.out / "edge0-audit.json").write_text(
            json.dumps(audit_edge0(args.root), indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (args.out / "trials.json").write_text(
            json.dumps(trials, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        (args.out / "sources.json").write_text(
            json.dumps(sources, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    for key, cell in summary["cells"].items():
        print(
            key,
            f"{cell['passed']}/{cell['total']}",
            cell["failed_reasons"],
            "median s",
            cell["median_attempt_seconds"],
        )


if __name__ == "__main__":
    main()
