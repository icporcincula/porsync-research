# Phase B: plugin accounting

## Publication update - 2026-11-19

User-authorized selected evidence release. Historical local-only/hold and pending-verification statements below describe preparation time and are superseded by this dated update.

E39 items 1 and 2 remain open: broader plugin-path accounting and actual subscription quota impact, and sufficient host/shadow integration evidence on local-table decisions. Default remains frontier-only; no routing promotion is supported. RAM floor 0 was an authorized accounting deviation, not a recommended threshold or controlled RAM calibration. The cold-start `recent_http400` label came from a synthetic in-memory cooldown initialized at process start, not a real HTTP 400. The retry observed the original five-minute cooldown in the same MCP process.

B0 passed 21/21; B1 passed 36/36 with no local attempts. B1-minus-B0 fixture-balanced mean median overhead was +99,410.5 cache-read tokens, -4,040.9 cache-write tokens, +547.8 output tokens and +13.094 seconds. B2 retry passed 15/15 final independent checks: 13 local successes and two local failures repaired by frontier. One earlier quota-interrupted attempt is archived and excluded, including after its key was rerun. Original B2 smoke/skip and the retry are separate cohorts.

B2-retry-minus-B1 fixture-balanced mean median deltas were -67,376.1 cache-read, -1,186.8 cache-write and -129.3 output tokens, but +306.625 seconds including cooldown and +6.113 seconds after subtracting observed waits. There is no speed win and no promotion conclusion. Fixed CLI context (~25k cache-write and ~92-135k cache-read versus 250-500 task output tokens) can dominate apparent savings. Unweighted token arithmetic is not subscription quota weighting, billed spend or a causal estimate.

E41 blind2 contains 288 saved attempts, separate from n01-n08, tuning, replay and frontier cohorts. Edge0 v5b is not blind; it and the gpt-oss recovery were tuned after earlier failures. The new tasks were held out from that observed tuning, which does not make the intervention blind. Cohorts are never pooled. v6 changes both the completion cap and read-tool policy; unequal budgets and cross-model quant/backend differences prevent a general harness ranking.

Only curated aggregates, outcome/usage rows, configuration, source hashes and offline analysis are released. Private implementation, fixture source, reference solutions (including heldout2_references.json), prompts, patches, transcripts, raw test output and personal paths remain withheld. Counts can be recomputed; generated code cannot be independently rescored from this release. No model runs or API spend were performed for publication.

## Historical run and analysis record

Local unpublished record; subscription only. Updated 2026-11-19T09:16:03.253079+00:00.

- B0: **complete**; 21/21 completed, 21 independently accepted, 0 local attempts.
- B1: **complete**; 36/36 completed, 36 independently accepted, 0 local attempts.
- B2: **skipped: B2 smoke never reached a local attempt: recent_http400**; 1/15 completed, 1 independently accepted, 0 local attempts.

B0 was retained without rerunning. E39 items 1 and 2 remain open beyond this narrow accounting/integration sample. Default stays **frontier-only**. These tiny synthetic fixtures are not held out and support **no routing-promotion conclusion**. Subscription quota weighting is unpublished: tokens are relative accounting, not plan percentages.

## Frozen conditions and commands

Source repo tmp/patchsmith-audit is read-only at 0e4f1424de66e60ad0e9189a6bada789a081ba71. Plans contain directory SHA-256, category-table hash, CLI version, runner hash and task text. Only fixture directories copied; no reference solutions. Sonnet, 600 s timeout, acceptEdits, no session persistence, provider/API environment stripped. JavaScript uses node --test; Python uses python -B -m unittest discover -q. Protected files restored before verification; edits reject acceptance. Per-trial strict MCP config launches codex_mcp.py using Python -B, with isolated psdata. Claude Code has no MCP proposal-apply tool; its documented path is saved hash/base verification, git apply --check then git apply via Bash. No API path added.

Frozen prompt wording is withheld; SHA-256 is included in config.json. The private record retains exact wording.

Commands: python -B scripts/e39_plugin_accounting.py --arm B1 --dry; --arm B2 --dry (freezes both plans); B1 smoke --arm B1 --only B1-bug1-sonnet-0; full/resume --arm B1; B2 smoke --arm B2 --only B2-bug1-sonnet-0; full/resume --arm B2 only if a local attempt actually ran. Summary: python -B scripts/e39_plugin_accounting_summary.py. All CLI starts guarded by Dec 10 Manila deadline and live edge0 process + /v1/models health. Usage stop exits 3; rerun same command skips completed keys. Runner exceptions stop and are reported.

