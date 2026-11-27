> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E55 results: OCRia-nano-1 vs Tesseract through LiteParse, CPU only (private)

Run 2026-11-25 on the frozen protocol (`docs/small-evals/e55-ocria-nano-protocol.md`). Nothing was tuned, rerun or replaced. Raw rows, page images and labels stay under git-ignored `tmp/e55/` (third-party dataset content, not copied). Data copied to `docs/small-evals/e55-data/`: `summary.json`, `throughput.json`, `preflight.json`, `freeze-hashes.json`.

Arm A = LiteParse 2.21.2 + built-in Tesseract (dpi 150). Arm B = LiteParse 2.21.2 + ocria-nano (dpi 250). 170 pages x 2 arms = 340 rows.

## Decision (frozen reading rule, verbatim from the analyzer)

Label: **`credible_first_pass`**

```json
"decision": {
  "label": "credible_first_pass",
  "checks": {
    "complete_and_error_rate_ok": true,
    "b_faster_upper_bound_below_1": true,
    "accuracy": {
      "receipt": {"noninferior": true, "clearly_worse": false},
      "form":    {"noninferior": true, "clearly_worse": false},
      "invoice": {"noninferior": true, "clearly_worse": false}
    }
  },
  "margin": -0.1
}
```

Clean-class summed-time ratio B/A (receipt+form+invoice): **0.588** (95% CI 0.536 to 0.650).

## Smoke and run integrity (observed)

- Smoke gate passed (6 rows). Primary: exit 0, 340 rows, `missing_pages` empty.
- Errors: A 0, B 0 (error rate 0 for both).
- Empty outputs (whitespace-only text): **A 18**, B 0. A's empties by class (derived from page-id prefix in rows): receipt 12, invoice 4, degraded 2, form 0. Empty output scores zero and stays in the denominator, per protocol.
- Receipt `n_scored` 47 of 50 (3 pages had no scorable field and are excluded from that metric, per protocol).

## Per-class results

Primary metric: receipt = field recall, form = word F1, invoice = field recall. ms = wall-clock per `parse()` call. "Primary fail" = field recall < 1 (receipt, invoice) or word F1 < 0.5 (form).

| Class | Arm | n | n scored | Primary mean | Word F1 | median ms | mean ms | p90 ms | empty | errors | primary fails |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| receipt | A | 50 | 47 | 0.301 | 0.361 | 133.2 | 204.5 | 378.7 | 12 | 0 | 35 |
| receipt | B | 50 | 47 | 0.791 | 0.695 | 199.3 | 237.4 | 405.5 | 0 | 0 | 14 |
| form | A | 50 | 50 | 0.593 | 0.593 | 479.9 | 550.9 | 874.5 | 0 | 0 | 12 |
| form | B | 50 | 50 | 0.793 | 0.793 | 210.2 | 217.8 | 287.1 | 0 | 0 | 0 |
| invoice | A | 50 | 50 | 0.240 | n/a | 947.6 | 920.5 | 1422.9 | 4 | 0 | 46 |
| invoice | B | 50 | 50 | 0.810 | n/a | 523.7 | 530.9 | 601.9 | 0 | 0 | 15 |

Per-field hit detail (total vs subtotal vs tax vs NIF) is not in the frozen summary, so it is not reported. Per-class empty counts for B are 0 everywhere; A's per-class empties are the counts above.

## B minus A (paired, bootstrap 95%) and time ratio

| Class | B-A primary | 95% interval | Time ratio B/A | 95% interval |
|---|---:|---|---:|---|
| receipt | +0.489 | 0.333 to 0.635 | 1.161 | 0.926 to 1.478 |
| form | +0.200 | 0.158 to 0.244 | 0.395 | 0.357 to 0.442 |
| invoice | +0.570 | 0.460 to 0.680 | 0.577 | 0.511 to 0.661 |
| clean classes pooled | | | 0.588 | 0.536 to 0.650 |

Observed: on receipts the median per-page time is higher for B (199 vs 133 ms) and the ratio interval straddles 1.0; B is faster on forms and invoices. The pooled "B faster" check passes on the clean classes only.

## Degraded slice (supplement, not a decision input)

20 pages (source mix: form 10, invoice 6, receipt 4), each scored with its source class's metric.

| Arm | Primary mean | Word F1 | median ms | mean ms | p90 ms | empty | primary fails |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 0.209 | 0.262 | 350.4 | 507.5 | 1256.2 | 2 | 18 |
| B | 0.646 | 0.480 | 279.2 | 345.1 | 565.7 | 0 | 9 |

