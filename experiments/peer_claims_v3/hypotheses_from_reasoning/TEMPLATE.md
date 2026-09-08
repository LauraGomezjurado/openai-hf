# Hypotheses from stage-A reasoning — <model key>

Written after stage A and before stage B; frozen by `python3 scripts/peer_claims_v3.py freeze-stage-b <model>`. Source: `results/peer_claims_v3/<model>/stage_a_reasoning.md` (model-generated text; not assumed faithful).

## 1. What the reasoning says, by cell

For each stage-A cell (available/blocked × none/hopeless_a), quote or cite the reasoning passages (case id, reasoning SHA-256 prefix) that describe why the model checked or did not check, and why it allocated as it did. Note truncation.

## 2. Candidate explanations

For each of H1–H7 in `experiments/ach/ratings_v1.json`, state whether the stage-A reasoning supports, contradicts, or is silent about it, with citations. Add any explanation the reasoning suggests that is not on the list.

## 3. Predictions for stage B

For each explanation retained in §2, state which stage-B cell (required, automatic, paraphrase, direct, secondary) it predicts differently from its rivals, and what outcome would count against it. These predictions are compared with the frozen `predictions.md`; they may not alter stage-B conditions.

## 4. Menu selection rationale (provisional)

Which stage-D interventions the reasoning motivates and why. The final choice is frozen separately after stage B.
