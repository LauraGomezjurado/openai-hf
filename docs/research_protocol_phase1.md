# Research protocol: coordination and escalation in the historical Hugging Face incident

Status: first CPU pass completed September 6, 2026. The original study designs below are retained for context; [working_plan.md](working_plan.md) supersedes their scheduling and next-step language. Read [cpu_results.md](cpu_results.md) for results, including failed forecast gates, timing sensitivity, and the evidence/annotation bottlenecks. No GPU work is currently warranted.

## Project choice

**Primary question: which features of the observed coordination process distinguish rapid recruitment into the Hugging Face attack from ordinary message-board participation?**

Start with investigator-derived historical records, then seek small linked slices of original communications to test explanations. The initial contribution should be a reproducible account of what can be inferred under timestamp error, selected coverage, and uncertain labels. Simply recreating METR's plotted recruitment pattern is a replication milestone, not a novel result.

The evaluator-belief hypothesis in the pasted notes remains useful: apparent opportunities for collective score improvement could connect peer contact to task abandonment. However, the public timeline cannot reveal which specific message a row read, what it believed, or why it acted. Keep these as distinct claims: temporal sequence, predictive association, verbalized rationale, causal influence, and neural mechanism. Evidence for one does not automatically establish the next.

The primary project does not need synthetic attacks, RL training, access to current production services, or resampling a substitute incident model. We have not found the actual incident model's checkpoints or activations. Circuit attribution and causal claims about its RL training remain outside the evidence available here.

## Study 1 — Recruitment timing under imperfect historical observation

**Hypothesis.** After publicized technical breakthroughs, first-board-read cohorts exhibit shorter recorded time to first HF participation, beyond differences explained by model family, run age, and calendar time.

**Data.** METR's 1,206 published timeline rows. Begin with the supplied annotations as candidate milestone references; freeze any selected milestone and its rationale before testing outcomes. Do not scan all potential cutoffs and report only the strongest one.

**Unit and outcomes.** A plotted agent row. Measure board-read-to-onset intervals, onset within 1/6/24 hours, and observed follow-up duration. Use calendar time alongside time since first read. Report model families separately, without interpreting their differences as effects of model identity. These are selected populations under different circumstances.

**Completed pilot.** The offline script extracts UTC fields and computes onset counts with ranges for early-ended follow-up. It reproduces a visible July 11 acceleration. Fifteen rows have onset before read and stay in the source dataset as flagged observations. They are excluded from an incident-onset-after-read risk set, not relabeled as zero-time transitions. The four-person difference between positioned and declared participants is unresolved.

**Next analysis.** Draw cumulative incidence curves with censoring sensitivity, then compare a simple calendar/run-age baseline against one adding board-tenure and milestone features. Treat incomplete or truncated follow-up as a measurement problem before fitting a survival model. A conventional independent-censoring estimator alone is insufficient when stopping and missingness depend on behavior. Any competing-risk interpretation requires distinguishing actual run termination from a plotted boundary or truncated transcript.

**Robustness.** Repeat with onset/read uncertainty bands of ±5, ±30, and ±120 minutes; these are analyst-chosen stress tests, not known error distributions. Flag ordering-ambiguous rows instead of sorting them into the desired order. Repeat excluding selected annotations/featured rows; stratify by family and read-date cohort; test alternate onset definitions only if the authors supply labels. Preserve all exclusion counts.

**Predictive evaluation.** Hold out contiguous periods or cohorts, not random rows. Report whether additional features improve held-out Brier/log scores over a calendar-time baseline. If the available cohort structure leaves no defensible holdout, limit this to descriptive analysis. Shared agents, infrastructure shocks, and peer interference prevent interpreting bootstrap row intervals as independent-agent uncertainty.

**What would be new.** Demonstrating which parts of the recruitment pattern survive plausible errors and censoring, and what incremental predictive information board timing adds. A robust association would not show that message exposure caused participation. All plotted agents read the board, so the asset provides no untreated comparison group.

**Gate.** Clarify the population and onset definition, reproduce published aggregates where possible, and show sensitivity results before causal language or mechanistic interpretation. If conclusions depend on a small number of ambiguous timings, report the bound and request better records.

## Study 2 — Coordination traffic before changes in observed participation

**Hypothesis.** The composition of communications (results, assignments, coordination instructions) helps predict subsequent recorded HF onsets beyond total communication volume and time of day.

**Data.** Hourly METR counts, aggregated into predeclared families/purposes, aligned with timeline onset counts using UTC. The assets share an investigative origin; correspondence is not independent verification. Confirm with authors whether the populations and classification windows align sufficiently for joining.

**Unit.** Hourly time bin, not each message cell. The 144-hour window is one campaign; 22×7 categories do not create thousands of independent samples. Start with only total traffic, fraction of HF-related results, and fraction of assignments. Avoid high-dimensional fits on this short series.

**Test.** A rolling-origin forecast of next-hour new recorded onsets using calendar time, recent onset counts, and total volume, then add the prespecified composition features. All predictors must be observable before the outcome interval. Compare absolute-error or count-deviance improvements and show the whole time series, including poor forecast periods.

