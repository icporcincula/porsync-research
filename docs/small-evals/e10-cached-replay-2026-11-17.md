# E10 — Cached replay and re-grading, 2026-11-17

**No differences found in the audited cached calculations.** Twelve summary files across eleven studies reproduce their archived values, with float tolerance 1e-10 relative / 1e-12 absolute. Separately, 6,315 answer/metric comparisons across eight studies reproduce their saved scores exactly. These sets overlap; they cover the original E01–E09 and E11–E16 studies, not every later replication cohort.

| Replay | Coverage | Result |
|---|---|---|
| E01–E06 | Six summary files from original cached outputs and local labels | Matched |
| E11 | Both 9B and 27B timing summaries | Matched |
| E12–E15 | Four context-study summaries | Matched |
| E07 | 252 receipt score comparisons, including X2/X3 cached transforms | Matched |
| E08 | 800 summary-number checks across N0–N3 | Matched |
| E09 | 600 frozen tool scores; corrected per-arm boolean counts compared separately | Matched |
| E12 | 840 rule/retrieval/sanity answer checks | Matched |
| E13 | 378 implied-rule answer checks | Matched |
| E14 | 1,440 detail-probe answer checks | Matched |
| E15 | 1,200 retrieval-answer checks | Matched |
| E16 | 805 metric dictionaries: 561 local, 204 frontier, 40 frontier repeats | Matched |

E16 function-at-five counts reproduce the published local exploratory table: B 31, K 30, G 29, DQ/DS 28, D/J 27, M/X 26, S 24, ORA 20, each out of 50 function-gold tasks. E16 gold was regenerated from the current patch parser and local source snapshots; the planned human gold audit remains absent.

## Reporting fix

The E12 summary CLI previously globbed `control.9b.f16.jsonl`, whose separate control schema lacks `arm`, and crashed before writing its summary. It now skips files prefixed `control.`. A regression test reproduces the mixed-directory case. The main cached summary matches after this fix; control results are not silently pooled into the main experiment.

## Reproduction and evidence

```sh
python portfolio/small-evals/e10_audit/replay_cached.py
python portfolio/small-evals/e10_audit/regrade_cached.py
```

Both scripts reject socket connections. Summary replay copies input JSON/JSONL to a temporary directory and redirects scorer outputs there. Historical summaries and raw outputs are not overwritten. Re-grading only reads cached inputs and writes a new audit report. The replay uses one computational thread and no GPU. Relevant input and source hashes accompany the private reports in `portfolio/small-evals/results/e10/cached-replay-2026-11-17/`.

Focused validation: 50 tests passed, covering the E12 regression, E21 duplicate/score checks, E36 incomplete/tampered review rejection, the six E10 fault triggers, E08 numbers and E09 corrected grader. A Windows pyreadline destructor warning appeared after pytest's successful exit; it did not fail the tests.

## Interpretation boundaries

This closes the original cached-calculation replay backlog within the declared scope. It does **not** prove independent truth of every published headline: E01/E02 retain cached parsed decisions, timing values cannot be remeasured from final outputs, and labels/checkers may share systematic errors with the original analyses. Some summary functions aggregate saved flags; the separate answer re-grading covers the specified contexts but does not audit every compressed-summary survival label or every retrieval recall annotation. E16's human scorer audit remains open. No equivalent-mutant classification or new mutation survival estimate was attempted. Synthetic fault validation and archived replay are separate evidence.

Public draft: this report, aggregate audit summary and method scripts only. Raw tickets, contracts, receipts, summaries, benchmark sources, full input manifests and traces stay private. Method scripts depend on excluded inputs and are not turnkey public reproductions. Existing publication hold remains; no commit or push.

## Publication authorization — 2026-11-17

The user authorized committing and pushing the selected CPU-only E10/E21/E36 changes. Earlier publication-hold statements describe preparation time and are superseded for these selected artifacts. Raw private inputs remain excluded from the public release.
