import json
from pathlib import Path
p=Path(__file__).resolve().parent
s=json.loads((p/'summary.json').read_text());t=json.loads((p/'trials.json').read_text())
assert len(t)==s['completed'] and len({r['key'] for r in t})==len(t)
for a in s['arms']:
 rows=[r for r in t if r['arm']==a['arm']]
 assert len(rows)==a['completed'] and sum(bool(r['green']) for r in rows)==a['final_passes']
 assert sum(r['local_pass'] for r in rows)==a['local_passes']
 assert sum(r['frontier_repair'] for r in rows)==a['frontier_repairs']
assert s['quota_savings_percent'] is None
print('E39 closeout selected counts verified:',len(t))
