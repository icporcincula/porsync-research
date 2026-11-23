"""Recompute E43 saved development accounting, without inference or rescoring."""
from collections import Counter
import json
from pathlib import Path


def analyze(root):
    rows = json.loads((root/'development-dispositions.json').read_text())
    design = json.loads((root/'next-design.json').read_text())
    assert len(rows)==17 and len({r['id'] for r in rows})==17
    launched = [r for r in rows if r['status']!='unstarted']
    final = [r for r in launched if '-final-' in r['id']]
    assert len(launched)==16 and len(final)==15
    assert sum(r['completed_requests'] for r in rows)==176
    assert sum(r.get('request_errors',0) for r in final)==0
    assert sum(r.get('reasoning_content_chars',0) for r in final)==0
    assert sum(r.get('think_markers',0) for r in final)==0
    interrupted = [r for r in rows if r['status']=='interrupted']
    assert len(interrupted)==1 and interrupted[0]['partial_generated_tokens_lower_bound']==100
    assert len([r for r in rows if r['status']=='unstarted'])==1
    counts = {}
    for candidate,expected in [('lfm3',126),('twil',50)]:
        group = [r for r in rows if r['candidate']==candidate]
        assert sum(r['completed_requests'] for r in group)==expected
        counts[candidate]=dict(Counter(r['disposition'] for r in group))
    assert counts['lfm3']==dict(accepted_pass=5,functional_failure=1,
                                artifact_excluded=1,compaction_blocked=1)
    assert counts['twil']==dict(accepted_pass=7,telemetry_interruption=1,budget_exhausted=1)
    assert design['new_development_attempts']==4*2*2*2==32
    b=design['stage_b']
    assert b['tasks']*b['repeats']*b['arms']==b['trials_per_candidate']==288
    assert b['maximum_trials']==2*b['trials_per_candidate']==576
    assert not b['collection_authorized'] and not b['holdout_package_frozen']
    return dict(launched_development_attempts=len(launched),final_session_probes=len(final),
                completed_requests=176,additional_interrupted_request_attempts=1,
                dispositions=counts,new_model_trials=0,stage_a_complete=False,
                limits='Saved accounting only; no code rescoring, inference reproduction or adapter-effect estimate.')


if __name__=='__main__':
    print(json.dumps(analyze(Path(__file__).resolve().parent),indent=2))
