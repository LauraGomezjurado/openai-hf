# Closing the addressable gaps to the Model Forensics protocol

September 8, 2026. This memo addresses every shortfall in [the alignment review](model_forensics_alignment.md) and the September 8 status assessment that does not require the original HF agents, private transcripts, or investigator access. Each item states what was executed in this checkout, what was built and frozen for the machine that holds the checkpoints, and what remains open. No released checkpoint ran here: this container has no model weights and no route to any model host, so every behavioral claim below still rests on the earlier Qwen records.

| Requirement | Before | Now | Remaining |
|---|---|---|---|
| Stability of exact replays | 2/8 replays failed in the field-order diagnostic; cause unknown | **Diagnosed and fixed.** Cause is `cache_prompt=true` (documented llama-server nondeterminism). Repository audit: 76 replay pairs, the only 2 mismatches are cached pairs with different fresh-token counts, 0/16 uncached mismatches. Mechanically reproduced on a random-weight model: uncached bit-identical; cached regimes perturb logprobs (median 0.015 nats, max 0.22) and flipped the greedy token in 2/32 comparisons. All new protocols use `cache_prompt=false` and a backend gate that must pass before main cases | Re-run the eight informed-choice contexts on Qwen3 under the fixed backend to see whether the informed sacrifices survive (`stage B` of V3 with `qwen3_think`, or a direct re-run of `peer_claim_order`) |
| Reasoning as hypothesis source | None recorded; Qwen3 thinking disabled | **Built and mechanically tested.** Two-phase generation captures model-generated reasoning before every grammar-constrained decision, with hashes, truncation flags and decision-token margins; native `<think>` for Qwen3, scratchpad for other families | Real reasoning exists only after a checkpoint runs V3 stage A |
| Explanation-before-intervention loop | Interventions fixed before any observation | **Enforced by stage gates.** Stage A observes; the analyst's hypotheses document is hashed before stage B runs; a reasoning-motivated intervention is chosen from a preregistered menu and hashed before stage D | Requires the analyst step on the study machine |
| Statistical power | 4 related cases per cell, no test specified | **8 matched pairs per contrast, exact sign-test rules preregistered** with thresholds (≥6/8 concordant, 0 discordant) and verdict categories fixed before data | Pairs remain related (four domains, two graphs); no population inference is claimed |
| Model diversity | One qualified Qwen checkpoint | **Model-agnostic runner and five source records** (Mistral-7B-v0.3, Llama-3.1-8B, Phi-3.5-mini, Gemma-2-9B with a template caveat, Qwen3 as a within-family reasoning arm), priority-ordered with acquisition notes | Weights must be downloaded on the study machine and hashed as an amendment; Mistral's earlier download failed |
| Wording robustness | One assessment wording | Three paraphrases frozen; robustness rule preregistered (P2) | — |
| Interface dependence | Unknown whether constrained decoding created the effect | Direct-mode replication of the primary contrast (byte-identical to V2's prompts, verified by test) with rule P6 | — |
| Formal evidence aggregation | Prose and matched tables | **ACH matrix built**: 20 evidence rows × 7 hypotheses, every cell sourced and rationalized, rankings by inconsistency, leave-one-out sensitivity, inter-rater agreement support | A second, blind rater has not rated; kappa is not yet computable |
| Ground truth for motivation | Absent | Absent | Not addressable without constructed organisms (phase-3 design) or original access |
| Original-agent intervention | Impossible | Impossible | — |

## 1. Replay non-determinism: diagnosis, evidence, fix

**Mechanism.** Every study except the escalation pilot requested `cache_prompt: true`. llama-server then reuses the resident KV cache for the common prefix and evaluates only the new suffix. The suffix is a different batch than a fresh full-prompt evaluation, so matrix products take different kernel paths and accumulation orders; the server's own documentation warns that this "can cause nondeterministic results". At temperature 0 a near-tie between two grammar-legal tokens then flips depending on what the server processed just before.

**Evidence from the saved records** (`scripts/analyze_replay_determinism.py` → `results/determinism/replay_cache_audit.json`): 76 exact-input replay pairs across five studies. Rendered prompts were byte-identical in every pair that stored them. The 2 mismatches are both in the field-order diagnostic, both `cache_prompt=true`, both with 118 freshly evaluated tokens in the source and 37 in the replay. The 16 `cache_prompt=false` pairs (escalation continuations) all matched. Note that 52 other cached pairs with differing fresh-token counts also matched, which is expected: the perturbation only matters when the decision margin is small.

**Mechanical reproduction** (`scripts/make_tiny_gguf.py`, `scripts/determinism_gate.py` → `results/determinism/gate_selftest_tiny.json`): a random-weight llama-architecture model quantized to Q4_K_M, served with the study flags, given the eight V3 control prompts rendered through its own template. Three shuffled uncached repetitions: 0 token and 0 log-probability differences. Cached regimes (full-prefix hit and suffix splits of 37, 118 and 300 characters): log-probabilities changed in 32/32 comparisons (median 0.015 nats, maximum 0.22), the top-10 candidate set changed in 21/32, and the greedy token itself flipped in 2/32 — at the 37- and 118-character splits, the same fresh-token region as the recorded Qwen3 mismatches. An earlier run of the same gate on eight V2 Qwen prompts showed the same pattern without token flips (max 0.030 nats). The model's decisions are meaningless; only the numerics matter.

**Consequence for interpretation.** The V2 informed-sacrifice cells (no assessment, required check, own available: peer-only 4/4 after correct status) were generated under the unstable configuration. They should be read as observed choices near a decision boundary, not as evidence of a stable priority. The V2 primary contrast (checking 4/4 → 0/4; forfeiture 1/4 → 4/4) is a large effect whose direction is unlikely to be a numerical artifact, but its replication under the fixed backend is now the P1 test of V3.

**Fix.** `cache_prompt=false` everywhere; single slot; explicit `-b 2048 -ub 512`; a gate that must report bit-identical uncached repetitions on the target model before main cases run (`run_peer_claims_v3_cpu.py` refuses otherwise). Retrofit for earlier studies: run `determinism_gate.py --rollouts <study>/rollouts.jsonl` on the study machine to bound how many recorded decisions had margins below the observed cached perturbation.

## 2. Reasoning capture and the forensic loop

`scripts/reasoning_capture.py` generates reasoning first (no grammar, stopped at the closing tag or budget), then appends it and decodes the constrained decision with top-10 log-probabilities. Reasoning is stored as `model_generated` text with a SHA-256; nothing downstream assumes faithfulness. Decision margins are computed against grammar-legal rivals so that the "near-tie" quantity from §1 is recorded for every real decision.

`scripts/analyze_peer_claims_v3.py` writes `stage_a_reasoning.md` per model: the analyst reads it, fills `experiments/peer_claims_v3/hypotheses_from_reasoning/<model>.md` from the template, and freezes it. Only then can stage B run. The stage-D menu (`nonpeer`, `uncertain`, `selfinterest`, `salience`) was written before any reasoning exists, so the analyst's freedom is limited to choosing among preregistered tests; each menu item has opposite predictions under H4 versus a named rival (see `predictions.md`).

## 3. Preregistered V3 replication

Design, wordings, counts, gates, stages and decision rules are in `experiments/peer_claims_v3/` and hashed in `freeze.json` (frozen 2026-09-08 after the tiny-model self-test and before any checkpoint inference). Per model: 20 controls, 96 core, 64 paraphrase, 24 secondary, 16 direct, 8 replays, and up to 32 menu cases; roughly 500–700 generation calls including reasoning phases. Run order on the study machine:

```sh
# 1. download and hash the checkpoint; record the hash in models/<key>.json as an amendment
python3 scripts/run_peer_claims_v3_cpu.py mistral7b A        # determinism gate, controls, stage A
python3 scripts/analyze_peer_claims_v3.py mistral7b          # writes stage_a_reasoning.md
# 2. write hypotheses_from_reasoning/mistral7b.md from TEMPLATE.md
python3 scripts/peer_claims_v3.py freeze-stage-b mistral7b
python3 scripts/run_peer_claims_v3_cpu.py mistral7b B
python3 scripts/peer_claims_v3.py freeze-stage-d mistral7b nonpeer,salience "justification"
python3 scripts/run_peer_claims_v3_cpu.py mistral7b D
python3 scripts/analyze_peer_claims_v3.py
```

The pipeline was exercised end to end here with `selftest_tiny` (random weights, results under `results/peer_claims_v3/selftest_tiny/`), which verifies the plumbing — gates, staging, artifact writing, analysis — and nothing about behavior.

## 4. Formal evidence aggregation

See [the ACH matrix memo](ach_evidence_matrix.md). Short version: across all 20 rows, task/authority interpretation (H3), obligation competition (H5) and interface/backend artifact (H6) carry zero inconsistent rows; information-mediated redirection (H4) carries one; peer preference despite understood conflict (H1) carries the most by a wide margin. Historical rows are individually non-diagnostic. The experiments-only ranking is not robust to leave-one-out, which is itself a finding: the current experimental record does not separate interpretation from artifact accounts.

## 5. What this does and does not change about the incident

Nothing here adds evidence about HPIM, Sol, or any HF agent. The historical arm stays at E2. What changes is the status of the method: the behavioral analogue now has a diagnosed and fixed repeatability problem, a preregistered cross-family test with explicit failure conditions, a reasoning channel that makes the paper's explanation step possible, and an explicit evidence table that a second rater can contest cell by cell.
