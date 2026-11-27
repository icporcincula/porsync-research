> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E56 protocol (frozen on commit): dpi-matched rerun of E55, OCRia-nano-1 vs Tesseract through LiteParse (private)

Date: 2026-11-25. Status: prepared and frozen by hash before any run. Private: no push, no publication, no public-evidence sync, no router change. CPU only; the runner refuses if `llama-server` or `strata` processes exist. Follow-up to E55 (private source reference withheld) (`credible_first_pass`).

## Question

E55 ran Tesseract at 150 dpi and ocria-nano at 250 dpi (each backend's documented default), so its accuracy and time advantage for ocria-nano could partly come from resolution. With both arms at the same dpi, does ocria-nano (B) still beat Tesseract (A) under the E55 reading rule? Decision: whether E55's `credible_first_pass` is a model effect or a default-dpi artifact. No router change follows.

## Design

Everything except dpi is the frozen E55 setup, reused unchanged and verified by the E55 freeze file at preflight: the same 170 seeded pages and 3 warmup pages, labels, manifest (arm order per page), `e55_parse.mjs`, `e55_analyze.py`, LiteParse 2.21.2, ocria-nano 1.0.0 hashes, `numWorkers: 1`.

- Run 1 (`dpi150`): A and B both at 150 dpi.
- Run 2 (`dpi250`): A and B both at 250 dpi.
- Each run is analysed independently with the unchanged E55 analyzer and reading rule (margin -0.10, uninformative-class rule, time check on the clean classes). Throughput supplement and smoke stage are not repeated (E55 smoke passed on the same harness; a run with an arm error rate above 10% is `incomplete` by the rule).
- Together with E55 this fills a 2x2 (backend x dpi) on the same pages: A150 and B250 from E55, A250 and B150 new. Compare only across rows measured in one run for timing; accuracy differences across runs use the same pages, so per-page values are comparable, but each run's timing is its own.

## Reading rule (frozen)

Per-run labels come from the E55 analyzer. The combined verdict is mechanical (`e56_run.py --stage verdict`):

- `dpi_robust`: both runs are `credible_first_pass`.
- `dpi_dependent`: exactly one run is `credible_first_pass`.
- `advantage_not_confirmed_when_dpi_matched`: neither is.

No per-run label is reinterpreted afterwards. `inconclusive` is a live outcome for either run. The verdict speaks only about this sample and CPU.

## Limits and caveats

The sample is the one E55 already scored, so it is not fresh: no tuning happened between runs, but the pages and the E55 result were known when this was designed. Running the two dpi in sequence on a desktop with uncontrolled background load adds timing noise, and run order (150 then 250) is not alternated. Matched dpi is not a fair-comparison guarantee: each backend may be tuned for its own default. Other confounds in E55 remain (Tesseract version embedded in LiteParse, number of cores ONNX Runtime uses, 6-page invoice label spot check, possible overlap of public pages with training data, unconfirmed FUNSD terms).

## Not claimed

Nothing about the vendor's ParseBench-2 score, 426 ms/page or 27.8 pages/s, the larger OCRia-1, handwriting, charts, math, tables or non-Latin scripts; nothing beyond the sampled public pages and this CPU; no production-readiness claim; no router change; no E39 resolution.

Credit: LlamaIndex (OCRia-nano-1, LiteParse), the Tesseract authors, Naver CLOVA (CORD), the FUNSD authors, Francisco-Cruz et al. (invoice set), Hugging Face.
