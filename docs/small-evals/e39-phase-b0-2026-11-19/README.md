# Phase B: plugin accounting

## Publication update - 2026-11-19

User-authorized selected evidence release. Historical local-only/hold and pending-verification statements below describe preparation time and are superseded by this dated update.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

## Historical run and analysis record

B0 status: **complete**. 21/21 completed; 21 accepted by independent tests. Updated 2026-11-19T04:48:33.607555+00:00.

B1 and B2 are not run in this authorization. No plugin overhead, local-token saving, live shadow outcome or routing accuracy conclusion is available. E39 items 1 and 2 remain open; default stays frontier-only.

Commands: `python -B scripts/e39_plugin_accounting.py --arm B0 --dry`; smoke `--arm B0 --only B0-bug1-sonnet-0`; full/resume `python -B scripts/e39_plugin_accounting.py --arm B0`. Offline refresh: `python -B scripts/e39_plugin_accounting_summary.py`.

## Frozen conditions

Seven original categorized fixtures, Sonnet, 3 repeats each, repeat-major order. Task text from eval/run_eval.py TASKS; categories checked before launch. Source HEAD, directory SHA-256, CLI version, exact task text, runner hash and prompt template frozen in private plan.json. Source repo read-only. No reference solutions copied.

Prompt (unchanged Phase A): `You are fixing a small repo in the current directory. Task: {task}` followed by a newline and `Run the project's tests to verify ({test_command}). Do not edit test files. Reply with one line when done.`

Python verification: `python -B -m unittest discover -q`; JavaScript: `node --test`, as in run_eval.py. Protected files include Python tests/configuration and JavaScript .test./.spec. files. Restore their original bytes before independent verification; any detected protected change rejects the task. 600 s CLI timeout, acceptEdits, no-session-persistence; same allowed tools and provider-env stripping as Phase A. No plugin configuration added. Edge0 process guard and Manila December 10 start deadline retained. Existing llama-server is untouched and is not the edge0-infer process named in the B0 guard.

No RAM-floor deviation applies to B0; the B1/B2 override and default-floor probe remain unrun.

## Accepted tasks: median [IQR]

| Fixture | Accepted/completed/planned | Input | Cache create | Cache read | Output | Turns | Seconds |
|---|---|---|---|---|---|---|---|
| bug1 | 3/3/3 | 8.00 [0.00] | 26204.00 [6.00] | 94065.00 [6.50] | 409.00 [3.00] | 4.00 [0.00] | 16.42 [4.88] |
| bug2 | 3/3/3 | 10.00 [0.00] | 26356.00 [22.00] | 134972.00 [13.50] | 508.00 [22.00] | 5.00 [0.00] | 18.28 [1.23] |
| feature | 3/3/3 | 8.00 [2.00] | 26255.00 [171.00] | 94165.00 [41359.00] | 398.00 [79.00] | 4.00 [1.00] | 16.72 [1.81] |
| multifile | 3/3/3 | 6.00 [0.00] | 23979.00 [75.00] | 91901.00 [17.50] | 294.00 [1.00] | 3.00 [0.00] | 13.17 [0.49] |
| refactor | 3/3/3 | 6.00 [0.00] | 23690.00 [8.50] | 91876.00 [5.00] | 244.00 [5.50] | 3.00 [0.00] | 12.22 [0.31] |
| offbyone | 3/3/3 | 8.00 [3.00] | 26348.00 [1471.50] | 94250.00 [41427.00] | 475.00 [156.50] | 5.00 [1.50] | 14.95 [2.53] |
| javascript | 3/3/3 | 6.00 [0.00] | 23947.00 [16.50] | 91740.00 [6.00] | 373.00 [11.00] | 4.00 [0.00] | 14.80 [0.20] |

Inclusive quartiles; IQR = Q3 minus Q1. Only independently accepted tasks contribute to these metrics. Missing observations are excluded, not zero-filled. Subscription quota weighting is unpublished: tokens measure relative cost, not plan percentages.

## Incidents and limits

All seven dry baseline checks failed as expected. Smoke bug1 repeat 0 passed 2 independent tests, changed scorer.py only, recorded 4 turns and 16.422 s. No model server was started, stopped or restarted.

Timeouts: 0; CLI errors: 0; protected-file violations: 0; missing usage: 0. Resolved models: claude-haiku-5-5, claude-sonnet-5-5.

The public checkout full verifier currently reports a hash mismatch in the unrelated pre-existing E41 harness-comparison README. That artifact is left untouched. B0 selected-file hashes and portable aggregate recomputation are checked separately; the full public checkout is not claimed clean.

Rejected trials: none recorded. Stops: [].

Usage is the top-level Claude CLI usage bundle. model_usage is retained separately and can include a small auxiliary Haiku call in a Sonnet trial; those entries are not additional Haiku-arm trials. CLI reported list-price cost is not subscription spend.

Tiny synthetic fixtures, three repeats per cell; not held out and no routing promotion. No shadow_report run because B1 has no real rows. Private prompts, CLI JSON, patches and hashes stay in tmp/e39-plugin-accounting-2026-11/B0. Local unpublished draft only. Raw artifacts and private implementation/fixture sources are withheld; this package supports aggregate recomputation, not independent re-scoring.

## November 19 Phase B follow-up

The B0 record above is the baseline snapshot. [Combined Phase B local draft](../e39-phase-b-2026-11-19/README.md): B1 completed 36/36 independent passes; B2 smoke passed in the frontier host but reached no local attempt due to the process-start cooldown, so 14 remaining trials were skipped. No routing-promotion conclusion; publication remains deferred.
