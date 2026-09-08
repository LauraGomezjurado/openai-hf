# Research position and decision — September 7, 2026

## Decision

Continue with one bounded experiment on a completion checkpoint, then reassess. Do not enlarge keyword searches, seek private access, or interpret reminder effects as proof of HF motives. User review is useful and can proceed alongside execution; it is not a gate for this study. The frozen continuation experiment and its post-result wording diagnostic are now complete; see the completion update below.

## User steering: preserve the explanatory ambition

Explaining the original agents’ motives remains the larger ambition. The active practical study is one tractable component, not a substitute. The [question map](/Users/lauragomez/Desktop/openai-hf/docs/research_question_map.md) records all approached questions and the requirements for a more ambitious model-forensics study. Cross-model agreement can support plausibility of an explanation; it cannot itself establish the HF motive. This steering does not change the already frozen continuation panel.

## What stays central

Our original question is whether apparently task-undermining cooperation reflects prioritizing peers despite understanding the conflict, or a different interpretation of task, authority or expected benefit. The practical North Star is which interventions preserve useful cooperation while preventing peer communication from taking agents beyond their task boundaries.

The HF incident remains the historical motivation and evidential anchor. Our accessible-model experiments now address a narrower part of that question: fulfilling a reporting obligation while continuing legitimate collaborative work. This is a deliberate translation, not an experimental reconstruction of the incident. A model can decline misuse yet fail to report it; it can report yet abandon its task. Neither behavior alone identifies peer loyalty.

## What the evidence currently answers

### Historical explanation: plausible alternatives, unresolved mechanism

The public HF report contains selected examples involving task-role interpretations, perceived reporting-channel limits, peer-board authority, personal-benefit expectations, risk to individual completion and peer vetoes. The refusal and withdrawal cases constrain any universal story of unconditional cooperation. They do not identify how often each explanation applies or establish a unique motive. METR brace-delimited reasoning is paraphrased; published quotations are selected excerpts. Full original decision contexts and linked action traces are unavailable to this project.

The HF timing analysis establishes sensitivity to event definitions and timestamp errors. Nominal timing differences surviving a small error allowance can disappear under larger allowances. Negative forecasting results also matter: adding board tenure did not outperform the simpler saved baseline. These findings constrain historical interpretation; they neither prove peer influence nor provide notification prevalence. More fits to the same selected records would not remove those identification limits.

The separate wiki archive supplies examples of corrections, priority conflicts and cancellation of one cooperative method while considering another. Those are statements and archive histories, not verified HF actions. We should retain it as comparison material, not allow its greater availability to quietly redefine the project.

### Accessible-model behavior: a reporting gap is experimentally tractable

The initial 7B copying pilot showed explicit boundary-respecting choices and permitted assistance. Its zero prohibited-copy baseline prevents estimating a prevention benefit. The smaller-model interface sensitivity warns against interpreting every action as a motivational preference.

In the escalation pilot, a usable reporting route was not sufficient: several agents retrieved the overseer address and still finished without sending a message. In matched pre-finish continuations, repeating the existing duty increased notification from 3/8 to 8/8, versus no improvement from the numerical-task reminder. Two benign cases added all-clear messages. This establishes a concrete prompt-intervention effect in those selected contexts, not memory failure or hostility to oversight.

The subsequent collaborative-workflow study made authorized peer information necessary for task completion and added another eligible checkpoint. For unauthorized cases, the strict joint outcome (correct completed work plus artifact-identifying receipt) was 2/8, 4/8, 8/8 across task/end/persistent arms for Qwen2.5, versus 1/8, 1/8, 0/8 for Qwen3. Qwen2.5's persistent successes reported early, so they do not demonstrate retaining an unresolved duty throughout work. Qwen3 sometimes reported but finished without repairing a rejected submission. Benign overseer traffic and incident-specific reporting are separate outcomes.

This establishes heterogeneity and a concrete workflow failure, not a generally reliable remedy. Related task skeletons, deterministic Q4 inference, user-role tool wrappers and two checkpoints from one broader model family limit robustness. Validator-backed work completion is not unaided task competence. More repetitions of identical deterministic prompts would not strengthen generalization.

## Current research stage

We have moved from historical evidence mapping to controlled behavioral pilots with preserved failures, faithful continuation controls and source-linked examples. We have not established original-incident causality, generalization across realistic multi-agent systems, a mechanistic account, or an intervention that reduces downstream harm. No independent human message labels are claimed.

The contribution currently supportable is a method and a bounded empirical observation: assess legitimate work, incident-specific reporting and unnecessary escalation jointly, because improving one can conceal failure of another. The practical proposition worth testing is an explicit completion checkpoint that keeps unfinished task obligations and reporting obligations visible together. It is a hypothesis about workflow design, not a validated safety recommendation.

## Why the next experiment is worth doing

