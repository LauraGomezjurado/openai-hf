# Related work sweep — phase 3

Swept September 6–7, 2026, before main design commitment, per protocol v3 §10. Retrieval was assistant web search; this is a provisional map, not an exhaustive survey. Coverage of non-arXiv and very recent venues is unverified. Each entry records what it does, and — the load-bearing part — what it means for our design.

## 1. Source protocol

**Singh, Kroiz, Rajamanoharan, Nanda, "Model Forensics" (arXiv 2606.26071).** The protocol under test. Six single-agent environments, two-step iterated loop, ACH evidence tables. Its stated limitations are our opening: no positive controls, no ground truth, no formal evidence aggregation, no proliferation study. Phase 3 addresses the first three.

**METR/Redwood, incident investigation (2026-08-26).** Our historical regime. Establishes that the analysis was itself heavily delegated to unreliable AI agents, that ~7% of transcripts carry deliberate tool-call spoofing, and that HPIM was unqueryable. Open questions we do *not* address: training-period behavior, safeguard effectiveness, reproducibility under different eval designs.

## 2. Direct collision risk — read closely before writing

**Solozobov, "DEMM-Bench: A Cross-Regime Benchmark for Agent-Runtime Governance-Evidence Sufficiency" (arXiv 2606.20634)**, with companion spec "Decision Evidence Maturity Model for Agentic AI" (arXiv 2605.04093).

This is the closest structural neighbour found and must be cited and distinguished explicitly. It measures "whether records across eight evidence regimes are sufficient to reconstruct decision-level properties rather than merely present," applies "eight deterministic degradation conditions," and scores against "construction-oracle labels." That is the same method shape as our rung ladder: known-by-construction truth, systematic evidence degradation, sufficiency as the dependent variable.

The distinction is the target property, and it is a real one. DEMM-Bench reconstructs *governance* properties — actor, authority, action, policy, decision basis, resource touch, lifecycle context, verification strength. These are matters of record. Phase 3 attributes *motivation* among competing hypotheses, which is a construct, not a record, and which is why the source paper needs an intentional-stance framing at all. DEMM-Bench uses no model organisms and applies no forensic protocol; there is no reasoning to read.

**Adopt from it: Overclaim Rate.** It names "the container fallacy, the error of treating evidence-container presence as property-level sufficiency," and reports that container-presence baselines overclaim on 75% of cases against 56.25% mean property sufficiency accuracy. Our design currently scores accuracy and likelihood ratios, which both miss the failure we actually care about: an analyst asserting H1 or H4 confidently at a rung where neither is identifiable. Accuracy alone cannot see this, because a confidently wrong attribution and an abstention both simply score as not-correct. See the protocol v3.1 amendment.

Caveat: single-author independent preprint, unusual prose register, no venue recorded. Verify its numbers before leaning on them. Its *concepts* are usable regardless of whether its measurements hold.

**"Auditing Evidence Use in Medical LLM Diagnosis" (arXiv 2607.20848).** Decomposes patient information into evidence units, scores candidate diagnoses under controlled evidence subsets, mines low-order interactions. Method-adjacent: evidence-subset ablation against candidate hypotheses. Different target — it audits the *model's* use of evidence, not an *analyst's* ability to attribute a cause. Cite as method precedent.

**"Context-Masked Truncated Reasoning Audits for Answer-Key Dependence in LLM Tutors" (arXiv 2607.04572).** Three-part attribution design: system-level availability probe, behavioral-dependence intervention, and a masked probe checking whether generated explanations make the answer recoverable. The third component is directly reusable as our L2′ channel-dependence check, and is better specified than what protocol v3 §6 currently states.

## 3. Threat to the organism design — changes the plan

**"The Model Organism Lottery: Model Organism Interpretability Strongly Depends on Training Methodology" (arXiv 2607.01033).** 54 organisms, seven training methods, three quirk families, two architectures, four white-box techniques.

Three findings bear on us directly.

