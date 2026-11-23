# E42: Invergent's Surogate engine versus stock llama.cpp on a 16 GB card

Final analysis, 2026-11-23. Primary collection: November 20–21; supplementary short repeat: November 22. Publication is authorized by the user's November 23 instruction. This report supersedes pending-analysis wording in earlier operational records; the frozen protocol and original results remain unchanged.

Invergent's Surogate engine delivered **0.7801 times stock llama.cpp's correct items per hour (95% paired item-bootstrap interval 0.7772–0.7830)** on the first 4,520 common items. A reversed-order, 30-minute-per-arm repeat returned 0.7805 (0.7754–0.7855). Accuracy stayed within the frozen two-percentage-point margin. This supports keeping llama.cpp as the default for this particular configuration; it does not establish a general engine ranking.

## Design and pre-registered outcome

One RTX 5060 Ti (16 GB), WSL2 Ubuntu 24.04, kernel 6.6.87.2-microsoft-standard-WSL2; VM configured for 12 GB RAM, 8 GB swap and 10 processors. Stock llama.cpp b11753 / d8d92973c used its Linux CUDA 13.4 release. Invergent's Surogate engine was 1.5.15+cu130. Both received the same Qwen3.5-9B Q4_K_M GGUF on WSL ext4, at configured context 32,768, concurrency one, temperature zero and thinking disabled. Invergent's Surogate engine automatically used an internal cached `.sinfer` representation; this was not a manually substituted checkpoint.

Source GGUF SHA-256: `03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8`; internal cache: `b2c58f801cc0b0fa4e7bd27353707b42f073d37c1b251293a80eab706aa1e35c`; ordered 30,000-item synthetic E26 pool: `831188c92bc126cca2f1c477fedd2af2ced4590295d1a31177e9ecf4a6be2bcf`.

The frozen primary design dispatches for two hours per arm, llama.cpp first. Correct/h is correct answers divided by elapsed wall time to finish the first K items both arms completed, multiplied by 3,600. It includes request overhead and gaps. It is not decoded tokens per second. The last in-flight request may finish after dispatch closes. A total 300-second deadline applies; length finishes count as wrong. The client uses one persistent connection and checks usage, finish reasons and reasoning parity.

The paired bootstrap uses 10,000 draws, seed zero, holding each arm's wall time per item fixed. Reported triplets are the bootstrap median and 2.5th/97.5th percentiles, as in the frozen scorer. These intervals cover item sampling only, not run-to-run variance, timing uncertainty or VM state.

## Primary outcome

| First 4,520 common items | Stock llama.cpp | Invergent's Surogate engine |
|---|---:|---:|
| Correct/h | 2,414.8 | 1,883.8 |
| Accuracy | 83.19% | 83.36% |
| Wall time for common prefix | 5,605.4 s | 7,200.7 s |

The correct/h ratio was 0.7801 (0.7772–0.7830): about 22% lower for Invergent's Surogate engine. The paired accuracy gap, Invergent's Surogate engine minus llama.cpp, was +0.177 percentage points (−0.1327 to +0.4867). This supports the specified accuracy margin on these tasks; it does not prove identical outputs or general equivalence.

| Item type | Common n | llama.cpp accuracy | Invergent's Surogate engine accuracy | Correct/h ratio, 95% interval | Accuracy gap in points, 95% interval |
|---|---:|---:|---:|---|---|
| Extraction | 1,501 | 81.01% | 81.95% | 0.7874 (0.7823–0.7932) | +0.9327 (+0.3997 to +1.5323) |
| Intent | 1,504 | 68.42% | 68.02% | 0.7740 (0.7657–0.7823) | −0.3989 (−1.1303 to +0.3324) |
| Triage | 1,515 | 100% | 100% | 0.7785 (0.7785–0.7785) | 0 (0–0) |

Type analyses are secondary, without multiplicity correction. The triage interval collapses because every observed answer was correct and timing is held fixed; it is not evidence of zero timing uncertainty.

