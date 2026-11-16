> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E09 — local tool-filter results

600 frozen test attempts: 150 requests × four arms, gemma-4-12b-it-Q4_K_M, local llama.cpp, one slot, thinking off. No frontier model or subscription. One synthetic catalogue, one deterministic run per arm.

| Arm | Supported success /50 | Unobservable success /50 | Post-filter success /50 | Invented argument /150 | Invalid final /150 |
|---|---:|---:|---:|---:|---:|
| T0 | 31 | 5 | 32 | 0 | 76 |
| T1 | 29 | 3 | 32 | 0 | 77 |
| T2 | 32 | 3 | 35 | 0 | 77 |
| T3 | 31 | 5 | 34 | 0 | 77 |

Unsupported requests combine 50 unobservable and 50 post-filterable cases. Claim/drop flags can overlap. Rates below use all 100 requests; invalid finals are listed separately and count in conservative error.

| Arm | False claim /100 | Silent drop /100 | Claim or drop /100 | Claim/drop/invalid /100 | Valid finals /100 |
|---|---:|---:|---:|---:|---:|
| T0 | 3 | 2 | 3 | 62 | 41 |
| T1 | 2 | 1 | 2 | 62 | 40 |
| T2 | 0 | 0 | 0 | 60 | 40 |
| T3 | 1 | 1 | 1 | 61 | 40 |

| Arm | Tool calls | Calls with invented arguments | Accepted invented arguments | Model-loop seconds |
|---|---:|---:|---:|---:|
| T0 | 255 | 0 | 0 | 588.3 |
| T1 | 226 | 0 | 0 | 583.5 |
| T2 | 199 | 0 | 0 | 557.8 |
| T3 | 205 | 0 | 0 | 551.1 |

Wilson 95% intervals, exact paired McNemar comparisons (exploratory, unadjusted), valid-final-only rates, per-call invention, acceptance and runtime are in `summary.json`. No equivalence follows from a non-significant difference. Shared output instructions already tell every arm to acknowledge unverifiable properties; this can make T0 strong. Prose claims are outside the mechanical scorer. T3 rejects unknown parameters but does not constrain model decoding. Generated request templates and a single catalogue limit generalisation.

Protocol and reproduction: runner README (not included in this public release). Raw traces and frozen code/input/runtime hashes are in this run directory.

Reporting amendment: after the first 34 test traces, an empty-item refusal exposed a false-claim scorer defect. The original metric requires both lack of tool application and lack of satisfying items; the frozen scorer checked only items. `e09_audit.py` restores the tool-evidence branch, with regression tests. Raw stored scores are untouched; `summary.json` preserves the original counts alongside corrected counts. No prompt, request, sampling or tool behaviour changed. This correction was made after seeing an early outcome and is not claimed as preregistered.
