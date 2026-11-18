"""Recompute per-cell and per-fixture pass counts from trials.json; no model calls.

Usage: python analyze.py [--write]   (--write regenerates summary.json)
"""
import collections
import json
import sys
from pathlib import Path


def summarize(rows):
    cells = collections.defaultdict(list)
    for row in rows:
        cells[(row['model'], row['harness'])].append(row)
    out = []
    for (model, harness), group in sorted(cells.items()):
        per = collections.OrderedDict()
        for row in sorted(group, key=lambda r: (r['fixture'], r['run'])):
            per[row['fixture'][:3]] = per.get(row['fixture'][:3], 0) + row['passed']
        out.append(dict(model=model, harness=harness, trials=len(group),
                        passed=sum(r['passed'] for r in group), per_fixture=per))
    return out


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    rows = json.loads((root / 'trials.json').read_text(encoding='utf-8'))
    assert len(rows) == 216
    assert len({(r['model'], r['harness'], r['fixture'], r['run']) for r in rows}) == 216
    result = summarize(rows)
    assert all(cell['trials'] == 24 for cell in result)
    if '--write' in sys.argv:
        (root / 'summary.json').write_text(json.dumps(result, indent=1) + '\n', encoding='utf-8', newline='\n')
    else:
        assert result == json.loads((root / 'summary.json').read_text(encoding='utf-8'))
    for cell in result:
        print(f"{cell['model']:32} {cell['harness']:36} {cell['passed']:2}/24  {list(cell['per_fixture'].values())}")
    print('Verified 216 unique trial rows in 9 cells of 24.')