## Full windows, failures and resources

| Full primary window | Stock llama.cpp | Invergent's Surogate engine |
|---|---:|---:|
| Rows / correct | 5,800 / 4,849 | 4,520 / 3,768 |
| Sidecar elapsed time | 7,200.45 s | 7,200.67 s |
| Full-window correct/h (different item sets) | 2,424.3 | 1,883.8 |
| Errors / reasoning leakage / length finishes | 0 / 0 / 0 | 0 / 0 / 0 |
| Empty replies / 300 s cap hits | 0 / 0 | 0 / 0 |
| Median / p95 / max item latency | 1.420 / 2.286 / 2.6 s | 1.701 / 3.210 / 3.6 s |
| Sampled peak VRAM | 6,785 MiB | 7,139 MiB |
| Minimum available WSL RAM | 2,369 MiB | 9,207 MiB |
| Peak used swap | 187 MiB | 0 MiB |

Resources were sampled every 60 seconds and can miss transient peaks. RAM is available memory inside the capped WSL VM, not Windows host RAM. Full-window correct/h is descriptive; the pre-registered comparison uses the common prefix.

## Hypotheses and H1 review

| Frozen hypothesis | Disposition | Evidence |
|---|---|---|
| H1: accepts the pinned file at configured 32K, under 15.5 GiB VRAM, without offload/OOM/spill | Not refuted within observation limits | 7,139 MiB sampled peak against 15,872 MiB gate; zero sampled swap; private log review below |
| H2: at least 1.2 times correct/h | Refuted | 0.7801 (0.7772–0.7830) |
| H3: at least 1.5 times median decode tokens/s | Refuted on secondary probes | 39.77 / 67.75 = 0.587 |
| H4: overall paired accuracy gap within two points | Supported on this pool | +0.177 (−0.1327 to +0.4867) points |
| H5: median TTFT ratio below two | Supported on secondary probes | 0.296 / 0.335 s = 0.884 |

The frozen scorer deliberately leaves H1 null; this is a manual assessment of archived evidence, not a new model run. The recorded server-log review found configured capacity 32,768 tokens, 512/512 KV pages, 5.9-second load, one sequence, no OOM/offload/error/warning lines and `preempted=0`. All 120 primary resource samples for Invergent's Surogate engine had zero used swap, and available WSL RAM never fell below 9,207 MiB. These observations do not refute H1. They do not prove absence of every transient spill or host-side pressure, and the short inputs never exercised a full 32K input. Raw server logs remain private; public readers cannot independently repeat this log review from the released package.

H3 and H5 use the fixed, previously visible 20-prompt Stage A cold-process streaming probes, not new primary-window probes. TTFT p50/p95 was 0.335/2.183 s for llama.cpp and 0.296/3.087 s for Invergent's Surogate engine. H5 uses p50; the p95 was worse. Short outputs make the decode estimates noisy. No separate probe uncertainty interval was specified or generated by the frozen scorer.

## Supplementary reversed-order repeat

After primary scoring, the user authorized 0.5 hours per arm, tagged `rep1`, with Invergent's Surogate engine first and llama.cpp second in one uninterrupted WSL invocation. It used the frozen model, pool, settings and launchers. This changes duration and order and is a deviation check, not a replacement primary window. The first 1,132 items overlap the primary prefix; this is a new execution, not an independent task sample.

| Repeat | Stock llama.cpp | Invergent's Surogate engine |
|---|---:|---:|
| Full rows / correct | 1,457 / 1,209 | 1,132 / 935 |
| Common-prefix correct/h | 2,391.9 | 1,866.8 |
| Common-prefix accuracy | 82.86% | 82.60% |
| Median / p95 item latency | 1.384 / 2.234 s | 1.654 / 3.105 s |
| Errors / reasoning leakage / length finishes | 0 / 0 / 0 | 0 / 0 / 0 |
| Sampled peak VRAM | 7,122 MiB | 7,106 MiB |
| Minimum available WSL RAM / peak swap | 2,356 / 30 MiB | 9,228 / 0 MiB |

