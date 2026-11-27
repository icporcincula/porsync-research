> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E50 results: calibrated harder pool (private)

Date: 2026-11-24. Status: all six frozen arm-blocks completed; private development result. No push, publication, promotion or router change. The protocol and run instructions remain frozen as a pre-run record.

Observed: mechanical calibration selected L3. On confirmation, A scored 25/48 (52.08%) and B scored 38/48 (79.17%). B/A correct-per-hour was 1.3465498918644159, with item-clustered bootstrap 95% interval [0.9765241667121909, 1.9928803036600016]. H1 and H2 held at their point estimates, but the lower speed-ratio bound did not exceed 1.0: `promising_again=false`. `ceiling_again=false`. This is the frozen reading rule, not evidence for a broader claim.

## Frozen method and preflight

Executed prompt 19 (private source reference withheld) against the frozen protocol (private source reference withheld). Prior protocol/scripts commit: `eff565f1d3e6bde0eefdbb58c1a2dcfde0c941c5`.

- Subscription/local execution only; no paid API or frontier calls.
- Calibration: seed 5001, 36 fixed interleaved items, 12 each at L2/L3/L4, A then B. Only A enters mechanical level selection. Calibration is descriptive and never pooled with confirmation.
- Confirmation: fresh seed 50, L3, 24 items / six families, two fixed-order repeats; A1, B1, B2, A2. All 48 samples per arm completed.
- Context 8,192; completion cap 6,144; temperature/top-p 1.0; one slot; timeout 300 s; per-block budget 4,500 s; one unscored warmup per block; two consecutive request errors would stop a block.
- Primary measure: correct / summed scored-request seconds * 3,600. Load, warmup and shutdown excluded. Errors, timeouts and length finishes fail. Exact final JSON scoring; reasoning excluded.
- Wilson 95% intervals; item-clustered bootstrap with both repeats kept together, 10,000 resamples, seed 5050. H1: B/A correct-per-hour >= 1.25. H2: B minus A accuracy >= -0.10. Promising again additionally requires lower bootstrap speed-ratio bound > 1.0.
- Preflight: only `fixtures.json`, `protocol.json`, `freeze-hashes.json` existed in `tmp/e50/`; 13 tests passed. Protected hashes and all four frozen script hashes matched before launch.
- Each launch check had GPU memory below 1,500 MiB, no llama-server / strata-inkling / ollama / edge0-infer process, and more than 4 GiB available RAM. Checks observed GPU 362, 400, 411, 411, 413, 411 MiB and RAM 12.82, 13.59, 13.59, 13.88, 13.05, 13.30 GiB in run order. One GPU job ran at a time. No unrelated process was stopped.

## Stage 1: observed calibration

| Arm | Level | n | Correct | Accuracy | Request seconds | Correct/hour | Length stops | Errors | Median completion tokens | p90 completion tokens | Max prompt tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A: llama.cpp IQ3_XXS | L2 | 12 | 12 | 100.00% | 534.323 | 80.850 | 0 | 0 | 2006.5 | 3476 | 715 |
| A: llama.cpp IQ3_XXS | L3 | 12 | 8 | 66.67% | 1125.300 | 25.593 | 4 | 0 | 4367.0 | 6144 | 1205 |
| A: llama.cpp IQ3_XXS | L4 | 12 | 3 | 25.00% | 1424.399 | 7.582 | 9 | 0 | 6144.0 | 6144 | 1695 |
| B: SQ-15 / Niko1221's Strata engine | L2 | 12 | 12 | 100.00% | 547.405 | 78.918 | 0 | 0 | 1864.0 | 3396 | 715 |
| B: SQ-15 / Niko1221's Strata engine | L3 | 12 | 10 | 83.33% | 1307.290 | 27.538 | 2 | 0 | 4100.0 | 6144 | 1205 |
| B: SQ-15 / Niko1221's Strata engine | L4 | 12 | 6 | 50.00% | 2126.902 | 10.156 | 6 | 0 | 6110.5 | 6144 | 1695 |

Selection result, verbatim from `tmp/e50/selection.json`:

```json
{
  "status": "selected",
  "level": 3,
  "arm_a_accuracy_by_level": {
    "2": 1.0,
    "3": 0.6666666666666666,
    "4": 0.25
  },
  "utc": "2026-11-24T11:49:31Z"
}
```

## Stage 2: observed confirmation at L3

| Arm | n | Correct | Accuracy | Wilson 95% | Request seconds | Correct/hour | Length stops | Errors | Median completion tokens | p90 completion tokens |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| A: llama.cpp IQ3_XXS | 48 | 25 | 52.08% | [0.383292, 0.655287] | 4756.018 | 18.923 | 23 | 0 | 5944.0 | 6144 |
| B: SQ-15 / Niko1221's Strata engine | 48 | 38 | 79.17% | [0.657411, 0.882697] | 5368.644 | 25.481 | 10 | 0 | 3991.0 | 6144 |

