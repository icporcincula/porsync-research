> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E47 exploratory pilot — 2026-11-24

**Local evidence draft; publication held.**

**The pristine release failed the matched-thinking assumption and did not preserve observed accuracy (4/12 versus 11/12). No controlled speed-win claim is supported.** The separate `strata-sq15-thinking` arm is a post-outcome diagnostic with a locally adapted Python serving policy, on the same spent pool; it never replaces the original release observations.

| Arm | Correct | Wilson 95% | Request seconds | Correct/hour | Length stops | Errors |
|---|---:|---|---:|---:|---:|---:|
| llama-iq3 | 11/12 | 64.6–98.5% | 136.19 | 290.8 | 1 | 0 |
| strata-sq15 | 4/12 | 13.8–60.9% | 9.35 | 1540.2 | 0 | 0 |
| strata-sq15-thinking | 12/12 | 75.8–100.0% | 88.43 | 488.5 | 0 | 0 |

All arms: 8,192 context, one slot, temperature 1.0, top-p 1.0, 1,024 completion tokens, 120-second request timeout and 900-second arm budget. Only final content is judged by exact JSON object equality, allowing one enclosing JSON fence; length finishes fail even if the visible JSON matches. Two consecutive request errors stop an arm. One separate arithmetic warmup precedes each arm. Correct/hour uses summed client request duration, including failures, and excludes downloads, load, warmup and shutdown. Acquisition finished before inference. Timing includes prompt caching as configured by each engine; no cache-equivalence claim. These throughput figures are arithmetic descriptions of the tested configurations, not an engine-only comparison.

Release-bundle inspection and an offline policy check establish that `inkling_dialect.template_kwargs` always sets effort none, and `finish_prompt` appends a direct-answer opener. Original SQ-15 replies have no reasoning field and only 17–34 completion tokens per scored item; the baseline reasons and one item exhausts the 1024-token cap with no final answer. This is a prompt-policy confound, not evidence that SQ-15 quantization caused the accuracy drop. The diagnostic adapter uses effort 0.9 (the shared template default), removes the forced answer opener and disables generic answer-room reservation. It changes no engine/weight/task/cap and was frozen before its first request, after observing the original outcomes. Remaining confounds: one order, new stochastic samples, different quants, DSpark, anti-loop and sampling implementations (the serving sampler limits candidate width), and caching. Diagnostic recovery can support a mechanism hypothesis, not prove causation or general accuracy equivalence.

The original SQ-15 engine log reports 2773 experts in VRAM and 299 on host (`hyb=1`), with global KV automatically mapped to 256 MiB of host RAM at 8192 context. Thus SQ-15 ran successfully but was **hybrid, not fully GPU resident**, on this configuration. This scopes the model-card full-residency claim; do not generalize it to other hardware/settings.

RTX 5060 Ti (16,311 MiB reported by nvidia-smi), driver 610.88; Windows WDDM; existing Python 3.12.7 and installed Python packages. Release Control and dedicated Inkling engine 0.1.66, v0.2.20, source build 2e87c08db18a. The bundled release Python 3.12.15 was not used. llama.cpp uses the E44 b50-8d60873 build and pinned Mainline_Support IQ3_XXS. SQ-15 includes DSpark on; the llama.cpp arm has no drafter. No vision file.

This is a 12-item exploratory synthetic structured-task pilot (three each inventory arithmetic, deduplication, scheduling and aggregation), one stochastic attempt per item. No coding, tools, agent harness, long-context or broad quality claim. The same fixed order ran on llama.cpp first and SQ-15 second, with no counterbalance or repeat. Accuracy intervals are descriptive and broad; equal observed accuracy would not establish equivalence. Model, quantization, engine and drafter are bundled differences. These fixtures are now spent.

Resource samples include startup, warmup and scored work (about two-second sampling; peaks can be missed):

```json
{
  "llama-iq3": {
    "sample_count": 73,
    "peak_gpu_used_mib": 12948.0,
    "minimum_ram_available_gib": 0.6783790588378906,
    "peak_swap_used_gib": 0.8929862976074219
  },
  "strata-sq15": {
    "sample_count": 10,
    "peak_gpu_used_mib": 15032.0,
    "minimum_ram_available_gib": 10.679546356201172,
    "peak_swap_used_gib": 0.8496971130371094
  },
  "strata-sq15-thinking": {
    "sample_count": 55,
    "peak_gpu_used_mib": 15032.0,
    "minimum_ram_available_gib": 10.55722427368164,
    "peak_swap_used_gib": 0.8425865173339844
  }
}
```

Credits: Thinking Machines Lab (Inkling 2 Mini), Niko1221 and contributors (Niko1221's Strata engine), and the llama.cpp authors. Upstream engine MIT; model Apache 2.0 with its acceptable-use policy. Weights and binaries are not redistributed.

The unchanged release parser discards thinking-channel text, including in the adapted diagnostic. Saved API responses therefore do not expose its hidden reasoning; increased completion counts and the verified prompt-policy change support the mechanism interpretation, without an independent raw-thought audit. Next step, if authorized later: a fresh harder pool, matched prompt/sampling policies, counterbalanced repeats and an adequate frozen completion cap. No promotion follows this pilot.

Verification: the HTTP/scoring mock check passed, original arm/fixture hashes stayed unchanged, the portable analyzer reproduced all 36 selected rows and metrics, and all eight selected evidence/index/release hashes match. Full verification of the existing public checkout fails at the unrelated `docs/patchsmith/blind2-2026-11-19/README.md` manifest entry; that file and its manifest entry were not changed. No full-repository verification or publication completion is claimed. Final GPU observation: 319 MiB used, 0% utilization; no owned llama-server or dedicated Inkling engine remains.

Private execution record: `tmp/e47/`; frozen protocol and fixture hashes, launch commands, raw responses, engine logs and telemetry are retained there. Plan and freeze (private source reference withheld). Scripts: `scripts/e47_pilot.py`, `e47_server_run.py`, `e47_analyze.py`, `e47_offline_check.py`. Only owned test servers were launched and stopped. No frontier call, API spend, commit, push, site change or deployment. Selected evidence is prepared locally in `tmp/porsync-research/docs/small-evals/e47-pilot-2026-11-24`; publication remains outstanding.

Source-versioning addendum: the user authorized private commit/push after collection. Selected versioned data and offline analysis (private source reference withheld) preserve the original collection report and provenance hashes. Public publication remains held.