Edge0 launch: powershell -NoProfile -File <private Edge0 launcher> 32768, one attempt only. Startup/cleanup and RAM samples are saved privately under operations/. No lower context or startup retry.

## RAM-floor deviation / calibration observation

B1/B2 set PS_ROUTER_RAM_FLOOR_BYTES=0, as explicitly authorized. This is an accounting/integration deviation, not a recommended default or a completed controlled health calibration. The default-floor probe documents actual health-gate behavior; the user requested it be recorded as a calibration result. It must not be interpreted as validating a RAM threshold. All cooldown/clean-window defaults remain unchanged.

```json
{
  "reason": "recent_http400",
  "decision": "frontier",
  "free_ram_bytes": 646610944,
  "default_floor_bytes": 2147483648,
  "override_present": false
}
```

## Accepted tasks: median [IQR]

| Arm | Fixture | Accepted/completed | Input | Cache create | Cache read | Output | Turns | Seconds |
|---|---|---|---|---|---|---|---|---|
| B0 | bug1 | 3/3 | 8.00 [0.00] | 26204.00 [6.00] | 94065.00 [6.50] | 409.00 [3.00] | 4.00 [0.00] | 16.42 [4.88] |
| B0 | bug2 | 3/3 | 10.00 [0.00] | 26356.00 [22.00] | 134972.00 [13.50] | 508.00 [22.00] | 5.00 [0.00] | 18.28 [1.23] |
| B0 | feature | 3/3 | 8.00 [2.00] | 26255.00 [171.00] | 94165.00 [41359.00] | 398.00 [79.00] | 4.00 [1.00] | 16.72 [1.81] |
| B0 | multifile | 3/3 | 6.00 [0.00] | 23979.00 [75.00] | 91901.00 [17.50] | 294.00 [1.00] | 3.00 [0.00] | 13.17 [0.49] |
| B0 | refactor | 3/3 | 6.00 [0.00] | 23690.00 [8.50] | 91876.00 [5.00] | 244.00 [5.50] | 3.00 [0.00] | 12.22 [0.31] |
| B0 | offbyone | 3/3 | 8.00 [3.00] | 26348.00 [1471.50] | 94250.00 [41427.00] | 475.00 [156.50] | 5.00 [1.50] | 14.95 [2.53] |
| B0 | javascript | 3/3 | 6.00 [0.00] | 23947.00 [16.50] | 91740.00 [6.00] | 373.00 [11.00] | 4.00 [0.00] | 14.80 [0.20] |
| B1 | bug1 | 6/6 | 16.00 [0.00] | 21682.00 [13.25] | 186680.50 [39.25] | 838.50 [15.50] | 7.00 [0.00] | 28.05 [4.29] |
| B1 | bug2 | 3/3 | 18.00 [1.00] | 21847.00 [114.50] | 223071.00 [2130.50] | 1001.00 [77.00] | 8.00 [0.00] | 28.27 [2.59] |
| B1 | feature | 6/6 | 16.00 [0.00] | 21887.50 [51.50] | 185006.00 [60.50] | 930.00 [43.50] | 7.00 [0.00] | 27.59 [3.22] |
| B1 | multifile | 6/6 | 18.00 [1.50] | 22251.00 [42.50] | 224651.00 [27665.00] | 1150.00 [55.75] | 9.00 [0.00] | 31.51 [1.09] |
| B1 | refactor | 3/3 | 14.00 [2.00] | 19309.00 [1495.50] | 182430.00 [19889.00] | 757.00 [248.50] | 6.00 [1.50] | 24.80 [4.80] |
| B1 | offbyone | 6/6 | 17.00 [2.00] | 21958.50 [308.00] | 204559.00 [39558.50] | 962.50 [214.25] | 8.00 [2.00] | 30.30 [12.44] |
| B1 | javascript | 6/6 | 14.00 [0.00] | 19558.00 [5.75] | 182445.00 [42.75] | 896.50 [48.25] | 7.00 [0.00] | 27.70 [1.68] |
| B2 | bug1 | 1/1 | 20.00 [-] | 22018.00 [-] | 260121.00 [-] | 1106.00 [-] | 9.00 [-] | 34.44 [-] |
| B2 | feature | 0/0 | - | - | - | - | - | - |
| B2 | multifile | 0/0 | - | - | - | - | - | - |
| B2 | offbyone | 0/0 | - | - | - | - | - | - |
| B2 | javascript | 0/0 | - | - | - | - | - | - |

