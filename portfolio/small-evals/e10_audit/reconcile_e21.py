"""Read-only E21 partial-run reconciliation; never import its serving harness."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

def analyze(rows):
    keys = [(r['kv'], r['length'], r['seed'], r['depth']) for r in rows]
    assert len(keys) == len(set(keys)), 'duplicate trials'
    cells = defaultdict(lambda: {'recorded': 0, 'passed': 0, 'planned': 12})
    for kv in ('f16', 'q8_0', 'q4_0'):
        for length in ('32k', '64k', '124k'):
            cells[kv+'/'+length]
    for r in rows:
        assert r['trial_done'] and r['ok'] == (r['code'] in r['answer'])
        assert r['seed'] in (1, 2) and r['depth'] in (.05, .2, .4, .6, .8, .95)
        assert r['kv']+'/'+r['length'] in cells
        cells[r['kv']+'/'+r['length']]['recorded'] += 1
        cells[r['kv']+'/'+r['length']]['passed'] += int(r['ok'])
    return {'recorded': len(rows), 'planned': 108, 'missing': 108-len(rows), 'cells': dict(cells)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('archive', type=Path)
    ap.add_argument('output', type=Path)
    a = ap.parse_args()
    raw = a.archive/'results/stage_b.jsonl'
    rows = [json.loads(x) for x in raw.read_text('utf-8').splitlines() if x.strip()]
    report = {'date': '2026-11-17', **analyze(rows), 'sources': {
        name: hashlib.sha256((a.archive/name).read_bytes()).hexdigest()
        for name in ('results/stage_b.jsonl', 'needle_recall.py', 'results/stage_b.log')},
        'limits': ['Partial grid; no quantized-KV comparisons', 'Code containment is not general QA quality',
                   'Protocol pre-run freeze not independently established', 'Sequential questions reuse cached prefixes'],
        'trials': rows}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('trials','sources')}, indent=2))

if __name__ == '__main__':
    main()
