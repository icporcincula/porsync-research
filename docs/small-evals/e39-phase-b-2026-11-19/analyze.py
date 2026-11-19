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

rows=json.loads(Path(__file__).with_name("trials.json").read_text())
s=json.loads(Path(__file__).with_name("summary.json").read_text())
assert len({r["key"] for r in rows})==len(rows)
for arm,v in s["arms"].items():
 cell=[r for r in rows if r["arm"]==arm]
 assert aggregate(cell)==v["groups"]
 assert len(cell)==v["completed"] and sum(r["green"] for r in cell)==v["accepted"]
 print(arm,len(cell),v["accepted"],v["status"])
