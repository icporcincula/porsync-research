> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E07/E08 local replication

The follow-up compares the original Qwen3.5-9B Q4_K_M control, Gemma 4 12B IT Q4_K_M, and Qwen3.6-27B UD-IQ3_XXS. The larger-profile fallback is gpt-oss-20b MXFP4 if the 27B cannot run the development workload at a usable speed within the available memory. Model selection uses development observations only. Each comparison is between complete deployments, including quantization and native templates.

The runner stages the original hash-verified source snapshots and frozen inputs into a separate workspace per model and eval. E07 uses 42 receipts and all original X arms, including three baseline calls and the check and repair derived from X0A. E08 uses 200 tables and all original N arms, with the two guards derived from the same N1 output. The original development gates apply. The original llama.cpp build, 16,384 context, one slot, seed 808, temperature zero, reasoning-off request configuration and 1,536-token cap carry over. All requests go to a server owned by the runner on 127.0.0.1. The runner processes one model at a time. Original results stay in their existing directories.

Primary comparisons follow the original reports. For E07, compare X1 with X0A on arithmetic contradictions and track exact printed totals, item F1, invalid outputs, repair triggers and wrong but internally consistent totals. Use the three X0 repeats as a within-profile noise diagnostic. For E08, compare N1 with N0 on the paired summary flag rate, then track fallback and repair for N2/N3 and descriptive direction diagnostics. Retain the original receipt-level and country-cluster bootstrap intervals respectively. Review per-profile verifier precision and missed semantic errors from the seeded samples separately from automatic metrics. Use raw finish reasons and server logs to diagnose incomplete outputs, and keep timing descriptive.

From the repository root:

    python portfolio/small-evals/e0708_replicate.py qwen35-9b gemma4-12b qwen36-27b --phases dev
    python portfolio/small-evals/e0708_replicate.py qwen35-9b gemma4-12b qwen36-27b --phases test report

The runners resume from completed item traces. The staged workspace contains the execution manifest, model and runtime hashes, logs and the original reporting outputs. The host needs permission for loopback connections.

All six development gates passed. The 27B used approximately 13,448 MiB of GPU memory in a spot sample during E08 development, so the main run uses the 27B. No model downloads or deletions were needed. The 9B weight and server executable hashes match the original freeze.

The frozen client sends the same request model label for every profile. The dedicated server's loaded GGUF, recorded in its launch arguments, response alias, properties and model digest, identifies the actual deployment. The full run records sampled host-wide GPU memory in gpu.csv.

## Gemma E08 audit

Codex reviewed all 50 passing N0/N1 summaries in the original seeded sample, plus the only flagged token. This was a single-reviewer descriptive audit. A clear error directly contradicts a displayed value, date, rank or direction. Loose wording about steadiness is tracked separately from explicit contradictions.

- **One clear error in 50 passing summaries.** Denmark, N1, test-050. Coal was 22.573 in 2003 and 14.602 in 2005. The sentence attaches both values to 2003, and both tokens pass numeric membership.
- **Eleven additional trend overstatements.** These are listed in the table below.
- **One flag, one false flag on semantic review.** Benin, N1, test-166. The gas maximum is 0.110, so the assertion that every displayed value is below 0.111 is true. The guard still replaced the summary, including after a repair attempt. The same output loosely calls oil growth steady despite a small dip from 2015 to 2016.

| Case | Arm | Trend wording and table evidence |
|---|---|---|
| test-182 Nigeria | N0 | Gas grew each year, but the initial 8.208 jump dwarfs the later changes described as steady growth. |
| test-041 Japan | N0 | Gas dipped from 256.681 in 2012 to 256.133 in 2013 despite the consistent-upward wording. |
| test-193 Indonesia | N1 | Gas dipped from 57.426 in 2006 to 57.078 in 2007. |
| test-138 Cuba | N1 | Gas dipped from 2.338 in 2007 to 2.228 in 2008. |
| test-108 Belgium | N0 | Gas dipped in 2004 and 2006. |
| test-085 Iran | N0 | Gas dipped from 293.265 in 2011 to 292.274 in 2012. |
| test-041 Japan | N1 | The same final-year gas dip qualifies the steady-growth wording. |
| test-116 Singapore | N0 | Oil rebounded in 2021 and declined in 2022, while the prose describes a rise in the following years. |
| test-096 Tunisia | N0 | Oil dipped from 9.999 in 1997 to 9.983 in 1998. |
| test-166 Benin | N0 | Oil dipped from 4.943 in 2015 to 4.910 in 2016. |
| test-057 Slovenia | N0 | Oil rose in 1997 and gas fell in 1997, qualifying the consistent/gradual trend wording. |

## E07 results

Every profile ran all 42 receipts in every arm. The passive check X2 preserved X0A. Values separated by slashes are X0A, X1 and X3 in that order.