The ratio was 0.7805 (0.7754–0.7855), with an accuracy gap of −0.265 points (−0.7951 to +0.2650). The similar ratio after reversing order and retaining process continuity reduces concern about an order-specific result. Two executions cannot estimate run-to-run variance reliably; no pooling is performed.

## Deviations, uncertainty and interpretation

1. Primary snapshots recorded different boot-time epochs, 14,898 seconds apart. The original same-VM condition is therefore unverified and was recorded as a protocol deviation. In the uninterrupted repeat, `/proc/stat` btime itself drifted 315 seconds. A differing btime is consequently not conclusive proof of a reboot. The repeat neither reconstructs primary continuity nor explains that larger discrepancy.
2. Both primary arms began with zero used swap, but memory states diverged. llama.cpp reached 187 MiB swap and 2,369 MiB available VM RAM; archived logs showed prompt-cache evictions. Its pressure appeared again within the short repeat. The faster arm experienced pressure, but that does not establish the direction or size of a memory-state effect. The comparison was not memory-matched and no causal explanation for the latency gap was tested.
3. Engine feature parity is uncontrolled: prompt caches, reset behavior, internal representations, flash attention, KV defaults, tokenization/templates and sampler paths may differ. This compares pinned serving configurations, not isolated kernels.
4. Stage A pilot labels and probe timings were visible before freeze; the first 20 tasks overlap the primary. Original Stage A VM restart evidence was retrospective. The Linux CUDA archive was 13.4; the installed Invergent's Surogate engine was 1.5.15 rather than the initial candidate 1.4.0. Original E26 Windows flag equivalence was not independently reconstructed. Harness/pool reads used the shared mount; model/cache storage used ext4.
5. The primary scorer ran unmodified on CPU. Its draft-report destination was redirected by a wrapper to preserve the then-applicable results-only write boundary. The generated draft rounds the ratio interval to two decimals; this report uses `score.json`'s four-decimal values. A separate additive scorer handled the short tagged repeat because the frozen scorer correctly rejects non-primary windows. No frozen preparation file or original result was changed.
6. One card, one model/quant, one synthetic pool, concurrency one and WSL2. There is no basis for generalizing to bare metal, other hardware, quants, models, concurrency or Invergent's published RTX 5090/H100/DGX Spark benchmark conditions. No claim of being the first measurement is made. No native-Windows E26 result is reused as an engine comparison.

## Decision and evidence availability

E42 is complete for its narrow question. Keep stock llama.cpp as the default for this 9B/Q4_K_M/concurrency-one setup; Invergent's Surogate engine does not earn a mandatory permanent arm on a speed-benefit rationale from this study. A new version, different workload or separately frozen higher-concurrency study could justify revisiting it. A full two-hour repeat is optional future work, not a prerequisite for closing this report. The cause of the latency gap and the primary boot-identity discrepancy remain unresolved.

The [public E42 evidence package](https://github.com/icporcincula/porsync-research/tree/main/docs/small-evals/e42-results-2026-11-23) contains this report, curated configuration, saved summaries, transformed per-item scoring/timing observations, numerical resource series, probe measurements, original window sidecars and a portable offline analyzer. It permits recomputation of the reported aggregates and bootstrap intervals from saved correctness labels; it cannot independently rejudge answers or reproduce inference without withheld inputs.

Prompts, reference answers, full model replies, raw logs/telemetry, operational environment files, private paths/implementation, weights, binaries and cache files are excluded. Transformed numeric resource series omit absolute timestamps. Original-source and released-file hashes and transformation notes distinguish the released observations from their sources. No blanket rights to upstream assets are granted.

Credit: Invergent's Surogate engine authors, the llama.cpp contributors and the Qwen authors. This is an independent configuration-specific evaluation, not a replication of Invergent's published benchmarks. E39's outstanding follow-ups remain open; E42 does not change its routing defaults.
