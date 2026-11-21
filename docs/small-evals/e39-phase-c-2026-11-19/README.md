# Phase C1: held-out route outcomes

Status: **complete**; 48/48 completed. C2 is not authorized.

C1 assigns multifile by a frozen two-source-file rule; this does not validate a runtime classifier. n=3 per cell. Cohorts are separate: set 1 informed v5b tuning; n09-n16 Edge0 v5b was not blind in E41. No promotion conclusion; default remains frontier-only.

Private runners and artifacts withheld. Run analyze.py here for selected aggregate checks.

The unchanged B2 retry launcher observes the original 300 s cooldown and 120 s clean window per MCP process. The cooldown consumes host wall time and about half of the unchanged 600 s deadline. RAM floor 0 is the documented deviation. Local seconds come from one saved run ledger per attempt, deduplicating repeated serialized tool results. Local error counts include blocked and other non-done statuses, with raw status/reason retained in details. Local-only pass requires a done ledger and passed local verification; repair requires final independent acceptance following a failed local attempt.

Token deltas use fixture-balanced means of differences of accepted-task medians against Phase A Sonnet. They are relative accounting, not subscription quota. Missing cells remain missing. Prompts, patches, transcripts and source solutions are excluded from public drafts. Subscription only; no API spend, commit, push or publication.

## blind2

Accepted/completed/planned: 24/24/24. Local done/error: 14/10; local-only passes 14; repairs 10; final passes 24. Timeouts 0; protected violations 0; CLI errors 0; missing usage 0.

| Clock | n | Median s | Q1-Q3 s | IQR s |
|---|---|---|---|---|
| local_seconds | 24 | 31.83599999999933 | 27.219250000000102 - 45.066500000000815 | 17.847250000000713 |
| cli_seconds | 24 | 354.594 | 345.63675 - 362.58575 | 16.949000000000012 |
| startup_wait | 24 | 300.4958575963974 | 300.30971843004227 - 300.6491768360138 | 0.3394584059715271 |
| adjusted_cli_seconds | 24 | 54.120449322700495 | 44.865884440422064 - 62.46716226768494 | 17.601277827262876 |

Token medians: {"input_tokens": 10.0, "cache_creation_input_tokens": 20877.0, "cache_read_input_tokens": 116572.5, "output_tokens": 986.5}.

Fixture-balanced mean median deltas (C1 minus A): {"input_tokens": {"n": 8, "mean": 4.5}, "cache_creation_input_tokens": {"n": 8, "mean": -4177.625}, "cache_read_input_tokens": {"n": 8, "mean": 58588.75}, "output_tokens": {"n": 8, "mean": 214}, "secs": {"n": 8, "mean": 338.041125}, "turns": {"n": 8, "mean": 0}, "adjusted_seconds": {"n": 8, "mean": 37.479631066799165}}.

| Fixture | Phase A Sonnet | E41 Edge0 v5b | C1 local | C1 final | C1 repairs |
|---|---|---|---|---|---|
| n09_rle | 3/3 | 3/3 | 2/3 | 3/3 | 1 (3 completed) |
| n10_ranges | 3/3 | 1/3 | 0/3 | 3/3 | 3 (3 completed) |
| n11_csv | 3/3 | 0/3 | 0/3 | 3/3 | 3 (3 completed) |
| n12_pager | 3/3 | 3/3 | 1/3 | 3/3 | 2 (3 completed) |
| n13_roman | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |
| n14_window | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |
| n15_suggest | 3/3 | 2/3 | 2/3 | 3/3 | 1 (3 completed) |
| n16_dictdiff | 3/3 | 3/3 | 3/3 | 3/3 | 0 (3 completed) |

## heldout1

Accepted/completed/planned: 24/24/24. Local done/error: 8/16; local-only passes 8; repairs 16; final passes 24. Timeouts 0; protected violations 0; CLI errors 0; missing usage 0.

| Clock | n | Median s | Q1-Q3 s | IQR s |
|---|---|---|---|---|
| local_seconds | 24 | 42.34350000000268 | 31.92974999999933 - 51.059000000001106 | 19.129250000001775 |
| cli_seconds | 24 | 367.2505 | 357.13225 - 378.00725 | 20.875 |
| startup_wait | 24 | 300.33732187747955 | 300.20788836479187 - 300.5536589026451 | 0.34577053785324097 |
| adjusted_cli_seconds | 24 | 66.92052987861632 | 56.615116346836075 - 77.63165437984465 | 21.016538033008572 |

Token medians: {"input_tokens": 14.0, "cache_creation_input_tokens": 24664.5, "cache_read_input_tokens": 195737.0, "output_tokens": 1339.5}.

Fixture-balanced mean median deltas (C1 minus A): {"input_tokens": {"n": 8, "mean": 7.5}, "cache_creation_input_tokens": {"n": 8, "mean": -2370.75}, "cache_read_input_tokens": {"n": 8, "mean": 96476.875}, "output_tokens": {"n": 8, "mean": 458}, "secs": {"n": 8, "mean": 348.326}, "turns": {"n": 8, "mean": 2.375}, "adjusted_seconds": {"n": 8, "mean": 47.85508037376403}}.

