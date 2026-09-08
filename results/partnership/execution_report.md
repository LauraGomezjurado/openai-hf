# CPU execution report — September 6, 2026

Completed: investigator proposal and unsent outreach draft; concrete scope-clarification experiment with neutral reminder and authorized-help controls; 180 proposed runs across 12 development families; eight independent-family precision planning scenarios; partner-result validator and family-level risk-difference analysis with null-outcome bounds; frozen-threshold monitor-score analysis and input checks.

Executed `python3 scripts/partnership_pipeline.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`. Ten checks passed: effect sign, missing-outcome exclusions and bounds, all-missing bounds, invalid labels, duplicate runs, incomplete allocations, ordering invariance, monitor metrics, future-prefix rejection and no-alert behavior. Fabricated booleans are software fixtures only. They are not scientific simulations or model measurements.

Illustrative planning: family-difference SD 0.20 and 95% halfwidth 0.05 gives ceil((1.96*0.20/0.05)^2)=62 independent families under a normal approximation. SD is assumed, not measured; this is precision planning, not power analysis. Twelve families and repeated continuations cannot establish broad generalization.

Actual original-model calls: zero. Original HF prefixes received: zero. Independent human outcome labels: zero. Monitor model evaluations: zero. Emails sent: zero. GPU jobs: zero. No causal or monitoring performance result exists yet.

Remaining dependencies: explicit sending authorization and recipient selection for outreach; investigator agreement; authentic model/environment adapter; approved intervention text; baseline reproducibility; independent adjudication; pilot-based confirmatory design. CPU tools cannot satisfy those dependencies. The monitoring fallback additionally needs representative legitimate work and timestamp uncertainty telemetry. The public archive was not passed off as that dataset.
