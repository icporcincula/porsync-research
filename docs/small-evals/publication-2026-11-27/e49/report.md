> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E49 results (private)

Date: 2026-11-24. Completed under the frozen protocol (private source reference withheld) and prompt 18 run instructions (private source reference withheld). Freeze commit: `641198d8`. No push, publication, site change, promotion or router change. Raw evidence remains git-ignored under `tmp/e49/`. This report is the explicitly selected private artifact; the public evidence update is deferred by the run instruction prohibiting publication and access to the public checkout.

## Observed result

All six arm-blocks completed in the frozen A1, B1, C1, C2, B2, A2 order, with 24 saved rows each. A and B each scored 48/48. B/A correct-per-hour ratio was 1.3035432716638766, with item-clustered bootstrap 95% interval [1.1932587604835314, 1.4325559228353686]. The saved reading rule gives `H1=true`, `H2=true`, and `promising_again=true`. This is only the frozen development reading, not equivalence or a general speed claim. C is a separate usability result: 2/48 correct, 4.17% accuracy, 133.23 correct/hour; it is never pooled with A or B.

Credit: Thinking Machines Lab for Inkling 2 Mini; Niko1221 and contributors for Niko1221's Strata engine; and the llama.cpp authors.

## Execution and pins

- Local serving only; no paid API or frontier call. One GPU job at a time; no retry, redraw, tuning or setting changes.
- NVIDIA RTX 5060 Ti, driver 610.88; context 8192, one slot, completion cap 4096, temperature/top-p 1.0, request timeout 300 s, arm-block budget 2700 s; one unscored warmup per session.
- A: llama.cpp E44 pin `b50-8d60873`, UD-IQ3_XXS, no drafter, default thinking on. B: Niko1221's Strata engine 0.1.66 (v0.2.20), build `2e87c08db18a`, SQ-15 revision `04996a1e...`, DSpark, locally adapted serving policy (effort 0.9, thinking on, no forced opener, `answer_room=false`). C: same engine/pack with pristine release policy, effort none and forced opener.
- Model SHA-256 verified by each runner: IQ3 `fd9ccedae17c1bb89744612fbb46730b5275f2a342133d0419776bd1ae311657`; SQ-15 `2ea32eed533afba257e2cbee7b073dc2c3da80fe55d1d2d794779b5498e30737`.
- Executable SHA-256 recorded in every launch: llama.cpp `27bdbbefdd69f5a269648f91f1e74587cc217bf7d0ccf92af3d625400394dda0`; Niko1221's Strata engine `0fbe343590148ac8a6e0c5f4da79eeef68e08888c3cc97c70a0f79457d6a7475`.
- Before the first block, `tmp/e49/` contained only fixtures, protocol and freeze-hashes. Required tests passed (9) before launch. Freeze and prompt were already committed. Other working-tree changes were preserved.

| Launch order | Arm/block | Available RAM at manual launch check (GiB) | GPU used (MiB) | Stop reason | Saved rows | Owned server exited |
|---|---|---:|---:|---|---:|---|
| 1 | A1 `llama-iq3-b1` | 11.233 | 321 | `completed` | 24 | True |
| 2 | B1 `strata-sq15-thinking-b1` | 13.539 | 320 | `completed` | 24 | True |
| 3 | C1 `strata-sq15-pristine-b1` | 13.585 | 320 | `completed` | 24 | True |
| 4 | C2 `strata-sq15-pristine-b2` | 13.564 | 320 | `completed` | 24 | True |
| 5 | B2 `strata-sq15-thinking-b2` | 13.551 | 320 | `completed` | 24 | True |
| 6 | A2 `llama-iq3-b2` | 13.407 | 320 | `completed` | 24 | True |

All launch checks had GPU utilization 0%, under 1500 MiB used, no llama-server, strata-inkling, Ollama or edge0-infer process, and over 4 GiB available RAM. Each preceding shutdown record was read and the GPU checked before the next launch. All six runner error logs are empty.

## Per-arm metrics

Correct/hour = correct / summed request seconds x 3600, including failures and excluding model hashing, load, warmup and shutdown. Wilson intervals are descriptive at the sample level; repeats are not independent items. Token percentiles use the frozen summarizer.

### Arm A: `llama-iq3`

