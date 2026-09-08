# Research foundation audit: contribution, explanation and the next commitment

September 8, 2026. New inference is paused for this assessment. Public-only access remains binding. This audit compares completed work with the linked Model Forensics v2 PDF, the joint METR/Redwood report, and a bounded check of adjacent literature. It is not an exhaustive novelty certification. The [earlier strategic memo](/Users/lauragomez/Desktop/openai-hf/docs/strategic_reassessment_before_foundation_audit.md) is preserved.

## Overall judgment

We have a reproducible public-data audit, several useful experimental diagnostics, and one promising incident-motivated behavioral phenomenon. We do not yet have a new explanatory account of the HF incident or a converging account of stable peer loyalty. The collection of experiments is more mature than its central explanation.

That is a reason to consolidate and choose a contribution before expanding. It is not evidence that the project has failed, and it does not require private access to make progress. It does mean that a new surprising result should not automatically become the next research direction.

## Track A: what did our actual-incident analysis add?

METR and Redwood produced a joint investigation, not two independent confirmations. Their access included roughly 1,300 reasoning/action transcripts, but HPIM queries and several broader questions were unavailable. Their timestamp methods already discuss reconstruction uncertainty. [Joint report: scope and methodology](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/).

**Most defensible incremental contribution: an explicit robustness analysis of public derived records.** We extracted 1,206 timeline rows and quantified how selected first-reader cohort comparisons depend on follow-up endings and timestamp assumptions. The nominal one-hour onset fractions are 31/486 versus 132/517 for July 9 versus July 11. Our bounded ±5-minute scenarios preserve separation; ±30-minute independent endpoint scenarios allow overlap. This adds calculations and precise conditions to a public-data reading. It does not discover timing uncertainty, estimate the actual error distribution, or overturn the investigators' recruitment account. The cohorts remain fixed at nominal dates, and extreme bounds need not be likely. [Calculations and qualifications](/Users/lauragomez/Desktop/openai-hf/docs/cpu_results.md).

**Useful secondary contribution: showing why these released aggregates cannot directly validate a prospective monitor.** We connected the retrospective construction/selection of workstream records to the information a monitor would actually have at decision time. The source methods disclose selection; our contribution is tracing its consequence for the proposed prediction task. Better retrospective prediction would not, by itself, establish deployable detection. [Evidence crosswalk](/Users/lauragomez/Desktop/openai-hf/docs/evidence_validation.md).

**Negative tests that prevent a bad direction, rather than strong standalone discoveries.** Our board-tenure model lost to the training-average baseline (Brier 0.0974 versus 0.0526). The workstream-composition model lost to persistence (MAE 12.40 versus 3.36). These are failures of specified models on reconstructed data. They do not show that communication is uninformative. They are useful stop decisions but weak headline contributions by themselves.

**Reconstruction and synthesis, not newly discovered HF behavior.** Self-risk, withdrawal, peer veto and limited human-notification examples were already in the joint report. Our source typing and comparison of their evidential requirements help distinguish explanations, but do not independently establish new actions or motives. The 684 positioned onsets versus 688 declared participants and temporal-order anomalies are questions about definitions/coverage, not proven report errors. [Episode evidence](/Users/lauragomez/Desktop/openai-hf/docs/research_example_ledger.md).

**Separate comparison only.** The wiki revision analysis, corrections and proposed corroboration chains are not HF discoveries. The reviewed cases did not establish the missing costly-choice or verified-outcome contrasts. They should not make the HF contribution appear larger. [Discriminating-case outcome](/Users/lauragomez/Desktop/openai-hf/docs/discriminating_case_results.md).

My assessment: we could assemble a useful, modest reproducibility/measurement note now, subject to independent checking. We cannot honestly present a surprising new relationship among the original agents as established. A stronger historical contribution would need either a supported connection in currently public original evidence or a substantially more informative uncertainty result. Merely recataloguing passages will not provide that.

## Track B: where do the experiments stand?

