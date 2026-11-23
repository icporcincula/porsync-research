"""Offline E42 aggregate reproduction. Requires Python 3 and NumPy.
No model requests. Correctness labels are taken as supplied, not independently rejudged.
Run: python analyze.py
"""
from pathlib import Path
import json
import numpy as np
DRAWS = 10_000
CAP_S = 300.0
ROOT = Path(__file__).resolve().parent
ARMS = ('9b_llama_wsl', '9b_surogate_wsl')

def read(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip().endswith("}")]


def ci(x) -> list[float]:
    return [round(float(v), 4) for v in np.percentile(x, [50, 2.5, 97.5])]


def prefix_k(order: list[str], finished: list[set[str]]) -> int:
    k = 0
    for i in order:
        if all(i in f for f in finished):
            k += 1
        else:
            break
    return k


def view(rows: dict[str, dict], order: list[str], k: int) -> dict:
    """Common first-k items in queue order: correct vector, types, wall seconds to finish them."""
    sel = [rows[i] for i in order[:k]]
    return {"correct": np.array([r["correct"] for r in sel], float), "type": np.array([r["type"] for r in sel]),
            "wall": max(r["end"] for r in sel) if sel else 0.0}


def cph(v: dict, mask=None) -> float:
    return float(v["correct"].sum() / v["wall"] * 3600) if v["wall"] else 0.0


