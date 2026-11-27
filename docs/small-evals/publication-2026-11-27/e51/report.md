> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E51 results: L3 with a 12,288-token cap (private)

Date: 2026-11-25 (Asia/Shanghai); execution began 2026-11-24. All four frozen blocks completed in order A1, B1, B2, A2. Private development result; no push, publication, promotion or router change. The frozen protocol is retained unchanged.

Observed: A scored 58/72 and B 60/72. The saved B/A correct-per-hour ratio is 0.8550469294428674. The frozen reading rule gives `H1=false`, `H2=true`, `ceiling_again=false`, and `promising_again=false`. No claim beyond these saved samples follows.

## Frozen method and launch checks

Executed the frozen protocol (private source reference withheld) without changing scripts, fixtures, cap, context, order or settings. L3 only, seed 51, 36 distinct items across six families, two fixed-order repeats: 72 samples per arm. No calibration. Arm A is llama.cpp IQ3_XXS with thinking; arm B is SQ-15 with Niko1221's Strata engine and the unchanged E49 thinking adapter (effort 0.9, answer_room=false, dspark drafting).

Context 16,384; completion cap 12,288; temperature/top-p 1.0; one slot; request timeout 600 s; arm-block budget 9,000 s; one unscored warmup per block; stop after two consecutive request errors. Exact final JSON scoring, reasoning excluded; errors, timeouts and length stops fail. Correct/hour = correct / summed scored-request seconds * 3,600; download, load, warmup and shutdown excluded. Wilson 95% intervals and item-clustered bootstrap (both repeats together), 10,000 resamples, seed 5151. H1 requires B/A >= 1.25; H2 requires B minus A accuracy >= -0.10. Promising again additionally requires the ratio interval lower bound > 1.0; ceiling again requires both arms at 100%. Headline comparison requires all 72 samples in each arm. Secondary metrics are descriptive, not gating.

Preflight found exactly the three frozen files in `tmp/e51/`; protected and frozen script hashes matched and 11 tests passed. Launch observations below had no llama-server, strata-inkling, ollama or edge0-infer process. Each launch had GPU use below 1,500 MiB and at least 4 GiB available RAM; runners also enforced their pinned model hashes. One GPU job ran at a time. No unrelated process was stopped.

| Block | GPU used MiB | Available RAM GiB |
|---|---|---|
| A1 | 411 | 12.306 |
| B1 | 321 | 12.436 |
| B2 | 322 | 13.220 |
| A2 | 348 | 13.091 |

## Observed per-arm results

### A: llama.cpp IQ3_XXS

| Metric | Value |
|---|---|
| n | 72 |
| Correct | 58 |
| Accuracy | 80.56% |
| Wilson 95% | [0.6996724105411147, 0.8804852062054944] |
| Scored request seconds | 7974.555199700058 |
| Correct/hour | 26.183278536695493 |
| Length stops | 1 |
| Length-stop rate | 1.39% |
| Request errors | 0 |
| Non-length n | 71 |
| Non-length correct | 58 |
| Non-length accuracy | 81.69% |
| Median completion tokens | 4913.0 |
| p90 completion tokens | 9400 |
| Max completion tokens | 12288 |
| Max prompt tokens | 1205 |

### B: SQ-15 / Niko1221's Strata engine

| Metric | Value |
|---|---|
| n | 72 |
| Correct | 60 |
| Accuracy | 83.33% |
| Wilson 95% | [0.7308929306946451, 0.9020062875743832] |
| Scored request seconds | 9648.055068900052 |
| Correct/hour | 22.387931915548815 |
| Length stops | 0 |
| Length-stop rate | 0.00% |
| Request errors | 0 |
| Non-length n | 72 |
| Non-length correct | 60 |
| Non-length accuracy | 83.33% |
| Median completion tokens | 3669.5 |
| p90 completion tokens | 9047 |
| Max completion tokens | 11812 |
| Max prompt tokens | 1205 |

B vs A comparison block, verbatim JSON values and formatting from `tmp/e51/summary-conf.json`:

```json
{
  "speed_ratio": 0.8550469294428674,
  "accuracy_diff": 0.02777777777777779,
  "bootstrap": {
    "ratio_ci95": [
      0.7171749009434315,
      1.061580272716848
    ],
    "accuracy_diff_ci95": [
      0.0,
      0.06944444444444453
    ],
    "skipped_resamples": 0
  },
  "H1": false,
  "H2": true,
  "ratio_lower_bound_above_1": false,
  "ceiling_again": false,
  "promising_again": false
}
```

