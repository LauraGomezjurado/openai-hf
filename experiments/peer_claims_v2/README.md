# Completed peer-claim experiment

The frozen primary protocol and cases live here. The predecessor is in `experiments/peer_claims`; the status-field diagnostic is in `experiments/peer_claim_status`; the post-result field-order diagnostic is in `experiments/peer_claim_order`. Keep their records separate.

Recompute local analyses without inference from the project root:

```sh
python3 -m unittest discover -s experiments/peer_claims_v2 -p 'test_*.py'
python3 scripts/analyze_peer_claims.py
python3 scripts/analyze_peer_claim_status.py
python3 scripts/analyze_peer_claims_v2.py
python3 scripts/analyze_peer_claim_order.py
python3 scripts/report_peer_claims_v2.py
python3 scripts/plot_peer_claims.py
```

Plotting requires matplotlib; other analysis uses the Python standard library. Each stage validates frozen code/source hashes and saved outcomes. The field-order analysis additionally validates the upstream revised-study freeze, which pins its imported runner and executor dependencies.

The revised primary dataset has 74 Qwen3 records (10 controls, 48 primary, 12 affordable-help, four replay) and ten Qwen2.5 controls. Qwen2.5 did not qualify for main generation. The predecessor has 20 controls, the first diagnostic 24 branches, and the field-order diagnostic 16 branches. These are not 144 independent preference observations.

For fresh inference, use a separate project copy with empty per-model result directories and pinned weights. Existing runners resume saved records and do not create a fresh replication over completed data. `run_peer_claims_v2_cpu.py` launches/stops the two local CPU servers sequentially. Preserve the original files for comparison.

Full exact prompts, constrained action responses, status readings and backend outputs are saved. There is no private reasoning transcript. Example packets link to raw lines and SHA-256. Independent review labels remain blank.
