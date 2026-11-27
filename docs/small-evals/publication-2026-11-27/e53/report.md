> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E53: reasoning-budget replay — results (private)

Date: 2026-11-25. Stage 0 run only. Replay-only: no tools executed, no full task, no E45/Z row written, no seal-out, no push, no publication, no public-evidence sync. This file reports exactly what `python scripts/e53_budget_replay.py run P`, `run S` and `analyze` produced under the frozen protocol (e53-reasoning-budget-replay-protocol.md (private source reference withheld)); nothing was retried, replaced, reordered or retuned.

**Analyzer decision: `promising`.** Reproduced stalls: `v7h-passk`, `v9g-flaky` (2 of 3; `v8g-spiral` did not reproduce). `req1024` and `startup2048` each converted and were enforced on both reproduced stalls.

Credit: Thinking Machines Lab (Inkling model) and the llama.cpp authors.

## Method (as run)

- Pinned llama.cpp b50 / `8d60873`, Inkling 2 Mini UD-IQ3_XXS, one slot, `-c 32768`, `:8090`. Reused `scripts/e48_stall_dose.py` and `scripts/e45_stall_capture.py` unchanged; reconstructed prompts, temperature 0, seed 45, `max_tokens` 8192, cumulative 1,200 s per-task cap.
- Server **P** = stock `[withheld local path]` (no `--reasoning-budget`), conditions `control`, `req0`, `req1024`, `req2048`, `req4096` (per-request `reasoning_budget_tokens`). `req0` is an enforcement probe, never a candidate.
- Server **S** = `[withheld local path]` (`--reasoning-budget 2048` startup flag), condition `startup2048` (no request change).
- Order: all of P (3 tasks), stop, all of S (3 tasks), stop, analyze. One GPU job at a time.
- Enforcement tolerance (fixed before collection): estimated reasoning tokens <= 1.25 x budget + 64. Estimated reasoning tokens = reasoning chars / chars-per-token, where chars-per-token is taken from the same task's stalled control (content empty, so completion tokens approximate reasoning tokens).
- Converted = `finish_reason: tool_calls` with every call structurally valid (known tool, object arguments, required keys/types). Structure only, not task correctness.

## Server start proof (OBSERVED)

- **P**: pre-start GPU idle (335 MiB used, 0% util on the first sample; no `llama-server`/`strata-inkling`/`ollama`/`edge0-infer`). `e45_server.ps1 start` returned `up`. The command line read by the runner check (`psutil`) was:
  `llama-server.exe -m ...Inkling-2-Mini-UD-IQ3_XXS.gguf --port 8090 --host 127.0.0.1 -c 32768 -np 1 --jinja -ngl 99 --alias inkling-iq3 --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0.0` — **no `--reasoning-budget`**.
- **S**: pre-start GPU idle (300 MiB used, 0% util; no competing process). `e53_server.ps1 start` returned `up`. Command line identical to P **plus `--reasoning-budget 2048`**; the runner check requires exactly `2048`.
- Load times from the server logs (`[withheld local path]`, `[withheld local path]`): `load_model: loading model ...` then `server_run_i: model loaded` then `server_on_li: listening on htt[withheld local path]`. Log prefixes: P `load_model` at `0.00.068`, `listening` at `0.11.663`; S `load_model` at `0.00.054`, `listening` at `0.11.804` (≈12 s from init to listening on each). Both were stopped after their batch; no `llama-server` remained and the GPU returned to ~300 MiB / 0%.

## Per-task, per-condition results (OBSERVED)

Estimated reasoning tokens (est) are derived from the same task's control chars-per-token. "repeat" is the largest count of an exact ≥20-char trimmed paragraph in the reasoning (screen only).

### v7h-passk, turn 3 — control stalled; chars/token 2.803

| Condition | Status | finish_reason | Comp tokens | Reasoning chars | Est reasoning tok | Enforced | Converted | Tool(s) | Wall s | Largest repeat |
|---|---|---|---:|---:|---:|:--:|:--:|---|---:|---:|
| control | observed | length | 8192 | 22966 | 8192.0 | – | no | none | 200.141 | 5 |
| req0 | observed | length | 8192 | 0 | 0.0 | true | no | none | 195.047 | 0 |
| req1024 | observed | tool_calls | 1086 | 3057 | 1090.4 | true | yes | read_file | 25.109 | 1 |
| req2048 | observed | length | 8192 | 19611 | 6995.3 | false | no | none | 189.985 | 117 |
| req4096 | observed | length | 8192 | 20362 | 7263.2 | false | no | none | 191.406 | 91 |
| startup2048 | observed | tool_calls | 2110 | 5624 | 2006.1 | true | yes | read_file | 52.235 | 3 |

