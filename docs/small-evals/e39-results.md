> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E39 results — Edge0-120B-q3k on RTX 5060 Ti 16 GB / 32 GB RAM

Initial measurements 2026-11-13 to 2026-11-14; interim agent-loop write-up updated 2026-11-15. Website article prepared in source on 2026-11-15; deployment not established. Later runs are reported separately below. Question and protocol: e39-edge0-120b-constrained-hardware.md (not included in this public release). Raw logs, scripts and samples: e39-logs/ (not included in this public release).

## Verdict

**It loads and is fast enough to be interactive, but reliable agent work remains unresolved.** The initial short runs completed without faults; later agent runs encountered OOM errors and prefill timeouts. With live-context budgeting, two subsequent harder-task runs passed **27/50 (54%) and 21/50 (42%)**, despite identical settings and no execution errors. These are separate runs, not a stable capability estimate. Under thinking-on defaults it decodes at about 45 tok/s and prefills at about 1,000 tok/s. It fits only just: 15.6 of 16.3 GiB of VRAM is used, and Windows free RAM fell to near zero during load and generation. The documented requirement (16 GiB GPU, 20 GiB RAM) was met in practice, with no headroom left on this machine.

**Correctness (thinking off, greedy, the E19 harness):** HumanEval+ 0.884, MBPP+ 0.669 (see "Correctness" below). That is 2nd on HumanEval+ but 6th of 8 on MBPP+ against the E19 models; Gemma 4 12B and Qwen3-Coder-30B-A3B match or beat it on both, and are smaller and faster on this card. Median request latency was 4.45 s.

Later measurements cover thinking-on HumanEval+ and the agent loop (see below). Still unmeasured: frontier performance on the harder tasks, plugin-path tokens per accepted task, cold-cache load time, NVFP4, and an enforced 20 GiB RAM cap.

## Setup (all reproducible from e39-logs)

| Item | Value |
|---|---|
| GPU / driver | RTX 5060 Ti, 16,311 MiB, compute 12.0, driver 610.88 |
| CPU / RAM | Ryzen 5 7500F (6 cores), 32 GB (31.6 GiB total) |
| OS | Windows 11 Pro 10.0.26200 |
| Engine | Edge0-AI/Edge0 commit `da9cc526747759227714ddde0728763d95306c04` (edge0-infer 0.2.0 + edge0-strata); llama.cpp pinned `3cf03257f2…` |
| Model | `Edge0/Edge0-120B-q3k` revision `dab5ce727d494e2018626fe8896bfdc774215b17` |
| Toolchain | CUDA 13.2.1, VS 2022 Build Tools 17.14.45 (MSVC), CMake 4.2.3, Ninja 1.13.2, uv 0.11.7 |
| Build | strata: `-DCMAKE_CUDA_ARCHITECTURES=120 -DSTRATA_ENABLE_CUDA=ON`, Release; edge0-infer: `--preset windows`. Scripts: `build-strata.bat`, `build-infer.bat` |
| Run | `edge0-infer serve --model … --context N` (defaults otherwise), served on :8000, model `edge0_120b`; thinking on (the model default); temperature 0; streamed responses |
| Other GPU users | the Qwen3.5-9B :1234 server and the embedding server were stopped first; ~0.8 GB of VRAM was used by Windows |

Build friction (reported as results): CUDA 13 and VS 2022 had to be installed first (neither was present; both need UAC). The first configure picked MinGW's `windres`/gcc from `C:\msys64\mingw64\bin` instead of MSVC; fix is MSVC first on PATH and `CC=cl CXX=cl` plus explicit `-DCMAKE_*_COMPILER`. The checkout, model download and build took roughly an evening; the model folder is **85.9 GB on disk** (92 files), not the 28 GiB weight size, because the repo includes the 47.7 GB `ple-fp8.gguf`. `inspect` marks `ple-fp8.gguf` as always required. Disk: the download needs ~86 GB free.

## Load and memory

| Context | Load to ready | Peak VRAM | Min Windows free RAM | Peak engine working set |
|---|---|---|---|---|
| 8,192 | ~100 s | 15,655 MiB | 0.01 GB | 15.7 GB |
| 32,768 | ~66 s | 15,640 MiB | 0.02 GB | 22.5 GB |

Load times are warm-cache: the model files were written shortly beforehand, so cold-boot load from SSD will be slower (not measured). Strata printed a warning at start: "RAM is tight – the model's experts take 26.7 GB of this PC's 32 GB, leaving 5.0 GB for everything else. Windows will slow down (paging to disk)." Free RAM sat near 0 GB during generation (the experts are file-cached), yet there was no crash, error or visible slowdown in the runs below. Memory samples every 5 s: `serve-mem-ctx*.csv` (columns: seconds, VRAM MiB, free RAM GB, engine working set GB).