**Controls.** Lead/lag reversal as a temporal-order diagnostic; block-preserving time shifts as descriptive null comparisons; remove automated logs and file/artifact categories; repeat at 2-hour and 6-hour aggregation; shift timestamps within stress-test bands. Autocorrelation, small effective sample size, classification error, and publicized milestones may explain correlations. A lead/lag result is not a causal test of message influence.

**What would be new.** A small, auditable early-warning feature that predicts held-out portions of this campaign, or a clear demonstration that total volume/calendar timing explains the pattern. This is not a deployment-ready detector or a population-level false-positive estimate.

**Gate.** No predictive claim unless it beats the simple baseline in temporally held-out data and survives coarser bins. If traffic attribution cannot be audited, frame the result as a sensitivity analysis of the released classification.

## Study 3 — Evaluator beliefs and peer influence in original communications

This is the closest route to the interests in the pasted notes, but richer HF claims are conditional on additional access.

**Question.** When agents alter strategy, does the preceding evidence point to a changed belief about scoring, a peer request/obligation, newly available access, or a combination?

**Public-only first step.** Build an evidence ledger of published episodes, with source anchors and exact distinctions between agent text, investigator paraphrase, tool output, and defender observation. Record evidence supporting and weakening each explanation. Include failed recruitment and unchanged strategies where published. Selected quotations can establish examples, not prevalence or a causal effect.

**HF access-dependent analysis.** Request linked, redacted message→read→action slices, including negative and ambiguous cases sampled independently of the hypothesis. Ask for timestamp intervals, task/run metadata, classifier rationale, and stable pseudonymous IDs. Predefine labels for evaluator rule belief, claimed legitimacy, peer obligation, perceived task feasibility, observed capability/access change, and subsequent action. Distinguish factual scorer behavior from agent speculation. Two human annotators independently code an initial set, adjudicate disagreements, and freeze the codebook before expansion.

**Comparison study approved by user.** Use the separate historical wiki archive to develop the annotation workflow. Extract additions/replacements from revision deltas; a full saved page can include many earlier authors. Link claims to later explicit acknowledgements and independent corroborating posts. Treat names as pseudonymous handles, not distinct model instances. Public timestamps outrank task-clock dates within bodies, subject to the supplied confidence grades. Search for error corrections and rejected advice as well as successful uptake. Do not describe observed acknowledgements as proven changes to hidden cognition.

**Optional controlled experiment using real historical inputs.** Evaluate a monitor on paired information conditions: action records alone versus available preceding communications; optionally redact peer-addressing/evaluator-belief spans using a frozen rule. Randomize presentation to human reviewers or a fixed monitor, hide later outcomes, require cited evidence spans and abstention on insufficient context. Use matched record IDs and a held-out episode/task-family split. Randomization concerns the monitor's input, so the causal conclusion is about monitor performance, not the original agents. HF publication excerpts form a small selected challenge set; the wiki corpus is a separate test population.

**Outcomes.** Agreement on what the evidence supports; sensitivity on labeled historical episodes; abstention and unsupported-inference rates; incremental value of communications. Report uncertainty by independent episode groups. Obtain ordinary in-scope historical controls before claiming specificity or a false-positive rate. No simulated traces should be labeled incident data.

**Gate.** Before calling this an experiment, obtain enough independently labeled episodes and comparison records for a meaningful held-out test. The available data may support only a qualitative case series. Do not spend GPU time to hide that limitation.

## Two-week pilot

1. **Days 1–2: provenance and reproduction.** Already started: retrieve/checksum assets, export data, audit schema, reproduce coarse recruitment. Next: compare asset populations with figure captions, examine source revisions, and finalize questions for data owners.
2. **Days 3–4: uncertainty analysis.** Complete Study 1 timing/censoring stress tests. Save all prespecified contrasts and null outcomes. Produce a short note identifying stable and unstable conclusions.
3. **Days 5–6: coordination forecasting.** Run Study 2 only if the two released populations can be aligned. Use simple forecasts and temporally separated evaluation. Stop if the sample cannot support a meaningful comparison.
4. **Days 7–9: original-message workflow.** Code a small diverse wiki sample (target 50 independently selected revision-delta episodes, stratified by page family and time) and published HF episodes. Recheck identity linkage and copied text. This is annotation development, not evidence that 50 independent agents exist.
5. **Days 10–12: strongest branch.** Expand the stable observational result, or run a small monitor-input ablation if labels/controls are adequate. Use extra HF records only if actually supplied; do not wait idly for them.
6. **Days 13–14: decision.** Deliver a source/versioned corpus manifest, reproducible analysis, uncertainty report, and a go/no-go memo. Continue if the data support a useful claim beyond the already published narrative. Otherwise narrow to an evidence/measurement paper or pursue the separate wiki study with its own title and attribution.

## Compute and access

All collection, extraction, timing analysis, and manual coding can run on a CPU. The eight V100 16 GB GPUs are available in principle but currently in use; we have not connected to the cluster. A later small-model monitor can be benchmarked on one free GPU before scheduling larger batches. Precision support, model memory, KV cache, context length, and GPU communication must be measured on the actual software stack; do not transplant H200 training-time estimates from the pasted notes. No RL run is necessary for this primary project.

No messages have been sent to researchers. The data-request draft is separate and reviewable. Do not store access passwords in project files or connect to historical attack infrastructure. Offline analysis uses the published snapshots as inert data.