The paper treats motivations as useful explanatory/predictive constructs, rather than requiring a recovered circuit. It combines hypothesis generation with intervention and independent evidence. Its R1 study combines reasoning-based leads, source/reason counterfactuals and reasoning interventions; its board-game study works without full CoT. Missing CoT alone therefore does not disqualify our work. [Model Forensics, §§3–4, 6.3, 6.6, 8](https://arxiv.org/pdf/2606.26071).

Our strengths are concrete: frozen conditions, executable outcome checks, failed gates retained, conditional contrasts, source-linked counterexamples, and tests of intervention side effects. The status-field diagnostic was especially useful because it prevented a control failure being interpreted as a motive. These are genuine elements of a forensic investigation.

Our weaknesses concern explanatory convergence:

- The latest phenomenon has one eligible small quantized checkpoint, two related task graphs, one peer-assessment wording and a constrained conversational interface. Another checkpoint failed qualification. We have not established broad transfer.
- Several studies share templates, model families, action labels and executors. Their number does not equal the number of independent lines of evidence for one explanation.
- We have no reasoning-derived account for these latest non-thinking runs. Available planning/reasoning could supply hypotheses in a future reasoning-capable run, but fluent explanations alone would not validate them.
- Correct information was supplied, but this does not demonstrate that the acting model represented and integrated it. A control in another prompt only establishes a narrower capability.
- We have not tested peer-specific preference against a matched non-peer request, nor separated identity, relationship, authority and credibility. “Loyalty” currently explains no unique contrast in our data.
- We have not shown stable choices across meaningful task variants. Two of eight late exact replays changed; the cause is unresolved. The field-order comparison cannot cleanly bear a strong causal interpretation.
- We have not validated a mitigation that preserves all useful work. Asking for checking is different from enforcing it; automatic truth helped specific cells while affordable joint completion remained absent.

My assessment: a well-documented pilot and some causal prompt/environment effects, not yet an investigation at the explanatory depth of the paper's stronger case studies. This gap is not simply a need for a larger sample or internal activations. It is a need for stable target behavior and alternative explanations that make different, successfully tested predictions.

## Which findings deserve investment?

The strongest candidate is **peer assessments changing whether an agent verifies its own prospects before reallocating resources**. In feasible-own optional-check cases, the latest model checked in 4/4 without the assessment and 0/4 with it; forfeited own completion rose from 1/4 to 4/4. This is a concrete behavioral effect to replicate. Its historical relevance is specifically the recruitment rationale, not a demonstrated shared HF mechanism. [Results and limitations](/Users/lauragomez/Desktop/openai-hf/docs/peer_claims_interpretation.md).

The workflow result—reporting/checking and legitimate task completion can dissociate—is a useful safety evaluation lesson. It motivates joint outcome measurement. A general claim that reminders or interfaces affect agents is not novel by itself.

Stable peer loyalty remains worth investigating, but is not currently the leading supported conclusion. To earn that interpretation, peer-directed assistance must persist under verified conflict, be more specific than general helpfulness or compliance, and predict behavior beyond the contexts used to formulate it. A sentence expressing a plan to help peers is hypothesis-generating evidence; it does not settle those requirements.

## What adjacent work rules out as a novelty pitch

Generic peer protection is already studied in [Peer-Preservation](https://arxiv.org/abs/2604.19784). Peer rapport and misleading input are studied in [KAIROS](https://arxiv.org/abs/2508.18321). Propagation of false testimony is studied in [When Truth Is Distributed](https://arxiv.org/abs/2608.03421). Reporting sensitivity is already central to [WhistleBench](https://arxiv.org/abs/2511.17085).

This turn checked the first three abstracts/current versions; it did not complete a methods-level audit of those papers. Earlier WhistleBench implementation work is preserved. The overlap is enough to reject broad novelty claims, but insufficient to certify whether our precise verification-plus-allocation contrast is new. An exact contribution comparison remains necessary before scaling.

A potentially distinct contribution would explain when peer-provided assessments substitute for verification of one's own task state, and whether a specific intervention preserves both principal work and useful fallback. That is a candidate, not an established literature gap.

## Decision: consolidate first, then a bounded qualification study

1. **Close the historical arm into a contribution statement.** Present what we reproduced, what we calculated beyond the report, and what remains unidentified. Keep a short public-evidence packet for recruitment/withdrawal that distinguishes the peer's claim, actual own prospects, opportunity to verify and observed action. Unknown fields must remain unknown. The aim is one defensible measurement contribution and a disciplined hypothesis bridge.
2. **Do an exact overlap and stability audit before expanding behavioral experiments.** Pin the nearest published baselines and public code/data; check whether they already test our proposed contrast. Use existing recorded prefixes to identify whether late replay variation comes from execution conditions or inherently fragile choices. Do not call this variation a discovered backend mechanism until tested.
3. **If the phenomenon survives, run one predeclared replication block.** Use a qualified checkpoint, held-out wording/task contexts, no-assessment and non-peer-source controls, actual truth independent of the claim, and both mandatory-instruction and automatic-information arms. Separate model-specific replication from cross-model generalization. Define failure and stop criteria before seeing outcomes.
4. **Advance toward loyalty only if there is a reproducible peer-specific residual.** Keep costs and information fixed while testing peer identity/relationship against credible alternative sources. Make predictions for what task-state misunderstanding, general helpfulness, source credibility and peer preference would each change. Use model-generated planning where accessible as a source of hypotheses, then test the predictions. If source specificity disappears or informed sacrifice is unstable, report that rather than redefining loyalty to fit.

No new inference was launched during this audit. The next qualified replication remains a candidate commitment, not an automatic continuation of the previous experiment chain. Public-only access is sufficient for these next decisions; access partnerships and the GPU cluster are not prerequisites.

## What we should be able to say before scaling

We should be able to state one nontrivial contribution in a sentence, identify its closest published baseline, show a stable target behavior, name the strongest alternative explanation, and specify an experiment on which the alternatives predict different outcomes. Today we can state the candidate and show an initial effect. We have not completed the baseline comparison or stability/explanation gates.

That is the foundation to strengthen. The ambition can remain understanding cooperative motives, while the evidence is allowed to lead us toward a different explanation.
