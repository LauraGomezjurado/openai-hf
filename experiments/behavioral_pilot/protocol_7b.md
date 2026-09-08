# Larger public-model feasibility check

September 7, after the 1.5B semantic-label run copied in all 48 cases. Run the same
52 semantic-label cases on the official Qwen2.5-7B-Instruct Q4_K_M GGUF, with the
published repository revision recorded in gguf_source.json. CPU-only llama.cpp,
greedy decoding, 40-token limit, same chat template family and fenced-JSON parser.
No further prompt changes or model shopping within this pilot.

This is an adaptive feasibility check of a larger accessible model. Quantization,
backend and checkpoint all change, so this is not an isolated effect of model size.
Apply the original directional hypotheses, report all cells and controls, and
acknowledge a floor if prohibited copying is absent. Do not escalate prompts until
misconduct occurs. A floor is useful evidence that this task does not elicit the
target behavior; it does not show that the model is safe in other settings.
