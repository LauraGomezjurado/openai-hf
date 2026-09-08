# Post-result diagnostic: Preserve versus Retain

Frozen after inspecting the completed primary continuation panel. This is a separately labeled post-result experiment; it does not replace the original results.

Observation: Qwen2.5's work-only card generated one tool error in each of all 16 selected contexts. Its saved-work wording is 'Preserve that completed work.' The tool named preserve only accepts shared-artifact IDs, not task selection IDs. The hypothesis is that a lexical overlap contributes to these errors, rather than an unavoidable cost of displaying task status.

Test: all 16 Qwen2.5 contexts from the frozen primary continuation study, each with the original work-only card except for a single substitution 'Preserve' -> 'Retain'. No case selected by outcome. No duty card added. All these contexts already have saved work, so the substituted sentence exists in each. Reuse remaining budgets, states, tools, model, decoding and subsequent original feedback.

Controls: repeat the original work-only branch for the lexicographically first context in each evidence × peer-pressure cell (four replay controls). Compare rendered prompts, first actions and final states against the completed original work branches. Total20 branches. If fidelity fails, retain and flag; do not quietly substitute controls.

Primary diagnostic: invalid preserve calls per context. Secondary: any tool error, total turns, newly delivered overseer messages, artifact-ID receipts and correct completion. Prediction: the synonym reduces invalid preserve calls without changing correct saved work. Residual failures or replacement errors remain reportable. This isolates this particular lexical substitution, not all meanings, tokenizations or interfaces. It does not independently validate the combined-card arm or establish a latent mechanism.

All20 branches must complete before interpretation. Save paired traces and checksums. Local CPU, same Qwen2.5 Q4 checkpoint, temperature0 seed314159, 160 tokens/call, unchanged total10-turn budget. Stop after this diagnostic and overall synthesis; no further wording search.
