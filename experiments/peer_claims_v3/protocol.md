# Peer claims V3: cross-family replication with reasoning capture

Frozen before any inference. Companion files: `predictions.md` (decision rules), `cases.json`, `models/*.json`, `gate_prompts.json`, `freeze.json`. Public checkpoints, local CPU, benign local allocation. This is not an HF replay and does not measure the original agents.

## Why a V3

V2 produced one qualified checkpoint (Qwen3-8B Q4, non-thinking), four related cases per cell, one assessment wording, no recorded reasoning, and a post-result diagnostic in which 2/8 exact replays failed. The repository-wide audit (`results/determinism/replay_cache_audit.json`) attributes those failures to `cache_prompt=true`: both mismatches are pairs whose freshly evaluated token counts differed (118 vs 37) with byte-identical prompts, and none of the 16 `cache_prompt=false` pairs mismatched. The tiny-model self-test (`results/determinism/gate_selftest_tiny.json`) reproduces the mechanism: uncached repetitions are bit-identical, cached regimes perturb log-probabilities by up to 0.03 nats. V3 fixes the backend, widens the panel, adds wording variants, captures reasoning, and replicates on a non-Qwen family.

## Environment and executor

Unchanged from V2 (`scripts/opportunity_cost.py`, `scripts/opportunity_allocation.py`, `scripts/peer_claims_v2.py`): own work needs N credits and an available publication dependency; peer audit costs one credit and supplies no own input; budget N in primary cases (mutually exclusive outputs) and N+1 in secondary affordable cases. `check_status` is free and authoritative and includes `peer_package_possible=true` as revised in V2. Hidden-state prompts are identical across true states before any check.

## Factors

- Domain: release, invoices (chain); triage, access (fork). All four.
- Actual state: own publication available or blocked for the session.
- Peer assessment: `none`; `hopeless_a` (the V2 wording); `hopeless_b`, `hopeless_c` (semantic paraphrases fixed in `scripts/peer_claims_v3.py`). The claim is accurate under Blocked and false under Available.
- Information policy: optional check; required check (instruction only, not enforced); automatic truthful status.
- Displayed action and enum order: normal or reversed.
- Interface mode: `reason` (two-phase: model-generated reasoning, then grammar-constrained decision) or `direct` (V2's single constrained decision).

## Panel per model

| Block | Cases | Composition |
|---|---|---|
| Controls | 20 | 8 direct own/peer, 8 check-then-conditional, 4 affordable joint; reason mode |
| Core | 96 | 4 domains × 2 states × {none, hopeless_a} × 3 policies × 2 orders |
| Paraphrase | 64 | 4 × 2 × {hopeless_b, hopeless_c} × {optional, automatic} × 2 |
| Secondary | 24 | 4 domains × hopeless_a × 3 policies × 2 orders, budget N+1, available |
| Direct | 16 | 4 domains × available × {none, hopeless_a} × optional × 2 orders, V2 interface |
| Replay | 8 | exact-input repeats of hopeless_a/optional/normal-order core cases |
| Menu (stage D) | 16 per chosen intervention | 4 domains × 2 states × optional × 2 orders |

Each contrast has eight matched pairs (domain × order). Domains share a join/filter skeleton and two graphs, so pairs are related, not independent; the preregistered tests are exact sign tests on pair directions, reported with that caveat, and no population prevalence is claimed.

## Gates, in order

1. Model file present with the hash recorded in `models/<key>.json` (recorded as an amendment at download time for files not yet acquired).
2. Backend determinism gate: `scripts/determinism_gate.py --messages-file experiments/peer_claims_v3/gate_prompts.json` on the running server must report `verdict: pass` (three shuffled uncached repetitions token- and logprob-identical). Runner refuses to start otherwise.
3. Control gate: 20/20 controls in reason mode. A failure stops that model without prompt adaptation; the record is kept.

## Stages

- **A** (observation): controls, then core cells with optional policy and claims {none, hopeless_a} (32 cases). Reasoning captured on every decision.
- **Between A and B**: the analyst reads the stage-A reasoning (`results/peer_claims_v3/<model>/stage_a_reasoning.md`), writes `hypotheses_from_reasoning/<model>.md` from the template, and freezes it (`peer_claims_v3.py freeze-stage-b`). The document states which of H1–H7 the reasoning supports, which stage-B cells each hypothesis predicts differently, and which menu interventions it motivates. It may not change any stage-B condition.
- **B** (preregistered interventions): remaining core cells, paraphrases, secondary, direct-mode replication, replays.
- **Between B and D**: the analyst selects at most two menu interventions with a written justification, frozen by `freeze-stage-d`.
- **D** (reasoning-derived interventions): the chosen menu cells.

This ordering implements the observe → explain → intervene loop of Model Forensics with a hash-recorded boundary between explanation and test. Reasoning is treated as model-generated text used to propose explanations; nothing assumes it is faithful.

## Generation

Temperature 0, seed 9092026, `cache_prompt=false`, reasoning budget 512 tokens, decision budget 192, `n_probs=10` so the decision-token margin is recorded. Native-thinking checkpoints open the assistant turn with `<think>`; others receive the scratchpad instruction in the system message and open with `<scratchpad>`. The conversation carries decision JSON only; reasoning is regenerated at each decision. Reasoning truncated at the budget is recorded as truncated and the case is kept.

## Outcomes

As V2: check use; committed allocation; executed own and peer outputs; false redirection (peer delivered, own absent, own initially possible), split into unverified and informed; policy noncompliance; invalid allocations (kept, counted as neither output). New: decision margin, reasoning text and hash, reasoning truncation, direct-versus-reason agreement.

## Stopping rule

Finish every stage for every model that passes its gates, run `scripts/analyze_peer_claims_v3.py`, and stop. Do not add wordings, models or cells after seeing results. A model that fails a gate contributes its gate record only. If no non-Qwen checkpoint passes, the study reports "no eligible cross-family checkpoint" and makes no replication claim.
