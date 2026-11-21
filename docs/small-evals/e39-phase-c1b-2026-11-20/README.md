# Phase C1b: held-out route outcomes

Status: **complete**; 48/48 recorded as completed trial rows; 0 unstarted keys remain. C2b is not authorized.

C1b assigns multifile by a frozen two-source-file rule; this does not validate a runtime classifier. n=3 per cell. Cohorts are separate: set 1 informed v5b tuning; n09-n16 Edge0 v5b was not blind in E41. No promotion conclusion; default remains frontier-only.

Private runners and artifacts withheld. Run analyze.py here for selected aggregate checks.

The unchanged B2 retry launcher observes the original 300 s cooldown and 120 s clean window per MCP process. The cooldown consumes host wall time and about half of the unchanged 600 s deadline. RAM floor 0 is the documented deviation. Local seconds come from one saved run ledger per attempt, deduplicating repeated serialized tool results. Local error counts include blocked and other non-done statuses, with raw status/reason retained in details. Local-only pass requires a done ledger and passed local verification; repair requires final independent acceptance following a failed local attempt.

Token deltas use fixture-balanced means of differences of accepted-task medians against Phase A Sonnet. They are relative accounting, not subscription quota. Missing cells remain missing. Prompts, patches, transcripts and source solutions are excluded from public drafts. Subscription only; no API spend, push or publication. The authorized I/O fix is a local Patchsmith feature-branch commit only.

## blind2

Accepted/completed/planned: 24/24/24. Local done/error: 17/7; local-only passes 17; repairs 7; final passes 24. Timeouts 0; protected violations 0; CLI errors 0; missing usage 0.

| Clock | n | Median s | Q1-Q3 s | IQR s |
|---|---|---|---|---|
| local_seconds | 24 | 28.05500000000029 | 24.300750000002154 - 33.05824999999095 | 8.757499999988795 |
| cli_seconds | 24 | 351.14 | 343.57849999999996 - 362.7575 | 19.17900000000003 |
| startup_wait | 24 | 300.3910118341446 | 300.19510012865067 - 300.6645093560219 | 0.4694092273712158 |
| adjusted_cli_seconds | 24 | 51.065492286682144 | 43.16066106891631 - 62.40178246927259 | 19.241121400356278 |

Token medians: {"input_tokens": 10.0, "cache_creation_input_tokens": 20764.5, "cache_read_input_tokens": 116526.0, "output_tokens": 954.5}.

Fixture-balanced mean median deltas (C1b minus A): {"input_tokens": {"n": 8, "mean": 3.5}, "cache_creation_input_tokens": {"n": 8, "mean": -4932}, "cache_read_input_tokens": {"n": 8, "mean": 43324}, "output_tokens": {"n": 8, "mean": 84.75}, "secs": {"n": 8, "mean": 332.2655}, "turns": {"n": 8, "mean": -0.75}, "adjusted_seconds": {"n": 8, "mean": 31.923128506422042}}.

| Fixture | Phase A Sonnet | E41 Edge0 v5b | C1 local | C1b local | C1b final | C1b repairs |
|---|---|---|---|---|---|---|
| n09_rle | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 1 (3 completed) |
| n10_ranges | 3/3 | 1/3 | 0/3 | 0/3 | 3/3 | 3 (3 completed) |
| n11_csv | 3/3 | 0/3 | 0/3 | 0/3 | 3/3 | 3 (3 completed) |
| n12_pager | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 0 (3 completed) |
| n13_roman | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |
| n14_window | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |
| n15_suggest | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 0 (3 completed) |
| n16_dictdiff | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |

## heldout1

Accepted/completed/planned: 24/24/24. Local done/error: 19/5; local-only passes 19; repairs 5; final passes 24. Timeouts 0; protected violations 0; CLI errors 0; missing usage 0.

