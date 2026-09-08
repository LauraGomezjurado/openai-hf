## Trace audit: a wording confound in the work card

The saved-work card says “Preserve that completed work.” The harness also exposes a tool named `preserve`, which only accepts a shared-artifact identifier. Qwen2.5's work-only branch made an invalid preservation call in all 16 contexts (eight unauthorized and eight authorized), adding 16 tool errors. In the combined-card branch there were three such errors in authorized contexts and none in unauthorized contexts. The selected benign-message example concerns a preservation error on an invoice ID, not a false accusation of credential misuse.

This materially limits an interpretation of the cards as merely displaying status. The wording can be construed as an additional action instruction. This is a researcher-designed ambiguity, not evidence of peer loyalty. Qwen3's unsaved-work card uses a different state-dependent sentence and has no “preserve” instruction; checkpoint contrasts must not ignore that initial-state difference.

A separately frozen post-result diagnostic changes only “Preserve” to “Retain” in all 16 Qwen2.5 work-only contexts, with four original-wording replay controls. It is not a replacement or correction to these primary observations, and does not independently test the combined-card arm. The diagnostic is complete: invalid preservation calls fell from 16/16 contexts to 0/16 with the synonym, while correct completion stayed 16/16. The four original-wording controls reproduced the error pattern and final states; one first action differed in its invalid argument. See the separately labeled diagnostic report.

[Diagnostic protocol](/Users/lauragomez/Desktop/openai-hf/experiments/workflow_completion/wording_control/protocol.md)

## Scientific interpretation of the primary panel

Completed September 8, 2026: 128 branches from 32 source contexts, using 172 generation calls. All 32 exact replays reproduced both first actions and final states. These are matched continuations, not 128 independent tasks.

The strongest selective result is Qwen3's repair contrast. Both unauthorized release contexts already had an incident-specific receipt but no saved submission. The work-status card changed the next action from finish to a correct submission, followed by finish; repeating the duty did not. This weakens explanations based on an inability to produce the correct selection or a hard shortage of remaining actions in those contexts. It does not distinguish forgetting from interpreting the task as sufficiently handled, context salience, or other instruction-response processes. Both cases belong to one domain: excluding release removes the entire joint-outcome gain.

Qwen2.5 already had correct saved work in every selected context, so it cannot test restoration of unfinished work. The duty card added two reports, while the work card added none; both cards added three. The extra gain of both over duty is one context, and its finite-panel interaction is +12.5 percentage points. That is not evidence of a general synergistic mechanism. The gain of both over replay remains positive after excluding any one domain (+16.7 to +50 percentage points), but the task structures remain related and the wording/tool confound is material.

The combined intervention reaches 5/8 joint outcomes for Qwen2.5 and 3/8 for Qwen3. It therefore does not solve the fixed panel. It also adds a benign message about a tool error on Qwen2.5. Joint completion should be evaluated alongside unnecessary actions, errors and message purpose, not merely final task validity.

These observations support decomposing obligation failures and using targeted controls to assess concrete interventions. They do not establish a model-level motivational double dissociation: the two checkpoints began in different work/report states, and the state-dependent work-card wording differed. The historical motive question remains open.

## Decision after the panel

The separately frozen single-word diagnostic is complete; stop this completion-card series. A broad safety recommendation is premature. If this workflow intervention is developed further, use neutral status wording, an independently scored report endpoint, native-interface checks and held-out task structures. A failure to report after our cards does not establish deliberate concealment.

The next major research direction should move closer to the original motive alternatives by testing genuine opportunity costs and task feasibility, rather than automatically adding more reminder variations. The [opportunity-cost study concept](/Users/lauragomez/Desktop/openai-hf/docs/opportunity_cost_study_concept.md) records the historical bridge and experimental requirements; that larger study is not yet implemented or executed.


[Completed single-word diagnostic](/Users/lauragomez/Desktop/openai-hf/docs/workflow_wording_results.md) · [Primary figure](/Users/lauragomez/Desktop/openai-hf/results/workflow_completion/completion_results.png)
