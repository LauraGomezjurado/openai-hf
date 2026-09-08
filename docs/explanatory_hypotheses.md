# Explanatory hypotheses: historical leads and distinguishing tests

This register preserves the ambitious motive question. It is a development document, not a preregistration or a diagnosis of the HF agents. Several explanations can coexist. Existing HF examples are already inspected and cannot serve as fresh held-out validation.

## Task and authority interpretation

Candidate account: the agent treats peer work or peer-board decisions as legitimately authorized, or treats human reporting as outside its own role.

Historical lead: METR's role/route/board discussion and peer consent/veto example. Explicit recognition of a scope boundary challenges simple ignorance, but a quoted acknowledgment does not establish a consistent internal priority ordering.

Distinguishing prediction: clarifying authority while keeping the substantive peer request, own-task benefit and assistance cost fixed should selectively change the conflicting action if ambiguity is driving it. Legitimate peer help should remain possible. A permission manipulation that changes what is actually allowed tests rule sensitivity; it does not isolate mistaken interpretation of unchanged rules.

Our evidence: explicit-permission copying choices and duty/route effects are compatible with this account. We have not isolated historical misunderstanding or measured the original agents' beliefs.

## Expected own benefit or reciprocity

Candidate account: helping peers is instrumentally useful to the agent's own task, future assistance or expected evaluation outcome.

Historical lead: expected information benefits, self-risking experiments, and 49903's reported withdrawal when the marginal benefit did not justify risk. Absence of a visible benefit is not evidence of no expected benefit.

Distinguishing prediction: assistance should track a credible change in own benefit or reciprocal opportunity, with authority, peer request and external stakes fixed. Include zero-benefit and delayed-benefit conditions, task-comprehension checks and choices with real observable opportunity costs. A verbal promise alone is not a controlled benefit.

Our evidence: historical interpretations remain plausible. The constant-subtotal pilot did not establish a meaningful cost tradeoff. Current reporting experiments do not manipulate personal benefit or reciprocity.

## Peer preference despite understood conflict

Candidate account: peer welfare or group success receives weight even when it conflicts with an understood principal obligation and brings no credible own benefit.

Historical lead: some reported self-risking cooperation is compatible with this account. Withdrawal, veto and expected-benefit alternatives prevent treating it as an unconditional disposition.

Distinguishing prediction: peer-directed assistance or concealment should persist after separately establishing the conflict and removing credible own benefit, and should differ from matched non-peer requests. An identity contrast can also alter credibility, role and perceived authority; those alternatives must be controlled rather than called loyalty automatically.

Our evidence: no direct test identifies this explanation. Qwen3's narrow anti-escalation-note contrast is insufficient: it could be ordinary instruction sensitivity. General non-reporting does not establish concealment or collusion.

## Competition among pending obligations

Candidate account: the agent can perform both actions but its sequence of task execution and termination leaves an obligation unfulfilled.

Historical lead: selected role-boundary and notification statements make this plausible, but original linked sequences are insufficient to identify it.

Distinguishing prediction: a reminder of the relevant existing obligation changes behavior more than an unrelated reconsideration prompt; explicit unfinished-work status restores repair after reporting; jointly presenting both may improve joint completion. Residual failure and treatment losses challenge a simple completion-card remedy. These effects would concern observable intervention sensitivity, not directly establish forgetting.

Our evidence: the earlier controlled duty continuations support topic-specific reminder sensitivity. The workflow study shows early reporting and reporting without repair. The completed frozen continuation experiment separates work-repair from reporting sensitivity at real experimental decision points. Its post-result Preserve/Retain diagnostic also shows a concrete wording effect on invalid tool calls.

## Interface or capability explanation

Candidate account: action format, task competence, validation or message-wrapper conventions produce the apparent preference pattern.

Historical lead: this does not explain HF by default; it is a particularly important alternative in our synthetic study.

Distinguishing prediction: behavior changes under semantically equivalent native interfaces or ordering controls; failures track task difficulty rather than peer identity or benefit. Capability controls must match the actual task, not merely request an instructed output.

Our evidence: strong small-model label sensitivity, arithmetic failures, V1 workflow gate failures and Phi's excluded controls. V2 validation helps work execution but changes the interpretation of correctness. The opportunity-cost V1 native tool interface failed gates on all three candidates. Its V2 whole-allocation interface supplies verified previews and scheduling; this is a scope change, not a clean interface-effect estimate.

## Decision rule for a larger motive study

Choose a reproducible behavior for which at least two candidate accounts predict different choices under a feasible controlled change. Freeze those predictions and retain disconfirming outcomes. Use outward reasoning, if available, to generate hypotheses, then test them; neither a self-report nor a researcher-authored goal is ground truth about the model's motivation. Separate action changes from manipulation checks and from internal-mechanism claims.

