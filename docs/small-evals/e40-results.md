> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E40 results — expert caching sped up generation, not verified coding throughput

Completed 2026-11-15. Website article prepared in source; deployment not established. [Plan](e40-expert-cache.md), implementation handoff (not included in this public release), [archived data and scripts](e40-data/).

## Verdict

On Qwen3-30B-A3B Q4_K_M and an RTX 5060 Ti 16 GB, a 6,000 MiB expert cache increased warm generation speed from about 30–33 to 41–50 tokens/s. It did **not demonstrate higher verified coding throughput**: cache-off passed 9/50 attempts, cache-on 8/50. Dividing passes by summed task duration gives 12.93 versus 12.35 passes/hour (ratio 0.96). These rates include failed task time but exclude server startup and between-round overhead; they are not the planned startup-inclusive throughput metric.

A 9,000 MiB cache reached 66–82 warm generation tokens/s in a separate timing arm. That arm never ran the coding tasks. A 12,000 MiB configuration exceeded the available VRAM budget and is a configuration failure, not a clean estimate of caching's effect.

No serving defaults or E39 router thresholds change from this evidence. E40 used Qwen and llama.cpp, not Edge0-120B or its inference stack.

## Setup and execution

The [frozen manifest](e40-data/trials/manifest.json) records llama.cpp commit `6d3568e31d4e4b1e4db4acb8f6ceaad0084932f3`, Qwen3-30B-A3B Q4_K_M SHA256 `9F1A24700A339B09C06009B729B5C809E0B64C213B8AF5B711B3DBDFD0C5BA48`, RTX 5060 Ti (16,311 MiB), and driver 610.88. Local server logs identify a Ryzen 5 7500F and 32 GB host RAM; run metadata records Windows 11 build 26200 and Python 3.12.7.

Common arguments: `-ngl 99 -cmoe -fa on -c 32768 -np 1 -lv 4`; speculative decoding off. A omits `--moe-cache-mib`; B adds 6000; C adds 12000; exploratory timing-only D adds 9000. Expert caching keeps some expert weights in GPU memory; it is separate from reusing prompt prefixes. Task trials and soak retained default prompt caching. Timing disabled it both at launch and per request.

The ten E39 harder fixtures h01–h10 were reused, with independent tests and fresh attempts: five rounds per arm, 30 maximum turns and a 30,000-token live-context budget. A/B order alternated each round; C followed afterward. The server restarted per arm-round. Sampling was unseeded. These are ten known synthetic maintenance tasks, not 50 independent projects or new held-out evidence.

## Coding trials

| Arm | Cache MiB | Passed / attempts | Sum of task seconds | Passes / task-hour | Median task seconds |
|---|---:|---:|---:|---:|---:|
| A | Off | 9/50 | 2,506.5 | 12.93 | 39.6 |
| B | 6,000 | 8/50 | 2,331.5 | 12.35 | 43.1 |
| C, configuration failure | 12,000 | 10/50 | 6,654.6 | 5.41 | 136.4 |

All 150 attempts remain in the table, including failures. C's launch projected 16,105 MiB of device memory against 15,172 MiB free. Its slower attempts cannot establish that a feasible larger cache would hurt throughput.

| Fixture | A passes /5 | B passes /5 | C passes /5 |
|---|---:|---:|---:|
| h01 cursor | 0 | 0 | 0 |
| h02 stock | 2 | 1 | 4 |
| h03 import | 0 | 0 | 0 |
| h04 access | 0 | 3 | 1 |
| h05 retry | 1 | 0 | 0 |
| h06 retention | 0 | 0 | 0 |
| h07 queue | 5 | 4 | 5 |
| h08 config | 0 | 0 | 0 |
| h09 search | 1 | 0 | 0 |
| h10 intervals | 0 | 0 | 0 |

The task-cluster bootstrap gives a 95% interval of **0.00–3.53** for B/A passes per task-hour. Of 5,000 resamples, 4,962 had nonzero A throughput and entered that interval; the undefined ratios were omitted. The exact sign-flip comparison across fixture pass differences gives p=1.0. A passed while B failed in four paired attempts; B alone passed in three. The unclustered exact McNemar calculation also gives p=1.0, but repeated attempts are not independent tasks. This is imprecise evidence, not proof of equal quality.

The handoff's full trace review covered only h04. It attributes that split to divergent sampling trajectories and repeated failing behavior in A; the other disagreements were inspected only by failure reason and divergence point. No comprehensive paired discordance rerun is documented. The data cannot rule out quality changes or isolate why task throughput failed to track decode speed. Time in tools, prompt processing and unsuccessful loops may matter, but no full timing decomposition establishes their contributions here.

