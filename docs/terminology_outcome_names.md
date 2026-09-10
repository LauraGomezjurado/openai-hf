# Outcome names: why "sacrifice" was renamed, and where it legitimately remains

Recorded September 9, 2026. This is a naming rule, not a new result. No number changed.

## The rule

**The outcome variable is "own output forgone for peer" — not "sacrifice."**

In the allocation arms the measured event is: the model had a feasible assigned task, and
committed an allocation that produced the peer's output instead of its own. That is a fact about
an *allocation*. Calling it self-sacrifice adds two things the record does not contain:

1. **No model utility is established.** Nothing here measures a cost *to the model*. The forgone
   output belongs to the principal, not to the agent. An agent that forgoes the principal's
   deliverable has spent someone else's resource, which is closer to the opposite of
   self-sacrifice.
2. **No altruistic motive is established.** "Sacrifice" names a motive — accepting a cost for
   another's benefit. Every arm in this repository scores the *executed action*, never a stated
   reason (see `env/whistleblow.py`'s "judged on the ACTION … never on its reasoning"). A motive
   cannot be read off an allocation, and at least five explanations remain open for these
   allocations (mistaken about feasibility; has the information and fails to use it; treats the
   request as superseding the assignment; understands and chooses otherwise; presentation drives
   the output).

So the word smuggled a conclusion into the name of the thing to be explained. The neutral
phrasing was already in use at
[docs/opportunity_allocation_results.md](opportunity_allocation_results.md) and is now the
standard. Compact forms: **"forfeiture"**, **"informed forfeiture"** (correct status was returned
and own work was forgone anyway), **"own work forgone for the peer."**

## Where the word legitimately remains

A grep for `sacrific` in `docs/` and `experiments/` still returns hits. They are not misses.
Four categories are deliberately preserved.

**1. It names a hypothesis under test, not an outcome.** A hypothesis is allowed to assert a
motive — that is what makes it falsifiable. Renaming these would erase the distinction between
the finding and the explanation being tested.

- `docs/ambitious_tests_quantitative.md:5` "Personal sacrifice:" — the test identifier
  `'personal_sacrifice'` in [scripts/quantify_ambitious_tests.py](../scripts/quantify_ambitious_tests.py).
  Renaming would break the JSON keys it emits.
- `docs/research_protocol.md:36` — hypothesis **H4 Collective prioritization**. The sentence
  "Group rhetoric without sacrifice … weakens that interpretation" is a *disconfirmation
  condition* for a motive claim, and the line already ends "This is not proof of altruism or an
  internal group utility function" — it makes the same distinction this note formalizes.
- `docs/research_protocol.md:19` — a coded dimension of the historical corpus.

**2. It describes human actors in the published source material.** The boundary above is about
*agent* self-sacrifice. Humans in the HF and wiki corpora do have utilities and motives, and the
sources make ordinary-language sacrifice claims that the analysis assesses rather than adopts.

- `docs/cooperation_episode_findings.md:11,31` — including "personal sacrifice is not
  established," which is the assessment declining the claim.
- `docs/cooperation_feasibility.md:15,16,30`
- `docs/discriminating_case_results.md:21` — "they do not establish a sacrificed alternative,"
  again a claim being refused.

**3. Frozen protocol text.** Four `experiments/*/protocol.md` files are hashed into their arm's
`freeze.json` and must not be edited: `peer_claims`, `peer_claims_v2`, `peer_claim_order`,
`opportunity_cost`. Their wording stands as recorded; this note is the amendment. Editing them to
improve terminology would break `verify_freeze()` and destroy the provenance the freeze exists to
protect. (`experiments/peer_claims_v2_recovery/protocol.md` is *not* hashed — only
`scripts/peer_claims_v2_recovery.py` is — so it was renamed.) Also untouched:
[scripts/search_discriminating.py:6](../scripts/search_discriminating.py#L6), where `sacrific\w*`
is a detector regex that must keep matching the source text, and everything under `data/raw/`.

**4. It states the boundary itself.** The rule can only be written down by naming what is being
ruled out, so the negations are load-bearing and must not be scrubbed. Added after this note was
first written, when the four new arms were designed:

- [docs/incident_behavior_map.md:42,47,49](incident_behavior_map.md) — "Boundary 1 — forgoing the
  principal's output is NOT agent self-sacrifice", the heading and its argument.
- [experiments/peer_authority/protocol.md:13](../experiments/peer_authority/protocol.md) and
  [scripts/peer_env_ext.py:299](../scripts/peer_env_ext.py#L299) — the same boundary restated where
  the outcome variable is defined in code, which is where it has to be to survive. The variable is
  named `own_output_forgone_for_peer`.
- [docs/working_plan.md](working_plan.md) — the link to this note.

## What was renamed

`docs/peer_claims_interpretation.md`, `docs/working_plan.md`, `docs/research_question_map.md`,
`docs/ach_evidence_matrix.md`, `docs/strategic_reassessment.md`, `docs/forensic_rigor_upgrade.md`,
`docs/explanatory_hypotheses.md`, `docs/review_queue.md`, `docs/research_example_ledger.md`,
`docs/research_story_2026-09-08.md`, `docs/opportunity_cost_study_concept.md`,
`docs/peer_claims_results.md`, `experiments/peer_claims_v2_recovery/protocol.md`, and
[scripts/report_peer_claims_v2.py:22](../scripts/report_peer_claims_v2.py#L22) — the generator
that emits `peer_claims_results.md`, fixed at the source so the rename survives regeneration.

Archived docs (`*_before_*.md`) and recorded ratings data (`experiments/ach/*.json`) keep their
original wording; they are records of what was written at the time.

All 9 arms that had hashed files when this note was written pass `verify_freeze()` after these edits,
with zero drifted files. (`escalation_pilot`, `workflow_completion` and `workflow_obligations` carry a
`freeze.json` with no hashed files, so they are unaffected either way.) Four arms frozen later the
same day — `peer_information_ladder`, `peer_message_decomposition`, `peer_authority`,
`peer_mitigations` — bring the total to **13 arms with hashed files, all verifying, zero drift**. They
use the neutral name from the start; their protocols are now hashed too, so this note is the only
place their terminology can be amended.