def paired(a: dict, b: dict, mask: np.ndarray, rng) -> dict:
    """Ratio b/a of correct per hour and accuracy gap b-a (points), bootstrapped over the masked items."""
    n = int(mask.sum())
    if n < 2:
        return {"n": n}
    ca, cb = a["correct"][mask], b["correct"][mask]
    # wall seconds per item, held fixed; a mask restricts items, not the clock
    wa, wb = a["wall"] / len(a["correct"]), b["wall"] / len(b["correct"])
    ra, rb, dif = [], [], []
    for _ in range(DRAWS // 500):
        idx = rng.integers(0, n, size=(500, n))
        sa, sb = ca[idx].sum(1), cb[idx].sum(1)
        ra.append(sa / (n * wa) * 3600)
        rb.append(sb / (n * wb) * 3600)
        dif.append((cb[idx].mean(1) - ca[idx].mean(1)) * 100)
    ra, rb, dif = np.concatenate(ra), np.concatenate(rb), np.concatenate(dif)
    ratio = rb / np.where(ra == 0, np.nan, ra)
    return {"n": n, "cph_a": round(float(ca.sum() / (n * wa) * 3600), 1), "cph_b": round(float(cb.sum() / (n * wb) * 3600), 1),
            "acc_a": round(float(ca.mean()), 4), "acc_b": round(float(cb.mean()), 4),
            "ratio_b_over_a": ci(ratio[~np.isnan(ratio)]), "acc_gap_points_b_minus_a": ci(dif)}


def compare(name_a: str, name_b: str, data: dict, order: list[str], rng, by_type: bool = False) -> dict:
    if not data.get(name_a) or not data.get(name_b):
        return {"missing": [n for n in (name_a, name_b) if not data.get(n)]}
    k = prefix_k(order, [set(data[name_a]), set(data[name_b])])
    a, b = view(data[name_a], order, k), view(data[name_b], order, k)
    out = {"K": k, "a": name_a, "b": name_b, "wall_a_s": round(a["wall"], 1), "wall_b_s": round(b["wall"], 1),
           "headline": paired(a, b, np.ones(k, bool), rng)}
    if by_type:
        out["by_type"] = {t: paired(a, b, a["type"] == t, rng) for t in sorted(set(a["type"]))}
    return out


def latency(rows: list[dict]) -> dict:
    s = np.array([r["secs"] for r in rows], float)
    return {"n": len(rows), "median_s": round(float(np.median(s)), 3), "p95_s": round(float(np.percentile(s, 95)), 3), "max_s": round(float(s.max()), 1),
            "error_share": round(sum(1 for r in rows if r["err"]) / len(rows), 4),
            "empty_share": round(sum(1 for r in rows if not r["reply_nonempty"]) / len(rows), 4),
            "cap_hit_share": round(sum(1 for r in rows if r["secs"] >= CAP_S) / len(rows), 4),
            "length_cut_share": round(sum(1 for r in rows if r.get("finish") == "length") / len(rows), 4)}


def resources(p: Path) -> dict:
    s = read(p)
    return {"peak_vram_mib": max(x["vram_mib"] for x in s), "min_ram_free_mib": min(x["ram_free_mib"] for x in s),
            "max_swap_used_mib": max(x["swap_used_mib"] for x in s)} if s else {}



def probe_summary(p: Path) -> dict:
    rows = [r for r in read(p) if r.get("err") == "" and r.get("ttft_s") is not None]
    if not rows:
        return {}
    ttft = np.array([r["ttft_s"] for r in rows], float)
    tps = np.array([r["decode_tps"] for r in rows if r.get("decode_tps")], float)
    return {
        "n": len(rows),
        "ttft_p50_s": round(float(np.median(ttft)), 3),
        "ttft_p95_s": round(float(np.percentile(ttft, 95)), 3),
        "decode_tps_median": round(float(np.median(tps)), 2) if len(tps) else None,
        "reasoning_leak_rows": sum(
            1 for r in rows if (r.get("reasoning_len") or 0) > 0
        ),
    }



def main():
    for tag in ('', '.rep1'):
        raw = {arm: read(ROOT / f'{arm}{tag}.metrics.jsonl') for arm in ARMS}
        order = [r['id'] for r in raw[ARMS[0]]]
        for arm, rows in raw.items():
            assert len(set(r['id'] for r in rows)) == len(rows)
            assert [r['id'] for r in rows] == order[:len(rows)]
        data = {arm: {r['id']: r for r in rows} for arm, rows in raw.items()}
        actual = compare(*ARMS, data, order, np.random.default_rng(0), by_type=True)
        saved = json.loads((ROOT / f'score{tag}.json').read_text())
        expected = dict(saved['headline'])
        expected.pop('note', None)
        assert actual == expected, ('headline mismatch', tag, actual, expected)
        for arm, rows in raw.items():
            assert latency(rows) == saved['latency'][arm]
            res = json.loads((ROOT / f'{arm}{tag}.resources.json').read_text())
            assert {'peak_vram_mib': max(r['vram_mib'] for r in res),
                    'min_ram_free_mib': min(r['ram_free_mib'] for r in res),
                    'max_swap_used_mib': max(r['swap_used_mib'] for r in res)} == saved['resources'][arm]
            meta = json.loads((ROOT / f'{arm}{tag}.window.json').read_text())
            assert meta['completed'] and meta['arm'] == arm
            assert meta['hours'] == (0.5 if tag else 2) and meta['tag'] == ('rep1' if tag else '')
            assert meta['limit'] == 0 and meta['pool_sha256'] == json.loads((ROOT / 'configuration.json').read_text())['pool_sha256']
            assert meta['elapsed_s'] >= meta['hours'] * 3600
            full = {'items': len(rows), 'correct': sum(r['correct'] for r in rows),
                    'wall_s': round(max(r['end'] for r in rows), 1),
                    'correct_per_hour': round(sum(r['correct'] for r in rows) / max(r['end'] for r in rows) * 3600, 1)}
            if tag:
                full.update(errors=sum(bool(r['err']) for r in rows), reasoning_leak_rows=sum(bool(r['reasoning_len']) for r in rows))
            assert full == saved['full_run'][arm]
            assert not any(r['err'] or r['reasoning_len'] or r['finish'] == 'length' for r in rows)
            if not tag:
                assert probe_summary(ROOT / f'probe.{arm}.cold.jsonl') == saved['probe'][arm]
                assert saved['items_finished'][arm] == len(rows)
                assert saved['reasoning_leak_share'][arm] == 0
        if not tag:
            h = saved['hypotheses']
            ratio = actual['headline']['ratio_b_over_a'][0]
            gap = actual['headline']['acc_gap_points_b_minus_a'][0]
            assert h['H1_loads_at_32k_under_15.5gb']['supported'] is None
            assert h['H2_surogate_ge_1.2x_correct_per_hour'] == {'ratio': ratio, 'supported': ratio >= 1.2}
            assert h['H4_accuracy_within_2_points'] == {'gap_points': gap, 'supported': abs(gap) < 2}
            for key, metric, threshold in [('H3_surogate_ge_1.5x_decode_tps', 'decode_tps_median', 1.5), ('H5_ttft_ratio_under_2x', 'ttft_p50_s', 2)]:
                value = round(saved['probe'][ARMS[1]][metric] / saved['probe'][ARMS[0]][metric], 3)
                assert h[key] == {'ratio': value, 'supported': value >= threshold if threshold == 1.5 else value < threshold}
        print(f"PASS {tag or 'primary'}: {sum(map(len, raw.values()))} rows; K={actual['K']}; ratio={actual['headline']['ratio_b_over_a']}; accuracy, latency, resources, sidecars and secondary probes verified")
    print('Intervals reproduce saved labels and fixed timing; raw answers, log review and inference are not independently reproduced.')

if __name__ == '__main__':
    main()