B-A +0.438 (0.270 to 0.613); time ratio B/A 0.680 (0.507 to 1.011). Synthetic degradation (blur, rotation, JPEG) is not real-world degradation.

## Consistent-triple recovery (receipts, supplement)

Eligible receipts (subtotal + tax = total): 15 (degraded slice: 2 eligible). Output contains all three values: A 0 of 15, B 9 of 15. Degraded: A 0 of 2, B 2 of 2.

## Escalation signature (descriptive)

Flag = fewer than 10 words, or (receipts, invoices) no amount-like token.

| Class | Arm | Flag rate | Sensitivity (primary fails caught) | Flag rate on pages that were fine |
|---|---|---:|---:|---:|
| receipt | A | 0.66 | 0.743 | 0.333 |
| receipt | B | 0.08 | 0.071 | 0.091 |
| form | A | 0.00 | 0.000 | 0.000 |
| form | B | 0.00 | n/a (no fails) | 0.000 |
| invoice | A | 0.48 | 0.522 | 0.000 |
| invoice | B | 0.02 | 0.000 | 0.029 |
| degraded | A | 0.45 | 0.444 | 0.500 |
| degraded | B | 0.05 | 0.000 | 0.091 |

Observed: for B the signature almost never fires, including on pages B fails (receipt 14 primary fails, 1 caught of 14; invoice 15 fails, 0 caught), so this signature does not identify B's failures. For A it catches roughly half to three quarters of failures, largely because A returns empty or amount-free text.

## Throughput supplement (never changes the decision)

6 single-arm Node processes per arm, one arm at a time, 170 pages each, all return codes 0.

| Arm | wall s | pages/s |
|---|---:|---:|
| A | 23.2 | 7.33 |
| B | 21.9 | 7.75 |

Caveat (as frozen): includes process and model start-up, so it is a lower bound on steady-state pages per second. The per-arm difference (about 6%) is a single run with no interval.

## Run conditions

`preflight.json` (2026-11-25 22:58): no GPU servers; Windows-11-10.0.26200; 12 logical CPUs; Node v24.13.0; Python 3.12.7; freeze ok, LiteParse 2.21.2. About 10.4 GiB free RAM at the start. Observed background: a node process (PID 25172, started 22 Nov, not mine) was running throughout; CPU load sampled after the runs was 19%. Background CPU load was not controlled, as the protocol states. No anomaly in the runner output.

## Caveats

- **Default-dpi confound:** arm A at 150 dpi and arm B at 250 dpi (each backend's documented default). Part of any B advantage, and part of its time cost, may come from the dpi difference rather than the model.
- **Invoice labels:** only a 6-page spot check was done before the freeze (totals 6 of 6, NIF 5 of 6 with one unreadable; date and iva_amount dropped). Remaining label errors are possible; they hit both arms equally.
- Protocol limits (verbatim): Default-dpi confound (150 vs 250). LiteParse chooses a worker count and ONNX Runtime may use more than one core even with `numWorkers: 1`, so "single core" is not enforced; background CPU load on this desktop is not controlled but is not a GPU job (preflight checks that). Receipt and form text are English/Indonesian/clean-ish scans; invoices are Portuguese phone photos; the sample is small and public datasets may be in the vendor's training data (unknown). Field hits use string presence anywhere on the page, so a value can match by coincidence, which affects both arms. Word F1 on forms ignores layout and order. Single machine, single run per page per arm (timing noise is not estimated beyond the page bootstrap).
- Hypothesis (not tested): A's 18 empty outputs and low receipt/invoice recall may reflect Tesseract failing on phone-photo and receipt layouts at 150 dpi; a dpi-matched rerun would be needed to separate this from the model.

## Not claimed (verbatim)

No reproduction of ParseBench-2 or the vendor's 59.2, 426 ms/page or 27.8 pages/s; nothing about the larger OCRia-1, handwriting, charts, math, tables or non-Latin scripts; nothing beyond the sampled public pages and this CPU; no production-readiness, cost or safety claim; no router change; no E39 resolution.

The vendor numbers (59.2, 426 ms, 27.8 pages/s) were not tested. No promotion, router change or claim beyond the sample follows from this result.

## Credit and terms

LlamaIndex (OCRia-nano-1, LiteParse), the Tesseract authors, Naver CLOVA (CORD, CC-BY-4.0 per the card), the FUNSD authors, Francisco-Cruz et al. (invoice dataset), Hugging Face. FUNSD terms are unconfirmed (the re-upload has no licence); nothing was redistributed and scoring was local only. The ocria-nano modified Open RAIL-M licence covers evaluation; reconfirm before any public write-up.
