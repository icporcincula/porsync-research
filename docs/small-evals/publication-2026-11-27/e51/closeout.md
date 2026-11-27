> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E47-E51 closeout: Inkling 2 Mini, Niko1221's Strata engine SQ-15 vs llama.cpp IQ3_XXS (private)

Status: **CLOSED 2026-11-25 (local-lane comparison line).** Private record. No publication, no push, no public-evidence sync (deliberately deferred under the private/no-publication instruction). Credit: Thinking Machines Lab (model), Niko1221 and contributors (engine), llama.cpp authors.

## What was asked

Whether the SQ-15 build of Inkling 2 Mini on Niko1221's Strata engine (arm B, thinking restored through the E49 adapter) gives more correct answers per hour than llama.cpp IQ3_XXS (arm A) on small synthetic reasoning tasks, at no more than 10 points lower accuracy.

## Observed, by experiment

| Exp | Pool and settings | A (llama.cpp IQ3_XXS) | B (SQ-15 thinking) | Reading |
|---|---|---|---|---|
| E47 | 12 items, one order, no repeats; release forced effort none | 11/12 in 136 s | 4/12 in 9 s (release); 12/12 in 88 s (post-outcome adapter diagnostic) | promising observation only; diagnostic was post-outcome |
| E49 | 48 samples per arm, cap 4096 | 48/48 | 48/48 | ceiling, no discrimination |
| E50 | harder calibrated pool, L3, 24 items x 2, cap 6144 | 25/48 | 38/48 | ratio 1.35, CI [0.98, 1.99], `promising_again` false; all 54 wrong rows were length stops |
| E51 | L3, 36 items x 2, fresh seed, cap 12288, context 16384 | 58/72, 26.2 correct/h, 1 length stop | 60/72, 22.4 correct/h, 0 length stops | ratio 0.855, CI [0.717, 1.062]; accuracy diff +0.028, CI [0.00, 0.069]; H1 false, H2 true, `promising_again` false |

All E51 blocks completed with no errors; frozen hashes intact. Details: E50 results (private source reference withheld), E51 results (private source reference withheld).

## Conclusion (what the rows support)

- **Observed:** with truncation largely removed (length stops 54 of 96 wrong rows in E50, 1 of 144 rows in E51), arm B was about as accurate as arm A (+2.8 points, interval touching zero) and was not faster per correct answer (0.855x, interval including 1.0).
- **Observed:** E50's apparent speed advantage for B did not reproduce at the larger cap.
- **Hypothesis, not tested:** E50's edge came from B finishing more answers inside the 6144 cap (B used fewer tokens at the median, 3,670 vs 4,913 in E51).
- **Observed anomaly:** both E51 A blocks fell to 0.75 GiB minimum available RAM with 7.1 GiB peak swap. Launch checks passed at start. Effect on A's speed is unknown; if it slowed A, the real gap in A's favor is understated for B, not overstated. An A-only rerun on an idle machine would address this and was offered but not run.
- Nothing here supports a promotion, a router change or an engine comparison claim.

## Limits that carry over

One synthetic pool type, six families, single-answer JSON. The schedule family scored 0/12 on both arms (floor), so the other five families are about 98% on both arms (A 58/60, B 60/60) and discriminate little on accuracy. Whole-stack confounding (model pack and quantization, engine, sampler, drafter, cache). Reasoning text unaudited. No coding, tool-use or long-context result. Pool design was adjusted after E49 and E50 outcomes, so later pools are not independent of earlier results.

## Decision

Close this comparison line. No further runs of the same question on this pool. Reopen only with a different question or a new pool type decided in advance. The optional A-only idle-machine recheck is left open for discussion.
