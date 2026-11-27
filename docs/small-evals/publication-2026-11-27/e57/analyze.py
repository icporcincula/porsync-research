"""Private, offline E57 paired task-cluster analysis. Never reads another study's data."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random



SEED = 5757
RESAMPLES = 10000
ARMS = ('C', 'B')
PLAN = [('C', 1), ('B', 1), ('B', 2), ('C', 2)]


def percentile_ci(values):
    if not values:
        return None
    values = sorted(values)
    def percentile(q):
        pos = (len(values) - 1) * q
        lo = int(pos)
        hi = min(lo + 1, len(values) - 1)
        return values[lo] + (values[hi] - values[lo]) * (pos - lo)
    return [percentile(.025), percentile(.975)]


def arm_stats(rows):
    n = len(rows)
    success = sum(bool(r['success']) for r in rows)
    seconds = sum(r['task_seconds'] for r in rows)
    return {'n': n, 'success': success, 'rate': success / n if n else None,
            'task_seconds': seconds, 'verified_per_hour': 3600 * success / seconds if seconds else None,
            'failure_codes': dict(Counter(r['failure_code'] for r in rows)),
            'boundary_violations': sum(r['failure_code'] == 'boundary_violation' for r in rows)}


def pair_bootstrap(rows, seed=SEED, resamples=RESAMPLES):
    tasks = sorted({r['task_id'] for r in rows})
    clusters = []
    for task in tasks:
        values = []
        for arm in ARMS:
            selected = [r for r in rows if r['task_id'] == task and r['arm'] == arm]
            values.extend([sum(r['success'] for r in selected), sum(r['task_seconds'] for r in selected)])
        clusters.append(values)
    rng = random.Random(seed)
    diffs, ratios = [], []
    for _ in range(resamples):
        co = cs = bo = bs = 0
        for _ in tasks:
            c, ct, b, bt = clusters[rng.randrange(len(tasks))]
            co += c
            cs += ct
            bo += b
            bs += bt
        diffs.append((bo - co) / (2 * len(tasks)))
        if co > 0 and bo > 0 and cs > 0 and bs > 0:
            ratios.append((bo / bs) / (co / cs))
    return {'accuracy_diff_ci95': percentile_ci(diffs), 'ratio_ci95': percentile_ci(ratios),
            'undefined_ratio_resamples': resamples - len(ratios), 'resamples': resamples, 'seed': seed}


def analyze(rows, stops, expected_ids=None, resamples=RESAMPLES):
    expected = set(expected_ids if expected_ids is not None else json.loads((Path(__file__).resolve().parent / "configuration.json").read_text())["order_repeat1"])
    keys = [(r['task_id'], r['arm'], r['repeat']) for r in rows]
    wanted = {(t, a, repeat) for t in expected for a in ARMS for repeat in (1, 2)}
    invalid = [r.get('attempt_id', str((r.get('task_id'), r.get('arm'), r.get('repeat')))) for r in rows
               if r.get('arm') not in ARMS or not isinstance(r.get('task_seconds'), (float, int))
               or not math.isfinite(r['task_seconds']) or r['task_seconds'] <= 0
               or not isinstance(r.get('success'), bool)
               or (r['success'] != (r.get('failure_code') == 'success'))
               or r.get('block') not in range(1, 5)
               or (r['arm'], r['repeat']) != PLAN[r['block'] - 1]]
    complete = (set(keys) == wanted and len(keys) == len(wanted) and not invalid
                and stops == {f'b{i}': 'completed' for i in range(1, 5)})
    stats = {a: arm_stats([r for r in rows if r['arm'] == a]) for a in ARMS}
    out = {'complete': complete, 'decision': 'incomplete', 'arms': stats, 'stops': stops,
           'invalid_rows': invalid, 'duplicate_attempts': len(keys) - len(set(keys)),
           'missing_attempts': len(wanted - set(keys))}
    if not complete:
        return out
    boot = pair_bootstrap(rows, resamples=resamples)
    c, b = stats['C'], stats['B']
    out['comparison_B_vs_C'] = {'accuracy_diff': b['rate'] - c['rate'],
                                'throughput_ratio': b['verified_per_hour'] / c['verified_per_hour']
                                if c['verified_per_hour'] and b['verified_per_hour'] else None,
                                'bootstrap': boot}
    discordant = Counter()
    table = []
    for tid in sorted(expected):
        totals = {a: sum(r['success'] for r in rows if r['task_id'] == tid and r['arm'] == a) for a in ARMS}
        discordant['B_more' if totals['B'] > totals['C'] else 'C_more' if totals['C'] > totals['B'] else 'equal'] += 1
        table.append({'task_id': tid, 'B_successes': totals['B'], 'C_successes': totals['C']})
    out['discordant_task_counts'] = dict(discordant)
    out['task_table'] = table
    violations = sum(s['boundary_violations'] for s in stats.values())
    serving = sum(r['failure_code'] in {'server_error', 'oom'} for r in rows)
    bfail = [r for r in rows if r['arm'] == 'B' and not r['success']]
    share = sum(r['failure_code'] in {'timeout', 'output_budget', 'truncation'} for r in bfail) / len(bfail) if bfail else 0
    lo, hi = boot['accuracy_diff_ci95']
    ratio = boot['ratio_ci95']
    acc_ok = lo > -.10
    speed_ok = ratio is not None and ratio[0] > 1
    ceiling = (b['rate'] >= .95 and c['rate'] >= .95) or (b['rate'] <= .05 and c['rate'] <= .05)
    out['checks'] = {'accuracy_noninferior': acc_ok, 'throughput_superior': speed_ok, 'serving_errors': serving,
                     'boundary_violations': violations, 'ceiling_or_floor': ceiling, 'B_budget_failure_share': share}
    if violations:
        decision = 'blocked_by_boundary_violation'
    elif serving > .10 * len(rows):
        decision = 'serving_failure'
    elif ceiling:
        decision = 'inconclusive'
    elif acc_ok and speed_ok:
        decision = 'advance'
    elif acc_ok:
        decision = 'inconclusive'
    elif share >= .5:
        decision = 'budget_failed'
    elif lo < -.10 and hi < 0:
        decision = 'clearly_worse'
    else:
        decision = 'not_advance'
    out['decision'] = decision
    out['clearly_worse_accuracy_check'] = lo < -.10 and hi < 0
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows-dir', default=str(Path(__file__).resolve().parent))
    parser.add_argument('--out')
    args = parser.parse_args()
    root = Path(args.rows_dir)
    rows = [json.loads(line) for path in sorted(root.glob('rows-b*-*.jsonl'))
            for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    stops = {p.stem.replace('stop-', ''): json.loads(p.read_text())['reason'] for p in root.glob('stop-b*.json')}
    result = analyze(rows, stops)
    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
