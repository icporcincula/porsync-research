> Public release note (2026-11-16): this is a curated historical record. References to raw traces, source data, private implementations or local paths describe the original archive, not necessarily files distributed here. See the root RELEASE.md for availability and reproduction limits.

# E08 frozen protocol — 2026-11-08

Local Qwen3.5-9B Q4_K_M; temperature 0, seed 808, one slot, thinking off,
16,384 context, 1,536 output tokens. Raw requests, responses, usage and timings retained.
No JSON grammar or retries. Generation failures/truncations remain visible.

200 country × five-year snapshots, three indicators (coal/oil/gas CO2, million tonnes),
from OWID's public CO2 CSV downloaded 2026-11-08. Source SHA and attribution in data.json.
Underlying source: Global Carbon Budget, Global Carbon Project, CC BY 4.0;
OWID processing CC BY 4.0. See https://github.com/owid/co2-data and
https://globalcarbonbudget.org/ (data attribution retained; not a climate accuracy study).

Phase-0 adjustment before inference: only 121 countries have complete values for all
three series. Sample up to two non-overlapping windows per country (1990–2023), seeded
808; five development snapshots, with their countries excluded from the 200 test
snapshots. Country-cluster bootstrap (10,000, seed 0) for paired comparisons.
Cells displayed to three decimal places; calculations use displayed cells.

Arms N0/N1 follow the spec; N2 derives directly from N1, N3 reuses the same N1
first attempt then permits one re-ask. This avoids duplicate deterministic inference
and makes guarding/repair comparisons paired. Frozen prompt text in run.py.
Number membership accepts cells, min/max, consecutive or endpoint differences and
percentage changes, rounded half-up to 0, 1 or 3 decimals; absolute changes accepted
for verbs such as 'fell'. Years 1900–2100 are excluded, even if an amount collides:
this known weakness is audited. Million/thousand/billion expressions normalized to
table units. Numeric digit notation is checked; spelled-out numbers, fractions,
unusual scientific notation and semantic relations are outside the checker.
No guarantee of semantic faithfulness. Default prompt asks not to convert units.

Hypotheses from spec retained. H2 'roughly halves' operationalized as a nonzero
N1 summary-flag rate at most 60% of N0. H4 compares fallback counts, undefined
if N2 has zero. H5 counts flags judged legitimate under the frozen operational
definition (not just membership replay), with genuinely supported extra precision
or alternative derivations treated as false flags.

Audit seed 1808: sample 50 flagged number occurrences and 50 passing summaries
from N0/N1 (all if fewer), read against full displayed tables. Conducted by this
agent, not an independent human; this limitation must accompany claims about audit
precision. Direction heuristic will be audited separately; numbers with correct
values can still make wrong claims. No public article or social drafts until E07
also finishes, per user instruction. Internal results/audit notes are run artifacts.

Reproduction from portfolio/small-evals:
`python -B -m e08_summaries.prepare`
`python -B -m pytest e08_summaries -q -p no:cacheprovider`
`python -B -m e08_summaries.run --phase dev`
`python -B -m e08_summaries.run --phase test`

Freeze JSON hashes code, inputs, GGUF, server and runtime DLLs before first call.
Do not change frozen code after inference; corrections require separate audited reporting.
