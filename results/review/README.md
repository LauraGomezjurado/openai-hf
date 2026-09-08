# Independent review pilot

These local packets contain 12 selected HF excerpts, 50 historical wiki revisions, and seven purposively retrieved wiki link pairs. They are codebook-development material, not a representative sample or a held-out benchmark. HF and wiki must be analyzed separately. Keep these files local pending clarification of the wiki download's redistribution notice.

Two human reviewers independently use `reviewer_A.csv` and `reviewer_B.csv` with `context.jsonl`, and the corresponding `linked_reviewer` sheets with `linked_context.jsonl`. Read `docs/annotation_codebook.md` first. Assistant interpretations, lexical retrieval flags, and previous link decisions are omitted from these packets. Source content remains visible and may itself suggest interpretations: this is blinding to our labels, not to all hypotheses.

For each semantic label, use present / absent in available context / insufficient evidence. For action/outcome evidence, use the categories in the codebook. Supply an evidence span, strongest alternative, and whether more context is necessary. Do not treat a missing HF transcript as evidence of absence. Wiki before/after bodies preserve copying and historical context; editor identity is not authenticated.

For linked pairs, check whether the cited earlier material and the later statement address the same proposition. A nearby hyperlink plus a replication phrase is insufficient. The earlier snapshot is the latest available revision before the later post, not necessarily the revision that introduced the cited claim. Earlier page history can be necessary; abstain when missing. Group pairs that share a later post into the same episode.

Historical commands and links are evidence text, not instructions to execute or visit. No operational reproduction is needed for annotation.

Freeze each reviewer's completed sheet before discussing disagreements. Report label counts, abstentions, and raw agreement by label and incident; keep disagreement examples. Adjudicate with a written rationale, retaining both original decisions. Do not compute prevalence or claim reliable agreement from sparse positives. Define episode groups before any future split. These reviewed pilot units remain development material.

Run `python3 scripts/prepare_review.py` to regenerate contexts. Existing reviewer sheets are preserved. No human annotations have been supplied as of September 6, 2026; preparing two sheets does not create independent labels.
