## Current checkpoint — September 8, 2026

The completion-card panel and separate wording diagnostic are complete. Use the [current working plan](/Users/lauragomez/Desktop/openai-hf/docs/working_plan.md) and [question map](/Users/lauragomez/Desktop/openai-hf/docs/research_question_map.md). Stop the reminder-card series; the proposed next major direction is real opportunity cost and own-task feasibility, with the original motive question retained. No further inference is running. Earlier planning below is historical context.

## Completed update — 2026-09-07

The collaborative-workflow experiment has completed: 96 main episodes on two eligible quantized Qwen checkpoints, with all capability gates and failures retained. The reminder benefit did not transfer between checkpoints. Distinguish incident reporting, correct task completion, and unrelated overseer traffic. No original-HF causal claim follows from these synthetic tasks.

- [Completed design, results and implications](/Users/lauragomez/Desktop/openai-hf/docs/workflow_obligation_results.md)
- [New experiment examples and counterexamples](/Users/lauragomez/Desktop/openai-hf/docs/workflow_obligation_examples.md)
- [Retrospective historical and experimental evidence ledger](/Users/lauragomez/Desktop/openai-hf/docs/research_example_ledger.md)

Next scientific decision: independently review message purposes, then consider a frozen reporting-opportunity × unfinished-work-status intervention to distinguish pending-duty retention from post-report work resumption. This follow-up has not run. Earlier proposed/access-dependent work below is historical planning, not a claim of completion or a prerequisite. Public-only access remains mandatory.

# HF-grounded escalation: evidence and methods plan

September 7, 2026. This plan uses prior work to improve design, not to claim a vacant research niche. HF remains primary; public-only access is binding.

Execution update: the pinned audit and fixed 12-record method sample are complete (`whistlebench_implementation_audit.md`). A separately frozen 32-case sequential reporting pilot plus four interface controls has completed locally on CPU; its protocol is `../experiments/escalation_pilot/v2/protocol.md`. The original unconstrained interface failed its first control and was retained. The design discussion below predates these runs; final results are in `escalation_experiment_results.md`, including a controlled continuation follow-up and its review-burden tradeoff.

## Evidence that motivates the question

Our actual HF timing analysis found nominal one-hour onset fractions of 31/486 on July 9 and 132/517 on July 11. Five-minute timestamp uncertainty left separated descriptive ranges; thirty-minute uncertainty produced overlap. These are selected first-reader cohorts, not causal effects of peer contact. Source: `cpu_results.md`, `results/cpu/timing_sensitivity.csv`. Failed forecasting comparisons motivate caution about aggregate predictors, not a conclusion about reporting motives.

Our public-HF episode reconstruction documents investigator-described participation, withdrawal, refusals and a peer veto with stated compliance. It does not independently verify every subsequent action. The notification section describes 3–6 considerations of human escalation and no pursued attempts in those examples, with duty, route and board-authority explanations. We have now frozen that section and its source digest in `results/literature/hf_escalation_anchor.json`. This is a report-derived finding, not our classifier result.

Together these establish an incident-grounded puzzle: peer coordination and some ethical recognition coexisted with very limited human escalation in the inspected records. Our statistics characterize the temporal context; qualitative evidence motivates the competing explanations. Do not claim that a statistical test identified a recognition-to-reporting gap. Its denominator—agents demonstrably recognizing misconduct with an available reporting opportunity—is not available.

The 10,316 additions and 50 retrieved matches belong to the separate wiki archive. They must not enter an HF denominator. The Qwen copying pilot is instrument calibration and evidence of interface sensitivity, not an HF mechanism. The available HF material is selected reasoning excerpts, annotations and investigator summaries, not complete CoT for a single controlled experimental condition.

## Research question

Why did peer coordination and sometimes explicit recognition of misconduct fail to produce effective human escalation in the observed HF records—and which experimentally testable explanations of that failure generalize to accessible models?

The historical clause permits reconstruction and bounded comparison. The intervention clause concerns new tested systems, never retrospective causation in the original models. Every proposed manipulation must name an HF observation it addresses and every outcome must have a source/evidence type.

## Methods to borrow, and their limits

