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