| n | Correct | Accuracy | Wilson 95% | Request seconds | Correct/hour | Length stops | Errors | Median completion tokens | p90 completion tokens |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 48 | 48 | 100.00% | 92.59% to 100.00% | 839.990201900 | 205.716685277 | 0 | 0 | 817.5 | 1437 |

Request time: mean 17.500 s, median 16.318 s, range 7.215 to 42.880 s.

### Arm B: `strata-sq15-thinking`

| n | Correct | Accuracy | Wilson 95% | Request seconds | Correct/hour | Length stops | Errors | Median completion tokens | p90 completion tokens |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 48 | 48 | 100.00% | 92.59% to 100.00% | 644.389964000 | 268.160600962 | 0 | 0 | 644.5 | 1046 |

Request time: mean 13.425 s, median 11.503 s, range 5.216 to 40.531 s.

### Arm C: `strata-sq15-pristine`

| n | Correct | Accuracy | Wilson 95% | Request seconds | Correct/hour | Length stops | Errors | Median completion tokens | p90 completion tokens |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 48 | 2 | 4.17% | 1.15% to 13.98% | 54.041749700 | 133.230327293 | 0 | 0 | 33.5 | 59 |

Request time: mean 1.126 s, median 1.149 s, range 0.545 to 2.205 s.

## Per-family accuracy

| Family | A correct/n (accuracy) | B correct/n (accuracy) | C correct/n (accuracy), separate |
|---|---|---|---|
| aggregate | 8/8 (100.00%) | 8/8 (100.00%) | 2/8 (25.00%) |
| dedup | 8/8 (100.00%) | 8/8 (100.00%) | 0/8 (0.00%) |
| intervals | 8/8 (100.00%) | 8/8 (100.00%) | 0/8 (0.00%) |
| inventory | 8/8 (100.00%) | 8/8 (100.00%) | 0/8 (0.00%) |
| machine | 8/8 (100.00%) | 8/8 (100.00%) | 0/8 (0.00%) |
| schedule | 8/8 (100.00%) | 8/8 (100.00%) | 0/8 (0.00%) |

## Per-block / repeat accuracy

| Arm/block | Correct/n | Accuracy | Wilson 95% | Request seconds |
|---|---:|---:|---|---:|
| A1 | 24/24 | 100.00% | 86.20% to 100.00% | 406.383541400 |
| B1 | 24/24 | 100.00% | 86.20% to 100.00% | 334.848912600 |
| C1 | 1/24 | 4.17% | 0.74% to 20.24% | 27.309137000 |
| C2 | 1/24 | 4.17% | 0.74% to 20.24% | 26.732612700 |
| B2 | 24/24 | 100.00% | 86.20% to 100.00% | 309.541051400 |
| A2 | 24/24 | 100.00% | 86.20% to 100.00% | 433.606660500 |

## B versus A: saved comparison verbatim

The following block is copied without numerical transformation from `tmp/e49/summary.json`:

```json
{
  "speed_ratio": 1.3035432716638766,
  "accuracy_diff": 0.0,
  "bootstrap": {
    "ratio_ci95": [
      1.1932587604835314,
      1.4325559228353686
    ],
    "accuracy_diff_ci95": [
      0.0,
      0.0
    ],
    "skipped_resamples": 0
  },
  "H1": true,
  "H2": true,
  "ratio_lower_bound_above_1": true,
  "promising_again": true
}
```

Bootstrap: 10,000 item-cluster resamples, seed 4949, keeping both repeats together. Accuracy difference is in proportions (0.0 = 0 percentage points). H1 uses the point speed ratio >=1.25; H2 uses point accuracy difference >=-0.10; the speed lower bootstrap bound must also exceed 1.0 for `promising_again`. The zero-width accuracy-difference interval reflects these observed all-correct samples, not population certainty.

## Descriptive paired table by item

Each cell reports correct/2 and summed request seconds for both repeats. C remains separate.

