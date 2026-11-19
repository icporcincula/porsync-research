# E39 B2 retry results (separate cohort; 2026-11-19)

## Publication update - 2026-11-19

User-authorized selected evidence release. Historical local-only/hold and pending-verification statements below describe preparation time and are superseded by this dated update.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

## Historical run and analysis record

B2-retry: 15/15 completed, 15 independently accepted, 15 local attempts in completed trials. Failures: []; stop reasons: ['usage_limit']. B0 21/21 and B1 36/36 retained without reruns; original B2 smoke/skip remains in the separate combined Phase B package.

Root cause: a fresh router process initializes its in-memory HTTP400 timestamp to now as an unknown-history precaution. No persisted cooldown file was read, and the router probe only checks TCP/RAM. A direct unchanged Edge0 request returned HTTP 200. The retry-only external launcher observes the original five-minute cooldown in the same MCP process; it never clears timestamps or shortens gates. Source checkout, category table, shadow/routing defaults and frontier-only default remain unchanged. Floor 0 remains a disclosed accounting/calibration deviation, not a recommended default.

Commands: `python -B scripts/e39_b2_retry.py --arm B2 --dry`; smoke with `--only B2-bug1-sonnet-0`; full/resume `python -B scripts/e39_b2_retry.py --arm B2`; offline `python -B scripts/e39_b2_retry_summary.py` and `python -B scripts/e39_b2_retry_record.py`. Prompt, fixture/trial order, verification, 600-second CLI timeout and Dec 10 deadline remain the original logic. Completed keys skip on resume; usage stops are retained. The source checkout and category table are unchanged.

Smoke: actual Edge0 transcript and proposal, 2/2 independent tests pass, local ledger 11.906 s; CLI total 327.093 s including 300.403 s observed startup wait. Whole-cohort local-ledger median 19.70300000000134 s across 15 saved local runs; local statuses {'done': 13, 'error': 2}; warmup median 300.50956177711487 s. These clocks measure different work. The frozen runner double/triple-counts repeated serialized tool results in raw local_seconds; this analysis uses one saved run ledger per local attempt. Raw rows and their hashes are preserved. The warmup consumes about half of the unchanged 600-second CLI deadline, leaving about 300 seconds for the task/host work. Uncapped local categories therefore have less remaining task time than a warm persistent process; this is a method limitation, not a measured serving default.

Host explicit pass/fail claims recognized in 15/15 final replies; disagreements with independent acceptance: 0/15. Unclassified replies are unknown, not failures or passes. Local verification present in 15 trials; disagreements with final independent acceptance: 2/15. Protected violations 0; timeouts 0; missing usage 0. Local verification and final host-applied verification are separate stages; agreement does not prove correctness beyond these tests.

### Accepted-task medians and B2-retry minus original B1

| Fixture | Accepted/completed | Local s median | CLI s median | Δ input | Δ cache write | Δ cache read | Δ output | Δ host turns | Δ CLI s |
|---|---|---|---|---|---|---|---|---|---|
| bug1 | 3/3 | 11.906 | 327.093 | -6.00 | -2269.00 | -72015.50 | -174.50 | -3.00 | +299.04 |
| feature | 3/3 | 21.063 | 341.235 | -2.00 | +748.50 | -32594.00 | +189.00 | -1.00 | +313.64 |
| multifile | 3/3 | 20.641 | 338.781 | -8.00 | -2553.00 | -109619.00 | -425.00 | -5.00 | +307.27 |
| offbyone | 3/3 | 17.657 | 336.125 | -5.00 | -2191.50 | -55202.00 | -100.50 | -3.00 | +305.82 |
| javascript | 3/3 | 19.703 | 335.047 | -4.00 | +331.00 | -67450.00 | -135.50 | -3.00 | +307.35 |

Negative token deltas mean fewer host tokens. Deltas are differences of per-fixture accepted medians, not paired causal effects. Failed tasks are listed separately, never silently removed from counts. No published subscription quota weighting is available. CLI cache context (~25k cache-write plus 92–135k cache-read) dwarfs 250–500 task output tokens: eliminating that entire output saves only about 0.16–0.43% of the unweighted combined context/output volume. That fixed context is 234–640 times the task output and can hide all of a task-output saving; extra host turns can overwhelm it. This arithmetic is not a billing or subscription conversion.

### Retry shadow diagnostic label

Original B1 remains its own cohort: 36/36 decisions were recent_http400, with 0 eligible local observations. B2 route mode does not emit actual shadow decision rows. The retry diagnostic below is a separately labelled **B2-retry route-derived eligibility projection**: mode is projected to shadow for the existing analyzer, while outcomes/turns/seconds are independent runner measurements. These are transformed diagnostic rows, not new B1 observations or host-reported shadow outcomes. No original B1 files or reports are rewritten.

