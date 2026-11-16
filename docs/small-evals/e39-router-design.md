> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E39 follow-on: implementer router (Edge0 vs frontier) — design

Status: **router implemented and offline-tested locally on `feature/e39-router`; measured frontier baseline retained. No live router/shadow cohort yet.** Written 2026-11-14 from the E39 soak, refactor-big, context-scaling and thinking runs, plus earlier picks from E19, E29 and E34. The frontier side (Sonnet, Haiku) was measured the same day, see "Measured frontier side". Every number below is from those runs unless marked "to measure".

## Question

When Patchsmith (or the Claude Code plugin) has a task to implement, should it go to the local Edge0-120B-q3k, or to a frontier model (Sonnet, or Haiku for cheap steps)? The router should decide **before** spending local wall-clock, and bail out **during** a run when the local model is failing. The cost metric is wall-clock plus frontier subscription quota. It is not dollars (subscription only, no API spend).

## What the data says Edge0 is good for

Source: E39 realistic soak, 24 rounds, 192 trials, temperature 0, thinking off, ctx 16k-24k budget. A "realistic" soak means the user's normal apps were running, so RAM was under pressure.

| Fixture (task category) | n | Pass | Median s | p95 s | Local verdict |
|---|---|---|---|---|---|
| bug1 (single-file bug fix) | 24 | 96% | 21 | 56 | local |
| multifile | 24 | 96% | 33 | 80 | local |
| javascript | 24 | 92% | 33 | 62 | local |
| feature | 24 | 88% | 30 | 71 | local, wall cap |
| offbyone | 24 | 88% | 31 | 187 | local, wall cap (heavy tail) |
| bug2 (harder bug) | 24 | 79% | 29 | 82 | local-first with escalation |
| refactor | 24 | 67% | 32 | 66 | frontier by default |
| blocked (must refuse) | 24 | 23/24 correct | n/a | n/a | local, safe |

Other facts that shape the router:

- **Server health matters more than task type.** Rounds containing an HTTP 400 (`ExpertCache::fill_slot_queued: out of memory`) passed 9/16 (56%). Clean rounds passed 136/176 (77%). Round time grew from about 3 min to 7-9 min late in the soak, with two 11 min spikes, which fits memory pressure.
- **Context budget.** refactor with `PS_CTX_BUDGET=28000` (ctx 32768) passed 4/5, against 3/5 at the 24k baseline. Five runs, so this is a hint, not a result. Prefill is 0.8-1.0k tok/s, so a 23k-token prompt costs 25-30 s before the first token. Needle retrieval was 12/12 up to the largest size tested.
- **Decode slows with context:** 38 tok/s at 1k, 24 at 6.5k, 17 at 13k. (The 38 at 28k is an unexplained outlier; do not use it.)
- **Temperature 0 is not deterministic.** The same prompt gave 117-148 tokens across 5 runs. The router must not assume a repeat run gives the same answer.
- **Thinking stays off.** Thinking-on HumanEval+ was 0.616 against 0.884, at about 12x the generation time.
- **Reference picks from earlier evals:** on raw code correctness, Gemma 4 12B and Qwen3-Coder-30B-A3B match or beat Edge0 on HumanEval+/MBPP+ and are faster on this card (E39 results, E19 table). Haiku 5.5 scored 99.2% (119/120) on the E29 workflow-equivalence subsample, so it is the natural cheap frontier tier. E34 arm 5 showed that a per-type router fitted on a small tune split (about 7 items per type) beat the single best model on correct/h by 6% but gave up 4.4 points of accuracy, with swap cost excluded. Treat that as a warning about fitting a router on few items.

## Design

The pattern follows the Amazon Decider setup (unverified, from a LinkedIn summary): a small model returns a choice plus a confidence for choice steps only, never generates text, and is rolled out behind a mode flag. Ours is simpler because the "decider" can start as a lookup table, not a model.

### Layer 1: static pre-check (before any tokens)

Input: task category, estimated prompt tokens, a health probe. Output: `local`, `local_with_cap` or `frontier`.

