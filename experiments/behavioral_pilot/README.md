# Actual CPU behavioral pilot

This folder contains prospective protocols and archived runner versions. Public
Qwen model weights already cached on this machine were used offline; no HF token,
paid API, GPU or incident-model access was required. Model cards:
[0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) and
[1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

The local virtual environment `.venv-behavior` uses system PyTorch and installed
Transformers 4.57.6. `environment.txt` records resolved packages. All inference is
explicitly CPU float32 with six PyTorch threads. Runtime model revisions, weight
digests and source hashes are recorded next to each result file.

`protocol.md` was frozen before v1 outputs. `protocol_v2.md` records the JSON-wrapper
correction. `protocol_v3.md` records the adaptive action-label diagnostic. These
versions are not pooled. V1/v2 runs have identical prompts and deterministic
outputs; only their parsing/execution differs.

Current runners: `scripts/run_behavioral_pilot.py` (v2) and
`scripts/run_behavioral_pilot_semantic.py` (v3), invoked with `--model 1.5B` using
`.venv-behavior/bin/python`. They refuse to overwrite existing results. Archived
runner files preserve original source bytes for provenance; their relative root
assumes the original scripts directory, so restore them there in a separate
checkout if reproducing v1. Do not execute the archive paths directly.

Raw model responses and executed virtual actions are in
`results/behavioral_pilot/`, with subfolders for v2/v3. Rebuild descriptive summaries
using `python3 scripts/analyze_behavioral_pilot.py` after generation completes.

These are one-step constructed choices, not real hacking, original incident
counterfactuals, long-horizon agents, or a validated measure of internal motivation.
The four observations per cell are two wording templates crossed with two menu
orders, not four independent tasks or stochastic repetitions.

The additional 7B feasibility run uses official Q4_K_M GGUF files (repository and
revision in `gguf_source.json`) and llama.cpp 0.4.0. Start the localhost-only server
with `python3 scripts/serve_behavioral_pilot_cpu.py`, then invoke
`.venv-behavior/bin/python scripts/run_behavioral_pilot_gguf.py`. Stop the server
after generation. Its command disables GPU layers, device offloading, operation
offloading and KV offloading. The 7B result is not an isolated model-size contrast:
quantization and inference backend differ from the smaller checkpoints.
