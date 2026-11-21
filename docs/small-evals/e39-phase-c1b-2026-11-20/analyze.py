import json, statistics
from pathlib import Path
def stats(values):
    v = [x for x in values if x is not None]
    q = statistics.quantiles(v, n=4, method='inclusive') if len(v) > 1 else None
    return dict(n=len(v), median=statistics.median(v) if v else None,
                q1=q[0] if q else None, q3=q[2] if q else None, iqr=q[2]-q[0] if q else None)

p=Path(__file__).parent
s=json.loads((p/'summary.json').read_text())
r=json.loads((p/'trials.json').read_text())
assert len(r)==s['completed']==len({v['key'] for v in r})
for g in s['cohorts']:
 c=[v for v in r if v['source_cohort']==g['cohort']]
 assert len(c)==g['completed']
 assert sum(v['green'] for v in c)==g['accepted']
 assert stats(v['secs'] for v in c)==g['cli_seconds']
 assert stats(v['startup_wait'] for v in c)==g['startup_wait']
 assert stats(v['adjusted_seconds'] for v in c)==g['adjusted_cli_seconds']
 assert stats(x['seconds'] for v in c for x in v['local_runs'])==g['local_seconds']
 assert sum(v['local_pass'] for v in c)==g['local_only_passes']
 assert sum(v['repair'] for v in c)==g['frontier_repairs']
 for k in g['tokens']:
  assert stats((v['usage'] or {}).get(k) for v in c)==g['tokens'][k]
print('C1b selected counts, local ledgers, clocks and tokens verified:',len(r))