| Clock | n | Median s | Q1-Q3 s | IQR s |
|---|---|---|---|---|
| local_seconds | 24 | 30.476999999998952 | 23.097999999998137 - 46.346999999997934 | 23.248999999999796 |
| cli_seconds | 24 | 363.4295 | 348.89050000000003 - 379.02725000000004 | 30.136750000000006 |
| startup_wait | 24 | 300.638968706131 | 300.43178445100784 - 300.8185033798218 | 0.3867189288139343 |
| adjusted_cli_seconds | 24 | 62.73660959434511 | 48.095976582050326 - 78.3265911421776 | 30.23061456012728 |

Token medians: {"input_tokens": 12.0, "cache_creation_input_tokens": 20854.0, "cache_read_input_tokens": 150784.0, "output_tokens": 1035.0}.

Fixture-balanced mean median deltas (C1b minus A): {"input_tokens": {"n": 8, "mean": 5}, "cache_creation_input_tokens": {"n": 8, "mean": -3664.5}, "cache_read_input_tokens": {"n": 8, "mean": 52730.375}, "output_tokens": {"n": 8, "mean": 350.375}, "secs": {"n": 8, "mean": 346.322125}, "turns": {"n": 8, "mean": 1}, "adjusted_seconds": {"n": 8, "mean": 45.643235308170325}}.

| Fixture | Phase A Sonnet | E41 Edge0 v5b | C1 local | C1b local | C1b final | C1b repairs |
|---|---|---|---|---|---|---|
| n01_bucket | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 0 (3 completed) |
| n02_semver | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 0 (3 completed) |
| n03_wrap | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 0 (3 completed) |
| n04_ledger | 3/3 | 1/3 | 1/3 | 2/3 | 3/3 | 1 (3 completed) |
| n05_bizdays | 3/3 | 2/3 | 1/3 | 1/3 | 3/3 | 2 (3 completed) |
| n06_lru | 3/3 | 2/3 | 0/3 | 3/3 | 3/3 | 0 (3 completed) |
| n07_template | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | 2 (3 completed) |
| n08_topo | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 0 (3 completed) |


Revision 2 Patchsmith HEAD: `2203eb0701265695511f2a4077d142b01aeee464`. Revision-1 smoke row and all artifacts are archived and excluded as an operational pre-fix stdin stall; they do not enter any revision-2 count. One local feature-branch fix commit was authorized; no push or publication.

## Harness comparison and prediction

Frozen MCP harness env: {"PS_HARNESS": "v5", "PS_MAX_TURNS": "30", "PS_CTX_BUDGET": "30000", "PS_BUDGET_MODE": "context"}. The route two-strike rule remains active. C1b revision 2 runs a patched Patchsmith HEAD (I/O fix only), unlike C1: stdin=subprocess.DEVNULL at three git ls-files calls; no router, gate, category or default changes. The harness environment is the experimental change; C1b versus E41 retains the route wrapper difference. n=3 per cell; cohorts are never pooled.

| Local stop reason | C1 | C1b completed attempts |
|---|---|---|
| done | 22 | 36 |
| loop_detected | 13 | 0 |
| repeated_test_failure | 12 | 12 |
| max_turns | 1 | 0 |
| other | 0 | 0 |
| Unavailable (no saved local ledger) | 0 | 0 |

Prediction comparison (partial counts cannot confirm/refute the full-cohort prediction): {"blind2": {"predicted": 15, "observed": 17, "completed": 24, "planned": 24}, "heldout1": {"predicted": 18, "observed": 19, "completed": 24, "planned": 24}}.


Revision-2 smoke completed in 357.969 s including cooldown: 30/30000 header, nine local turns, 29.141 local seconds, repeated_test_failure and a successful Sonnet repair. Initial-input text is omitted by the transcript. The user accepted offline non-empty v5 preload verification from saved turn-1 context_est as passing the smoke gate. The counted smoke and original smoke_preload_unverified stop remain unchanged; appended user-approved resume notes resolve that historical stop. All 48 revision-2 keys are now complete.

## Incidents and route-derived diagnostic

