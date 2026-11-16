> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E08 results — numeric membership in table summaries

Completed locally 2026-11-08, before E07 model calls. Experiment record; site publication authorized 2026-11-08.
Article and social drafts are prepared; see the publication links below.

The frozen numeric checker flagged 13/200 plain summaries and 6/200 instruction-only
summaries. These are **checker rejections, not measured factual-error rates**.
Manual review found 15/21 flagged numeric occurrences were supported approximations,
bounds or direct calculations that the allowed set omitted; two were ambiguous.
In a seeded sample of 50 passing summaries, 11 contained clear factual contradictions.

## Data and execution

- 200 five-year snapshots across 113 countries, coal/oil/gas CO2 in million tonnes.
- Public [OWID CO2 data](https://github.com/owid/co2-data), downloaded 2026-11-08;
  underlying [Global Carbon Budget / Global Carbon Project data](https://robbieandrew.github.io/GCB2025/), CC BY 4.0.
  Authors and source SHA retained in data manifest (not included in this public release).
- Up to two non-overlapping windows per country, years 1990–2023. Five development
  snapshots use countries excluded from test. Only 121 countries were eligible for
  the initial one-window design, so this sampling choice was made before inference.
- Values displayed to 3 decimals; cells, extrema, consecutive/end-to-end differences
  and percentage changes accepted at 0, 1 or 3 decimals. Calculations use displayed
  cells. Digit-based numeric extraction; years 1900–2100 excluded. Million-unit
  expressions normalized. Spelled-out numbers and semantic claims are not validated.
- Existing Qwen3.5-9B Q4_K_M, llama.cpp b11753-d8d92973c, RTX 5060 Ti 16 GB;
  thinking off, temperature 0, seed 808, c=1, context 16,384, output cap 1,536.
  Full model/server/DLL hashes, prompts, inputs and Python source frozen before inference.
- Five development calls; 406 scored model calls (400 initial + six re-asks).
  All 406 ended with `stop`, none with `length`. Scored generation time 925.841 s
  (15.43 minutes), excluding setup, development and audit time. No remote model API
  or subscription. Server stopped on completion.

## Results

| Arm | Summaries rejected by membership checker | Rejected numbers / extracted numbers | Whole-summary template fallbacks |
|---|---:|---:|---:|
| N0: plain prompt | 13/200 (6.5%) | 14/1,124 (1.25%) | 0 |
| N1: numbers-only instruction | 6/200 (3.0%) | 7/1,351 (0.52%) | 0 |
| N2: guard N1, immediate template | 0/200 | 0/1,338 | 6/200 (3.0%) |
| N3: guard N1, one re-ask then template | 0/200 | 0/1,340 | 3/200 (1.5%) |

N2 and N3 reuse the **same N1 first attempt**, rather than regenerating nominally
identical text. Zero membership failures after guarding follows from the guard and
template construction; it does not establish zero factual errors.

N1 minus N0 summary-flag rate: −3.5 percentage points, paired country-cluster
bootstrap 95% interval **−7.32 to 0.00 points** (10,000 draws, seed 0). The interval
includes zero. Arms were generated N0 then N1 within shuffled snapshots; there is
no separate E08 A/A repeat, so this is not a claim of general prompt superiority.

## Manual audit

The frozen sampling plan requested 50 flagged occurrences and 50 passing summaries.
Only 21 N0/N1 numeric occurrences were flagged, so **all 21** were reviewed, plus
the seeded 50 passing summaries (seed 1808). Review was performed by the agent
against the full tables, **not an independent human audit**. Occurrences can share
a summary or country; do not treat them as independent trials.

- **15 false flags, 4 legitimate flags, 2 uncertain approximate centers.** The
  observed false-flag fraction is at least 71.4%, or 81.0% if both uncertain cases
  count as false flags. This is a poor verifier-precision result.
- Examples: “more than 130 million” correctly describes 329.436 − 198.530 = 130.906;
  2.727 → approximately 2.73 is ordinary 2-decimal rounding; an unlisted upper bound
  such as “below 0.02” can be supported without matching any allowed value.
- **11/50 passing summaries had clear contradictions** involving direction,
  extrema, ranking, chronology, attribution or an unsupported numerical relation.
  Nine additional summaries overstated non-monotonic series with “steady” or
  “consistent” language; these looser judgements are reported separately.
- Example: a passing summary calls gas 182.887 the largest source, although oil
  is 207.743. Another says a quantity rose from 20.738 to 19.831. Every number can
  be in the table while the relation is false.
- A post-freeze reporting heuristic flagged 32 fuel/sentence direction pairs.
  Manual review confirmed 10 (31.25%). Most false flags assigned a verb to the
  wrong fuel or interval. This heuristic is exploratory, not a frozen treatment.

The audit categories are descriptive annotations made after reading outputs.
Approximate prose is subjective; two cases were left uncertain. No frozen scorer,
prompt, sample or stored output was changed to improve the result. The audit does
not estimate semantic error rates for all 800 arm outputs or prove the remaining
passing sample is error-free.

## Frozen hypotheses

| Hypothesis | Verdict on frozen operational endpoint |
|---|---|
| H1: N0 rejects ≥15% of summaries | Refuted: 6.5%; this does not imply factual errors are below 15%. |
| H2: N1 roughly halves rejection without reaching zero | Descriptively met: 6/13 = 46.2% of N0, within the pre-run ≤60% definition; paired interval includes zero. |
| H3: N2 fallback ≤20% | Met: 3.0%. |
| H4: N3 halves N2 fallback | Met exactly: 3 vs 6. |
| H5: verifier false-flag rate ≤10% | Refuted in agent audit: at least 15/21 (71.4%). |

## Artifacts and validation

Protocol (not included in this public release),
[frozen run](../../portfolio/small-evals/results/e08/run-v1/freeze.json),
[summary](../../portfolio/small-evals/results/e08/summary.json),
audit sample (not included in this public release),
manual decisions (not included in this public release).

`e08_report.py` checks frozen file hashes, the exact 200-ID grid, original prompts,
raw response text, every stored numeric score, and guard/fallback derivation.
42 numeric/parser tests and the shared lint, frozen-format integrity, compile and
test gates pass. Data source is a convenience public CSV, three related indicators
and one local model: no general claim about dashboard summaries or other models.