Inclusive quartiles, IQR=Q3-Q1. Accepted independent tests only; missing fields excluded, never zero-filled. Each cell is a separate fixture; pooled totals would overweight B1 local-table fixtures.

## B1 minus B0 overhead; B2 minus B1 host tokens added (negative = saved)

Differences of per-fixture accepted medians, not paired trials or subscription percentages. B2 comparisons without local attempts do not measure local savings.

| Comparison | Fixture | Input | Cache create | Cache read | Output | Turns | Seconds | Local attempts |
|---|---|---|---|---|---|---|---|---|
| B1 - B0 | bug1 | +8.00 | -4522.00 | +92615.50 | +429.50 | +3.00 | +11.63 | 0 |
| B1 - B0 | bug2 | +8.00 | -4509.00 | +88099.00 | +493.00 | +3.00 | +9.98 | 0 |
| B1 - B0 | feature | +8.00 | -4367.50 | +90841.00 | +532.00 | +3.00 | +10.88 | 0 |
| B1 - B0 | multifile | +12.00 | -1728.00 | +132750.00 | +856.00 | +6.00 | +18.34 | 0 |
| B1 - B0 | refactor | +8.00 | -4381.00 | +90554.00 | +513.00 | +3.00 | +12.58 | 0 |
| B1 - B0 | offbyone | +9.00 | -4389.50 | +110309.00 | +487.50 | +3.00 | +15.35 | 0 |
| B1 - B0 | javascript | +8.00 | -4389.00 | +90705.00 | +523.50 | +3.00 | +12.90 | 0 |
| B2 - B1 | bug1 | +4.00 | +336.00 | +73440.50 | +267.50 | +2.00 | +6.38 | 0 |
| B2 - B1 | feature | - | - | - | - | - | - | 0 |
| B2 - B1 | multifile | - | - | - | - | - | - | 0 |
| B2 - B1 | offbyone | - | - | - | - | - | - | 0 |
| B2 - B1 | javascript | - | - | - | - | - | - | 0 |

Fixture-balanced B1-minus-B0 mean of per-fixture median differences (7 fixtures when complete): {"input_tokens": 8.714285714285714, "cache_creation_input_tokens": -4040.8571428571427, "cache_read_input_tokens": 99410.5, "output_tokens": 547.7857142857143, "turns": 3.4285714285714284, "secs": 13.093714285714286}. These are descriptive values, not paired differences or quota weights.


## Real shadow reports and outcome agreement

Host outcomes: 36/36; pass/fail disagreement vs independent acceptance: 0/36; turn-count disagreement: 36/36. Host turns are requested so far, whereas CLI turns cover the completed session; these scopes differ and unequal counts alone are not false outcome reports. Host seconds exceed the entire runner wall time in 36/36 reports; these are unreliable elapsed measurements. Host turns/seconds are self-reported, not automatically trusted. The second report replaces pass, turns and seconds with independent CLI/runner measurements for existing outcomes only; missing outcomes are not fabricated.

Unique task IDs checked before merging. Default-floor probe excluded from arm rows. Commands run separately: python -B tmp/patchsmith-audit/eval/shadow_report.py tmp/e39-plugin-accounting-2026-11/B1-merged-host.jsonl; same with B1-merged-verified.jsonl.

```json
{
  "host": {
    "local_completed": 0,
    "local_pending": 0,
    "local_disagreements": 0,
    "local_disagreement_rate": null,
    "frontier_completed": 36,
    "frontier_easy": 36,
    "frontier_easy_rate": 1.0,
    "orphan_outcomes": 0,
    "promotion_bar": 0.1,
    "struggle_turns": 10,
    "below_bar": false,
    "note": "Descriptive proxy only: frontier success does not establish local correctness. No automatic promotion."
  },
  "verified": {
    "local_completed": 0,
    "local_pending": 0,
    "local_disagreements": 0,
    "local_disagreement_rate": null,
    "frontier_completed": 36,
    "frontier_easy": 36,
    "frontier_easy_rate": 1.0,
    "orphan_outcomes": 0,
    "promotion_bar": 0.1,
    "struggle_turns": 10,
    "below_bar": false,
    "note": "Descriptive proxy only: frontier success does not establish local correctness. No automatic promotion."
  }
}
```