## Observed families and blocks

| Family | A correct/n | A accuracy | A length stops | B correct/n | B accuracy | B length stops |
|---|---|---|---|---|---|---|
| aggregate | 12/12 | 100.00% | 0 | 12/12 | 100.00% | 0 |
| dedup | 12/12 | 100.00% | 0 | 12/12 | 100.00% | 0 |
| intervals | 10/12 | 83.33% | 1 | 12/12 | 100.00% | 0 |
| inventory | 12/12 | 100.00% | 0 | 12/12 | 100.00% | 0 |
| machine | 12/12 | 100.00% | 0 | 12/12 | 100.00% | 0 |
| schedule | 0/12 | 0.00% | 0 | 0/12 | 0.00% | 0 |

| Block in run order | n | Correct | Accuracy | Request seconds | Stop reason | Owned server exited |
|---|---|---|---|---|---|---|
| A1 | 36 | 28 | 77.78% | 3860.319893 | completed | true |
| B1 | 36 | 30 | 83.33% | 4848.913082 | completed | true |
| B2 | 36 | 30 | 83.33% | 4799.141987 | completed | true |
| A2 | 36 | 30 | 83.33% | 4114.235307 | completed | true |

## Observed resource extrema

Computed from all two-second `*-resources.jsonl` samples. RAM/swap are host-wide; sampled extrema can miss between-sample peaks. No resource-monitor error rows were recorded.

| Block | Samples | Min available RAM GiB | Peak swap GiB | Peak GPU used MiB | Min GPU free MiB | Peak GPU util % | Peak temp C | Peak power W |
|---|---|---|---|---|---|---|---|---|
| A1 | 1878 | 0.751320 | 7.061440 | 14036.0 | 2015.0 | 98.0 | 68.0 | 126.68 |
| B1 | 2355 | 8.088158 | 1.333485 | 15069.0 | 982.0 | 99.0 | 63.0 | 118.93 |
| B2 | 2335 | 9.530888 | 1.350597 | 15095.0 | 956.0 | 100.0 | 63.0 | 120.24 |
| A2 | 1998 | 1.213566 | 7.129799 | 14009.0 | 2042.0 | 98.0 | 68.0 | 138.05 |

Both A blocks fell below 4 GiB available RAM during execution (minimum 0.751320 GiB); peak swap was 7.129799 GiB. All launch checks passed the frozen 4 GiB requirement. These are observed resource conditions; their effect on outcomes was not isolated.

## SQ-15 placement in Niko1221's Strata engine

`tmp/e51/conf-strata-sq15-thinking-b1-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.26s), experts=2773 VRAM / 299 host (6.80s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.56 GiB free VRAM): global KV = 0 VRAM + 16384 mapped host tokens (512.0 MiB host RAM, max_ctx=16384)
```

`tmp/e51/conf-strata-sq15-thinking-b2-engine.log`:

```text
[InkCUDA] Loaded [withheld local path] (SQ-15): trunk=2.07 GB (1.30s), experts=2773 VRAM / 299 host (8.56s, hyb=1, promo=0, pf_buf=64MB), sm120_tc=1, screen=1
[InkCUDA] Auto Host KV Offload (kv_fmt=0, 1.56 GiB free VRAM): global KV = 0 VRAM + 16384 mapped host tokens (512.0 MiB host RAM, max_ctx=16384)
```

## Observed anomalies and standing limits

- All four blocks completed without launch failure, crash, timeout, request error, budget stop, retry or redraw. Runner error logs are empty. No output was replaced or hand-edited. No paid API or frontier call was used.
- One length stop: A1, `e51-L3-intervals-3`, 12,288 completion tokens, parse-error flag. A1 also had an incorrect non-length `intervals-4` row; its parsed JSON did not match the oracle. The other 24 wrong rows were schedule rows, all non-length finishes with parsed JSON. Thus there were 25 incorrect non-length rows overall. Reasoning text was not audited; no cause is inferred.
- Schedule scored 0/12 in each arm, with zero length stops. It remains reported separately as specified; these data do not establish an uncapped result or a general family-wide floor.
- No recorded prompt-plus-cap overflow: both arms max prompt 1,205 tokens; 1,205 + 12,288 = 13,493 < 16,384. Both saved context-overflow flags are false. All requests used the frozen cap and context.
- Whole-stack confounding remains: model pack/quantization, engine, sampler, drafter and cache differ. These results do not isolate an engine or quantization effect.
- Small n: 36 distinct synthetic items, two repeats, 72 samples per arm, six families and one mechanically selected level. No equivalence, general engine/quantization, coding, tool, long-context or production claim.

