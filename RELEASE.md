# Public evidence release — 2026-11-16

## Included

Nine study groups linked by the website: reports, aggregate results, frozen configurations and selected analysis scripts. E40 includes all 150 trial rows, 90 timing observations and VRAM series. E39 includes the bounded local-validation observations, retrieval prompt, partial MBPP score summary and sample-ID/hash manifest. Historical identifiers remain stable for citation.

## Withheld or unavailable

This is not the complete private archive. Receipt images/text, contract excerpts, third-party datasets, generated benchmark solutions, full model-response traces, private project code and agent transcripts are excluded pending redistribution/privacy review. Later E39 logs exist only on the run machine; exact E40 timing source prompts were not archived. Model weights and runtimes are not supplied. No claim is made that these excluded files cannot ever be published.

The reports retain historical descriptions of full-archive checks; those descriptions do not imply the underlying files are public. Unavailable Markdown links have been replaced with explicit notes. Historical build/status paragraphs describe their original date, not the present website deployment.

## Reproduction boundary

The E40 paired and timing analyses run directly on the included data. Other reporting scripts and E39 diagnostic scripts are method references: they depend on excluded inputs, private implementation modules, local runtimes or machine paths and are not turnkey reproductions. Do not run the E39 diagnostic script without adapting its environment; it initiates local inference. The public package supports inspection of reported aggregates, not independent regeneration of every study or scoring of every raw response.

## Publication review and transformations

An explicit file allowlist was exported from a fixed source revision, without private repository history or uncommitted work. No broad directory mirror was used. Machine-local user/workspace paths were generalized. Text was normalized to UTF-8/LF; E40 analysis input paths were made portable and misleading cold/warm timing labels corrected to first/later. Source and released hashes are recorded in MANIFEST.json. Results were not changed. Raw data exclusions reduce redistribution and privacy exposure; automated secret checks are supplementary, not a guarantee.

## Rights and provenance

This release does not grant rights to excluded datasets, third-party implementations or model weights. No blanket open-source license is asserted over historical artifacts. Consult upstream terms when obtaining inputs independently. Public availability permits inspection; obtain permission before redistribution or reuse where required. Author-created aggregate measurements are distinguished from source datasets by the file inventory and study reports.
