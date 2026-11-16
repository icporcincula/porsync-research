"""Replay all E07 scores and report paired outcomes with the repeat floor."""
import json
from collections import Counter
import numpy as np
from e07_receipts.prepare import ROOT, gold_parse, ocr_text
from e07_receipts.checks import score
from e07_receipts.run import messages
from e08_summaries.runtime import BASE, sha, write


def ci(values):
    a = np.array(values,dtype=float)
    idx = np.random.default_rng(0).integers(0,len(a),(10000,len(a)))
    return {"mean":float(a.mean()),"ci95":np.quantile(a[idx].mean(axis=1),[.025,.975]).tolist()}


def main():
    frozen = json.loads((ROOT / "run-v1/freeze.json").read_text("utf-8"))
    for name,digest in frozen["files"].items():
        assert sha(BASE / name) == digest,name
    tasks = json.loads((ROOT / "tasks.json").read_text("utf-8"))
    data = json.loads((ROOT / "data.json").read_text("utf-8"))
    assert sha(ROOT / "annotations.json") == data["annotations_sha256"]
    annotations = {r["index"]: r["annotation"] for r in json.loads((ROOT / "annotations.json").read_text("utf-8"))}
    for task in tasks:
        assert gold_parse(annotations[task["index"]]) == task["gold"]
        assert ocr_text(annotations[task["index"]]) == task["text"]
    paths = list((ROOT / "run-v1/test").glob("*.json"))
    assert len(paths) == 4 * len(tasks)
    traces = {(x["id"],x["arm"]):x for p in paths for x in [json.loads(p.read_text("utf-8"))]}
    assert set(traces) == {(t["id"],a) for t in tasks for a in ("X0A","X0B","X0C","X1")}
    arms = {a:[] for a in ("X0A","X0B","X0C","X1","X2","X3")}
    finishes = Counter()
    seconds,calls = 0,0
    for task in tasks:
        for arm in ("X0A","X0B","X0C","X1"):
            trace = traces[task["id"],arm]
            assert trace["request"]["messages"] == messages(task,arm)
            for call in [trace] + ([trace["X3"]] if arm == "X0A" and trace["X3"]["reasked"] else []):
                raw = call["response"]["choices"][0]
                assert raw["message"]["content"] == call["text"]
                try:
                    output = json.loads(call["text"])
                except ValueError:
                    output = None
                assert output == call["output"]
                assert score(task["gold"],output) == call["scores"]
                finishes[raw["finish_reason"]] += 1
                calls += 1
                seconds += call["seconds"]
            arms[arm].append(trace["scores"])
        first = traces[task["id"],"X0A"]
        assert first["X2"]["output"] == first["output"]
        assert score(task["gold"],first["X2"]["output"]) == first["X2"]["scores"]
        assert score(task["gold"],first["X3"]["output"]) == first["X3"]["scores"]
        arms["X2"].append(first["X2"]["scores"])
        arms["X3"].append(first["X3"]["scores"])
    summary = {"receipts":len(tasks),"model_calls":calls,"generation_seconds":seconds,"finish_reasons":dict(finishes),"arms":{}}
    for arm,rows in arms.items():
        wrong = [r for r in rows if not r["total_correct"]]
        summary["arms"][arm] = {"invalid":sum(not r["valid"] for r in rows),"contradictions":sum(r["contradiction"] for r in rows),"flagged":sum(r["flagged"] for r in rows),"total_correct":sum(r["total_correct"] for r in rows),"subtotal_correct":sum(r["subtotal_correct"] for r in rows),"item_f1_macro":sum(r["item_f1"] for r in rows)/len(rows),"known_count_matches":sum(r["known_count_matches"] for r in rows),"known_count_total":sum(r["known_count_total"] for r in rows),"wrong_totals":len(wrong),"wrong_totals_flagged":sum(r["flagged"] for r in wrong),"wrong_totals_valid_consistent":sum(r["valid"] and not r["flagged"] for r in wrong)}
    summary["X1_minus_X0A_contradiction"] = ci([int(b["contradiction"])-int(a["contradiction"]) for a,b in zip(arms["X0A"],arms["X1"])])
    summary["X3_minus_X0A_total_accuracy"] = ci([int(b["total_correct"])-int(a["total_correct"]) for a,b in zip(arms["X0A"],arms["X3"])])
    summary["repair"] = {"reasked":sum(traces[t["id"],"X0A"]["X3"]["reasked"] for t in tasks),"total_fixes":sum(not a["total_correct"] and b["total_correct"] for a,b in zip(arms["X0A"],arms["X3"])),"total_breakages":sum(a["total_correct"] and not b["total_correct"] for a,b in zip(arms["X0A"],arms["X3"]))}
    summary["floor"] = {repeat:{"parsed_output_changes":sum(traces[t["id"],"X0A"]["output"] != traces[t["id"],repeat]["output"] for t in tasks),"raw_text_changes":sum(traces[t["id"],"X0A"]["text"] != traces[t["id"],repeat]["text"] for t in tasks)} for repeat in ("X0B","X0C")}
    summary["instruction_raw_output_changes"] = sum(traces[t["id"],"X0A"]["text"] != traces[t["id"],"X1"]["text"] for t in tasks)
    summary["instruction_parsed_output_changes"] = sum(traces[t["id"],"X0A"]["output"] != traces[t["id"],"X1"]["output"] for t in tasks)
    # Post-run descriptive charge-field checks, separate from frozen primary metrics.
    summary["posthoc_charge_accuracy"] = {}
    for arm in ("X0A","X1","X3"):
        outputs = [traces[t["id"],"X0A"]["X3"]["output"] if arm == "X3" else traces[t["id"],arm]["output"] for t in tasks]
        summary["posthoc_charge_accuracy"][arm] = {k:sum(isinstance(o,dict) and o.get(k) == t["gold"][k] for t,o in zip(tasks,outputs)) for k in ("tax","service")}
    # Enumerate all errors and repairs for transparent case-by-case review.
    audit = [{"task":t,"baseline":traces[t["id"],"X0A"],"instruction":traces[t["id"],"X1"]} for t in tasks if any(not traces[t["id"],a]["scores"]["total_correct"] or traces[t["id"],a]["scores"]["flagged"] or traces[t["id"],a]["scores"]["item_f1"] < 1 or any(traces[t["id"],a]["output"].get(k) != t["gold"][k] for k in ("tax","service")) for a in ("X0A","X1"))]
    write(ROOT / "audit-cases.json",audit)
    write(ROOT / "summary.json",summary)
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
