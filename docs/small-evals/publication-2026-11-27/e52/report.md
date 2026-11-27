> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E52 results - private

Date: 2026-11-25. Status: complete execution; frozen reading-rule decision **`not_advance`**. No push, publication, public-evidence sync, promotion or router change.

## Observed result

Both Stage 1 compatibility gates passed. All four scored blocks completed in the frozen A1, B1, B2, A2 order, with 72 attempts per arm and no boundary violation. A (Qwen3.6-27B UD-IQ3_XXS) succeeded on 51/72; B (Ternary Bonsai 2.5 27B PTQ1_0) on 57/72. B's success rate is 0.7917, below the prospective 0.80 threshold, so the frozen rule does not advance B. This is a study-selection result for this pool and configuration.

The development rows are unscored and excluded from every scored table and the analyzer comparison. Every scored failure remains in the denominator. Success means the saved runner row passed its independent acceptance requirements; no model-written patch was judged for quality by the reporting agent.

## Stage 1 compatibility gate

| Gate evidence | A | B |
|---|---:|---:|
| Result | PASS | PASS |
| Context | 32,768 | 32,768 |
| Health within 600 s, without observed OOM | yes | yes |
| Successful read_file tool results | 8 | 9 |
| Successful glob results | 0 | 1 |
| Successful edit_file / write_file results | 6 / 1 | 6 / 2 |
| Visible run_tests tool results | 6 | 8 |
| Finish tool results | 4 | 4 |
| Tool-result -> assistant continuations | 16 | 18 |
| Parsed tool argument objects | 27 | 30 |
| Malformed calls in development rows | 0 | 0 |
| Reasoning markers in tool arguments | 0 | 0 |
| Reasoning characters, separately recorded | 9561 | 3809 |

Evidence: `tmp/e52/dev-{A,B}-launch.json`, `-health.json`, `-warmup.json`, `-shutdown.json`, `dev-{A,B}.jsonl`, and `transcripts/b0-{A,B}-r1-dev-*.jsonl` / `.requests.json`. Message-role filtering excludes interleaved event records when counting continuations. Tool arguments parsed as JSON objects; no `<think>`, `</think>` or `reasoning_content` markers were observed inside them. Reasoning was recorded separately in request metadata, never used to repair calls. Gate observations did not reveal reasoning embedded in arguments. Both owned servers exited.

| Development task | A failure_code | A seconds | A turns | B failure_code | B seconds | B turns |
|---|---|---:|---:|---|---:|---:|
| dev-a-clamp | success | 21.110 | 3 | success | 13.921 | 3 |
| dev-b-fullname | success | 26.609 | 4 | success | 9.359 | 4 |
| dev-c-ordinal | success | 43.969 | 3 | success | 13.312 | 3 |
| dev-d-upper | success | 17.265 | 4 | success | 18.360 | 6 |
| dev-e-mean | success | 24.969 | 3 | success | 12.405 | 3 |
| dev-f-lastindex | success | 34.562 | 5 | success | 8.499 | 5 |

## Scored per-arm statistics

Attempt-level resource extrema below are the analyzer's saved-row sampler values. Full server-lifetime resource-log extrema, including load and warmup, are reported separately because the sampling windows differ.

| Metric | A | B |
|---|---:|---:|
| Attempts (n) | 72 | 72 |
| Successes | 51 | 57 |
| Success rate | 0.7083 | 0.7917 |
| Wilson 95% interval | [0.5949, 0.8006] | [0.6843, 0.8695] |
| Summed task seconds | 5,573.806 | 1,989.787 |
| Verified tasks per hour | 32.940 | 103.127 |
| Failure-code counts (including success) | success: 51; wrong_patch: 18; empty_turn: 1; server_error: 1; loop: 1 | success: 57; wrong_patch: 11; server_error: 2; loop: 1; truncation: 1 |
| Latency median, all attempts (s) | 42.281 | 20.133 |
| Latency median, successes (s) | 41.453 | 17.281 |
| Output tokens, including reasoning | 159851 | 92697 |
| Tool calls | 408 | 563 |
| Visible-test runs | 88 | 102 |
| Recovered-after-red attempts | 7 | 5 |
| Malformed calls | 1 | 2 |
| Empty turns | 11 | 0 |
| Request length stops | 8 | 3 |
| Blocked edit attempts | 1 | 0 |
| Peak GPU (MiB, row sampler) | 13,881.000 | 8,422.000 |
| Minimum free RAM (bytes, row sampler) | 538796032 | 1361809408 |
| Peak swap (bytes, row sampler) | 6960054272 | 2736267264 |
| Boundary violations | 0 | 0 |

Verified tasks per hour = 3,600 * successes / summed end-to-end task seconds, including failures, thinking, tools, visible tests and acceptance. Server load and warmup are reported separately and are not added to this frozen metric. Token totals are those saved by the runner; no unrecorded tokens are imputed for failed server responses.

