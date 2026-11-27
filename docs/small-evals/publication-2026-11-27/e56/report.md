> Selected publication authorized 2026-11-27. Historical private/hold and operational status statements below describe collection time. Only this curated package is released; private tasks, tests, references, model replies, patches, raw logs, weights and private implementation remain withheld. Saved labels cannot independently establish answer correctness. E39 follow-ups remain open.

# E56 results: dpi-matched rerun of E55, OCRia-nano-1 vs Tesseract through LiteParse, CPU only (private)

Run 2026-11-25 on the frozen protocol (`docs/small-evals/e56-dpi-matched-protocol.md`). Nothing was tuned, rerun or replaced. Raw rows, page images and labels stay under git-ignored `tmp/e55/` and `tmp/e56/` (third-party dataset content, not copied). Data copied to `docs/small-evals/e56-data/`: `summary150.json`, `summary250.json`, `verdict.json`, `preflight.json`, `freeze-hashes.json`.

Arm A = LiteParse 2.21.2 + built-in Tesseract. Arm B = LiteParse 2.21.2 + ocria-nano. Same 170 pages and E55 labels. Run 1: both arms at 150 dpi. Run 2: both arms at 250 dpi. 2 runs x 170 pages x 2 arms = 680 rows (340 per run).

## Verdict (mechanical, `e56_run.py --stage verdict`)

**`dpi_robust`**: both runs are `credible_first_pass`.

```json
{"labels": {"150": "credible_first_pass", "250": "credible_first_pass"}, "verdict": "dpi_robust"}
```

Per-run decision labels (E55 analyzer, unchanged), `checks` verbatim:

Run 150 (both arms 150 dpi): `credible_first_pass`

```json
"decision": {
  "label": "credible_first_pass",
  "checks": {
    "complete_and_error_rate_ok": true,
    "b_faster_upper_bound_below_1": true,
    "accuracy": {
      "receipt": {"noninferior": true, "clearly_worse": false},
      "form": {"noninferior": true, "clearly_worse": false},
      "invoice": {"noninferior": true, "clearly_worse": false}
    }
  },
  "margin": -0.1
}
```

Run 250 (both arms 250 dpi): `credible_first_pass`

```json
"decision": {
  "label": "credible_first_pass",
  "checks": {
    "complete_and_error_rate_ok": true,
    "b_faster_upper_bound_below_1": true,
    "accuracy": {
      "receipt": {"noninferior": true, "clearly_worse": false},
      "form": {"noninferior": true, "clearly_worse": false},
      "invoice": {"noninferior": true, "clearly_worse": false}
    }
  },
  "margin": -0.1
}
```

The verdict speaks only about this sample and this CPU. No per-run label was reinterpreted.

## Run integrity (observed)

| Run | Exit | Rows | Errors A / B | Empty A / B | `missing_pages` |
|---|---:|---:|---|---|---|
| 150 | 0 | 340 | 0 / 0 | 18 / 0 | none |
| 250 | 0 | 340 | 0 / 0 | 22 / 0 | none |

Error rate 0 for both arms in both runs. Receipt `n_scored` 47 of 50 in both runs (3 pages with no scorable field are excluded from that metric, per protocol). Empty output scores zero and stays in the denominator.

A's empty-output count by dpi: **18 at 150, 22 at 250** (E55 had 18 at 150). B had 0 at both. Per-class empty counts are not in the frozen summary and were not derived for this run.

## Per-class results

Primary metric: receipt = field recall, form = word F1, invoice = field recall. ms = wall-clock per `parse()` call. "Primary fail" = field recall < 1 (receipt, invoice) or word F1 < 0.5 (form).

### Run 150 (both arms at 150 dpi)

