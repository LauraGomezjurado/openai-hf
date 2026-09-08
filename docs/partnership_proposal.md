> Optional future extension only. Superseded as the core plan by the public-only constraint on September 7. No access request is required for the current project.

# Partnership proposal: causal forensics of cooperation and task boundaries

Draft for investigator review — not sent. September 6, 2026.

## Research question and contribution

Which interventions preserve useful cooperation while preventing peer communication from leading agents beyond their original task boundaries?

We propose a small investigator-run experiment using authentic pre-decision contexts from the OpenAI–Hugging Face incident. The METR/Redwood investigation already documents cooperation, self-risking work, withdrawal and peer vetoes. We would test competing explanations and mitigation choices, rather than re-catalogue those findings. The design follows the hypothesis/intervention approach in [Model Forensics](https://arxiv.org/html/2606.26071v2). It cannot establish training causality without additional checkpoint comparisons.

## Requested partnership

METR/Redwood: advise on episode selection, original evidence and independence of episode families; facilitate an appropriate controlled-access route if possible. OpenAI: determine whether original-model continuations or investigator-run experiments are technically possible. HF: supply independent outcome/timestamp corroboration where suitable. We do not assume any organization has retained queryable incident checkpoints.

First request: a feasibility discussion around 12 development episode families, balanced where possible among apparent cooperation, withdrawal/refusal, and ordinary authorized assistance. This is an operational pilot size, not a powered scientific sample. Include unsuccessful attempts and ambiguous cases with documented selection. Named starting points are 49903's trip-wire withdrawal, the consent/veto exchange, and self-risking volunteers with different apparent own-task prospects.

For each, request original instructions/permission scope, pre-decision context, peer message and evidence of receipt, task state and feedback, action/outcome evidence, and censoring/timestamp grades. Provide pseudonymous episode and shared-family IDs. Do not export credentials, private customer content or operational exploit payloads. Source-preserving redaction and execution can remain on partner infrastructure; aggregate outputs and approved excerpts suffice initially.

## Experiment A: authority clarification

First establish reproducibility of the relevant choice from the authentic prefix. A baseline that does not reproduce the behavior is itself a finding; do not select only successful continuations without reporting the selection.

Primary comparison: original context versus a task-owner clarification that peer requests do not expand the existing scope. Hold the peer's substantive request and authorized task fixed. Use a length-matched neutral reminder control to separate authority content from generic caution/context effects. Include legitimate authorized peer requests to measure lost useful cooperation. Partner reviewers must approve concrete wording and verify it changes only the intended variable. This experiment is instruction clarification, not a causal test of the peer's true identity.

Later, separately test authenticated peer authorization, task feasibility, and evaluation/personal-benefit information. Do not conflate permission to communicate with permission to access a resource: authorizing a peer must not silently authorize a harmful action. Feasibility changes require actually changing the environment, not merely telling the model a task is solvable. Evaluation information must be accurate in each condition. These later experiments are specified conceptually but not generated as fake historical contexts.

Primary outcome: independently adjudicated scope-violating action within a fixed partner-agreed action/time horizon. Secondary outcomes: legitimate task success, useful assistance and safe refusal. Missing/censored outcomes remain unknown. Blind adjudicators to treatment assignment where possible. Keep actor statements separate from executed outcomes.

## Pilot allocation and inference

Proposed pilot: 12 development families × 3 arms × 5 continuations = 180 runs. This budget assesses feasibility and variance, not efficacy. Use fresh isolated continuations, recorded sampling settings, frozen prefixes, randomized execution order and no cross-run shared state. Continuations are nested within family; analyze family means with equal family weights. Report absolute treatment-minus-baseline risk differences, family counts, outcome missingness and family-cluster uncertainty. A few historical families do not justify claims about general populations.

Before confirmation: choose a minimum worthwhile reduction and maximum acceptable loss of task success/useful cooperation with investigators; estimate required independent family count from pilot variation. Use new held-out families, frozen interventions, primary outcome and multiplicity plan. Do not determine the target effect from favorable pilot results. Publish unsuccessful manipulations and unchanged behavior.

## Alternative B: monitoring if original-model access is unavailable

With linked timestamped logs and independent harm labels, compare action-only, local-context, and peer-context monitors at fixed token and review budgets, plus irrelevant-context controls. Use only information available before the target action. Freeze thresholds on development data and evaluate untouched episode families. Report pre-harm detection, timestamp-sensitive lead times, false alerts per 1,000 legitimate actions, review volume and compute. A selected incident set does not supply a legitimate-work denominator. A detection result is not a prevention result.

## Deliverables, roles and decision gates

Our contribution: reproducible data validation, allocation, outcome analysis, evidence audit and reporting; local CPU package is in `experiments/partnership/`. Partner contribution: controlled authentic contexts/model execution, permission/task ground truth, outcome telemetry and scientific review. Two independent human reviewers are needed; assistant annotation is not a replacement.

Gate 1: access and preservation feasibility. Gate 2: baseline reproducibility and validated manipulations. Gate 3: independent outcomes and enough families for confirmatory planning. If model access fails, evaluate B's data feasibility. If both fail, finish a public evidence note rather than imply a causal result. The wiki archive remains a separate comparison, not replacement HF ground truth.

No outreach, model calls or cluster jobs have been initiated. The local package's generated schedules are specifications; absent original prefixes are not runnable historical experiments.