## Speed (temperature 0, streamed, single request at a time)

Decode tok/s counts streamed chunks (chunk count matched `usage.completion_tokens`). TTFT includes prefill. Prefill tok/s is prompt tokens / TTFT, a lower bound.

| Case | Context | Prompt tok | TTFT | Decode tok/s |
|---|---|---|---|---|
| smoke | 8K | 59 | 1.87 s | 33.1 |
| coding (400 tok) ×4 | 8K | 70 | 0.87–1.05 s cold, 0.21 s with prefix cache | 44.5, 45.0, 53.0, 46.6 |
| agent-style (one shell command) | 8K | 89 | 0.94 s | 46.6 |
| sustained 1,500 tok | 8K | 67 | 1.19 s | 44.8 (33.5 s total) |
| prefill ~1K | 8K | 963 | 1.81 s | 41.2 |
| prefill ~3K | 8K | 3,063 | 3.86 s | 37.0 |
| prefill ~6K | 8K | 6,063 | 5.69 s | 43.3 |
| prefill ~12K | 32K | 12,063 | 11.13 s | 36.5 |
| prefill ~24K | 32K | 24,063 | 21.3 s | 45.7 |
| coding after long prompt | 32K | 70 | 0.8 s | 46.1 |

Approximate prefill: ~790 tok/s at 3K, ~1,065 at 6K, ~1,084 at 12K, ~1,130 at 24K. Decode held at 37–53 tok/s with no degradation across a 1,500-token generation or after a 24K prompt. Engine's own log reports the same (e.g. `decode_tokens_per_second: 46.1`).

Comparison to Edge0's published figures is **not** like for like: theirs is an RTX 5090 D under a cgroup limit (62.4 tok/s chat decode, 430/778 tok/s prefill at 4K/16K). Ours is a different GPU, no enforced limit, our own prompts, and thinking on. Prefill here is higher than their constrained figure and decode is lower, which this data cannot explain.

## Observations

- The model thinks first. Every reply began with a reasoning section ("We need to respond to user…") that counts toward `max_tokens`. With `max_tokens` 400 the coding replies hit `stop_reason: length` while still thinking, so no final answer was produced (strata logs the hint to set a reasoning budget). Any agent harness needs a thinking budget or a large token limit. Reported tok/s therefore overstates the speed of useful output.
- Temperature 0 repeated the same opening text across runs, but Edge0 documents that results are not bit-for-bit repeatable; not tested.
- Prefix caching works (65 of 70 tokens reused on repeats; TTFT 0.21 s).

## Correctness (evalplus, same harness as E19)

evalplus 0.3.1 with the E19 Windows patches, greedy decoding, `--backend openai`. Thinking was **off** (a proxy on :8001 injects `chat_template_kwargs.enable_thinking=false`), which matches every E19 row. Context 16,384. Scripts and logs: `e39-logs/evalplus/`.

| Model | HumanEval base / + | MBPP base / + |
|---|---|---|
| **Edge0-120B-q3k (this run)** | 0.915 / **0.884** | 0.791 / **0.669** |
| Gemma 4 12B | n/a / 0.890 | n/a / 0.749 |
| Qwen3-Coder-30B-A3B | n/a / 0.878 | n/a / 0.738 |
| Qwen2.5-Coder 14B | n/a / 0.872 | n/a / 0.738 |
| Nemotron Bolt | n/a / 0.860 | n/a / 0.717 |
| Qwen3.5-9B (ref) | n/a / 0.848 | n/a / 0.646 |

E19 rows are the "+" columns only (other E19 rows omitted: Mellum 2, Devstral 24B, gpt-oss-20b). Against all E19 rows Edge0 is 2nd on HumanEval+ (behind only Gemma 4 12B; +3.6 pts over the 9B) and 6th of 8 scored on MBPP+ (+2.3 pts over the 9B, 8 pts under Gemma, and below Devstral 24B at 0.698). One greedy run, so differences of 1-2 points (2-4 problems on HumanEval+) are noise. 23 of 545 requests ended on the token limit (`stop_reason: length`); whether those are failures was not broken down.

### Latency during the evalplus run

Per request, from the engine's own log (545 requests: 164 HumanEval, 378 MBPP, 3 smoke), single client, thinking off:

| Metric | Median | p95 | Mean |
|---|---|---|---|
| Total request time | 4.45 s | 14.04 s | 5.45 s |
| Time to first token | 0.84 s | 1.27 s | 0.90 s |
| Decode tok/s | 58.7 | 66.7 | 57.8 |
| Generated tokens | 206 | 696 | 251 |
| Prompt tokens | 107 | 246 | 129 |

