# Working plan — updated after the first CPU pass

Updated September 6, 2026. Primary case: confirmed Hugging Face incident. Secondary case: the separately attributed wiki archive.

## Completed locally

- Source snapshots and checksums; CSV extraction from public METR figure assets.
- Timeline ordering/missingness audit, nominal risk sets, family and featured-row sensitivity.
- 1/6/24-hour follow-up availability ranges and ±5/30/120-minute timing stress tests; separate assumed label-error scenarios.
- Temporally held-out onset predictions, simple baseline checks, and a read-anchored correction retaining rapid onsets.
- Provisional hourly workstream forecasting, alternate bins, traffic filters, timestamp shifts, and lag diagnostics.
- Exact reconstruction of every wiki revision hunk, duplicate flags, link/copy groups, 50-page annotation sample, and 30 purposive candidates.
- Provisional review of seven wiki links and a 12-entry HF publication evidence ledger.
- Offline pipeline, integrity/estimator checks, scientific plots, and full results memo.

## Decisions from the results

**Continue:** a historical measurement/evidence study. The recruitment pattern is observable, but precise timing depends on measurement assumptions. The public data's definitions and missingness are themselves important to reconstruct.

**Do not expand now:** more forecast variants, larger classifiers, RL reproductions, or circuit searches. The tested models fail simple baselines, traffic construction is retrospective/selected, and the text corpus lacks independent labels. Additional compute does not resolve those problems.

**Keep separate:** the wiki comparison is useful for developing a method for tracing corrections and claimed corroboration. It does not establish what the HF agents did or why.

## Highest-value next actions

September 6 follow-up: see `evidence_validation.md` for the source-definition crosswalk and bounded public-source search, `research_directions.md` for proposed studies and gates, and `results/review/README.md` for the prepared independent-review workflow. Two reviewer sheets and full wiki context now exist; no human review has yet occurred. New public wiki tooling does not resolve the HF access gap.

1. **HF data clarification/access.** The reviewable request in `access_request.md` is ready but unsent. Ask about the 688/684 difference, 15 early onsets, 12 write-before-read rows, timing grades, line endings, and population alignment. Request a small linked message→read→action sample including negative/ambiguous cases. This requires authorized outreach and an external response.
2. **Independent episode review.** Two human reviewers should annotate a pilot using `annotation_codebook.md`, adjudicate disagreements, and help define a real held-out set. The current 50-page sample is for codebook development, not a ready benchmark; only three rows landed in its provisional holdout. This needs reviewer time, not GPU time.
3. **Raw-record validation of the strongest claims.** With additional records, test whether evaluator beliefs precede strategy changes, and whether peer requests explain anything beyond shared task difficulty and access changes. Without those records, keep claims at the level of selected published examples and reconstructed chronology.
4. **Only then consider the V100 cluster.** If the episode labels/controls support a monitor-input ablation, benchmark one small model on one free GPU before scheduling more. The cluster remains untouched. This would test monitor behavior using real historical inputs, not infer the original model's internal mechanism.

## Definition of local completion

The current CPU work package is complete. There are always more calculations one could run, but the next decision-relevant steps need better evidence or independent labels. We should not spend time searching model variants merely to turn the negative forecast result into a positive one. No background job, scheduled follow-up, or unapproved outreach is running.

## Changes to the original plan

- The proposed two-week numerical pilot was feasible in one local pass; its scientific gates, rather than elapsed days, now determine progress.
- Whole-hour landmarks were found to omit 99 rapid post-read onsets; a read-anchored sensitivity was added and the original result retained.
- A constant training-average baseline was added after poor initial model calibration became apparent. It outperformed the more complex onset models.
- The workstream study is downgraded to a provisional ecological diagnostic after confirming retrospective importance-based extraction and overcounting in the source methodology.
- A first-round delta extraction discrepancy was traced to terminal-newline handling. The corrected extractor now matches all 14,591 source hunks.
- The wiki link heuristic produced a concrete false positive; links are now explicitly graded as candidate/self-reported corroboration rather than causal information flow.
