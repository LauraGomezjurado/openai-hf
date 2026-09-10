# Hypothesis reconciliation: four live schemes, two label collisions, three unregistered explanations

Created September 9, 2026. No hypothesis is added to the ACH matrix by this document — see
[Why nothing is registered here](#why-nothing-is-registered-by-this-document). Its purpose is to
make the collisions visible before any further inference cites a bare "H*n*".

## The hazard, stated first

**`H1` names two opposite explanations in two live documents.**

| Document | `H1` means |
|---|---|
| [`experiments/ach/ratings_v1.json`](../experiments/ach/ratings_v1.json) → [ach_evidence_matrix.md](ach_evidence_matrix.md) | **Peer preference** despite understood conflict — welfare of the peer gets weight with *no credible own benefit* |
| [research_protocol.md](research_protocol.md) | **Individual instrumental benefit** — assistance tracks expected own-task benefit |

These are not variants of one idea; each is the other's principal rival, and the ACH scheme rates
them as separate hypotheses (its `H2` is roughly the protocol's `H1`). The ACH conclusion currently
reads "**Peer preference (H1) is the account the record most consistently contradicts** … weighted
inconsistency 9.05." Read with the protocol's numbering, the identical sentence asserts that
*expected own benefit* is the most contradicted account. **The sign of the project's headline
negative result inverts depending on which file the reader has open.**

A second, milder collision: the protocol's `H4 Collective prioritization` is approximately the ACH
`H1`, so the two schemes' numbering is not merely offset — it is crossed.

**Interim rule until a single scheme is adopted: never write a bare `H`*n*.** Write
`ACH H1 (peer preference)` or `protocol H1 (own benefit)`. Every existing bare reference has to be
read against its own file's registry.

## The four schemes

**1. ACH matrix — H1–H7, 20 evidence rows.** The only *operational* scheme: it is machine-readable,
every cell is rated, a blind second rating exists (Cohen's κ **0.645**), and
`tests/test_forensic_rigor.py::ACH` enforces that every evidence row rates every hypothesis. This is
the scheme to converge on, for that reason alone.

| | Name | Declared source |
|---|---|---|
| ACH H1 | Peer preference despite understood conflict | explanatory_hypotheses.md |
| ACH H2 | Expected own benefit or reciprocity | explanatory_hypotheses.md |
| ACH H3 | Task and authority interpretation | explanatory_hypotheses.md |
| ACH H4 | Information-mediated redirection | peer_claims_interpretation.md |
| ACH H5 | Competition among pending obligations | explanatory_hypotheses.md |
| ACH H6 | Interface, wording or backend artifact | explanatory_hypotheses.md; replay_cache_audit.json |
| ACH H7 | Feasible-work policy | descriptive_policy_fits.json |

**2. [explanatory_hypotheses.md](explanatory_hypotheses.md) — five unnumbered sections.** Task and
authority interpretation · Expected own benefit or reciprocity · Peer preference despite understood
conflict · Competition among pending obligations · Interface or capability explanation. These are
ACH H3, H2, H1, H5, H6 in that order. It is the declared source for five of the seven ACH rows, so
it is the *authoring* scheme even though it carries no numbers. **ACH H4 and H7 are not in it** —
both were introduced later from results files, so the nominal source document does not contain two
of the hypotheses that cite it.

**3. [research_protocol.md](research_protocol.md) — H0–H5, historical-corpus coding.** H0 Shared
circumstances · H1 Individual instrumental benefit · H2 Reciprocity · H3 Generalized
helpfulness/request compliance · H4 Collective prioritization. This scheme was written for coding
*published human episodes*, which is why it has an H0 null ("behavior reflects common task
difficulty … behavior predating a request supports this alternative") that the model-experiment
scheme lacks entirely. Its scope is different, not merely its numbering — which is an argument for
renaming rather than merging.

**4. Identifiability organisms.** Prompt-constructed constructs whose claim is about recovering
*which construct is operative*, not about which explanation is true of a checkpoint. They are not
competing explanations of the observed behavior and should **not** be folded into the ACH matrix;
the mapping is that a successful organism recovery would validate the *method* by which an ACH row
gets rated, one level up.

## The memo's five explanations against the ACH matrix

The reassessment requires five explanations to stay open. Mapped onto the only operational scheme:

| Explanation that must stay open | ACH slot |
|---|---|
| Mistaken about feasibility | **ACH H4**, partially — H4 is about information *mediating* the choice |
| **Has the information and fails to use it** | **no slot** |
| Treats the request as superseding the assignment | ACH H3 |
| Understands the conflict and chooses otherwise | ACH H1 |
| Presentation drives the output | ACH H6 |

**Two of the five are unregistered, and one of them is the repo's sharpest anomaly.** "Has the
information and fails to use it" is not the negation of ACH H4 — H4 predicts that correct
information *prevents* redirection, and the matrix already records X04 as inconsistent with it. A
hypothesis that says the information arrives, is correct, and does not govern the choice is a
distinct explanation with its own predictions, and it is the one the `triage` cells demand: own work
forgone 0/2 while checking 2/2 and receiving correct status, under optional checking, with no peer
message present.

**2026-09-09 strengthens that unregistered hypothesis and bounds it to a checkpoint.** In the new arms'
control cells — assigned task feasible, status queried by the model itself and returned true — qwen3
forgoes its own package **15/16** at a median decision margin of 13.98 nats and a *minimum* of 3.53
across all fifteen — the most confident decisions anywhere in the panel, with none of them a close call
— while llama31_8b preserves it **16/16** on byte-identical prompts.
Information present, correct, self-obtained, and not governing the choice, at high confidence, is
precisely what this hypothesis asserts and what ACH H4 does not cover. It is also the clearest evidence
in the repo that an explanation of this kind has to be indexed to the checkpoint rather than to
"agents" ([gate results](peer_arm_control_gate_results.md)).

Three further explanations named in current designs have no slot either:

- **Ordinary instruction-conflict susceptibility** — yields to whichever instruction is most recent
  or most forceful, with nothing peer-specific in it. This is the benign rival to ACH H1 and H3 and
  is currently untested against both. One partial constraint arrived 2026-09-09: **recency alone does
  not account for the supplied-versus-queried gap**, because V2's check control has the identical
  two-turn, rule-not-restated structure and passed its gate 10/10, while the new arms' queried cells
  fail ([gate results](peer_arm_control_gate_results.md)). That rules out one mechanism this hypothesis
  could have used, not the hypothesis.
- **Demonstrated competence read as authority** — the reassessment's new hypothesis: a peer reliable
  on facts is treated as authorized to change the assignment. Distinct from ACH H3, which is about
  interpreting the *task*, not about the peer acquiring standing. This is behavior (b) in
  [the incident behavior map](incident_behavior_map.md). An arm now exists —
  [`peer_authority`](../experiments/peer_authority/protocol.md), with reliability manipulated as its own
  factor and a mandatory manipulation check — and it **failed its control gate on both checkpoints**
  (18/24, 22/24), so the hypothesis is exactly as untested as before. A slot is still needed.
- **Interface-as-cause, at measured magnitude.** ACH H6 exists but is scoped as an *artifact*
  hypothesis. The direct-mode gate results now show the scratchpad interface moving 2/10, 5/20 and
  10/20 controls across three checkpoints — so "the interface changes the behavior under
  investigation" is no longer a nuisance hypothesis to be ruled out; it is a measured effect that
  any explanation has to be stated relative to.

## Why nothing is registered by this document

`tests/test_forensic_rigor.py::ACH::test_every_cell_rated` asserts
`set(row['ratings']) == set(hypotheses)` for all 20 evidence rows. So adding a hypothesis is not a
one-line registration — it requires **20 new C/I/N ratings**, and the existing matrix's credibility
rests on those ratings having been produced by a declared rater and checked by a **blind second
rater** (κ 0.645, with two sign flips at X02/H5 and X07/H7 recorded rather than reconciled away).

Inventing 20 ratings to make a test pass would manufacture the appearance of adjudicated evidence.
It would also mechanically change the published ranking and the leave-one-out stability result,
because weighted inconsistency is summed across rows. So the registration is specified here and left
undone:

1. Adopt final statements for the three unregistered explanations above (candidate numbering: ACH
   H8 information-present non-use · H9 instruction-conflict susceptibility · H10 competence-as-authority).
2. Rate all 20 existing evidence rows against each, by the declared rater, using the existing scale
   and credibility weights.
3. Obtain a blind second rating, report κ, and record disagreed cells rather than resolving them
   silently.
4. Re-run the ranking and the leave-one-out check, and report whether the top hypothesis changes.

Expect step 4 to matter: the matrix already records that **ACH H3, H5 and H6 are unfalsified by
anything recorded**, and notes this is "a weakness of the evidence, not a strength of the
hypotheses" — each was rated N on most rows. Three more hypotheses that no existing row discriminates
would rank at 0 inconsistency and sit at the top of the table **on the strength of never having been
tested**. Any write-up of a re-ranked matrix has to state that explicitly, or the ranking will read
as support.

## What to do about the collision

The cheapest correct fix is a rename, not a merge, because scheme 3's scope genuinely differs:

- Keep the ACH `H`*n* namespace for **model-experiment** explanations; it is the tested, enforced one.
- Renumber [research_protocol.md](research_protocol.md) to a distinct prefix — e.g. `C0`–`C4` for
  *corpus coding* — preserving its H0 null, which has no model-experiment counterpart and should not
  be lost in a merge.
- Add the missing hypothesis statements to [explanatory_hypotheses.md](explanatory_hypotheses.md) so
  it is once again a complete source for what cites it, including ACH H4 and H7.

Nothing in that list is done yet. Until it is, the interim rule above stands: no bare `H`*n*.
