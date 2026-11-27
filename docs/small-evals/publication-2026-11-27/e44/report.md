> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E44 write-up: Inkling 2 Mini local harness arms vs a frontier baseline

Status: **closed 2026-11-23.** Private; publication held; no public-repo edits. All numbers come from saved rows (see Sources). This note is descriptive: n = 8 fixtures, one model, one quant.

## Question

On eight fresh, never-shown fixtures (n17–n24), how often does a local Inkling 2 Mini stack finish the task, with Patchsmith v5b or with Aider, and how does that compare with frontier Claude (Sonnet, Haiku) given the same fixtures and the same tests?

## Setup (frozen before any attempt)

| Arm | Stack | Attempts |
|---|---|---|
| Patchsmith v5b | Inkling 2 Mini UD-IQ3_XXS, llama.cpp `b50-8d60873` CUDA, 32K context, thinking always on, 8,192-token cap, 30 turns | 3 per fixture (24) |
| Aider | same model, build and cap; whole-file, `--auto-test`, 1,800 s limit | 3 per fixture (24) |
| Sonnet / Haiku | subscription `claude -p`, direct CLI, same prompt template as E39, 600 s limit | 3 per fixture per model (48) |

Pass = the fixture's own tests green with protected test/config files restored and unchanged. Protocols: local arms (private source reference withheld), frontier companion (private source reference withheld). The 16-fixture pilot (n01–n16) is tuning data and is not pooled.

## Results

| Arm | Passes | Rate | Clopper-Pearson 95% |
|---|---|---|---|
| Sonnet | 24/24 | 100% | 85.8–100% |
| Haiku | 24/24 | 100% | 85.8–100% |
| Patchsmith v5b (local) | 21/24 | 87.5% | 67.6–97.3% |
| Aider (local) | 9/24 | 37.5% | 18.8–59.4% |

Per fixture (passes of 3):

| Fixture | Sonnet | Haiku | v5b | Aider |
|---|---|---|---|---|
| n17_cron | 3 | 3 | 2 | 0 |
| n18_money | 3 | 3 | 2 | 0 |
| n19_pq | 3 | 3 | 3 | 3 |
| n20_slug | 3 | 3 | 3 | 1 |
| n21_duration | 3 | 3 | 2 | 0 |
| n22_matrix | 3 | 3 | 3 | 3 |
| n23_intervals | 3 | 3 | 3 | 3 |
| n24_ini | 3 | 3 | 3 | 0 |

Paired per-fixture sign comparisons (unit = fixture; ties kept; exact two-sided p, descriptive):

| Comparison | Wins / losses / ties | p |
|---|---|---|
| v5b vs Aider | 5 / 0 / 3 | 0.0625 |
| Sonnet vs Aider, Haiku vs Aider | 5 / 0 / 3 | 0.0625 |
| Sonnet vs v5b, Haiku vs v5b | 3 / 0 / 5 | 0.25 |

None reaches 0.05. With 8 fixtures this design cannot detect a small difference, so read the direction, not the p-values.

## Cost in time and quota

| Arm | Wall time per attempt |
|---|---|
| Sonnet | median 19.5 s (IQR 17.2–22.1), mean 5.0 turns |
| Haiku | median 34.8 s (IQR 31.7–39.9), mean 9.2 turns |
| Patchsmith v5b | per-fixture medians 112–917 s; range 77–1,159 s overall |
| Aider | about 60–190 s (all 15 misses ended near 190 s on the token cap) |

Frontier calls used subscription quota only (no API spend). Totals for 24 attempts: Sonnet 636K cache-create / 2.64M cache-read / 27K output tokens; Haiku 805K / 6.29M / 105K. Token totals are not quota percentages. The local arms use no quota but take roughly 3–45× longer per attempt (comparing per-fixture v5b medians with the frontier overall medians) on the same fixtures and occupy the single GPU for the whole run (scored arm 3 h 41 min).

## What the failures were