1. **Category table** (the soak table above, stored as JSON next to the plugin config):
   - pass >= 85% and p95 <= 90 s: `local`
   - pass >= 85% and p95 > 90 s: `local_with_cap` (cap = 2 x median, floor 60 s; offbyone is the case that needs it)
   - 70-85%: `local_with_cap` with escalation allowed
   - < 70%: `frontier`
2. **Size gate:** prompt tokens > 24k means `frontier`. Beyond that, prefill alone costs 25 s or more and decode drops under 20 tok/s.
3. **Health gate:** if the Edge0 server is down, or free RAM is below a threshold, or an HTTP 400 was seen in the last N minutes, use `frontier` until the server has been clean for M minutes. Thresholds N, M and the RAM floor are **to measure**; the soak only shows the correlation, not a cutoff.
4. **Unknown category:** `frontier`. The table only covers what was measured.

### Layer 2: runtime escalation (during a run)

Escalate to frontier, carrying over the task and any partial diff, on any of:

- agent returns `blocked` for a category that is not in the "must refuse" set,
- wall-clock cap exceeded (from Layer 1),
- HTTP 400 / connection error / server restart,
- the same test fails twice with an identical error.

Escalation is one-way per task. Sonnet is the default target; Haiku only for categories where it is later shown to pass.

### Rollout modes (config flag)

| Mode | Behaviour |
|---|---|
| `frontier-only` | Router off. Everything goes to the frontier model. Default and instant rollback. |
| `shadow` | Frontier does the work. The router also makes its call and logs it. Local is not run, so shadow costs no extra wall-clock. |
| `route` | Router decides. Layer 2 escalation active. |

Shadow logging: one JSONL line per task with category, prompt tokens, router decision, reason, and later the outcome (frontier pass/fail, wall-clock). The disagreement report is "router said local, frontier failed or needed more than X turns" and the reverse. Promote shadow to route only when disagreement on the `local` bucket is under a bar chosen in advance (suggest 10%, to be fixed before any data is seen).

## Expected value check

Local-first expected time = p x E[t_local | success] + (1 - p) x (E[t_local | failure] + t_frontier), where a failed local attempt costs the time until it stops (capped by the wall-clock cap). The earlier form, t_local + (1 - p) x (cap + t_frontier), added the local time twice on failures; the figures in the measured-frontier section below used that older form, so they overstate local-first time somewhat (bug1 comes out a slight local win, about 23 s against 26 s, under the corrected form with a 60 s failure cost). With the soak numbers, bug1 is 21 s median at 96%, so local wins whenever a frontier round trip takes more than a few seconds. Refactor at 67% with a 32 s median wastes about a third of its runs. Whether that beats going straight to frontier depends on t_frontier, which **has not been measured** (Sonnet through the plugin). That measurement is the first thing to run, because it sets every threshold above.

## Measured frontier side (Sonnet and Haiku via Claude CLI)

Run 2026-11-14 with `C:\e39\frontier_bench.py` (kept outside the repo; raw rows in `C:\e39\frontier\results.jsonl`). Same 7 fixtures as the soak (blocked excluded), 10 trials per model per fixture, 140 trials, subscription only. Scoring used the same independent tests as the Edge0 runs. The run was resumable, no usage limit was hit.

| Fixture | Edge0 pass | Edge0 median / p95 s | Sonnet pass, median / p95 s | Haiku pass, median / p95 s |
|---|---|---|---|---|
| bug1 | 96% | 21 / 56 | 10/10, 26 / 27 | 10/10, 28 / 48 |
| bug2 | 79% | 29 / 82 | 10/10, 43 / 47 | 10/10, 34 / 46 |
| feature | 88% | 30 / 71 | 10/10, 26 / 29 | 10/10, 36 / 40 |
| multifile | 96% | 33 / 80 | 10/10, 29 / 31 | 10/10, 32 / 35 |
| refactor | 67% | 32 / 66 | 10/10, 29 / 30 | 10/10, 31 / 36 |
| offbyone | 88% | 31 / 187 | 10/10, 27 / 31 | 10/10, 31 / 41 |
| javascript | 92% | 33 / 62 | 10/10, 25 / 25 | 10/10, 27 / 34 |