Fewer than 30 local-table decisions with outcomes means the intended below-10% bar cannot be assessed. Even a descriptive below_bar=true would not establish local correctness or justify promotion. Cold-start recent_http400 gates are integration observations, not local-table accuracy observations.

## Incidents, exclusions and limits

B0: timeouts=0, CLI errors=0, protected violations=0, missing usage=0, permission denials=0; rejected=[]; stops=[]; decision reasons={}.

B1: timeouts=0, CLI errors=0, protected violations=0, missing usage=0, permission denials=5; rejected=[]; stops=[]; decision reasons={'recent_http400': 36}.

B2: timeouts=0, CLI errors=0, protected violations=0, missing usage=0, permission denials=2; rejected=[]; stops=[]; decision reasons={'recent_http400': 1}.

2026-11-19: No leftover Edge0/llama-server or blind batch process at launch; blind2 log ended 2c DONE. Edge0 launched once at ctx 32768 (owned server); startup succeeded. Free RAM fell from 24.37 GiB to approximately 0.3-0.8 GiB. No retry or context reduction. Default-floor probe was gated by recent_http400 before RAM; free RAM 646,610,944 bytes at the probe. No health windows altered. B0 21/21 retained without rerun. Both B1/B2 plan hashes and prompt wording frozen before B1 smoke.

Offline audit initially assumed no permission denials and stopped on an assertion (not a runner exception; no trial restarted). B1-bug1-sonnet-1 attempted PowerShell, which is outside the frozen allowedTools list, and was denied. It continued through the allowed tools and independently passed. Denials are retained and counted; no permissions broadened and no prompt/runner changed.

B1 complete: 36/36 independently accepted; 36 decision/outcome pairs, all frontier/recent_http400; no local generation. Five permission denials across B1 recovered through allowed paths. Host pass reports agree 36/36, but all 36 elapsed reports exceed runner wall time, and reported pre-completion turns differ from final CLI totals. Both shadow reports have 0 eligible local observations and null local disagreement rates.

B2 bug1 repeat-0 smoke independently passed in the frontier host, but route mode returned recent_http400 before any transcript/partial diff. Local-attempt smoke criterion FAILED: 0 local attempts. Remaining 14 B2 trials skipped as instructed; no cooldown change, waiting workaround, retry, or fake local result. B2 had two recovered permission denials. One CLI smoke is included descriptively, excluded from claims about tasks handled locally. No local token savings estimate exists.

Edge0 stopped cleanly after the B2 smoke via CTRL_BREAK_EVENT sent only after console-process ownership was verified. Server logs show stopping acceptance, active requests finished, [strata] stopped, and edge0-strata exit code 0. Launcher, edge0-infer and both owned Python children exited; no Edge0/llama-server process remained. GPU usage returned to 484 MiB / 0% utilization; free RAM 28,613,836 KiB. No force kill, restart or unrelated process stop. The same single server remained up between B1 and B2 to avoid another RAM-heavy startup; it was stopped immediately after the terminal B2 smoke.

Final offline validation: integration audit verified exactly one implement_task invocation in each of the 37 new CLI trials, matching fixture/task text and captured usage; B1 has exactly one matching decision/outcome pair per trial. All saved artifact hashes and frozen runner/plan hashes matched. Selected public-draft accounting recomputation passed for B0/B1/B2; eight changed public report/data/index files passed the credential/personal-path scan. Full public manifest verification has exactly one mismatch, the pre-existing unrelated E41 harness-comparison README. Private Patchsmith source remains clean at 0e4f1424de66e60ad0e9189a6bada789a081ba71. No commit, push or publication.


Usage is the top-level CLI bundle; modelUsage is retained separately and may include auxiliary Haiku usage. CLI list-price cost is not subscription spend. No pooling with Phase A/E41, no held-out routing claim, no site edits, commit, push or publication. Raw prompts/transcripts/patches and fixture/private implementation source remain private. Selected aggregate draft supports accounting recomputation only, not independent re-scoring. The pre-existing unrelated E41 public README hash mismatch is not repaired or claimed clean.


## Separate B2 retry (2026-11-19)

[Completed retry](../e39-phase-b2-retry-2026-11-19/README.md): 15/15 accepted, 13 local successes and 2 frontier repairs. Original B0/B1/B2 retained and not pooled. Historical E41 manifest mismatch noted above was corrected during the later offline cleanup.
