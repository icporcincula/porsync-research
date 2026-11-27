> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E55 protocol (frozen on commit): OCRia-nano-1 vs Tesseract, independent CPU re-measurement on public receipts, forms and invoices (private)

Date: 2026-11-25. Status: prepared and frozen by hash before any scored run; no scored page has been parsed. Private: no push, no publication, no public-evidence sync, no router change. Draft and rationale: e55-ocria-nano-draft.md (private source reference withheld). CPU only; it must not overlap a timed GPU study (the runner refuses if `llama-server` or `strata` processes exist).

## Question

On 150 seeded public pages (50 receipts, 50 forms, 50 invoices) plus a 20-page synthetic degraded slice, on this machine's CPU, how does LiteParse with ocria-nano (arm B) compare with LiteParse with Tesseract (arm A, the vendor's own baseline) on key-field accuracy, word accuracy and wall-clock per page? Decision: is a CPU-only tiny parser a credible first pass in a local-first pipeline with escalation, and which document classes need escalation. No router change follows from any outcome. The vendor's ParseBench-2 score (59.2), 426 ms/page and 27.8 pages/s claims are not tested or reproduced here.

## Pins

- LiteParse npm `@llamaindex/liteparse` 2.21.2 (Apache-2.0), installed in `tmp/e55/lp` with `package-lock.json` hashed in the freeze file. Node v24.13.0, Windows 11, AMD Ryzen 5 7500F (6 cores / 12 threads). Python 3.12.7.
- ocria-nano 1.0.0 weights pulled with `lit models pull ocria-nano` (ONNX Runtime 1.31.1); sha256 of every model file is in `tmp/e55/freeze-hashes.json`. Arm A uses LiteParse's built-in Tesseract (not a separately installed Tesseract); its version is whatever the LiteParse 2.21.2 native build embeds and is not separately exposed.
- Arm A: `ocrBackend: tesseract`, dpi 150, `ocrLanguage` default (eng). Arm B: `ocrBackend: ocria-nano`, dpi 250. These are each backend's documented default; the dpi difference is a vendor-default confound and is disclosed. Both: `numWorkers: 1`, JSON output, one page per call.
- Licence (read 2026-11-25): the ocria-nano model licence is a modified Open RAIL-M. Its "Research Purposes" definition expressly includes evaluating or benchmarking the Model by any person, including publishing the results, and Attachment A exempts Research Purposes from the revenue, funding and Competing Service limits. This study is evaluation only: no product, service, distillation or derivative. Reconfirm before any public write-up; attribution to LlamaIndex with a link and the licence copy is required.

## Data

Seed 55 (`scripts/e55_sample.py`); everything under git-ignored `tmp/e55/`, nothing redistributed.

| Class | Source | Pages | Ground truth used | Terms |
|---|---|---:|---|---|
| receipt | `naver-clova-ix/cord-v2` test, seeded 50 of 100 | 50 | total, subtotal, tax amounts (fields present per page) and all labelled words | CC-BY-4.0 per the card |
| form | `nielsr/funsd` test, all 50 | 50 | words only | no licence on this re-upload; original FUNSD terms not confirmed; local scoring only |
| invoice | `Francisco-Cruz/InvoicesReceiptsPT`, seeded 50 of 1,003 | 50 | `total` and `nif_seller` | apache-2.0 tag; Portuguese phone photos |
| degraded | seeded 20 of the 150 pages above, transformed | 20 | the source page's labels | derived; synthetic degradation |

Warmup (unscored): 3 other CORD test pages. The degraded transform is frozen: Gaussian blur radius 1.2, rotation 1.5 degrees (sign seeded per page, white fill, expand), JPEG quality 35, saved at quality 92. Synthetic degradation is not real-world degradation.

Invoice label check (done 2026-11-25 by looking at the page images, before the freeze): 6 pages checked (of 12 pulled from the seeded order). Totals matched on 6 of 6. Seller NIF matched on 5 and was unreadable on 1 (faint print). One date label was wrong (label 02.02.19, page shows 02.01.19) and one `iva_amount` label had lost its decimal separator (299 for 2,99). Therefore `date` and `iva_amount` are dropped and only `total` and `nif_seller` are scored. This was a small spot check, not a full audit; remaining label errors are possible and affect both arms equally. Some CORD pages have no total or only a subtotal label; pages with no scorable field are excluded from that metric and counted.

Not covered: no table-structure ground truth. The vendor's headline strength (tables) is untested here; nothing is claimed about tables beyond invoice totals.

## Metrics (frozen)

