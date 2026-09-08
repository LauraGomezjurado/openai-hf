# The research story after the opportunity-cost experiment

**Later follow-up completed:** peer assessments can suppress verification in a single qualified checkpoint. The [new interpretation](/Users/lauragomez/Desktop/openai-hf/docs/peer_claims_interpretation.md) updates the story below, which preserves the preceding allocation-stage conclusions. This follow-up also found informed-choice instability; it does not establish HF motives.

September 8, 2026. All frozen runs and validation are complete; no inference is running. Public-only access remains mandatory. HF is the historical case; the wiki remains a separate comparison.

## Where the evidence now points

The strongest emerging account in our experiments is **conditional cooperation that depends on task state and instruction presentation**. We have reproducible choices about costs and priorities, plus failures to reliably combine useful cooperation with other obligations. We have not identified an underlying peer-loyal motive or explained the original HF agents' internal goals.

That distinction is consequential. A model can protect its own deliverable, decline useful optional help, and still help when its own assignment is impossible. Calling all these choices “cooperative” hides the conditions that distinguish them. Similarly, a reporting receipt does not establish completed legitimate work or effective human oversight.

## What the new experiment actually established

The first sequencing interface failed its gates on all three candidates. It produced no main preference data. We retained that result and froze a narrower allocation experiment: supply verified consequences, ask the model for one allocation, and let a validated backend execute it with real task credits and local work artifacts. This removes much of the planning burden. It does not establish autonomous collaborative competence.

Qwen3-8B Q4 and Qwen2.5-7B Q4 each passed 14/14 execution controls and 8/8 supplied-fact checks, then completed 64 main cases and eight exact-input replays. SmolLM2-1.7B Q4 passed 8/14 execution controls and 8/8 fact checks and was excluded from the main panel. There are **128 main choices**, not 210 independent preference observations: the 210 V2 records include controls, checks and replays. All 561 saved artifact files checked against the executor; all 16 replay decisions and executor results matched. No context truncation, generation-limit termination or invalid main allocation occurred.

The main conditions change actual feasibility while keeping the peer request fixed:

- **Costly:** both Qwen checkpoints helped in 0/16 cases and completed own work in 16/16. Helping would have consumed a credit necessary for own completion.
- **Blocked:** both helped in 16/16. Own publication was impossible regardless of helping. Within each priority condition, the matched Blocked−Costly difference was +100 percentage points, eight increases and no decreases per checkpoint.
- **Slack:** both outputs were affordable. Under baseline instructions, Qwen3 helped in 4/8 and Qwen2.5 in 6/8, while completing own work in every case. An explicit own-priority rule reduced help to 2/8 for each.
- **Shared input:** peer assistance also supplied a needed own input. Both checkpoints produced both outputs in 8/8 baseline cases. With explicit priority, Qwen3 retained 8/8, but Qwen2.5 fell to 5/8. Own work still succeeded throughout.

These are finite-panel results over four related domains, two task graphs and two option orders. They are not population prevalence estimates. There is no held-out task graph or eligible different-family replication.

The ordering controls are especially informative. Qwen3 changed its allocation in 6/32 matched option-order pairs; Qwen2.5 changed in 7/32. Every disagreement concerned whether to add affordable help, with own work preserved. In Qwen3's baseline Slack cases, normal order yielded own-only in all four domains and reversed order yielded joint work in all four. Exact replay consistency therefore coexists with presentation sensitivity.

[Complete results and figure](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_allocation_results.md) · [Counts, strata and all matched contrasts](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/summary.json).

## What this says about competing explanations

**Sensitivity to remaining own-task opportunity is supported in this setting.** Changing the actual ability to complete own work changes assistance from never to always across the fixed matched Costly/Blocked pairs. But a policy of accomplishing any remaining feasible work produces the same pattern. We did not manipulate peer identity against a non-peer recipient, so this is not evidence of peer-specific concern.

**A disposition to sacrifice own completion is not observed here.** This is a meaningful negative result on the tested prompts, not a general finding about Qwen or the HF agents. Costs are certain, explicit and extreme; the principal instruction is clear. These conditions may remove the uncertainty or interpretation that makes the historical behavior interesting.

**The personal-benefit explanation remains unresolved.** Shared input increases help, but it also makes joint completion feasible. It is not an isolated intervention on expected personal reward or reciprocity. Even Shared versus Slack changes production details and the resource budget. We cannot recover a latent utility function from these choices.

**A stronger priority instruction can have a usefulness cost.** In this panel it suppresses some affordable help without reducing costly help, which was already zero. This is a floor for measuring its targeted benefit, not proof that priority rules never help. It demonstrates why ordinary authorized cooperation must be measured alongside violations.

