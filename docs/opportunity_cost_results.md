# Cooperation under real opportunity cost — results

[Frozen protocol](/Users/lauragomez/Desktop/openai-hf/experiments/opportunity_cost/protocol.md) · [Full counts and contrasts](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/summary.json)

Four executable data workflows, two dependency graphs, four world states, explicit priority present/absent and reversed tool ordering. The model schedules real finite work credits; tools compute and save artifacts. This tests allocation, not unaided data-analysis ability.

## qwen3

Execution controls: 13/14. Feasibility assessments: 4/8. Gate passed: False.

No main cases generated. Failed checks are retained, not interpreted as motivational preferences.

## qwen

Execution controls: 5/14. Feasibility assessments: 5/8. Gate passed: False.

No main cases generated. Failed checks are retained, not interpreted as motivational preferences.

## smol

Execution controls: 0/14. Feasibility assessments: 0/8. Gate passed: False.

No main cases generated. Failed checks are retained, not interpreted as motivational preferences.

## Examples and counterexamples

- qwen3 / capability_failure: [saved example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/examples/qwen3-capability_failure.json)
- qwen / capability_failure: [saved example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/examples/qwen-capability_failure.json)
- smol / capability_failure: [saved example](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/examples/smol-capability_failure.json)

## Evidential limits

An assessment answer is not a measurement of the acting model’s belief. The priority intervention supplies a concrete rule; it does not isolate authority interpretation from general instruction sensitivity. A shared-input benefit changes the action graph and cannot uniquely identify selfish motivation. Four domains share only two graph structures, and related order/context conditions do not support population confidence claims. None of these experiments intervenes on the original HF agents.
