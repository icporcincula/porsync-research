> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E54 results - private

Date: 2026-11-25. Status: complete execution; frozen reading-rule decision **`not_advance`** for Bonsai (B) against production Inkling (C). No push, publication, public-evidence sync, promotion or router change. Frozen protocol: e54-bonsai-vs-inkling-protocol.md (private source reference withheld) (commit 1b26d9a0). Machine-readable summary: e54-data/summary.json (private source reference withheld) (copy of `tmp/e54/summary.json`, produced by `python scripts/e54_analyze.py --out tmp/e54/summary.json`).

## Observed result

All six scored blocks completed in the frozen order (C r1, B r1, CB r1, CB r2, B r2, C r2): 72 attempts per arm, 216 total, no stopped block, no boundary violation, no serving error. Every scored failure stays in the denominator. Success means the saved runner row passed its independent acceptance requirements; no model-written patch was judged for quality by the reporting agent.

B and C each succeeded on 61/72 (0.847). The B-minus-C accuracy difference is 0.000, with a task-cluster bootstrap 95% interval of [-0.111, +0.111]. The rule requires the lower bound to be above -0.10, so the accuracy check fails by 0.011 and the decision is `not_advance`. B's throughput is 3.40x C's (95% interval 2.08 to 5.26), which passes the throughput check. Neither arm is at a ceiling or floor.

This is a precision limit, not evidence that B is worse. With 36 tasks per repeat the interval around a tie is about +/-0.11, so the data neither show nor rule out a loss of up to about 11 points. It is a study-selection result for this pool and configuration only.

| Frozen check | Value | Pass |
|---|---|---|
| B and C each complete 72 attempts, no stopped block | yes | yes |
| No boundary violation in any arm | 0 | yes |
| Serving-error attempts (limit 10%) | 0 | yes |
| B-C accuracy 95% lower bound above -0.10 | -0.111 | **no** |
| B/C throughput 95% lower bound above 1.0 | 2.08 | yes |
| Not both at ceiling or floor | not at ceiling/floor | yes |

## Stage 1 gate

All three arms passed the development gate (six unscored dev tasks each; excluded from every scored table). C 5/6, CB 5/6, B 6/6. `dev-c-ordinal` was a wrong patch for C and CB; B passed it. The per-request `reasoning_budget_tokens` field on CB produced no HTTP error.

## Scored per-arm statistics

| Metric | C (Inkling) | CB (Inkling + budget 1024) | B (Bonsai) |
|---|---:|---:|---:|
| Attempts | 72 | 72 | 72 |
| Successes | 61 | 58 | 61 |
| Success rate | 0.8472 | 0.8056 | 0.8472 |
| Wilson 95% interval | [0.747, 0.913] | [0.700, 0.881] | [0.747, 0.913] |
| Summed task seconds | 8,052.1 | 9,065.3 | 2,366.8 |
| Verified tasks per hour | 27.27 | 23.03 | 92.78 |
| Failure codes (non-success) | truncation 7, wrong_patch 4 | truncation 3, timeout 3, wrong_patch 8 | wrong_patch 10, loop 1 |
| Latency median, all (s) | 45.80 | 49.09 | 21.55 |
| Latency median, successes (s) | 34.97 | 40.34 | 20.09 |
| Output tokens (incl. reasoning) | 355,768 | 366,514 | 112,126 |
| Tool calls | 407 | 481 | 430 |
| Visible-test runs | 67 | 73 | 106 |
| Recovered-after-red attempts | 2 | 5 | 8 |
| Malformed calls | 0 | 0 | 0 |
| Empty turns | 27 | 22 | 0 |
| Length stops | 27 | 22 | 0 |
| Blocked edit attempts | 0 | 3 | 1 |
| Peak GPU (MiB) | 15,911 | 15,911 | 8,430 |
| Min free RAM (bytes) | 154,689,536 | 238,133,248 | 599,597,056 |
| Peak swap (bytes) | 3,755,683,840 | 4,070,670,336 | 4,709,662,720 |
| Boundary violations | 0 | 0 | 0 |

Verified tasks per hour = 3,600 x successes / summed end-to-end task seconds, including failures, thinking, tools, visible tests and acceptance. Server load and warmup are not included.

## Per-family success (of 12)

