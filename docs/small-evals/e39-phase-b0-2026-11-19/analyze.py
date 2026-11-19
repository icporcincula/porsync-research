METRICS = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens', 'turns', 'secs')
import json, statistics
from pathlib import Path
rows=json.loads(Path(__file__).with_name("trials.json").read_text())
assert len({r["key"] for r in rows})==len(rows)
print("completed",len(rows),"accepted",sum(r["green"] for r in rows))

def aggregate(rows):
    groups = []
    for name in ('bug1', 'bug2', 'feature', 'multifile', 'refactor', 'offbyone', 'javascript'):
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

actual=aggregate(rows)
expected=json.loads(Path(__file__).with_name("summary.json").read_text())["groups"]
assert actual==expected, "Aggregate mismatch"
print(json.dumps(actual,indent=2))