(Two javascript run-9 trials landed after the interim tally: Sonnet 25.4 s, Haiku 34.0 s, both green.)

What it shows:

- **Frontier is as fast as Edge0 on these fixtures and passed 140/140.** Its tail is tight (p95 at most 48 s). Edge0 only has a median edge on bug1 (about 5-7 s).
- **So routing to local does not save wall-clock on the fixtures where Edge0 is good.** Local-first expected time = p x E[t_success] + (1 - p) x (E[t_failure] + t_frontier). The figures below were computed with the older, conservative form t_local + (1 - p) x (cap + t_frontier) (60 s cap, Sonnet medians); they overstate local-first time on failures, so read bug1 as a tie or slight local win and the rest as frontier wins or ties: bug1 about 24 s against 26 s (tie), multifile about 36 s against 29 s, javascript about 38 s against 25 s, feature about 41 s against 26 s, bug2 about 50 s against 43 s, refactor about 61 s against 29 s. Frontier wins or ties everywhere on time.
- **The case for routing to local is subscription quota and offline use, not speed.** Each local pass leaves Sonnet/Haiku quota untouched. That is worth measuring: tokens per task from the `usage` field in the results file give the quota cost per frontier task.
- **Table update for Layer 1:** refactor and bug2 go to `frontier` by default (refactor was already under 70%; bug2 moves from escalation to frontier because its frontier time is no worse). bug1, multifile and javascript are the `local` bucket. feature and offbyone are `local_with_cap`.

### Quota cost per frontier task

From the `usage` field of the same 140 trials (script: `C:\e39\quota_tally.py`). Means per task, all fixtures:

| Model | Turns | Output tokens | Fresh input (input + cache create) | Cache-read input |
|---|---|---|---|---|
| Sonnet | 4.6-8.0 | about 700 (420-1,090) | about 29.7k | about 295k |
| Haiku | 6.8-9.6 | about 1,590 (1,310-2,150) | about 19.5k | about 257k |

Reading it: most of each task's tokens are the Claude Code system prompt and tool definitions (about 20-30k, created once and re-read every turn), not the task. So the quota a task costs is dominated by a near-fixed per-task overhead plus a few hundred to a couple of thousand output tokens. Each locally-handled task saves roughly that bundle. Haiku writes more output and takes more turns than Sonnet on the same fixture, so the saving per task is not much smaller on Haiku. How the subscription weights these token types is not published, so treat the table as relative cost, not as a percentage of any plan. Also, the CLI overhead may be larger than what the plugin path costs, so this likely overstates the per-task saving if the plugin's orchestrator already holds the context.

Caveats: the CLI path does not go through the Patchsmith plugin (`implement_task`) and uses a simpler prompt, so the numbers are not like-for-like on orchestration overhead. Fixtures are tiny. n = 10 per cell, and 10/10 only bounds the true pass rate at roughly 69-100%. All frontier trials passed, so this measures speed, not whether the frontier model is better on harder work. `blocked` was not run on the frontier side.

## Known gaps and risks

- The table comes from 7 synthetic fixtures with 24 trials each. Intervals are wide: 79% on 24 trials spans roughly 60-91%. Real repo tasks may not map onto these categories.
- Fixtures were run through the Patchsmith harness, not through the plugin path (Sonnet orchestrator -> `implement_task` -> Edge0). That path passed one end-to-end test only.
- The health thresholds are guesses until measured. The machine's load during the soak (user apps running) is the intended deployment condition, but it varies.
- Partial MBPP+ (106 of 378 problems) was never scored, so there is no thinking-on correctness figure beyond HumanEval+.
- The Amazon numbers (44x cheaper, 4,215 to 897 ms) come from an unverified LinkedIn summary and are not evidence for this design.

## Next steps (not started)