Hypotheses and reading rule: H1 and H2 were frozen before requests. H1 is false at the saved point estimate, H2 is true, and the ratio interval lower bound is below 1.0. Therefore `promising_again=false`; `ceiling_again=false`. Hypothesis only: any proposed explanation for the stack difference or effect of a larger cap would require further measurements. No mechanism is established, and no promotion or router change follows.

## E50 side-by-side (different cap and item set; not pooled)

| Study | Completion cap | Distinct items / samples per arm | A correct | B correct | B/A correct-hour ratio | Ratio bootstrap CI95 |
|---|---|---|---|---|---|---|
| E50 | 6144 | 24 / 48 | 25/48 | 38/48 | 1.3465 | [0.9765, 1.9929] |
| E51 | 12288 | 36 / 72 | 58/72 | 60/72 | 0.8550469294428674 | [0.7171749009434315, 1.061580272716848] |

E50 used context 8,192, fresh seed 50 and shorter timeout/budget; E51 used context 16,384 and seed 51. These are separate development results. The side-by-side does not isolate a cap effect and is not pooled evidence.

## Verification and private provenance

Final verification: GPU idle at 348 MiB and 0% utilization; no model process, owned runner PID or saved owned server PID remained. All four shutdown records report `owned_server_exited=true`. `python -m pytest scripts/test_e51.py -q`: 11 passed before and after execution. Existing pytest-asyncio and anyio/pytest deprecation warnings were emitted.

The three required hashes below matched their supplied pins before and after. Protocol hash also matches the freeze record; all five frozen scripts match `tmp/e51/freeze-hashes.json` and the protocol pins.

| File | SHA-256 |
|---|---|
| `tmp/e45/log.jsonl` | `2d40ccd3e22a0c1ffa735854726a49e0562e86fbbf91431939ce3211d47c437d` |
| `tmp/e45v2/cohort-seal.json` | `157b16a24aa6074f134f35a3ef5d063a1b12792d96ff40b4fb372d037266f012` |
| `tmp/e51/fixtures.json` | `e78f3696f54a0ecc83ef34673fa3ab4fb17d9ceb6bb1efebbc55465de8543801` |
| `tmp/e51/protocol.json` | `bca370f4872e5c2ea8fc53809c5d6a5dba834a815a8eb4965b9e43514fbf2a73` |
| `scripts/e51_pool.py` | `220573e392fc018b62995638ee7f415e7c9641f8a2792a7cde18e31dfb0fc4b3` |
| `scripts/e51_pilot.py` | `b174bc562c7ca8a49982dd17eccda1160ffaacb49da59664f2b8a5624f2d081b` |
| `scripts/e51_server_run.py` | `b9740a3053f9aa786d4c43f37cc3d2458d5dd5e511bf924a7ce37e2250633fbf` |
| `scripts/e50_pool.py` | `d116d1d88b54f52cf613662ee72008840963f9b63a8920fa56829587ea5f6585` |
| `scripts/e49_thinking_server.py` | `789a46306d80085e58b527a20b451820cef1fefed9a28173a5ea07ea91b1c937` |

Saved summary SHA-256: `bb7fb66e79d2f22a3a1f87eec4dbfced468fecb913938feb3817436b3bcb9a33`. Raw outputs remain private and git-ignored under `tmp/e51/`. Only this report is selected for commit. Unrelated working-tree changes, protected E45/E47/E49/E50 files and attempt markers were left alone.

Public evidence synchronization and website updates are explicitly deferred by the private/no-publication instruction. `tmp/porsync-research` was not accessed or changed. A future authorized release still requires review of selected artifacts and public evidence synchronization; no public update is claimed complete.

Credit: Thinking Machines Lab for Inkling 2 Mini; Niko1221 and contributors for Niko1221's Strata engine; the llama.cpp authors for llama.cpp.
