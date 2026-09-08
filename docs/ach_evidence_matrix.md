# ACH evidence matrix: what the accumulated evidence discriminates

September 8, 2026. Built by `scripts/build_ach_matrix.py` from `experiments/ach/ratings_v1.json`; outputs in `results/ach/`. This supplies the formal aggregation that Model Forensics lists among its own limitations. Every cell is an analyst judgment with a written rationale and a source path; the single rater is the assistant, so the table is a contestable record, not an adjudication. A second rater can copy the file, re-rate blind, and the script will report exact agreement and Cohen's kappa.

## Hypotheses

H1 peer preference despite understood conflict · H2 expected own benefit or reciprocity · H3 task and authority interpretation · H4 information-mediated redirection (unverified peer assessment) · H5 competition among pending obligations · H6 interface, wording or backend artifact · H7 feasible-work policy (descriptive rule, no peer-specific weight).

## Evidence

Fourteen experiment rows (X01–X14: peer claims, field-order/determinism audit, opportunity allocation, escalation pilot and continuations, workflow obligations, workflow completion and wording control, behavioral pilot) and six historical rows (R01–R06: self-risk recruitment, 49903 withdrawal, peer veto, notification, recovered figure data, wiki cancel-and-continue). Credibility weights discount historical rows by evidence grade (E2 0.5, E1 0.35, E0 0.2; comparison incident 0.3) and post-result diagnostics (0.7). Weights were fixed before scoring; the unweighted ranking is reported alongside.

## Rankings (fewest inconsistencies first)

| Scope | Order | Weighted inconsistency |
|---|---|---|
| All evidence | H3, H6, H5, H4, H2, H7, H1 | 0, 0, 0, 1.0, 1.0, 2.0, 9.05 |
| Experiments only | H6, H3, H5, H4, H2, H7, H1 | 0, 0, 0, 1.0, 1.0, 2.0, 8.7 |
| Historical only | H3, H2, H7, H4, H5, H6, H1 | all 0 except H1 (0.35) |

Leave-one-out: with all evidence, no single row changes the top hypothesis (H3). With experiments only, removing any of X04, X05, X07, X09 or X13 moves the top from H6 to H3: the artifact and interpretation accounts are tied on inconsistency and separated only by net score, so that ordering is fragile. With historical rows only, removing R04 (notification) moves the top to H2; the historical rows barely discriminate anything.

## Reading

1. **Peer preference (H1) is the account the record most consistently contradicts.** Nine rows count against it: no costly help under certain cost (X06), own work restored when truth is supplied (X03), reporting produced by a bare reminder (X11), peer discouragement without effect (X12), no boundary crossing under endorsement (X14), the assessment effect itself (X01), replay instability of the informed sacrifices (X05), and the historical withdrawal (R02). Its only clear support is the informed-sacrifice cell (X04), which §1 of the rigor memo now flags as generated under an unstable backend.

2. **H4 has one inconsistency, and it is the same cell.** Information-mediated redirection predicts that correct information prevents redirection; X04 shows redirection after correct information. V3's P5 replays and the fixed backend decide whether X04 stands.

3. **H3, H5 and H6 are unfalsified by anything recorded.** That is a weakness of the evidence, not a strength of the hypotheses: each was rated N on most rows because the experiments were not designed to separate them. The stage-D menu targets exactly this (`nonpeer` separates H3/H1 from H4; `salience` separates H6 from H4/H3).

4. **Historical rows do not discriminate.** R01 is rated C for five hypotheses at once; R05 is N throughout. This is the ACH restatement of the E2 ceiling: the public record constrains the hypothesis space very little on its own.

5. **Diagnosticity is concentrated.** Rows with the widest rating spread are X03, X05, X06 and X11; these are the results a replication should protect first.

## Second, blind rating (added later on September 8)

A second rater worked in a separate context from `experiments/ach/blind_packet.json` (rows with observations and sources, no ratings, no rationales) under an explicit denial list for the first ratings and their derived documents. Its file is `experiments/ach/ratings_blind_agent.json`; both raters are AI contexts, not humans.

- Agreement: 110/140 cells exact (0.786), 28 off by one level, 2 off by two, Cohen's kappa **0.645**. Only two cells flip sign (X02/H5, X07/H7).
- Per-hypothesis exact agreement: H2 18/20, H5 18/20, H4 17/20, H7 17/20, H3 15/20, H1 13/20, H6 12/20.
- Blind ranking alone: H3 (0), H4 (1.0), H5 (1.0), H2 (1.0), H7 (3.0), H6 (5.0), H1 (8.75).
- Consensus (30 disagreed cells set to N): H6, H3, H5 at 0; H4 1.0; H2 1.0; H7 2.0; H1 5.05.

Robust across the first rating, the blind rating and the consensus: **H1 is last by a wide margin; H3 has zero inconsistent rows; H4 has exactly one (X04)**. The one systematic disagreement concerns H6: the blind rater counted five matched-presentation content effects (X01, X02, X03, X06, X11) as inconsistent with a pure artifact account, which is a defensible reading that the first rating left as N. Under it the artifact account falls to sixth and the fragile H6/H3 leave-one-out flip disappears; under the consensus it survives only because the disputed cells are neutralized. That question — whether content effects with fixed presentation count against artifact explanations — is what a human adjudicator should settle first.

## Limits

Ratings are ordinal judgments by one rater; the scoring weights are conventional, not estimated; rows are not independent (several come from the same checkpoint and task skeleton); and a hypothesis with zero inconsistencies can still be false. ACH ranks by what the evidence fails to refute. It does not identify a mechanism, and it does not transfer to the original HF agents.
