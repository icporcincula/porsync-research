# E21 — Stage B partial-run reconciliation, 2026-11-17

**Stage B started but did not finish.** The local archive contains 13 unique completed trials from a planned 108. Rechecking exact planted-code containment in every saved answer reproduces all 13 saved passes. This corrects the older protocol's “not run” wording and the tracker's ambiguous “Stage B, 13 trials” status.

| KV dtype / prompt length | Recorded passes / trials | Planned trials |
|---|---:|---:|
| f16 / approximately 32K tokens | 12 / 12 | 12 |
| f16 / approximately 64K tokens | 1 / 1 | 12 |
| f16 / approximately 124K tokens | Not run | 12 |
| q8_0 / each of 32K, 64K, 124K | Not run | 36 total |
| q4_0 / each of 32K, 64K, 124K | Not run | 36 total |

The 95 absent trials are missing evidence, not failures. There is no measured comparison between KV dtypes, no completed 64K cell, and no 124K evidence. H4/H5 remain unresolved. Stage A's earlier timing findings are not changed by this reconciliation.

## Method and provenance

Read the separate `e21-glimmer-offload` checkout's `needle_recall.py`, `results/stage_b.jsonl` and `results/stage_b.log`; no harness import, inference or service operation. The current harness describes three dtypes, three lengths, two seeds and six depths (108 trials), at 44 offloaded layers and context 131072. Completed rows are all f16, finish reason `stop`, with twelve 32K questions across seeds 1/2 and the first 64K question from seed 1. Answers contain the exact planted code; duplicate trial keys were checked.

The separate checkout is on `master` at `88decd3441678f0225c417253881fb70bfdd2e85`, with no configured remote. README is modified; the Stage B harness, data and log are untracked. Those files were read without modification. Thus the current local files do not independently prove the harness's claimed pre-run freeze, nor establish public availability. The log ends after the thirteenth pass; it does not establish why the run stopped. Earlier references to a “public repo” must not be treated as verified publication.

The [reconciled archive](../../portfolio/small-evals/results/e21/stage-b-reconciled-2026-11-17.json) preserves all 13 synthetic answer rows, source hashes and the missing-cell counts. The [offline analyzer](../../portfolio/small-evals/e10_audit/reconcile_e21.py) validates uniqueness and saved scores. Reproduce locally with:

```sh
python portfolio/small-evals/e10_audit/reconcile_e21.py PATH_TO_E21_ARCHIVE tmp/e21-reconciled.json
```

## Limits and next step

Code containment is a narrow retrieval check, not general long-document understanding. Six sequential questions reuse one cached document prefix; later timings are not independent cold-prefill measurements. Two documents at 32K and one question at 64K do not support a reliable quality curve. Reconstruct/freeze a continuation protocol before any future GPU run; the missing grid is deferred while the GPU is in use. The historical raw archive remains unchanged.

Public evidence draft prepared locally with this report, selected synthetic trial rows and analyzer. No full server logs, model files or unrelated source exported. Existing publication hold remains; nothing committed or pushed.

## Publication authorization — 2026-11-17

The user authorized committing and pushing the selected CPU-only E10/E21/E36 changes. Earlier publication-hold statements describe preparation time and are superseded for these selected artifacts. Raw private inputs remain excluded from the public release.
