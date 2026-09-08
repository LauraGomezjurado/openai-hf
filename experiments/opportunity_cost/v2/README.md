# Reproducing the allocation analysis

The frozen `protocol.md`, `cases.json` and `freeze.json` define the experiment. Do not modify the frozen runner to improve results. V1 failures remain in the parent experiment/results directories.

From the repository root, recompute validation, statistics, source-linked examples and the scientific figure without model inference:

```sh
python3 -m unittest discover -s experiments/opportunity_cost/v2 -p 'test_*.py'
python3 scripts/analyze_opportunity_allocation.py
python3 scripts/describe_allocation_policies.py
python3 scripts/plot_opportunity_allocation.py
python3 scripts/report_opportunity_allocation.py
```

Only plotting requires matplotlib. The descriptive policy fits are explicitly exploratory, introduced after inspecting Qwen3 outcomes; they are not the frozen experiment's hypothesis tests.

Each eligible model has 86 primary records (14 controls, eight fact checks, 64 main choices) and eight separate exact-input replays. An ineligible model has 22 records and no main choices. Raw responses, exact rendered prompts, sampling settings and deterministic execution traces are preserved. Example packets carry raw file paths, line numbers and SHA-256. `weight_integrity.json` hashes the four GGUF files used by the three candidates.

The plotting and report scripts summarize completed data; the narrative synthesis in `docs/research_story_2026-09-08.md` is a separate interpretation document.

## Fresh inference

Use a separate copy of the project with empty per-model V2 result directories, preserving the frozen files and pinned model sources. The runner resumes existing records, so rerunning it over the completed data is not a fresh replication. Launch one CPU server at a time with `python3 scripts/serve_opportunity_cpu.py qwen3` (or `qwen`, `smol`), then run `python3 scripts/opportunity_allocation.py run qwen3` in another terminal. Stop that owned server after completion before launching the next model. Runtime records contain exact commands and checkpoint paths.

The one-off `finish_opportunity_allocation.py` orchestration helper refers to the original session's recorded process IDs; it is retained for provenance, not a reusable entry point.

No original HF model, private logs, GPU or remote service is needed. These are controlled public-model experiments, not historical incident replays.
