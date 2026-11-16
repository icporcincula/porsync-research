> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E03 local replication

The replication reran the original E03 contract-field extraction task on Gemma 4 12B Q4_K_M and Qwen3.6-27B UD-IQ3_XXS. It used the frozen 630 field–excerpt pairs across five fields (315 labeled present and 315 labeled absent). Each profile made 1,890 requests. F3 is an offline filter of F2, so it adds no inference calls.

## What the arms compare

| Arm | Actual implementation |
|---|---|
| F0 | Request JSON and say to use null for unstated values. No response schema. |
| F1 | The identical F0 prompt with an enforced nullable-value schema. |
| F2 | Request a verbatim quote and extracted value, use an explicit `NOT_STATED` sentinel, and enforce the evidence/value schema. |
| F3 | Keep a non-null F2 answer only if the evidence is a non-empty normalized substring of the excerpt. |

The prose in the original study describes F0 versus F1 as an omission-instruction contrast. The frozen prompts already give that instruction in both arms, so the realized contrast is schema enforcement. F2 changes the prompt, schema and abstention representation together.

The original Qwen3.5-9B Q4_K_M results are historical, from llama.cpp b11408. Both new profiles ran on b11753, one slot, 2,048-token context, 200 generated tokens, temperature zero, f16 KV, prompt caching and reasoning disabled. The comparison is between deployments, including differences in quantization and server version. Both weights were already installed.

## Results

Each metric has a denominator of 315 per arm. Recall uses the original overlap criterion. Strict match is the original scorer's normalized substring metric.

| Profile | Arm | Invention | Recall | Strict match |
|---|---|---:|---:|---:|
| Qwen3.5-9B (original) | F0 | 20 | 296 | 289 |
| | F1 | 21 | 298 | 290 |
| | F2 | 19 | 275 | 241 |
| | F3 | 19 | 272 | 238 |
| Gemma 4 12B | F0 | 11 | 285 | 280 |
| | F1 | 11 | 285 | 280 |
| | F2 | 17 | 291 | 240 |
| | F3 | 17 | 287 | 237 |
| Qwen3.6-27B | F0 | 15 | 293 | 289 |
| | F1 | 15 | 293 | 289 |
| | F2 | 13 | 290 | 230 |
| | F3 | 13 | 290 | 230 |

The substring check caught **0 of 49** F2 inventions across the three deployments on this shared sample. It removed three overlap-correct values from the original 9B, four from Gemma and zero from the 27B. For example, Gemma and both Qwen deployments cited the Colombian Civil Code passage in chunk 345 for Governing Law. The passage explains the order in which payments are applied. It does not designate the law governing the agreement.

The original 6.7-point overlap-recall loss from F0 to F2 did not recur at that magnitude. Gemma gained 1.9 points (95% contract-clustered interval −0.3 to +4.1) and the 27B lost 1.0 point (−3.0 to +1.0). Gemma's invention rate rose 1.9 points (+0.4 to +3.8), while the 27B's fell 0.6 points (−2.7 to +1.3). Strict match fell in all three profiles (−15.2, −12.7 and −18.7 points for the 9B, Gemma and 27B respectively). F2's output contract and its tendency to produce longer values can affect the substring-based strict score.

Among non-null answers on labeled-present F2 cases, the substring check accepted 275/279 quotes for the 9B, 288/293 for Gemma and 291/291 for the 27B. Those accepted quotes contained a full normalized gold span in 196, 143 and 195 cases respectively. This diagnostic measures literal span coverage. Semantic support was spot-checked with individual examples.

Both replication profiles completed all 3,780 calls combined. No prompt truncations were logged. One Gemma F2 output hit the generation cap and was unparseable. One 27B F0 output hit the cap and still parsed under the original scorer.

## Scoring and reproduction

The original scorer defines invention as a non-null value on a labeled-absent field–excerpt pair. Recall uses token overlap on labeled-present pairs. The stricter value match also accepts a normalized substring of the gold span. Absence labels are excerpt-level and can be noisy. Quote matching measures literal coverage. Even a quote containing a gold span does not independently establish that the extracted value is supported.

Run from `portfolio/small-evals` with the local model weights and runtime paths configured as in the runner:

```powershell
python -B e03_replicate.py gemma4-12b qwen36-27b
python -B e03_replication_report.py
```

Each model folder includes the input/runtime freeze and original scorer summary. The runner writes raw F0–F2 outputs, the sample copy and server logs to the same folder locally. `diagnostics.json` adds paired bootstrap intervals by contract title, quote coverage, surviving quote/value pairs and generation finish reasons. The original result files are separate under `results/e03/`.