- Patchsmith's 3 misses: all `blocked no_tool_calls` (an empty turn stopped the run); no timeouts, no wrong-but-finished answers. The pilot already showed 11 of 16 runs wasting 1–5 empty turns. This points at harness handling of empty reasoning turns, not at the task.
- Aider's 15 misses: all hit the 8,192-token cap through always-on reasoning (the pilot found runaway repetition at the same stage). Equalising the cap removed the pilot's timeout confound, but did not rescue Aider.
- Frontier: no timeouts, CLI errors or protected-file violations in 48 trials.

## Reading

1. The local Inkling + Patchsmith v5b stack solved 21/24 on fresh fixtures, which is the headline for the cheap lane: usable, not certified.
2. The fixtures do not separate frontier from v5b. The frontier arms are at ceiling (48/48), so the only information is that v5b lost 3 attempts to harness behaviour on 3 fixtures (n17, n18, n21; the hardest by v5b time).
3. Harness matters more than model here: same model and cap, 87.5% vs 37.5%.
4. The sign comparisons show direction only. A router decision needs more than 8 fixtures and real tasks (see E45).

## Limits

- Different harnesses and prompts: direct CLI for frontier, Patchsmith or Aider for local. This is outcome evidence, not a controlled model comparison and not a routing promotion.
- Fixture authors had seen the pilot outcomes, so difficulty may track what was known to be solvable for the local arm. The model had not seen these fixtures. The frontier fixtures were never shown to either frontier model.
- n = 3 per cell: 3/3 bounds a pass rate only to about 29–100%. Attempts cluster by fixture, so attempt-level intervals are descriptive.
- One quant (IQ3_XXS), one build; Q3_K_XL is corrupt on CUDA and parked. Vendor benchmark figures are not reproduced here.
- User-level Claude Code configuration was loaded for frontier runs, as in earlier cohorts. The Sonnet runs also recorded `claude-haiku-5-5` in `modelUsage` (the CLI's own background calls), so Sonnet token totals include small Haiku usage.
- The nested `patchsmith-audit` HEAD moved during the frontier run (fixtures, task file and runner hashes still match the plan; time of the move not recorded).
- The frozen protocol file shows `?` where PowerShell dropped en-dash and multiplication characters. Cosmetic only; content and rules unaffected.
- Reasoning-token counts and the cause of Patchsmith's empty turns were not analysed.

## Wording to fix in the frozen scored-arm protocol (not edited)

Line 3 says "Part of the E43 candidate G follow-up". E44 is its own study. Record the correction here rather than edit the frozen file.

## Sources

- Local arms: `[withheld local path]` (`aider/results.jsonl`, `v5`, `v5.table.md`); summary in inkling-2-mini-readiness.md (private source reference withheld).
- Frontier: `tmp/e44-frontier-heldout3-2026-11/` (`plan.json`, `results.jsonl`, `summary.json`, `paired.json`); results (private source reference withheld). Runner `scripts/e44_frontier_heldout3.py`, summary `scripts/e44_frontier_heldout3_summary.py`.

## Publication

Held. No public-repo edit, push or site article. Selecting artifacts for `porsync-research` needs explicit authorization; raw transcripts and fixtures stay private until then.


## 2026-11-27 publication accounting correction

The original prose total of Aider 9/24 was an arithmetic error: the per-fixture table sums to 10/24, and the unchanged saved `aider/results.jsonl` rows contain ten green booleans in 24 attempts (n19 3, n20 1, n22 3, n23 3; other fixtures 0). Correct total: **10/24 (41.7%)**, exact Clopper-Pearson 95% interval **22.1 to 63.4%** (unrounded 0.22109690534667853 to 0.6335693543436376). Accordingly there are 14 Aider misses, not 15. This corrects saved-label accounting only; no patches, tests, transcripts or model outputs were rescored and no attempt was rerun. The fixture-level comparison remains five wins, zero losses, three ties, exact sign p=0.0625. Original text/table and rows are preserved. The selected public release and site article use the corrected total and disclose this discrepancy. Earlier publication holds are superseded only for the selected package by prompt 27.
