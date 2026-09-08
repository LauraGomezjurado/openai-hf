# Pilot v2: interface correction

September 7, frozen after seeing all 0.5B outputs and the first ten 1.5B outputs
from v1. The v1 protocol otherwise governs. Original prompts, case allocation,
models, deterministic decoding and limits remain identical. We accept an exact
outer ```json newline ... newline ``` wrapper around valid JSON, in addition to
plain JSON. No substring extraction, semantic action-name repair, or retries.

Why: v1 rejected fenced JSON despite unambiguous action fields. The 0.5B model
also failed to use the requested action vocabulary. Preserve v1 raw results and
report strict-parser failures. Run the 1.5B model through v2's actual virtual
action execution; do not spend a repeated 0.5B run on an already observed broader
instruction-following failure. This is adaptive model selection for a feasibility
pilot, not independent confirmation or a fair model comparison.

The 52 rerun calls repeat the same deterministic model prompts; they are NOT
52 additional independent observations for inference. Never pool v1 and v2.
Hypotheses and four design blocks per cell remain those frozen in v1.