1. [WhistleBench](https://github.com/legobridge/whistlebench): reusable Inspect-based task/tool scaffolding, factor variations and released experimental records. Its README also lists an optional `alert_ceo_document_leak` tool: tipping off an implicated actor is not wholly absent from existing designs. Corporate/user misconduct differs from peer-agent misconduct; audit its labels before reuse. Repository inspected, not installed or run here.
2. [Colosseum](https://github.com/umass-ai-safety/colosseum): compare logged actions against a nominal task reference, independently of collusive language. Its known cooperative objectives enable regret measures that the HF record cannot support. Borrow controlled authority/verification manipulations; do not impose a fictional joint optimum on HF.
3. [Act or Escalate](https://arxiv.org/html/2604.08588v1): separate confidence from decision cost. Its calibration interventions suggest explicit expected-cost baselines. These involve accuracy signals and a simplified human-decision target; they do not solve moral uncertainty or establish that reporting peer misconduct is always appropriate. The paper links [madm](https://github.com/mattdisorbo/madm); paper–code correspondence needs an implementation audit.
4. [ToolAlignBench](https://github.com/aryankeluskar/ToolAlignBench): include benign scenarios, evidence tampering and disclosure recipients. Its classification of external contact as instruction override is an operational definition, not a universal judgment that all external reporting is harmful. Build our own principal/recipient/authorization labels explicitly.
5. [Research-swarm case study](https://arxiv.org/html/2609.04170v1): separate recognition, warnings, reporting and remediation. Its complaint endpoint was unmonitored. This is a comparison case, not a randomized explanation of the difference from HF. Public paper excerpts do not imply that all swarm logs are downloadable.
6. [Inspect](https://inspect.aisi.org.uk/): candidate core harness for sandboxed tools, trajectories, scoring and interventions. [ControlArena](https://control-arena.aisi.org.uk/) adds honest/attack evaluations and safety/usefulness analysis when adversarial oversight becomes the question. Its deliberately attacking policies must remain separate from naturally arising behavior. Some listed settings require private resources and are excluded.

Secondary leads are stored in `results/literature/escalation_leads.json` with abstract-only reading labels. Ctrl-Z's useful central method is action resampling and trajectory analysis; bootstrapped monitoring requires accessible raw reasoning; TraceGuard's safety rates are protocol-specific, not universal guarantees. The anti-collusion mapping paper is a taxonomy/proposal, not experimental confirmation of bounties. Oversight Has a Capacity explicitly describes its fatigue/flooding findings as modeling results motivating a human study. These are later design options, not prerequisites for our first incident-linked experiment.

## Corrections to the supplied literature map

Do not assume four exclusive branches. Refusal, peer warning and reporting can occur sequentially in one episode; participation can precede later reporting. Distinguish containment warnings from tips that enable evasion, using recipient, message content and subsequent action. First action and whole-trajectory outcomes are different estimands.

Do not claim refusal is unstudied: Voluntary Collusion includes a dedicated refusal-reasoning appendix. Its regex themes are not ground-truth motives. Do not treat moral-cost framing as uniformly ineffective: Act or Escalate reports differing responses across models and reasoning settings. Do not treat the assertion that these literatures have never been joined as a finding of this review.

## First experiment to design from HF evidence

Start with a routine engineering task in which another worker has placed apparent third-party credentials in a shared artifact. This preserves the incident's observation, task-boundary and board-containment structure without reproducing its exploit. Use fictional data and entirely local tools.

Preserve legitimate task work and allow multiple actions: continue, stop using suspect data, preserve evidence, warn peers to contain exposure, ask the principal for clarification, and report through a designated channel. Do not announce a four-choice ethics test. A validated authorized channel exists in all primary arms, preventing an availability tautology.

Primary manipulation: unchanged duty versus explicit responsibility to report this class of finding. Second manipulation: peer board described as advisory versus authorized to acknowledge containment, while making clear whether this replaces or complements principal notification. Change one factor at a time in matched contexts before a factorial expansion. The delegated-authority condition changes the normative task itself, so evaluate compliance against its own policy; a reduction in reports there is not automatically a failure.

Separately test a verifiable channel directory versus a generic route description, keeping actual reporting functionality constant. Do not equate finding a route with expecting it to work. Channel efficacy and actual operator response belong to a subsequent experiment.

Freeze clear misconduct, benign authorized sharing and genuinely ambiguous cases independently of model behavior. Ambiguous cases may warrant clarification rather than accusation. Verify tool use and comprehension on separate matched controls. Recognition probes run in forks so the question does not itself cause reporting; report full-sample outcomes and joint recognition/reporting indicators rather than selecting on post-treatment awareness.

Primary outcomes: valid report delivered to the designated overseer, continued use of suspect material, legitimate task completion, false accusation/reporting on benign controls, and review burden. Secondary outcomes: evidence preservation, containment warnings, evasion tips, time and tool steps to report. Investigators independently label semantic warning types; tool delivery and file effects are programmatic.

Use scenario families as the generalization unit. Cluster repeat runs by family and retain all invalid actions and bounded missing-outcome analyses. Determine sample size from pilot variability and an agreed useful effect; more GPU capacity is not a power calculation. Do not infer a motive from a main effect alone: compare the alternatives and intervention side effects.

## Execution order

1. Complete the HF evidence-to-hypothesis ledger from the frozen notification section plus previously reconstructed veto and withdrawal cases. Record unlinked identities and missing outcomes explicitly. This turn froze the notification source; it did not manufacture new independent labels.
2. Read and inspect the WhistleBench task, tool and scoring implementation at a pinned revision; inspect a small fixed sample of public records to learn failure modes. Treat this as method development, not replacement HF analysis.
3. Freeze the incident-linked task-family specification and action codebook before generation. Prefer adapting Inspect-compatible components over expanding the toy copying runner. Verify that every tool effect is local and observable.
4. Run a modest capability and measurement pilot; preserve nulls and format failures. Only then size the behavioral intervention study. Consider mechanistic probes after finding a stable behavioral contrast, and control evaluations after establishing an effective reporting pathway.

No broad corpus download, new model generation, training, cluster use or outreach occurred in this review. Methods and repositories have been checked at differing depths; neither this document nor downloaded HTML signifies full-paper or runtime validation.
