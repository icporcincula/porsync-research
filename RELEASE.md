# Public evidence release â€” 2026-11-16

## Included

Nine study groups linked by the website: reports, aggregate results, frozen configurations and selected analysis scripts. E40 includes all 150 trial rows, 90 timing observations and VRAM series. E39 includes the bounded local-validation observations, retrieval prompt, partial MBPP score summary and sample-ID/hash manifest. Historical identifiers remain stable for citation.

## Withheld or unavailable

This is not the complete private archive. Receipt images/text, contract excerpts, third-party datasets, generated benchmark solutions, full model-response traces, private project code and agent transcripts are excluded pending redistribution/privacy review. Later E39 logs exist only on the run machine; exact E40 timing source prompts were not archived. Model weights and runtimes are not supplied. No claim is made that these excluded files cannot ever be published.

The reports retain historical descriptions of full-archive checks; those descriptions do not imply the underlying files are public. Unavailable Markdown links have been replaced with explicit notes. Historical build/status paragraphs describe their original date, not the present website deployment.

## Reproduction boundary

The E40 paired and timing analyses run directly on the included data. Other reporting scripts and E39 diagnostic scripts are method references: they depend on excluded inputs, private implementation modules, local runtimes or machine paths and are not turnkey reproductions. Do not run the E39 diagnostic script without adapting its environment; it initiates local inference. The public package supports inspection of reported aggregates, not independent regeneration of every study or scoring of every raw response.

## Publication review and transformations

An explicit file allowlist was exported from a fixed source revision, without private repository history or uncommitted work. No broad directory mirror was used. Machine-local user/workspace paths were generalized. Text was normalized to UTF-8/LF; E40 analysis input paths were made portable and misleading cold/warm timing labels corrected to first/later. Source and released hashes are recorded in MANIFEST.json. Results were not changed. Raw data exclusions reduce redistribution and privacy exposure; automated secret checks are supplementary, not a guarantee.

## Rights and provenance

This release does not grant rights to excluded datasets, third-party implementations or model weights. No blanket open-source license is asserted over historical artifacts. Consult upstream terms when obtaining inputs independently. Public availability permits inspection; obtain permission before redistribution or reuse where required. Author-created aggregate measurements are distinguished from source datasets by the file inventory and study reports.

## Added 2026-11-16: Patchsmith/Aider exploratory comparison

Reviewed and approved for publication on 2026-11-16. Five curated files add a report, 159 source-hashed trial rows, summary, retrospective configuration and offline analyzer. These summarize completed runs; no new inference occurred. The duplicate Aider result is excluded. Original result hashes are retained per row; patches, prompts, private paths, full logs and task sources are withheld. Counts can be recomputed, but code cannot be independently re-scored from this package. Exact model/server identities and run-time Patchsmith revision are incomplete. This is not B2 or daily-use validation and does not close E39 follow-up. The initial source_revision remains provenance for the original release; new entries explicitly identify uncommitted local sources. Publication includes only these selected artifacts; private logs and code remain excluded.

## E41 Patchsmith v5b vs Aider cross-model comparison â€” 2026-11-19

Five curated files in `docs/patchsmith/harness-comparison-2026-11-19/`: report, 216 trial rows (Patchsmith v5b and Aider, four local models, 8 held-out fixtures x 3 runs), summary, retrospective configuration and an offline analyzer. Completed runs only; no new inference. Not blind: v5b and the gpt-oss harmony-finish fix were written after seeing failures on these fixtures. Quant and serving flags differ per model. The opencode arm is excluded as a launcher fault. Transcripts, server logs, patches, fixture sources, reference solutions and the private Patchsmith source stay withheld; counts are recomputable, runs are not re-scorable. A blind follow-up on new fixtures (n09-n16) is running and is not part of this release.

## CPU-only eval evidence â€” November 17 release

User-authorized release of selected CPU-only follow-ups:

- [E10 fault triggers](docs/small-evals/e10-triggers-2026-11-17.md) and [cached replay](docs/small-evals/e10-cached-replay-2026-11-17.md): six injected faults detected, 12 summaries and 6,315 answer/metric checks match. Independent gold validation and equivalent-mutant classification remain.
- [E21 partial Stage B](docs/small-evals/e21-results.md): 13/108 planned trials recorded, all code-containment checks pass; no dtype comparison. Selected synthetic trials and source hashes included.
- [E36 review preparation](docs/small-evals/e36-review-package-2026-11-17.md): blinded review tooling prepared for 200 frozen items; independent human labels remain pending. Website excerpts and predictions are excluded.

Method scripts require excluded private modules or data; they are not turnkey public reproductions. No model calls or GPU/service actions. Only selected reports, synthetic/aggregate observations and method scripts are released; private traces, source datasets and full private input manifests remain excluded. This authorization does not publish the separate E39 or Sprocket drafts. Historical hold wording in the reports is superseded by their dated authorization notes.


## E39/E41 selected publication - 2026-11-19

User authorized publication of the E39 B0/B1/original B2 and separate B2-retry packages, and E41 blind2. Only those selected packages and the first-set report follow-up pointer are added; unrelated local drafts are excluded.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

Original-source hashes and historical transformations are retained. Report authorization banners and follow-up pointers were added; configuration publication labels were refreshed. No numerical results were changed. Source hashes do not certify run-time executable snapshots. Historical hash-drift statements are preparation records; the staged release is verified as a whole before commit.

Selected text files were normalized to LF and trailing line whitespace removed. Original byte hashes remain in the provenance manifest; numerical results are unchanged.

## E39 held-out routing and closeout selected release - 2026-11-21

User-authorized release of four E39 packages: Phase A held-out summary, Phase C (C1), Phase C1b revision 2 and the operational closeout pilot. Each contains curated outcome/usage rows or summaries, configuration where present, an offline `analyze.py` and a README with limits. Original-source hashes are in the working-tree record; released-file hashes are in MANIFEST.json. Withheld: private runners, fixtures, reference solutions, prompts, patches, transcripts, raw test output and machine paths. Not included: the E39 frontier follow-up, the C2a label probe, E42, E43 and Sprocket drafts. No model runs or API spend were performed for this publication.