All scoring is deterministic string matching in `scripts/e55_analyze.py`; an oracle control (labels fed in as parser text) scores 1.0 on every page.

1. **Field hit.** Amounts: the label's digit string equals the digit string of some numeric token in the output (separators ignored, whole-token match). NIF: the label's digits appear in the output, optionally split by single spaces, not inside a longer digit run. Page field recall = hits / labelled fields.
2. **Word F1.** Case-folded, edge-punctuation-stripped word multisets, labelled words versus output words. Receipts and forms.
3. **Primary metric per class.** receipt: field recall; invoice: field recall; form: word F1. Degraded pages use the source class's metric and are reported separately; they do not enter the decision.
4. **Consistent-triple recovery (receipts).** Among receipts whose labels have subtotal + tax = total, the share where the output contains all three values. Reported with its eligible count; not a decision input.
5. **Time per page.** Wall-clock around one `parse()` call, in one Node process holding both arms warm, after 3 unscored warmup pages, arm order alternated per page by the frozen seed (170 pages: 85 A-first, 85 B-first). Reported as median, mean, p90 per class, and the ratio of summed time B/A with a page-bootstrap 95% interval.
6. **Parse failure.** A thrown error or no output. Empty output scores zero (it stays in the denominator); an error rate above 10% for either arm makes the run `incomplete`.
7. **Escalation signature.** A page is flagged when the output has fewer than 10 words, or (receipts and invoices) no amount-like token. Reported per class per arm: flag rate, how many primary failures it catches, and how often it flags a page that was fine. Primary failure: field recall below 1 (receipt, invoice) or word F1 below 0.5 (form). Descriptive.
8. **Throughput supplement (never changes the decision).** 6 single-arm Node processes (one per physical core), pages sharded, wall time per arm. Includes process and model start-up, so it is a lower bound on steady-state pages per second.

## Reading rule (frozen)

Bootstrap: 10,000 resamples over pages within class, seed 55, 95% percentile intervals, paired B minus A. Noninferiority margin -0.10 (as in E54). A class is **uninformative** and excluded when both arms are at or above 0.98 or both at or below 0.02. Time check uses the clean classes (receipt, form, invoice).

- `incomplete`: any scored page or arm row missing, or an arm error rate above 10%.
- `credible_first_pass`: B is faster (upper bound of the summed-time ratio B/A below 1.0), and at least two classes are informative, and every informative class has a B-minus-A lower bound above -0.10.
- `faster_but_less_accurate`: B is faster and at least one informative class has a B-minus-A upper bound below 0 (B clearly worse).
- `not_better_than_baseline`: the lower bound of the time ratio is at least 1.0 (B not faster).
- `inconclusive`: anything else (for example B faster but an interval that straddles the margin).

With about 50 pages per class an `inconclusive` result is a live outcome, as E54 showed: a tie with an interval of about +/-0.1 cannot prove noninferiority at a -0.10 margin unless the per-page paired differences are small. Report that honestly rather than loosening the rule afterwards. Degraded, throughput, triples and escalation numbers are supplements.

## Stages

preflight (no GPU servers, hashes match) -> smoke gate (3 warmup pages: no errors, all rows present, each arm returns text on at least one page; an empty result from one arm on one page is a parser outcome, not a gate failure) -> primary timed run (170 pages x 2 arms) -> throughput supplement -> `e55_analyze.py`. Failed or empty pages are never rerun or replaced. The primary output file is never overwritten.

## Limits and caveats

Default-dpi confound (150 vs 250). LiteParse chooses a worker count and ONNX Runtime may use more than one core even with `numWorkers: 1`, so "single core" is not enforced; background CPU load on this desktop is not controlled but is not a GPU job (preflight checks that). Receipt and form text are English/Indonesian/clean-ish scans; invoices are Portuguese phone photos; the sample is small and public datasets may be in the vendor's training data (unknown). Field hits use string presence anywhere on the page, so a value can match by coincidence, which affects both arms. Word F1 on forms ignores layout and order. Single machine, single run per page per arm (timing noise is not estimated beyond the page bootstrap).

## Not claimed

No reproduction of ParseBench-2 or the vendor's 59.2, 426 ms/page or 27.8 pages/s; nothing about the larger OCRia-1, handwriting, charts, math, tables or non-Latin scripts; nothing beyond the sampled public pages and this CPU; no production-readiness, cost or safety claim; no router change; no E39 resolution.

Credit: LlamaIndex (OCRia-nano-1, LiteParse), the Tesseract authors, Naver CLOVA (CORD), the FUNSD authors, Francisco-Cruz et al. (invoice set), Hugging Face.