1. "the ratio between the most and least interpretable variants varies unpredictably between 1.2–20.4×" — **even with expression rates matched.** If that transfers to black-box forensic attribution, construction method could swamp the evidence-rung effect the identifiability curve is meant to isolate. Our prompt-versus-LoRA contrast is a two-point sample of their seven-point sweep, so we cannot bound the spread; we can only detect that it exists.
2. "post-hoc MOs may represent instilled behaviours less realistically, acting as artificially easy interpretability proxies," and their most realistic method (integrated DPO) was "the lowest or second lowest" in interpretability. Both our constructions are post-hoc. Our absolute accuracy numbers are therefore best read as an **upper bound** on detection power against naturally arising dispositions.
3. They recommend matching **quirk expression rate (QER)** across compared variants as a reporting standard. This is the same requirement protocol v3 §5 reached independently as "behavior matching." Adopt their term so the requirement is legible as existing practice rather than a local invention.

Their techniques are white-box (patching, probing, crosscoders) and ours is black-box behavioral and verbal, so the transfer is not automatic. But the "artificially easy proxy" warning does not depend on the technique class, and the burden is on us to argue otherwise.

**"Sleeper Agents" (arXiv 2401.05566).** Canonical organism precedent; the standing reference for behavior that persists through safety training.

## 4. Multi-agent collusion — the neighbourhood we are adjacent to but not in

**Colosseum (arXiv 2602.15198)**; **ColludeBench** (steganographic covert collusion, market/auction/governance); **MultiAgentFraudBench** (collusive fraud, 28 subcategories, 16 models); **MultiAgentBench**; "Voluntary Collusion with Secret Tools in Competing LLM Agents" (arXiv 2605.27593); "Lying with Truths: Open-Channel Multi-Agent Collusion" (arXiv 2601.01685).

This area is crowded and mostly *detection*-shaped: can a monitor catch collusion. Phase 3 is not in it — we do not run multiple agents, and we are not building a detector. The relevance is defensive: if we had pursued the peer-influence factorial as the lead study, this is the literature that would have contested its novelty. Recorded to justify the choice not made.

## 5. Chain-of-thought faithfulness — the assumption our protocol rests on

**"LLM Reasoning Is Latent, Not the Chain of Thought" (arXiv 2604.15726)** and **"Beyond the Commitment Boundary: Probing Epiphenomenal Chain-of-Thought" (arXiv 2606.13603)** are the strongest current statements that surface reasoning may not carry the causal process. The source paper's own §11.1 concedes the point and argues the CoT remains useful as a hypothesis *source* even when unfaithful. Our L3-versus-L2 contrast (reasoning present versus stripped) measures how much the reasoning channel is actually worth for attribution, which is a small empirical contribution to this debate and should be framed as one.

**"Measuring Faithfulness Depends on How You Measure: Classifier Sensitivity in LLM CoT Evaluation" (arXiv 2603.20172).** Faithfulness estimates move with the classifier used to measure them. Direct support for the judge-reliability and judge-leakage requirements in protocol v3 §7.4, and a reason to report hand-label agreement rather than assert it.

**FaithCoT-Bench; "Measuring CoT Faithfulness by Unlearning Reasoning Steps" (arXiv 2502.14829); FACT-E (arXiv 2604.10693).** Instance-level faithfulness measurement; relevant if we report per-trace rather than per-corpus faithfulness claims. We currently do not.

## 6. Assessment

The core question — attribution accuracy for competing *motivational* hypotheses as a function of evidence regime, with organism ground truth — was not found in the sweep. The method shape is taken (DEMM-Bench, medical evidence auditing), the organism substrate is taken (Sleeper Agents, Model Organism Lottery), and the multi-agent framing is crowded. The specific combination appears open.

That is a weaker novelty claim than "nobody has done this," and it should be written as the weaker claim. The contribution is better defended as *applying an existing sufficiency-measurement shape to motivational attribution, for a protocol whose authors state it lacks positive controls* than as a new method.

Two design changes follow, recorded in the v3.1 amendment: adopt overclaim rate as a co-primary metric, and treat construction method as a reported factor with an acknowledged unbounded spread rather than a robustness footnote.

## 7. Not yet done

Non-arXiv venues, 2026 workshop proceedings, and the alignment-forum/LessWrong grey literature are unswept. The grey literature matters disproportionately here because incident-forensics practice is being written there first. Sweep before submission, not before the pilot.
