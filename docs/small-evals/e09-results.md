> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E09 — the model did not invent filters; output format was the bigger problem

**Completed locally on 2026-11-08.** 600 test attempts, four arms, 150 frozen requests, Qwen3.5-9B Q4_K_M on the local RTX 5060 Ti. No external model API, frontier-model evaluation or subscription was used. E16 remains paused.

Across **1,696 tool calls, none invented a parameter**. Among readable structured finals, no unsupported constraint was falsely listed as applied or silently dropped. This leaves the main filter-error hypotheses with a baseline of zero; the extra wording had no such errors to reduce in this setup.

That is not perfect tool use: **72/600 attempts failed the final-output contract**, and one further attempt used incorrect category values and reported no matches. Overall, 527/600 satisfied the task and output requirements.

| Arm | Tool-description change | Supported /50 | Unobservable /50 | Post-filterable /50 | All tasks /150 | Invalid final /150 |
|---|---|---:|---:|---:|---:|---:|
| T0 | Plain parameter docs | 47 | 40 | 44 | 131 | 19 |
| T1 | T0 + “These are the only filters…” | 48 | 47 | 47 | 142 | 7 |
| T2 | T1 + disclose unsupported filters | 50 | 30 | 42 | 122 | 28 |
| T3 | T2 + reject unknown arguments | 49 | 37 | 46 | 132 | 18 |

Each group has 50 requests. Unobservable requests require attributes absent from the catalogue: waterproof, organic materials, or machine washable. Post-filterable requests require colour, size, or minimum rating, which are returned in tool results but have no search parameter. Correct unobservable responses return no IDs and disclose the missing evidence. Supported and post-filterable tasks require grounded, matching product IDs.

The 72 invalid finals comprised 54 tool calls emitted as text instead of a final answer, 15 answers containing JSON plus extra prose, and three malformed JSON answers. They were counted as failures, with no retry or JSON extraction. The extra tool-call text commonly appeared after the four-call budget. One valid T1 answer also failed: it searched with category values `Dune bags` and `Dune` instead of separating category `bags` and brand `Dune`.

T1 had fewer invalid finals than T0 here (7 versus 19). A **post-hoc**, unadjusted paired exact McNemar test gives p=0.00754; six format comparisons are published. This is an exploratory finding from one templated catalogue and one deterministic pass, not a general recommendation. T2 produced more format failures, especially on unavailable attributes. The original structured filter-error metrics stayed at zero in all arms. On unsupported requests, valid-final denominators were T0 84/100, T1 94/100, T2 72/100, T3 83/100; conservative error including unreadable finals was respectively 16%, 6%, 28%, 17%.

H1's predicted ≥25% T0 claim/drop error was not observed. H2–H3 could not demonstrate reductions from zero baseline invention/drop. H4 cannot establish a behavioural benefit from rejection when no arm attempted unknown arguments; the server rejection path is covered by tests. Supported success ranged from 47–50/50, with all six paired p-values ≥0.25. This does not establish equivalence; Wilson intervals and all comparisons are in the machine-readable summary.

Two qualifications matter. Every arm already received the same instruction to disclose unverifiable requirements, so this is an incremental tool-description test against a strong baseline. The requests use narrow generated templates, one catalogue, a fixed price bound, and an in-stock condition redundant with that bound. Matching post-filter outcomes do not prove the model's internal filtering process. Natural-language prose claims are retained but are outside the mechanical claim metric.

A reporting defect was identified when 34 test traces were complete: the frozen scorer marked supported filter claims in correct empty-item refusals as false claims, overlooking that the search tool had applied those filters. A separate, tested audit scorer restores the original specification's tool-evidence branch. Legacy false-claim counts (T0 16, T1 19, T2 8, T3 16) remain in the summary and raw traces; corrected counts are zero. This is an explicitly post-start correction. Prompts, tools, requests, sampling and queue were unchanged.

Validation: ten tests pass; correctness lint, reporting format/frozen-byte integrity, and compilation pass. Every one of the 1,696 logged tool results replays exactly against the frozen SQLite catalogue. All 600 request/arm pairs, raw final decoding and legacy scores are checked. A seeded 21-case trace audit is included. The 600 test model loops took 2,071.9 seconds; the runner stopped its own server afterward.

- Protocol and reproduction (not included in this public release)
- Inputs and run notes (not included in this public release)
- Full result tables (not included in this public release)
- Summary, intervals and comparisons (not included in this public release)
- Scoring amendment (not included in this public release)
- Trace audit (not included in this public release)