1. ~~Measure t_frontier for Sonnet and Haiku on the same 7 fixtures.~~ Done 2026-11-14 through the Claude CLI (10 trials each). Still open: repeat through the plugin path to include orchestration overhead.
2. ~~Measure frontier quota cost per task.~~ Done, see "Quota cost per frontier task". Still open: the same measurement for the plugin path, where the orchestrator's own turns also count, and a check of how much real quota burn matches the token counts.
3. Run a harder task set (real repo tasks, larger files) on both sides. The fixtures are too easy to separate the models, and Edge0's advantage, if any, has to show up on realistic work.
4. Implement Layer 1 as a JSON table plus a function in the plugin; start in `shadow`.
5. Add the Layer 2 triggers to `implement_task` behind the mode flag.
6. Choose the health thresholds from a second soak that varies RAM pressure deliberately.
7. Re-check the table after any change to the Edge0 build, quant, or serving flags.


## Codex progress — 2026-11-14

Implemented in the separate `tmp/patchsmith-audit` Git repository, on the new
`feature/e39-router` branch based on `feature/claude-code-plugin`. The parent
research repository remains on `master`. Nothing committed, pushed or opened as
an external PR. Pre-existing parent/nested-repository changes were preserved.

Built:

- Layer 1 JSON table with the fixed measured decisions, actual initial prompt
  estimate, 24k size gate, TCP/RAM health probe and HTTP-400/clean cooldowns.
  N=5 minutes, M=2 minutes and free-RAM floor=2 GiB are named, configurable,
  **provisional values to measure**, not new evidence. Unknown RAM fails closed.
  Process-local health history starts with a conservative full cooldown on restart.
- `frontier-only` default, `shadow`, and `route`; category is available in the
  Hermes and MCP implement/queue interfaces. Default and shadow never generate
  locally. Shadow records decisions and accepts actual host outcomes via the
  new `record_router_outcome` tool.
- Route-only blocked/cap/transport/repeated-test escalation, one isolated local
  attempt, rollback and a saved full partial diff for the frontier host. Safety
  failures (protected tests, Git state, verification, rollback) do not escalate.
  Feature/offbyone caps are 60/62 seconds. Local requests now use temperature 0.
- Shadow report with the frozen strictly-below-10% local-bucket bar. The formerly
  unspecified X is fixed at **10 host turns** before any live shadow data.
  Reports reverse disagreements, missing outcomes and zero-data cases; rejects
  duplicates. It never promotes automatically.
- Ten multi-file synthetic maintenance fixtures with read-only independent tests,
  separate reference repairs, an offline seed/reference validator, and `--harder`
  selection in the direct-local evaluation harness. Unknown categories remain
  frontier; these tasks do not inherit the old fixture accuracy estimates.

Integration boundary: this plugin had no frontier execution transport. A
`frontier_required` result hands the original task and partial-diff context to
its subscription host, with Sonnet as the intended target. The host must continue
without re-delegating and record actual outcomes. No hosted API or Claude CLI
executor was introduced, and a handoff is not a completed frontier run. The
host's model cannot be selected by this code. See the clone's `docs/ROUTER.md`
for the full contract and limitations.

Verification (Windows, Python 3.12.7):

- `python -B -m pytest tests -q --disable-plugin-autoload -p no:cacheprovider --tb=short`
  -> **159 passed, 1 skipped in 58.76 s**. This includes the existing suite and
  routing checks. One earlier run had a mock-signature failure; it was corrected.
- After the final safety-precedence hardening,
  `python -B -m pytest tests/test_router.py -q --disable-plugin-autoload -p no:cacheprovider --tb=short`
  -> **42 passed in 7.63 s**, including four added cases. These overlap the full
  suite count; do not add them as independent tests.
- `python -B eval/validate_harder.py` -> all **10/10 seeded fixtures exit 1** and
  **10/10 reference repairs exit 0**, with byte-identical tests. No model involved.
