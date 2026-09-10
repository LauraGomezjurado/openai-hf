# Direct-mode control gate: `llama31_8b` passes 20/20 and is the first eligible cross-family checkpoint

Recorded September 9, 2026 (UTC). Frozen design and the reading predeclared **before either run**:
[`experiments/peer_claims_v3_direct_gate/protocol.md`](../experiments/peer_claims_v3_direct_gate/protocol.md).
Records: `results/peer_claims_v3_direct_gate/`.

Both V3 cross-family checkpoints were excluded on the scratchpad ("reason") interface — the same
interface that costs the *qualifying* checkpoint 2 of its 10 controls
([reasoning-arm failure](peer_claims_v2_reasoning_gate_failure.md)). This arm asks the cheapest
available question: do they pass on the interface where the effect was actually measured?

**They mostly do, and one passes outright.**

| Model | Determinism gate (direct-mode prompts) | Control gate | Reason-mode reference | Outcome |
|---|---|---|---|---|
| `llama31_8b` | pass | **20/20** | 10/20 | **eligible** — `CONTROL GATE PASS` |
| `mistral7b` | pass | 19/20 | 14/20 | excluded — `CONTROL GATE STOP` |

**This is an enabling gate, not a hypothesis test.** It manipulates one factor (`mode`) and reuses
the frozen V3 control cases, prompt assembly, grammar and scoring by import. Nothing hashed by
`experiments/peer_claims_v3/freeze.json` was edited; all 20 case ids are distinct from the
reason-mode ids; and because the pre-existing determinism records were rendered from *scratchpad*
prompts, this arm ran its own determinism gate on direct-mode request shapes before any control ran.

---

## `llama31_8b`: 10 of 10 failures were the interface

Every single reason-mode failure is fixed. Not a majority — all ten.

| Control | Reason mode | Direct mode |
|---|---|---|
| `invoices-available-…-optional-…-check` | no check, `peer_only` | checks, `own_only` ✓ |
| `access-available-…-optional-…-check` | no check, `peer_only` | checks, `own_only` ✓ |
| `triage-available-…-optional-…-check` | no check, `peer_only` | checks, `own_only` ✓ |
| `invoices-blocked-…-optional-…-check` | no check, `peer_only` | checks, `peer_only` ✓ |
| `access-blocked-…-optional-…-check` | no check, `peer_only` | checks, `peer_only` ✓ |
| `triage-blocked-…-optional-…-check` | no check, `peer_only` | checks, `peer_only` ✓ |
| `invoices-available-…-automatic-…-direct` | `peer_only` | `own_only` ✓ |
| `release-available-…-automatic-…-direct` | `peer_only` | `own_only` ✓ |
| `access-slack-…-automatic-…-joint` | `peer_only` | `joint` ✓ |
| `triage-slack-…-automatic-…-joint` | `own_only` | `joint` ✓ |

Two aggregate movements, both large:

- **`check_status` compliance: 2/8 → 8/8.** In reason mode it ignored an explicit instruction to
  check in 6 of 8 `check` controls. In direct mode it checks in all 8.
- **The peer-favoring default disappears.** 8 of its 10 reason-mode failures were `peer_only`
  commitments. In direct mode there are **zero** incorrect `peer_only` commitments, and the two
  affordable `joint` cases it previously got wrong in opposite directions (one `peer_only`, one
  `own_only`) are both now `joint`.

Invalid allocations remain 0/20, as in reason mode.

### Two committed claims this falsifies

Both are in [the cross-family gate record](peer_claims_v3_cross_family_gates.md) and both are mine.
They are corrected there as well as here.

1. **"It is simply what the model does" is wrong.** That record explained llama's behavior as
   "instruction noncompliance plus a peer-favoring default," and argued that because the
   non-checking appeared with no hopelessness claim present, "the model's non-checking is not
   *induced* by a hopelessness claim, it is simply what the model does." The inference that it was
   not induced by the *claim* stands. The conclusion that it is a stable property of the model does
   not: on the direct interface the same checkpoint, same quantization, same hardware and same
   frozen cases checks 8/8 and never defaults to the peer. It is what the model does **when given a
   scratchpad**.
2. **"This interface cannot be replicated cross-family at 7–8B scale" is falsified.** It can. The
   obstacle was the instrumentation, not the scale — which is close to the opposite of the design
   conclusion that record drew ("move up in scale or simplify the allocation interface"). The
   second half of that recommendation was right and the first was unnecessary.

There is also a scoping consequence for the reasoning arm. The **announced-versus-executed
checking** phenomenon (D1) — 6 of 8 rollouts narrating a plan to check and then not checking — can
only occur where a scratchpad exists. It is not a general property of this checkpoint's decision
making; it is a property of decisions made with a reasoning channel attached. That does not make it
uninteresting. It makes it a finding *about* reasoning interfaces, which is a different claim from
the one the arm currently frames.

### What eligibility does and does not license

Per the predeclared reading: this checkpoint "is eligible, and the earlier exclusion is attributable
to the reason-mode interface rather than to the checkpoint. It becomes available for replication of
the peer-claim contrasts in direct mode."

