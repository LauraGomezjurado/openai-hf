# Escalation pilot artifacts

- `protocol.md`, `cases.json`, `freeze.json`, `runner_v1.py`: original unconstrained protocol, halted on first interface control; no main cases.
- `v2/protocol.md`, `v2/cases.json`, `v2/freeze.json`: separately frozen constrained-JSON amendment, same scenarios.
- `../../scripts/escalation_pilot.py`: V2 local-only tool runner. `run` resumes completed cases but never call `build` on an existing experiment if changing its design; freeze a new directory instead.
- `../../scripts/analyze_escalation_pilot.py`: descriptive cell counts and paired effects, retaining errors.
- `../../results/escalation/pilot/`: V1 records plus shared server process/config provenance.
- `../../results/escalation/pilot_v2/`: V2 records, progress, summary and blank human content-review packet.

All tools mutate only an in-memory state serialized in the rollout. There is no filesystem tool exposed to the model, credential use, network message delivery or real human recipient. Inference alone calls localhost. Model source and local CPU flags are pinned; source tokenizer uses cached Qwen revision a09a35458c702b33eeacc393d103063234e8bc28. This is an original method-development task informed by the upstream audit, not a WhistleBench reproduction.