### v8g-spiral, turn 3 — control did NOT reproduce; chars/token n/a

| Condition | Status | finish_reason | Comp tokens | Reasoning chars | Est reasoning tok | Enforced | Converted | Tool(s) | Wall s | Largest repeat |
|---|---|---|---:|---:|---:|:--:|:--:|---|---:|---:|
| control | observed | tool_calls | 5358 | 11787 | – | – | (control) yes | write_file | 127.391 | 8 |
| req0 | observed | length | 8192 | 0 | – | – | no | none | 193.453 | 0 |
| req1024 | observed | tool_calls | 1084 | 3145 | – | – | yes | read_file | 24.797 | 1 |
| req2048 | observed | tool_calls | 2103 | 6095 | – | – | yes | read_file | 47.781 | 2 |
| req4096 | observed | length | 8192 | 22888 | – | – | no | none | 188.250 | 6 |
| startup2048 | observed | length | 8192 | 20102 | – | – | no | none | 167.656 | 9 |

Because the control already emitted a valid `write_file` call, v8g is **not** in the reproduced set; its conditions are recorded but do not count toward the gate.

### v9g-flaky, turn 2 — control stalled; chars/token 2.645

| Condition | Status | finish_reason | Comp tokens | Reasoning chars | Est reasoning tok | Enforced | Converted | Tool(s) | Wall s | Largest repeat |
|---|---|---|---:|---:|---:|:--:|:--:|---|---:|---:|
| control | observed | length | 8192 | 21670 | 8192.0 | – | no | none | 197.312 | 24 |
| req0 | observed | length | 8192 | 0 | 0.0 | true | no | none | 195.188 | 0 |
| req1024 | observed | tool_calls | 1084 | 2816 | 1064.5 | true | yes | read_file | 25.344 | 1 |
| req2048 | observed | tool_calls | 2108 | 5310 | 2007.4 | true | yes | read_file | 48.453 | 1 |
| req4096 | observed | tool_calls | 4156 | 11034 | 4171.2 | true | yes | read_file | 95.390 | 5 |
| startup2048 | observed | tool_calls | 2108 | 5433 | 2053.9 | true | yes | read_file | 49.203 | 1 |

## Controls reproduced (OBSERVED)

- `v7h-passk` — reproduced: control `length`, 8192 tokens, 22966 reasoning chars, 0 calls, 200.1 s.
- `v9g-flaky` — reproduced: control `length`, 8192 tokens, 21670 reasoning chars, 0 calls, 197.3 s.
- `v8g-spiral` — **not reproduced**: control emitted a valid `write_file` call (`tool_calls`, 5358 tokens, 127.4 s). This differs from the E45/E48 stall on this turn at the same temperature-0/seed-45 settings.

2 of 3 controls stalled, which meets the protocol's `min_reproduced` of 2, so a gate decision is possible. The reproduced set is exactly 2 tasks.

## Enforcement probe: `req0` (OBSERVED)

On both reproduced stalls, `req0` (`reasoning_budget_tokens: 0`) emptied the reasoning channel (`reasoning_chars: 0`, `reasoning_present: false`) but did **not** end the turn: `finish_reason: length` at 8192 completion tokens after ~195 s, with ~141,997 content characters and no tool call. The same happened on v8g.

- **Observed:** setting the per-request budget to 0 changed the output channel vs control (control carried 21.7k–22.9k reasoning chars; req0 carried none), so the per-request `reasoning_budget_tokens` field is read and applied at request time by this build. The "0 = immediate end" documented behaviour ends the **reasoning section**, not generation: the model continued in the content channel to the output cap.
- **Hypothesis (not established):** with the thinking section removed, the model falls back to long non-reasoning filler here, so `req0` is not a usable way to force a tool call. This says nothing about N>0 budgets.

The per-request field and the startup flag are therefore both reachable, but they behaved differently on the reproduced stalls: the tight request budget `req1024` and the startup `2048` flag each enforced and converted, whereas looser request budgets (`req2048`, `req4096`) were enforced only on `v9g-flaky` and not on `v7h-passk`. This is consistent with the E48 note that the budget re-arms per thinking-start tag (a per-section rather than aggregate turn budget): a larger allowance lets a reasoning loop start again and run to the output cap.

## Analyzer `by_condition` block (verbatim)

