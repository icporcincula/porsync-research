# E39 operational closeout pilot

Status: **complete**, 24/24 completed. Authorized after C1b completion; separate pilot and no pooling with C1/C1b. Patchsmith HEAD 2203eb0 unchanged. C2b skipped.

| Arm | Completed/8 | Final passes | Local passes | Repairs | Eligible shadow / matched |
|---|---:|---:|---:|---:|---:|
| direct | 8/8 | 8 | 0 | 0 | 0/0 |
| shadow | 8/8 | 8 | 0 | 0 | 7/7 |
| route | 8/8 | 8 | 3 | 4 | 0/0 |

## Paired tasks

| Fixture | Fixed category | Direct final | Shadow final | Route final/local |
|---|---|---|---|---|
| f01_percent | multifile | True | True | True/False |
| f02_ttl | multifile | True | True | True/True |
| f03_dependencies | multifile | True | True | True/False |
| f04_routes | multifile | True | True | True/False |
| f05_slug | bug1 | True | True | True/True |
| f06_balance | bug1 | True | True | True/True |
| f07_query | feature | True | True | True/False |
| f08_manifest | omitted/unknown | True | True | True/False |

## Health, recovery and accounting

{"observations": 22, "pressure_skips": [{"requested_mib": 64, "available_bytes": 305709056, "reason": "Cannot retain frozen 1 GiB free reserve"}, {"requested_mib": 128, "available_bytes": 305770496, "reason": "Cannot retain frozen 1 GiB free reserve"}, {"requested_mib": 256, "available_bytes": 305786880, "reason": "Cannot retain frozen 1 GiB free reserve"}], "requests": 5, "correct": 5, "natural_faults": 0, "fresh_process": [{"health": {"server_up": true, "free_ram_bytes": 505802752, "http400_age_seconds": 0.0, "clean_seconds": 0.0}, "decision": ["frontier", "recent_http400"]}]}

Final server/GPU observation: {"at": "2026-11-20T23:10:29.565384+00:00", "edge0_processes_remaining": 0, "clean_shutdown": true, "gpu_utilization_percent": 0, "gpu_free_mib": 15356, "gpu_used_mib": 695, "natural_oom_log_mention": false, "context": 32768, "start_attempts": 1}

Matched per-task raw token deltas, startup-inclusive wall and wait-adjusted wall are saved in summary.json. No percentage subscription-quota saving can be inferred. Actual quota impact remains unavailable.

## Limits

- Eight authored synthetic tasks, one repeat per arm: exploratory broader coverage, not comprehensive real-repository validation.
- Process startup cooldown and RAM-floor-0 deviation retained; default stays frontier-only.
- No observed natural OOM/prefill stall means natural recovery remains unverified.
- Bounded pressure cannot establish an optimal/safe RAM threshold without a controlled failure boundary.
- Subscription weighting and directly measured quota impact unavailable; token deltas are relative accounting.
- C2b skipped; categories fixed by task structure, not runtime-classifier validation.
- Direct trials run before server load; shadow/route pair order alternates; no randomized session replication.

Subscription CLI only; no paid provider API, routing promotion, code/default changes, commit, push or publication. Any usage-limit or runner exception stops the pilot and waits for the user. No automatic server restart.


## Manual resume completion - 2026-11-21

User-authorized continuation completed the nine unfinished keys; the original 15 completed rows were not rerun. **24/24 independently accepted**, direct 8/8, live shadow 8/8 and route 8/8. Route outcomes: 3 local-only passes, 4 local-attempt failures repaired by frontier and 1 frontier-only decision without a local attempt. Seven eligible live-shadow decisions have matched outcomes; the omitted/unknown category remains separate and no runtime-classifier validation or routing promotion is inferred. No completed trial timed out.

The original usage-limit stop and interrupted attempt are retained; its artifacts were archived with hashes before resuming that key. The resumed session used one new owned Edge0 launch with the same frozen sources/settings; original health diagnostics were retained without repetition. This introduces session/startup/order confounding and does not create an independent replication. Natural OOM/prefill recovery and actual subscription-quota impact remain unverified; no quota percentage or general speed/quality claim is made. CPU health feasibility and eight synthetic contract tasks are the disclosed scope.

Final owned-server shutdown was clean at **07:10:29 Manila**: zero Edge0 processes, 695 MiB GPU/0%. Independent Windows/WSL model-process check at **07:15:35** was empty, GPU 714 MiB/0%. The 08:00 watchdog/deadline was not reached. No user :1234/:1235 stack was touched or PC power-off issued. No automatic retry, paid API, C2b, teacher/training/scorer, E42/E43 restart, routing/default change, research-repository commit or push occurred during the run itself; the evidence was released afterwards (2026-11-21). Selected public evidence only.


