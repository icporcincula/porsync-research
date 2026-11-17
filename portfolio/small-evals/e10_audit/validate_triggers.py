"""CPU-only behavioral validation of the six recorded E10 source patches.

Execute selected function ASTs with explicit synthetic inputs/dependencies; never
import runners or start services. This is a function-level audit, not cached rescoring.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import tempfile
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def functions(source, names, namespace):
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<audited-functions>', 'exec'), namespace)
    return namespace


def observe(name, source):
    if name == 'parser_first_option':
        f = functions(source, ['parse_option'], {})['parse_option']
        return [f('beta', ['alpha', 'beta']), f('unknown', ['alpha', 'beta'])]
    if name in {'label_compares_to_itself', 'floor_reuses_a'}:
        from common.stats import boot_ci, flips
        with tempfile.TemporaryDirectory(prefix='e10-trigger-') as temp:
            root = Path(temp)
            out = root / 'e01'
            out.mkdir()
            for arm, values in {'A': [0, 0], 'A2': [1, 0], 'C1': [1, 1]}.items():
                (out / f'{arm}.c1.r1.jsonl').write_text(''.join(json.dumps({'i': i, 'queue': v}) + '\n' for i, v in enumerate(values)))
            ns = dict(argparse=argparse, json=json, Path=Path, np=np, RESULTS=root,
                      QIDS=['queue'], ARMS=['A', 'A2', 'C1'], EDITS=['C1'],
                      sample=lambda: [{'labels': [{'queue': 0}, {'queue': 0}]}],
                      boot_ci=boot_ci, flips=flips)
            functions(source, ['read', 'vec', 'main'], ns)
            argv = sys.argv
            try:
                sys.argv = ['e10-trigger']
                with contextlib.redirect_stdout(io.StringIO()):
                    ns['main']()
            finally:
                sys.argv = argv
            row = json.loads((out / 'summary.json').read_text())['c1']['C1']['r1']
            key = 'queue_acc_delta_vs_A' if name == 'label_compares_to_itself' else 'queue'
            return row[key]['mean'] if key != 'queue' else row[key]['attributable']['mean']
    if name == 'verifier_accepts_prompt_numbers':
        import re
        from decimal import Decimal, ROUND_HALF_UP
        from e08_summaries.numbers import PATTERN, SCALES
        ns = dict(re=re, Decimal=Decimal, ROUND_HALF_UP=ROUND_HALF_UP, PATTERN=PATTERN, SCALES=SCALES)
        functions(source, ['extract', 'rounded', 'allowed', 'verify'], ns)
        return ns['verify']({'values': {'sales': [10, 20]}, 'metadata': 'reference 731'}, 'Sales were 731.')['flagged']
    if name == 'tool_grader_trusts_answer':
        from e09_tools.catalogue import FIELDS, matches, products, requests
        from e09_tools.score import score as frozen_score
        from e09_tools.test_score import transcript
        ns = dict(FIELDS=FIELDS, matches=matches, products=products, frozen_score=frozen_score)
        functions(source, ['score'], ns)
        task = requests()[1]
        trace = transcript(task, items=[], filters_applied=['waterproof'], constraints_not_applied=[])
        return ns['score'](task, trace)['false_claim']
    if name == 'stream_decision_at_end':
        from common.stream_json import StreamJSON
        class Response:
            status_code = 200
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def iter_lines(self):
                for chunk in ['{"queue":"a","priority":"b","sentiment":"c",', '"notes":"later"}']:
                    yield 'data: ' + json.dumps({'choices': [{'delta': {'content': chunk}}]})
                yield 'data: [DONE]'
        ticks = iter([0., 1., 4., 5.])
        client = SimpleNamespace(base='offline', payload=lambda *a: {}, http=SimpleNamespace(post=lambda *a, **k: Response()))
        ns = dict(OpenAIClient=object, StreamJSON=StreamJSON, json=json, TIMEOUT_S=1,
                  QIDS=['queue', 'priority', 'sentiment'], time=SimpleNamespace(perf_counter=lambda: next(ticks)))
        functions(source, ['stream_one'], ns)
        row = ns['stream_one'](client, [], 10, {})
        return [row['t_decision'], row['total_s']]
    raise ValueError(name)


def run():
    # Parse the historical definitions without executing sabotage.py's CLI.
    tree = ast.parse((ROOT / 'e10_audit/sabotage.py').read_text(encoding='utf-8'))
    faults = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'faults' for t in n.targets))
    expected = {'parser_first_option': [1, -1], 'label_compares_to_itself': -1.,
                'floor_reuses_a': .5, 'verifier_accepts_prompt_numbers': True,
                'tool_grader_trusts_answer': True, 'stream_decision_at_end': [1., 5.]}
    rows = []
    for name, filename, before, after in faults:
        path = ROOT.parent / 'tally' / filename if filename.startswith('baselines/') else ROOT / filename
        raw = path.read_bytes()
        source = raw.decode('utf-8')
        assert source.count(before) == 1, (name, 'patch must match exactly once')
        baseline = observe(name, source)
        mutant = observe(name, source.replace(before, after, 1))
        assert baseline == expected[name], (name, 'baseline failed', baseline)
        assert mutant != expected[name], (name, 'fault not detected', mutant)
        rows.append(dict(fault=name, source=path.relative_to(ROOT.parent).as_posix(),
                         source_sha256=hashlib.sha256(raw).hexdigest(), expected=expected[name],
                         baseline=baseline, mutant=mutant, baseline_pass=True, mutant_rejected=True))
    return dict(date='2026-11-17', scope='function ASTs with synthetic inputs; no inference or cached headline rescoring',
                python=platform.python_version(), numpy=np.__version__, rows=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
