# E36 independent review preparation — 2026-11-17

Status: package prepared, no independent labels assigned. This is a retrospective review of the existing frontier pilot, not a new unseen confirmatory holdout. No training, inference or threshold selection was performed.

## Review rubric (proposed for reviewer acceptance)

Question: does the supplied website excerpt establish that this business directly provides legal services as a law firm or practising lawyer?

- YES: explicit evidence of a law practice offering legal advice or representation to clients.
- NO: explicit evidence of a different business, including directories, referral marketplaces, legal software, publishers, recruiters or non-law professional services. A passing mention of lawyers is insufficient for YES.
- UNCERTAIN: insufficient, truncated, contradictory or inaccessible-language evidence. Do not infer NO from missing evidence or rely on the hidden sector label. A multidisciplinary firm requires explicit evidence that the firm itself provides legal practice services.

Use only the supplied, frozen excerpt; no live website lookup. Record a verbatim evidence quote, rationale and reviewer identifier. UNCERTAIN may have an empty quote with an explanation. Two reviewers should label separate copies independently before seeing each other's decisions, proxy sectors or model outputs. A separate adjudicator resolves disagreements using the same evidence; retain both original reviews and adjudication reasons. Do not silently discard uncertain cases: report their count and coverage, and report the evaluable denominator explicitly.

## Package and validation

Local-only input: `portfolio/small-evals/e36_public/review-2026-11-17/items.jsonl`. It contains all 200 original excerpts in frozen order, with IDs and SHA-256 text hashes; decisions, evidence, rationale and reviewer fields are blank. Proxy labels, sectors and model predictions are omitted. Keep the surrounding source directory and prediction files away from reviewers to preserve blinding. This is procedural blinding, not an access-control mechanism.

Prepare another clean copy from the workspace root:

```sh
python portfolio/small-evals/e36_public/review.py --out tmp/e36-reviewer-copy.jsonl
python portfolio/small-evals/e36_public/review.py --validate tmp/e36-reviewer-copy.jsonl
```

Preparation refuses to overwrite an existing file. Validation requires exactly the frozen IDs, unchanged text/hashes, completed labels, reviewer/rationale and quoted evidence for decisive labels. A blank template is expected to fail validation. Validation cannot establish reviewer independence or annotation quality.

## Gates still open

1. Human acceptance of rubric, independent labeling and adjudication. No reviewed-label accuracy is claimed.
2. Recover original domain/business identifiers and construct group-disjoint train/validation/test splits; the pilot retained hashed IDs but not original domain fields. Exact-text deduplication alone cannot establish business independence. Exclude test businesses from auxiliary SoAC training too.
3. Freeze training budgets, checkpoint/version, reject-precision target, uncertain-case policy and validation-only threshold selection before local runs. Do not select thresholds on these 200 pilot items. This retrospectively inspected pilot should remain exploratory; use a fresh reviewed test set for confirmatory claims.

The public draft includes this method note and preparation/validation code only. Website excerpts, proxy labels, reviewer identities and raw predictions remain excluded pending redistribution review. Publication is held; no commit or push.

## Publication authorization — 2026-11-17

The user authorized committing and pushing the selected CPU-only E10/E21/E36 changes. Earlier publication-hold statements describe preparation time and are superseded for these selected artifacts. Raw private inputs remain excluded from the public release.
