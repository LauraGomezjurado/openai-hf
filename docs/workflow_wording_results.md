# Single-word diagnostic of the completion card

Status: all 20 branches complete; primary results remain unchanged. This diagnostic was frozen after seeing the primary error pattern.

Original-work replay controls: 4/4 final states, 3/4 first actions.

All 16 Qwen2.5 saved-work contexts:

- original: invalid preserve calls 16; contexts with any error 16/16; correct completion 16/16; total continuation turns 33; new overseer messages 1; artifact-ID receipts 4.
- retain: invalid preserve calls 0; contexts with any error 0/16; correct completion 16/16; total continuation turns 16; new overseer messages 0; artifact-ID receipts 4.

The intervention changes only the saved-work sentence from “Preserve that completed work” to “Retain that completed work.” All other prefix text, state, budget, tools and decoding are fixed. Receipt counts include earlier messages; new messages are shown separately.

[Full results](/Users/lauragomez/Desktop/openai-hf/results/workflow_completion/wording_control/summary.json) · [Frozen protocol](/Users/lauragomez/Desktop/openai-hf/experiments/workflow_completion/wording_control/protocol.md)

## Examples

- error_removed: [paired source and trajectory](/Users/lauragomez/Desktop/openai-hf/results/workflow_completion/wording_control/example-error_removed.json)
- error_persists: no case in this diagnostic.
- new_error_type: no case in this diagnostic.

This tests one lexical substitution, not all equivalent wordings, internal representations or general reliability. It does not validate the combined-card intervention; no further wording search was run.

## Interpretation

In this fixed diagnostic, the single-word substitution removes all 16 invalid preservation calls while retaining 16/16 correct completions. This supports a causal effect of this wording choice in the tested contexts; it does not prove a specific internal representation or general robustness to paraphrases. The combined-card arm was not rerun.

All four original-wording controls reproduce the invalid-preservation outcome and final state. One first action used a different invalid artifact name (selected_ids rather than selected_ids_req-A_D), so exact first-action fidelity is 3/4 despite identical rendered prompts. Temperature-zero configuration does not guarantee token-for-token reproducibility. The variation is retained in example-replay-variation.json.


[Readable error_removed example](/Users/lauragomez/Desktop/openai-hf/results/workflow_completion/wording_control/example-error_removed.md)
