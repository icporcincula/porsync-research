# Patchsmith and Aider exploratory comparison — 2026-11-16

Status: completed-run consolidation; curated evidence approved for publication
on 2026-11-16. No new inference or server changes were performed.
This is exploratory evidence, not the prospectively frozen B2 comparison or a
daily-use release gate. It does not close E39 or Sprocket.

## Findings

On the ten harder fixtures, Aider with test feedback passed 30/30 saved trials;
Patchsmith passed 47/50. Both passed every saved easy trial. These observations
provide no demonstrated correctness or median-latency advantage for Patchsmith.
They do not establish general superiority for Aider: task exposure, unequal repeat
counts, execution limits and unmeasured host/review workflows limit interpretation.

| Arm | Set | Passed | Median seconds | Range seconds | Total attempt seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| Aider one shot | Easy, 7 tasks × 3 | 21/21 | 5.90 | 4.3–6.5 | 120.9 |
| Aider one shot | Harder, 10 tasks × 3 | 18/30 | 11.25 | 8.3–54.6 | 432.0 |
| Aider test loop | Easy, 7 tasks × 1 | 7/7 | 5.60 | 4.7–6.3 | 38.7 |
| Aider test loop | Harder, 10 tasks × 3 | 30/30 | 19.25 | 7.9–158.6 | 907.5 |
| Patchsmith loop | Easy, 7 tasks × 3 | 21/21 | 6.30 | 3.187–15.219 | 154.201 |
| Patchsmith loop | Harder, 10 tasks × 5 | 47/50 | 22.15 | 8.141–87.625 | 1395.612 |

Medians include failures. Seconds are harness-recorded attempt durations, not time
to human-accepted completion. Aider timing includes its subprocess startup; both
harnesses run final external checks after the measured operation. No matched cold
start, model-load, human review, repair or host-token measurement was collected.
Repeats of the same fixture are not independent new tasks. There are 17 distinct
fixtures and 159 unique archived trial rows, not 159 independent tasks.

## Source accounting and batch completion

| Source JSON | Trials | Passed | Inclusion |
| --- | ---: | ---: | --- |
| aider-run1 | 17 | 13 | One shot, first pass |
| aider-run2 | 17 | 14 | One shot, second pass |
| aider-run3 | 17 | 12 | One shot, third pass |
| aider-testloop-1 | 10 | 10 | Earlier harder test-loop pass |
| aider-testloop-h2 | 10 | 10 | Final batch |
| aider-testloop-h3 | 10 | 10 | Final batch |
| aider-testloop-easy | 7 | 7 | Final batch |
| ps-probe | 10 | 10 | Earlier harder pass; included despite probe label |
| ps-harder-2 | 20 | 20 | Two earlier harder passes |
| ps-easy | 21 | 21 | Final batch |
| ps-harder-3 | 10 | 9 | Final batch |
| ps-harder-4 | 10 | 8 | Final batch |

`aider-smoke-results.json` is byte-identical to `aider-run3.json`; it is archived
but excluded as a duplicate. The initial single-task wiring probe described in the
conversation has no separate surviving result file and is not counted again.
`ps-probe.json` requested h01 in its command but actually contains all ten harder
fixtures; the earlier harness ignored that filter with `--harder`. Count actual
rows, not the filename or requested fixture count.

The final `run_all.sh` batch completed all 68 planned trials (65 passed, three
blocked). `run_all.done` contains `ALLDONE`, with observed local modification time
2026-11-16 10:53:18 (Asia/Shanghai). The marker alone would not establish success:
the shell script has no fail-fast handling. All six expected JSON result files
were also checked for the expected rows and outcomes. No interrupted batch remains.

## Failure review

All three final-batch failures are Patchsmith harder trials, with status `blocked`:

