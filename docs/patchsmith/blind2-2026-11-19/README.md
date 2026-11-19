# E41 blind set 2: n09–n16, four local models

## Publication update - 2026-11-19

User-authorized selected evidence release. Historical local-only/hold and pending-verification statements below describe preparation time and are superseded by this dated update.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

## Historical run and analysis record

Analyzed 2026-11-19 from completed saved outputs only. No inference, GPU use, server operation, commit, push, deployment or publication. Curated public evidence is prepared locally under the existing publication hold.

## Result

On these eight new synthetic tasks, v6 improves gpt-oss from **13/24 to 19/24**, while Aider passes **23/24**. Qwen3-Coder changes from **14/24 to 15/24**, versus Aider **17/24**. Qwen3.6 passes **24/24 in both Patchsmith arms**, versus Aider **23/24**. Edge0 passes **18/24 with v5b, 17/24 with v6, and 23/24 with Aider**: no v6 gain on this cohort. This does not establish a general harness winner. In particular, the earlier n01–n08 Qwen3-Coder advantage for Patchsmith does not repeat here.

| Deployment | Patchsmith v5b (`v5`) | Patchsmith v6 | Aider |
|---|---:|---:|---:|
| gpt-oss-20b MXFP4 | 13/24 | 19/24 | 23/24 |
| Qwen3-Coder-30B-A3B-Instruct Q3_K_M | 14/24 | 15/24 | 17/24 |
| Qwen3.6-35B-A3B UD-IQ3_XXS | 24/24 | 24/24 | 23/24 |
| Edge0-120B q3k | 18/24 | 17/24 | 23/24 |

Edge0 is now included from the successful post-reboot rerun. The earlier 12:43 launch failed twice at context 32,768 (13:02 retry; 13:22 failure); the original morning batch also logged a startup failure. The user reports a RAM spike and reboot; the surviving run log establishes startup outcomes, not the RAM-spike cause or reboot itself. The rerun starts 14:00:37, is ready 14:01:45, and completes all arms at **16:32:59 +08:00 on 2026-11-19**. `serve.ps1 32768` and the surviving server log confirm unchanged 32,768 context, preserving within-Edge0 arm context comparability. Startup failures are operational exclusions, not failed task attempts. No retry or service action was performed by this analysis. Do not pool this cohort with n01–n08, tuning, replay, held-out or frontier trials.

## Design and chronology

Eight fixtures × three attempts × three arms × four models = **288 saved attempts**, with no missing or duplicate keys. The fixtures cover run-length encoding, number ranges, CSV parsing, pagination, Roman numerals, rolling windows, suggestions and dictionary differences. A pass is the saved independent `unittest discover -q` outcome, not the model's finish claim.

The separate Patchsmith checkout is clean at `0e4f1424de66e60ad0e9189a6bada789a081ba71` on `feature/e39-router`. The fixture commit `b30f29c` is dated 07:13:50 +08:00; v6 commit `0e4f142` is dated 07:17:01; the batch starts at 07:18:54, all on November 19. Commit notes say v6 was designed from n01–n08 failures before these tasks were run. This supports holding n09–n16 out from observed failure-driven tuning, not independence of task authorship or external preregistration. **Edge0 v5b and the gpt-oss recovery fix were tuned after earlier failures and are not blind interventions.** Their n09–n16 scores concern a separate cohort held out from that observed tuning; they do not make the earlier n01–n08 replay results blind. The historical source uncertainty in the earlier report remains historical; this follow-up has committed fixtures and harness code. Current source hashes are recorded separately from run-time evidence and are not proof of an archived executable/runtime snapshot.

The batch runs v5, then v6, then Aider, serially for each model. v5 selects frozen v5b, including the pre-existing narrow Harmony finish recovery. v6 adds **both** a 4,096-token completion cap (v5b: 2,048) and withdrawal of read-only tools after five consecutive reads until an edit or test resets the counter. This is a two-change package, not an isolated output-cap or tool-policy ablation. Both Patchsmith arms use 30 maximum turns, 30,000 live-context tokens and a 420-second request timeout. Aider uses whole-file edits, automatic testing, tests supplied read-only, no Git/repository map/auto-lint, and a 600-second process timeout. Its wrapper does not explicitly pin sampling temperature. These are unequal whole harness budgets, not matched-latency arms.

Edge0 uses `edge0-infer serve` with the q3k model and context 32,768 from `blind2c.ps1`/`serve.ps1`. Other serving configurations come from `blind2.ps1` and `blind2b.ps1`: native Docker-distributed Vulkan llama-server, context 32,768, flash attention on, Jinja, 99 GPU layers. gpt-oss uses default KV/MoE options; Qwen3-Coder uses q8_0 K/V and six CPU MoE layers; Qwen3.6 uses q8_0 K/V and eight CPU MoE layers. Quantization and backend defaults confound cross-model comparisons. The hardware is the earlier RTX 5060 Ti 16 GB / Ryzen 5 7500F / approximately 32 GB RAM setup. No model was loaded to recheck fit. Exact runtime revision and Aider effective sampling defaults remain incompletely pinned.

