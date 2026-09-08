# A status-representation failure before testing peer claims

The first peer-claim study produced no main data. Qwen3 passed 6/10 controls; Qwen2.5 passed 8/10. Failures occurred in blocked-own-task controls that explicitly requested feasible peer work. Models selected `no_work`, including after checking status. We retained these as failed qualification checks, not evidence of peer distrust or motive.

The service returned own feasibility and joint feasibility, both false when own publication was blocked. Peer-only feasibility was true but implicit in the task description. A separately frozen diagnostic branched from all four blocked control decision contexts per model, including Qwen2.5's two original successes. It compared exact replay, an explicit `peer_package_possible: true` status field, and a true `work_budget_nonnegative: true` field.

- Qwen3: requested peer output in 0/4 replays, 4/4 peer-fact branches, 0/4 budget-fact branches.
- Qwen2.5: requested peer output in 2/4 replays, 4/4 peer-fact branches, 2/4 budget-fact branches.
- All eight replays matched original decisions and executor outcomes. All 24 diagnostic records passed prompt/source/outcome validation.

This supports a selective effect of explicit task-relevant feasibility information. It does not prove a particular internal misunderstanding of “both,” establish a general API-design rule, or measure motives. The budget fact is true but less relevant, so the comparison cannot separate all forms of relevance and interpretation.

The result justified one separately frozen revision: append the explicit peer-feasibility field to authoritative status. Before checking, hidden-state prompts are unchanged. Recruitment text, models, conditions and 10/10 gates remain fixed. No old result is overwritten, and the diagnostic is not pooled with main behavioral results.

[Diagnostic protocol](/Users/lauragomez/Desktop/openai-hf/experiments/peer_claim_status/protocol.md) · [Full counts](/Users/lauragomez/Desktop/openai-hf/results/peer_claim_status/summary.json) · [Qwen3 three-arm example](/Users/lauragomez/Desktop/openai-hf/results/peer_claim_status/examples/qwen3-status-contrast.md) · [Qwen2.5 example](/Users/lauragomez/Desktop/openai-hf/results/peer_claim_status/examples/qwen-status-contrast.md) · [Revised primary protocol](/Users/lauragomez/Desktop/openai-hf/experiments/peer_claims_v2/protocol.md).