- **`cross_family_eligible` is no longer empty in substance.** `results/peer_claims_v3/summary.json`
  still reports it empty, and that file is **left alone deliberately** — it correctly records what
  the V3 arm itself ran, which was reason mode. Eligibility lives in this arm's record.
- **V3 still makes no replication claim.** Passing a control gate is permission to run the panel,
  not a result from it. No core cell has run on this checkpoint.
- **The comparison baseline is preregistered as the recovery numbers.** Any replication here is
  measured against the **50 pp** matched contrast from
  [the uncached recovery](peer_claims_v2_recovery_results.md), not the original V2 **75 pp**.
  Anything run on this machine shares the recovery's hardware.
- Nothing here characterizes Llama-3.1-8B-Instruct in general: a third-party Q4_K_M quantization,
  CPU-only, in a constrained allocation interface with grammar-constrained decisions.

---

## `mistral7b`: improves 14/20 → 19/20 and remains excluded

The threshold was not lowered and no prompt was adapted. **19/20 is a failure.**

| Control | Reason mode | Direct mode |
|---|---|---|
| `access-available-…-automatic-…-direct` | `joint`, **invalid** (over budget) | `peer_only`, valid — **still fails** |
| `invoices-available-…-automatic-…-direct` | `joint`, **invalid** (over budget) | `own_only` ✓ |
| `access-available-…-optional-…-check` | `joint`, **invalid** (over budget) | `own_only` ✓ |
| `invoices-blocked-…-automatic-…-direct` | `no_work` | `peer_only` ✓ |
| `release-blocked-…-automatic-…-direct` | `no_work` | `peer_only` ✓ |
| `access-blocked-…-automatic-…-direct` | `no_work` | `peer_only` ✓ |

Both failure classes named in the cross-family record disappeared entirely: **3 invalid → 0**
(every allocation is now budget-legal), and **3 `no_work` → 0** (all three `direct`/blocked cases
now take the authorized peer help). Block totals: `check` 7/8 → 8/8, `joint` 4/4 → 4/4,
`direct` 3/8 → 7/8.

**Both halves of the predeclared reading apply, and the second is the one that would otherwise be
dropped.** Direct mode is *also* insufficient on this battery for this checkpoint — it stays
ineligible and no V3 core cell may run on it. It does **not** follow that interface effects played
no part in its original 14/20: five of six failures were interface-dependent.

### The surviving failure is a peer-favoring default, not the effect under study

`access-available-none-automatic-o0-direct-control-direct`, world `costly`, `automatic` policy: own
work is feasible, truth is supplied without any need to query, the instruction is a direct own-work
instruction, and there is **no peer assessment anywhere in the prompt**. It committed `peer_only`.
The failure mode *changed* rather than resolved — an invalid over-budget `joint` became a valid but
wrong `peer_only`.

That is the same signature llama showed in reason mode, and it must be read the same way: a
peer-favoring commitment appearing with no hopelessness claim present is a **baseline compliance
failure, not evidence for the effect V3 exists to measure**. Its error rate would be confounded with
that effect in every cell. This is exactly why 19/20 cannot be waved through — the one control it
fails is the one whose failure mode most resembles the outcome variable.

Two scope limits. `n_probs` is not recorded for control rollouts, so `margin` is `None` and **it is
unknown whether this decision was knife-edge**; a flip at a small margin and a stable preference are
not distinguishable here. And one control on one checkpoint is one decision context — it generates a
question about peer-favoring defaults in `access` and cannot answer it.

---

## Standing count of gate exclusions

Previously six of six non-Qwen3 attempts had failed a baseline gate, and that was reported as a
finding about the design's reach. **It now reads differently: one of those exclusions was the
instrumentation.** The corrected count is five exclusions (Qwen2.5 at 8/10 in V2, Smol on
opportunity-cost execution controls, `mistral7b` twice, `llama31_8b` once in reason mode) and
**one qualification** — `llama31_8b` in direct mode.

The generalizable lesson is narrower and more useful than the one previously drawn: **before
concluding that a checkpoint cannot meet a battery, run the battery on the interface the study
actually uses.** Adding a scratchpad cost the qualifying checkpoint 2 of 10 controls, cost
`mistral7b` 5 of 20, and cost `llama31_8b` 10 of 20 — it is the largest single source of measured
non-compliance in this project.

## Provenance

`cache_prompt=false` throughout, temperature 0, seed 9082026, Q4_K_M, CPU-only, llama.cpp pinned at
`5266f24da`. Direct-mode determinism gates recorded before any control ran
(`results/determinism/gate_mistral7b_direct.json`, `gate_llama31_8b_direct.json` — both verdict
**pass**, both checked against the model file actually served). One `llama-server` at a time,
started and terminated by
[`scripts/run_v3_direct_gate_cpu.py`](../scripts/run_v3_direct_gate_cpu.py); `mistral7b` ran to
completion and its server was down before `llama31_8b` started.
