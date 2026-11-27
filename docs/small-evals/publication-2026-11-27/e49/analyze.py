"""Portable selected analysis functions; collection and task code omitted."""

import json, math, random, statistics

from pathlib import Path

ARMS = ['llama-iq3', 'strata-sq15-thinking', 'strata-sq15-pristine']

MAX_TOKENS = 4096

CONTEXT = 8192

N_PER_ARM = 48

SPEED_BAR = 1.25

ACC_MARGIN = -0.10

BOOT_N = 10000

BOOT_SEED = 4949

def wilson(k, n):
    if not n:
        return None
    z = 1.959963984540054
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** .5) / den
    return [mid - half, mid + half]

def pct(values, q):
    if not values:
        return None
    s = sorted(values)
    return s[max(0, min(len(s) - 1, int(-(-q * len(s) // 1)) - 1))]

def arm_summary(rows):
    n = len(rows)
    k = sum(r['correct'] for r in rows)
    sec = sum(r['seconds'] for r in rows)
    toks = [r['completion_tokens'] for r in rows if r.get('completion_tokens') is not None]
    fam = {}
    for r in rows:
        f = fam.setdefault(r['family'], dict(n=0, correct=0))
        f['n'] += 1
        f['correct'] += r['correct']
    blocks = {}
    for r in rows:
        b = blocks.setdefault(str(r['block']), dict(n=0, correct=0, seconds=0.0))
        b['n'] += 1
        b['correct'] += r['correct']
        b['seconds'] += r['seconds']
    return dict(n=n, correct=k, accuracy=k / n if n else None, wilson95=wilson(k, n), seconds=sec,
                correct_per_hour=k / sec * 3600 if sec else None,
                errors=sum(bool(r.get('error')) for r in rows),
                length_stops=sum(r.get('finish_reason') == 'length' for r in rows),
                median_completion_tokens=statistics.median(toks) if toks else None,
                p90_completion_tokens=pct(toks, 0.9), per_family=fam, per_block=blocks,
                complete=n == N_PER_ARM)

def bootstrap(rows_a, rows_b):
    items = sorted({r['id'] for r in rows_a})
    def agg(rows):
        d = {}
        for r in rows:
            c, s, n = d.get(r['id'], (0, 0.0, 0))
            d[r['id']] = (c + r['correct'], s + r['seconds'], n + 1)
        return d
    A, B = agg(rows_a), agg(rows_b)
    rng = random.Random(BOOT_SEED)
    ratios, diffs, skipped = [], [], 0
    for _ in range(BOOT_N):
        pick = [items[rng.randrange(len(items))] for _ in items]
        ca = sum(A[i][0] for i in pick); sa = sum(A[i][1] for i in pick); na = sum(A[i][2] for i in pick)
        cb = sum(B[i][0] for i in pick); sb = sum(B[i][1] for i in pick); nb = sum(B[i][2] for i in pick)
        diffs.append(cb / nb - ca / na)
        if ca == 0 or sa == 0 or sb == 0:
            skipped += 1
            continue
        ratios.append((cb / sb) / (ca / sa))
    def ci(v):
        v = sorted(v)
        return [v[int(0.025 * len(v))], v[min(len(v) - 1, int(0.975 * len(v)))]] if v else None
    return dict(ratio_ci95=ci(ratios), accuracy_diff_ci95=ci(diffs), skipped_resamples=skipped)

def analyze(rows):
    by = {a: [r for r in rows if r['arm'] == a] for a in ARMS}
    out = dict(arms={a: arm_summary(v) for a, v in by.items() if v})
    A, B = by['llama-iq3'], by['strata-sq15-thinking']
    if len(A) == N_PER_ARM and len(B) == N_PER_ARM:
        sa, sb = out['arms']['llama-iq3'], out['arms']['strata-sq15-thinking']
        ratio = sb['correct_per_hour'] / sa['correct_per_hour'] if sa['correct_per_hour'] else None
        diff = sb['accuracy'] - sa['accuracy']
        boot = bootstrap(A, B)
        h1 = ratio is not None and ratio >= SPEED_BAR
        h2 = diff >= ACC_MARGIN
        lower = boot['ratio_ci95'][0] if boot['ratio_ci95'] else None
        out['comparison_B_vs_A'] = dict(speed_ratio=ratio, accuracy_diff=diff, bootstrap=boot, H1=h1, H2=h2,
                                        ratio_lower_bound_above_1=bool(lower is not None and lower > 1.0),
                                        promising_again=bool(h1 and h2 and lower is not None and lower > 1.0))
    else:
        out['comparison_B_vs_A'] = 'unavailable: arms A and B must both finish all 48 samples'
    return out

if __name__ == '__main__':
    root=Path(__file__).resolve().parent
    actual=analyze(json.loads((root/'trials.json').read_text()))
    expected=json.loads((root/'summary.json').read_text())
    assert actual == expected, 'summary mismatch'
    print('E49: saved summary and bootstrap reproduced')