| Fixture | Phase A Sonnet | E41 Edge0 v5b | C1 local | C1 final | C1 repairs |
|---|---|---|---|---|---|
| n01_bucket | 3/3 | 3/3 | 1/3 | 3/3 | 2 (3 completed) |
| n02_semver | 3/3 | 3/3 | 2/3 | 3/3 | 1 (3 completed) |
| n03_wrap | 3/3 | 3/3 | 1/3 | 3/3 | 2 (3 completed) |
| n04_ledger | 3/3 | 1/3 | 1/3 | 3/3 | 2 (3 completed) |
| n05_bizdays | 3/3 | 2/3 | 1/3 | 3/3 | 2 (3 completed) |
| n06_lru | 3/3 | 2/3 | 0/3 | 3/3 | 3 (3 completed) |
| n07_template | 3/3 | 3/3 | 1/3 | 3/3 | 2 (3 completed) |
| n08_topo | 3/3 | 3/3 | 1/3 | 3/3 | 2 (3 completed) |

## Incidents and route-derived diagnostic

Excluded quota-interrupted attempts: [{"key": "C1-n13_roman-sonnet-1", "excluded_from_completed": true, "local_runs": [{"status": "done", "reason": "auto_finish", "seconds": 30.0940000000046, "turns": 8}], "final_acceptance": "unavailable: subscription usage stop before independent runner verification"}, {"key": "C1-n02_semver-sonnet-2", "excluded_from_completed": true, "local_runs": [{"status": "error", "reason": "execution_error", "seconds": 43.546999999991385, "turns": 11}], "final_acceptance": "unavailable: subscription usage stop before independent runner verification"}]. These local ledgers are preserved separately and do not count as completed passes or local failures.

Stop rows: [{"kind": "stop", "key": "C1-n09_rle-sonnet-0", "reason": "preflight_implementation_error"}, {"kind": "stop", "key": "C1-n13_roman-sonnet-1", "reason": "usage_limit"}, {"kind": "stop", "key": "C1-n02_semver-sonnet-2", "reason": "usage_limit"}].

Every completed timeout remains a censored failure and is not retried at a longer timeout. Incomplete usage-stop attempts are excluded from completed-trial estimates and must be archived before resuming the same key. Local failures: {"C1-n09_rle-sonnet-0": [{"status": "blocked", "reason": "loop_detected", "seconds": 30.01600000000326, "turns": 11}], "C1-n10_ranges-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 31.67199999999866, "turns": 10}], "C1-n11_csv-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 32.0, "turns": 10}], "C1-n10_ranges-sonnet-1": [{"status": "blocked", "reason": "loop_detected", "seconds": 57.125, "turns": 21}], "C1-n11_csv-sonnet-1": [{"status": "blocked", "reason": "loop_detected", "seconds": 25.593000000000757, "turns": 10}], "C1-n12_pager-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 36.125, "turns": 11}], "C1-n15_suggest-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 31.547000000005937, "turns": 8}], "C1-n10_ranges-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 54.32799999999406, "turns": 18}], "C1-n11_csv-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 38.8440000000046, "turns": 13}], "C1-n12_pager-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 23.95300000000134, "turns": 9}], "C1-n02_semver-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 55.06199999999808, "turns": 14}], "C1-n03_wrap-sonnet-0": [{"status": "blocked", "reason": "loop_detected", "seconds": 16.5, "turns": 8}], "C1-n04_ledger-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 45.25, "turns": 10}], "C1-n06_lru-sonnet-0": [{"status": "blocked", "reason": "loop_detected", "seconds": 42.96899999999732, "turns": 11}], "C1-n08_topo-sonnet-0": [{"status": "error", "reason": "execution_error", "seconds": 33.45299999999406, "turns": 12}], "C1-n01_bucket-sonnet-1": [{"status": "blocked", "reason": "loop_detected", "seconds": 18.125, "turns": 6}], "C1-n05_bizdays-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 32.375, "turns": 13}], "C1-n06_lru-sonnet-1": [{"status": "error", "reason": "execution_error", "seconds": 39.82799999999406, "turns": 11}], "C1-n07_template-sonnet-1": [{"status": "blocked", "reason": "loop_detected", "seconds": 28.985000000000582, "turns": 14}], "C1-n01_bucket-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 30.593999999997322, "turns": 13}], "C1-n03_wrap-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 56.90699999999197, "turns": 23}], "C1-n04_ledger-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 23.64100000000326, "turns": 8}], "C1-n05_bizdays-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 41.71800000000803, "turns": 10}], "C1-n06_lru-sonnet-2": [{"status": "blocked", "reason": "loop_detected", "seconds": 70.8289999999979, "turns": 19}], "C1-n07_template-sonnet-2": [{"status": "blocked", "reason": "max_turns", "seconds": 47.030999999988126, "turns": 25}], "C1-n08_topo-sonnet-2": [{"status": "error", "reason": "execution_error", "seconds": 15.48399999999674, "turns": 7}]}.

C1 route-derived eligibility projection: {"local_completed": 48, "local_pending": 0, "local_disagreements": 1, "local_disagreement_rate": 0.020833333333333332, "frontier_completed": 0, "frontier_easy": 0, "frontier_easy_rate": null, "orphan_outcomes": 0, "promotion_bar": 0.1, "struggle_turns": 10, "below_bar": true, "note": "Descriptive proxy only: frontier success does not establish local correctness. No automatic promotion."}. Mode is transformed to shadow; final outcome, turns and seconds are independent runner measurements. These are not live B1 shadow observations. Repaired local failures count as final passes in this diagnostic; no promotion conclusion.


Preflight implementation incident: the original dry path omitted offline router assertions and misnamed fixture rows; baseline/reference checks passed and the label rule executed at plan freeze. The original smoke was stopped during cooldown, with no saved local attempt or completed trial at that stop. Buffered host output/usage is unavailable. The faulty frozen runner is archived; the user authorized correction, and revision 2 passed all 16 complete dry checks before a fresh server session. Current results appear above.

Selected public evidence (published 2026-11-21). Private source, prompts, generated code, traces and machine paths withheld. Aggregate checks do not independently rescore solutions.
