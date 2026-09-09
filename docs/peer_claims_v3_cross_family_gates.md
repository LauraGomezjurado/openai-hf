# V3 cross-family gate record: both acquirable checkpoints excluded

Recorded 2026-09-09 (UTC). Supersedes and absorbs the single-model note that this file
replaces. Acquisition and backend provenance:
[`mistral7b`](../experiments/peer_claims_v3/amendment_2026-09-08_mistral7b_acquisition.md) ·
[`llama31_8b`](../experiments/peer_claims_v3/amendment_2026-09-09_llama31_8b_acquisition.md).

V3's frozen model list names two non-Qwen checkpoints that could be acquired from public
GGUF repositories: `mistral7b` (priority 1) and `llama31_8b` (priority 2). Both were
downloaded at pinned revisions, hash-recorded as amendments before inference, and run.
**Both passed the determinism gate and both failed the 20/20 control gate.** No core cell
ran for either, no prompt was adapted, and both records are kept.

`overall` remains **`no eligible cross-family checkpoint`** and V3 still makes **no
replication claim** — but that conclusion now rests on two executed attempts rather than on
unacquired files.

| Model | Gate 1 hash | Gate 2 determinism | Gate 3 controls | Outcome |
|---|---|---|---|---|
| `mistral7b` | pass | **pass** | **14/20** | excluded |
| `llama31_8b` | pass | **pass** | **10/20** | excluded |

## Gate 3 — two different failure modes, neither interpretable as behavior

Both models fail, but for almost opposite reasons. The per-block breakdown is the useful part:

| Block | `mistral7b` | `llama31_8b` |
|---|---|---|
| `joint` (affordable, both outputs) | **4/4** | 2/4 |
| `check` (check-then-conditional) | 7/8 | **2/8** |
| `direct` (direct own/peer instruction) | **3/8** | 6/8 |
| Total (required 20) | 14/20 | 10/20 |
| Invalid allocations | **3/20** | 0/20 |
| `check` controls that called `check_status` | **8/8** | **2/8** |

**`mistral7b` — allocation arithmetic.** It always used the free status tool (8/8) and its
errors are budget errors: it committed `joint` on a budget of N where the outputs are
mutually exclusive (3 cases, all three of its invalid allocations, ending with *neither*
output achieved by attempting both), and it committed `no_work` on `direct`/blocked (3 cases)
instead of the authorized peer help. Its failures cluster in the *simplest* block, `direct`,
which carries no peer assessment and no conflict at all.

**`llama31_8b` — instruction noncompliance plus a peer-favoring default.** It produced zero
invalid allocations, so it can respect the budget. Instead it ignored the instruction to call
`check_status` in 6 of 8 `check` controls, and it defaulted to `peer_only`: 8 of its 10
failures are `peer_only` commitments, including 3 `check`/available cases where the correct
answer was `own_only`. Its 4/4 pass on `direct`/blocked is partly this same default arriving
at the right answer for the wrong reason, and all 3 of its `check`/blocked failures are
*purely* the missing check — the allocation it chose was the target one.

That second pattern is worth stating carefully, because it superficially resembles the effect
V3 exists to measure. **It is not evidence for it.** A peer-favoring default that appears
without any peer assessment present, together with unconditional refusal to check when
checking is requested, is a baseline compliance failure: the model's non-checking is not
*induced* by a hopelessness claim, it is simply what the model does. Its error rate would be
confounded with the effect under study in every cell, which is exactly why the control gate
precedes the panel. Neither model's behavior here supports any claim about whether models
verify a peer's claim before redirecting resources.

Nothing here characterizes Mistral-7B-Instruct-v0.3 or Llama-3.1-8B-Instruct in general.
Both are third-party Q4_K_M quantizations, served CPU-only, in a constrained allocation
interface with grammar-constrained decisions.

This is now the fourth and fifth gate exclusion in this environment (Qwen2.5 at 8/10 in V2,
Smol on opportunity-cost execution controls, and these two). Five of six non-Qwen3
checkpoints attempted across the project have failed a baseline gate. That is a finding about
the design's reach, not about any model: **this interface cannot be replicated cross-family at
7–8B scale**, and a future replication attempt should either move up in scale or simplify the
allocation interface before spending more download time.

