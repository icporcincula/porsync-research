> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E57: Bonsai versus Inkling through Patchsmith (private)

Completed 2026-11-26 at 22:53:50 local time (Asia/Shanghai). All 360 scored attempts and 12 unscored development attempts completed. The frozen rule returns **advance**: Bonsai passes the prespecified 10 percentage point accuracy noninferiority margin and verified-throughput superiority gate. This advances evaluation eligibility; it does not establish accuracy superiority or authorize production promotion.

| Measure | Inkling C | Bonsai B |
|---|---:|---:|
| Verified successes / attempts | 163 / 180 | 168 / 180 |
| Verified success rate | 90.56% | 93.33% |
| All scored attempt seconds, including failures | 21,712.507 | 5,363.626 |
| Verified tasks per hour | 27.026 | 112.760 |

B minus C accuracy is +2.78 percentage points, with paired task-cluster 95% interval **−3.33 to +8.89 points**. B/C verified-throughput ratio is **4.172**, interval **2.957–5.643**. Deterministic percentile bootstrap: 10,000 resamples, seed 5757; both arms and repeats stay in each task cluster. No undefined ratio resamples. The accuracy interval includes zero; a higher observed success count does not prove higher accuracy. Of 90 task clusters, B had more successes on 10, C on 9, and 71 were tied.

| Family | Scored attempts per arm | C successes | B successes |
|---|---:|---:|---:|
| feature_edge_cases | 40 | 36 | 38 |
| scorer_summary_repair | 40 | 40 | 38 |
| new_script | 40 | 29 | 34 |
| multi_file_change | 40 | 38 | 38 |
| single_file_repair | 10 | 10 | 10 |
| test_driven_recovery | 10 | 10 | 10 |

These family counts are descriptive, without separate confirmatory tests. The pool contains 90 tasks, 45 Python and 45 JavaScript, with the six prespecified family counts 20/20/20/20/5/5. Each task ran twice per arm. All six development tasks passed on both arms; development observations were not used for tuning.

Block order was C1, B1, B2, C2; successes were 83, 84, 84, 80 out of 90 respectively. C failures: 10 truncations, 4 wrong patches, 2 timeouts, 1 server error. The server error on `f57-ns-epoch` was HTTP 500 while parsing malformed tool-call JSON; it remains counted as a failure with its elapsed time. B failures: 10 wrong patches and 2 blocked refusals. No boundary violations, duplicate rows, missing attempts or invalid rows. All four stop records say completed. The final owned server shutdown confirms exit; no production configuration was changed.

## Methods and deviations

Frozen execution protocol (private source reference withheld), authoring notes (private source reference withheld), first continuation amendment (private source reference withheld), and second continuation amendment (private source reference withheld) are the method record. Task authoring commit: `00ca3b55c73fa1cf10ad9c3b3e78bf83c6f66d14`. Execution commit: `685f887a`. Continuation commits: `8f8aa5b3`, `f41e3fe0`. Frozen protocol SHA-256: `cd2084708cb5081992606b19ad1b315db49f0bc1042b881c685696f40fbc2680`.

The user paused the campaign after 176 completed attempts. Block-2 `f57-ns-csv2md` was interrupted and restarted from pristine fixtures after explicit authorization. A second unexpected process disappearance occurred after 351 completed attempts; the cause is unknown. Block-4 `f57-ns-sortlines` was interrupted and restarted from pristine fixtures after explicit authorization. Both partial workspaces and original markers remain, and both replacement rows are flagged administrative restarts. No completed result was rerun or discarded. Separate continuation locks, workspaces and server logs retain provenance. Original frozen files, budgets, tasks, scoring and analysis remain unchanged.

Primary timing excludes partial compute from the two interrupted attempts, along with server loading, warmup and downtime. Thus the primary throughput ratio describes completed scored attempts, not total campaign cost or uninterrupted reliability. A total-cost or reliability claim cannot be made from it. No sensitivity estimate is substituted for the prespecified statistic. The stale running status after the unexplained process loss was corrected in the user update; live status alone was insufficient evidence of an active run.

The arms differ in weights, quantization, runtime, sampler and reasoning policy. C uses Inkling-2-Mini IQ3_XXS, thinking off, temperature 0; B uses Ternary Bonsai 2.5 27B PTQ1 with medium reasoning and temperature 1. Shared limits: 32,768 context, 24,000 input budget, 25 turns, 8,192 per-request output, 49,152 cumulative output, 900-second model phase, one slot, unchanged Patchsmith v5 harness. Hardware: RTX 5060 Ti 16 GB and Ryzen 5 7500F. No paid API was used.

This is a synthetic hand-authored coding pool, with small families at ceiling and several simple repairs. Family and language effects are not established. The result does not isolate compression, prove general coding superiority, resolve E39 follow-ups, or establish the user's everyday incumbent configuration. Further deployment decisions require a separate authorized step; no new model run is required to close E57.

## Validation and evidence

Final offline checks: **46 passed in 88.60 seconds** (21 E57 execution/continuation checks and the unchanged 25-test E52 regression suite). The sole warning is the existing unregistered `slow` pytest mark in E52. E52 also passed 25 tests before and after task authoring; authoring validation recorded 193 E57 pool tests and a clean 96-task self-check. No pool, reference, hidden suite or original execution source was changed during closeout. Git diff checks passed. The closeout verified frozen hashes, all block orders, 360 rows, all 1,440 expected scored attempt artifacts and identical recomputed analysis; its manifest hashes 1,910 selected evidence files.

Machine-readable summary (private source reference withheld) contains the frozen analysis and per-task table. The evidence manifest (private source reference withheld) hashes private rows, stop records, request/transcript artifacts, resources, protocol/freeze records, administrative markers and continuation scripts. Raw evidence stays in ignored `tmp/e57`; workspaces stay in `[withheld local path]`. Do not rerun the original campaign, remove its locks or rematerialize this spent pool. Offline reproduction: `python -B scripts/e57_analyze.py --rows-dir tmp/e57`; closeout verification: `python -B scripts/e57_closeout.py`.

Publication and public-evidence synchronization remain explicitly deferred. No public repository was accessed, no website article was published, no push was made, and no default model/router was changed. The public record remains unsynchronized by authorization, rather than being described as complete. Only local models were run; no forbidden prior-study result file or sealed task contents were manually inspected.