- `python -m ruff check .` -> all checks passed. `python -m ruff format --check
  router.py tests/test_router.py eval/shadow_report.py eval/validate_harder.py`
  -> four files already formatted. `python -m compileall -q router.py loop.py
  llm.py tools.py codex_mcp.py __init__.py eval tests` and `git diff --check` passed.
- Sandboxed loopback HTTP tests initially failed to connect; the suite passed
  outside the Windows network sandbox using temporary fake servers only.

Not done: live shadow collection/promotion, harder-fixture model runs, RAM-pressure
soak/calibration, plugin-path timing/quota repeat, or real frontier round-trip.
No local llama/Edge0 server was started, stopped or restarted. No GPU work, API
spend, Claude model runs, article publication or Sprocket P2 work occurred.
The ten tasks are broader synthetic contract tests, not real-repo difficulty
validation. TCP readiness is weaker than inference health, health observations
are not shared across processes, non-unittest repeat detection uses whole-output
fingerprints, and cleanup/Git overhead can extend elapsed time beyond a cap.

Table values were not changed or disputed. The earlier heuristic would classify
feature differently, but the explicit measured-table update and handoff take
precedence; feature remains capped local. The new fixtures supply no data to
change any row.

Files changed are listed in the change manifest (not included in this public release).


## Harder fixtures h01–h10, Edge0 measurement — 2026-11-14 (no Claude quota)