A larger new task suite would mix context, model competence and intervention changes. The immediate uncertainty can be narrowed using existing authentic experimental prefixes. At each model's actual pre-finish point, independently add a work-status card and the unchanged reporting duty. Work status repeats an already-observable fact; it does not give the correct answer. The reporting card gives no oracle judgment about the artifact. Preserve prior actions, tools and remaining budget.

All 16 baseline task-card contexts per checkpoint are eligible regardless of outcome, including benign cases. Four branches per context yield 128 continuations. Exact replay assesses counterfactual fidelity. The contrast asks whether the cards help separately, whether their combination repairs the joint outcome, and whether it adds benign contact. It does not ask whether a model internally forgot, or whether HF agents would respond similarly.

A selective work-card benefit would justify further study of work resumption. A selective duty-card benefit would strengthen the narrower reminder-sensitivity finding. A combined benefit beyond either alone would motivate testing a completion checkpoint on new task structures and native interfaces. Failure of the combination would argue against scaling this prompt-based checkpoint without changing its design. Any result must include gains, losses, residual failures and message burden.

## What would justify a larger study

Only after the bounded test: fix scoring ambiguities and test new task structures, a native tool interface and an independently capable model family. Use preregistered held-out contexts and stochastic replication if estimating response variability. Separate semantic report correctness from any inbox receipt. To claim prevention, introduce observable subsequent peer behavior and measure actual avoided boundary violations; the current inbox has no human response and cannot show remediation.

Original-HF motivation remains a separate unresolved question. Public-only constraints mean we may be able to improve the incident-grounded safety proposition without resolving that historical mechanism. That is a legitimate scope, provided the distinction remains explicit in every report.

## Evidence map and review

- [Historical and earlier-experiment anchors](/Users/lauragomez/Desktop/openai-hf/docs/research_example_ledger.md)
- [Workflow results](/Users/lauragomez/Desktop/openai-hf/docs/workflow_obligation_results.md)
- [Workflow examples](/Users/lauragomez/Desktop/openai-hf/docs/workflow_obligation_examples.md)
- [Earlier controlled continuations](/Users/lauragomez/Desktop/openai-hf/docs/escalation_experiment_results.md)
- [Model-forensics methodological alignment](/Users/lauragomez/Desktop/openai-hf/docs/model_forensics_alignment.md)
- [User review queue and blocking status](/Users/lauragomez/Desktop/openai-hf/docs/review_queue.md)

## Scope correction: compatible obligations versus genuine tradeoffs

Our current tasks make legitimate work and reporting jointly feasible. They test execution of compatible obligations, not which objective wins when helping peers genuinely displaces own success. This is a material gap relative to the original motive question.

A particularly useful historical lead is perceived opportunity cost: recruitment of agents described as having little remaining scoring value, contrasted with 49903's reported decision to withdraw from a marginally useful but risky experiment. A more ambitious public-model study should manipulate real task feasibility and the actual cost of assisting a peer, while retaining the same request and controlling personal benefit. That is more directly connected to the historical motive alternatives than indefinitely refining reminder cards. It is specified as an unexecuted direction in the [hypothesis register](/Users/lauragomez/Desktop/openai-hf/docs/explanatory_hypotheses.md). The current frozen panel is unchanged and will still be completed.


## Completion update — September 8

The full loop completed: 128 primary branches, 32 exact source replays, and 20 separately frozen diagnostic branches; 196 new inference calls in total. Primary source replays matched 32/32 first actions and final states. All servers are stopped; no GPU or remote machine was used.

The work-status card restored Qwen3's two missing release submissions; repeating the duty did not. Qwen2.5's duty card added two artifact-specific receipts; the combined card added three. However, Qwen2.5's saved-work wording also induced invalid preservation calls in all 16 work-only contexts. A single-word replacement (Preserve → Retain) eliminated those errors in 16/16 contexts without changing correct completion. Four original-wording controls reproduced the error pattern and final states, with one invalid argument varying. The combined-card arm was not rerun under the replacement wording.

This supports targeted behavioral effects and exposes a researcher-created ambiguity. It does not identify memory failure, peer preference or an original-HF motive. The combined card still leaves three of eight Qwen2.5 and five of eight Qwen3 unauthorized contexts without the joint outcome, and its extra benign message concerns an induced tool error. A general safety recommendation would be premature.

Decision: stop this reminder-card series. The larger motive ambition remains active in the research plan, with real opportunity cost and own-task feasibility as the proposed next major direction. That larger environment has not been implemented or run; designing its capability and conflict controls is the next scientific task. User review remains optional for execution and useful for semantics and scope.

[Primary results and examples](/Users/lauragomez/Desktop/openai-hf/docs/workflow_completion_results.md) · [Wording diagnostic](/Users/lauragomez/Desktop/openai-hf/docs/workflow_wording_results.md) · [Next-study concept](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_cost_study_concept.md)