## Per-fixture passes

Each cell is out of three. PS5 means frozen v5b; PS6 means v6.

| Fixture | gpt PS5 | gpt PS6 | gpt Aider | Coder PS5 | Coder PS6 | Coder Aider | Q3.6 PS5 | Q3.6 PS6 | Q3.6 Aider | Edge0 PS5 | Edge0 PS6 | Edge0 Aider |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| n09 RLE | 3 | 2 | 3 | 1 | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 3 |
| n10 ranges | 0 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 1 | 3 |
| n11 CSV | 0 | 2 | 2 | 1 | 1 | 1 | 3 | 3 | 2 | 0 | 1 | 3 |
| n12 pager | 3 | 2 | 3 | 1 | 1 | 1 | 3 | 3 | 3 | 3 | 3 | 3 |
| n13 Roman | 1 | 2 | 3 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 3 |
| n14 window | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 |
| n15 suggest | 1 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 2 | 1 | 3 |
| n16 dictdiff | 2 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |

gpt-oss v6 gains nine successes across ranges, CSV, Roman numerals, suggestions and dictdiff, but loses one each on RLE, pagination and rolling windows. Its net +6 is not uniform improvement. Coder's +1 is gains on RLE/dictdiff and a loss on suggestions. Edge0 gains one CSV success with v6 but loses one RLE and one suggestions success, net -1. This small set shows no v6 benefit for Edge0. Three repeats per task give little precision; repeated attempts are not 24 independent task samples. No significance or model ranking claim is made.

## Failure audit

| Arm | Failed attempts and saved stopping reasons |
|---|---|
| gpt-oss v5b | 4 execution errors (HTTP 500), 4 model-blocked, 2 loop stops, 1 turn cap |
| gpt-oss v6 | 2 execution errors (HTTP 500), 1 model-blocked, 1 loop stop, 1 turn cap |
| gpt-oss Aider | 1 unsuccessful CSV edit; normal process exit, log reports a token limit |
| Coder v5b | 1 execution error (HTTP 500), 5 model-blocked, 2 failed-test stops, 2 turn caps |
| Coder v6 | 9 model-blocked; no terminal execution error |
| Coder Aider | 6 unsuccessful edits (CSV 2, pagination 1, Roman 3), 1 pagination timeout |
| Qwen3.6 v5b/v6 | No failed attempts |
| Qwen3.6 Aider | 1 CSV timeout |
| Edge0 v5b | 4 turn caps, 1 model-blocked finish, 1 loop stop |
| Edge0 v6 | 3 turn caps, 3 loop stops, 1 no-tool-calls stop |
| Edge0 Aider | 1 window generation-limit/empty-answer failure; normal process exit |

Full fixture/repeat/turn failure identities are in [summary.json](summary.json). Repeat IDs are normalized to 1–3 (the Aider source uses 0–2).

The gpt-oss server log has eight parser exceptions across the entire batch: two malformed JSON argument strings and six input/channel parse failures. Not all server exceptions are terminal failures: two final-channel finish messages are recoverable by the existing client recovery, whereas the saved rows contain six terminal execution errors. v6's terminal errors are n09 repeat 1 and n12 repeat 2, both malformed channel/input messages; the larger cap does not eliminate these. The log includes a final-channel `json` message without the `finish` marker that the narrow recovery requires. Do not equate all final-channel errors with recoverable finishes.

Unlike the earlier cohort, Coder has one observed JSON argument parse error, in v5b n09 repeat 3. Its server log contains one parser exception; Qwen3.6 has none. Coder's remaining failures involve substantial unsuccessful interaction, with all three arms failing Roman numerals and struggling with CSV/pagination. Inspected Aider logs show repeated failed tests, reflection stops and a token-limit diagnostic on one CSV run. These observations support task/harness difficulty in this setup, not an intrinsic model ceiling or a pure transport explanation. The Aider token-limit message reports an unknown `0` limit; it does not establish the actual server context capacity.

### Edge0 failure review and source reconciliation

All **72/72 expected keys** are present exactly once: 24 per arm. All 48 Patchsmith transcript results match one and only one per-run record by transcript identity, status, stopping reason and turns; no orphan records remain. The original `.out` files are **UTF-16 with BOM**, while the result JSON is UTF-8. Console and saved table fixture counts agree with the independent-test rows. The [Edge0 audit](edge0-audit.json) includes original byte hashes for all 128 files under the supplied Edge0 directory, including results, consoles, tables, transcripts, Aider logs and per-run records. Hashes disclose provenance; raw traces remain private.

There are **no terminal execution/parser errors or request/process timeouts** among Edge0 task attempts. The surviving server log contains no observed error/exception lines; this is not proof that every malformed response would be diagnosed. Failure mechanisms overlap with wrong edits, so they are not disjoint measures of model ability:

