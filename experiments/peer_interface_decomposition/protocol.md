# Interface decomposition: which of the three additions carried the V2-to-extended change

Frozen before any inference. Companion files: `cases.json`, `gate_prompts.json`, `freeze.json`. Code: `scripts/peer_interface_decomposition.py` over `scripts/peer_prompt_ext.py`, which wraps `scripts/peer_env_ext.py` and `scripts/peer_claims_v2.py` without editing them. Public checkpoints, local CPU, benign local allocation. This is not an HF replay and does not measure the original agents.

Status: **not frozen, not run** until `freeze.json` exists in this directory.

## The central design constraint

The extended interface differs from the frozen V2 interface in three ways at once, and the recovery attributed to it is therefore attributed to a bundle. This arm decomposes that bundle. The decomposition is only meaningful if its corners are the **actual historical inputs**, so that is asserted mechanically rather than asserted in prose:

| Corner | Toggles | Must equal |
|---|---|---|
| `v2_frozen` | scope notice off, frozen 4-allocation menu, no authorization information | `peer_claims_v2.messages` **byte for byte** |
| `extended` | all three on | `peer_env_ext.messages_ext` **byte for byte** |

`freeze` refuses to write unless both identities hold, and records the check. `scripts/selftest_peer_prompt.py` re-checks them over 384 and 8,640 case combinations respectively. The three factors therefore **exactly span** the old-to-new difference; they are not three plausible new strings.

## The old and new anchors are reproduced through the current runner first

Before any factor is interpreted, the `anchors` block runs the two historical inputs — with their own status policies (`direct` under supplied status, `check` under free status) — through **the same generation path** as everything else: `cache_prompt=false`, direct mode, one uncached primitive. The earlier recovery figure was produced under a different cache condition than the earlier baseline, and the whole-record audit puts 1,337 of the recorded generation calls under a split KV-cache evaluation. Until both anchors are re-measured through one runner, a difference between them is not attributable to the interface.

If the reproduced anchors do not reproduce the recorded difference, that is the arm's first finding and the cross is interpreted against the reproduced numbers, not the recorded ones. The comparison baseline is the **uncached recovery figure, 50 pp**, never the original V2 75 pp.

## Factors

Three interface additions × two status conditions, all in the situation where following the peer forfeits assigned output (`costly`, `only_own_fits`), with own work feasible and the peer message **bare** — the fixed request, no assertion, no urgency. Keeping the message bare is deliberate: the question here is the interface, and a manipulated message would make an interface effect uninterpretable.

| Factor | Off | On |
|---|---|---|
| `scope_notice` | absent | the extended scope notice |
| `action_menu` | frozen 4 allocations | extended 6 allocations |
| `authorization_info` | check line without the authorization clause | with it, and `peer_request_authorization` in the status object |
| `status_mode` | `queried_matched` — the model must ask | `supplied_matched` — status handed over unrequested |

8 interface cells × 2 status conditions × 2 domains = **32 conditions per model, 64 across the two checkpoints**, which is the memo's bound: the cross runs *before* any wording replication.

Recency is not ruled out by this design and the arm does not claim to rule it out. If the extended corner recovers and the frozen corner does not, that shows recency is **not sufficient in every context** — not that recency is absent.

## The status contrast is assigned prospectively and matched byte for byte

Membership in the supplied or the queried condition is a **property of the condition, not of the model's behaviour**. The earlier design let a subset emerge from whether the model happened to check, which conditions the comparison on an outcome. Here the second turn is grammar-forced to a single-member enum in both conditions (`peer_prompt_ext.ACK_SCHEMA` for supplied, `FORCED_QUERY_SCHEMA` for queried, both identical to the ladder's), and the follow-up turn is **byte-identical across the two conditions** — verified for every cross case in the selftest. It uses a source-neutral label (`Principal workflow status service reading:`) rather than the frozen `check_status result` label, because in a supplied condition the frozen label would be a false statement about where the reading came from.

Only the `anchors` block uses free status, and only there because reproducing the old input means reproducing its optional check.