Wall time: HumanEval+ 937 s (5.7 s/problem), MBPP+ 2,078 s (5.5 s/problem); scoring the samples took about 1.5 and 4.4 min. Decode is faster here (about 59 tok/s) than the 45 tok/s measured with thinking on. I did not isolate why, so treat the difference as unexplained; it is not a like-for-like speed comparison with the E19 models.

## Not done

1. Thinking-on MBPP+ was only partially generated; the 106 archived samples were subsequently scored in the local follow-up below. The full 378-problem run remains incomplete. Thinking-on HumanEval+ and agent-loop results are now reported below; the initial scope has been superseded.
2. Cold-cache load, NVFP4, and an enforced 20 GiB RAM limit (Windows has no cgroup equivalent; a Job Object limit would be the route).
3. Context beyond 24K prompt tokens (131,072 is the model default). 32K ran stably with a 24K prompt.
4. Tuning knobs (`--pool-workers`, `--pcie-mode`, `--vram-reserve-mib`, `--kv-resident`) left at defaults.

## Implication for the sprocket study

None yet: it cannot share the GPU with the :8081/T/Q/Z servers (one model at a time), and a thinking-first 120B at ~45 tok/s is slower per useful token than the 9B arms. If wanted later it would be a separate arm needing its own prereg amendment.


## Agent work: the useful limit is reliability (interim, 2026-11-15)

The loading test answered whether a 120B model could respond on this machine. It did not establish that it could finish unattended coding work. The follow-up used Patchsmith, independent tests and fresh task attempts. The [router record](e39-router-design.md) contains the original soak, frontier timing and implementation details; the write-up handoff (not included in this public release) records the later runs and code changes.

On the original seven small coding fixtures, Edge0 passed 67-96% per fixture over 24 repeats. Sonnet and Haiku through the Claude CLI each passed 70/70 (140/140 together), with fixture medians of 25-43 seconds and 27-36 seconds respectively. Edge0 medians were 21-33 seconds. These are tiny fixtures and different orchestration paths, so they establish neither general frontier superiority nor plugin-path savings. They do show that fast local decoding did not translate into a broad task-latency advantage. The original blocked/refusal fixture was excluded from the frontier comparison.

Thinking remained off for agent work. In a separate correctness comparison, thinking-on HumanEval+ scored 0.616 against 0.884 with thinking off, at about 12 times the generation time. Partial thinking-on MBPP+ output was unscored at that point; the local follow-up below now reports that subset separately.

### Harder synthetic tasks and the budget correction

The ten h01-h10 fixtures exercise multi-file maintenance contracts. They are synthetic tasks with independent tests, not ten unseen production projects. Each run below contains five attempts per fixture. The live-context runs used Edge0-120B-q3k, a 32,768-token context, temperature 0, thinking off, 30 maximum turns and a 30,000-token budget.

| Run | Budget and client | Done with green tests | Execution errors |
|---|---|---|---|
| Original | Cumulative, 24,000 | 18/50 (36%) | Not tabulated here |
| Larger cumulative budget | Cumulative, 30,000 | 7/50 (14%) | Not tabulated here |
| ctxfix | Live-context, original client | 12/50 (24%) | 8 |
| retryrun | Live-context, retry-capable client | 27/50 (54%) | 0 |
| repeat2 | Same settings as retryrun | 21/50 (42%) | 0 |

The old budget counted cumulative prompt expenditure across turns, including repeatedly supplied context. The corrected budget caps the live prompt instead. This removes a premature cumulative-spend stop, but does not guarantee completion: repeated tool calls and the turn limit still stop unsuccessful attempts. Commit `5e8045a` introduced the mode and transient-fault retry; `844fed1` made live-context budgeting the default. `PS_BUDGET_MODE=cumulative` restores the earlier behavior.

The ctxfix run had two server OOM HTTP 400s and six prefill stalls reaching the 180-second client timeout. The handoff reports average free host RAM of about 0.68 GB. Memory pressure is a plausible explanation, not an isolated causal result. The client now retries once on a timeout or an HTTP 400 explicitly reporting out of memory; other 400s and second failures surface.

**The later gain cannot be credited to the retry.** Neither retryrun nor repeat2 had logged OOM, HTTP 400 or HTTP 499 events, and the retry probably never fired. Token-count log lines containing 400 or 499 are not HTTP failures. Unit coverage exists, but recovery from a live fault remains unverified. The runs changed conditions and are not a controlled ablation of the retry or budget mode.

| Fixture | retryrun | repeat2 |
|---|---|---|
| h01_cursor | 2/5 | 2/5 |
| h02_stock | 3/5 | 4/5 |
| h03_import | 4/5 | 4/5 |
| h04_access | 3/5 | 4/5 |
| h05_retry | 3/5 | 2/5 |
| h06_retention | 3/5 | 0/5 |
| h07_queue | 2/5 | 4/5 |
| h08_config | 2/5 | 1/5 |
| h09_search | 3/5 | 0/5 |
| h10_intervals | 2/5 | 0/5 |

