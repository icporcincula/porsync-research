> Selected publication authorized 2026-11-27. Only this curated package is released; private tasks, hidden tests, references, planner brief text, model replies, patches, transcripts, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish correctness. E39 follow-ups remain open.

# E58: Does a frontier planner brief lift Bonsai through Patchsmith?

**Result: no detectable pass-rate effect for either planner.** Bonsai 2.5 implemented 32 authored tasks through frozen Patchsmith v5 under three arms: task text only (A), a claude-sonnet-5-5 brief plus the task (P1), and a gpt-6.1-sol brief plus the task (P2). All six scored blocks completed. No Patchsmith edit, router change or production change was made.

## Design

- Same model, harness (v5), limits (32,768 context, 24,000 input budget, 25 turns, 900 s per task) and scoring as E57. Briefs travel inside the task text, wrapped as "Planning notes from a separate planning model. They may be wrong; the task statement and the tests decide." (`configuration.json`, field `wrapper`).
- Planners saw the task statement and visible files only, never hidden tests or Bonsai output, through the `claude` and `codex` CLIs with no tools (subscription, no paid API). One brief per task per planner, generated once, hash recorded, never regenerated. Rules: at most 550 words, no diff, at most two fenced blocks of six lines. A scan of all 144 files in the two brief directories found no diff or patch markers.
- Pool: large `x58-` pool of authored tasks. An unscored arm-A headroom screen (12 tasks) passed the pre-registered gate at 9/12 = 0.75. The 8 screened scored tasks were excluded; 32 scored tasks remain. Earlier pools were dropped for no headroom: Aider polyglot 10/10 and the first authored pool 12/12 on arm A, both unscored.
- Blocks in palindromic order, two repeats: b1 A r1, b2 P1 r1, b3 P2 r1, b4 P2 r2, b5 P1 r2, b6 A r2. Repeat 2 reverses task order.
- Briefs: gpt-6.1-sol accepted 32/32; claude-sonnet-5-5 accepted 20/32 and 12 exceeded the word cap on every attempt. Rejected briefs were not regenerated, so P1 ran the 20 tasks it briefed. P1 comparisons use those 20 tasks; P2-versus-P1 uses the 20-task intersection. The 12 dropped tasks are not a random sample.

## Results

Unit = task; per-task score = mean success over its two repeats. Paired task-cluster bootstrap, 10,000 resamples, both repeats kept together. Label `helps` only if the interval lower bound is above 0.

| Contrast | Tasks | Pass rate | Diff | 95% interval | Better / worse / tied | Label |
|---|---:|---|---:|---|---|---|
| P1 vs A | 20 | 0.900 → 0.950 | +0.050 | 0.000 to 0.125 | 2 / 0 / 18 | no_detectable_effect |
| P2 vs A | 32 | 0.812 → 0.891 | +0.078 | −0.016 to 0.188 | 5 / 2 / 25 | no_detectable_effect |
| P2 vs P1 (intersection) | 20 | 0.950 → 0.875 | −0.075 | −0.200 to 0.000 | 0 / 2 / 18 | no_detectable_effect |
| P2 vs A (same 20 tasks) | 20 | 0.900 → 0.875 | −0.025 | −0.100 to 0.050 | 1 / 2 / 17 | no_detectable_effect |

Attempt totals: A 52/64, P1 38/40, P2 57/64. P1 vs A is borderline: the lower bound is exactly 0 with two better tasks and none worse. P2's full-set gain (+0.078) disappears on the 20 tasks both planners briefed (−0.025), so it comes from tasks Sonnet did not brief. With 20 to 32 tasks only large effects were detectable.

Discordant tasks (A then planner, per-task mean of 2 repeats): P1 better on `x58-antibiotic-exact-viability-fractions` and `x58-meteorite-record-prototype-merge` (both 0.5 → 1.0). P2 better on antibiotic (0.5 → 1.0), aquarium-quarantine-transfers (0 → 1.0), origami-reservation-preview (0.5 → 1.0), planetarium-periodic-cue-timeline (0.5 → 1.0), racquet-stringing-batch-continuity (0 → 1.0); worse on meteorite (0.5 → 0.0) and taxidermy-absent-default-unification (1.0 → 0.5). Full lists are in `summary.json`.

Cost (Bonsai attempt seconds per verified task, planner time separate): A 96.9 s; P1 50.4 s plus 231 s of planner time once; P2 70.0 s plus 620 s once. The speed difference was not tested and P1 ran a subset, so it is descriptive. Planner token counts were not recorded; only wall seconds exist.

Validity: all attempts complete (A 64, P1 40, P2 64), 0 boundary violations, server-error rate 0 for all arms.

## Phase 2: Hermes delivery check (no performance claim)

Setup: Hermes v0.23.0 with the `patchsmith` plugin installed from a clean clone of the Patchsmith audit repository at commit 58b1642 (the working tree had uncommitted unrelated edits and was not used). The installed plugin's `register()` and `implement_task` / `apply_patch` handlers were called directly (`phase2/e58x_p2.py direct 5`) with the saved Sol brief plus task for the first five tasks both planners briefed, against the pinned Bonsai server, scored with the frozen hidden-suite acceptance. **Hermes' own language model choosing and calling the tool was not tested** (see Addendum A1).

