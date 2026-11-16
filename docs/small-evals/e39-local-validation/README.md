> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E39 local follow-up — 2026-11-15

Local validation requested after the E39/E40 write-ups. No frontier calls,
subscription tokens, router-table changes or global route-mode changes.

## Frozen scope and execution

`run.py` records a six-minute, thirteen-probe observation using the actual router
health functions, seven small inference requests, three existing-category route
attempts, four deliberately injected transport-fault cases, and a longer-context
retrieval prompt. Patchsmith stays at `844fed1`; the model, build and 32,768-token
context match the earlier E39 setup. Temperature zero, thinking off.

The five-minute startup cooldown and 2 GiB available-RAM floor are left at their
defaults. A `recent_http400` startup decision denotes conservative unknown
history; it is **not evidence that an HTTP 400 actually occurred**. TCP readiness
is weaker than inference readiness. `load.json` measures time to `/v1/models`,
with unspecified filesystem cache state, not cold load or time to first answer.

`launch.ps1` temporarily replaces the previously loaded E40 Qwen server and
restores its exact arguments afterward. It never stops unrelated applications.
The existing EvalPlus harness scores archived samples concurrently during part
of the observation; therefore this is a shared-load diagnostic, not a controlled
RAM-pressure experiment. No deliberate memory exhaustion is used.

## Archived thinking-on MBPP subset

The previously unscored interrupted generation contains 106 of 378 problems.
`score_partial_mbpp.py` selects precisely those IDs, retains standard EvalPlus
tests/reference results, and writes separate artifacts without modifying the
original samples or harness. The source SHA-256 and IDs are in
`partial-mbpp-manifest.json`.

| Same 106 problem IDs | Base tests | Base and extended tests |
|---|---|---|
| Thinking on, newly scored archived samples | 98/106 | 87/106 (82.1%) |
| Thinking off, existing archived scores | 95/106 | 84/106 (79.2%) |

The combined score requires **both** base and extended tests to pass. Counting
the extended status alone would incorrectly give 90/106 and 84/106. This is a
nonrandom, interrupted subset, not a complete thinking-on MBPP+ result and not
evidence that thinking helps generally. The existing full thinking-off 253/378
result and the thinking-on HumanEval+ result remain separate. No missing sample
was counted as a failure or newly generated here.

## Interpretation boundaries

An injected OOM response tests the real client's retry path followed by real
Edge0 inference. It does not establish recovery from actual GPU/RAM exhaustion.
The timeout injection drops the first request before backend inference and uses
a diagnostic 10-second client timeout; it does not reproduce the production
180-second prefill stall or duplicate server work. Exhausted retries and generic
400 responses must surface rather than falsely report recovery.

Existing-category route attempts are integration checks, not held-out accuracy
measurements. A health-gated `frontier_required` response is a local routing
decision only; no frontier executor is called and it is not a completed task.
New paired held-out evidence still requires frontier outcomes before comparison
or promotion. Natural OOM recovery and a useful health cutoff need a larger,
controlled series with both successful and failing conditions.

Cold-cache measurement would require controlling the OS cache; an enforced
20 GiB limit requires a separate process-tree memory-limit protocol. NVFP4 needs
a different model artifact. None of these conditions is substituted by this run.
No settings are selected from these observations.

## Health, routing and retry results

All 13 health probes found the server reachable, with only **0.011–0.347 GiB**
of host RAM available. The first ten decisions used `recent_http400` for the
startup cooldown; the final three used `low_ram`. All seven two-token inference
checks returned the expected `2`: median 1.25 s, range 0.625–21.312 s. The slow
request overlapped partial-MBPP scoring. Small successful requests despite low
RAM do not establish safe agent workloads or justify a lower threshold.

After the full cooldown, `bug1`, `multifile` and `feature` all returned
`frontier_required` with `low_ram`. Their fixture checkouts stayed clean. Thus
the actual default gate was exercised, but **no local routed coding attempt ran**.
This is an operational reason the local path remains unvalidated, not a model
coding failure or a successful routed task.

| Controlled proxy case | HTTP attempts | Observed result |
|---|---|---|
| One OOM-specific 400, then real Edge0 | 2 | Recovered, correct `2` |
| Generic non-OOM 400 | 1 | Error surfaced, no retry |
| OOM-specific 400 on both attempts | 2 | Error surfaced after one retry |
| One dropped/delayed request, then real Edge0 | 2 | Recovered, correct `2`, 10.875 s |

All four behaved as intended. This establishes controlled transport recovery
with a real inference backend, while natural OOM/prefill-stall recovery remains
unmeasured. No natural fault was induced and no health threshold was calibrated.

## Longer context and restoration

The saved prompt contains an opening marker, 28,000 repetitions of `word`, and
a request to return the marker. Actual input was **28,036 tokens**, output nine
tokens. Edge0 returned the correct `cobalt-river-739` in **25.344 s**. Server
timing was 24.419 s to first token and 15.8 decode tokens/s. This extends simple
retrieval beyond the earlier 24K prompt observation; one repetitive prompt does
not establish long-context coding, document reasoning or 131K support.

The initial E40 restoration process exited before readiness because the CUDA
`bin/x64` DLL search path was absent. It was relaunched with the original E40
launcher search path and unchanged serving arguments. `launch.ps1` now includes
that path. Historical Edge0 logs were not overwritten; this directory contains
the new server log and the exact longer-context prompt.

Final restoration verification found only the expected Qwen `llama-server.exe`
on port 8140, no Edge0/Strata process, and health `ok`; see
`restoration-verified.json`. Artifact assertions checked all thirteen health
rows, seven successes, three unchanged source checkouts, four fault outcomes
and the exact long-context marker/token count. Python scripts parsed, website
research checks passed (48 studies), targeted ESLint passed, and `git diff
--check` passed. The nested Patchsmith checkout remains clean. The previously
reported unrelated website production-build failure was not retested.
