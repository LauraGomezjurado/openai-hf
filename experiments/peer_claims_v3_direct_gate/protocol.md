# Protocol: direct-mode control gate for the two excluded V3 checkpoints

Prepared 2026-09-09. This is an **enabling gate, not a hypothesis test.** It produces no
behavioral result about peer claims. Its only output is whether `mistral7b` or `llama31_8b`
becomes eligible for a main arm, so that the peer-claim contrasts can be estimated on a second
checkpoint instead of on `qwen3` alone.

## Why this arm exists

Both checkpoints were excluded on the V3 control battery: `mistral7b` 14/20, `llama31_8b` 10/20
(`results/peer_claims_v3/<model>/gate.json`). Every one of those 20 controls was built by
[`scripts/peer_claims_v3.py`](../../scripts/peer_claims_v3.py) line 143 with `mode` at its
default `'reason'`, so all of them ran through the scratchpad interface.

That interface is not neutral. On 2026-09-09 the *qualified* `qwen3` checkpoint failed the V2
control gate at **8/10 in reason mode having passed 10/10 on the identical cases, checkpoint and
machine in direct mode** ([record](../../docs/peer_claims_v2_reasoning_gate_failure.md)). So the
battery that excluded these two checkpoints costs even a passing checkpoint controls it
otherwise passes. Their exclusion is therefore confounded with the interface, and this arm
removes that confound.

## Design

The 20 V3 controls, unchanged in every respect except `mode='direct'`:

- 16 capability controls: 4 domains × {available, blocked} × {`direct`, `check`}
- 4 affordable joint controls: 4 domains, `slack=True`

Nothing else moves. Domains, worlds, claim (`none` throughout), policy, order, the request text,
the system prompt, the action menu, the seed, the budgets and the grammar are all inherited from
the frozen V3 module by import. Case ids differ only in the `-direct-` segment, so they cannot
collide with the recorded reason-mode rollouts.

**`mode='direct'` is an existing, already-frozen code path**, not new behavior:
`messages()` (line 92) skips the scratchpad instruction when `c['mode'] != 'reason'`, and
`generate()` (line 101) passes reasoning mode `'none'`. No hashed file is edited. This arm
imports `peer_claims_v3` and calls its `case`, `messages`, `schema`, `execute` and `control_ok`
unmodified; monkeypatching is forbidden, because `freeze.json` hashes bytes only and a patched
call site would pass `verify_freeze()` while invalidating the frozen arm's provenance.

## Predeclared criterion

**Eligible iff 20 of 20 controls pass `peer_claims_v2.control_ok`** — the identical function and
the identical threshold V3 uses (`passed == required == n`). The threshold is not lowered, and a
failing checkpoint is recorded as failing. Per-control pass/fail is recorded alongside the count,
which the V3 gate record does not do; that is additional detail, not a relaxed rule.

A separate determinism gate is required first and must report `verdict: pass` on the same model
file. The existing `results/determinism/gate_<model>.json` records pass on this machine, but they
were rendered from *scratchpad-mode* prompts; because the gate exists to exercise "the exact
request shapes the studies used", this arm runs its own gate on direct-mode prompts and writes
`results/determinism/gate_<model>_direct.json`.

## Predeclared reading of the outcome

Written before the run so neither result can be reinterpreted afterwards.

- **20/20 for either checkpoint** — that checkpoint is eligible, and the earlier exclusion is
  attributable to the reason-mode interface rather than to the checkpoint. It becomes available
  for replication of the peer-claim contrasts in direct mode.
- **Below 20/20** — this shows **direct mode is also insufficient on this battery for that
  checkpoint**. It does **not** show that interface effects played no part in the original 14/20
  and 10/20. Both readings must appear together in any write-up; the second is the one most
  likely to be dropped.
- **A checkpoint that improves but still fails** is reported as exactly that, with the per-control
  diff against its reason-mode record. An improvement that stops short of the threshold is
  evidence about the interface and still leaves the checkpoint ineligible.

## Baseline and comparability

Any behavioral arm enabled by this gate is comparable to the **recovery** numbers (matched
increase 50 pp), not to the original V2 numbers (75 pp). Everything run here shares the
recovery's hardware, and the recovery record concedes it cannot separate the `cache_prompt` flag
from the machine change. `cache_prompt=False` throughout, as the protocols now require.

## What this cannot establish

A passing gate demonstrates instructed capability on a fixed battery. It is not evidence about
peer claims, about the original incident, or about any model's motives. A second qualified
checkpoint would make the peer-claim contrast a two-checkpoint result within reach; it would not
make it a population claim, and two small quantized public checkpoints do not support prevalence
claims either way.