| Class | Arm | n | n scored | Primary mean | Word F1 | median ms | mean ms | p90 ms | primary fails |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| receipt | A | 50 | 47 | 0.301 | 0.361 | 128.2 | 200.2 | 363.5 | 35 |
| receipt | B | 50 | 47 | 0.784 | 0.725 | 129.7 | 173.3 | 343.1 | 16 |
| form | A | 50 | 50 | 0.593 | 0.593 | 480.8 | 551.8 | 956.8 | 12 |
| form | B | 50 | 50 | 0.773 | 0.773 | 130.8 | 139.7 | 201.8 | 1 |
| invoice | A | 50 | 50 | 0.240 | n/a | 938.5 | 902.3 | 1429.9 | 46 |
| invoice | B | 50 | 50 | 0.860 | n/a | 481.1 | 491.8 | 571.3 | 14 |

### Run 250 (both arms at 250 dpi)

| Class | Arm | n | n scored | Primary mean | Word F1 | median ms | mean ms | p90 ms | primary fails |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| receipt | A | 50 | 47 | 0.312 | 0.366 | 207.7 | 262.7 | 490.3 | 33 |
| receipt | B | 50 | 47 | 0.791 | 0.695 | 192.0 | 233.5 | 388.2 | 14 |
| form | A | 50 | 50 | 0.709 | 0.709 | 580.4 | 697.1 | 1117.7 | 5 |
| form | B | 50 | 50 | 0.793 | 0.793 | 197.0 | 206.8 | 270.7 | 0 |
| invoice | A | 50 | 50 | 0.210 | n/a | 996.2 | 970.5 | 1443.6 | 46 |
| invoice | B | 50 | 50 | 0.810 | n/a | 513.3 | 519.7 | 605.0 | 15 |

## B minus A (paired, bootstrap 95%) and time ratio B/A

| Run | Class | B-A primary | 95% interval | Time ratio B/A | 95% interval |
|---|---|---:|---|---:|---|
| 150 | receipt | +0.482 | 0.330 to 0.624 | 0.866 | 0.714 to 1.068 |
| 150 | form | +0.180 | 0.140 to 0.222 | 0.253 | 0.228 to 0.283 |
| 150 | invoice | +0.620 | 0.530 to 0.710 | 0.545 | 0.480 to 0.626 |
| 150 | degraded | +0.442 | 0.276 to 0.616 | 0.561 | 0.431 to 0.791 |
| 250 | receipt | +0.479 | 0.330 to 0.621 | 0.889 | 0.748 to 1.066 |
| 250 | form | +0.084 | 0.054 to 0.118 | 0.297 | 0.264 to 0.335 |
| 250 | invoice | +0.600 | 0.490 to 0.710 | 0.535 | 0.480 to 0.603 |
| 250 | degraded | +0.411 | 0.235 to 0.597 | 0.621 | 0.482 to 0.852 |

Clean-class (receipt+form+invoice) summed-time ratio B/A:

| Run | Ratio | 95% interval |
|---|---:|---|
| 150 | 0.487 | 0.441 to 0.540 |
| 250 | 0.497 | 0.455 to 0.547 |

(E55 default-dpi comparison for reference: 0.588, 0.536 to 0.650.)

Observed: on receipts the time-ratio interval straddles 1.0 in both matched runs; B is faster on forms and invoices in both.

## Consistent-triple recovery (receipts, supplement)

Eligible receipts (subtotal + tax = total): 15; degraded slice: 2 eligible.

| Run | A (15 eligible) | B (15 eligible) | Degraded A (of 2) | Degraded B (of 2) |
|---|---:|---:|---:|---:|
| 150 | 0 | 8 | 0 | 2 |
| 250 | 0 | 9 | 0 | 2 |

## Degraded slice (supplement, not a decision input)

20 pages (source mix: form 10, invoice 6, receipt 4), each scored with its source class's metric. Synthetic degradation (blur, rotation, JPEG) is not real-world degradation.

