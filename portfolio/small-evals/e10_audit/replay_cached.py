"""Offline cached-summary replay. Historical inputs are copied, never overwritten.

No model calls. Context scorers aggregate stored correctness flags; that boundary
is explicit rather than claiming independent answer re-grading.
"""
import contextlib
import hashlib
import importlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import socket
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import paths

MODULES = {1: 'e01_noise_floor.score', 2: 'e02_injection.score',
           3: 'e03_omit.score', 4: 'e04_phrase.score', 5: 'e05_answer_first.score',
           6: 'e06_judge.score', 11: 'e11_cost_curve.summary',
           12: 'e12_context_use.score', 13: 'e13_implied.score',
           14: 'e14_compaction.score', 15: 'e15_rag.score'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def differences(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        return sum((differences(a.get(k), b.get(k), path+'/'+k) for k in sorted(a.keys() | b.keys())), [])
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return sum((differences(x, y, path+'/'+str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    if isinstance(a, (float, int)) and isinstance(b, (float, int)):
        if (math.isnan(a) and math.isnan(b)) or math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12):
            return []
    if a == b:
        return []
    return [{'path': path, 'historical': a, 'replayed': b}]

def main():
    os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MPLBACKEND='Agg')
    def offline(*args, **kwargs):
        raise RuntimeError('Network disabled during cached replay')
    socket.socket.connect = offline
    source = ROOT / 'results'
    report = {'date': '2026-11-17', 'scope': 'original cached studies; no replication cohorts',
              'comparison_tolerance': {'relative': 1e-10, 'absolute': 1e-12}, 'studies': {}}
    dest = source / 'e10' / 'cached-replay-2026-11-17'
    dest.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='e10-replay-') as temp:
        work = Path(temp)
        for n in MODULES:
            folder = source / f'e{n:02}'
            target = work / folder.name
            target.mkdir()
            for p in folder.iterdir():
                if p.suffix in ('.json', '.jsonl') and not p.name.startswith('summary'):
                    shutil.copyfile(p, target / p.name)
        paths.RESULTS = work
        for n, module in MODULES.items():
            key = f'e{n:02}'
            record = {'module': module, 'source_sha256': digest(ROOT / (module.replace('.', '/')+'.py')),
                      'inputs': {p.name: digest(p) for p in sorted((source/key).glob('*.jsonl'))},
                      'scope': 'cached summary replay; stored flags reused where scorer does so'}
            log = io.StringIO()
            try:
                mod = importlib.import_module(module)
                sys.argv = [module]
                with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                    mod.main()
                    if n == 11:
                        sys.argv = [module, '--model', '27b']
                        mod.main()
                summaries = {}
                for p in sorted((work/key).glob('summary*.json')):
                    old = source/key/p.name
                    delta = differences(json.loads(old.read_text('utf-8')), json.loads(p.read_text('utf-8')))
                    summaries[p.name] = {'differences': delta, 'historical_sha256': digest(old), 'replayed_sha256': digest(p)}
                    shutil.copyfile(p, dest / (key+'-'+p.name))
                assert summaries, 'no summaries generated'
                record.update(status='matched' if all(not x['differences'] for x in summaries.values()) else 'changed', summaries=summaries)
            except Exception as exc:
                record.update(status='blocked', error=f'{type(exc).__name__}: {exc}')
            (dest/(key+'.log')).write_text(log.getvalue(), encoding='utf-8')
            report['studies'][key] = record
            print(key, record['status'], record.get('error', ''))
    (dest/'report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
