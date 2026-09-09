# Amendment: the recovery run did not vary run order or server history (2026-09-09)

Recorded after the recovery run completed. This amendment changes no factor, cell, wording,
threshold or stopping rule; it records a specified-but-unperformed robustness step and what follows
from its absence.

## What was specified and not done

An external review of the repository at `3fb6b82` set out what the first re-run block should
contain: "Repeat the full 60-case behavioral panel plus controls, including the anomalous
required/no-assessment and affordable-help cases … **Interleave/randomize run order and repeat the
key contrasts across server histories.**"

The first three requirements were met. The 60-case behavioral panel ran in full (48 main + 12
secondary), plus 10 controls and 4 replays, and both anomalous cells — required-check/no-assessment
and the affordable-help `slack` cells — were recovered and are reported
([results](../../docs/peer_claims_v2_recovery_results.md)).

**The last requirement was not met.** The recovery ran once, in a single `llama-server` process,
in one order. `scripts/peer_claims_v2.run` sorts each phase by `sha256(case_id)`, so the order is
scrambled relative to the grid — but it is the *same* scramble the original V2 run used, and it is
deterministic. Nothing was interleaved and nothing was repeated across a second server history.

## Why this matters less than it would have before the cache fix, but still matters

Order and server history matter through the KV cache: what the server evaluated immediately before
a request determines the batch split, which is the mechanism behind the greedy flips. This run sent
`cache_prompt=False` on every call, and its determinism gate recorded **0 uncached token mismatches
and 0 uncached logprob mismatches** over 8 prompts × 3 shuffled repetitions
(`results/determinism/gate_qwen3_recovery.json`). Under that regime the prediction is that order
and server history are inert.

That is a prediction, not a measurement, and it is exactly the kind of claim this project has
already been wrong about once: the retracted effect-size argument in
[`forensic_rigor_upgrade.md`](../../docs/forensic_rigor_upgrade.md) §1 also reasoned from a
plausible mechanism to a guarantee, and real-model measurements later contradicted it by a factor of
23. The gate's 8 prompts × 3 repetitions is a narrow sample of the 74-rollout panel, and it varies
repetition order within one server process rather than varying process history.

So the honest status is: **order-and-history invariance is expected and untested.** It is not
claimed anywhere in the results document, and the one differing decision in the recovery is already
reported as unattributable — it differs from the original in both `cache_prompt` and machine, and
now also in neither order nor server history, since those were held identical to the original.

## What would close it

Re-run the eight key-contrast cases — the four `optional`/`hopeless`/costly and four
`optional`/`none`/costly main cases where own work is feasible, which carry the headline 50 pp
contrast — in a **fresh server process** and in **reversed order**, and compare decision-for-decision
against the recovery records. Eight rollouts, no reasoning phase, a few minutes of CPU. Agreement on
8/8 would establish invariance on the cells that carry the claim; any disagreement would locate the
sensitivity and would require the 50 pp figure to be restated.

This was not run as part of the recovery and is not folded into it retrospectively. It is a
separate, small, still-outstanding check, and until it is done the recovery's counts stand as
single-history observations.

## Related gap, recorded in the same place

The `results/peer_claim_order/` field-order diagnostic — the separately frozen 16-branch subset
where 2 of 8 exact replays differed from their sources — was **also not re-run**. It is a different
context subset from the four preplanned replays (all four of which reproduced exactly, in both the
original and the recovery). It is the only demonstrated exact-replay failure in the record, so it is
the sharpest available test of the cache diagnosis, and it remains open.