```json
"by_condition": {
 "control": {"converted": 0, "converted_and_enforced": 0, "enforced": 0, "of": 2},
 "req0": {"converted": 0, "converted_and_enforced": 0, "enforced": 2, "of": 2},
 "req1024": {"converted": 2, "converted_and_enforced": 2, "enforced": 2, "of": 2},
 "req2048": {"converted": 1, "converted_and_enforced": 1, "enforced": 1, "of": 2},
 "req4096": {"converted": 1, "converted_and_enforced": 1, "enforced": 1, "of": 2},
 "startup2048": {"converted": 2, "converted_and_enforced": 2, "enforced": 2, "of": 2}
}
```

`decision`: `promising`. `reproduced`: `["v7h-passk", "v9g-flaky"]`. `missing`: `[]`. `unobserved`: `[]`. (`of` = 2 reproduced stalls; `req0` "enforced" is trivially true at est=0 and is excluded from candidate conditions by the analyzer.)

Reading-rule check: `promising` requires some candidate condition to convert and be enforced on ≥2 of the reproduced stalls. `req1024` (2/2) and `startup2048` (2/2) meet it; `req2048` and `req4096` reach only 1/2.

## Per-turn time versus control (OBSERVED)

| Task | control | req1024 | req2048 | req4096 | startup2048 |
|---|---:|---:|---:|---:|---:|
| v7h-passk | 200.1 s | 25.1 s | 190.0 s | 191.4 s | 52.2 s |
| v8g-spiral | 127.4 s (converted) | 24.8 s | 47.8 s | 188.3 s | 167.7 s |
| v9g-flaky | 197.3 s | 25.3 s | 48.5 s | 95.4 s | 49.2 s |

Every converting+enforced condition finished well under its control; conditions that stalled ran to the 8192-token cap at ~190 s like the controls. No condition hit the 1,200 s per-task cap.

## Anomalies (OBSERVED)

- `v8g-spiral` control did **not** stall this replay (valid `write_file` at 127.4 s), unlike the E45/E48 stall. This removes it from the reproduced set; it is reported as-is, not re-run.
- `req0` produced identical 141,997 content characters and 8192 completion tokens on all three tasks despite different prompts — deterministic (temperature 0, seed 45) but task-invariant filler; recorded, not interpreted.
- On `v8g-spiral` (outside the gate denominator) the startup `2048` flag stalled while the per-request `req1024`/`req2048` converted, the reverse of the reproduced pattern; recorded, not counted.
- No timeout, HTTP error, GPU event or RAM event occurred. All 18 planned rows (15 on P, 3 on S) are `observed`; `missing` and `unobserved` are empty.

## Interpretation

- **OBSERVED:** on the two reproduced stalls, a per-request reasoning budget of 1024 and the startup `--reasoning-budget 2048` each turned `length`-with-no-call into a structurally valid `read_file` call, with estimated reasoning tokens inside the tolerance (1090/2006 and 1065/2054). The looser request budgets converted on only one of the two. `req0` emptied reasoning but did not convert.
- **HYPOTHESIS:** the budget works by ending a reasoning loop early enough that the model reaches a tool call before the output cap; a budget loose enough to let the loop restart (per-section re-arm) does not reliably help. Startup-flag and per-request enforcement can differ on a given turn (v8g), for reasons these three turns cannot isolate.
- **Scope of the decision:** `promising` licenses only a later, separately specified full-loop or fresh-task test; it is not a result about task success, and nothing here promotes a setting, changes the router, or claims beyond three temperature-0 turns.

## Not claimed (from the frozen protocol)

No cause beyond what the raw files show, no task-success or quality claim, no promotion, no router change, no claim beyond three turns at temperature 0 (replays are deterministic, so not independent samples). No model quality inference from a tool call that merely parses.

## Integrity and verification

- Preflight: the two required hashes matched (`tmp/e45/log.jsonl` `2d40ccd3…437d`; `tmp/e45v2/cohort-seal.json` `157b16a2…f012`), `e53_budget_replay.py check` printed `ok`, `pytest scripts/test_e53.py` passed 14, `tmp/e53/` held no `P/` or `S/` folder, free RAM 11.75 GiB, GPU idle.
- Post-run: both required hashes still match, `check` still prints `ok`, tests still 14 passed, no `llama-server` process remains, GPU ~300 MiB / 0%. Raw rows live under git-ignored `tmp/e53/P/` and `tmp/e53/S/`; `tmp/e53/summary.json` holds the full analyzer output.
- No frozen file, E45 log, cohort seal or `.attempt` marker was written; no seal-out; no condition added, retuned, reordered or retried. Only `docs/small-evals/e53-results.md` is committed (private).
