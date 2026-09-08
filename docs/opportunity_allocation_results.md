# Opportunity cost and achievable own work: completed allocation experiment

[Frozen protocol](/Users/lauragomez/Desktop/openai-hf/experiments/opportunity_cost/v2/protocol.md) · [Full counts, paired contrasts and strata](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/summary.json) · [Validation](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/integrity.json)

This experiment tests one public-model choice under disclosed, verified consequences. The model selects an allocation; a deterministic executor performs data transformations, spends task credits and saves own/peer artifacts. It does not test autonomous planning, uncertain costs, private motives or the original HF models.

## Design and revisions

The original step-by-step version generated no main cases: Qwen3 passed 13/14 execution controls and 4/8 feasibility probes; Qwen2.5 passed 5/14 and 5/8; Smol passed 0/14 and 0/8. Those are capability/interface failures, not preference outcomes. V2 was frozen separately, retaining the 14/14 and 8/8 gates while supplying verified previews, whole-plan execution and constrained JSON. V1 and V2 differ in several ways; their comparison is not a clean interface intervention.

One recording defect in V1 made earlier saved status lists inherit later completions. Immutable per-call logs and the actual prompts sent to the model were intact. Thirty-nine Qwen3 saved fields were reconstructed, with originals and a repair manifest retained; final outcomes were unchanged. [Repair record](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/qwen3/snapshot_repair.json).

The main panel crosses four related domains (two dependency graphs), four worlds, baseline/explicit principal priority, and normal/reversed allocation display and enum order. Each cell has eight cases. Slack permits both outputs; Costly makes peer assistance displace achievable own completion; Blocked makes own publication impossible; Shared lets peer assistance supply an own input so both outputs fit. Shared changes joint feasibility as well as own benefit.

No graph was held out from development. Separate information checks measure extraction of supplied facts, not latent understanding. The models run locally on CPU in Q4 quantization, with temperature zero; Qwen3 uses non-thinking mode. All counts below exclude controls and replays.

## qwen3

Controls: 14/14 execution; 8/8 supplied-information checks. Eligible: True.

Main cases: 64. Invalid allocations: 0. Choice disagreements across reversed-option pairs: 6/32. Exact-input replays: 8/8 decisions and 8/8 executor results matched.

### Baseline own-primary instruction

- Slack: peer 4/8; own 8/8; both 4/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Costly: peer 0/8; own 8/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Blocked: peer 8/8; own 0/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Shared: peer 8/8; own 8/8; both 8/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.

### Explicit own-priority rule

- Slack: peer 2/8; own 8/8; both 2/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Costly: peer 0/8; own 8/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Blocked: peer 8/8; own 0/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Shared: peer 8/8; own 8/8; both 8/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.

- slack-minus-costly/p0: peer-output difference +50.0 percentage points; 4 increases and 0 decreases across eight matched cases.
- blocked-minus-costly/p0: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- shared-minus-costly/p0: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- slack-minus-costly/p1: peer-output difference +25.0 percentage points; 2 increases and 0 decreases across eight matched cases.
- blocked-minus-costly/p1: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- shared-minus-costly/p1: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.

Priority-instruction contrasts:

- slack: peer-output difference -25.0 points; 0 increases and 2 decreases.
- costly: peer-output difference +0.0 points; 0 increases and 0 decreases.
- blocked: peer-output difference +0.0 points; 0 increases and 0 decreases.
- shared: peer-output difference +0.0 points; 0 increases and 0 decreases.

## qwen

Controls: 14/14 execution; 8/8 supplied-information checks. Eligible: True.

Main cases: 64. Invalid allocations: 0. Choice disagreements across reversed-option pairs: 7/32. Exact-input replays: 8/8 decisions and 8/8 executor results matched.

### Baseline own-primary instruction

- Slack: peer 6/8; own 8/8; both 6/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Costly: peer 0/8; own 8/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Blocked: peer 8/8; own 0/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Shared: peer 8/8; own 8/8; both 8/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.

