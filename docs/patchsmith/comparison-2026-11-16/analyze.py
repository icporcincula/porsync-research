"""Recompute descriptive summaries from curated trial rows; no model calls."""
import collections
import json
from pathlib import Path
import statistics


def summarize(rows):
    groups = collections.defaultdict(list)
    for row in rows:
        groups[(row['arm'], row['set'])].append(row)
    return [dict(arm=arm, set=task_set, trials=len(group),
                 passed=sum(r['passed'] for r in group),
                 median_secs=round(statistics.median(r['secs'] for r in group), 3),
                 total_secs=round(sum(r['secs'] for r in group), 3),
                 min_secs=round(min(r['secs'] for r in group), 3),
                 max_secs=round(max(r['secs'] for r in group), 3))
            for (arm, task_set), group in sorted(groups.items())]


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    rows = json.loads((root / 'trials.json').read_text(encoding='utf-8'))
    assert len({(r['source'], r['source_row']) for r in rows}) == len(rows)
    assert len(rows) == 159
    result = summarize(rows)
    expected = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
    assert result == expected
    print(json.dumps(result, indent=2))
    batch = [r for r in rows if r['final_batch']]
    assert len(batch) == 68 and sum(r['passed'] for r in batch) == 65
    print('Verified 159 unique archived trials; final batch 65/68.')
