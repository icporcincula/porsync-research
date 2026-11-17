# Porsync Research

Public evidence behind the experiments at [porsync.com/research](https://porsync.com/research).
These are small, hardware-constrained studies, with negative results, uncertain comparisons and unfinished work documented alongside the findings.

## Start here

| Study | Evidence |
| --- | --- |
| Contract extraction replication | [Report and model summaries](portfolio/small-evals/results/e03-replication/README.md) |
| Receipt arithmetic | [Report](docs/small-evals/e07-results.md) · [Summary](portfolio/small-evals/results/e07/summary.json) |
| Numeric table summaries | [Report](docs/small-evals/e08-results.md) · [Summary](portfolio/small-evals/results/e08/summary.json) |
| Numeric-check replications | [Report and summaries](portfolio/small-evals/results/e0708-replication/README.md) |
| Tool-use replication | [Report and comparisons](portfolio/small-evals/results/e09-replication/README.md) |
| Instruction-following replication | [Results](portfolio/small-evals/results/e13-replication/README.md) |
| Context-summary replication | [Results](portfolio/small-evals/results/e14-replication/README.md) |
| 120B model on 16 GB / coding reliability (E39) | [Interim report](docs/small-evals/e39-results.md) · [Local validation](docs/small-evals/e39-local-validation/README.md) |
| Patchsmith/Aider exploratory fixtures | [Report](docs/patchsmith/comparison-2026-11-16/README.md) · [159 trials](docs/patchsmith/comparison-2026-11-16/trials.json) |
| Expert-cache comparison (E40) | [Report](docs/small-evals/e40-results.md) · [150 trials](docs/small-evals/e40-data/trials/trials.csv) |

## Check the evidence

Python 3, standard library only; no model calls or GPU required:

```sh
python verify.py
python docs/patchsmith/comparison-2026-11-16/analyze.py
python docs/small-evals/e40-data/scripts/paired.py
python docs/small-evals/e40-data/scripts/timing_sum.py
```

The manifest records hashes and publication transformations. It establishes file identity, not independent certification of the experiments. Public Git history begins with this curated release; private development history is not included.

Read [RELEASE.md](RELEASE.md) before interpreting reproducibility or reusing files. Questions and methodological corrections are welcome as GitHub issues; identify the study, file and claim involved.

**E39 follow-up is planned:** frontier comparisons on harder and real-fix tasks, plugin token accounting, host/shadow checks, controlled RAM-health calibration, natural-fault recovery and held-out routing evaluation. The router remains frontier-only; successful local routed coding and promotion are not established. E40 does not close those gaps.

## CPU-only eval evidence — November 17 release

User-authorized release of selected CPU-only follow-ups:

- [E10 fault triggers](docs/small-evals/e10-triggers-2026-11-17.md) and [cached replay](docs/small-evals/e10-cached-replay-2026-11-17.md): six injected faults detected, 12 summaries and 6,315 answer/metric checks match. Independent gold validation and equivalent-mutant classification remain.
- [E21 partial Stage B](docs/small-evals/e21-results.md): 13/108 planned trials recorded, all code-containment checks pass; no dtype comparison. Selected synthetic trials and source hashes included.
- [E36 review preparation](docs/small-evals/e36-review-package-2026-11-17.md): blinded review tooling prepared for 200 frozen items; independent human labels remain pending. Website excerpts and predictions are excluded.

Method scripts require excluded private modules or data; they are not turnkey public reproductions. No model calls or GPU/service actions. Only selected reports, synthetic/aggregate observations and method scripts are released; private traces, source datasets and full private input manifests remain excluded. This authorization does not publish the separate E39 or Sprocket drafts. Historical hold wording in the reports is superseded by their dated authorization notes.