Every unsuccessful attempt in these two runs ended in `loop_detected`, except one `max_turns` stop in each run. These are stalled agent attempts, not recorded transport errors. Fixture median times were about 22-45 seconds. The six-pass aggregate swing and the three-pass swings on h06 and h09 make per-fixture routing estimates premature. Repeats of ten known tasks do not provide the breadth of 100 independent tasks.

### Replay of real fixes

Four historical fix commits qualified by failing before the fix and passing afterward with the same tests. Three attempts per task produced **0/12 under cumulative budgeting and 7/12 under live-context budgeting**. This is encouraging evidence that the harness budget matters. It is a small exploratory replay from one author's repositories, not a matched proof of the size of the budget effect or a general coding benchmark. Frontier results on these tasks are not measured.

### Router decision and remaining evidence

The router remains **`frontier-only` by default**. Its category table is unchanged. A label such as `multifile` cannot transfer the original fixture's 96% success rate to harder work; unknown tasks stay on frontier. Implementation and offline tests do not establish a successful live routed deployment.

Shadow mode can validate logging and the host handoff. Its proposed below-10% frontier-disagreement bar cannot establish local quality: frontier passed every original fixture, so that bar could pass even if the local choice were poor. Promotion requires local-side paired evaluation on held-out tasks with independent tests. No shadow cohort or route promotion has been measured.

The correct local-first expected-time expression is `p * E[t_success] + (1 - p) * (E[t_failure] + t_frontier)`. Medians are not conditional means, and no measured end-to-end routed latency is available. Quota saving must likewise be measured as frontier tokens per accepted, verified task through the host; CLI token totals do not establish subscription savings. Offline execution is possible with a local host, not an offline Claude subscription path.

Next when quota returns: measure frontier performance on h01-h10 and the mined tasks, plugin-path tokens per accepted task, and host/shadow integration. Health thresholds and live retry recovery also remain unvalidated. [E40 is now complete](e40-results.md): a separate Qwen/llama.cpp cache experiment, with faster generation but no demonstrated coding-throughput gain. These historical Edge0 runs are not its matched cache-off baseline.

### What is still missing: more than frontier calls

The quota-blocked work is frontier comparison on harder and mined tasks, plugin-path token accounting, and host/shadow measurements. Separately, live retry recovery and health thresholds need validation; local routing promotion needs paired held-out evidence and a measured end-to-end routed run. A route flip is a conditional deployment decision, not a missing benchmark to perform automatically. Optional coverage gaps remain: cold-cache load, thinking-on MBPP+ completion/scoring, NVFP4, an enforced RAM cap, longer contexts and serving-knob tuning. None is silently completed by E40.

### Evidence and verification boundary

Initial raw artifacts are in `e39-logs/`. Later artifacts remain outside this repository under `C:\e39\`: `ctxfix`, `retryrun`, `repeat2`, `replay_v1` and `replay` (plus the earlier `harder`, `harder2` and `frontier` runs). The harder-run console summaries use UTF-16. For this write-up, the three live-context summaries and both replay result files were read directly; retryrun/repeat2 fixture totals and replay totals agree with the handoff. Fault attribution and historical test results are reported from that handoff, not from a new model run or full log audit.

The Patchsmith checkout was clean on `feature/e39-router` at `844fed1` when inspected. The handoff reports **168 tests passed, 1 skipped** through its pre-commit hook; that suite was not rerun for this documentation change. No model runs, server changes, router-table edits, site publication or push were performed for the write-up.


## Local validation follow-up — 2026-11-15

The [local validation record](e39-local-validation/README.md) archives the follow-up scripts, raw observations and limitations. Scoring the 106 archived thinking-on MBPP samples gave 98/106 base and 87/106 combined base-plus-extended passes. On exactly those IDs, the historical thinking-off run passed 95/106 and 84/106. This interrupted, nonrandom subset is not a full MBPP+ score or a reliable thinking benefit estimate. No additional MBPP samples were generated.

The local follow-up exercised the default health gate: available RAM was 0.011–0.347 GiB, and all three route checks returned `frontier_required` with `low_ram`; no routed coding attempt ran. Seven short inference probes succeeded. All four injected retry cases behaved as intended against the real backend, but natural OOM/prefill-stall recovery is still unmeasured. One 28,036-token retrieval prompt returned the correct marker in 25.344 s. The original E40 server was restored and its health endpoint returned `ok`. No threshold, table or global mode changed.

Still open locally: controlled health calibration and natural-fault recovery; a successful routed coding attempt was blocked by the unchanged RAM gate. Paired held-out comparisons remain incomplete without frontier outcomes. Optional cold-cache, enforced-cap, alternate-quant and full thinking-on MBPP generation were not run.