| Item | A | B | C (usability only) |
|---|---|---|---|
| aggregate-0 | 2/2; 33.850 s | 2/2; 15.455 s | 0/2; 2.005 s |
| aggregate-1 | 2/2; 20.700 s | 2/2; 16.269 s | 0/2; 1.997 s |
| aggregate-2 | 2/2; 23.355 s | 2/2; 20.851 s | 2/2; 2.031 s |
| aggregate-3 | 2/2; 36.612 s | 2/2; 15.363 s | 0/2; 2.060 s |
| dedup-0 | 2/2; 56.271 s | 2/2; 61.615 s | 0/2; 4.204 s |
| dedup-1 | 2/2; 63.236 s | 2/2; 46.356 s | 0/2; 3.162 s |
| dedup-2 | 2/2; 65.185 s | 2/2; 59.232 s | 0/2; 3.410 s |
| dedup-3 | 2/2; 48.939 s | 2/2; 34.736 s | 0/2; 2.749 s |
| intervals-0 | 2/2; 43.927 s | 2/2; 35.622 s | 0/2; 3.173 s |
| intervals-1 | 2/2; 44.898 s | 2/2; 40.120 s | 0/2; 2.880 s |
| intervals-2 | 2/2; 37.880 s | 2/2; 27.360 s | 0/2; 2.524 s |
| intervals-3 | 2/2; 32.278 s | 2/2; 27.819 s | 0/2; 2.656 s |
| inventory-0 | 2/2; 22.435 s | 2/2; 16.313 s | 0/2; 1.244 s |
| inventory-1 | 2/2; 17.145 s | 2/2; 16.289 s | 0/2; 1.191 s |
| inventory-2 | 2/2; 22.832 s | 2/2; 15.365 s | 0/2; 1.231 s |
| inventory-3 | 2/2; 15.445 s | 2/2; 17.426 s | 0/2; 1.108 s |
| machine-0 | 2/2; 17.201 s | 2/2; 11.251 s | 0/2; 1.162 s |
| machine-1 | 2/2; 17.203 s | 2/2; 11.792 s | 0/2; 1.230 s |
| machine-2 | 2/2; 21.134 s | 2/2; 13.055 s | 0/2; 1.219 s |
| machine-3 | 2/2; 16.121 s | 2/2; 13.779 s | 0/2; 1.153 s |
| schedule-0 | 2/2; 43.383 s | 2/2; 33.236 s | 0/2; 2.914 s |
| schedule-1 | 2/2; 43.217 s | 2/2; 29.225 s | 0/2; 2.972 s |
| schedule-2 | 2/2; 48.388 s | 2/2; 34.003 s | 0/2; 2.703 s |
| schedule-3 | 2/2; 48.354 s | 2/2; 31.858 s | 0/2; 3.060 s |

## Resource extrema (observed samples)

From each `*-resources.jsonl` (approximately every 2 s). Ranges are sampled extrema, not guaranteed instantaneous peaks. GiB uses 2^30 bytes. No resource-sampling errors.

| Block | Samples | GPU used MiB min-max | GPU free MiB min-max | Utilization % min-max | Temperature C min-max | Power W min-max | RAM available GiB min-max | Swap used GiB min-max |
|---|---:|---|---|---|---|---|---|---|
| A1 | 203 | 322.00-12933.00 | 3118.00-15729.00 | 0.00-98.00 | 42.00-68.00 | 7.14-123.43 | 0.586182-11.977234 | 0.670071-1.161072 |
| B1 | 169 | 322.00-15035.00 | 1016.00-15729.00 | 0.00-95.00 | 44.00-66.00 | 8.41-123.63 | 10.107899-13.539593 | 1.053223-1.097519 |
| C1 | 20 | 324.00-15035.00 | 1016.00-15727.00 | 0.00-99.00 | 45.00-62.00 | 8.10-118.94 | 10.251762-13.601608 | 1.092632-1.092632 |
| C2 | 20 | 322.00-15035.00 | 1016.00-15729.00 | 0.00-99.00 | 44.00-61.00 | 8.11-116.26 | 10.244480-13.598614 | 1.092625-1.092625 |
| B2 | 159 | 322.00-15035.00 | 1016.00-15729.00 | 0.00-99.00 | 43.00-66.00 | 8.32-124.56 | 9.261875-13.584614 | 1.090717-1.100597 |
| A2 | 214 | 324.00-12933.00 | 3118.00-15727.00 | 0.00-96.00 | 46.00-69.00 | 8.45-121.98 | 0.558201-13.362343 | 0.856537-1.173019 |

Observed anomaly: available RAM dipped below 4 GiB during the A runs (sampled minima 0.586182 GiB in A1 and 0.558201 GiB in A2). The hard stop is specifically below 4 GiB **at a launch check**; all launch checks passed, so no block was interrupted or retried. These pressure observations remain a limitation; no causal effect on timing is established.

## SQ-15 expert and KV placement

Exact placement lines from each Niko1221's Strata engine log follow. All four sessions used hybrid expert placement and mapped host global KV.

