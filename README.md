# Porsync Research

Public evidence behind the experiments at [porsync.com/research](https://porsync.com/research).
These are small, hardware-constrained studies, with negative results, uncertain comparisons and unfinished work documented alongside the findings.

## Start here

| Study | Evidence |
| --- | --- |
| Contract extraction replication | [Report and model summaries](portfolio/small-evals/results/e03-replication/README.md) |
| Receipt arithmetic | [Report](docs/small-evals/e07-results.md) · [Summary](portfolio/small-evals/results/e07/summary.json) |
| Numeric table summaries | [Report](docs/small-evals/e08-results.md) · [Summary](portfolio/small-evals/results/e08/summary.json) |
| Numeric-check replications | [Report and summaries](portfolio/small-evals/results/e0708-replication/README.md) |
| Tool-use replication | [Report and comparisons](portfolio/small-evals/results/e09-replication/README.md) |
| Instruction-following replication | [Results](portfolio/small-evals/results/e13-replication/README.md) |
| Context-summary replication | [Results](portfolio/small-evals/results/e14-replication/README.md) |
| 120B model on 16 GB / coding reliability (E39) | [Interim report](docs/small-evals/e39-results.md) · [Local validation](docs/small-evals/e39-local-validation/README.md) |
| Patchsmith/Aider exploratory fixtures | [Report](docs/patchsmith/comparison-2026-11-16/README.md) · [159 trials](docs/patchsmith/comparison-2026-11-16/trials.json) |
| Patchsmith v5b vs Aider on four local models (E41) | [Report](docs/patchsmith/harness-comparison-2026-11-19/README.md) · [216 trials](docs/patchsmith/harness-comparison-2026-11-19/trials.json) |
| Expert-cache comparison (E40) | [Report](docs/small-evals/e40-results.md) · [150 trials](docs/small-evals/e40-data/trials/trials.csv) |

## Check the evidence

Python 3, standard library only; no model calls or GPU required:

```sh
python verify.py
python docs/patchsmith/comparison-2026-11-16/analyze.py
python docs/patchsmith/harness-comparison-2026-11-19/analyze.py
python docs/small-evals/e40-data/scripts/paired.py
python docs/small-evals/e40-data/scripts/timing_sum.py
```

The manifest records hashes and publication transformations. It establishes file identity, not independent certification of the experiments. Public Git history begins with this curated release; private development history is not included.

Read [RELEASE.md](RELEASE.md) before interpreting reproducibility or reusing files. Questions and methodological corrections are welcome as GitHub issues; identify the study, file and claim involved.

**E39 follow-up is planned:** frontier comparisons on harder and real-fix tasks, plugin token accounting, host/shadow checks, controlled RAM-health calibration, natural-fault recovery and held-out routing evaluation. The router remains frontier-only; successful local routed coding and promotion are not established. E40 does not close those gaps.

## CPU-only eval evidence — November 17 release

User-authorized release of selected CPU-only follow-ups:

- [E10 fault triggers](docs/small-evals/e10-triggers-2026-11-17.md) and [cached replay](docs/small-evals/e10-cached-replay-2026-11-17.md): six injected faults detected, 12 summaries and 6,315 answer/metric checks match. Independent gold validation and equivalent-mutant classification remain.
- [E21 partial Stage B](docs/small-evals/e21-results.md): 13/108 planned trials recorded, all code-containment checks pass; no dtype comparison. Selected synthetic trials and source hashes included.
- [E36 review preparation](docs/small-evals/e36-review-package-2026-11-17.md): blinded review tooling prepared for 200 frozen items; independent human labels remain pending. Website excerpts and predictions are excluded.

Method scripts require excluded private modules or data; they are not turnkey public reproductions. No model calls or GPU/service actions. Only selected reports, synthetic/aggregate observations and method scripts are released; private traces, source datasets and full private input manifests remain excluded. This authorization does not publish the separate E39 or Sprocket drafts. Historical hold wording in the reports is superseded by their dated authorization notes.


## E39/E41 selected update - November 19, 2026

- [E39 direct CLI baseline B0](docs/small-evals/e39-phase-b0-2026-11-19/README.md): 21/21 independently accepted.
- [E39 B0/B1/original B2 accounting](docs/small-evals/e39-phase-b-2026-11-19/README.md): B1 36/36; original B2 reached no local attempt.
- [E39 separate B2 retry](docs/small-evals/e39-phase-b2-retry-2026-11-19/README.md): 15/15 final passes, 13 local successes and two frontier repairs; one archived quota-interrupted attempt excluded. No speed win or routing promotion; items 1 and 2 remain open.
- [E41 separate n09-n16 blind2 cohort](docs/patchsmith/blind2-2026-11-19/README.md): v5b/v6/Aider passes out of 24: gpt-oss 13/19/23, Qwen3-Coder 14/15/17, Qwen3.6 24/24/23, Edge0 18/17/23. Edge0 v5b is not blind; cohorts are never pooled.

Earlier planned-work/hold wording above is historical; the linked reports give the current measured scope and remaining gaps. This release does not include the separate frontier/Phase A or Sprocket local drafts.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

Run the three E39 package `analyze.py` scripts and the first-set E41 analyzer directly. For blind2:

```sh
python -B docs/patchsmith/blind2-2026-11-19/analyze.py --trials docs/patchsmith/blind2-2026-11-19/trials.json --out recomputed/blind2
python -B verify.py
```

## E39 held-out routing and closeout - November 21, 2026

- [Phase A frontier held-out](docs/small-evals/e39-phase-a-heldout-2026-11-19/README.md): 96/96 frontier trials recorded (aggregate summary).
- [Phase C / C1 held-out route](docs/small-evals/e39-phase-c-2026-11-19/README.md): 48/48 route trials; local baseline for the next item.
- [Phase C1b revision 2](docs/small-evals/e39-phase-c1b-2026-11-20/README.md): 48/48 route trials. blind2 17/24 local-only passes (predicted 15), heldout1 19/24 (predicted 18); 24/24 final passes in each, 12 frontier repairs. n=3 per cell; set 1 informed tuning, so cohorts are not blind and never pooled.
- [Operational closeout pilot](docs/small-evals/e39-closeout-2026-11-20/README.md): 24/24 trials, eight authored synthetic tasks, one repeat per arm. Direct, shadow and route each ended 8/8 on final passes; route had 3 local-only passes, 4 frontier repairs and 1 frontier-only decision. It was stopped once by a subscription usage limit and resumed in a fresh session, which adds startup and order confounding.

No natural OOM or prefill stall occurred, so natural-fault recovery is unverified. Token deltas are relative accounting, not subscription quota; no percentage saving is claimed. C2b was not run, so the runtime classifier is not validated. The router default remains frontier-only and no promotion is supported. E39 items 1 and 2 stay open. Private runners, fixtures, reference solutions, prompts, patches and transcripts are withheld, so generated code cannot be rescored.

## E42 completed engine comparison — November 23, 2026

[Report and reproducible saved-label analysis](docs/small-evals/e42-results-2026-11-23/README.md): Invergent's Surogate engine 1.5.15 / stock llama.cpp b11753 correct/h ratio **0.7801 (95% paired item-bootstrap interval 0.7772–0.7830)** on the first 4,520 common synthetic tasks, Qwen3.5-9B Q4_K_M, RTX 5060 Ti 16 GB, WSL2, concurrency one. A supplementary reversed-order 30-minute-per-arm repeat returned **0.7805 (0.7754–0.7855)** on 1,132 common tasks. Accuracy stayed within the frozen two-point overall margin. H2/H3 refuted, H4/H5 supported, H1 not refuted within sampled resources and private log review. Primary VM continuity remains unverified; memory states differed; intervals cover item sampling with timing fixed, not run-to-run uncertainty. Keep llama.cpp as the default for this configuration; no general engine ranking.

Selected publication authorized November 23. The package releases transformed scoring/timing observations, numerical resource series without absolute timestamps, fixed probe observations, saved summaries, window sidecars, curated configuration, provenance and an offline NumPy analyzer. It recomputes aggregates from saved labels, not answer correctness or inference. Prompts, references, full replies, raw logs/telemetry, operational paths, private implementation, weights, binaries and cache files remain withheld. Sidecar row hashes identify withheld originals; MANIFEST hashes identify released files. No upstream assets or blanket third-party license are supplied. No E39/E43 draft is included by this authorization; E39's outstanding follow-ups remain open.

## E43 incomplete compatibility pilot - November 23, 2026

[Selected compatibility record and offline accounting](docs/small-evals/e43-compatibility-2026-11-23/README.md): smaller bases and separate adapters served 32K, but full Stage A remains incomplete. Original Qwen paging stop, all 16 launched smaller-model attempts and the missing final cell are retained. Runtime repairs passed scripted CPU checks; a new 32-probe development design and conditional two-candidate Stage B scope are recorded. No new model trials, scored study, adapter-benefit claim or routing promotion. Withheld private tasks/code/graders/traces prevent independent rescoring. This selected E43 publication supersedes earlier E43 publication holds only for this package; unrelated drafts remain excluded. E39 follow-ups remain open.

## Selected evaluation articles and evidence — November 27, 2026

[Release index](docs/small-evals/publication-2026-11-27/README.md): E47/E49/E50/E51 Inkling pack development sequence; E52/E53/E54/E57 Bonsai eligibility sequence; E55/E56 CPU OCR and matched-DPI rerun; E44 held-out harness comparison. The existing E43 incomplete compatibility package is retained unchanged and linked for its new explanatory article. E29/E31b already have articles. E34 remains user-deferred, E45 excluded, E32 paused, E46/E48 without selected results. E39 outstanding follow-ups remain open.

E54 not_advance becomes E57 advance on a fresh pool; advance means evaluation eligibility, not accuracy superiority or production approval. The E57 accuracy interval -3.33 to +8.89 points includes zero. Two administrative restarts and excluded partial compute are disclosed. E51 did not reproduce the earlier apparent speed advantage. E56 dpi_robust is same-sample evidence, not fresh validation. E43 Stage A remains incomplete and Stage B unrun.

Only selected reports, configurations, summaries, analysis and transformed outcome/timing rows are released. Original-source hashes and transformations are recorded in the package PROVENANCE.json; root MANIFEST.json records released bytes. Absolute machine paths are redacted; unavailable relative links become private-source notes. Private tasks, hidden tests, references, generated code, test output, raw replies/transcripts/logs, operational timestamps, credentials, personal information, weights and private implementation are withheld. Saved labels cannot be independently rescored. E55/E56 publish aggregate summaries and scoring method only; third-party pages, labels and OCR text remain withheld (FUNSD terms unconfirmed). OCRia-nano-1 by LlamaIndex is credited with original model link and license copy, rechecked November 27 for research publication; no weights or model modifications are distributed. No blanket third-party license or endorsement is implied. No new model runs, API spend, server/GPU actions or inference reproduction.

Run the release package's E47/E49/E50/E51/E52/E53/E54/E57/E44 analyze.py scripts with Python 3 and no arguments. E52/E54/E57 output matches the adjacent summary.json. E43's existing analyzer verifies development accounting. OCR aggregate-only release does not support independent full bootstrap/scoring reproduction. This authorization supersedes historical holds only for the selected package and does not release unrelated local drafts.

E44 publication correction: the historical prose total Aider 9/24 was an arithmetic error. Its table and saved green rows agree on **10/24 (41.7%; exact descriptive 95% interval 22.1–63.4%)**, with 14 misses. Original text/rows remain intact; the appended report erratum and public analyzer disclose/reproduce the correction. No patch rescoring or model rerun; five fixture wins, zero losses and three ties, p=0.0625, are unchanged.

## E58 planner-brief evaluation — November 27, 2026

[Package](docs/small-evals/e58-2026-11-27/report.md): does a frontier planner brief lift Bonsai 2.5 through frozen Patchsmith v5? 32 authored tasks, arms A (task text), P1 (claude-sonnet-5-5 brief) and P2 (gpt-6.1-sol brief), two repeats, six blocks, all completed. **No contrast shows a detectable pass-rate effect.** P1 vs A +0.050 (95% interval 0.000 to 0.125, 20 tasks); P2 vs A +0.078 (−0.016 to 0.188, 32 tasks); P2 vs P1 on the 20-task intersection −0.075 (−0.200 to 0.000). P1 ran only the 20 tasks where Sonnet's brief met the 550-word cap (12 rejected, not regenerated), so P1 and A task sets differ. P2's full-set gain disappears on the shared 20 tasks.

A small Hermes delivery check (no performance claim) called the installed `patchsmith` plugin handlers directly: 3 of 5 tasks delivered through route mode plus `apply_patch` and passed the hidden suite, one escalated on a loop, one on low free RAM. Findings: the plugin manifest omits three registered tools; the default router mode never uses the local model; a cold router escalates until it has health history. **Addendum A1:** Hermes v0.23.0 requires a model with at least 64K context, the pinned Bonsai server serves 32K, so the first Hermes attempt failed. **A1 follow-up (2026-11-28):** with Bonsai restarted at 65,536 context for the check only (unfrozen deviation), Hermes chose and called the tool correctly on every attempt; after finding that Hermes does not forward process environment to plugins and fixing a test-command quoting fault, 4 of 5 tasks were delivered through Hermes and passed the hidden suite (meteorite looped). Five attempts kept in `phase2/a1/`; delivery only, no performance claim.

Released: report, configuration, reduced outcome/timing rows in the E57 schema, brief hashes/word counts/timings, stop records, summary, portable `analyze.py` (reproduces `summary.json` byte-identically) and `provenance.json` with original-source hashes and transformations. Withheld: tasks, hidden tests, references, planner brief text, replies, patches, transcripts, logs, weights and private implementation. Saved labels cannot be independently rescored. E39 follow-ups remain open. No paid API, new model run or website change in this release.
