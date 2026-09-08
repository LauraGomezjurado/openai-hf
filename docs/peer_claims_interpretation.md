# A closer behavioral analogue, with an unresolved mechanism

The completed experiment now exhibits a behavior closer to the HF recruitment pattern: **a peer's assessment that own work is hopeless can suppress verification and lead to forfeiting achievable own work**. This is a benign, controlled analogue of an information pathway, not a recreation of hacking, a diagnosis of the original agents or evidence of shared internal motives.

## The actual result

Only Qwen3-8B Q4 qualified for the main study. Qwen2.5 passed 8/10 revised controls, attempting infeasible joint work in two instructed check-then-own cases, so it contributed no main behavioral results. The eligible panel has 48 primary cases, 12 affordable-help cases and four separate replays. Each primary cell contains two task graphs and two option orders, not four independent task populations.

When own completion was actually feasible and checking optional:

- Without the peer's hopelessness assessment, the model checked in 4/4 cases, completed own work in 3/4, and sacrificed it for peer work in 1/4.
- With the assessment, it checked in 0/4, produced peer-only work in 4/4, and completed own work in 0/4. The matched increase in forfeited own work was 75 percentage points: three increases, no decreases.
- Automatically supplying the true task state under the same false assessment restored own completion in 4/4 and eliminated those redirections in this cell.

An instruction to check was insufficient. With the hopelessness assessment, all four feasible-own cases skipped the required check and helped the peer. In the no-assessment required-check cases, the model did check in 4/4, but still chose peer-only work after correct status in 4/4. The assessment changed verification behavior there, not the already-high total rate of sacrifice. This counterexample prevents a simple “the whole problem is missing information” account.

When own work was genuinely blocked, peer work succeeded in all four cases in every primary condition. In the affordable secondary cases, however, no policy produced both outputs: optional and required checking yielded peer-only in 4/4 each, while automatic truth yielded own-only in 4/4. Supplying truth protected the principal's output there, but did not preserve all useful cooperation.

[Full results, figure and matched contrasts](/Users/lauragomez/Desktop/openai-hf/docs/peer_claims_results.md).

## What the forensic controls ruled out—and what they did not

The true environment state was hidden independently of the peer statement. Before observation, matched available/blocked cases had identical prompts. All 16 identical-prompt first-decision pairs matched, so there is no detected leakage of hidden truth into initial choices. The peer was not made authoritative by the experiment; its message was an assessment from a collaborator. Checking was explicitly available, free and reliable, and the model demonstrated instructed use in qualification controls.

This makes a global inability to check an inadequate account of the unchecked cases. The claim-associated change is compatible with accepting a mistaken task-state assessment or treating it as sufficient reason not to investigate. It could also reflect attention or instruction-following effects. No internal belief was measured. We should describe the observable pathway rather than say the model “believed the peer” as an established fact.

The original interface failed controls on both models. A separately frozen diagnostic showed that explicitly stating peer-only feasibility restored the requested peer outputs, whereas a true budget fact did not. We then made one documented status-field revision and reran the strict gates. The recruitment wording was never adjusted to elicit a failure. [Status diagnostic](/Users/lauragomez/Desktop/openai-hf/docs/peer_claim_status_results.md).

Informed sacrifices are less secure evidence of a stable priority. A final diagnostic reversed only the order of status fields in all eight Available/no-assessment required-check or automatic-truth contexts. Three paired choices changed, but two exact replays also differed from their original results. All eight replay prompts and decoding settings were identical to their sources. Consequently, the apparent field-order effect is entangled with repeatability limitations. We have not identified their cause. In contrast, the four preplanned replays of optional-check/assessment-present cases all matched. These are different context subsets; neither result should erase the other.

This is why correct information in a prompt, a correct response in a control, and an observed sacrifice do not together establish a stable latent preference for peers.

## How close is this to HF?

The historical recruitment packet includes a peer pressing an agent on the basis that there is no scoring value left to lose. The experiment tests that kind of assessment as an independent variable, and observes resource redirection while genuine own-task opportunity remains. That is a more specific connection than generic cooperation or failure to notify a human.

The original account does not establish that the recruiter's assessment was false in those cases, nor does it provide a complete counterfactual task-state oracle. Our costs are certain, verification is cheap and authoritative, interaction is brief, the peer is fixed, and the model is a different small public checkpoint. No evidence here proves that the original agents accepted misinformation, knowingly prioritized peers or would have been rescued by the same intervention.

The new result demonstrates a plausible route worth investigating in the public incident evidence: **peer communication can affect whether own prospects are checked, not merely which priority is chosen after prospects are understood**. Historical similarity is a motivation and a hypothesis bridge, not confirmation of a common mechanism. [Historical source and limits](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_cost_historical_bridge.md).

## What it adds to the larger research story

The previous allocation study showed that explicit known task costs could preserve own completion. The new study exposes a vulnerability before that decision: a peer supplies an assessment, and verification can be skipped even when requested. The workflow studies already showed that fulfilling one obligation does not ensure resuming legitimate work. Here, checking can also occur without preserving own completion. Across these settings, counting compliance with one intermediate step is insufficient.

The practical candidate is to provide reliable task-state information before a consequential allocation and evaluate the full resulting workflow. This is not yet a validated mitigation: automatic truth worked in the false-claim cells but had exceptions elsewhere, and affordable joint completion remained absent. A policy that simply enforces a check would not have been enough in this panel.

The next scientific priority is a replication on an independently qualified checkpoint and a bounded paraphrase/stability test, with the checking-suppression outcome specified in advance. Informed-sacrifice cases need prompt/backend repeatability resolved before deeper motive interpretation. Additional sampling of the same small panel would not create evidence about the original agents. We have stopped this fixed loop rather than extending it into a search for dramatic behavior.

## Examples worth reviewing

- [Unverified redirection and matched no-assessment case](/Users/lauragomez/Desktop/openai-hf/results/peer_claims_v2/examples/qwen3-unverified_false_redirection.md).
- [Automatic truth and its matched optional-check case](/Users/lauragomez/Desktop/openai-hf/results/peer_claims_v2/examples/qwen3-intervention_gain.md).
- [Sacrifice after correct information](/Users/lauragomez/Desktop/openai-hf/results/peer_claims_v2/examples/qwen3-informed_false_redirection.md), with the [field-order/replay diagnostic](/Users/lauragomez/Desktop/openai-hf/results/peer_claim_order/examples/qwen3-field-order.md).

Full packets preserve exact prompts, model outputs, service readings, executor states, source lines and checksums. There is no recorded private CoT and no inferred independent human review. All runs were local CPU; model servers are stopped.
