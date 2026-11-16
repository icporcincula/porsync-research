> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E07 protocol — before first model call

CORD v2 test split: all 100 annotations downloaded from the public Hugging Face
rows service, 2026-11-08, CC BY 4.0, NAVER CLOVA / Park et al.
Exact annotation SHA, dataset metadata, download URL and revision caveat retained.
Images not downloaded. Model input uses human-transcribed valid_line words,
row_id grouping and geometry ordering; no category/group labels or gt_parse leak.
This evaluates extraction from annotated text, not OCR performance on images.

Phase-0 selection: 42 eligible, 58 excluded. Explicit subtotal required; no inferred
gold subtotal; discount/unmodelled-charge receipts excluded; ambiguous annotation
fields excluded, not hand-corrected to retain cases. Both gold identities must hold
within 1 rupiah: sum of printed line prices = subtotal; subtotal + tax + service =
total. Full exclusion log retained. Never multiply line price by quantity twice.
This selected subset is easier and smaller than the full CORD test split.

Hand-checked fixtures: receipt 3 DONAT GULA 11000+0=11000;
receipt 5 TRAD KY TOAST CARTE 28182+2818=31000;
receipt 10 CINNAMON SUGAR 17000+0=17000. Tests assert those values, normalization
and independence of input text from structured gold. Missing count remains null.

Local Qwen3.5-9B Q4_K_M, same pinned server/GGUF/DLLs as E08; thinking off,
temperature 0, seed 808, 16,384 context, c=1, max 1,536 tokens. No grammar,
automatic JSON cleanup, implicit retry or fallback. One independent synthetic
receipt is the development gate; no test outcomes inspected to change prompts.
Freeze includes all Python sources and exact task files before first model call.

X0A/B/C: three identical baseline generations per receipt. X1 adds arithmetic
instruction. X2 passively checks X0A without modifying it. X3 uses the same X0A,
one re-ask only for schema/JSON or arithmetic failure, no automatic correction.
Queue randomized seed 7707. Raw responses, usage and timings retained.

Hypotheses from spec retained: H1 >=10% baseline contradictions; H2 no statistically
clear instruction-only reduction (paired 10,000 bootstrap, seed 0; upper CI<0 refutes);
H3 checker flags >=60% of wrong totals; H4 >=20% of wrong totals internally consistent;
H5 re-ask net gain on exact total accuracy >0. Undefined denominators explicitly
reported. Baseline hypotheses use X0A; repeats quantify the floor separately.
JSON/schema failures reported separately from arithmetic contradictions, included
as wrong extractions. Item F1 = exact multiset normalized name + line price;
quantity correctness/coverage separately reported for annotated quantities.

No public write-ups before both E08 and E07 finish. Internal results and audit
notes are scientific run artifacts. Pre-commit lint/format-integrity/build/test
config is shared with e08_summaries/.pre-commit-config.yaml.

Run from portfolio/small-evals:
`python -B -m e07_receipts.prepare`
`python -B -m pytest e07_receipts -q -p no:cacheprovider`
`python -B -m e07_receipts.run --phase dev`
`python -B -m e07_receipts.run --phase test`
