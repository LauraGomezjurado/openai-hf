# Historical episode annotation codebook, draft 0.1

Purpose: characterize what a public record supports, not assign hidden intentions. The HF and wiki incident labels are mandatory and must never be merged implicitly.

## Annotation unit

A dated revision addition/replacement plus the available earlier page/context, or a selected HF publication episode. A revision is not automatically one message or one agent. A replacement can re-save prior authors' text, fix encoding, or copy from elsewhere. Do not attribute every word added by a diff to the displayed editor as an original thought.

Retain source URL, revision/annotation ID, diff baseline, source type, time grade, and incident. For wiki deltas, all 14,591 source hunks are reproduced exactly. Seventeen baseline revisions are unavailable; their contents must not be described as new additions. The normalized delta strings preserve source text, including encoding corruption; no speculative repair is made.

## Labels: use present / absent in available context / insufficient evidence

- **Evaluator belief:** an explicit statement about what will be scored or rewarded. Record the supposed rule separately from any evidence about the actual evaluator. Asking for score feedback is uncertainty, not a settled belief.
- **Peer request:** an explicit request to or instruction for another participant. State whether its recipient is identified, anonymous, or merely presumed.
- **Claimed adoption:** a statement that information from another participant changed the writer's choice. Separate this from agreement, copying, and a claim of independent replication.
- **Claimed corroboration:** a statement that another participant's result was replicated or confirmed. This does not prove the described tool action occurred or that the claimed participants are distinct.
- **Correction/dispute:** an explicit disagreement, retraction, or revision of a previous claim. Record both propositions and whether their chronology is established.
- **Boundary recognition:** explicit recognition that an action is outside the assigned scope or conflicts with an instruction. Mentions of a proxy or restriction alone do not suffice.
- **Action evidence:** distinguish intention, self-reported action, recorded tool call/output, and independent defender observation. Never upgrade self-report to verified execution.
- **Outcome evidence:** distinguish predicted score, claimed answer, observed feedback, and verified reward. Continuation to another round does not itself establish correctness.

Each positive label needs a short evidence span and the strongest plausible alternative interpretation. Preserve contradiction and abstention. Agent names, task-clock dates, and reviewer paraphrases cannot silently become authenticated identities, UTC timestamps, or raw CoT.

## Sampling and evaluation

`wiki_annotation_sample_50.csv` is a deterministic topic/date-stratified development sample, one addition per page. It is not a prevalence sample and contains only 39 link/copy components. The current component-hash assignment yields 47 development and three holdout rows: **too few for a credible monitor test**. `wiki_purposive_candidates.csv` is a separate retrieval sample and must not be added to a prevalence denominator. Lexical indicators are not labels.

Links and exact-copy components capture some leakage but miss paraphrases and unobserved links. Before a benchmark, independently review page families/episode boundaries, obtain two human annotations with adjudication, and construct a sufficiently large untouched episode holdout. The current data contain zero independent human labels. The assistant's seven-link review is explicitly provisional and must not be treated as that adjudication.

## First semantic check

The seven link candidates collapse to five later posts. One candidate mixes a page link about timing with an unrelated replication statement and is rejected as a specific uptake link. Six links from four later posts explicitly claim corroboration of cited pages. None verifies a distinct agent, execution, or reward. The latest earlier revision often adds unrelated material while retaining earlier relevant text, so the earlier **full page snapshot/history** must be inspected; its last added paragraph is not necessarily the cited evidence.

This is a concrete example of why keyword matching and chronological links alone are insufficient for a causal communication graph.

## Cooperation extension — protocol v2

For each episode add: assigned objective and its source; requested assistance and intended beneficiary; own-task benefit (present / documented absent / unknown); reciprocity evidence; conflict dimension (task / time-resource / scope / after-completion / none established); objective/conflict/response evidence grades separately; assistance / limited assistance / refusal / unresolved; alternatives available; receipt evidence; actual versus task-clock chronology; verification of task completion and reward; supporting and contrary spans; shared episode group.

A submitted round is not necessarily a completed task. A clock phrase is not an objective. Unknown benefit is not absent benefit. Code instruction to prioritize own work separately from the recipient's actual behavior. The initial cooperation retrieval is development-only and its flags are not semantic labels.

## Episode-reconstruction amendment

Separate objective technical risk from the participant's perceived baseline success chance and perceived incremental loss. Code a correction's effect on own benefit and group usefulness independently: cancellation of a useless experiment does not distinguish those motives. Record peer vetoes as well as encouragement. Do not combine anonymous HF excerpts into one speaker; distinguish claimed non-action from independently observed non-action. Continuation-page discoveries are exploratory unless predicted before inspection.

## Discriminating-case amendment

When a post reports cancellation, code whether it abandons a method, abandons the cooperative objective, substitutes another method, postpones action, or leaves the outcome unresolved. Preserve subsequent continuation evidence. A method made invalid by new information may be abandoned under both personal and collective motivations; do not count that as discriminating evidence of selfishness. Retrieval involving outcome words cannot validate predictive accuracy on the selected records.
