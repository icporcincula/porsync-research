"""E55 scorer and frozen reading rule.

    python scripts/e55_analyze.py --rows tmp/e55/run/rows.jsonl \
        --labels tmp/e55/sample/labels.json --manifest tmp/e55/sample/manifest.json \
        [--throughput tmp/e55/run/throughput.json] --out tmp/e55/summary.json

Arms: A = LiteParse + Tesseract (vendor baseline), B = LiteParse + ocria-nano.
All scoring is deterministic string matching against human labels; no model judge.
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path
from statistics import median

SEED = 55
BOOT = 10000
MARGIN = -0.10  # noninferiority margin on B-A for the per-class primary metric (as in E54)
CEILING, FLOOR = 0.98, 0.02
FAIL_LIMIT = 0.10
CLEAN = ("receipt", "form", "invoice")
AMOUNT_FIELDS = ("total", "subtotal", "tax")
SIGNATURE_MIN_WORDS = 10
AMOUNT_RE = re.compile(r"\d{1,3}(?:[.,]\d{3})+|\d+[.,]\d{2}\b")


# ---------- normalization and matching ----------

def digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def number_tokens(text: str) -> set[str]:
    toks = re.findall(r"\d[\d.,]*", text or "")
    return {digits(t) for t in toks if digits(t)}


def amount_hit(gt: str, text: str) -> bool:
    g = digits(gt)
    return bool(g) and g in number_tokens(text)


def nif_hit(gt: str, text: str) -> bool:
    g = digits(gt)
    if not g:
        return False
    # the id's digits, optionally split by single spaces, not embedded in a longer digit run
    pat = r"(?<!\d)" + r" ?".join(g) + r"(?!\d)"
    return re.search(pat, text or "") is not None


def field_hit(name: str, gt: str, text: str) -> bool:
    return nif_hit(gt, text) if name == "nif_seller" else amount_hit(gt, text)


def words(s: str) -> list[str]:
    out = []
    for w in (s or "").split():
        w = re.sub(r"^\W+|\W+$", "", w.casefold())
        if w:
            out.append(w)
    return out


def word_f1(gt_words: list[str], text: str) -> float:
    g = Counter(w for x in gt_words for w in words(x))
    p = Counter(words(text))
    if not g or not p:
        return 0.0
    overlap = sum((g & p).values())
    if overlap == 0:
        return 0.0
    prec, rec = overlap / sum(p.values()), overlap / sum(g.values())
    return 2 * prec * rec / (prec + rec)


def triple_eligible(fields: dict) -> bool:
    try:
        sub, tax, tot = (int(digits(fields[k])) for k in ("subtotal", "tax", "total"))
    except (KeyError, ValueError):
        return False
    return sub + tax == tot


def has_amount(text: str) -> bool:
    return bool(AMOUNT_RE.search(text or ""))


def escalation_signature(cls: str, text: str) -> bool:
    if len(words(text)) < SIGNATURE_MIN_WORDS:
        return True
    return cls in ("receipt", "invoice") and not has_amount(text)


# ---------- per-page scoring ----------

def score_page(page: dict, label: dict, text: str) -> dict:
    cls = page.get("src_cls", page["cls"])
    out = {"cls_metric": cls}
    fields = label.get("fields", {})
    if cls in ("receipt", "invoice"):
        hits = {k: field_hit(k, v, text) for k, v in fields.items()}
        out["field_hits"] = hits
        out["primary"] = sum(hits.values()) / len(hits) if hits else None
    if label.get("words"):
        out["word_f1"] = word_f1(label["words"], text)
        if cls == "form":
            out["primary"] = out["word_f1"]
    if cls == "receipt" and triple_eligible(fields):
        out["triple"] = all(field_hit(k, fields[k], text) for k in ("subtotal", "tax", "total"))
    out["signature"] = escalation_signature(cls, text)
    out["n_words"] = len(words(text))
    return out


def primary_failed(s: dict) -> bool:
    p = s.get("primary")
    if p is None:
        return False
    return p < 0.5 if s["cls_metric"] == "form" else p < 1.0


# ---------- statistics ----------

def boot_ci(values: list[float], stat, seed: int = SEED) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    vals = sorted(stat([values[rng.randrange(n)] for _ in range(n)]) for _ in range(BOOT))
    return vals[int(0.025 * BOOT)], vals[int(0.975 * BOOT) - 1]


def mean(v):
    return sum(v) / len(v)


def paired_ratio_ci(pairs: list[tuple[float, float]]) -> dict:
    """ratio of summed times B/A over pages, bootstrap over pages."""
    def stat(ps):
        a = sum(p[0] for p in ps)
        return sum(p[1] for p in ps) / a if a else float("nan")
    lo, hi = boot_ci(pairs, stat)
    return {"ratio_b_over_a": stat(pairs), "lo": lo, "hi": hi}


# ---------- analysis ----------

def analyze(rows: list[dict], labels: dict, manifest: dict, throughput: dict | None = None) -> dict:
    pages = {p["page_id"]: p for p in manifest["pages"]}
    by = {}
    for r in rows:
        by.setdefault(r["page_id"], {})[r["arm"]] = r
    complete = [pid for pid, a in by.items() if "A" in a and "B" in a and pid in pages]
    missing = sorted(set(pages) - set(complete))
    arm_stats = {}
    for arm in "AB":
        rs = [by[pid][arm] for pid in complete]
        arm_stats[arm] = {"pages": len(rs), "errors": sum(1 for r in rs if r["error"]),
                          "empty": sum(1 for r in rs if not (r["text"] or "").strip())}
        arm_stats[arm]["error_rate"] = arm_stats[arm]["errors"] / len(rs) if rs else 1.0

    groups = list(CLEAN) + ["degraded"]
    result = {"missing_pages": missing, "arms": arm_stats, "classes": {}}
    scored = {}
    for pid in complete:
        for arm in "AB":
            scored[(pid, arm)] = score_page(pages[pid], labels[pid], by[pid][arm]["text"] or "")
    for cls in groups:
        pids = [pid for pid in complete if pages[pid]["cls"] == cls]
        if cls == "degraded":
            sub_groups = {}
            for pid in pids:
                sub_groups.setdefault(pages[pid]["src_cls"], []).append(pid)
        else:
            sub_groups = {cls: pids}
        entry = {"n": len(pids), "per_arm": {}, "diff": None, "time": None, "subclass_n": {k: len(v) for k, v in sub_groups.items()}}
        usable = [pid for pid in pids if scored[(pid, "A")].get("primary") is not None]
        entry["n_scored"] = len(usable)
        for arm in "AB":
            prim = [scored[(pid, arm)]["primary"] for pid in usable]
            ms = [by[pid][arm]["ms"] for pid in pids]
            sig = [scored[(pid, arm)]["signature"] for pid in pids]
            fails = [primary_failed(scored[(pid, arm)]) for pid in usable]
            flagged_fail = [scored[(pid, arm)]["signature"] for pid in usable if primary_failed(scored[(pid, arm)])]
            f1 = [scored[(pid, arm)]["word_f1"] for pid in pids if "word_f1" in scored[(pid, arm)]]
            trip = [scored[(pid, arm)]["triple"] for pid in pids if "triple" in scored[(pid, arm)]]
            entry["per_arm"][arm] = {
                "primary_mean": mean(prim) if prim else None,
                "word_f1_mean": mean(f1) if f1 else None,
                "triple_recovered": sum(trip), "triple_eligible": len(trip),
                "ms_median": median(ms) if ms else None, "ms_mean": mean(ms) if ms else None,
                "ms_p90": sorted(ms)[int(0.9 * (len(ms) - 1))] if ms else None,
                "signature_rate": mean(sig) if sig else None,
                "primary_fail_count": sum(fails),
                "signature_sensitivity": (sum(flagged_fail) / len(flagged_fail)) if flagged_fail else None,
                "signature_on_ok_pages": (sum(scored[(pid, arm)]["signature"] for pid in usable if not primary_failed(scored[(pid, arm)]))
                                          / max(1, sum(1 for pid in usable if not primary_failed(scored[(pid, arm)])))) if usable else None,
            }
        if usable:
            diffs = [scored[(pid, "B")]["primary"] - scored[(pid, "A")]["primary"] for pid in usable]
            lo, hi = boot_ci(diffs, mean)
            entry["diff"] = {"b_minus_a": mean(diffs), "lo": lo, "hi": hi}
            a_m, b_m = entry["per_arm"]["A"]["primary_mean"], entry["per_arm"]["B"]["primary_mean"]
            entry["ceiling_floor"] = (a_m >= CEILING and b_m >= CEILING) or (a_m <= FLOOR and b_m <= FLOOR)
        if pids:
            entry["time"] = paired_ratio_ci([(by[pid]["A"]["ms"], by[pid]["B"]["ms"]) for pid in pids])
        result["classes"][cls] = entry

    # overall timing on the clean classes only
    clean_pids = [pid for pid in complete if pages[pid]["cls"] in CLEAN]
    if clean_pids:
        result["time_clean"] = paired_ratio_ci([(by[pid]["A"]["ms"], by[pid]["B"]["ms"]) for pid in clean_pids])
    result["decision"] = decide(result, len(missing))
    if throughput:
        result["throughput_supplement"] = throughput
    return result


def decide(res: dict, n_missing: int) -> dict:
    checks = {}
    complete = n_missing == 0 and all(res["arms"][a]["error_rate"] <= FAIL_LIMIT for a in "AB")
    checks["complete_and_error_rate_ok"] = complete
    t = res.get("time_clean")
    speed_pass = bool(t) and t["hi"] < 1.0
    slower = bool(t) and t["lo"] >= 1.0
    checks["b_faster_upper_bound_below_1"] = speed_pass
    informative, acc = [], {}
    for cls in CLEAN:
        c = res["classes"].get(cls, {})
        if not c.get("diff") or c.get("ceiling_floor"):
            acc[cls] = "uninformative"
            continue
        informative.append(cls)
        acc[cls] = {"noninferior": c["diff"]["lo"] > MARGIN, "clearly_worse": c["diff"]["hi"] < 0}
    checks["accuracy"] = acc
    all_ni = len(informative) >= 2 and all(acc[c]["noninferior"] for c in informative)
    any_worse = any(acc[c]["clearly_worse"] for c in informative)
    if not complete:
        label = "incomplete"
    elif speed_pass and all_ni:
        label = "credible_first_pass"
    elif speed_pass and any_worse:
        label = "faster_but_less_accurate"
    elif slower:
        label = "not_better_than_baseline"
    else:
        label = "inconclusive"
    return {"label": label, "checks": checks, "margin": MARGIN}


def load_jsonl(p: str) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--throughput")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    thr = json.loads(Path(a.throughput).read_text(encoding="utf-8")) if a.throughput and Path(a.throughput).exists() else None
    res = analyze(load_jsonl(a.rows), json.loads(Path(a.labels).read_text(encoding="utf-8")),
                  json.loads(Path(a.manifest).read_text(encoding="utf-8")), thr)
    Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(res["decision"]["label"])


if __name__ == "__main__":
    main()
