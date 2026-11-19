# Patchsmith v5b vs Aider across four local models, 2026-11-19

Status: completed-run consolidation of the held-out fixtures n01-n08 only. A separate second fixture cohort (n09-n16) is complete and is not pooled here; see [the blind2 package](../blind2-2026-11-19/README.md). Edge0 v5b/v6/Aider passed 18/17/23 of 24 there. Edge0 v5b remains nonblind, having been tuned on earlier failures.
No new inference was performed to produce this package. This is exploratory
evidence, not a preregistered comparison. It does not close the E39 follow-ups.

## Question

Edge0-120B-q3k scored poorly under Patchsmith's tool-call loop early on. Is that
the model or the harness? Aider, an established harness that uses whole-file
edits, is the control. Both ran the same eight held-out fixtures (n01-n08), three
runs each, on four local models.

## Results

Passes out of 24 (8 fixtures × 3 runs). Per-fixture counts are n01..n08.

| Model (quant) | Patchsmith v5b | Aider | Patchsmith per fixture | Aider per fixture |
| --- | ---: | ---: | --- | --- |
| Edge0-120B (q3k) | 20 | 20 | 3 3 3 1 2 2 3 3 | 3 3 3 1 3 3 3 1 |
| Qwen3-Coder-30B-A3B (Q3_K_M) | 19 | 14 | 3 1 3 3 3 3 3 0 | 3 0 3 3 2 3 0 0 |
| gpt-oss-20b (MXFP4), before fix | 14 | 22 | 1 2 1 2 3 2 2 1 | 3 3 3 3 1 3 3 3 |
| gpt-oss-20b (MXFP4), after fix | 15 | 22 (not rerun) | 2 1 1 2 2 3 2 2 | same |
| Qwen3.6-35B-A3B (UD-IQ3_XXS) | 24 | 23 | 3 3 3 3 3 3 3 3 | 3 3 3 3 3 2 3 3 |

Every count is recomputed from [trials.json](trials.json) by [analyze.py](analyze.py)
(216 rows, nine cells of 24). Do not pool these cells into one headline number.

Patchsmith failure types (runs that did not pass):

- Edge0: 2 `max_turns`, 2 `loop_detected` (n04, n05, n06).
- Qwen3-Coder: 3 `model_blocked`, 2 `max_turns` (n02, n08). No server errors; Aider
  also scores 0/3 on n02, n07 and n08 for this model.
- gpt-oss before the fix: 8 `execution_error` (HTTP 500), 2 `loop_detected`.
- gpt-oss after the fix: 6 `execution_error`, 2 `loop_detected`, 1 `model_blocked`.

## What this does and does not show

- Patchsmith is not uniformly behind Aider: ahead on Qwen3-Coder, level on Edge0,
  one run ahead on Qwen3.6, behind on gpt-oss. With three runs per fixture, a
  one-run difference is noise. This package does not show that Patchsmith beats Aider.
- The gpt-oss gap is largely an interaction between the model's output format and
  the server. The server returns HTTP 500 when the model's harmony-format output
  does not parse. Three causes appear in the server log: a `finish` call addressed
  to the final channel (recovered by the fix), tool-call JSON truncated mid-string
  while writing code (most of the remaining errors), and one malformed
  commentary-channel call. Only the first is recovered. Aider never puts code
  inside a JSON string and avoids these errors. The study compares whole harnesses,
  not one variable, so format alone is not established as the cause.
- Only 3 of the 8 pre-fix errors have a matching parse failure in the server log
  that was inspected; the other five show HTTP 500 in the transcripts but are not
  confirmed against the server log.
- The fix fires only on that specific HTTP 500, so it cannot change the other
  three models' numbers, and those cells were not rerun.
- A whole-file fallback for Patchsmith is not warranted in general by these data.
  It is an untested follow-up for gpt-oss only.
- Qwen3.6 is near ceiling on these fixtures at a low-bit quant; they stop
  discriminating there.

## Limitations

- **Not blind.** Patchsmith v5b was edited after the first held-out failures were
  seen (an initial run of the harness scored 17/24 on Edge0). The gpt-oss fix was
  written after reading the gpt-oss failures. The fixtures were written after
  earlier arms' failures were seen, so they are not independent of the tuning.
  Neither the 20/24 nor the 15/24 is a generalization result.
- Quant and serving flags differ per model and confound every cross-model
  comparison. Edge0 runs on a different inference server than the other three.
  See [configuration.json](configuration.json).
- Three runs per fixture; eight fixtures; one fixture family.
- The earlier tuning-set (h01-h10) and replay results are not part of this package
  and must not be pooled with these cells.
- An opencode arm was excluded: it was launched with a shell/argument-list fault
  and scored 0/50, which is a launcher error and not a result.
- Seconds in trials.json are harness-recorded attempt durations. Aider rows carry
  no turn count.

## Withheld

Raw transcripts, server logs, patches, fixture sources and model weights are not
included. Counts can be recomputed from the trial rows; the runs cannot be
re-scored from this package. The Patchsmith source is private; the revision that
contains the harness and the gpt-oss fix is recorded in the configuration file
only as an identifier.


## November 19 follow-up publication

The [separate n09-n16 cohort](../blind2-2026-11-19/README.md) is now selected for authorized publication. Edge0 v5b remains nonblind; cohorts are never pooled. Earlier first-set numerical results are unchanged. Fixtures, reference solutions, private implementation and raw traces remain withheld.