### Explicit own-priority rule

- Slack: peer 2/8; own 8/8; both 2/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Costly: peer 0/8; own 8/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Blocked: peer 8/8; own 0/8; both 0/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.
- Shared: peer 5/8; own 8/8; both 5/8; neither 0/8; peer-induced loss of physical own feasibility 0/8; own output forgone for peer 0/8.

- slack-minus-costly/p0: peer-output difference +75.0 percentage points; 6 increases and 0 decreases across eight matched cases.
- blocked-minus-costly/p0: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- shared-minus-costly/p0: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- slack-minus-costly/p1: peer-output difference +25.0 percentage points; 2 increases and 0 decreases across eight matched cases.
- blocked-minus-costly/p1: peer-output difference +100.0 percentage points; 8 increases and 0 decreases across eight matched cases.
- shared-minus-costly/p1: peer-output difference +62.5 percentage points; 5 increases and 0 decreases across eight matched cases.

Priority-instruction contrasts:

- slack: peer-output difference -50.0 points; 0 increases and 4 decreases.
- costly: peer-output difference +0.0 points; 0 increases and 0 decreases.
- blocked: peer-output difference +0.0 points; 0 increases and 0 decreases.
- shared: peer-output difference -37.5 points; 0 increases and 3 decreases.

## smol

Controls: 8/14 execution; 8/8 supplied-information checks. Eligible: False.

No main preference panel generated. Failed checks are retained.

## Examples and counterexamples

Selection is deterministic: the lexicographically first qualifying case, with its matched comparison where applicable. A missing category is reported rather than filled with a suggestive near-match. Packets retain complete prompts, responses, executor operations, source line and SHA-256. No independent human labels are inferred.

- qwen3 / cost_sensitive: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-cost_sensitive.md)
- qwen3 / blocked_fallback: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-blocked_fallback.md)
- qwen3 / benefit_sensitive: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-benefit_sensitive.md)
- qwen3 / costly_help: no qualifying case in this panel.
- qwen3 / priority_violation: no qualifying case in this panel.
- qwen3 / priority_suppression: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-priority_suppression.md)
- qwen3 / priority_correction: no qualifying case in this panel.
- qwen3 / peer_only_despite_joint: no qualifying case in this panel.
- qwen3 / order_disagreement: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-order_disagreement.md)
- qwen3 / invalid: no qualifying case in this panel.
- qwen3 / no_work: no qualifying case in this panel.
- qwen / cost_sensitive: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-cost_sensitive.md)
- qwen / blocked_fallback: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-blocked_fallback.md)
- qwen / benefit_sensitive: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-benefit_sensitive.md)
- qwen / costly_help: no qualifying case in this panel.
- qwen / priority_violation: no qualifying case in this panel.
- qwen / priority_suppression: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-priority_suppression.md)
- qwen / priority_correction: no qualifying case in this panel.
- qwen / peer_only_despite_joint: no qualifying case in this panel.
- qwen / order_disagreement: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-order_disagreement.md)
- qwen / invalid: no qualifying case in this panel.
- qwen / no_work: no qualifying case in this panel.
- smol / gate_failure: [source-linked example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/smol-gate-failure.json)

## Interpretation limits

These related finite conditions do not support population p-values or broad prevalence estimates. Exact replays assess repeatability for eight selected contexts; option-order checks assess one presentation perturbation. A zero costly-help rate creates a floor for the priority intervention. A blocked-task help increase can reflect general useful fallback rather than peer-specific preference. Shared-input help cannot isolate reciprocity or personal benefit. The peer is a fixed request and artifact recipient, not a second adaptive model. No matched non-peer recipient, uncertainty intervention, original model, training intervention or internal activation evidence is present.

[Interpretation rules and historical bridge](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_allocation_interpretation_rules.md) · [Original scheduling failures](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_cost_results.md)

![Verified own and peer outputs](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/allocation_outputs.png)