`tmp/e49/strata-sq15-thinking-b1-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.22s), experts=2773 VRAM / 299 host (6.63s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.56 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

`tmp/e49/strata-sq15-pristine-b1-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.24s), experts=2773 VRAM / 299 host (6.62s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.57 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

`tmp/e49/strata-sq15-pristine-b2-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.24s), experts=2773 VRAM / 299 host (6.55s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.57 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

`tmp/e49/strata-sq15-thinking-b2-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.24s), experts=2773 VRAM / 299 host (7.66s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.56 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

## Anomalies and hypothesis limits

- Observed: all 144 scored requests ended with `finish_reason=stop`; no length stops or recorded request errors, no budget/error stops, and no runner error log content. C1 had one JSON parse error, counted incorrect; parse errors are distinct from the summary's request-error metric. All remaining incorrect C answers failed exact equality. No observed startup or shutdown failure.
- Observed usability result: C answered in 54.04174970005988 summed request seconds (mean 1.126 s/request), with only 2 correct answers, both in regional aggregation (one per repeat). Its shorter requests did not yield higher correct/hour than A or B. C is not pooled into the matched-thinking comparison.
- Hypothesis H3: the raw request times were shorter and accuracy lower for C on this pool. This is descriptive evidence on release-policy usability, not an isolated causal test of reasoning policy. There is no saved H3 boolean or H3 bootstrap in the frozen summary, and none is invented here.
- Standing limits: a B-versus-A gap is a whole-stack difference. Quantization, sampler implementations (including serving candidate-width limits), DSpark drafter availability and prompt caching differ. B uses a locally adapted serving policy. Engine, weights and installed release were unmodified.
- Reasoning-channel text is discarded by the unchanged release parser and was not audited. Completion-token counts are the only reasoning-effort evidence; they do not prove a reasoning mechanism.
- Only 24 synthetic items with two repeats (48 samples per arm), six structured-task families, and one development run on this machine. Both thinking arms saturated this pool at 48/48; longer inputs and more steps did not establish calibrated difficulty. No equivalence, general engine or quant win, coding/tool/long-context result, or claim beyond these samples.
- E47 supplied the hypothesis only; no E47 evidence is pooled. No promotion, router change, publication or site update follows from this result.

## Final verification

- `python -m pytest scripts/test_e49.py -q`: 9 passed before launch and 9 passed after all six blocks. Existing pytest plugin deprecation warnings were emitted (asyncio fixture loop scope and anyio CallSpec2); no test failed.
- GPU after A2: 320 MiB used, 0% utilization, no model-serving process. All six recorded owned server PIDs and all six runner PIDs were absent; all shutdown records say `owned_server_exited=true`.
- The three required protected hashes and the protocol hash match preflight and final checks. Frozen script hashes match `tmp/e49/freeze-hashes.json` (and protocol pins). No protected file or attempt marker was edited.

| File | Verified SHA-256 |
|---|---|
| `tmp/e45/log.jsonl` | `2d40ccd3e22a0c1ffa735854726a49e0562e86fbbf91431939ce3211d47c437d` |
| `tmp/e45v2/cohort-seal.json` | `157b16a24aa6074f134f35a3ef5d063a1b12792d96ff40b4fb372d037266f012` |
| `tmp/e49/fixtures.json` | `efabe515e8f146825e023b3ed83b7b9142bf327db621b3ad5a23d0af9245ad7e` |
| `tmp/e49/protocol.json` | `b20a5811362473b10cf1513c52cd06ec2768445b9d7279e272c381778e6c93ee` |
| `scripts/e49_pool.py` | `b86b32887064d82883f388714f83e043f0fde68adef65cc5aa1b112503e7f9ef` |
| `scripts/e49_pilot.py` | `e568186b0fa0308dc361172aa16e519f5f66a37fdb902ef514c4068ba48dc234` |
| `scripts/e49_server_run.py` | `e73c31da6254554bf93b3afd6209fda50b3534e3d34860e8fd6ad52ddd2f84e1` |
| `scripts/e49_thinking_server.py` | `789a46306d80085e58b527a20b451820cef1fefed9a28173a5ea07ea91b1c937` |

Commit scope: this report only; prompt 18 was already committed in `641198d8`. No push. Raw outputs remain ignored. Unrelated root documentation and nested-repository changes were left alone under the explicit-path run instruction.