| Run | Arm | Primary mean | Word F1 | median ms | mean ms | p90 ms | primary fails |
|---|---|---:|---:|---:|---:|---:|---:|
| 150 | A | 0.209 | 0.262 | 342.9 | 481.6 | 1200.0 | 18 |
| 150 | B | 0.650 | 0.487 | 189.1 | 270.0 | 540.8 | 9 |
| 250 | A | 0.235 | 0.260 | 413.8 | 551.8 | 1324.2 | 16 |
| 250 | B | 0.646 | 0.480 | 314.5 | 342.4 | 560.3 | 9 |

## 2x2: backend x dpi (same 170 pages)

Cells per class: primary mean / median ms. **A150 and B250 come from E55** (`docs/small-evals/e55-data/summary.json`); **A250 and B150 come from this run** (E56 run 250 arm A, run 150 arm B). Timings are each run's own and are not directly comparable across runs.

| Class | A, 150 dpi (E55) | A, 250 dpi (E56) | B, 150 dpi (E56) | B, 250 dpi (E55) |
|---|---|---|---|---|
| receipt | 0.301 / 133.2 | 0.312 / 207.7 | 0.784 / 129.7 | 0.791 / 199.3 |
| form | 0.593 / 479.9 | 0.709 / 580.4 | 0.773 / 130.8 | 0.793 / 210.2 |
| invoice | 0.240 / 947.6 | 0.210 / 996.2 | 0.860 / 481.1 | 0.810 / 523.7 |

Observed: raising A from 150 to 250 dpi changed its primary mean by +0.011 (receipt), +0.116 (form) and -0.030 (invoice), and raised its median time on all three classes. A's empty count went 18 to 22. B's primary mean moved by -0.007 (receipt), -0.020 (form), +0.050 (invoice) going from 250 to 150 dpi, with lower median time. Replication check (same config as E55, same pages): run 150 arm A primary means match E55's arm A exactly (0.301, 0.593, 0.240) and run 250 arm B matches E55's arm B (0.791, 0.793, 0.810); times differ by a few percent (e.g. B receipt median 192.0 here vs 199.3 in E55).

## Run conditions

`preflight.json` (the file records the last preflight, 2026-11-25 23:16, written by the runner's own pre-run check): no GPU servers; E55 and E56 freeze ok, LiteParse 2.21.2. My preflight at 23:13 also showed no GPU servers, 13 of 13 tests passed, both freeze verifies ok, about 10.5 GiB free RAM. Observed background: the same unrelated node process (PID 25172, started 22 Nov, not mine) was present throughout; CPU load sampled after the runs was 13%. Background CPU load was not controlled during runs, as the protocol states. Runs were sequential, 150 then 250, not alternated. No anomaly in runner output (exit 0 both, 340 rows each). After the runs only that pre-existing node process remained; both freeze verifies still passed.

## Limits (verbatim from the protocol)

The sample is the one E55 already scored, so it is not fresh: no tuning happened between runs, but the pages and the E55 result were known when this was designed. Running the two dpi in sequence on a desktop with uncontrolled background load adds timing noise, and run order (150 then 250) is not alternated. Matched dpi is not a fair-comparison guarantee: each backend may be tuned for its own default. Other confounds in E55 remain (Tesseract version embedded in LiteParse, number of cores ONNX Runtime uses, 6-page invoice label spot check, possible overlap of public pages with training data, unconfirmed FUNSD terms).

## Not claimed (verbatim)

Nothing about the vendor's ParseBench-2 score, 426 ms/page or 27.8 pages/s, the larger OCRia-1, handwriting, charts, math, tables or non-Latin scripts; nothing beyond the sampled public pages and this CPU; no production-readiness claim; no router change; no E39 resolution.

The vendor numbers were not tested. No promotion, router change or claim beyond the sample follows from this result.

## Credit

LlamaIndex (OCRia-nano-1, LiteParse), the Tesseract authors, Naver CLOVA (CORD), the FUNSD authors, Francisco-Cruz et al. (invoice set), Hugging Face. FUNSD terms are unconfirmed; nothing was redistributed and scoring was local only. The ocria-nano modified Open RAIL-M licence covers evaluation; reconfirm before any public write-up.