Historical usage stop: B2-offbyone-sonnet-2 produced a local proposal ([{'status': 'done', 'reason': 'auto_finish', 'turns': 7, 'seconds': 16.360000000000582, 'tokens_est': 11538}]); local verification ['passed'], but quota stopped the host before application and independent verification. That interrupted attempt is archived, excluded from accepted-task aggregates and is neither a pass nor a test failure. Total local attempts including that archive: 16. Interrupted artifacts remain hash-inventoried under operations/usage-stop-B2-offbyone-sonnet-2. The unchanged runner resumes with fresh isolated psdata and skips completed keys. Current completed/accepted counts are 15/15 of 15; the historical usage stop remains recorded.

Ran eval/shadow_report.py only after eligible retry decisions existed, using the disclosed route-derived projection:

```json
{
  "local_completed": 15,
  "local_pending": 0,
  "local_disagreements": 0,
  "local_disagreement_rate": 0.0,
  "frontier_completed": 0,
  "frontier_easy": 0,
  "frontier_easy_rate": null,
  "orphan_outcomes": 0,
  "promotion_bar": 0.1,
  "struggle_turns": 10,
  "below_bar": true,
  "note": "Descriptive proxy only: frontier success does not establish local correctness. No automatic promotion."
}
```

### Speed, failures and shutdown

Fixture-balanced mean of accepted median deltas vs original B1: {'input_tokens': -5.0, 'cache_creation_input_tokens': -1186.8, 'cache_read_input_tokens': -67376.1, 'output_tokens': -129.3, 'turns': -3.0, 'secs': 306.6248}. Per-fixture changes are shown above, including any increases. End-to-end median was 336.125 s including cooldown; subtracting each measured wait yields a descriptive median of 35.275 s across 15 trials. The warmup-adjusted fixture comparison below describes the speed result; this is not a paired causal estimate. Local inference alone must not be compared with the whole B1 host session as if both clocks measured the same work.

Of 15 completed trials, local statuses were {'done': 13, 'error': 2}. Local failures by key/reason: {'B2-feature-sonnet-2': ['execution_error'], 'B2-offbyone-sonnet-2': ['execution_error']}. Feature repeat 2 and the resumed offbyone repeat 2 escalated after repeated failing tests; the frontier host repaired these tasks. Local-vs-final disagreements: 2/15; a failed local attempt repaired by frontier is not a false local pass. The archived usage-interrupted attempt remains excluded even after its trial key is rerun. Host final claims disagree with independent acceptance in 0/15 recognized replies. No failure-rate advantage over B1 is established; B1 made no local attempts.

Subtracting the actually observed startup wait per trial, then comparing fixture medians, gives deltas in seconds {'bug1': -1.3652390117645083, 'feature': 13.527075496673596, 'javascript': 7.017705167770412, 'multifile': 6.4135120258331355, 'offbyone': 4.970133609771729}; fixture-balanced mean +6.113 s. Positive means slower. The route-derived shadow report uses final host/runner outcomes, so its zero final-outcome disagreements do not count the two local failures; the local-verification result above does.

Edge0 had 2 successful single-attempt launches, separated by the subscription usage stop, both at unchanged ctx 32768. Logged HTTP status counts across both sessions: {'200': 106}, including the original direct probe. Per-second warmup RAM samples ranged from 0.017 to 0.894 GiB free. This was severe RAM pressure under the floor-0 deviation, not RAM-threshold validation. Clean shutdown: both sessions strata exit code 0; verified owned-console CTRL_BREAK; no forced kill. No Edge0/strata/llama-server remains; GPU utilization 0%, 15557 MiB free and 494 MiB used remains.

Fewer than 30 observations cannot assess the intended below-10% bar. Even a descriptive below_bar result on this projection is not a promotion decision or evidence of local correctness. These are original category-table fixtures, not held-out routing evidence. E39 items 1 and 2 remain open beyond the narrow measurements. Default remains frontier-only. No API spend, commit, push or publication.

Local unpublished draft. Private prompts, traces, patches, fixture/reference source, implementation and machine paths are withheld. This package supports aggregate recomputation, not independent rescoring of generated code. Method script names above refer to excluded private sources.


### Offline cleanup verification (2026-11-19)

All 134 public manifest hashes passed after selected refreshes. Portable E41 analyses verified 216 first-set and 288 blind2 rows; Edge0 blind2 remains 18/17/23 of 24, with v5b nonblind. E39 original B0/B1/B2 and retry aggregates were checked separately; original frontier 124/124 and Phase A 96/96 remain unchanged. The Phase A comparison snapshot was refreshed from completed E41 saved files; its earlier missing Edge0 rows and partially completed Qwen3.6/Aider snapshot are retained through provenance hashes. Frozen runner/launcher hashes and saved trial artifact hashes passed. The stale E41 first-set README manifest entry was corrected without altering its numeric results. Selected public artifacts passed the credential/private-path scan. All changes remain local, uncommitted, unpushed and unpublished; the separate Patchsmith checkout stays clean and unpushed.
