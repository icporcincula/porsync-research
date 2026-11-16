> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E40 — Does expert caching improve useful local inference?

Status: **runs completed 2026-11-15; [results](e40-results.md) written up and website article prepared in source.** The original plan below is preserved; execution deviations are listed in the results. Generation improved, but verified coding throughput did not improve clearly. Deployment is not established.

## Question and motivation

On our hardware, does caching MoE experts in VRAM improve end-to-end coding throughput without reducing correctness or increasing memory failures?

A Threads screenshot claims an RTX 3060 Ti improved from 30.2 to 54.3 tokens/s on an unspecified “Qwen3 35B” through one expert-cache setting. That is a 79.8% increase, but the exact benchmark, model, quantization and command are unverified. It is motivation, not evidence or a target we expect to reproduce. Testing on different hardware is an independent evaluation, not replication of that claim.

Technique: controlled paired ablation of GPU expert caching for mixture-of-experts inference. Public implementation context: [llama.cpp expert-cache RFC](https://github.com/ggml-org/llama.cpp/discussions/24528). Availability and flags must be checked against the pinned implementation before execution; do not assume a universal GUI toggle.

Local motivation is stronger than the screenshot: [E39](e39-router-design.md) recorded `ExpertCache::fill_slot_queued: out of memory` failures and context-dependent decode speed. E39 used Edge0's inference stack; its cache is not assumed equivalent to llama.cpp's. Historical E39 numbers are context, not a matched cache-off baseline.

## Scope and prerequisites

- First use one available MoE model supported by the selected backend. Prefer an existing Qwen MoE GGUF if compatible; inventory exact local weights before selecting it. Do not substitute a dense model to test expert caching.
- Record GPU/VRAM, CPU, RAM, OS, driver, backend repository and commit, build flags, model hash/quantization, and full launch/request commands.
- Verify that cache-off actually disables expert caching and cache-on actually uses it, from implementation and runtime logs. Unsupported controls mean this comparison is unavailable, not a zero gain.
- Freeze model, prompts, scoring, launch configuration, cache budgets and run order in a run manifest before confirmatory measurement. Select feasible cache budgets in a separate pilot, with pilot results excluded from the headline.
- Use the same backend build for off/on. If that is impossible, label a backend/build comparison separately; it cannot isolate the cache effect.

## Arms

| Arm | Expert cache | Purpose |
|---|---|---|
| A | Explicitly off | Matched baseline |
| B | On, conservative fixed budget | Main paired comparison |
| C | On, larger fixed budget with documented memory headroom | Exploratory capacity/stability tradeoff |

Hold weights, quantization, KV type, context capacity, thread count, GPU offload placement, sampling, batch sizes and output limits fixed. Record unavoidable placement changes. Keep speculative decoding off in the primary comparison. If tested later, use a separate cache off/on × speculation off/on factorial, with the same draft configuration; do not attribute its gain to caching.

Expert caching, prompt-prefix reuse and KV caching are different mechanisms. Disable prompt-prefix reuse for the primary timing comparison while keeping KV configuration constant. Record any cache profiling/training prompts; they must not include confirmatory tasks.

## Measurement plan

1. **Pilot and A/A check:** repeat A to estimate timing variation and validate timing/log collection. Check cache residency/hits when exposed, available memory and errors. Freeze budgets and practical gain threshold after the pilot but before confirmatory trials.
2. **Timing:** freeze ten representative prompts at each of approximately 1k, 8k and 16k actual input tokens, within the model's supported capacity. Run three paired repeats per prompt/arm, counterbalancing arm order. Report actual token counts, early EOS and output length; never force equal output lengths in correctness tasks. Keep a separate fixed-length decode microbenchmark if supported.
3. **Cold and warm:** separately report first request after a server restart and subsequent requests. Document expert-cache reset/warmup behavior and OS file-cache state. Server restart alone does not imply cold filesystem cache. Use identical disjoint warmup prompts for warm comparisons, including warmup cost separately.
4. **Useful work:** reuse the ten E39 harder fixtures with their independent tests, five paired runs each for A/B (100 trials). Fresh isolated task workspaces, identical prompts, loop budgets and deadlines. These are known synthetic fixtures, not new held-out evidence. Retain failed, timed-out and OOM trials in denominators and elapsed cost.
5. **Stability:** repeat A/B under recorded normal desktop load for an equal fixed 30-minute window per arm, counterbalanced over two sessions. Observe memory pressure; do not deliberately exhaust the user's RAM. Log any stop/restart and count recovery time. Stop an arm on repeated OOM/crash (two consecutive failures), retaining its incomplete exposure and failures rather than reporting it as a completed soak.

Primary outcome: **test-passing coding tasks per elapsed hour**, including failures and recovery overhead. Also report pass count/rate, median and p95 task latency, time to first token, prompt-processing and decode tokens/s separately, peak VRAM, minimum free RAM, cache hit/residency metrics when available, and OOM/HTTP/crash counts. Report loading/warmup costs separately and show a startup-inclusive throughput view.

Pair observations by fixture/prompt and repeat. Report paired differences and uncertainty, clustering by task rather than treating repeated runs as independent tasks. Ten fixtures give limited generalization; small pass-rate differences are inconclusive. Do not claim unchanged quality merely because a significance test fails. Inspect every A-pass/B-fail discordance and rerun paired cases to distinguish instability from reproducible regressions.

## Decision and deliverables

Select B only if its useful-work gain exceeds the frozen pilot-informed practical threshold, uncertainty supports a gain, and no reproducible correctness regression or additional memory-failure pattern appears. Otherwise retain A or mark the result inconclusive. Fast decode alone is not a win. C is exploratory and requires a new confirmation before selection.

Save a manifest, exact commands, raw per-request/task JSONL, model outputs, independent test outcomes and memory/error traces under a dedicated E40 results directory. Write `e40-results.md` after measurement, including negative results and limitations. Do not change E39 router thresholds or production serving defaults from an exploratory timing result.

Open before execution: exact model/backend, supported cache controls, available VRAM/RAM, pilot-informed budgets and threshold, frozen prompts and GPU scheduling slot. No E40 results exist yet.
