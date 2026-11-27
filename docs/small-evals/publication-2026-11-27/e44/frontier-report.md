> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E44 companion: frontier heldout3 results

Status: **complete**; 48/48 trials recorded. Updated 2026-11-23T05:03:47.005025+00:00. Publication held; companion source authorized for local commit.

Frozen design: protocol (private source reference withheld). Eight fixtures n17â€“n24; two CLI aliases; three repeats per cell. No pooling with the n01â€“n16 tuning pilot. The actual local launch script is `[withheld local path]` (underscore).

Commands: `python -B scripts/e44_frontier_heldout3.py --dry`; smoke `python -B scripts/e44_frontier_heldout3.py --only heldout3-n17_cron-haiku-0`; background `python -B scripts/e44_frontier_heldout3.py` (stdout `tmp/e44-frontier-heldout3-2026-11/run.out`, stderr `run.err`). Resume the same runner command after user quota reset/authorization. Offline refresh: `python -B scripts/e44_frontier_heldout3_summary.py`.

Raw plan, baseline checks, CLI JSON, tests, patches, row sidecars, hashes and missing-key list remain in `tmp/e44-frontier-heldout3-2026-11/`. Summary verifies saved artifact hashes. No public repository edits or pushes; companion source authorized for local commit. GPU/server and local processes were untouched.

| Model | Green/completed/planned | CP 95% | Median s | Q1â€“Q3 s (IQR) | Mean turns | Input/create/read/output | Timeouts/errors/protected |
|---|---|---|---|---|---|---|---|
| sonnet | 24/24/24 | 85.8%â€“100.0% | 19.46 | 17.16â€“22.07 (4.91) | 4.96 | 190 / 636176 / 2638495 / 27069 | 0/0/0 |
| haiku | 24/24/24 | 85.8%â€“100.0% | 34.75 | 31.70â€“39.86 (8.15) | 9.17 | 318 / 805217 / 6285437 / 104966 | 0/0/0 |

Times exclude nulls, quartiles use inclusive interpolation; IQR is undefined for fewer than two observations. CP attempt intervals are descriptive; attempts cluster by fixture. Token totals are not quota percentages.

| Fixture | Sonnet | Haiku | Inkling Aider | Inkling v5b |
|---|---|---|---|---|
| n17_cron | 3/3 | 3/3 | 0/3 | 2/3 |
| n18_money | 3/3 | 3/3 | 0/3 | 2/3 |
| n19_pq | 3/3 | 3/3 | 3/3 | 3/3 |
| n20_slug | 3/3 | 3/3 | 1/3 | 3/3 |
| n21_duration | 3/3 | 3/3 | 0/3 | 2/3 |
| n22_matrix | 3/3 | 3/3 | 3/3 | 3/3 |
| n23_intervals | 3/3 | 3/3 | 3/3 | 3/3 |
| n24_ini | 3/3 | 3/3 | 0/3 | 3/3 |

Local counts come exclusively from saved rows, never logs; source snapshot hashes are in paired.json. Incomplete cells remain missing.

- sonnet vs aider: 5 wins / 0 losses / 3 ties across 8/8 complete paired fixtures; exact sign p=0.0625 (descriptive).
- sonnet vs v5b: 3 wins / 0 losses / 5 ties across 8/8 complete paired fixtures; exact sign p=0.25 (descriptive).
- haiku vs aider: 5 wins / 0 losses / 3 ties across 8/8 complete paired fixtures; exact sign p=0.0625 (descriptive).
- haiku vs v5b: 3 wins / 0 losses / 5 ties across 8/8 complete paired fixtures; exact sign p=0.25 (descriptive).

Smoke inspected before batch launch: {   "key": "heldout3-n17_cron-haiku-0",   "green": true,   "seconds": 30.031,   "turns": 6,   "resolved_models": [     "claude-haiku-5-5"   ],   "inspected": [     "claude.json",     "tests.txt",     "patch.diff"   ],   "tests_passed": 3,   "production_files_changed": [     "cronfield.py",     "service.py"   ],   "protected_files_changed": [] } .

Dry gate: 8/8 failing baselines verified with discovered tests and no reference files copied.

Resolved IDs: {"sonnet": ["claude-haiku-5-5", "claude-sonnet-5-5"], "haiku": ["claude-haiku-5-5"]}. Missing usage rows: {"sonnet": 0, "haiku": 0}.

Incidents: []. Missing frontier trials: 0. Full keys are in summary.json. The mandated Haiku n17 smoke precedes the repeat-major batch; no other order changes. No defective fixture has been identified.

Caveats: different harnesses/prompts (direct CLI versus Patchsmith/Aider); n=3 per cell, so 3/3 only bounds a pass rate to about 29â€“100%; n=8 fixtures is descriptive only. User-level Claude Code configuration was loaded as in earlier cohorts. This is outcome evidence, not a routing promotion. Pilot tuning data are not pooled. A crash is retried once with first artifacts retained; timeouts and other results count. Usage stops await the user, never loop. No deadline or edge0-wait logic. Public evidence synchronization is deferred by the explicit E44 publication hold; no public files prepared or edited.

Final provenance check: the nested patchsmith-audit HEAD advanced from 2203eb0701265695511f2a4077d142b01aeee464 at launch to 58b164207be0730f703e98880d1a939b09c71441 by final inspection (commit: E44 held-out set 3 fixtures/references and PS_COMPLETION_CAP override). This companion made no commits. The frozen runner, protocol, task JSON and all eight fixture directory hashes still match plan.json; all saved artifact hashes verify. The timing of the external HEAD change was not recorded.
