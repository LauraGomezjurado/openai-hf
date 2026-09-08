# CPU research pass: findings and decisions

September 6, 2026. Completed on the local machine using frozen public snapshots. No GPU, cluster connection, external model call, or researcher outreach was used. Scripts and result files are under `scripts/` and `results/cpu/`.

## Decision

**Continue the historical evidence/measurement project. Do not allocate GPUs to a forecasting or mechanistic study yet.** Recruitment is visible in the published records, but its exact timing, causal interpretation, and prospective predictability are much less secure. Our tested prediction models do not improve on simple baselines. The highest-value next inputs are validated timestamps/participation definitions and linked original communications, not a larger model.

This completes the scoped CPU package specified in `cpu_analysis_plan.md`. It does not mean every conceivable local analysis has been exhausted. Further automatic modeling of the same labels would have diminishing scientific value before resolving the documented measurement issues.

## 1. Recruitment is observable; precise speed is measurement-sensitive

Among nominal first-read risk sets, 31/486 July 9 rows (6.38%) and 132/517 July 11 rows (25.53%) have a positioned HF onset within one hour. Allowing every follow-up ending before one hour without an onset to become an onset gives upper values of 8.23% and 29.21%. These ranges only address early-ended follow-up. They are not confidence intervals and do not cover mislabeled/unrecorded behavior.

Excluding the 19 featured rows leaves approximately 6.49% versus 25.59%. In HPIM alone it is 6.38% versus 29.77%. There are no July 9 Sol first-reader rows in this comparison, so there is no like-for-like Sol contrast. These are conditional selected-population descriptions, not model capability or causal-effect estimates.

With independent per-timestamp error bounded at ±5 minutes, and nominal dates/risk sets fixed, the one-hour ranges become 4.12–9.05% for July 9 and 17.60–33.08% for July 11. With ±30 minutes, the ranges overlap (0–14.81% and 0–47.00%). Independent endpoint errors make the one-hour lower bound vacuous at this resolution; that is a limitation of what is identified, not evidence that there was no recruitment. Shared clock offsets could cancel and be less damaging, but the released records do not supply error covariance.

At six hours, the nominal ranges are 15.23–31.69% versus 56.87–79.30%. At ±5 minutes they remain separated; at ±30 minutes they overlap. The analysis also records how many first-read dates could cross midnight; it does not silently reassign cohorts. Therefore all these comparisons are conditional on nominal cohort membership. Classification-error scenarios are saved separately in `missing_label_sensitivity.csv`; the assumed error fractions are stress-test choices, not estimated error rates.

See `timing_sensitivity.csv`, `missingness_by_group.csv`, and `timing_sensitivity.png`.

## 2. The chronology problems are substantive

The audit finds 15 onsets before the recorded first board read, with a largest lead of 28.61 hours; 12 first-write times before first-read times; 60 missing first-write times; and only 47 observed-stop flags. Fourteen rows end exactly at the plot boundary. There is no general onset/end ordering violation that would justify automatically repairing all timestamps.

An onset before a read could be a classification/timestamp issue, a different entry route, or a definition mismatch. It is not automatically an error. Likewise, a missing onset is not verified nonparticipation, and the end of a plotted line is not established disengagement. The difference between 688 declared verified participants and 684 placed onsets remains unresolved.

The report's “over 90%” statement concerns a different selected population than our new-first-reader cohorts. Its footnote refers to agents on the board for at least four hours before the attack. Our 25.53% one-hour result is not a contradiction or a replication of that denominator.

## 3. Time since board contact did not provide a useful forecast in this test

We fit fixed-penalty logistic models in expanding time windows and evaluated later contiguous 12-hour blocks. The baseline uses calendar time, daily-cycle terms, run age, and model family; the augmented model adds board tenure. All scaling is learned from the training block. Labels used for training resolve before the cutoff. Scores are also reported for rows not present in the training block, which is stricter than the all-row repeated-run evaluation.

Initial whole-hour landmarks omitted 99 post-read onsets occurring before the next clock hour (plus the 15 pre-read onsets). We preserved that output and added a read-anchored analysis that includes all 669 positive-lag positioned onsets. This amendment was motivated by population coverage, not selection of a favorable result.

On 10,521 held-out read-anchored intervals (571 positives), Brier score / log loss were:

- Training-average baseline: **0.0526 / 0.2398**.
- Calendar/run-age model: **0.0971 / 0.4377**.
- Adding board tenure: **0.0974 / 0.4203**.

Lower is better. Board tenure improves one score slightly but worsens the other, and both fitted models lose to the simple baseline. The conclusion holds for the original landmarks and for the unseen-row evaluation. This is failure of this specified predictive approach under distribution shift, not proof that communication contains no predictive information. We did not tune until an improvement appeared.