Setup: Edge0-120B-q3k, ctx 32768, temperature 0, thinking off, `eval/run_eval.py --harder --runs 5`, 50 trials, run unattended, user apps possibly open. Raw: `C:\e39\harder\` (outside repo). Wall time about 26 min.

| Fixture | Pass | Median s | Failure modes |
|---|---|---|---|
| h01_cursor | 2/5 | 29 | loop_detected 2, context_budget 1 |
| h02_stock | 0/5 | 26 | loop_detected 3, context_budget 2 |
| h03_import | 4/5 | 25 | loop_detected 1 |
| h04_access | 2/5 | 24 | context_budget 3 |
| h05_retry | 0/5 | 24 | context_budget 5 |
| h06_retention | 2/5 | 34 | context_budget 3 |
| h07_queue | 2/5 | 39 | context_budget 3 |
| h08_config | 0/5 | 30 | loop_detected 1, context_budget 4 |
| h09_search | 2/5 | 28 | context_budget 3 |
| h10_intervals | 4/5 | 23 | context_budget 1 |
| **All** | **18/50 (36%)** | | |

- Server: 519 HTTP 200, 0 HTTP 400 in `serve.err`. The failures are not server errors; they are the Patchsmith loop stopping the run (`context_budget` and `loop_detected`, about 12 turns).
- Memory: free RAM fell to 0.01 GB at the low point, VRAM peaked at 15,549 MiB. Run completed regardless.
- Read: on realistic multi-file tasks Edge0 passes 36%, against 67–96% on the original seven. This supports keeping everything outside the five table rows on `frontier`, and treating the h-style category as `unknown`. No table value changed.
- Caveat: `context_budget` may reflect the loop's turn/budget setting rather than model capability; the loop budget was not tuned, so a rerun with a larger budget would separate the two. Not done. Frontier pass rate on h01–h10 is unmeasured (needs quota).

## Review of the Codex E39 critique and follow-up (2026-11-15, no Claude quota)

Claude's assessment of the external critique, plus the no-quota follow-ups done.

- **Shadow disagreement cannot gate promotion.** Frontier passed 140/140 on the fixtures, so a "frontier struggled" rate sits near 0% whatever Edge0's quality. The 10% bar would pass vacuously. Shadow mode validates logging and host integration only. Promotion needs a local-side paired replay on held-out tasks with independent tests.
- **Categories are fixture labels.** `multifile` scored 96% originally and the ten harder multi-file fixtures scored 36%, so the label does not predict success. No runtime classifier assigns real tasks to categories; unknown stays `frontier`, and `frontier-only` stays the default.
- **Net quota saving must be measured through the host** as frontier tokens per accepted, verified task. Offline use holds for a local host (Hermes), not for the Claude plugin path.
- **Health calibration:** the process-local cooldown fails closed and may block short-lived hosts; the RAM floor rests on one run (0.01 GB free, yet 519 HTTP 200 and 0 HTTP 400).
- **Expected-time formula corrected** (see Expected value check).

### Held-out task candidates mined from real history

`C:\e39\mine_commits.py` scans fix commits that touch Python source and tests (small diffs) in six local repos; `C:\e39\verify_mined.py` checks each by overlaying the commit's tests on the parent (must fail) and running them at the commit (must pass). Only 6 commits matched the filter; 4 qualify (fail before, pass after):

| Repo | Commit | Subject |
|---|---|---|
| porsynth-automations | c5aedeeb | slm-mesh T8.3 scorer grammar for every S3 adapter |
| porsynth-automations | 1bf3d146 | first-circle reconcile winner = earliest scraped_at |
| porsynth-automations | 29395258 | first-circle reconcile re-points shadow+frontier lead_ids |
| sprocket | b91bce41 | Bound model repair and correct run cost accounting |

Rejected: bd3e6016 (tests fail both before and after) and 136228cf (same). These are candidates only. No model has been run on them. The set is small and drawn from one author's repos, so treat results as indicative; some tasks depend on repo context that a fixture-style checkout would need to include.

### Still open
Loop-budget rerun of h01-h10 and local-side replay on the four candidates (both need the GPU and a server start), health-block instrumentation, observable-feature gating once there is data, and everything needing Claude quota (plugin-path tokens per accepted task, frontier pass rates on h01-h10).


## Interim write-up update — 2026-11-15

The [consolidated E39 results](e39-results.md#agent-work-the-useful-limit-is-reliability-interim-2026-11-15) supersede the earlier unstarted-run notes above. Separate harder-task runs returned 18/50 (cumulative 24k), 7/50 (cumulative 30k), 12/50 (live-context, eight execution errors), then 27/50 and 21/50 (live-context with the retry-capable client, zero execution errors). Do not pool these changing conditions into one success rate.

The live prompt, rather than cumulative token spend across turns, now determines the context budget by default (`844fed1`; opt-in implementation and retry in `5e8045a`). `PS_BUDGET_MODE=cumulative` restores the old behavior. The client retries once for a timeout or an OOM-specific HTTP 400. The 12/50 run had two OOM errors and six prefill timeouts; the later runs had no corresponding live faults, so the retry's benefit is not demonstrated. Remaining failures were repeated-tool-call stalls, plus one maximum-turn stop in each later run. Identical settings produced 27/50 and 21/50: category counts remain noisy.

Real-commit replay is now measured: 0/12 cumulative versus 7/12 live-context across four tasks, three repeats each. These are exploratory runs, not a controlled causal estimate. The router table remains unchanged and `frontier-only` remains the default. Shadow disagreement validates neither local correctness nor promotion; local-side paired evidence is still required.

Quota-blocked and not measured: plugin-path tokens per accepted task, frontier pass rates on h01-h10 and the mined candidates, the shadow cohort, and a live route flip. Resume those measurements when quota returns. Health calibration and live retry recovery remain open. The checkout was clean on `feature/e39-router` at `844fed1` when inspected for this write-up; earlier uncommitted-status notes describe their dates. Claude owns E40 implementation; no E40 code or runs were added here.


## Local validation follow-up — 2026-11-15

The local follow-up exercised the default health gate: available RAM was 0.011–0.347 GiB, and all three route checks returned `frontier_required` with `low_ram`; no routed coding attempt ran. Seven short inference probes succeeded. All four injected retry cases behaved as intended against the real backend, but natural OOM/prefill-stall recovery is still unmeasured. One 28,036-token retrieval prompt returned the correct marker in 25.344 s. The original E40 server was restored and its health endpoint returned `ok`. No threshold, table or global mode changed. See [the raw local validation record](e39-local-validation/README.md). The earlier statements that all retry checks and partial-MBPP scoring are unstarted are historical: injected recovery now passed, and archived MBPP subset scoring is complete. This does not close natural recovery or calibration.
