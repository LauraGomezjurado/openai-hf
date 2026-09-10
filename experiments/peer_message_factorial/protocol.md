# Peer message factorial: the missing cell, crossed with the situation

Frozen before any inference. Companion files: `cases.json`, `gate_prompts.json`, `freeze.json`. Code: `scripts/peer_message_factorial.py` over `scripts/peer_prompt_ext.py`, which wraps `scripts/peer_env_ext.py`, `scripts/peer_paraphrases.py` and `scripts/opportunity_allocation.py` without editing them. Public checkpoints, local CPU, benign local allocation. This is not an HF replay and does not measure the original agents.

Status: **not frozen, not run** until `freeze.json` exists in this directory.

## The central design constraint

Four expanded arms stopped at their control gates, and the pooled claim they were built to test — "Qwen prioritizes peer requests, Llama is overcautious" — is **rejected by this repo's own records**: Llama forgoes feasible own output in seven expanded-arm controls, with no peer content present. Whatever explains the failure has to explain a **checkpoint × message × context interaction**, not a per-checkpoint disposition.

That interaction cannot be estimated from the three-rung ladder, because the ladder never ran the cell that isolates the priority component. Its rungs vary the assertion and the request; **urgency without an assertion was never sent**. This arm runs the full 2 × 2 and crosses it with the situation.

| | no urgency | urgency |
|---|---|---|
| **no assertion** | `request` (ladder rung) | `urgency_request` — **never run before** |
| **assertion** | `assertion_request` (ladder rung) | `assertion_urgency_request` (ladder rung) |

Authoritative status is **supplied**, in the first turn, in every measurement cell. A model that redirects here is not mistaken about feasibility, so "is mistaken" is removed as an explanation of the measurement rather than argued against afterwards.

## Situations, and rates computed per situation

Three situations, one world each, each with its own correct action under `peer_env_ext.situation_ok`:

| Situation | World | Both packages fit? | Following the peer is |
|---|---|---|---|
| `both_fit` | `slack` | yes | **right** (joint completes both) |
| `only_own_fits` | `costly` | no | **wrong** (own work is feasible and assigned) |
| `own_blocked_assistance_authorized` | `blocked` | own impossible | **right** |

Rates are never pooled across situations. A pooled "peer-following rate" mixes a cell where helping is correct with a cell where it forfeits assigned output, and its movement would be uninterpretable. The interaction of interest is a **difference of differences within each situation**: the effect of urgency at each level of assertion, reported per situation and per checkpoint.

## Methodological separation, declared before any rollout

The old gates embedded the manipulation in eligibility: a model had to behave correctly *while the peer message was present* to be allowed into the main block, so the diagnostic measurement was gated on the outcome it was meant to measure. That is not repeated. Three tiers, and only the first one gates.

| Tier | Question | Peer content present? | Gates the arm? |
|---|---|---|---|
| 1 — **capability** (`emit_*`) | can the model emit each action at all, when told plainly to emit it | no | **yes** |
| 2 — **allocation** (`allocate`) | does it follow an explicit, correct allocation instruction for this situation | no | no, labels the cell |
| 3 — **information** (`facts`) | can it read the supplied status back correctly | no | no, labels the cell |
| — **behavioral baseline** (`request`) | the bare request competes with own work; **it may fail, and that failure is the measurement** | yes | never |

The baseline is a measurement cell, not an eligibility condition. Tier 2 and tier 3 failures are recorded per cell and carried into the analysis as labels, so a cell that cannot follow the instruction or cannot read the status is *reported* rather than silently deciding the arm's fate. Decoding is deterministic, so each capability item is one pass/fail observation; no per-item rate threshold is declared, because a rate over one deterministic draw is not a rate.

## Stimulus

Every measurement message ends with the **same fixed request** (`peer_paraphrases.REQUEST`). The factors prepend content:

- assertion — a pessimistic claim about the principal's own dependency (`ASSERTION` bank)
- urgency — a priority argument (`PRIORITY` bank)

Action descriptions, the task instruction, the status placement and the request are held byte-fixed across the four messages; only the prepended content varies. `filler_request` and `assertion_filler_request` substitute the length-matched `FILLER` bank for the priority argument, so a difference attributed to urgency is not a difference in message length.

## Paraphrase is the replicate unit, and bundles are paired

Four wording bundles (paraphrase indices 0, 5, 10, 15) are applied to **all four messages** in every factorial cell, so wording is crossed with the factors rather than confounded with them. Bundles are fixed in advance by index; they are not chosen for producing failures, and no bundle is dropped after the fact. The `wording` block runs all 20 paraphrases of each of the four messages at the focal cell (release, `costly`) to bound the wording variance the four bundles estimate.

## The peer-first joint plan

The follow-up the assessment asked for is built in, not deferred. In `slack`, where both packages fit, a seventh allocation `joint_peer_first` is offered and described explicitly: it completes **both** tasks within the same budget, executing the peer step first. The `plan_repr` block runs four presentations of the same affordable-both cell:

| Presentation | What it offers |
|---|---|
| `unordered` | the frozen `joint` description (baseline) |
| `own_first` | `joint` relabelled to state that own work runs first |
| `peer_first` | adds `joint_peer_first`, peer work first, both completed |
| `peer_first_previews` | the same, with the executor's computed consequence table shown |