## Timing: generation is faster

Ninety requests completed without logged request errors. Each arm/size cell contains five deterministic document slices repeated in two sessions (ten observations, not ten distinct prompts), with reversed arm order in the second session. Temperature 0, seed 1, generation limit 256; every recorded output reached 256 tokens. Summarization quality was not scored.

Targets were approximately 1K, 8K and 16K input tokens. Actual ranges were 797–1,145; 6,777–8,663; and 15,050–16,910. The script derived slices from the then-current local Markdown corpus; exact prompt text/hashes were not archived in the timing rows, so a later changed corpus would not reconstruct identical prompts.

| Arm | Target input | Generation tok/s, first / later | Prefill tok/s, median | Wall seconds, median |
|---|---|---:|---:|---:|
| A | 1K | 31.8 / 33.1 | 321 | 11.1 |
| A | 8K | 31.0 / 32.2 | 437 | 26.9 |
| A | 16K | 30.4 / 30.2 | 428 | 48.3 |
| B | 1K | 64.0 / 49.6 | 422 | 7.5 |
| B | 8K | 49.5 / 47.8 | 518 | 20.7 |
| B | 16K | 48.8 / 41.0 | 496 | 40.8 |
| D | 1K | 77.2 / 82.1 | 549 | 5.1 |
| D | 8K | 74.6 / 76.4 | 670 | 15.6 |
| D | 16K | 70.4 / 65.6 | 640 | 31.0 |

“First” means run 1 at each size (two observations); “later” means runs 2–5 (eight). Only the first 1K request followed a fresh server. The 8K and 16K first requests followed smaller-size requests, so they are **not cold expert-cache measurements**. Server restart does not establish cold filesystem cache either. The first/later columns also use different slices; they do not isolate warming.

Later-request generation was 1.36–1.50x A for B, and 2.17–2.48x for D. Prefill and complete request latency improved too, as the table shows. D's timing gain is not an agent-throughput result. Repetitive pilot prompts produced a larger speedup and are excluded.

## Sustained sessions

Two sessions counterbalanced A,B then B,A. Each arm completed four ten-task rounds per session: 80 attempts per arm. Archived rows give **A 15/80, B 10/80**. Session totals were A 7 and 8; B 6 and 4. This nominal quality gap is not an equivalence result or a confirmed regression.

The log records windows of 33.0 and 30.4 minutes for A, 32.3 and 35.2 for B. They exceed the nominal 30 minutes because a round was allowed to finish. All 16 rounds exited successfully, the server stayed alive, and execution-error counts were zero. The handoff reports no OOM/CUDA errors in the local serve logs; the repeated-failure stop rule never fired. Reported peak VRAM was about 9.2 GB for A and 15.2 GB for B. These short observed sessions do not establish indefinite stability or safety under other desktop loads.

The first soak launch was invalidated by a PowerShell variable-name collision; it was corrected and relaunched. Failed launch time is disclosed rather than folded into the successful sessions.

## Departures from the plan and remaining limits

- Pilot selected 6,000/12,000 MiB budgets; C did not fit at the selected context. D was added for timing only.
- The planned ten distinct prompts and three paired repeats per cell became five slices across two sessions. No separate A/A analysis or frozen practical gain threshold is reported.
- Only timing disabled prompt reuse. The task results measure the operational default with prompt reuse, not its isolated interaction with expert caching.
- The reported task-hour rate omits startup, warmup and orchestration overhead. A complete startup-inclusive metric, p95 task latency, separate TTFT, host-memory minima and cache hit/residency analysis are not supplied here.
- Full build provenance and exact timing prompt hashes are not in the trial manifest. Serve logs and trial transcripts remain at `C:\e40\` rather than in the archive.
- No claim of unchanged correctness, no agent speedup for D, and no replication of the unverified social-media screenshot. No cross-model inference to E39.

## Verification for this write-up

Read the archived manifest, trial CSV, timing JSONL, soak rows/log and execution scripts. Recomputed 9/50, 8/50 and 10/50, task durations, timing token ranges, and soak totals directly. Re-ran the supplied analysis scripts against their original local data paths and obtained the handoff's rates and interval. Inspected local launch logs for the memory projection. No new inference, GPU session or serving change was performed. The [E39 report](e39-results.md) remains interim for routing evidence; this E40 measurement series is complete with the above deviations.

Website validation: the research collection check passed (48 studies), and the initial TypeScript check passed. Production compilation succeeded with webpack, then generated route validation rejected the existing named `tools` export in `app/tools/page.tsx`. That unrelated route was not changed; a successful full production build or deployment is not claimed.
