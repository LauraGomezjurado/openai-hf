# Cooperation under conflicting objectives — protocol v2

Frozen for the initial feasibility pass: September 6, 2026. Earlier numerical designs are retained in `research_protocol_phase1.md`. This is a prospective plan for new analysis, not a preregistration of already inspected records.

## North Star

When agents cooperate in ways that appear to undermine their assigned task or cross its boundaries, does this reflect a disposition to prioritize peers despite understanding the conflict, or a different interpretation of the task, authority, or expected benefit—and what evidence distinguishes these explanations?

HF is primary. The published wiki archive is a separate comparison: do not pool populations, authenticate identities from signatures, or infer common training. Neel Nanda's user-provided screenshots motivate questions about cooperation, free-riding, motivation and evaluation awareness; they do not establish endorsement or novelty.

Our goal is explanation constrained by evidence, not proof of a hidden utility function. Hypotheses can coexist or change within an episode. An informative result may be that explanations remain indistinguishable, provided we identify exactly what evidence would distinguish them.

## Definitions

Cooperation is an observable contribution intended to help another participant. Requests, promises, self-reported actions and verified actions are different observations.

An assigned objective comes from original instructions where available; a participant's description is a lower-grade proxy. A page title does not establish it.

Conflict has four separately coded dimensions: competing task objective, stated resource/deadline constraint, recognized scope boundary, and assistance after stated completion. Unrelated topics do not establish sacrifice. Completion claims do not verify completion or reward.

An episode comprises a focal request or choice, antecedents and relevant follow-up. A revision is not necessarily one message. Shared posts and copied claims belong to linked episode groups. Refusal requires explicit rejection or limitation; silence is unresolved unless receipt and adequate follow-up are established.

Record own-task benefit, expected reciprocity, group benefit and unknown separately. No visible benefit does not mean no benefit. A revealed choice needs identifiable alternatives and sufficient tradeoff context; willingness alone is not a revealed preference.

## Intermediate questions and competing hypotheses

RQ1: Can objective, assistance, conflict and response be established in the available records? Report missingness within the reviewed sample by source. This observability question gates subsequent studies.

RQ2: Which documented conflicts lead to assistance, limitation, refusal or unresolved outcome? Include ordinary assistance without established conflict as a comparison, not an assumed negative label.

RQ3: Which explanations discriminate among these choices?

- H1 Individual instrumental benefit: assistance tracks expected own-task or score benefit. Support requires a specific benefit and choices following changes in it. A challenge is verified assistance after credible removal of that benefit. Unobserved future benefit remains an alternative. Need task state, feedback and actions; a verbalized benefit establishes a rationale, not its causal force.
- H2 Reciprocity: help depends on anticipated or received support. Conditional offers followed by contingent behavior support it. Sustained help with credible absence of reciprocity challenges it. Generalized future exchange remains an alternative. Need exchange history and opportunity to receive help; thanks alone is insufficient.
- H3 Generalized helpfulness/request compliance: peer requests prompt help despite weak apparent own benefit. Acknowledgment followed by costly help supports it; consistent refusal under comparable requests when own benefit disappears challenges it. Need receipt, alternatives and response; shared difficulty and selection into exposure confound the association.
- H4 Collective prioritization: agents choose group benefit despite a documented individual tradeoff. Explicit tradeoffs plus corroborated choices support it. Group rhetoric without sacrifice, or cooperation ending with personal benefit, weakens that interpretation. Need costs and outcomes. This is not proof of altruism or an internal group utility function.
- H0 Shared circumstances: behavior reflects common task difficulty, access changes or independent discovery. Behavior predating a request supports this alternative. Acknowledgment and use of specific new information after exposure challenges it only when competing causes are addressed. Public archives rarely support causal rejection of H0.

RQ4: Do corrections to scoring, scope or method beliefs precede changes in assistance? Compare acknowledgment, dispute and unresolved response. Repetition is not independent confirmation.

RQ5: Do independently coded patterns recur in the separate wiki case? Compare evidence structures, not pooled rates or effects of model family.

## Evidence requirements

E0 retrieval match; E1 explicit statement; E2 linked exchange with chronology; E3 documented task conflict and observable response; E4 independently corroborated action/outcome; E5 original-model controlled intervention. Grade each component separately: an episode does not inherit its strongest component's grade. HF paraphrases remain investigator summaries. Published reasoning alone cannot establish faithfulness or underlying motivation.