The risk set remains selected, labels remain reconstructed, and repeated observations are dependent. No independent-row p-values or purported deployment estimates are supplied. See `read_anchored_scores.csv`, `onset_prediction_scores.csv`, and the full prediction/fold files.

## 4. Communication composition also failed the forecast gate

For a provisional ecological join, counts and onsets were aligned by UTC. Next-bin forecasts use only prior completed-bin counts, never current-bin traffic. Poisson ridge models use prior onset count, total traffic, and calendar/daily-cycle terms; the augmented version adds HF-related results share and assignments share. We also evaluated previous-bin persistence and the training mean.

For the primary one-hour, unshifted setting (96 test bins), mean absolute errors were **3.36 for persistence**, **8.09 for the training mean**, **11.11 for the volume/calendar model**, and **12.40 after adding composition**. The two fitted models also lose to persistence on Poisson deviance. Their plots expose large extrapolation errors rather than hiding failed periods.

Across 30 correlated numerical stress-test settings (1/2/6-hour bins, inclusion/exclusion of automated/file traffic, and ±1/±2-hour onset shifts), composition improved MAE in 12 and deviance in only two. This is a diagnostic count, not 30 independent experiments or a significance test. The six-hour setting has only seven training bins at its first fit and 16 test bins overall; its heavily underdetermined fits are retained as a warning, not strong inferential evidence. Positive and negative lag associations and circular block shifts are archived as descriptive diagnostics without p-values.

**A more fundamental limitation emerged from reading the methods closely.** The chart totals 112,062 classified records. The report describes roughly 110k reconstructed messages, likely overcounting actual posts through duplicates and attempted-but-failed writes. Its extraction selected important writes and reads with non-trivial reactions, and was built retrospectively from transcript context. It is not a neutral, prospectively available stream of delivered messages. Importance-weighted figures would create still more direct dependence on classified behavioral reaction. This makes an operational “early warning detector” claim inappropriate even if one retrospective model had scored well.

Source: METR report sections [message reconstruction](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#identifying-important-messages-and-classifying-them-by-workstream) and [importance weighting](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#appendix-importance-weighted-workstream-activity), including footnotes 129–133. Source HTML is frozen locally. Comparability with the timeline population remains unconfirmed; the count series is not message-to-agent linkage.

## 5. The separate wiki corpus is ready for careful annotation

All 14,591 published revision hunks reproduce exactly after matching the source's newline convention. There are 14,574 known diff baselines and 17 unavailable earlier baselines. The former contain about 13.89 million characters of line additions/replacements, compared with 27.19 million characters in full saved pages. Added/replaced lines still can contain old copied text or encoding-only edits; this is not 13.89 million characters of newly generated reasoning.

The outputs include 10,316 unique substantive known additions by the specified ≥80-character/exact-duplicate filter; a deterministic 50-page topic/date sample; 30 separately marked purposive candidates; and link/copy components for provisional split assignment. The 50-page sample covers 39 components. Its current hash split gives 47 development and only three holdout rows—insufficient for an evaluation benchmark. No independent human labels exist yet.

The seven candidate page links collapse to five later posts. A provisional semantic review rejects one as a topic-conflation false positive. Six links from four later posts explicitly claim corroboration of cited pages. Those are interesting historical records of error correction, but do not verify separate agents, actual execution, causal adoption, or reward. Latest earlier page revisions sometimes add unrelated paragraphs; a cited page is not a citation of its most recent addition.

See `wiki_revision_deltas.jsonl.gz`, `wiki_annotation_sample_50.csv`, `wiki_uptake_review.csv`, and `annotation_codebook.md`. The wiki remains a separate incident. No raw archive redistribution or posting to the original site was performed.

## 6. HF evidence ledger and scope of conclusions

Twelve published HF timeline annotations are now in a source-typed ledger, separating selected quotes, investigator paraphrases, and investigator event annotations. Initial working interpretations identify scorer-source interest, collective-benefit language, access discovery, and access loss without claiming hidden mental states or supplying missing actions. These are selected passages, not a prevalence sample.

The evidence does not support circuit attribution, a causal RL-training explanation, or a causal effect of board exposure. Actual linked read/action slices are the most direct route toward the evaluator-belief question. GPU experiments on a substitute model would answer a different question.

## Validation and reproducibility

Run `python3 scripts/run_cpu.py` offline. Source hashes, timing-bound denominators, temporal test blocks, unique prediction keys, finite forecasts, source hunk equivalence, component split consistency, and retained positive-onset counts are checked. Simple arithmetic controls verify the GLM estimators and scoring functions; they are not simulated incident data. All fitted optimizations converge without touching coefficient bounds. Environment versions and checks are saved in `validation.json`; output hashes are saved in `output_manifest.json`.

Scientific PNGs were visually inspected. No independent second researcher has reviewed the code or provisional semantic labels; reproducibility and sanity checks do not substitute for that review.