- `ps-harder-3`, h08_config: `loop_detected`; repeated-tool-call stop.
- `ps-harder-4`, h01_cursor: `model_blocked`, 12 turns, 72.797 seconds. The model
  argued that returning no next cursor on the final page conflicted with standard
  pagination. The fixture explicitly requires a next cursor only when another page
  exists; the test expectation matches that contract. This is a failed task, not
  evidence that the test is defective. Its internal attempt log shows one remaining
  edge-test failure; the external check shows baseline failures after no successful
  patch was applied. These are different states, not contradictory scores.
- `ps-harder-4`, h10_intervals: `loop_detected`, nine turns, 20.469 seconds; the
  attempt history lists no touched files. This final failed trial was the last
  ledger entry, not a crash or interruption of the batch.

Loop-stop labels identify the stopping mechanism; the available summaries do not
establish why the model repeated calls. Do not infer a server outage or prescribe
a guardrail change from these labels alone. Failed trial artifacts remain retained.

## Configuration and interpretation limits

The session reported Qwen3.5-9B on llama-server at loopback port 1234. Saved
Patchsmith metadata and Aider settings use model alias `qwen3.5:9b`. Exact model
digest/quantization, server build, launch configuration and run-time GPU residency
are not established by this package; Patchsmith used `require_gpu=false`.

Aider logs identify v0.86.2. The retained runner uses whole-file edits, temperature
0, max_tokens 8192, thinking disabled, no git, no repo map, no auto-lint, and a
600-second subprocess timeout. Tests are passed as read-only context. Test-loop
arms additionally enable auto-test with the fixture test command. One-shot arms
do not receive test feedback during editing and are not the like-for-like loop
comparator. The diff-format variant was not run.

Patchsmith metadata records one attempt, max_turns 25 and context budget 24000.
The inspected checkout is `feature/e39-router` at `844fed1`; its current harness
calls `implement_local` directly, bypassing host dispatch, with apply mode inside
disposable fixtures. The exact run-time source revision was not stored in these
result metadata. Current source inspection does not prove historical identity.
This does not validate the ordinary plugin/revision/comparison routing paths or
separate reviewed application. No Aider MCP wrapper arm was measured.

Both arms use the bundled fixture checks, run again outside the coding loop.
Those are separate executions, not hidden or independently authored holdout tests.
Tests were available to the model; correctness is limited to what they cover.
Known development fixtures, sequential arm order, unequal budgets and unequal
repeat counts prevent a controlled claim of general superiority. There was no
prospective protocol, human acceptance review or measurement of guardrail and
integration benefits. Aider's per-fixture log filenames were overwritten between
passes; the archive contains only the surviving logs, not full traces for every run.

## Recompute and provenance

Run `python analyze.py` here. It checks the curated [trial rows](trials.json),
[summary](summary.json), unique source-row identities and final-batch totals.
No model or GPU is needed. Each trial retains its original result-file SHA-256
and source row. The private archive inventory (withheld) hashes 50
original files copied byte-for-byte out of the temporary scratchpad; originals
remain untouched. The `private/` archive is gitignored, contains local paths and
generated patches/logs, and is not selected for publication. The virtual environment,
model weights and temporary task workspaces were not archived.

Curated rows extract only source identity, fixture, arm, outcomes and timing;
they omit patches, prompts, local paths and raw traces. This supports recomputing
the descriptive counts, not independently re-scoring code or reproducing inference.
The companion configuration documents known settings and unknown provenance.

## Next step and publication state

Finish E39/Sprocket close-outs under the existing sequencing requirement. Then
establish passing integration checks, fix the required dispatch paths, and freeze
the B2 protocol before new measurements: Patchsmith, direct Aider and a pinned
Aider MCP wrapper on harder real-project tasks, with independent acceptance,
comparable budgets, review effort, isolation and host usage. Make the planned
build/reuse/contribute decision before substantial onboarding/release work.

A curated copy of this report, trial rows, summary, configuration and analyzer is
selected for publication in the separate public-evidence repository, with its
index, release notes and provenance manifest. Private archives remain excluded.
No website update or new inference is included; E39 follow-up remains open.