Neither arm is at an overall ceiling or floor. There are family ceilings (12/12): single-file repair for both arms; multi-file change and test-driven recovery for B. These small synthetic-family ceilings limit discrimination and do not establish broad reliability.

## Per-family success

| Family | A successes / n | B successes / n |
|---|---:|---:|
| feature_edge_cases | 5 / 12 | 6 / 12 |
| multi_file_change | 10 / 12 | 12 / 12 |
| new_script | 7 / 12 | 5 / 12 |
| scorer_summary_repair | 9 / 12 | 10 / 12 |
| single_file_repair | 12 / 12 | 12 / 12 |
| test_driven_recovery | 8 / 12 | 12 / 12 |

## Per-block success, stop and startup

| Block | Arm / repeat | Successes / n | Summed task seconds | Stop reason | Load seconds | Warmup seconds | Owned server exited |
|---|---|---:|---:|---|---:|---:|---|
| b1 | A / 1 | 27 / 36 | 2962.962 | completed | 5.562 | 4.188 | yes |
| b2 | B / 1 | 29 / 36 | 1019.239 | completed | 3.546 | 0.813 | yes |
| b3 | B / 2 | 28 / 36 | 970.548 | completed | 3.562 | 0.766 | yes |
| b4 | A / 2 | 24 / 36 | 2610.844 | completed | 5.594 | 4.016 | yes |

| Development launch | Load seconds | Warmup seconds |
|---|---:|---:|
| dev-A | 20.828 | 5.594 |
| dev-B | 4.063 | 0.797 |

## Analyzer comparison and decision - verbatim

Source: `python scripts/e52_analyze.py --out tmp/e52/summary.json`. The selected comparison and decision fields below preserve the analyzer's values and JSON formatting.

```json
{
  "comparison_B_vs_A": {
    "accuracy_diff": 0.0834,
    "throughput_ratio": 3.130761173106941,
    "ratio_defined": true,
    "bootstrap": {
      "accuracy_diff_ci95": [
        -0.05555555555555547,
        0.2222222222222222
      ],
      "ratio_ci95": [
        2.0594504283352526,
        4.731874863237566
      ],
      "resamples": 10000,
      "undefined_ratio_resamples": 0,
      "seed": 5252
    }
  },
  "decision": "not_advance"
}
```

The analyzer reports `complete: true`, `stopped_blocks: []`, B rate >= 0.80 false, accuracy-difference lower bound > -0.10 true, throughput-ratio lower bound > 1 true, and no boundary violation true. There were three serving-error attempts; B's budget-failure share is 0.0667. Accuracy thresholds are prospective selection rules, not proven noninferiority.

## Server-lifetime resource extrema

From each `*-resources.jsonl`, including startup, warmup and task execution. RAM and swap are system-wide, not attributed solely to the server. Low-RAM samples mean available RAM < 4 GiB; sample counts are descriptive and not exact event durations. Logs sample approximately every two seconds plus collection overhead.

| Launch | Samples | Peak GPU MiB | Minimum free RAM bytes (GiB) | Peak swap bytes (GiB) | Peak GPU degrees C | Low-RAM samples | Monitor errors |
|---|---:|---:|---:|---:|---:|---:|---:|
| dev-A | 91 | 14006 | 549908480 (0.512) | 1141645312 (1.063) | 74 | 76 | 0 |
| dev-B | 41 | 8426 | 3147370496 (2.931) | 1046667264 (0.975) | 70 | 9 | 0 |
| b1-A | 1443 | 13880 | 440721408 (0.410) | 6960054272 (6.482) | 79 | 151 | 0 |
| b2-B | 499 | 8422 | 1959895040 (1.825) | 2154840064 (2.007) | 78 | 159 | 0 |
| b3-B | 476 | 8422 | 1783021568 (1.661) | 2736267264 (2.548) | 78 | 70 | 0 |
| b4-A | 1272 | 13881 | 554082304 (0.516) | 3228307456 (3.007) | 79 | 87 | 0 |

## Observed anomalies and limits of diagnosis

