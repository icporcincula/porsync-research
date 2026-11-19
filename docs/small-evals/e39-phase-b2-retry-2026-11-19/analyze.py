import json, statistics
from pathlib import Path
METRICS=('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens', 'turns', 'secs')
NAMES=('bug1', 'bug2', 'feature', 'multifile', 'refactor', 'offbyone', 'javascript')
def aggregate(rows):
    groups = []
    for name in NAMES:
        cell = [r for r in rows if r['name'] == name]
        accepted = [r for r in cell if r['green']]
        metrics = {}
        for key in METRICS:
            values = [(r.get('usage') or {}).get(key) if key.endswith('_tokens') else r.get(key) for r in accepted]
            values = [v for v in values if v is not None]
            q = statistics.quantiles(values, n=4, method='inclusive') if len(values) >= 2 else None
            metrics[key] = dict(n=len(values), median=statistics.median(values) if values else None,
                                q1=q[0] if q else None, q3=q[2] if q else None, iqr=q[2]-q[0] if q else None)
        groups.append(dict(fixture=name, completed=len(cell), accepted=len(accepted), metrics=metrics))
    return groups

p=Path(__file__).parent
r=json.loads((p/'trials.json').read_text())
s=json.loads((p/'summary.json').read_text())
assert len({v['key'] for v in r})==len(r)==s['completed']
assert sum(v['green'] for v in r)==s['accepted']
assert aggregate(r)==s['groups']
assert sum(v['local_attempt_ran'] for v in r)==s['local_attempts']
assert [l['seconds'] for v in r for l in v['local_runs']]==s['local_seconds']['values']
print('B2-retry:',len(r),'completed;',s['accepted'],'accepted;',s['local_attempts'],'local attempts; aggregates verified')
