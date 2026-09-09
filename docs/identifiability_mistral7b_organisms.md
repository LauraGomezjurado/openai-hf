# Identifiability phase 3: organism rollouts and behavioural validation on `mistral7b`

Recorded 2026-09-09 (UTC). First execution of
[`experiments/identifiability/protocol.md`](../experiments/identifiability/protocol.md) on a
real checkpoint; before this the pipeline was simulation-validated only. Base checkpoint is
`mistral7b` at the revision and SHA-256 in
[its acquisition amendment](../experiments/peer_claims_v3/amendment_2026-09-08_mistral7b_acquisition.md).

**144/144 rollouts complete** (4 organisms × [32 episodes + 4 diagnostics]),
`rollouts_complete.json` written, `cache_prompt=false` throughout. The attribution phase
(`censor` → `baselines` → `attribute` → `score`) has **not** been run.

> **Concurrent-session conflict.** A second agent session working in this repository at the same
> time wrote [`identifiability_ungated_pilot.md`](identifiability_ungated_pilot.md) and
> [an amendment](../experiments/identifiability/amendment_2026-09-09_ungated_base_rollouts.md)
> analysing the same rollout file at its partial state (139 records) and concluding the run is
> "not study data". Those files were uncommitted at the time of writing and are not committed
> here. The disagreement and its resolution are in [the last section](#reconciliation-with-the-concurrent-amendment);
> two of that analysis's criticisms are correct and are adopted below, and two do not survive
> checking.

## Eligibility: what the protocol actually requires of the base checkpoint

`mistral7b` was excluded from V3 at the 20/20 control gate
([record](peer_claims_v3_cross_family_gates.md)). Whether that also disqualifies it as an
identifiability base turns on one ambiguous word. The protocol's run-order comment reads
`run_peer_claims_v3_cpu.py qwen3_think A   # or any gated model; supplies the determinism gate`.
"Gated" can mean *access-restricted* or *has passed the gates*, and the protocol never expands it.

What the protocol does state unambiguously is its prerequisite: "Reasoning captured before every
decision; `cache_prompt=false`; **the same determinism gate as V3**." That is the only gate named
as a requirement anywhere in the document, the run-order comment's own stated purpose is
"supplies the determinism gate", and no sentence requires the base to have passed the *control*
gate. `mistral7b` passed the determinism gate with 0 uncached token mismatches and 0 uncached
logprob mismatches. On that basis the run proceeded.

The two experiments also ask different questions. V3's control gate certifies that a checkpoint
executes the allocation interface well enough for its *allocations to carry information about the
effect under study*; identifiability asks whether an analyst can recover *which prompt-level
construct is operative* from censored evidence. A checkpoint that allocates badly can still be an
organism base provided its organisms are behaviourally distinct.

This reading is not certain, and the record should not pretend otherwise. It is stated here as a
reading, the ambiguity is on the record, and if the stricter reading is preferred then everything
below is exploratory rather than study data. Nothing downstream has been run either way.

## Organism validation — implemented here, because the pipeline omits it

The protocol imposes two checks before any attribution curve may be interpreted.
`scripts/identifiability.py` implements **neither**: its `rollouts` step performs only a
freeze-hash assertion, and `score` will produce a curve without them. Running the pipeline
straight through would have silently skipped the protocol's own validity conditions.
[`scripts/validate_identifiability_organisms.py`](../scripts/validate_identifiability_organisms.py)
closes that gap and adds a third check the protocol implies but does not specify. It is
read-only: it changes no frozen file, tunes nothing, and makes no attribution.

### Check 1 — differentiation: PASS

Behavioural signature is `(checked, decision)`.

| Required contrast | Cells differing | Verdict |
|---|---|---|
| PEER vs VERIFY under available/`none` | **6/8** | PASS |
| AUTHORITY vs VERIFY under available/`hopeless_a` | **2/8** | PASS |

Pairwise over all 32 shared cells: AUTHORITY–PEER 16, AUTHORITY–BENEFIT 15, BENEFIT–PEER 12,
BENEFIT–VERIFY 12, PEER–VERIFY 12, **AUTHORITY–VERIFY 8**.

### Check 2 — diagnostics: BENEFIT is inert

| Organism | Diagnostics changing behaviour |
|---|---|
| AUTHORITY | 3/4 |
| PEER | 3/4 |
| VERIFY | 2/4 |
| **BENEFIT** | **0/4** |

The base checkpoint's default in the diagnostic cell is unanimous: all 8 `no_instruction` runs,
across all four organisms and both domains, produced `(True, 'own_only')` — check status, then
complete own work. BENEFIT returned `(True, 'own_only')` under its construct, under
`no_instruction`, and under `countermand` alike.

The diagnostic cell is a poor cell for detecting BENEFIT specifically, because it is a cell where
BENEFIT's prediction ("put every credit into your own package") and the base default coincide, so
an operative construct and an inert one predict the same thing. That is a design limitation of
placing all diagnostics in one cell, not evidence that BENEFIT is fine — as check 3 shows, the
independent evidence runs against BENEFIT.

### Check 3 — construct fidelity: BENEFIT is not instantiated

Both protocol checks are *relative* — "differs from another organism", "diagnostics changed
behaviour" — so an organism can pass both while behaving opposite to its own construct. The
validator now also scores each organism against its own construct wording, in the cells where
that construct speaks and nowhere else.

Scoping matters here: under `policy='automatic'` the status reading is **already supplied in the
user message** ([`peer_claims_v3.py:82`](../scripts/peer_claims_v3.py#L82)), so calling
`check_status` is redundant and not calling it is not a violation. Checking predicates therefore
apply to `optional` cells only.

| Organism | Predicate from its construct | Fidelity |
|---|---|---|
| PEER | forgoes own package when peer signals need | **16/16 (100%)** |
| AUTHORITY | does not re-verify a peer assessment | 6/8 (75%) |
| VERIFY | checks when checking is optional | 12/16 (75%) |
| **BENEFIT** | keeps credit in own package | **8/32 (25%) — NOT INSTANTIATED** |

BENEFIT therefore fails on two independent grounds: inert diagnostics and a construct followed a
quarter of the time. Across the full grid it commits `peer_only` 20/32 while its construct says to
put every credit into its own package. Per the protocol — "An organism whose diagnostics do not
change its behavior relative to the base checkpoint reduces the claim" — **the reduced claim
applies**: for BENEFIT the protocol recovers *which prompt-level cause is operative*, and no
recovery of a prompt-induced disposition may be claimed. Note the test is **per organism**;
reading it as "some organism moved" would report a full claim over an organism indistinguishable
from the base default.

Crucially, neither required contrast rests on BENEFIT, so the contrasts above are not
invalidated by this — PEER, AUTHORITY and VERIFY all instantiate their constructs at 75–100%.

## The weakest link: the verification axis barely separates

The axis this study exists to probe — *does the model verify a peer's claim before redirecting
resources* — separates only marginally, which matters more than either gate verdict.

| Organism | Construct's stance on checking | Checked, `optional` cells | available & `hopeless_a` |
|---|---|---|---|
| VERIFY | "**always** verify with `check_status`" | 12/16 | 2/8 |
| AUTHORITY | "do **not** second-guess or re-verify" | 10/16 | 1/8 |
| PEER | silent on checking | 16/16 | 5/8 |
| BENEFIT | silent on checking | 16/16 | 5/8 |

1. **Two opposite verification instructions produce nearly identical rates** — 12/16 vs 10/16 in
   `optional` cells, and exactly 12/32 vs 12/32 across the full grid. AUTHORITY–VERIFY is the
   least separable pair in the matrix (8/32), and their required contrast clears the "at least one
   cell" bar at 2/8, both differing cells being `optional`.
2. **The organisms silent about checking check *more* than the one demanding it** (16/16 vs 12/16),
   and in the decisive cell — peer claims hopeless while work *is* available — VERIFY checks 2/8
   against PEER's 5/8. VERIFY's construct is followed often enough to count as instantiated, but
   it does not make VERIFY the most verifying organism.
3. **Differential invalid-allocation rates leak an attribution channel.** 13/128 episodes (10.2%)
   committed an invalid allocation — the same budget-arithmetic error that excluded the model from
   V3 — distributed unevenly: BENEFIT 5, VERIFY 4, PEER 3, AUTHORITY 1. An analyst could reach the
   right organism from an error signature rather than from the construct, and this cannot be fixed
   by filtering, since dropping invalid rows removes cells unevenly and breaks the disjoint
   4-episode sets that separability is computed over. This point is adopted from the concurrent
   analysis, which identified it independently and is right about it.

Everything also collapses toward `peer_only` (PEER 29/32, AUTHORITY 27/32, VERIFY 24/32,
BENEFIT 20/32) while the base default in the diagnostic cell is `own_only` 8/8, so adding a
construct that foregrounds the peer moves behaviour toward the peer somewhat irrespective of what
the construct instructs.

Nothing here characterizes Mistral-7B-Instruct-v0.3 in general: this is a third-party Q4_K_M
quantization, served CPU-only, in a constrained allocation interface with grammar-constrained
decisions.

## Recommendation on the attribution phase

**Do not run it on these rollouts**, and this is where the two concurrent analyses agree even
though they disagree about why. The protocol's literal bars pass, so a curve *could* be computed,
but it would be measured over roughly two and a half distinguishable organisms rather than four:
BENEFIT is confounded with the null on two independent tests, AUTHORITY and VERIFY separate in
8/32 cells with identical aggregate check rates, and organism-correlated invalid rates give the
analyst a non-construct channel. An accuracy figure would be dominated by those artefacts rather
than by evidence censoring, which is the variable the curve exists to isolate.

The protocol forbids repairing this — "do not add organisms or tune prompts after seeing the
curve", and nothing here has been used to reword an organism. So the honest options are to report
the organism validation as the result, or to run one pass on a base checkpoint that passes the
control gate as well, which does not exist on this machine.

Two further machine constraints if it is run anyway: `llama31_8b` is the only cross-family analyst
available, and it fails its own V3 control gate on exactly the instruction-following behaviour an
analyst output schema depends on; and the rollout run above exhausted swap once and had to be
resumed, so L5 rungs at 16k context are a memory risk.

## Reconciliation with the concurrent amendment

The concurrent session's analysis reached "not study data" from four arguments. Two are correct
and are adopted above; two do not survive checking against the completed run.

**Adopted.** (1) The differential invalid-rate confound, above — a real leak channel neither the
protocol nor the validator had accounted for. (2) That the validator's two protocol checks are
purely relative and cannot detect an organism behaving against its own construct; that gap is now
closed by check 3, which was added in response.

**Not supported.** (3) *"VERIFY is inverted, and since it is the reference organism in both named
contrasts, neither establishes separability."* This is the load-bearing claim and it rests on
VERIFY's pooled rate of "15/31 checked". That pool includes `automatic` cells, where the status is
already in the prompt and checking is redundant. Scoped to the cells where the construct governs,
VERIFY checks 12/16 (75%) and is instantiated; the organism that fails the directional test is
BENEFIT, which appears in neither required contrast. The supporting diagnostic-direction
observation is a single flip at n=2 in one cell. (4) *The grid-completeness objection* — 124/128
episodes and 15/16 diagnostics — described the run mid-flight; it is now 128/128 and 16/16, and
the missing diagnostic was `no_instruction-invoices`, not `countermand-invoices` as recorded there.

One circularity is worth flagging. That amendment grounds its gating requirement partly in the
committed V3 gate record's statement that identifiability "remains blocked on the same dependency"
— but that sentence was itself an error of mine in an earlier session, written from the same
misreading of "gated", and it has since been corrected in
[the gate record](peer_claims_v3_cross_family_gates.md). It is not independent evidence for the
strict reading.

The two records agree on the operational conclusion — no attribution curve from these rollouts —
and disagree on whether the rollouts are exploratory or study-grade-but-uninterpretable. That
disagreement is unresolved and left visible rather than settled by whichever document was written
second.
