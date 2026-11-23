# E43 incomplete adapter/harness compatibility pilot

Both smaller Q8 bases and separate F16 LoRAs loaded and served 32K context on the pinned b12600 runtime. **Full Stage A is incomplete; adapter benefit and transfer remain unmeasured.** The original Qwen3.8-27B configuration stopped for sustained WSL paging before readiness (one base load, no task probes or model requests); this is not proof that every 27B configuration is infeasible.

The smaller-model budget retained 16 launched attempts: 15 final-session probes plus one initial interrupted TwIL attempt. LFM3: eight final probes, five accepted passes, one functional failure, one bytecode-artifact exclusion despite a functional pass, and one compaction-blocked probe. TwIL: seven final-session accepted passes; adapter/OpenCode/development-task-2 was unstarted. The initial TwIL attempt produced at least 100 tokens according to server logs, with no completed-response usage. There were 176 completed model requests and one additional interrupted request attempt, not 177 completed responses. No final-session HTTP errors or returned reasoning fields/think markers were recorded; this does not prove internal reasoning absence.

Development covered only two of the four intended tasks. Missing ripgrep caused OpenCode search errors; one probe failed compaction. The saved LFM3/Patchsmith failure was a candidate arithmetic TypeError, reproduced independently on CPU; the syntax-only development check did not catch it. It remains failed. The original bytecode exclusion remains excluded under its original policy. These development counts are descriptive accounting, not model quality rankings or scored benchmark results. Runtime changed from the original Qwen attempt, so smaller size alone cannot explain compatibility.

Revision 3 fixes the isolated ripgrep dependency, disables automatic compaction for bounded trials, and records one exact inert CPython cache file symmetrically while grading only source in a clean namespace. Real OpenCode grep/glob/shell passed scripted CPU checks, including simulated high usage without compaction. This verifies plumbing, not real context exhaustion or model behavior. No new model trials ran. A fresh symmetric 32-attempt development matrix is designed, with 300-second caps and a four-hour operational budget; complete guarded execution/budget validation is still required at the next collection session.

Stage B is amended to separate conditional studies for both candidates: 24 fresh tasks × 3 repeats × 4 arms = 288 trials per candidate, maximum 576. Neither candidate is selected from development pass rate. The holdout and final execution/budget freeze remain incomplete; no scored launch or training has run. E39 follow-ups remain open and routing remains frontier-only.

## Evidence and reproduction

- `development-dispositions.json`: selected outcome/request accounting, including interrupted and unstarted entries.
- `configuration.json`, `sources.json`: saved settings and upstream identity metadata, not redistributed weights.
- `next-design.json`: prospective amended scope, CPU checks and launch prerequisites.
- `PROVENANCE.json`: withheld original hashes and disclosed transformations.
- `analyze.py`: portable standard-library accounting checks. Run `python -B analyze.py` from any directory; no model/network activity.

Raw prompts/responses, code, tasks, graders/references, logs, operational paths, weights and binaries are withheld. Independent code rescoring and inference reproduction are unavailable. Public saved-label accounting is reproducible. Upstream models retain their own license restrictions; this package redistributes no model assets. No website article accompanies this incomplete pilot.