| Family | C | CB | B |
|---|---:|---:|---:|
| single_file_repair | 12 | 12 | 12 |
| multi_file_change | 12 | 11 | 10 |
| test_driven_recovery | 12 | 12 | 12 |
| scorer_summary_repair | 9 | 10 | 10 |
| feature_edge_cases | 8 | 5 | 7 |
| new_script | 8 | 8 | 10 |

## Per-block results

| Block | Arm / repeat | Successes / 36 | Summed task seconds | Failures |
|---|---|---:|---:|---|
| 1 | C / 1 | 31 | 3,671.3 | truncation 3, wrong_patch 2 |
| 2 | B / 1 | 31 | 1,221.7 | wrong_patch 5 |
| 3 | CB / 1 | 29 | 4,874.9 | truncation 3, wrong_patch 3, timeout 1 |
| 4 | CB / 2 | 29 | 4,190.3 | wrong_patch 5, timeout 2 |
| 5 | B / 2 | 30 | 1,145.2 | wrong_patch 5, loop 1 |
| 6 | C / 2 | 30 | 4,380.8 | truncation 4, wrong_patch 2 |

## Task-level pattern

Tasks not solved in both repeats by all three arms (successes out of 2, C / CB / B): b6-cache-keys 2/1/0; c1-parse-size 0/0/0; c3-lru-cache 2/1/2; c4-wrap-text 0/0/2; c5-parse-query 2/0/0; c6-token-bucket 2/2/1; d3-uniq-lines 0/0/0; d5-env-to-json 0/0/2; e4-family-accuracy 0/0/0; e5-wilson-interval 1/2/2. Three tasks (c1-parse-size, d3-uniq-lines, e4-family-accuracy) fail in every attempt of both B and C.

The equal totals hide opposite failure modes. B-only successes total 5 task-attempts (c4-wrap-text and d5-env-to-json twice each, e5-wilson-interval once); for c4-wrap-text and d5-env-to-json, C's failures were truncations. C-only successes total 5 (b6-cache-keys and c5-parse-query twice each, c6-token-bucket once), which are B misses. C stalled (27 empty turns, 7 truncations); B never produced an empty turn and instead lost on wrong patches. This is descriptive: the tasks are few and per-task counts are two attempts.

## Supplements (never change the decision)

- CB vs C: accuracy difference -0.042 (95% interval -0.125 to +0.014); throughput ratio 0.84 (0.60 to 1.26). The 1024-token budget cut truncations from 7 to 3 but added 3 timeouts and 4 more wrong patches, and C's stall tasks (c4-wrap-text, d5-env-to-json) were not rescued. E53's structural stall conversion therefore did not translate into task success in this pool.
- B vs CB: accuracy difference +0.042 (interval -0.042 to +0.139); throughput ratio 4.03 (2.13 to 7.00).
- B budget-failure share: 0.

## Limits and caveats

- 36 scored tasks, two repeats. Repeats are not independent draws of tasks, so the bootstrap clusters on task. The interval is wide by construction.
- B samples at temperature 1.0 and C/CB at temperature 0, per the frozen arm definitions, so the arms differ in more than the model.
- C and CB ran close to the memory limit (free RAM down to 155 MB, swap up to 4 GB). It was tagged as a resource observation; no failure was attributed to it, but it is not excluded as a throughput factor.
- Reported throughput is single-slot, one machine (16 GB GPU), harness v5 with `PS_BUDGET_MODE=context`.
- Synthetic task families have ceilings (single_file_repair and test_driven_recovery are 12/12 for every arm) that limit discrimination.

## Possible follow-up (not started)

A larger or fresh task pool for B vs C would be needed to narrow the interval. This needs a new frozen protocol and a prospective sample-size choice. E55 remains parked.

## Provenance and credit

Frozen files and pins are recorded in `tmp/e54/freeze-hashes.json` (E52 fixtures sha256 06666f53...456e, protocol.json sha256 f1b2cbf5...0ac, Patchsmith HEAD 58b164207be0730f703e98880d1a939b09c71441). Run artifacts (rows, transcripts, resource logs) remain under git-ignored `tmp/e54/`. Credit: Thinking Machines Lab, Niko1221's Strata engine and contributors, the llama.cpp authors, PrismML (Bonsai runtime), Qwen and Unsloth.