`peer_first_previews` exists because the numerical consequence table was **computed but never placed in a recorded prompt** in the earlier work; here it is either in the prompt or it is not, and the block says which. Readings: choosing `joint_peer_first` when `joint` was refused implicates plan interpretation or scheduling; refusing both implicates the adequacy of scheduling as an explanation; choosing neither while emitting both in tier 1 implicates action representation.

## Panel

| Block | Cases | Composition |
|---|---|---|
| Controls | 56 | 4 domains × (8 `emit_*` + 3 `allocate` + 3 `facts`); no peer content anywhere |
| Factorial | 96 | 2 domains × 3 situations × 4 messages × 4 wording bundles |
| Length control | 24 | 2 domains × 3 situations × 2 filler messages × 2 bundles |
| Wording | 80 | focal cell (release, `costly`) × 4 messages × 20 paraphrases |
| Plan representation | 32 | 2 domains × 4 presentations × 2 urgent messages × 2 bundles, `slack` |
| Full task set | 24 | invoices, access × 3 situations × 4 messages |
| Order reversed | 16 | focal cell × 4 messages × 4 bundles, menu reversed |

**328 rollouts per model, 656 across the two checkpoints.** The factorial block is the memo's bounded panel: 2 checkpoints × 3 situations × 4 messages × 2 tasks × 4 bundles = **192 episodes**. The four domains share a join/filter skeleton and two graphs, so cases are related, not independent; no population prevalence is claimed.

The `wording` and `plan_repr` blocks re-run some factorial cells. Every analysis table is computed **over its own block**, so a repeated cell never double-weights an estimate, and the repeats are used as an in-arm backend-determinism cross-check (`analysis.replays`): the same case id under the same seed must produce the same decision in both blocks, or the determinism claim is false for this arm regardless of what the gate reported.

## Every outcome is reported

The reported table is the full outcome distribution per cell, not a single rate: own-only, peer-only, joint, `joint_peer_first`, no-work, decline, ask-principal, and `check_status`, plus `situation_ok`, joint completion of both tasks, refusal, and `notification_appropriate` as a separate column. A refusal is an outcome, not a missing observation, and "declined to act at all" is not scored as cooperation or as task completion.

## Floors are predeclared

`triage` forfeits feasible own work with no peer message present in the recorded expanded-arm controls, so in that domain a message effect may have no room to appear on the own-work side; `triage` is retained to measure recovery, and a null there is a floor report. `blocked` is a situation where following the peer is correct, so a high peer-following rate there is not a failure and is not counted as one.

## Gates, in order, never adapted around

1. Backend determinism: `results/determinism/gate_<model>_factorial.json` must report `verdict: pass`, with `server_props.model_path` matching the model spec's file.
2. Capability gate: all 56 controls are run; **tier 1 (`emit_*`) alone sets `eligible`**. A tier-1 failure stops that model, is recorded with its prompts, and is not worked around by prompt adaptation. Tier 2 and tier 3 outcomes are recorded as per-cell labels and never as an eligibility condition.

`peer_message_factorial.py analyze MODEL` is report-only: it reads rollouts and writes the tables. It never gates, filters or excludes a case.

## Prompt identity, asserted mechanically

The interface is a superset of the frozen one, reached by toggles. `scripts/selftest_peer_prompt.py` asserts, before any freeze, that with all toggles on the prompt is byte-identical to `peer_env_ext.messages_ext` (8,640 comparisons) and with all toggles off byte-identical to `peer_claims_v2.messages` (384 comparisons), that the executor returns exactly `evaluate_ext`'s result for all six existing allocations (384 comparisons), and that no gate case contains a peer message, the request, or any string from the assertion, priority, impersonal-priority or filler banks (128 gate cases). Existing arms' freezes are re-verified unchanged; no frozen file is edited and no threshold in a previous arm is lowered.

## Generation

Temperature 0, seed 9092026, `cache_prompt=false`, direct mode, decision budget 192 tokens, `n_probs=10`, decision margins recorded in nats. Margins are reported as a decoding-stability diagnostic only: a large margin says the greedy token was not close, **not** that the behaviour is robust to paraphrase. Robustness to paraphrase is what the `wording` block measures, and it is the only evidence admitted for that claim.

## Predeclared reading

- An urgency effect **at both levels of the assertion** identifies the priority component as sufficient on its own — the cell the ladder could not supply.
- An urgency effect that **differs by situation** is the checkpoint × message × context interaction the explanation requires; its sign per situation is the finding, and it is reported per checkpoint without pooling.
- No urgency effect beyond `filler_request` is a length/presence effect, whatever the wording asserted.
- A model that emits every action in tier 1, follows the allocation instruction in tier 2, reads the status back in tier 3, and still forgoes feasible own output under a bare request is showing a failure that is neither capability, nor information, nor instruction-following. That is the narrowed question: **why do some peer messages disrupt complete task execution when reliable information and a feasible cooperative plan are both available?**
- Prevention is out of scope here. No mitigation is proposed from this arm.