| Profile | Exact printed total | Arithmetic contradictions | Item F1 | Repairs triggered | Generation time |
|---|---:|---:|---:|---:|---:|
| Qwen3.5-9B | 41 / 41 / 41 | 4 / 4 / 3 | .895 / .895 / .907 | 4 | 219 s |
| Gemma 4 12B | 42 / 42 / 42 | 2 / 1 / 1 | .909 / .930 / .917 | 2 | 302 s |
| Qwen3.6-27B | 42 / 42 / 42 | 0 / 0 / 0 | .905 / .901 / .905 | 0 | 500 s |

All responses parsed and met the schema. No repair changed printed-total correctness. The 9B's one wrong total was internally consistent and escaped the passive check. Gemma's instruction reduced the count by one receipt, with a paired bootstrap interval of -7.1 to 0 percentage points. One of Gemma's baseline repeats also differed by one receipt. The two Qwen profiles had identical raw outputs across all baseline repeats. The 9B rerun reproduced all 172 generated outputs in the original E07 and all non-timing metrics.

## E08 results

Each profile summarized the same 200 tables from 113 countries. All 1,212 generation calls ended normally and all N0/N1 texts were nonempty. The 9B reproduced all 406 original generated outputs and all non-timing metrics.

| Profile | N0 flags | N1 flags | N1 minus N0, 95% interval | N2 fallbacks | N3 fallbacks | Generation time |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3.5-9B | 13 | 6 | -3.5 pp [-7.3, 0.0] | 6 | 3 | 925 s |
| Gemma 4 12B | 0 | 1 | +0.5 pp [0.0, +1.5] | 1 | 1 | 964 s |
| Qwen3.6-27B | 6 | 5 | -0.5 pp [-3.5, +2.5] | 5 | 1 | 2,010 s |

The 9B met the original approximate-halving threshold. The added deployments had a one-flag increase and a one-flag decrease. The paired country-cluster contrasts in instruction effect versus the 9B were +4.0 pp [0.0, +7.9] for Gemma and +3.0 pp [-1.5, +7.7] for the 27B. Gemma also emitted 735 numeric tokens in N0 and 1,271 in N1, so the arms offered the verifier different numbers of opportunities to flag. Both guards produced zero flagged final summaries on every profile.

The seeded 50-summary audits found clear errors in 11 passing 9B summaries, one passing Gemma summary, and two passing 27B summaries. The 9B audit carries forward from the original because its sampled text and sample JSON reproduced exactly. These are single-reviewer, descriptive audits of passing outputs. They measure a different outcome from the paired whole-cohort flag rates.

## Qwen3.6-27B E08 audit

The same rubric was applied to all 50 sampled passing summaries and all 15 flagged number occurrences. Two passing summaries contained clear contradictions.

- Taiwan, N0, test-139. The summary claimed gas increased each year. It fell from 26.853 in 2008 to 26.140 in 2009.
- Spain, N0, test-015. Gas rose from 39.970 to 68.893, about 72%. The claim that it more than doubled passed because both stated values occur in the table.

Additional loose trend wording appeared in Ireland N1 test-199, Chile N1 test-175, Switzerland N0 test-034, Moldova N1 test-042, Israel N1 test-006, and Iran N0 test-085. These concern small reversals or a rebound described as a decline across the post-peak period. Taiwan also used loose wording about the oil trend in the same summary that contains the clear gas error.

| Flag assessment | Occurrences | Cases and evidence |
|---|---:|---|
| Genuine numeric error | 2 | Latvia N1 test-105, 2009 total 7.310 versus 7.260. Benin N1 test-170, 2023 total 5.623 versus 5.463. |
| False flag, correct displayed-cell sum | 4 | Tanzania N1 test-119, both 5.075 and 7.518. Latvia N1 test-105, 8.432. Benin N1 test-170, 4.869. |
| False flag, supported approximate statement | 6 | Belarus N0 test-040, values above 31. Yemen N0 test-121, about 0.25. South Africa N0 test-188, approximate lower bound 325. Netherlands N1 test-086, around 47.7. Tajikistan N0 test-196, around 1.23. Jordan N0 test-077, around 7.8. |
| Uncertain approximation | 3 | Bangladesh N0 and N1 test-179, about 52.6 for 52.683 and 52.654. Yemen N0 test-121, around 0.27 as the upper end of a range that includes 0.278. |

The 27B repair replaced a wrong Latvia total with verified components. It rewrote three other flagged outputs without fallback and repeated the wrong Benin total, which the final fallback replaced. Gemma's repair also reached the fallback, on the valid Benin upper bound. Fallback removes the model's interpretation and keeps the fixed endpoint sentences.

## Execution verification

The full run completed with exit code zero. It made 1,722 test generation calls over loopback across both studies. The peak sampled host-wide GPU memory was 13,464 MiB, with the 27B loaded. C: had approximately 119 GiB free at completion. All 62 existing E07/E08 scorer tests passed. The per-model workspaces with raw traces, generated reports, runtime properties and freeze manifests are retained on the run host.