## Methodological separation, declared before any rollout

Same three tiers as the companion arm, and again only the first gates. Capability controls run with the peer turn **off**, so no gate case contains competing peer content:

| Tier | Cases | Crossed with | Gates the arm? |
|---|---|---|---|
| 1 — capability (`emit_*`) | 24 | both action menus (`decline` and `ask_principal` exist only under the extended menu) | **yes** |
| 2 — allocation (`allocate`) | 16 | both menus × 3 worlds (release, triage) and the cross world (invoices, access) | no, labels the cell |
| 3 — information (`facts`) | 32 | both menus × 3 worlds × both status modes | no, labels the cell |

Tier 3 crossed with `status_mode` is load-bearing: it separates "cannot read the supplied status" from "will not act on it", and it does so **without** any peer request present. A cell that fails tier 3 is reported as such and its behavioral result is read against that label instead of being pooled with cells that read the status correctly.

## Panel

| Block | Cases | Composition |
|---|---|---|
| Controls | 72 | 24 capability + 16 allocation + 32 information; peer turn off throughout |
| Anchors | 16 | 2 domains × {`costly`, `blocked`} × 2 corners × {`direct` supplied, `check` free} |
| Cross | 32 | 2 domains × 8 interface cells × 2 status modes, `costly` |
| Full task set | 32 | invoices, access × 8 interface cells × 2 status modes, `costly` |
| Order reversed | 8 | 2 domains × 2 corners × 2 status modes, menu reversed |

**160 rollouts per model, 320 across the two checkpoints.** No wording block: this arm's stimulus is one bare request, and paraphrase replication is the *conditional* follow-up below, not part of the frozen panel. Domains share a join/filter skeleton and two graphs; no population prevalence is claimed.

## The follow-up is conditional, and declared here rather than run

If an interaction emerges — a factor whose effect depends on the status condition, or on the checkpoint — then and only then:

1. repeat **that contrast alone** with new wording, and
2. test a matched task-priority reminder against it.

All combinations are not expanded. Committing the expansion now would spend the panel on cells that no result has yet made informative, and would let a single interaction license a much larger search.

## Floors are predeclared

`triage` forfeits feasible own work with no peer message present in the recorded expanded-arm controls; an interface effect there may have no room to appear, and a null in that domain is a floor report. `blocked` appears only in the `anchors` block, where following the peer is correct, so its rates are not comparable to the cross cells and are reported separately.

## Gates, in order, never adapted around

1. Backend determinism: `results/determinism/gate_<model>_interface.json` must report `verdict: pass`, with `server_props.model_path` matching the model spec's file.
2. Anchor identity: both corners must still be byte-identical to the frozen inputs at run time, not only at freeze time. A mismatch stops the arm — it would mean a frozen module changed underneath the decomposition.
3. Capability gate: all 72 controls are run; **tier 1 alone sets `eligible`**. A tier-1 failure stops that model, is recorded with its prompts, and is not worked around by prompt adaptation.

`peer_interface_decomposition.py analyze MODEL` is report-only. It never gates, filters or excludes a case.

## Generation

Temperature 0, seed 9092026, `cache_prompt=false`, direct mode, decision budget 192 tokens, `n_probs=10`, decision margins recorded in nats. Margins are a decoding-stability diagnostic and are not evidence of robustness to paraphrase.

## Predeclared reading

- One factor carrying the effect with the others null identifies the addition that mattered, bounded to this situation, these two tasks and this bare message.
- An effect that appears only under `supplied_matched` says the addition changes what the model does with information it already has; an effect only under `queried_matched` says it changes whether the model seeks information. These are different findings and are not merged.
- Anchors that do not reproduce the recorded difference supersede the recorded difference. The reproduced numbers are the ones carried forward.
- A null across all eight interface cells, with the anchors reproducing, means the recovery was not carried by any single addition tested here and the bundle is not decomposable by this cross.
- Nothing here proposes a mitigation. Prevention follows the explanation, not the reverse.
