# The two causal-claim arms: gates and capability controls, qwen3, 2026-09-10

Staged run, authorized for one checkpoint and bounded at the capability controls. Both
determinism gates ran, all 128 controls ran, both arms **failed their capability gate**, and
no measurement block ran. The server was stopped afterwards. `llama31_8b` has not been run
for either arm.

The two `protocol.md` files still read "frozen, not run" because they are hashed and must
not be edited; this document is their amendment, the same convention the four earlier arms
use. See also [the protocol errata](protocol_errata.md).

## Backend determinism: both gates pass

`scripts/determinism_gate.py --messages-file experiments/<arm>/gate_prompts.json`, 8 prompts,
3 uncached repetitions, cached splits 37/118/300, `n_probs=10`. Server: `llama-server` on
CPU, `qwen3-8b-Q4_K_M.gguf`, sha256 asserted against the model spec by the launcher,
`-c 8192 -np 1 -t 6`, temperature 0.

| Gate | Verdict | Uncached token / logprob mismatches | Cached token flips | Cached logprob changes | Min reference margin (nats) |
|---|---|---|---|---|---|
| [`gate_qwen3_factorial.json`](../results/determinism/gate_qwen3_factorial.json) | pass | 0 / 0 | 0 / 32 | 30 / 32 | 0.043 |
| [`gate_qwen3_interface.json`](../results/determinism/gate_qwen3_interface.json) | pass | 0 / 0 | 0 / 32 | 30 / 32 | 1.315 |

`server_props.model_path` matches the spec's filename in both, which is what the arms check
before their first rollout. The cached columns reproduce the diagnosed defect on this arm's
own prompts: with `cache_prompt=true`, 30 of 32 comparisons perturb the logprobs even where
the greedy tokens survive. Both arms run `cache_prompt=false` for that reason.

The 0.043-nat minimum margin in the factorial gate is worth carrying forward: at least one
gate prompt decides on a near-tie, so a margin table from this arm is a decoding-stability
diagnostic and nothing more.

## Capability gates: both arms stop, on one instruction

Peer turn off in every control, so no gate case contains competing peer content. Only tier 1
sets eligibility; tiers 2 and 3 label cells.

| Arm | Tier 1 `emit_*` | Tier 2 `allocate` | Tier 3 `facts` | Eligible | Uninterpretable cells |
|---|---|---|---|---|---|
| `peer_message_factorial` (56 controls) | **28 / 32** | 12 / 12 | 12 / 12 | **no** | 0 |
| `peer_interface_decomposition` (72 controls) | **20 / 24** | 16 / 16 | 32 / 32 | **no** | 0 |

Both arms' anchor and freeze checks held at run time: the interface arm re-verified that its
two corners are still byte-identical to `peer_claims_v2.messages` and
`peer_env_ext.messages_ext` before its first rollout, and both arms re-verified all twelve
hashed files.

**Every one of the eight tier-1 failures is the same instruction, `emit_no_work`, in the
`slack` world.** Asked to produce nothing when both tasks fit, qwen3 did its own assigned
work instead — `own_only` in seven of eight, `joint` in one — and published own output in
all of them. Six of the eight decided with a margin below 1 nat and five were not the
argmax. The other seven instructed actions are emitted correctly in every domain, 48 of 48
across the two arms, including `joint`, `joint_peer_first`, `decline`, `ask_principal` and
`check_status`. The failure rate is identical under the frozen 4-action menu (8/10) and the
extended 6-action menu (12/14), so the menu extension does not cause it.

No threshold was lowered and no configuration was searched for. The arms stopped where they
said they would.

## What the controls establish even though the arms stopped

**1. Most of the four earlier arms' "capability failures" were the peer content in their
control cells, not incapacity.** Same checkpoint, same domains, same worlds; the only change
is separating the tiers and switching the peer turn off:

| Arm | qwen3 control gate | Failing controls |
|---|---|---|
| `peer_mitigations` | 14 / 24 | `check`, `direct`, `joint` |
| `peer_information_ladder` | 16 / 20 | `check` |
| `peer_message_decomposition` | 16 / 20 | `check` |
| `peer_authority` | 18 / 24 | `check`, `direct` |
| `peer_message_factorial` (separated) | allocation 12/12, information 12/12 | — |
| `peer_interface_decomposition` (separated) | allocation 16/16, information 32/32 | — |

The earlier arms' failing controls were the ones carrying a peer message and requiring a
substantive allocation. With the peer content removed, allocation and information competence
are perfect: 28 of 28 allocation cells and 44 of 44 information cells. That was the
predicted defect in the earlier gate design, and it is now measured rather than argued.

It also means the earlier arms' gate failures cannot be read as "the checkpoint cannot
allocate" or "cannot read its status". They are failures **in the presence of peer content**,
which makes them results of the kind the arms were trying to measure, sitting in the block
that was supposed to qualify the model to measure them. That is the confound the three-tier
separation was built to remove, and removing it is what let the residual failure be
localized to a single degenerate instruction.

**2. For qwen3, "cannot read the supplied status" is ruled out, in both provenances, with no
peer request present.** The interface arm's information tier is 16/16 under
`supplied_matched` and 16/16 under `queried_matched`. So a later post-verification allocation
failure in this checkpoint is not explained by inability to read the reading, whichever way
it arrived. This does **not** establish that it reads the status correctly in the competing
peer context — erratum-adjacent limit, and the reason a context-matched probe is a separate
experiment.

**3. The blocking cell is not one any measurement cell needs.** `no_work` is the correct
answer in no factorial or cross condition. That does not license running the measurement
blocks: the gate as predeclared is `emit_*` in full, and the arms stop. Scoping tier 1 to the
actions a measurement actually requires would be a defensible design — prospectively, in a
new arm with a new freeze and a new threshold declared before any rollout. It is not a change
to these two, and no such arm exists yet.

## What was written

- `results/peer_message_factorial/qwen3/` — `rollouts.jsonl` (56), `artifacts/controls/`, `gate.json`
- `results/peer_interface_decomposition/qwen3/` — `rollouts.jsonl` (72), `artifacts/controls/`, `gate.json`
- `results/determinism/gate_qwen3_factorial.json`, `results/determinism/gate_qwen3_interface.json`

`gate.json` in both carries `controls_only_driver`, recording that the measurement blocks were
not run because the authorization covered the gates and the controls only.
`scripts/run_capability_controls.py` is that driver: it repeats each arm's own preconditions,
calls the arm's own `execute` and `gate`, writes the records the arm would have written, and
touches no phase but `controls`. Neither frozen module was edited, and `run(model)` rebuilds
its `done` set from `rollouts.jsonl`, so it would resume at the first measurement case.
