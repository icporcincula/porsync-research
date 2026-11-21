# Phase A: frontier held-out outcomes

Status: **complete**. 96/96 trials recorded. Updated 2026-11-19T14:17:34.271725+00:00.

All 16 dry baselines failed with discovered tests; reference files were absent. Independent verification uses `python -B -m unittest discover -q`, matching both local evaluation scripts. The inspected Haiku n09 smoke passed 3 tests, changed production files only, recorded usage and resolved to `claude-haiku-5-5` (25.094 s, 6 turns).

Commands: `python -B scripts/e39_frontier_heldout.py --dry`; `python -B scripts/e39_frontier_heldout.py --only blind2-n09_rle-haiku-0`; background `python -B scripts/e39_frontier_heldout.py > tmp/e39-frontier-heldout-2026-11/run.out 2>&1`. Resume with the same command. Offline refresh: `python -B scripts/e39_frontier_heldout_summary.py`.

Private plan, transcripts, patches, artifact hashes, dry output, missing-key list and machine-readable summaries are under `tmp/e39-frontier-heldout-2026-11/`. The original 124-trial runner is unchanged. No E41 server operation, router change, commit or publication is authorized here.

| Cohort | Model | Green/completed/planned | Median s | Q1–Q3 s | Mean turns | Input/create/read/output tokens | Timeouts/errors/protected |
|---|---|---|---|---|---|---|---|
| blind2 | sonnet | 24/24/24 | 18.80 | 17.39–20.34 | 5.17 | 180 / 640265 / 2304970 / 23619 | 0/0/0 |
| blind2 | haiku | 24/24/24 | 29.16 | 26.15–33.98 | 7.67 | 252 / 762916 / 4680324 / 71577 | 0/0/0 |
| heldout1 | sonnet | 24/24/24 | 19.98 | 15.84–21.71 | 4.92 | 198 / 623245 / 2863241 / 21723 | 0/0/0 |
| heldout1 | haiku | 24/24/24 | 30.63 | 27.71–35.28 | 8.12 | 272 / 760424 / 5123800 / 80926 | 0/0/0 |

Times exclude nulls; inclusive quartiles, IQR = Q3 − Q1 (undefined with fewer than two timings). Token counts are summed, not subscription quota percentages. Resolved model IDs and missing usage counts are retained in the JSON summary.

## Paired fixture outcomes

Local cells come exclusively from saved E41 rows; source hashes are retained privately. `missing (x/n)` means fewer than three completed rows. The E41 batch is complete; the saved-row table was refreshed after its completion on 2026-11-19. Set-1 v5 means v5b; v6 was not run there. gptoss is the original arm, not the separately tuned gptoss-fix rerun.

### blind2

| Fixture | Sonnet | Haiku | edge0 v5 | edge0 v6 | edge0 aider | gptoss v5 | gptoss v6 | gptoss aider | qwen3coder v5 | qwen3coder v6 | qwen3coder aider | qwen36 v5 | qwen36 v6 | qwen36 aider |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| n09_rle | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n10_ranges | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n11_csv | 3/3 | 3/3 | 0/3 | 1/3 | 3/3 | 0/3 | 2/3 | 2/3 | 1/3 | 1/3 | 1/3 | 3/3 | 3/3 | 2/3 |
| n12_pager | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 1/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| n13_roman | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 2/3 | 3/3 | 0/3 | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| n14_window | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n15_suggest | 3/3 | 3/3 | 2/3 | 1/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n16_dictdiff | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

### heldout1

| Fixture | Sonnet | Haiku | edge0 v5 | edge0 aider | gptoss v5 | gptoss aider | qwen3coder v5 | qwen3coder aider | qwen36 v5 | qwen36 aider |
|---|---|---|---|---|---|---|---|---|---|---|
| n01_bucket | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n02_semver | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 0/3 | 3/3 | 3/3 |
| n03_wrap | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n04_ledger | 3/3 | 3/3 | 1/3 | 1/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| n05_bizdays | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| n06_lru | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| n07_template | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 |
| n08_topo | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 0/3 | 0/3 | 3/3 | 3/3 |

## Incidents and limits

E41 was still running with llama-server at launch; no edge0-infer process was present. Its batch and read-only Patchsmith checkout were untouched. Before each new trial, the runner checks the Manila deadline and waits while edge0-infer exists. Stops: [{"key": "heldout1-n02_semver-haiku-1", "reason": "usage_limit"}]. Missing trials: 0.

- Frontier and local prompts/harnesses differ: direct CLI versus Patchsmith/Aider.
- n = 3 per cell; 3/3 bounds the pass rate at only about 29–100%.
- Set 1 was used to tune v5b, so it is not blind for the local arm.
- Fixture labels are not a runtime classifier.
- This is paired outcome evidence, not a routing promotion. Plugin accounting, host/shadow integration, health calibration and natural recovery remain open.
- User-level Claude Code configuration was loaded, as in the earlier cohort.


Selected aggregate evidence, published 2026-11-21. Raw prompts, transcripts, patches, fixtures and private source remain excluded.