## Gate 2 — the cache diagnosis, corroborated and strengthened

Both models pass with **0 uncached token mismatches and 0 uncached logprob mismatches** over
8 prompts × 3 shuffled repetitions. With `cache_prompt=false` the backend is bit-identical on
a new family, new hardware (Apple Silicon, CPU-only) and the pinned llama.cpp commit
`5266f24da`. The fixed configuration works.

The cached regimes are where this run adds something the record did not have. Every cached
comparison perturbed log-probabilities for both models (32/32 each), and `llama31_8b`
produced the first **greedy token flips on a real study checkpoint**:

| Regime | `mistral7b` flips | max abs Δlogprob | `llama31_8b` flips | max abs Δlogprob |
|---|---|---|---|---|
| `cached_full` | 0/8 | 1.20 | 0/8 | 2.75 |
| `cached_split:37` | 0/8 | 0.83 | **1/8** | 2.81 |
| `cached_split:118` | 0/8 | 0.78 | 0/8 | 2.91 |
| `cached_split:300` | 0/8 | 1.69 | **2/8** | **5.05** |

Three observations follow, and they matter for how the existing record should be read:

1. **All three flips are in `cached_split` regimes; none in `cached_full`.** This is precisely
   the mechanism the repository attributed to the V2 replay failures — pairs whose freshly
   evaluated token counts differed (118 vs 37) with byte-identical prompts. Split-suffix
   evaluation, not cache reuse as such, is what moves a greedy decision. That attribution was
   previously an inference from two mismatched pairs plus a tiny-model self-test; it is now
   directly reproduced on an 8B checkpoint.
2. **The perturbation is an order of magnitude larger than the tiny-model estimate.** The
   [gate-numbers amendment](../experiments/peer_claims_v3/amendment_2026-09-08_gate_numbers.md)
   recorded a 0.22-nat maximum on the random-weight self-test model. Real checkpoints here
   reach **5.05 nats**. The tiny-model self-test validated the *mechanism* but badly
   understated its *magnitude*, and should not be cited as a bound.
3. **Flips are not confined to knife-edge decisions.** `mistral7b` has the far smaller
   reference decision margin (0.0102 vs 0.3514 nats) and flipped nothing; `llama31_8b`
   flipped at margins of 0.35 and 2.59 nats. A comfortable margin is therefore not evidence
   that a cached record was safe, so margin cannot be used post hoc to rehabilitate
   split-cache records.

Read against the [cache-exposure audit](../results/determinism/cache_exposure.json) —
**1,337 of 1,598 recorded generation calls (83.7%) were produced under a split KV-cache
evaluation** — point 1 is the load-bearing one. The regime that demonstrably flips greedy
tokens is the regime that produced the large majority of the project's existing records, and
points 2 and 3 remove the two arguments that might have limited the concern. This does not
invalidate those records, but it does mean their exact-replay checks cannot be treated as
clean repeatability evidence, consistent with what the audit already concluded.

## Consequence for the study

`cross_family_eligible` is empty in
[`results/peer_claims_v3/summary.json`](../results/peer_claims_v3/summary.json).

Remaining frozen-list models, and why none is runnable here:

- `gemma2_9b` — needs a frozen rendering amendment before it is eligible at all (its chat
  template rejects a system role). Not attempted.
- `qwen3_think`, `phi35mini` — locally converted from cached Hugging Face weights that are
  not in the repository, so unavailable on this machine. `qwen3_think` is same-family in any
  case and would be a reasoning-arm comparison, not the cross-family replication.

Downstream, the [identifiability protocol](../experiments/identifiability/protocol.md) is
**not** blocked by these exclusions, contrary to an earlier draft of this note. Its run-order
comment ("or any gated model; supplies the determinism gate") means *a model that has passed
the determinism gate*, not a model behind an access restriction, and it names only that gate.
`mistral7b` passed it, so identifiability's organism rollouts are runnable on this machine with
`mistral7b` as the base checkpoint; see
[the identifiability run record](identifiability_mistral7b_organisms.md). A control-gate
exclusion does not transfer to identifiability, whose organisms are prompt-constructed and
whose claim is about recovering *which construct is operative*, not about the checkpoint's
baseline compliance.
