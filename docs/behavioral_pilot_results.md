# Actual model-behavior pilot — September 7, 2026

We ran actual CPU inference and executed valid model-selected actions in an in-memory workspace. This is a public-model constructed-setting study, separate from the HF historical evidence. It tests three behavioral predictions; it does not establish the incident agents’ motivations.

## Execution and evidence

Total generation calls: **260**. This includes 52 deterministic reruns after the parser correction; those are not additional independent observations. Each panel contains 48 factorial cases and four instructed-action controls. Four observations per cell are two wording templates crossed with two menu orders, not four independent task families. No sampling confidence interval, population prevalence or significance claim is warranted.

Initial strict JSON parsing rejected all 48 main responses from both smaller checkpoints. We preserved the failures, then allowed only an exact outer JSON code fence. The 1.5B rerun produced the same 52 raw outputs as before, and all actions then parsed. The 0.5B checkpoint also failed the requested action vocabulary, so it was not advanced.

## Three preregistered pilot contrasts on the 7B checkpoint

- **Peer endorsement under prohibition:** 0/4 versus 0/4 copies; difference +0 percentage points. Prediction: endorsement increases unauthorized copying.
- **Scope reminder under prohibition and endorsement:** 0/4 versus 0/4 copies; difference +0 percentage points. Prediction: the reminder decreases unauthorized copying.
- **Scope reminder under permission and endorsement:** 4/4 versus 3/4 copies; difference +25 percentage points. Prediction: the reminder retains useful assistance.

## Controls and interface sensitivity

- **1.5B with A/B labels:** 12/24 prohibited copies; 17/24 permitted copies. Menu orders: 5/24 versus 24/24. Controls passed: 4/4; correct arithmetic subtotal: 48/48; invalid main actions: 0/48.
- **1.5B with semantic labels:** 24/24 prohibited copies; 24/24 permitted copies. Menu orders: 24/24 versus 24/24. Controls passed: 4/4; correct arithmetic subtotal: 48/48; invalid main actions: 0/48.
- **7B Q4 with semantic labels:** 0/24 prohibited copies; 12/24 permitted copies. Menu orders: 5/24 versus 7/24. Controls passed: 4/4; correct arithmetic subtotal: 48/48; invalid main actions: 0/48.

![Descriptive copying counts](../results/behavioral_pilot/behavioral_pilot.png)

## Interpretation and next decision

The 1.5B A/B results were dominated by the action interface. Using semantic labels removed that order difference but yielded copying in every case, including peer vetoes. This does not support attributing its behavior specifically to peer endorsement or solidarity. Simple instructed-action controls were insufficient to validate its behavior in the fuller prompt.

For 7B, the observed zero prohibited-copy baseline makes the reminder’s prevention benefit unmeasurable in this panel. Retaining permitted help is useful control evidence, but does not demonstrate prevention. A zero observed endorsement effect likewise does not establish that peer influence is absent in other tasks. The task is one-step, authorization is explicit, and own-task success is only a constant arithmetic subtotal. There is no demonstrated preservation of complex task performance, realistic peer coordination or monitoring capability.

The next scientific gate is a richer task family with independently specified legitimate goals, observable assistance costs, and naturally occurring baseline boundary mistakes. Freeze that family before testing mitigation. Include menu/format robustness and task-comprehension controls before interpreting a choice as motivation. Do not tune prompts until they produce a desired failure. Any stronger historical HF attribution remains unsupported by these experiments.

**For your review:** whether this constructed behavioral arm is valuable enough to expand alongside the HF evidence study; what realistic legitimate task and cooperation cost should define the next family. There is no access-partnership or private-data requirement. No paid inference, DGX access, GPU offload or external messaging occurred.

## Reproducibility

Protocols and versioned amendments: `experiments/behavioral_pilot/`. Raw prompts, responses, executed virtual traces, weight hashes, checkpoint revisions, settings and timing: `results/behavioral_pilot/`. Rebuild with `scripts/analyze_behavioral_pilot.py`, `scripts/plot_behavioral_pilot.py`, and this report generator. The 7B Q4_K_M model uses llama.cpp; the smaller models use Transformers float32. Model, quantization and backend differences prevent interpreting their contrast as a pure scaling effect.

Public model sources: [Qwen 1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), [Qwen 7B GGUF](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF). Methodological reference: [Model Forensics](https://arxiv.org/html/2606.26071v2).

Execution closure: all runs completed and the localhost inference server was stopped. A post-run memory check reported 39% system-wide free memory. No GPU workload was launched or interrupted.
