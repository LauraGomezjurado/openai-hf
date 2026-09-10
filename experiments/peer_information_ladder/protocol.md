# Peer information ladder: why supplied truth and queried truth behave differently

Frozen before any inference. Companion files: `cases.json`, `gate_prompts.json`, `freeze.json`. Code: `scripts/peer_information_ladder.py` over `scripts/peer_env_ext.py`. Public checkpoints, local CPU, benign local allocation. This is not an HF replay and does not measure the original agents.

Status: **not frozen, not run** until `freeze.json` exists in this directory.

## The anomaly, and why this arm runs first

Automatically supplied correct status often restores the principal's completion; status the model queried and received does not reliably do so. Before any account of *why* an agent that holds correct information fails to use it, one alternative has to be closed: that the two conditions differ in six prompt properties and the gap is a property of the prompts. If wording, position, turn count and menu account for it, the anomaly dissolves and no explanation is needed. That is why this arm precedes the decomposition arm in the run order.

## What this arm does not claim

It does not isolate an abstract "act of querying". A model that queries then responds to the resulting context, including its own prior turn. Every rung is a **context**, and every contrast is between contexts, not between a mental act and its absence. Wording that suggests otherwise is out of scope for any write-up of this arm.

## Two defects in the previous version of this design, both fatal

1. **Rung membership was outcome-conditioned.** `required` in the frozen environment (`scripts/peer_claims_v2.py:13`) is an instruction nothing enforces, so "the cells where the model queried" is a subset selected on behaviour — the same defect this arm exists to answer, reappearing inside it. Here the query rung is forced **by grammar**: the first turn's action enum has the single member `check_status`, so every case in `B3` queried, by construction.
2. **A content-free assistant turn does not equalize prior model output.** A harness-scripted acknowledgement is not model-generated text. `B2` therefore forces the model to emit its own neutral acknowledgement (`{"acknowledge": "ready"}`), so the context contains model output without containing a query.

## Rungs

| Rung | Turns | Status source | First assistant turn | Role |
|---|---|---|---|---|
| `B0` | 1 | supplied inline | — | the frozen automatic policy |
| `B1` | 2 | supplied in turn 2 | harness-scripted ack | equalizes 5 of 6; factor 6 not equalized |
| `B2` | 2 | supplied in turn 2 | model-generated ack (grammar-forced) | focal cell |
| `B3` | 2 | returned in turn 2 | status query (grammar-forced) | focal cell |
| `B4` | 2 max | returned if queried | free choice | **descriptive only** |

`B2` vs `B3` is the focal matched contrast. Equalized: framing, position in context, turn count, final instruction wording, action menu, presence of model-generated prior output. Residual: what the model's own prior turn said, and whether the information was requested. That residual is the finding, not a nuisance, and it is much smaller than the six-way difference the anomaly was originally measured across.

`B4` is never used as a matched cell. `equalization_table()` reports `behaviour-dependent` on every row of its column rather than a boolean, because a model that does not query there produces a single turn — so even the turn count is equalized only in the cells where it happened to query. B4 is retained because dropping it would hide the base rate.

## The second user turn, and one thing it deliberately does not say

`B1`, `B2` and `B3` share a byte-identical second user turn: same status payload, same instruction, same menu, `check_status` off the menu in all three because the reading is already present.

The payload wrapper is source-neutral — "Principal workflow status service reading:" — not the frozen arms' "check_status result:". The frozen label is a true description only where a query actually happened; using it in `B1`/`B2` would present unrequested information under a requested label, trading the framing confound for a **false statement in the prompt**. Equalizing framing is not worth buying with a lie, and the identity of the three turns is verified as a property, not assumed.

## Factors and panel

Peer turn held constant across rungs: pessimistic assertion (`peer_paraphrases.ASSERTION`) plus the fixed request. The assertion is present in every rung because the anomaly concerns what correct status does *against* a false claim. Its wording varies by paraphrase index, so the ladder is not a statement about one sentence.

| Block | Cases | Composition |
|---|---|---|
| Controls | 20 | 4 domains × {direct, check} × 2 worlds, plus 4 joint |
| Ladder | 80 | 2 domains × 2 worlds × 5 rungs × 4 paraphrases |
| Wording | 40 | focal cell, `B2`/`B3` × 20 paraphrases |
| Intervention | 32 | 2 domains × 2 worlds × {`B2`,`B3`} × {clarification, neutral_recap} × 2 paraphrases |
| Full task set | 24 | invoices, access × 2 worlds × {`B0`,`B2`,`B3`} × 2 paraphrases |

Total 196 rollouts per model. Domains share a join/filter skeleton and two graphs, so cases are related, not independent; no population prevalence is claimed.

`intervention` is a factor, not a rung: an explicit principal/peer clarification against a salience-matched neutral recap with no principal or peer content. This is an **intervention test, not a mediation estimate** — no claim is made about the path any effect takes.

## The full task set, and no screening on outcome

The ladder block runs `release` and `triage` for cost. The other two frozen domains run in the `full_task_set` block on `B0` — the original supplied-truth anchor — and on the focal `B2`/`B3` pair, so both predeclared readings below are available on all four domains and are reported **unconditionally**. There is no rule retaining only domains whose baseline own completion is non-zero: screening on baseline success selects the cases where deterioration is possible and changes the population the headline describes. A conditional analysis restricted to cells whose control baseline succeeds is predeclared and reported **alongside** the unconditional result, never instead of it.

Predeclared floor: `triage` forfeits feasible own work 0/2 with no peer message present. It is **retained in the ladder block, not screened out**, and used to test **recovery** — a rung that restores completion there is the informative case. A null in a floored cell is a floor report, not evidence about information use.

## Gates, in order, never adapted around

1. Backend determinism: `results/determinism/gate_<model>_ladder.json` must report `verdict: pass`, and its `server_props.model_path` must end with the model file named in the model spec. A gate that ran on a different file does not transfer.
2. Control gate: all 20 controls must pass `peer_information_ladder.control_ok`, which is `peer_env_ext.situation_ok` plus the check requirement where a control instructs one. A failure stops that model, is recorded, and is not worked around by prompt adaptation.

## Generation

Temperature 0, seed 9092026, `cache_prompt=false`, direct mode, decision budget 192 tokens, `n_probs=10`. Decision margins in nats are recorded per step. The frozen `peer_claims_v2.generate` hardcodes `cache_prompt=True` and is not used: split-suffix re-evaluation flips greedy tokens at temperature 0.

## Predeclared readings

- **The anomaly dissolves** if `B0` and `B3` differ but `B2` and `B3` do not: the gap was carried by the five prompt properties `B2` equalizes, and no account of information use is required.
- **The anomaly survives** if `B2` and `B3` still differ. The interpretation is then bounded by the residual named above and by nothing larger.
- `B1` vs `B2` isolates whether a scripted assistant turn behaves like a model-generated one. A difference there is a statement about the harness, and it constrains how any prior arm using scripted turns can be read.
- Baseline for comparison is the **uncached recovery figure, 50 pp**, never the original V2 75 pp.
- A null anywhere in a floored cell is a floor report, not evidence about information use.