Findings:

- `hermes plugins validate` fails: `compare_models`, `revise_proposal` and `task_preflight` are registered but missing from `provides_tools` in `plugin.yaml`. Install still works.
- The Hermes-facing path is the router, not the loop used in E58. `PS_ROUTER_MODE` accepts frontier-only (default), shadow or route; `off` is rejected. With defaults every call returns `frontier_required` and Bonsai is never used. Route mode forces propose mode, so the patch is applied by a separate `apply_patch` call, which worked.
- A cold process escalates (`health_recovering`, then `recent_http400`) until the router builds health history. `PS_ROUTER_CLEAN_MINUTES=0` and `PS_ROUTER_HTTP400_MINUTES=0` (documented overrides) were set for the final attempt. The three earlier attempts (rejected mode, `health_recovering`, `recent_http400`) never reached Bonsai and are retained in `phase2/`.
- All five tasks were given category `multifile`, a local category in the router table; the label was chosen for the check, not measured.
- Final attempt: 3 of 5 delivered through route plus `apply_patch` and passed the hidden suite; one (meteorite, which P2 also failed in the scored run) escalated with `loop_detected`; one escalated before any model call because free RAM was under the router's 2 GiB default floor. 0 boundary violations. The stock plugin client does not send the Bonsai sampler settings used in E58, so these outcomes and the 22 to 33 s timings are not comparable to the scored blocks.

## Addendum A1: Hermes 64K context requirement (opened 2026-11-27; Hermes-driven check run 2026-11-28)

Hermes v0.23.0 rejects any model with a context window under 64,000 tokens. The pinned Bonsai server serves 32,768 and its 24,000-token input budget is part of the frozen protocol, so the pinned server cannot drive Hermes; the first attempt failed in 14 s before any task. Phase 2 above therefore called the plugin handlers directly.

**Hermes-driven check (2026-11-28, delivery only, no performance claim).** Same pinned weights and sampler flags, started by hand with only `-c 65536` (an unfrozen deviation; 10.8 of 16.3 GB VRAM). Hermes, driven by that server, was asked to call `implement_task` (workdir, mode, task text with the saved Sol brief) on the first five tasks that both planners briefed, in route mode with the Phase 2 router overrides, scored by the frozen hidden suite. The plugin's own budget stayed at the frozen 24,000 input. Five attempts, all kept (`phase2/a1/attempt1-rows.json` to `attempt5-rows.json`; driver `phase2/a1/e58x_a1.py`):

| Attempt | Change | Outcome |
|---|---|---|
| 1 | No category passed | 5 of 5 tool calls correct; 0 delivered (`frontier_required`) |
| 2 | Instruction names `category: "multifile"` | 0 delivered; plugin still in `frontier-only` mode |
| 3 | `PS_*` settings written to Hermes' own `.env` | 4 of 5 ran locally, meteorite `loop_detected`; nothing applied (route mode is propose-only) |
| 4 | Instruction also asks for `apply_patch` | gravure and climbing delivered and passed; the three JS tasks did not |
| 5 | The three JS tasks rerun with `.env` values single-quoted | perfumery and mushroom delivered and passed; meteorite `loop_detected` |

Findings: (1) Hermes choosing and calling the tool is established for this plugin with a Bonsai driver at 64K: the correct tool and arguments on every attempt. (2) Hermes does not forward its process environment to plugins, so `PS_*` settings must be in Hermes' own `.env` (backed up and restored byte for byte each attempt). (3) Attempt 4's two JS failures were a configuration fault on my side, not the model: the double-quoted Windows test command was evidently mangled and the plugin ran `pytest` on JS tasks ("no tests ran"); single quoting fixed it. This cause is inferred from transcripts; the parsing step was not inspected. (4) Best configuration, composed from attempts 4 (two Python tasks) and 5 (three JS tasks): **4 of 5 delivered through Hermes and passed the hidden suite, 0 boundary violations**; meteorite looped in attempts 3 to 5, as in Phase 2 and the scored P2 run. Hermes time was 76 to 117 s per task with one 271 s outlier.

Not comparable to the scored blocks: the router, propose-then-apply path and stock client (no E58 sampler settings sent) differ from the measured loop, the server context differs, and five tasks with repeated attempts support only the statement that the path works, not a rate. The earlier sentence that Hermes driving the tool was not tested no longer applies; the A1 status is **run, delivery established, no performance claim**.

## Limits and what is not claimed

No claim about which planner is smarter, no router or promotion decision, no coding-ability claim beyond this pool, no effect on other models or pools, and no E39 resolution. The arms share a model and harness; only the added brief differs, and the brief text is part of the result but withheld here (hashes, word counts and timings are in `briefs-summary.json`). Pools and screens that were dropped are described above from private records; their rows are not released. The public record supports saved-label accounting and the bootstrap, not independent rescoring of code or inference reproduction. Reduced rows follow the E57 public schema; hidden-suite output tails, changed-file lists and timestamps are removed (`provenance.json` lists transformations and original-source hashes).

## Reproduce

`python analyze.py` in this directory reads only files here and rewrites `summary.json` byte-identically.
