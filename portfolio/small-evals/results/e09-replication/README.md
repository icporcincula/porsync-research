> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E09 local replication protocol

Use Gemma 4 12B IT Q4_K_M and gpt-oss-20b MXFP4. The original Qwen3.5-9B run is the reference. Reuse the 500-product catalogue, 150 test requests, four tool-description arms and shuffled attempt order. Each new profile has 600 planned test attempts.

Use the original llama.cpp executable, loopback endpoint, native tool parsing, 16K context, one slot, reasoning off, temperature 0, seed 9009, 1,024 output tokens per turn and four-call limit. Run one model at a time. Keep the existing 7/10 supported-development gate separately for each profile. Use the original runtime settings without model-specific retries, output cleanup or prompt changes. Record gate failures and transport failures separately from test outcomes.

Apply the published corrected E09 scorer from the outset for reporting and retain the original scorer fields for trace replay. Report invented arguments per attempt and per call, attempted and accepted unknown keys, malformed finals, task success by request group, claims and drops. Inspect native calls for rejected arguments and category values outside the catalogue. The primary paired contrasts are T1 versus T0 and T2 versus T0 on final format, alongside invention counts per arm. T3 tests server enforcement separately from model behaviour. Use the original report's Wilson intervals and exact paired comparisons. Compare profiles on the same requests and describe profile-specific effects without treating a single catalogue as representative of all tool use.

From `portfolio/small-evals`, run `python -B e09_replicate.py PROFILE dev`, then `test` and `report` for profiles that pass. The runner writes the staged freeze and raw traces under each profile directory. This write-up includes the aggregate summary. The raw traces remain in the local run directory.

## Development gate

| Profile | Supported successes | Valid finals | Test eligibility |
|---|---:|---:|---|
| Gemma 4 12B IT Q4_K_M | 10/10 | 10/10 | Passed |
| gpt-oss-20b MXFP4 | 6/10 | 10/10 | Stopped at development |

Both profiles made native tool calls and neither invented an argument key during development. All four gpt-oss misses used category values outside the exact-match catalogue (`Jackets`, `jacket` or `shirt`), so the queries returned zero products. The shared tool description names the category parameter and leaves its allowed values implicit. This result describes the model and tool interface together.

## Test results

Gemma completed all 600 matched attempts on the local RTX 5060 Ti. It invented zero argument keys in 885 tool calls, matching the original Qwen run's zero in 1,696. All 885 logged calls replayed exactly against SQLite, and the report verified all 600 request/arm pairs, saved legacy scores, and raw final decoding. Gemma used valid catalogue category values in every test search that specified a string category. GPT-OSS has no test outcomes because it failed the development gate.

| Arm | Gemma supported /50 | Gemma unobservable /50 | Gemma post-filterable /50 | Gemma all tasks /150 | Invalid finals Gemma /150 | Invalid finals Qwen /150 |
|---|---:|---:|---:|---:|---:|---:|
| T0 | 31 | 5 | 27 | 63 | 76 | 19 |
| T1 | 29 | 3 | 25 | 57 | 77 | 7 |
| T2 | 32 | 3 | 25 | 60 | 77 | 28 |
| T3 | 31 | 5 | 25 | 61 | 77 | 18 |
| Total | 123/200 | 16/200 | 102/200 | 241/600 | 307/600 | 72/600 |

Task success includes the full output contract. Gemma selected correct post-filtered IDs in 133/200 attempts, of which 102/200 also satisfied all task requirements. Qwen passed 527/600 tasks overall.

Gemma's T0-to-T1 and T0-to-T2 changes were both 76 to 77 invalid finals, with exact paired McNemar p = 1.00 for each. The original T1 improvement (19 to 7) and T2 increase (19 to 28) did not recur. Of Gemma's 307 invalid finals, 163 contained a JSON object plus extra text, 134 were prose, and 10 contained tool-call text. These categories include Gemma's native tool-call marker, which the original reporter groups under `other`. The 307 failures all ended with a server stop rather than a length finish.

Among Gemma's 161 readable finals on unsupported requests, six attempts had a false structured claim or a silent drop under the corrected scorer. Counting unreadable finals as failures brings the combined error to 245/400 unsupported requests. The shared final-output instructions, templated requests and single catalogue limit what can be inferred about other tools or deployments.

Gemma's test loops took 2,281 seconds (38 minutes). Both weights were already installed and all inference ran over loopback. The 10 E09 scorer and catalogue tests passed.

- [Gemma summary, intervals and paired comparisons](gemma4-12b/results/e09/replication/summary.json)
- [Original Qwen report](../../../../docs/small-evals/e09-results.md)
