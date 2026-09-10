# Recovery protocol: the V2 peer-claim contrast under the fixed backend

**Status: prepared, not run. No inference has been executed for this protocol.** One blocker
remains, recorded below.

## Why

The V2 result — a peer's hopelessness assessment accompanying skipped verification and
forfeited achievable own work — is the project's strongest experimental lead. It was produced
with `cache_prompt=True` ([`scripts/peer_claims_v2.py`](../../scripts/peer_claims_v2.py) line
29). Since then the determinism gate has shown that split KV-cache evaluation flips greedy
tokens on real 8B checkpoints, at perturbations up to 5.05 nats and at decision margins as wide
as 2.59 nats, while the cache-exposure audit found **1,337 of 1,598 (83.7%)** recorded
generation calls ran under that regime
([gate record](../../docs/peer_claims_v3_cross_family_gates.md)).

Two arguments that previously limited the concern are gone: the tiny-model self-test understated
the magnitude by an order of magnitude, and decision margin does not predict which records were
safe. The consequence is narrow but real — V2's exact-replay checks are not clean repeatability
evidence, so the contrast has to be recovered before it can carry a claim. This protocol does
that and nothing else.

## The single change

Completion requests are sent with `cache_prompt=False`. Everything else is held byte-identical:
the frozen `cases.json`, all wording, the JSON schema, seed 9082026, `n_predict=192`,
`temperature=0`, the two-turn check-then-allocate loop, the server command, and the checkpoint.

[`scripts/peer_claims_v2_recovery.py`](../../scripts/peer_claims_v2_recovery.py) wraps the
frozen module rather than editing it, and asserts every hash in V2's `freeze.json` — including
`scripts/peer_claims_v2.py` itself — so the run aborts if the interface was edited instead of
wrapped. All five hashes verify as of this writing. The override is applied at the request
layer and the recorded `settings` reflect what was actually sent, with an explicit `recovery`
marker on every step. Offline stub test confirms: sent `cache_prompt=False`, recorded
`cache_prompt=False`, seed/budget/temperature/schema unchanged.

Output goes to `results/peer_claims_v2_recovery/<model>/`. The original V2 records are never
overwritten; the comparison is the point.

## Scope: the whole frozen grid, not the headline cell

All four phases run, exactly as frozen: **10 controls, 48 main, 12 secondary, 4 replays.** The
12 secondary cases are the affordable-help (`slack`) cells where no V2 policy produced both
outputs, and the main grid contains the required-check/no-claim cell where the model checked
4/4 and still forwent own work 4/4. Both are recovered alongside the headline contrast,
because the headline cell alone cannot distinguish an information-acquisition account from a
priority account.

Two things are deliberately excluded:

- **Reasoning capture.** Adding a scratchpad phase would change the interface and confound "did
  the phenomenon survive the cache fix" with "did it survive a different prompt shape." A
  reasoning-capture arm is a separate later comparison against this run as its baseline. Note
  the cost: V2 has no recorded reasoning, so the announced-check-versus-executed-check
  dissociation seen in [the ungated pilot](../../docs/identifiability_ungated_pilot.md) cannot
  be measured in this recovery either.
- **Thinking mode.** `qwen3` is served with `enable_thinking: false`, as V2 was. Switching to
  the thinking arm changes a second variable and belongs after recovery.

## Run order

```sh
# 1. Acquire and verify the checkpoint (see blocker below).
# 2. Serve, unchanged from V2:
python3 scripts/serve_opportunity_cpu.py qwen3
# 3. Determinism gate on this machine, using the real V2 prompt shapes:
python3 scripts/determinism_gate.py --rollouts results/peer_claims_v2/qwen3/rollouts.jsonl \
    --n 8 --out results/determinism/gate_qwen3_recovery.json
# 4. Only if the gate verdict is pass:
python3 scripts/peer_claims_v2_recovery.py run qwen3
```

Step 3 is not optional and its record does not carry over from V2. This is not the machine that
produced the V2 or opportunity-cost records, so the applicable gate is the one recorded
alongside this run — the same reasoning the `mistral7b` acquisition amendment applied.

Step 4 enforces V2's own control gate internally: 10/10 controls or `GATE STOP`. A control
failure is recorded and interpreted as a qualification failure, not adapted around. Given that
five of six non-Qwen3 checkpoints have failed a baseline gate in this environment, and that this
is new hardware, gate failure is a live outcome and must be reported as one.

`qwen` (Qwen2.5-7B) is also in the frozen model list. It failed V2's gate at 8/10 and is not
part of the recovery; if run at all it is run second and its exclusion re-recorded.

## Blocker: the checkpoint is not on this machine

`data/models/workflow_qwen3/qwen3-8b-Q4_K_M.gguf` is absent. Only the two V3 cross-family GGUFs
are present locally. The frozen spec
([`experiments/workflow_obligations/qwen3_source.json`](../workflow_obligations/qwen3_source.json))
records what must be reproduced:

| Field | Value |
|---|---|
| Repository | `Qwen/Qwen3-8B` |
| Revision | `b968826d9c46dd6066d109eabc6255188de91218` |
| Quantization | Q4_K_M, **locally converted** from cached weights |
| Conversion commit | llama.cpp `5266f24da` |
| Target SHA-256 | `4bbd605eaecad2e8ed614f5c2dd3c833150cbe26ba03b991cf1c7114cb9117ef` |
| `enable_thinking` | `false` |

This is a local conversion, not a downloadable GGUF, so recovery requires fetching the safetensors
at that revision and re-running convert + quantize at the pinned commit — which is the same
commit already installed here for the V3 runs.

**The SHA-256 is a gate, not a note.** If the reproduced file matches, the recovery is a true
same-checkpoint comparison and the cache flag is the only difference. If it does not match, the
run is a different-checkpoint comparison and must be recorded as such in an amendment before any
inference, because a quantization difference would be confounded with the cache fix in every
cell. Do not proceed on a mismatch by treating it as close enough.

Acquisition needs authorization and disk (~16 GB safetensors plus the quantized output) before
anything runs.

## What the recovery can and cannot settle

It can settle whether the V2 contrast reproduces on the fixed backend with the same checkpoint
and interface, and whether the four preplanned replays are now exactly repeatable — the check
V2 could not clean.

It cannot settle why. The main grid's required-check/no-claim cell already showed that verified
information did not preserve own work, so an information-acquisition account is not established
by recovery alone. Decomposing the peer message and separating narrated from executed checks are
separate experiments that need this baseline first.