- v5b turn caps: n10 repeats 2–3 and n11 repeats 1–2; loop: n15 repeat 3; model-blocked finish: n11 repeat 3. Repeated no-op or unsuccessful edits, failed tests and unsupported claims about corrupted tests/stale bytecode appear in the transcripts. Those model claims are not established environmental faults.
- v6 turn caps: n09 repeat 1 and n11 repeats 1–2; loops: n10 repeat 3 and n15 repeats 1–2. n10 repeat 1 ends `no_tool_calls`: the assistant emits tool markup as plain text without a parsed tool call. This is an observed interaction/format failure, not a server-side parser exception.
- STOP guard warnings appear in **3 of 6** failed v5b transcripts and **5 of 7** failed v6 transcripts (six v6 warning events). STOP is a tool warning, not an extra trial or necessarily the final stop reason. The failure table retains the terminal reason.
- All 13 failed Patchsmith attempts have failed in-loop tests and `applied=false`; independent checks run after rollback and therefore show unrepaired baselines. These are operational attempt failures with unsuccessful work, not 13 independently submitted wrong patches. No attempt is removed or re-scored. There are no terminal `tests_failed` rows for Edge0.
- Aider n14 repeat **2** (original ID 1) spends 180.5 seconds in long reasoning, produces an empty answer, logs a token-limit warning, and has no applied-edit marker. The process exits 0 while independent tests fail. Classify this as **generation-limit/empty-answer**, not a genuine wrong submitted fix or a process timeout. Aider reports an unknown limit `0`, which does not prove server context exhaustion. The portable selected-row category remains the original coarse `unsuccessful_edit`; this review supplies the narrower interpretation.

## Descriptive timing

Median seconds per attempted task, including failures:

| Deployment | v5b | v6 | Aider |
|---|---:|---:|---:|
| gpt-oss | 49.304 | 45.757 | 26.550 |
| Coder | 50.204 | 74.406 | 61.300 |
| Qwen3.6 | 30.078 | 26.711 | 128.900 |
| Edge0 | 29.320 | 35.093 | 310.750 |

Patchsmith timing includes its runner's trial work; Aider records process wall time before the final independent check. Edge0 ran later after a reboot reported by the user. Fixed arm order, differing budgets, process startup, early failures and timeout censoring prevent interpreting this as an isolated inference-speed comparison or net verified-throughput gain. No timing claim is used to promote a router.

## Reproduction, validation and release boundary

From this package directory, recompute the selected saved-row aggregates with Python 3 (standard library only):

```sh
python -B analyze.py --trials trials.json --out recomputed
```

Private extraction mode requires excluded raw inputs. No model calls or tests are executed by the analyzer.

The analyzer checks the full expected key grid, unique repeats, boolean outcomes, Patchsmith saved independent-test return codes, failing baselines, no test filenames in reported changed files, and Aider's saved test-tail agreement and test-loop flag. This is a saved-evidence audit, not a rerun or independent verification of unarchived file integrity. Aider's runner supplied tests read-only but did not archive a protected-file hash check. Private transcripts and failure logs were inspected; raw inputs were hashed. [sources.json](sources.json) preserves original result hashes; [configuration.json](configuration.json) records selected method and diagnostic provenance. Selected trials omit prompts, patches, code, notes, test output, authentication and personal paths. No fixture/reference solutions or private implementation code are released.

This package is a local draft with selected rows, a portable analyzer, configuration, report and hashes. It is **unpublished**, as are the existing E41 public drafts; no live availability claim is added. Earlier unrelated manifest drift is reported separately rather than silently repaired. No website/article edit was needed for this analysis-only request. Publication, source commits, site integration and deployment remain deferred.

Follow-up: freeze effective runtime/sampling settings, counterbalance order, expand distinct unseen tasks, and separately ablate the completion cap and read-tool withdrawal if causal attribution is wanted. No reruns are initiated here. E39 plugin accounting/integration, health calibration, natural recovery and runtime routing validation remain open; the router stays frontier-only. See [the earlier comparison](../harness-comparison-2026-11-19/README.md) for n01–n08 and historical tuning limits.

## Completed analysis checks

All 288 expected trial keys and saved outcome checks pass. Private-input and curated/public-row recomputations produce identical summaries; all 96 per-fixture table cells match. Analyzer Ruff lint/format and selected-document link checks pass. Local draft package hashes pass; publication and commit IDs remain for the user. Edge0 hash/audit checks cover all 128 supplied files and 48 per-run records. The repository-wide public manifest still differs on the pre-existing `docs/patchsmith/harness-comparison-2026-11-19/README.md`; that unrelated file and its historical hash were preserved. The Patchsmith checkout remains clean. Two recoverable finish events were confirmed in v5b gpt-oss transcripts (n13 repeat 1 and n14 repeat 3). No generated task code was executed in this analysis.
