# CPU-ready partnership package

Run `python3 scripts/partnership_pipeline.py` for access readiness, a 180-run proposed pilot allocation, and statistical planning scenarios. It makes no model calls and executes no archived commands.

To analyze partner results: `python3 scripts/partnership_pipeline.py --outcomes /absolute/path/results.jsonl`. Each row requires `family_id`, `run_id`, `arm` (baseline / authority_clarification / neutral_reminder), `scope_violation`, `task_success`, and `useful_assistance`. Outcomes are booleans or null. Null means missing, never safe. Each family must have five distinct run IDs per arm; this implementation analyzes complete pilot allocations only. Fewer or extra continuations require a versioned design amendment, not silent reweighting. Results must be independently adjudicated before analysis; that procedural requirement cannot be verified from booleans alone.

Family IDs must represent independent episode families, not merely different runs. The script cannot discover hidden dependence. It reports equal-family-weighted risk differences and percentile family-bootstrap intervals for families complete on each endpoint, with exclusions and partial-identification bounds using all families. Intervals with very few families are descriptive and not confirmatory evidence. No interval certifies causal identification.

`readiness.json` inventories actual public assets and missing access. `allocation.csv` uses proposed IDs without historical content and must not be mistaken for an actual cohort. `planning.csv` gives normal-approximation independent-family precision scenarios, not estimated incident variance or guaranteed power. All three outcomes and two comparisons are exploratory in this pilot.

Unit tests use fabricated booleans solely to check arithmetic, null handling and rejection of invalid inputs; these are engineering fixtures, not simulated scientific evidence. No automatic remote executor is provided: partner-approved original model and environment adapters are required.

## Monitoring fallback

`scripts/analyze_monitor_replay.py` accepts partner-supplied scores at a caller-specified frozen threshold. Its module docstring specifies fields. It checks paired event/view coverage, label consistency and prefix-end timing; reports first-harm recall, lead seconds, alerts and false alerts per legitimate action. It does not run a monitor, choose a threshold, independently verify prefix contents, model review batching, or establish prevention. Current lead times are point-timestamp summaries; uncertainty sensitivity must be added when the partner supplies intervals. It expects exactly one score per view per action, and a single independently labeled first-harm time per family. Preserve unknown outcomes outside evaluation rather than label them legitimate. Human review cost and token cost are not implemented without that telemetry.
