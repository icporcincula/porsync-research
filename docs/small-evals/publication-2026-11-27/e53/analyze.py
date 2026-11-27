"""Recompute structural gate from released per-turn facts, without replies."""
import json
from pathlib import Path
s=json.loads((Path(__file__).resolve().parent/'summary.json').read_text())
reproduced=[t for t,v in s['tasks'].items() if v['control_stalled']]
assert sorted(reproduced)==sorted(s['reproduced'])
for label,expected in s['by_condition'].items():
    facts=[s['tasks'][t]['conditions'][label] for t in reproduced]
    actual={'of':len(facts),'converted':sum(bool(f['converted']) for f in facts),'enforced':sum(bool(f['enforced']) for f in facts),'converted_and_enforced':sum(bool(f['converted'] and f['enforced']) for f in facts)}
    assert actual==expected,(label,actual,expected)
assert s['decision']=='promising'
assert any(v['converted_and_enforced']>=2 for k,v in s['by_condition'].items() if k not in ('control','req0'))
print('E53: structural conversion accounting reproduced; no task-success claim')
