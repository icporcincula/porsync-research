> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E07 results — receipt arithmetic self-consistency

Completed locally 2026-11-08, after E08's runs and audit. Experiment record; site publication authorized 2026-11-08.
Article and social drafts are prepared; see the publication links below.

Four of 42 baseline extractions contradicted their own arithmetic. The only wrong
total was internally consistent, so the checker missed it. One re-ask fixed a line
amount in one flagged receipt; exact total accuracy stayed 41/42.

## Data and execution

- All 100 test annotations from [CORD v2](https://huggingface.co/datasets/naver-clova-ix/cord-v2),
  NAVER CLOVA / Park et al., CC BY 4.0. Public word annotations downloaded
  2026-11-08; exact annotation SHA and source metadata retained.
- **42 eligible, 58 excluded**, without hand-correcting gold to keep receipts:
  35 missing explicit subtotal, 9 discounts/unmodelled charges, 8 failing gold
  identities, and 6 missing or ambiguous required fields/amounts. Exact reasons
  in exclusion log (not included in this public release).
- Both gold identities must hold within 1 rupiah: sum of item **line amounts** =
  subtotal; subtotal + tax + service = total. Price is not unit price multiplied
  by quantity again. Missing quantities remain null in gold; absent charges are zero.
- Input text reconstructed from `valid_line` words, grouped by row ID and ordered
  by geometry. Category labels and `gt_parse` never enter the prompt. These are
  **human-transcribed annotated regions**, not an OCR-engine or image benchmark.
- The subset contains 100 top-level gold items; 80 have annotated quantities.
  Twenty receipts have one item; 26 have tax and 8 service charges. The selection
  favors simpler, explicitly self-consistent receipts and does not represent full CORD.
- Same pinned local Qwen3.5-9B Q4_K_M/server/GPU as E08; thinking off,
  temperature 0, seed 808, c=1, context 16,384, output cap 1,536. No JSON grammar,
  cleanup, hidden retries, automatic correction or external model service.
- One independent synthetic development gate (correct total and schema; item-name/
  quantity extraction was imperfect). Then 168 initial calls (42 × 4), plus four
  repair calls: **172 scored calls**, all finish reason `stop`, none `length`.
  Generation time 217.360 s (3.62 minutes), excluding setup, development and audit.

## Results

| Arm | Arithmetic contradictions | Invalid JSON/schema | Exact total | Exact subtotal | Macro item F1 |
|---|---:|---:|---:|---:|---:|
| X0A: baseline | 4/42 (9.52%) | 0/42 | 41/42 | 41/42 | 89.47% |
| X0B: identical-prompt repeat | 4/42 | 0/42 | 41/42 | 41/42 | 89.47% |
| X0C: identical-prompt repeat | 4/42 | 0/42 | 41/42 | 41/42 | 89.47% |
| X1: arithmetic instruction | 4/42 | 0/42 | 41/42 | 41/42 | 89.47% |
| X2: passive checker on X0A | 4/42 | 0/42 | 41/42 | 41/42 | 89.47% |
| X3: one re-ask on flagged X0A | 3/42 (7.14%) | 0/42 | 41/42 | 41/42 | 90.67% |

X2 never edits the output. X3 starts from exactly X0A. All raw text and parsed
outputs in repeats B/C match A on all 42 receipts: observed A/A floor 0/42 for each
repeat. X1 changes **one** parsed output: it corrects a tax/service swap in receipt
94. Primary endpoints stay unchanged; it is not identical in every field.

Item F1 uses exact multiset normalized name + line amount, averaged per receipt.
Exact name+amount+count matches among the 80 annotated-count gold items are 66
for baseline/X1 and 67 after repair. This joint match count is **not standalone
quantity accuracy**. Zero-price modifiers and shortened names can fail strict gold
matching despite being reasonable application outputs.

Post-hoc descriptive charge checks: baseline tax 38/42 and service 41/42 correct;
instruction-only tax 39/42 and service 42/42. Charge sums alone cannot detect swaps.
These were added in reporting, not substituted for frozen primary outcomes.

## What the checker caught and missed

All four baseline arithmetic flags are real violations of the declared output contract:

- Receipts 14 and 38 copy correct totals but omit printed PB1 tax (25,585 and
  60,394 respectively). Re-asks leave both unchanged.
- Receipt 41 merges duplicate item lines with count 2 but leaves each price as
  one copy's amount. Under the required full-line-amount contract, item prices sum
  to 255,411 instead of subtotal 316,017. Re-ask leaves it unchanged.
- Receipt 84 uses unit price 12,000 instead of line amount 24,000 for two Arem Arem.
  Re-ask fixes the line amount, clearing the contradiction and improving item F1.

**Wrong total missed: receipt 34.** The model multiplies already-complete amounts
75,000 and 10,000 by quantities 5 and 2, yielding subtotal 395,000, tax 39,500 and
total 434,500. These figures add up, but the printed/gold total is **93,500**.
It passes the identity check, so X3 never re-asks it. Thus wrong-total coverage is
0/1 and wrong-but-consistent share 1/1. These denominators are too small for a
general detection-rate claim. The four arithmetic flags all already had correct totals.

The instruction-only arm fixes receipt 94's tax/service assignment (12,733/8,330),
a change invisible to either sum. Its primary metrics remain identical to baseline.

## Hypotheses and uncertainty

| Hypothesis | Verdict |
|---|---|
| H1: baseline contradictions ≥10% | Refuted on the frozen threshold: 4/42 = 9.52%, narrowly below 10%; no broad low-error claim. |
| H2: instruction does not significantly reduce contradictions | No reduction observed: same four cases. This is not evidence of equivalence. |
| H3: identity check flags ≥60% of wrong totals | Refuted in this sample: 0/1. Very weak denominator. |
| H4: ≥20% of wrong totals are internally consistent | Met in this sample: 1/1; not a population estimate. |
| H5: re-ask has positive net exact-total accuracy | Refuted: zero total fixes, zero breakages. One line-item repair still succeeded. |

Paired 10,000-draw bootstrap, seed 0, yields 0-point difference and [0,0] sample
interval for both X1−X0A contradiction and X3−X0A total accuracy: every paired binary
endpoint is unchanged. These degenerate empirical intervals do not establish zero
population uncertainty or equivalence. Baseline repeated calls are not independent
receipts and are not pooled as n=126.

## Audit and validation

The agent manually reviewed all ten baseline/instruction error or charge-assignment
cases and all four re-asks. Decisions (not included in this public release)
distinguish genuine arithmetic failures from strict-name and modifier taxonomy
penalties. This is not an independent human audit. The scorer was not changed
after inference; charge metrics and notes are explicitly post-hoc reporting.

Protocol (not included in this public release),
[freeze](../../portfolio/small-evals/results/e07/run-v1/freeze.json),
[summary](../../portfolio/small-evals/results/e07/summary.json),
case traces (not included in this public release).

`e07_report.py` verifies source hashes, annotation hash, text/gold reconstruction,
the complete 42 × 4 grid, exact prompts, raw JSON and every stored primary score.
Twenty arithmetic/data tests pass, including three manually checked receipt fixtures
and a regression showing wrong-but-consistent totals escape the checker. Shared
pre-commit lint, frozen-format integrity, compile and all 62 E07/E08 tests pass.
Both owned local model servers stopped after their runs.

