"""Re-grade original E07/E08/E09/E12-E16 cached answers, entirely offline.

Inputs and current Python sources are hash-inventoried. Gold labels remain the
historical labels; this does not replace a human gold/scorer audit.
"""
import hashlib
import json
from pathlib import Path
import socket
import sys
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
RESULTS = ROOT/'results'
INPUTS = {}

def read(path):
    INPUTS[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text('utf-8'))

def lines(path):
    INPUTS[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return [json.loads(x) for x in path.read_text('utf-8').splitlines() if x.strip()]

def main():
    def offline(*args, **kwargs):
        raise RuntimeError('Network disabled during regrade')
    socket.socket.connect = offline
    report = {'date': '2026-11-17', 'studies': {}, 'inputs': INPUTS}
    def record(name, observations):
        report['studies'][name] = {'checks': len(observations),
            'mismatches': [{'id': key, 'saved': old, 'current': new} for key, old, new in observations if old != new]}
        print(name, len(observations), 'checks', len(report['studies'][name]['mismatches']), 'mismatches')

    from e07_receipts.checks import score as receipt_score
    tasks = {t['id']: t for t in read(RESULTS/'e07/tasks.json')}
    obs = []
    for p in sorted((RESULTS/'e07/run-v1/test').glob('*.json')):
        row = read(p)
        if 'id' not in row:
            continue
        for label, call in [('base', row)] + [(k, row[k]) for k in ('X2', 'X3') if k in row]:
            obs.append((p.stem+'/'+label, call['scores'], receipt_score(tasks[row['id']]['gold'], call['output'])))
    record('e07', obs)

    from e08_summaries.numbers import verify
    tasks = {t['id']: t for t in read(RESULTS/'e08/tasks.json')}
    obs = []
    for p in sorted((RESULTS/'e08/run-v1/test').glob('*.json')):
        row = read(p)
        if p.stem not in tasks:
            continue
        for arm in ('N0', 'N1', 'N2', 'N3'):
            obs.append((p.stem+'/'+arm, row[arm]['check'], verify(tasks[p.stem], row[arm]['text'])))
    record('e08', obs)

    from e09_tools.score import score as frozen_score
    from e09_audit import score as corrected_score
    tasks = {t['id']: t for t in read(RESULTS/'e09/requests.json')}
    obs, counts = [], defaultdict(lambda: defaultdict(int))
    for p in sorted((RESULTS/'e09/run-20261108-v1/test').glob('*.trace.json')):
        row = read(p)
        obs.append((p.stem, row['scores'], frozen_score(tasks[row['id']], row)))
        new = corrected_score(tasks[row['id']], row)
        for k, v in new.items():
            if isinstance(v, bool):
                counts[row['arm']][k] += int(v)
    record('e09', obs)
    summary = read(RESULTS/'e09/run-20261108-v1/summary.json')
    report['studies']['e09']['corrected_counts'] = dict(counts)
    report['studies']['e09']['corrected_count_mismatches'] = [
        {'arm': a, 'metric': k, 'saved': summary['arms'][a]['all']['counts'][k], 'current': v}
        for a, vals in counts.items() for k, v in vals.items()
        if k in summary['arms'][a]['all']['counts'] and summary['arms'][a]['all']['counts'][k] != v]

    from e12_context_use.build import final_turn
    for name in ('e12', 'e13'):
        obs = []
        for row in lines(RESULTS/name/'9b.f16.jsonl'):
            arm = row['arm'] if name == 'e12' else 'U'
            check = final_turn(row['rule'], row['seed'], arm)[1]
            obs.append(('/'.join(str(row[k]) for k in ('length', 'rule', 'seed', 'arm')), row['ok'], bool(check(row['out']))))
        record(name, obs)

    from e14_compaction import details
    streams = {}
    obs = []
    for row in lines(RESULTS/'e14/9b.f16.jsonl'):
        if row['seed'] not in streams:
            streams[row['seed']] = details.build_stream(row['seed'])
        detail = next(d for d in streams[row['seed']].details if d.kind == row['kind'])
        obs.append((f"{row['seed']}/{row['arm']}/{row['kind']}", row['ok'], bool(detail.check(row['out']))))
    record('e14', obs)

    from e15_rag import corpus
    record('e15', [(f"{r['size']}/{r['arm']}/{r['qid']}", r['ok'], bool(corpus.check(r['out'], r['answer'])))
                   for r in lines(RESULTS/'e15/9b.f16.jsonl')])

    from e16_repo_dict.score import metrics, patch_gold
    obs, counts = [], defaultdict(lambda: [0, 0])
    gold = {}
    for task in read(RESULTS/'e16/local/full-tasks.json'):
        base = RESULTS/'e16/local/sources'/task['base_commit']
        gold[task['instance_id']] = patch_gold(base, task['patch'])
        for name in gold[task['instance_id']]['files']:
            p = base/name
            if p.is_file():
                INPUTS[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    for cohort in ('local-core-overnight-retry-20261110', 'local-seven-full-20261111',
                   'frontier/full-g', 'frontier/full-d', 'frontier/full-ds', 'frontier/full-s',
                   'frontier/rep-g', 'frontier/rep-d'):
        for row in read(RESULTS/'e16'/cohort/'scored.json'):
            new = metrics(gold[row['task']], row['submitted'])
            obs.append((cohort+'/'+row['task']+'/'+row['arm'], row['metrics'], new))
            if new['func_at_5'] is not None:
                counts[cohort+'/'+row['arm']][0] += new['func_at_5']
                counts[cohort+'/'+row['arm']][1] += 1
    record('e16', obs)
    report['studies']['e16']['function_at_5'] = dict(counts)
    report['source_sha256'] = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in ROOT.glob('**/*.py') if 'results' not in p.relative_to(ROOT).parts}
    dest = RESULTS/'e10/cached-replay-2026-11-17/regrade.json'
    dest.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