B vs A comparison block, verbatim JSON values and formatting from `summary-conf.json`:

```json
{
  "speed_ratio": 1.3465498918644159,
  "accuracy_diff": 0.27083333333333326,
  "bootstrap": {
    "ratio_ci95": [
      0.9765241667121909,
      1.9928803036600016
    ],
    "accuracy_diff_ci95": [
      0.10416666666666674,
      0.4375
    ],
    "skipped_resamples": 0
  },
  "H1": true,
  "H2": true,
  "ratio_lower_bound_above_1": false,
  "ceiling_again": false,
  "promising_again": false
}
```

Per-family confirmation accuracy (observed; n=8 per arm/family):

| Family | A correct/n | A accuracy | B correct/n | B accuracy |
|---|---:|---:|---:|---:|
| aggregate | 5/8 | 62.50% | 7/8 | 87.50% |
| dedup | 4/8 | 50.00% | 7/8 | 87.50% |
| intervals | 1/8 | 12.50% | 8/8 | 100.00% |
| inventory | 7/8 | 87.50% | 8/8 | 100.00% |
| machine | 8/8 | 100.00% | 8/8 | 100.00% |
| schedule | 0/8 | 0.00% | 0/8 | 0.00% |

Per-block confirmation accuracy (observed):

| Arm | Block | n | Correct | Accuracy | Request seconds |
|---|---:|---:|---:|---:|---:|
| A: llama.cpp IQ3_XXS | 1 | 24 | 11 | 45.83% | 2401.669 |
| A: llama.cpp IQ3_XXS | 2 | 24 | 14 | 58.33% | 2354.349 |
| B: SQ-15 / Niko1221's Strata engine | 1 | 24 | 19 | 79.17% | 2554.039 |
| B: SQ-15 / Niko1221's Strata engine | 2 | 24 | 19 | 79.17% | 2814.605 |

## Block outcomes and resources

| Execution order | Saved tag | Rows | Stop reason | Owned server exited |
|---:|---|---:|---|---|
| 1 | `cal-llama-iq3-b1` | 36 | `completed` | `true` |
| 2 | `cal-strata-sq15-thinking-b1` | 36 | `completed` | `true` |
| 3 | `conf-llama-iq3-b1` | 24 | `completed` | `true` |
| 4 | `conf-strata-sq15-thinking-b1` | 24 | `completed` | `true` |
| 5 | `conf-strata-sq15-thinking-b2` | 24 | `completed` | `true` |
| 6 | `conf-llama-iq3-b2` | 24 | `completed` | `true` |

Resource extrema from the complete two-second `*-resources.jsonl` samples (observed, host-wide; sampled peaks can miss between-sample extrema):