- Low-memory samples occurred during all six launches. Every prelaunch check passed: devA 12.737 GiB; devB 12.883 GiB; b1 13.001 GiB; b2 12.819 GiB; b3 13.201 GiB; b4 13.136 GiB free RAM. Prelaunch GPU use was 467 MiB for devA and 333 MiB for every subsequent launch, with no competing model process. Low-memory samples were retained, not rerun.
- Three `server_error` rows report HTTP 500 because the runtime could not parse tool-call arguments as JSON: `b2-B-r1-d5-env-to-json`, `b2-B-r1-d2-todo-cli`, and `b4-A-r2-c1-parse-size`. They remain serving errors under the frozen classifier. The analyzer records malformed-call counts A 1, B 2. There was no unrecorded parser repair or retry. Each serving error was followed by a non-serving-error row, so no two-consecutive-error stop fired.
- B has one `truncation` row, `b3-B-r2-d5-env-to-json` (saved reason `loop_detected`, one request length stop). Classification priority is retained as saved. A has one `empty_turn` failure (`b1-A-r1-d1-csv-stats`, saved reason `max_turns`); empty-turn totals count transcript events, not just failed attempts. Request length-stop totals are A 8 and B 3, distinct from task failure codes.
- One blocked edit attempt is recorded for `b1-A-r1-d1-csv-stats`. The saved boundary-violation counts remain zero; a blocked edit is not reclassified as a boundary violation.
- No recorded scored prompt exceeded the 24,000 harness-input budget: maximum `max_prompt_tokens` was A 9,771 and B 5,230. Development maxima were A 2,051 and B 2,358, also below budget. No row has `context_budget`, `oom`, `timeout`, `output_budget` or `boundary_violation` as its reason/failure code. A failed request may lack usage metadata; no missing prompt/token usage is inferred.
- Peak GPU temperature was 79degrees C. Resource logs contain memory, utilization, temperature and power, but no clock or throttle-reason field. Thermal throttling is not established by these logs; temperature alone cannot determine it.
- No block stopped early, and no attempt, marker, row or block was restarted, replaced, removed or hand-edited. No patch quality review was performed. Sealed suites and reference files were not opened for inspection or placed into a model prompt.

## Hypotheses

No causal explanation for the accuracy, speed, low-memory observations or tool-format failures is established. Memory pressure, model/runtime differences and order effects could matter, but these measurements do not isolate them. No diagnostic model runs, tuning, sampler changes or additional attempts were added.

## Order limitation - frozen protocol text

> **Order: balanced blocks, not per-task alternation.** Two 27B models cannot be resident together on 16 GB, so alternating per task would mean a server restart per task. Blocks: **A repeat 1, B repeat 1, B repeat 2, A repeat 2** (36 tasks each). Repeat 1 uses a task order shuffled with seed 5252; repeat 2 uses the exact reverse. Order limitation (model load state, thermal drift) is disclosed, not corrected.

## Not claimed - frozen protocol text

> No FP16 equivalence, no isolation of ternary compression (base revisions, quant, reasoning and runtime all differ), no coding-ability claim beyond a small synthetic pool, no router change, no E39 resolution. Fresh synthetic tasks authored with the references in view and never run against either model: difficulty is uncalibrated, so a ceiling or floor is possible.

## Verification and private provenance

- Frozen protocol: e52-bonsai-patchsmith-protocol.md (private source reference withheld). Execution used the frozen `e52_server_run.py`, `e52_run.py` and `e52_analyze.py` without edits; no protected scripts or Patchsmith sources were modified.
- Preflight directory contained only `sealed/`, `tasks/`, `fixtures.json`, `freeze-hashes.json` and `protocol.json`; no prior rows/dev/stop/run outputs existed.
- Preflight test command: `python -m pytest scripts/test_e52.py -q -p no:cacheprovider`, with `E52_TMP=[withheld local path]` and `E52_WORK=[withheld local path]`: **25 passed in 232.51 s**. Same post-run command/environment: **25 passed in 228.20 s**. Nonfatal pytest plugin/deprecation and unknown `slow` mark warnings were present.
- Final `R.check_frozen()` returned `ok`. Its implemented source/fixture checks passed; sealed contents were not manually inspected. Patchsmith nested checkout is clean at pinned HEAD `58b164207be0730f703e98880d1a939b09c71441`.
- All six shutdown records confirm `owned_server_exited: true`. Final GPU check after scored runs: 334 MiB, no llama-server, strata-inkling, ollama or edge0-infer process. No unowned process was stopped or replaced.
- Four required SHA-256 hashes matched before execution and after the scored runs (case-insensitive comparison):

| File | SHA-256, unchanged |
|---|---|
| `tmp/e45/log.jsonl` | `2d40ccd3e22a0c1ffa735854726a49e0562e86fbbf91431939ce3211d47c437d` |
| `tmp/e45v2/cohort-seal.json` | `157b16a24aa6074f134f35a3ef5d063a1b12792d96ff40b4fb372d037266f012` |
| `tmp/e52/fixtures.json` | `06666f53cf4e433c0f269307ebacefc9bac2103f989405921a543c463943456e` |
| `tmp/e52/protocol.json` | `04f87627d5f68f299f8c6c67a9c3420d52ba5548415ab8931260aab11f2aee46` |

Raw evidence remains private and git-ignored under `tmp/e52/`: saved rows, stop records, launch/health/warmup/shutdown records, resource logs and transcripts. Only this report is selected for commit. Existing unrelated root and nested-repository changes are preserved. No public checkout was touched, no paid API or frontier call was used, and nothing was pushed or published. Public evidence synchronization is explicitly deferred by this run's private/no-publication instruction.

Credit: PrismML for the Bonsai model and runtime fork; Qwen for the base models; Unsloth for the control quantization; the llama.cpp authors for the runtime foundation.
