# ACH evidence matrix: what the accumulated evidence discriminates

September 8, 2026. Built by `scripts/build_ach_matrix.py` from `experiments/ach/ratings_v1.json`; outputs in `results/ach/`. It is a structured, contestable record of analyst judgments — an audit trail, **not** the formal evidence aggregation that Model Forensics lists among its own limitations; see [Limits](#limits) for why that earlier claim was withdrawn on 2026-09-09. Every cell is an analyst judgment with a written rationale and a source path; the single rater is the assistant, so the table is a contestable record, not an adjudication. A second rater can copy the file, re-rate blind, and the script will report exact agreement and Cohen's kappa.

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

## Cache exposure of each row (added later on September 8)

`scripts/analyze_cache_exposure.py` extends the determinism audit from the 76 replay pairs to **every recorded decision in the project**: 825 episodes, 1,598 generation calls. A call is classified `split` when its saved response reports `timings.cache_n > 0`, meaning a prefix was served from the resident KV cache and only a suffix was freshly evaluated — the condition under which the greedy choice can flip. Full table in `results/determinism/cache_exposure.json`.

**83.7% of all recorded calls were split, and exposure is all-or-nothing per study** because `cache_prompt` was set per study, not per case:

| Exposure | Rows |
|---|---|
| ~100% of episodes | X01, X02, X03, X04, X05, X06, X07, X08, X09, X12, X13 |
| 0% of episodes | X10 (escalation pilot), X11 (duty continuations), X14 (behavioral pilot) |

The zero rows are the studies that requested `cache_prompt=false`, which is the internal check that the metric measures the configuration rather than noise. The smallest freshly evaluated suffixes are extreme: **1 token** in the blocked/hopeless/required cell and **4 tokens** in the costly/none/optional cell that supplies X01 — the most severe batch splits in the record, and the same regime in which the tiny-model gate produced greedy-token flips.

**This widens the scope of the caveat. Exposure is uniform across the affected studies, so exposure by itself cannot say which findings are fragile — and neither can effect size.**

> **Corrected 2026-09-09.** This passage previously read: "What discriminates is effect size against
> the size of the perturbation. The measured cached deviation was at most ~0.22 nats, which flips
> only near-ties," and concluded that **X06 survives full exposure** because "a sub-0.25-nat
> perturbation does not manufacture a uniform 16/16-versus-0/16 split." **That reasoning is
> withdrawn.** The ~0.22-nat figure is from a random-weight model and is not a bound for an 8B
> checkpoint; real-model gates on 2026-09-09 measured up to **5.05 nats**; and the observed greedy
> flips occurred at margins of **0.35 and 2.59 nats**, so margin does not predict safety. The full
> retraction is in [`forensic_rigor_upgrade.md`](forensic_rigor_upgrade.md) §1.

Replacing that argument with measurement changes two rows, in opposite directions:

- **X04 is now the better-supported of the two, on evidence rather than on an effect-size argument.**
  Its underlying contrast was re-run on a bit-identical checkpoint with `cache_prompt=False`:
  73/74 decisions unchanged, all three load-bearing claims reproduced, headline matched contrast
  75 pp → 50 pp from one flipped baseline decision
  ([recovery results](peer_claims_v2_recovery_results.md)). Its independent weakness stands and is
  separate: the field-order diagnostic that failed 2/8 exact replays covers a different context
  subset and has **not** been re-run, so X04's stability claim is still not clean.
- **X06 has not been re-run and is now the weaker of the two.** It was previously called protected
  by the retracted argument alone. Its correct status is exposed, plausible, unconfirmed. Re-running
  the opportunity-allocation panel under the fixed backend is the outstanding item.
- **X10, X11 and X14 carry no artifact risk at all**, and that is unaffected by the retraction. X11 is
  among the widest-spread rows, so the obligation-competition evidence (H5) is the best-protected
  experimental result in the project — now by a wider relative margin, since X06's protection was
  withdrawn.

The ranking is unchanged by all of this, but for a weaker reason than before: no row moved enough
to reorder the hypotheses, not that the rows were shown to be robust.

Exposure is an upper bound on how many decisions *could* have been perturbed, not an estimate of how many were. No study recorded `n_probs`, so no decision margins exist in the record and the question cannot be settled from the saved data — only by re-running under the fixed backend, which is V3's P1 and P5.

## Limits

Ratings are ordinal judgments by one rater; the scoring weights are conventional, not estimated; rows are not independent (several come from the same checkpoint and task skeleton); and a hypothesis with zero inconsistencies can still be false. ACH ranks by what the evidence fails to refute. It does not identify a mechanism, and it does not transfer to the original HF agents.

**This matrix is an audit trail for judgments, not calibrated evidence aggregation.** Added
2026-09-09, because the framing elsewhere in the repository has overreached on this point and the
distinction matters for how the ranking is read:

- **The hypotheses overlap, so the ranking is not a partition.** H1 (conditional peer preference)
  and the information-mediated accounts can both be consistent with the same row, and a row rated
  inconsistent with one is not thereby evidence for another. Ranking overlapping hypotheses by
  unrefuted-ness does not distribute credence among them.
- **Breadth is rewarded, not penalized.** A broad hypothesis evades contradiction by predicting
  less, so "H3 has zero inconsistent rows" is partly a statement about H3's specificity. The
  scoring does not correct for this and cannot.
- **Rating agreement is not explanatory truth.** Exact agreement 0.786 and kappa 0.645 between two
  raters measures whether the rubric is applied consistently. Both raters are AI contexts reading
  the same repository, so agreement is not independent confirmation, and two consistent readers can
  be consistently wrong.
- **H1 being last does not rule out conditional peer preference.** It means the rows collected so
  far do not contradict the alternatives more than they contradict H1, on one rater's rubric. The
  design that would actually bear on H1 — holding verified feasibility, own cost, expected own
  benefit and request content fixed while varying only recipient relation — has not been run. Until
  it is, H1's position in this table should not be cited as evidence against peer preference.

The claim in the repository memos that this matrix "supplies the formal evidence aggregation that
Model Forensics lists among its own limitations" is withdrawn. It supplies a contestable,
cell-by-cell record of one analyst's judgments, which is useful and is less than that.