Excluded quota-interrupted attempts: [{"key": "C1b-n02_semver-sonnet-2", "excluded_from_completed": true, "local_runs": [{"status": "done", "reason": "auto_finish", "seconds": 27.09299999999348, "turns": 6}], "final_acceptance": "unavailable: subscription usage stop before independent runner verification"}]. These local ledgers are preserved separately and do not count as completed passes or local failures.

Stop rows: [{"kind": "stop", "key": "C1b-n09_rle-sonnet-0", "reason": "smoke_preload_unverified"}, {"kind": "stop", "key": "C1b-n02_semver-sonnet-2", "reason": "usage_limit"}].

Every completed timeout remains a censored failure and is not retried at a longer timeout. Incomplete usage-stop attempts are excluded from completed-trial estimates and must be archived before resuming the same key. Local failures: {"C1b-n09_rle-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 29.14100000000326, "turns": 9, "stop_reason": "repeated_test_failure"}], "C1b-n10_ranges-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 33.030999999988126, "turns": 9, "stop_reason": "repeated_test_failure"}], "C1b-n11_csv-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 28.640999999988708, "turns": 8, "stop_reason": "repeated_test_failure"}], "C1b-n10_ranges-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 33.13999999999942, "turns": 10, "stop_reason": "repeated_test_failure"}], "C1b-n11_csv-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 23.219000000011874, "turns": 6, "stop_reason": "repeated_test_failure"}], "C1b-n10_ranges-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 33.98399999999674, "turns": 9, "stop_reason": "repeated_test_failure"}], "C1b-n11_csv-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 25.077999999994063, "turns": 7, "stop_reason": "repeated_test_failure"}], "C1b-n05_bizdays-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 25.485000000000582, "turns": 6, "stop_reason": "repeated_test_failure"}], "C1b-n07_template-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 42.54700000000594, "turns": 9, "stop_reason": "repeated_test_failure"}], "C1b-n04_ledger-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 20.578000000008615, "turns": 6, "stop_reason": "repeated_test_failure"}], "C1b-n05_bizdays-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 45.88999999999942, "turns": 7, "stop_reason": "repeated_test_failure"}], "C1b-n07_template-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 44.187999999994645, "turns": 9, "stop_reason": "repeated_test_failure"}]}.

C1b route-derived eligibility projection: {"local_completed": 48, "local_pending": 0, "local_disagreements": 0, "local_disagreement_rate": 0.0, "frontier_completed": 0, "frontier_easy": 0, "frontier_easy_rate": null, "orphan_outcomes": 0, "promotion_bar": 0.1, "struggle_turns": 10, "below_bar": true, "note": "Descriptive proxy only: frontier success does not establish local correctness. No automatic promotion."}. Mode is transformed to shadow; final outcome, turns and seconds are independent runner measurements. These are not live B1 shadow observations. Repaired local failures count as final passes in this diagnostic; no promotion conclusion.

Selected public evidence (published 2026-11-21). Private source, prompts, generated code, traces and machine paths withheld. Aggregate checks do not independently rescore solutions.

User-approved smoke-gate resolution: offline verification from saved files (turn-1 context_est 2776; approximately 1300 without preload; non-empty preload recomputation 2737, 4021 characters) was accepted as passing. Original smoke trial remains counted; smoke_preload_unverified stop row remains historical and is followed by an appended resume note. Same revision 2, unchanged plan and runners, Patchsmith HEAD 2203eb0701265695511f2a4077d142b01aeee464. No further code changes.

The configuration explanation is descriptively supported: both cohort counts are closer to the prediction than C1. These are descriptive n=3-per-fixture comparisons. blind2: 17/24 local passes versus predicted 15/24, 24/24 final passes, 7 repairs; heldout1: 19/24 local passes versus predicted 18/24, 24/24 final passes, 5 repairs. C1 local baselines: heldout1 8/24, blind2 14/24. Cohorts remain separate; unchanged route two-strike rule and disclosed I/O fix limit attribution. No promotion; default stays frontier-only.