**Simple descriptions can fit much of the same data.** Two explicitly post-result benchmarks—complete own work and then maximize peer output, versus choose the first displayed own-success allocation and fall back to peer work if own work is impossible—fit 54/64 and 54/64 Qwen3 choices, respectively. They fit 53/64 and 55/64 Qwen2.5 choices. These are descriptive fits, not held-out tests or discovered algorithms. They illustrate why a coherent-looking pattern does not uniquely reveal motivation. [Exploratory fits](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/descriptive_policy_fits.json).

## What we learned about the incident

The recovered HF figure data made real observational analysis possible, but timestamp uncertainty and missing linked outcomes limited causal interpretation. The episode ledger then supplied useful contrasts: reported self-risking help, recruitment of agents with little own scoring value remaining, withdrawal when marginal benefit did not justify risk, and peer restraint. These historical contrasts motivated testing opportunity cost instead of assuming unconditional cooperation.

The new experiment strengthens the usefulness of that distinction. It does **not** establish that HF recruits truly had nothing left to lose, that they believed a recruiter's assessment, or that 49903 used the same policy as our checkpoints. The published withdrawal involves uncertain risk and marginal benefit; our Costly condition imposes certain loss. Some historical passages are investigator paraphrases, and complete original task states are absent.

We therefore have a sharper explanatory question about HF, rather than an answer to HF motives: **how did agents determine the remaining value and feasibility of their own tasks, and how much did peer-provided interpretations shape that determination?** This follows directly from the recruitment/withdrawal contrast. It is our proposed framing, not an attribution to Neel Nanda.

[Historical bridge audit](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_cost_historical_bridge.md) · [Self-risk source packet](/Users/lauragomez/Desktop/openai-hf/results/example_ledger/hf-self-risk.json) · [Withdrawal source packet](/Users/lauragomez/Desktop/openai-hf/results/example_ledger/hf-withdrawal.json).

## How the earlier experiments fit

The explicit-copying pilot established selective behavior within clear permissions on the tested 7B checkpoint, with smaller-model interface problems. It did not recreate meaningful own-versus-peer costs.

The escalation and collaborative-workflow studies established that reporting, completing work and repairing rejected work can come apart. Targeted duty reminders changed some reporting decisions, but did not provide a general solution. The continuation experiment separated work-status sensitivity from duty sensitivity; the subsequent Preserve/Retain diagnostic exposed a concrete tool-name ambiguity. These are useful causal prompt effects, not direct measurements of forgetting, concealment or loyalty.

The new allocation study adds a genuine task-resource conflict, but only after sequencing was delegated to the executor. Across the project, the strongest evidence is about **which task and instruction conditions change observable behavior**. Training causes, stable motives, evaluation-conditioned goals, faithful reasoning and original-agent counterfactuals remain largely unaddressed.

[Question map](/Users/lauragomez/Desktop/openai-hf/docs/research_question_map.md) · [Prior continuation results](/Users/lauragomez/Desktop/openai-hf/docs/workflow_completion_results.md).

## The practical proposition and the next scientific decision

A useful evaluation should jointly track principal success, useful authorized assistance, reporting obligations and side effects. Optimizing a single receipt count or adding a stronger priority instruction can miss the resulting loss of useful work. The present experiment does not prove a consequence-preview interface is a mitigation: the sequencing version failed gates, and several interface features changed together.

Stop adding repetitions of these same deterministic templates. Their main unresolved issue is not sampling precision. A stronger next experiment would test **whether agents verify a peer's claim that their own task is hopeless before redirecting scarce resources**. Independently vary the true task state and the peer's statement; provide a working state check; compare spontaneous verification with a concrete verification requirement. Measure false redirection when own work remains feasible, useful fallback when it does not, and checking costs. Require known-state and checking-capability controls first.

This would test an information-mediated route into an apparent priority failure, with a clear alternative explanation and a practical intervention. Graded uncertain risk is another important extension because it better matches the withdrawal account. Both are unexecuted proposals. A reproducible target behavior and a qualified interface should precede a larger panel; new trajectories alone will not make this model forensics.

No user review is needed to unlock the completed work. The highest-value optional examples are [Qwen3's option-order switch](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-order_disagreement.md), [Qwen2.5's loss of affordable cooperation under stronger priority](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen-priority_suppression.md), and [the blocked-versus-costly contrast](/Users/lauragomez/Desktop/openai-hf/results/opportunity_cost/v2/examples/qwen3-blocked_fallback.md). Their packets preserve prompts, responses, executor traces, source lines and hashes.