| Saved tag | Samples | Max GPU used MiB | Min GPU free MiB | Max GPU util % | Max temp C | Max power W | Min available RAM GiB | Max swap GiB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cal-llama-iq3-b1` | 1498 | 13036.000 | 3015.000 | 98.000 | 69.000 | 141.980 | 1.029 | 6.146 |
| `cal-strata-sq15-thinking-b1` | 1932 | 15126.000 | 925.000 | 99.000 | 65.000 | 127.360 | 9.705 | 1.324 |
| `conf-llama-iq3-b1` | 1170 | 13024.000 | 3027.000 | 98.000 | 69.000 | 137.490 | 1.515 | 6.297 |
| `conf-strata-sq15-thinking-b1` | 1251 | 15126.000 | 925.000 | 100.000 | 63.000 | 117.940 | 8.935 | 1.323 |
| `conf-strata-sq15-thinking-b2` | 1374 | 15126.000 | 925.000 | 99.000 | 64.000 | 119.200 | 9.514 | 1.313 |
| `conf-llama-iq3-b2` | 1145 | 13024.000 | 3027.000 | 98.000 | 68.000 | 127.460 | 1.271 | 6.052 |

No resource-monitor error rows. Available RAM fell below 4 GiB during all three A blocks (minimum 1.029 GiB overall); all launch checks exceeded 4 GiB. The frozen stop condition is explicitly a launch check; no threshold or setting was changed. Peak swap during A was 6.297 GiB. Resource pressure is an observed run condition; its effect on results was not isolated.

## SQ-15 placement in Niko1221's Strata engine

Exact expert/KV placement lines from each saved engine log:

`tmp/e50/cal-strata-sq15-thinking-b1-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.22s), experts=2773 VRAM / 299 host (6.80s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.57 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

`tmp/e50/conf-strata-sq15-thinking-b1-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (2.71s), experts=2773 VRAM / 299 host (11.12s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.55 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

`tmp/e50/conf-strata-sq15-thinking-b2-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.25s), experts=2773 VRAM / 299 host (17.04s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.55 GiB free VRAM): global KV = 0 VRAM + 8192 mapped host tokens (256.0 MiB host RAM, max_ctx=8192)
```

## Observed anomalies and limits

- All six blocks completed; no launch failure, crash, request error, timeout, budget stop, retry, redraw or hand-edited output. Each runner stderr file is empty. No paid API use.
- Length stops: calibration A 13, B 8; confirmation A 23, B 10 (54/168 scored rows overall). Every incorrect saved row has `finish_reason=length`; all 54 also have a parse-error flag. No incorrect non-length row was observed. This does not establish how uncapped answers would score.
- No recorded prompt-plus-cap context overflow: largest prompt 1,695 tokens across calibration (1,695 + 6,144 = 7,839 < 8,192); confirmation max prompt 1,205 (sum 7,349). All summary context-overflow flags are false. No cap/context was changed.
- Confirmation B took more summed request seconds than A (5,368.644 vs 4,756.018), while correct/hour was higher because more saved answers scored correct. Correct/hour is the frozen metric, not raw request latency or tokens/second.
- Whole-stack difference: model pack/quantization, engine, sampler, drafter and cache differences are confounded. Arm B uses the unchanged E49 thinking adapter (effort 0.9, thinking on, no forced opener, answer_room=false), dspark drafting and hybrid placement. This is not an isolated engine or quantization comparison.
- Reasoning text was not audited. Small n: 24 distinct confirmation items, two repeats, 48 samples per arm. Six synthetic families and one selected level; calibration is spent and never pooled. This is a development result, not equivalence or a general coding, tool, long-context or production result.

Hypotheses versus observation: H1 and H2 were fixed before data and evaluate true at the saved point estimates. The speed-ratio lower bootstrap bound is below 1.0; the required reading rule therefore does not label E50 promising again. No mechanism for the stack difference is established. No promotion or router change follows from this run.

## Verification and private provenance

Final verification on 2026-11-24: GPU idle at 411 MiB / 0%, no model process left, all six shutdown records report `owned_server_exited=true`. `python -m pytest scripts/test_e50.py -q`: **13 passed** before and after execution. Pytest emitted existing pytest-asyncio fixture-loop-scope and anyio/pytest alias deprecation warnings.

Protected and frozen hashes matched before and after:

| File | SHA-256 |
|---|---|
| `tmp/e45/log.jsonl` | `2d40ccd3e22a0c1ffa735854726a49e0562e86fbbf91431939ce3211d47c437d` |
| `tmp/e45v2/cohort-seal.json` | `157b16a24aa6074f134f35a3ef5d063a1b12792d96ff40b4fb372d037266f012` |
| `tmp/e50/fixtures.json` | `fc9cf5494dcd885af55d3860cb6055ebb59a113b9426dd5534cb59c8e91b15bb` |
| `tmp/e50/protocol.json` | `18edd80c923145442436ce47542cd624967739f66a9c948fdf7f767c61aa4736` |
| `scripts/e50_pool.py` | `d116d1d88b54f52cf613662ee72008840963f9b63a8920fa56829587ea5f6585` |
| `scripts/e50_pilot.py` | `40886177aa4426765da844bfde8675f9b5baefeddff17ee858c09453d744b9b5` |
| `scripts/e50_server_run.py` | `d96802e9d32729c677f1e73b6f290b9af6a3c8804701cfba60643433092f64d8` |
| `scripts/e49_thinking_server.py` | `789a46306d80085e58b527a20b451820cef1fefed9a28173a5ea07ea91b1c937` |

Saved analysis provenance (raw outputs remain git-ignored and private):

| File | SHA-256 |
|---|---|
| `tmp/e50/selection.json` | `a2600d1a2df827a4f2371acc6da509436208434288154a3446ddaf2044fe64a6` |
| `tmp/e50/summary-cal.json` | `09cef9c6ca2b117fab3ab7393beb3e11aa4a9d1474cc01e2a5eb86b3a9211d48` |
| `tmp/e50/summary-conf.json` | `07a7dbf88f4e841afd767b16b336a8b91518e3e4836437b853a0cbba3208c564` |

The original freeze record is retained unchanged. Frozen E50/E49/E47/E45 files and attempt markers were not edited. No arm-block was rerun or replaced; selection was written only by `e50_pilot.py select`. Existing unrelated working-tree changes were left alone. Public evidence synchronization and website updates are deliberately unpublished under the explicit private/no-publication instruction; `tmp/porsync-research` was not accessed or changed. Any future authorized release must separately review selected artifacts and synchronize the public record before linking it.

Credit: Thinking Machines Lab for Inkling 2 Mini; Niko1221 and contributors for Niko1221's Strata engine; the llama.cpp authors for llama.cpp.
