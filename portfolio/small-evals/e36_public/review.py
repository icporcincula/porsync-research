"""Prepare blinded human-review JSONL or validate completed independent reviews.

This never calls a model and never converts missing/uncertain labels to NO.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load_subset(path):
    data = json.loads(path.read_text('utf-8'))
    body = {k: v for k, v in data.items() if k != 'sha256'}
    assert hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest() == data['sha256']
    ids = [r['id'] for r in data['items']]
    assert len(ids) == len(set(ids)) == data['n']
    return data

def validate(rows, subset):
    expected = {r['id']: r for r in subset['items']}
    assert len(rows) == len(expected), 'incomplete review'
    assert len({r['id'] for r in rows}) == len(rows), 'duplicate ID'
    assert {r['id'] for r in rows} == set(expected), 'ID mismatch'
    for r in rows:
        assert r['decision'] in ('YES', 'NO', 'UNCERTAIN'), 'missing/invalid decision'
        assert r['reviewer'].strip() and r['rationale'].strip(), 'reviewer/rationale required'
        assert r['text'] == expected[r['id']]['text'], 'review text changed'
        assert r['text_sha256'] == hashlib.sha256(r['text'].encode()).hexdigest(), 'text hash mismatch'
        if r['decision'] != 'UNCERTAIN':
            assert r['evidence_quote'] and r['evidence_quote'] in r['text'], 'verbatim supporting quote required'
    return {label: sum(r['decision'] == label for r in rows) for label in ('YES', 'NO', 'UNCERTAIN')}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--subset', type=Path, default=HERE/'frozen_subset.json')
    ap.add_argument('--out', type=Path)
    ap.add_argument('--validate', type=Path)
    args = ap.parse_args()
    subset = load_subset(args.subset)
    if args.validate:
        rows = [json.loads(s) for s in args.validate.read_text('utf-8').splitlines() if s.strip()]
        print(json.dumps(validate(rows, subset)))
    else:
        assert args.out, '--out is required'
        rows = [dict(id=r['id'], text=r['text'], text_sha256=hashlib.sha256(r['text'].encode()).hexdigest(),
                     decision='', evidence_quote='', rationale='', reviewer='') for r in subset['items']]
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
        print(f'Prepared {len(rows)} blinded items; no labels assigned')

if __name__ == '__main__':
    main()