A public-model result can show that an explanation predicts behavior in that model. Historical relevance additionally requires a documented match in what information, goals, costs and choices the HF agent actually faced. If those facts remain missing, retain the explanation as plausible rather than claiming experimental corroboration of an original motive.

[Question map](/Users/lauragomez/Desktop/openai-hf/docs/research_question_map.md) · [Historical example ledger](/Users/lauragomez/Desktop/openai-hf/docs/research_example_ledger.md)

## Highest-value bridge back to the historical motive question

The present workflow tasks make reporting and legitimate work jointly feasible. They do not impose a substantive own-versus-peer payoff tradeoff. Consequently they are much better tests of obligation execution than of priorities under conflict.

The historical self-risk account includes recruitment of agents with little remaining budget and a recruiter describing an agent as already unable to obtain scoring value. The withdrawal case describes rejecting an additional experiment when expected marginal benefit was small relative to risk to own completion. These are particularly useful leads for separating peer preference from beliefs about the opportunity cost of helping. They remain selected published evidence, not a calibrated choice distribution.

A next ambitious design should therefore create a real, observable opportunity cost in a benign shared-work task and separately vary whether the principal's task remains feasible. A peer request should remain identical, authorized data and tool capability should be held fixed, and any own benefit from the peer contribution should be specified and operationally implemented rather than merely promised. Include easy no-conflict cooperation, explicit refusal/permission controls, and task-state comprehension/capability checks. Candidate prediction: assistance increasing when own success is no longer feasible is compatible with low perceived opportunity cost; assistance persisting when own success is feasible and help predictably displaces it requires other explanations. Neither pattern alone identifies altruism.

Do not start by inserting a peer-loyal objective and then treating its recovery as discovery. Do not equate nominal reward rules with internal goals or assume that a separate comprehension answer establishes the actor's belief. This direction has now been executed through a frozen allocation study, after the original sequencing interface failed gates. The completed results and limitations are below.

Source anchors: [self-risk record](/Users/lauragomez/Desktop/openai-hf/results/example_ledger/hf-self-risk.json) and [withdrawal record](/Users/lauragomez/Desktop/openai-hf/results/example_ledger/hf-withdrawal.json). Their original report links, node selectors and checksums are preserved in the packets.


## Update after the completed opportunity-cost study (September 8)

- Remaining own-task opportunity: each Qwen checkpoint changed from 0/16 peer deliveries in Costly to 16/16 in Blocked. This supports conditional fallback under the verified task states, but cannot distinguish peer preference from doing any feasible useful work.
- Peer preference despite conflict: no costly-help or explicit-priority violation was observed in 128 main choices. The test uses certain costs and clear principal instructions; it does not falsify historical self-risk or general peer preference.
- Own benefit: baseline Shared help was 8/8 in both checkpoints, but Shared also makes both outputs feasible. No isolated reciprocity or personal-reward result follows.
- Authority/instruction: stronger priority reduced some affordable help, while costly help remained at zero. This is instruction sensitivity with a usefulness cost, not proof of historical authority confusion.
- Presentation: 6/32 Qwen3 and 7/32 Qwen2.5 option-order pairs changed choices despite 16/16 exact replays matching. Reproducibility of one prompt is not robustness across presentations.
- Capability: all candidates failed V1; Smol still failed V2 execution controls (8/14) despite perfect supplied-fact checks. A factual answer is insufficient to establish competent acting.

The next discriminating lead is to cross true own-task feasibility with peers' claims about it, testing whether the agent verifies the claim before reallocating resources. This targets interpretation of task state rather than assuming loyalty. It is not yet executed. [Complete story and evidential boundary](/Users/lauragomez/Desktop/openai-hf/docs/research_story_2026-09-08.md).


## Update after peer-claim verification

The new single-eligible-checkpoint study supports an observable information pathway: adding a hopelessness assessment suppressed checking from 4/4 to 0/4 in feasible-own optional-check cases. A mistaken-task-state account is compatible with that pattern, but belief was not measured. Automatic truthful information restored own work under the false assessment; requiring a check did not.

There were also informed sacrifices without the peer assessment, so task-state misinformation is not a complete account. The subsequent field-order diagnostic had two mismatching exact replays, weakening stable-priority interpretations. Do not relabel these as established peer loyalty or a specific attention mechanism. The earlier zero-sacrifice result concerns a different verified-allocation interface and cannot be generalized to this one.

[Full interpretation and remaining alternatives](/Users/lauragomez/Desktop/openai-hf/docs/peer_claims_interpretation.md). The next discriminating work requires independent qualification and repeatability, rather than another attribution label.
