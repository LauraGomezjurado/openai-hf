"""Two-phase generation that records model-generated reasoning before a constrained decision.

Model Forensics (Singh et al., arXiv 2606.26071) uses reasoning traces to *generate*
explanations and interventions to *test* them. Every completed study here decoded a
grammar-constrained JSON object directly, with Qwen3 thinking disabled, so the record
contains no reasoning at all and the first half of that loop could not run.

This module adds the missing channel without changing what is scored:

1. ``reason``: free generation from the rendered prompt, no grammar, stopped at the
   closing reasoning tag or a token budget. For checkpoints with a native thinking
   template (Qwen3 with ``enable_thinking=true``) the assistant turn is opened with
   ``<think>``; for other instruction-tuned checkpoints a scratchpad instruction is
   appended and the turn is opened with ``<scratchpad>``.
2. ``decide``: the same prompt plus the captured reasoning and closing tag, then the
   grammar-constrained decision with ``n_probs`` so the decision-token margin is saved.

Both phases use ``cache_prompt=false``. The reasoning text is stored with a SHA-256 and
labeled ``model_generated``; it is a hypothesis source, not a measurement of internal
state, and its faithfulness is not assumed anywhere.
"""
import hashlib
import json
import time

MODES = {
    'native_think': {'open': '<think>\n', 'close': '</think>', 'instruction': ''},
    'scratchpad': {'open': '<scratchpad>\n', 'close': '</scratchpad>',
                   'instruction': ' Before the JSON, think through the situation inside <scratchpad> and </scratchpad> tags. After the closing tag, return only the requested JSON.'},
    'none': {'open': '', 'close': '', 'instruction': ''},
}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def add_instruction(messages, mode):
    """Return a copy of the messages with the mode's instruction appended to the system message."""
    ms = [dict(m) for m in messages]
    extra = MODES[mode]['instruction']
    if extra:
        if ms and ms[0]['role'] == 'system':
            ms[0]['content'] += extra
        else:
            ms.insert(0, {'role': 'system', 'content': extra.strip()})
    return ms


def generate(post, rendered_prompt, schema, mode, seed, reasoning_budget=768, decision_budget=192, n_probs=10):
    """post(endpoint, payload) -> llama-server JSON. Returns a record with both phases."""
    spec = MODES[mode]
    record = {'mode': mode, 'seed': seed, 'reasoning': None, 'reasoning_sha256': None, 'reasoning_truncated': None, 'reasoning_response': None}
    prompt = rendered_prompt
    if mode != 'none':
        p1 = {'prompt': rendered_prompt + spec['open'], 'n_predict': reasoning_budget, 'temperature': 0, 'seed': seed, 'cache_prompt': False, 'stop': [spec['close']], 'n_probs': 0}
        r1 = post('completion', p1)
        text = r1.get('content') or ''
        record.update({'reasoning': text, 'reasoning_sha256': sha(text), 'reasoning_truncated': r1.get('stop_type') == 'limit', 'reasoning_stop_type': r1.get('stop_type'), 'reasoning_label': 'model_generated',
                       'reasoning_response': {k: r1.get(k) for k in ['tokens_predicted', 'tokens_evaluated', 'stop_type', 'stopping_word', 'truncated', 'timings']}})
        prompt = rendered_prompt + spec['open'] + text + '\n' + spec['close'] + '\n\n'
    p2 = {'prompt': prompt, 'n_predict': decision_budget, 'temperature': 0, 'seed': seed, 'cache_prompt': False, 'json_schema': schema, 'n_probs': n_probs}
    r2 = post('completion', p2)
    try:
        decoded = json.loads((r2.get('content') or '').strip())
    except ValueError:
        decoded = None
    probs = r2.get('completion_probabilities') or []
    record.update({'decision_prompt_sha256': sha(prompt), 'decision_settings': {k: v for k, v in p2.items() if k != 'prompt'}, 'decision_response': r2, 'decoded': decoded,
                   'decision_top_logprobs': [[(t.get('token'), float(t.get('logprob', 0.0))) for t in (p.get('top_logprobs') or [])] for p in probs],
                   'ended_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    return record


def margin_for_value(top_logprobs, value, legal_values=()):
    """Log-probability margin at the decision position between the chosen value and its best legal rival.

    Scans generated positions for the first one where some top-k candidate begins ``value`` (after stripping
    quotes and whitespace). The margin is that candidate's logprob minus the best logprob among candidates
    that begin a *different* legal value. Grammar-forced tokens need not be the pre-grammar argmax, so the
    chosen candidate is located by text rather than by rank. Returns None when no such position or rival
    exists within the top-k; with no ``legal_values`` any other candidate counts as a rival.
    """
    def strip(t):
        return str(t).strip(' "\t\n')
    target = strip(value)
    others = [strip(v) for v in legal_values if strip(v) != target]
    for entries in top_logprobs:
        chosen = [lp for tok, lp in entries if strip(tok) and target.startswith(strip(tok))]
        if not chosen:
            continue
        rivals = [lp for tok, lp in entries if strip(tok) and not target.startswith(strip(tok)) and (not others or any(o.startswith(strip(tok)) for o in others))]
        if not rivals:
            return None
        return max(chosen) - max(rivals)
    return None
