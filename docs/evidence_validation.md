# Evidence validation and remaining access questions

Updated September 6, 2026. This separates what a public source defines from what our extraction reproduces and what remains independently unvalidated.

## HF timestamp and event crosswalk

The [METR timestamp methodology](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#timestamp-reconstruction-methodology) describes environmental clock anchors, interpolation over transcript-message position, and endpoint extrapolation. Its held-out-anchor test is encouraging but explicitly biased toward denser regions. This validates part of the investigators' reconstruction procedure; it does not supply event-specific uncertainty for our rows. Our ±5/30/120-minute scenarios remain assumptions, not calibrated confidence intervals.

The [timeline data](https://metr.org/assets/js/agent_timeline/data.js) and [renderer](https://metr.org/assets/js/agent_timeline/chart.js) support extraction of first board read/write, HF participation, and line endpoints. The renderer warns that participation is AI-graded and timing approximate. We have not independently validated those classifications. An ending line need not represent a deliberate decision to stop.

Local extraction finds 1,206 rows, 684 positioned onsets versus 688 declared participants, 15 onsets preceding first read, and 12 writes preceding first read. These are reproducible discrepancies/orderings, not proven source errors. Event semantics, incomplete exposure capture, and reconstruction error remain competing explanations. Request per-event anchor distance, interpolation/extrapolation status, timing intervals, classification evidence, and reasons for unpositioned participants before interpreting these cases.

The report's >90% statement uses a board-active population defined in footnote 30. Our July 9/11 cohorts use first recorded read dates. Neither denominator substitutes for the other. Request an explicit population/ID crosswalk before attempting replication of that statement.

The [workstream methods](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#identifying-important-messages-and-classifying-them-by-workstream) describe retrospective importance selection and reconstructed records. The extracted 112,062 classifications cannot be treated as unique delivered messages or as information available to a monitor at that hour. Message IDs, deduplication and selection provenance are the gate for a prospective prediction study.

The [HF replay](https://huggingface-anatomy-of-frontier-lab-model-intrusion.static.hf.space/index.html) exposes a curated sequence, not the underlying event log. Its 21 entries cannot validate individual METR rows. Request an event dictionary and redacted record-level joins; aggregate totals cannot supply those joins.

## Follow-up public discovery

- The first 100 public repository records returned by the METR organization API did not identify a website/report-source repository by name. This was a bounded discovery check, not an exhaustive search of repository contents or private history.
- [Simon Willison's September 4 article](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/) provides a SQLite conversion of the already-published wiki archive. Useful tooling; not independent incident evidence. No redundant database download was needed.
- The [Help, peer research log](https://helppeer.app/research) reports additional historical link investigations and distinguishes post-publication activity. It describes an automated, reviewed research workflow. Treat its entries as discovery leads requiring original-record verification, not independent confirmation of actor identity. We did not follow embedded operational links or contact live boards. Its claimed extra traces have not been joined to our corpus or attributed to HF.

No newly located source in this pass resolves the HF row-level definitions or supplies original HF message→read→action chains. This is a bounded search result, not a claim that no other public record exists.

## Review readiness

`results/review/` now contains context and two blank independent reviewer sheets for 62 units (12 HF excerpts and 50 wiki revisions), plus seven linked wiki pairs. Before/after wiki bodies are included; assistant interpretations and lexical flags are omitted. The historical excerpt selection remains visible and biased. Linked pairs share later posts and are not seven independent episodes.

Independent completed human reviews: zero at preparation. Review and adjudication require actual reviewers. The packets and unsent access request make that work concrete; further CPU runs cannot substitute for it.