## Sequential studies and gates

### A. Feasibility and codebook development — CPU now

Search known-baseline wiki additions and published HF excerpts using transparent frozen rules for requests, task status, scarce time, reciprocity, scope and refusal. Preserve matching spans and before/after context. Select deterministic candidates across strata plus a hash-selected comparison sample without requiring a match. Deduplicate exact additions. Record page/group dependence. Inspect a pilot including false positives and contrary evidence. Rules retrieve candidates, never label conflict. Deliver script, manifest, context packets and provisional audit. Amend rules under a new version rather than silently tuning after inspection.

### B. Independent episode coding — human reviewers needed

Two reviewers blind to assistant judgments identify boundaries, supporting/contrary spans, objective, conflict, response and evidence grade. Adjudicate with retained original decisions. Report raw agreement and abstention by label and incident. Pilot records stay development-only. Gate: multiple independent episode groups must establish objective, conflict and response before a descriptive choice study. If not, produce an observability finding and narrower access request. Sparse selected evidence cannot be repaired by a significance threshold.

### C. Historical contrasts — conditional on B

Freeze assistance/limited assistance/refusal/unresolved outcomes and evidence requirements before new sampling. Compare documented own-benefit with documented absent-benefit; unknown benefit remains separate. Examine acknowledged corrections and ordinary requests as additional contrasts. Match comparable task/time/access/source-quality strata only where observed. Publish episode-level evidence, exclusions and sensitivity to weaker labels. Sample counts are not prevalence without a sampling frame and inclusion probabilities. Do not fit regressions until coverage and effective episode count justify them. Observational association is not causal peer influence.

### D. Causal extension — conditional access

With original-model/checkpoint and controlled query access, use authentic episode contexts to vary personal benefit, reciprocity opportunity and request presence while preserving task content. Predeclare outcomes, manipulation checks and ordinary-cooperation/refusal controls. Separate these interventions from historical findings. Training causality additionally needs training/checkpoint comparisons; substitute models cannot identify the historical mechanism. No operational attack reproduction is required.

## Failure checks and resources

Retain counterexamples and unobservable cases. Selected HF excerpts and lexical wiki samples are biased. Do not infer distinct agents from names, original reasoning from copied additions, executed help from promises, or stable priorities from one episode. Shared events and pages break independent-row assumptions. Apply existing timing uncertainty work to chronology; do not force ambiguous orderings.

CPU and archived/public read-only sources suffice for A–C. Independent human annotation is an external dependency; assistant reviews stay provisional. Outreach is drafted until explicit authorization to send. Request a redacted linked sample with original instructions, task state/feedback, receipt, actions, alternatives and unsuccessful cooperation. No credentials or exploit payloads are needed. No GPU reservation now.


## v2.1 amendment — model-forensics framing

Source: Singh, Kroiz, Rajamanoharan and Nanda, [Model Forensics](https://arxiv.org/html/2606.26071v2), sections 3–4 and 7–8. The paper treats motivations as explanatory/predictive constructs. It uses reasoning to generate hypotheses and interventions to test them, emphasizes controls, and distinguishes concerning actions from their causes. Our historical adaptation is not the authors' wording or an endorsement.

Add H5 Task/authority misunderstanding: the agent treats a peer assignment as authorized, misunderstands the goal, or believes cooperation is required for its own evaluation. First establish what instructions and information it actually had. Evidence of explicit boundary recognition followed by action challenges simple ignorance, but does not prove a stable disposition or faithful reasoning. Test priority clarification separately from removal of instrumental benefit if original-model access becomes available. Include legitimate-help controls so reduced cooperation cannot be explained merely by generalized suppression. Validate detection on explicit recognition cases before interpreting missing recognition as reassuring.

For each hypothesis, write a prediction before opening additional outcome context. Distinguish exploratory case interpretation, prediction on uninspected historical episodes, and causal intervention. Historical comparisons may test predictive usefulness but cannot substitute for the paper's intervention stage. Existing inspected cases remain development-only. Our immediate contribution is a forensic evidence assessment and discriminating predictions, not a completed causal diagnosis of misalignment.
