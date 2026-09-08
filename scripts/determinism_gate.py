"""Backend repeatability gate for llama-server based experiments.

Every experiment in this repository decodes at temperature 0 and treats an
exact-input replay as a repeatability check. That check is only meaningful if
the backend is itself repeatable. This gate measures it directly instead of
assuming it.

For each prompt it requests the same completion under three regimes:

* ``uncached``: ``cache_prompt=false``; the whole prompt is evaluated fresh.
  Repeated three times, in shuffled order, interleaved with the other prompts.
* ``cached_full``: ``cache_prompt=true`` immediately after an identical request,
  so nearly all tokens come from the resident KV cache.
* ``cached_split:<k>``: ``cache_prompt=true`` immediately after a primer request
  whose prompt is the same text minus its last ``k`` characters, so roughly the
  last ``k`` characters are evaluated as a fresh suffix batch. ``k`` values are
  chosen to bracket the fresh-token counts seen in the recorded mismatches.

Each response is compared with the first uncached response: generated tokens,
and the top-``n_probs`` log-probabilities per generated token (pre-sampling
softmax of the logits, as llama-server reports them). The gate also records the
smallest top-1/top-2 margin among grammar-legal candidates for the decision
token, which is the quantity that decides whether a last-bit numerical change
can flip a greedy choice.

Verdict: ``pass`` when every uncached repetition is token- and logprob-identical
to the reference. Cached regimes are reported but never gate, because the
protocols now forbid ``cache_prompt=true``; their divergence is the documented
mechanism, not a failure of the fixed configuration.

Usage (server already running on --url):

    python3 scripts/determinism_gate.py --rollouts results/peer_claims_v2/qwen3/rollouts.jsonl --n 8 --out results/determinism/gate_qwen3.json
    python3 scripts/determinism_gate.py --prompt-file prompts.json --out results/determinism/gate_tiny.json

``--rollouts`` extracts rendered prompts and JSON schemas from saved study
records, so the gate exercises the exact request shapes the studies used.
"""
import argparse
import hashlib
import json
import pathlib
import random
import time
import urllib.request

R = pathlib.Path(__file__).resolve().parents[1]


def post(url, endpoint, payload, timeout=600):
    req = urllib.request.Request(url.rstrip('/') + '/' + endpoint, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def prompts_from_rollouts(path, n, seed):
    """Deterministic sample of (prompt, schema, legal_values) from a saved rollouts.jsonl."""
    out = []
    for line in pathlib.Path(path).read_text().splitlines():
        r = json.loads(line)
        steps = r.get('steps') or [r]
        for s in steps:
            settings = s.get('settings') or {}
            schema = settings.get('json_schema')
            prompt = s.get('rendered_prompt')
            if prompt and schema:
                out.append({'prompt': prompt, 'json_schema': schema, 'n_predict': settings.get('n_predict', 192)})
    rng = random.Random(seed)
    rng.shuffle(out)
    return out[:n]


def legal_values(schema):
    """Enumerated string values anywhere in the schema; used to approximate grammar-legal candidates."""
    found = []

    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get('enum'), list):
                found.extend(str(v) for v in x['enum'])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(schema)
    return found


def decision_margin(probs, legal):
    """Smallest margin (nats) between the best and second-best grammar-legal candidate at any generated position.

    A candidate token is treated as legal at a position when its text (after stripping a leading quote or
    space) is a prefix of some enumerated value, or the position is not inside an enumerated value (then all
    candidates count). This is an approximation of the grammar; it is reported, not used for gating.
    """
    best = None
    for p in probs or []:
        top = p.get('top_logprobs') or p.get('top_probs') or []
        if len(top) < 2:
            continue
        cands = []
        for t in top:
            text = str(t.get('token', '')).lstrip(' "')
            ok = (not legal) or any(v.startswith(text) for v in legal) or text == ''
            if ok:
                cands.append(float(t.get('logprob', t.get('prob', 0.0))))
        if len(cands) >= 2:
            cands.sort(reverse=True)
            m = cands[0] - cands[1]
            best = m if best is None else min(best, m)
    return best


def completion(url, prompt, schema, n_predict, cache_prompt, n_probs, seed):
    payload = {'prompt': prompt, 'n_predict': n_predict, 'temperature': 0, 'seed': seed, 'cache_prompt': cache_prompt, 'json_schema': schema, 'n_probs': n_probs}
    t0 = time.time()
    resp = post(url, 'completion', payload)
    probs = resp.get('completion_probabilities') or []
    return {'content': resp.get('content'), 'tokens': resp.get('tokens'), 'timings': {k: resp.get('timings', {}).get(k) for k in ['prompt_n', 'cache_n', 'predicted_n']},
            'tokens_cached': resp.get('tokens_cached'), 'top_logprobs': [[(t.get('token'), float(t.get('logprob', t.get('prob', 0.0)))) for t in (p.get('top_logprobs') or p.get('top_probs') or [])] for p in probs],
            'decision_margin': decision_margin(probs, legal_values(schema)), 'wall_s': round(time.time() - t0, 3)}


def compare(ref, other):
    """Token identity plus log-probability agreement over candidates present in both top-k lists."""
    same_tokens = ref['tokens'] == other['tokens'] and ref['content'] == other['content']
    max_diff = 0.0
    membership_changed = False
    n = min(len(ref['top_logprobs']), len(other['top_logprobs']))
    for i in range(n):
        a = dict(ref['top_logprobs'][i])
        b = dict(other['top_logprobs'][i])
        if set(a) != set(b):
            membership_changed = True
        for k in set(a) & set(b):
            max_diff = max(max_diff, abs(a[k] - b[k]))
    identical = (max_diff == 0.0 and not membership_changed) if n else None
    return {'tokens_identical': same_tokens, 'max_abs_logprob_diff_common': max_diff if n else None, 'topk_membership_changed': membership_changed if n else None, 'logprobs_identical': identical}


def run(url, prompts, splits, reps, seed, n_probs):
    rng = random.Random(seed)
    results = []
    for i, p in enumerate(prompts):
        results.append({'index': i, 'prompt_sha256': hashlib.sha256(p['prompt'].encode()).hexdigest(), 'prompt_chars': len(p['prompt']), 'uncached': [], 'cached': []})
    # Uncached repetitions in shuffled, interleaved order.
    for rep in range(reps):
        order = list(range(len(prompts)))
        rng.shuffle(order)
        for i in order:
            p = prompts[i]
            results[i]['uncached'].append(completion(url, p['prompt'], p['json_schema'], p['n_predict'], False, n_probs, seed))
    # Cached regimes: primer then the real request.
    for i, p in enumerate(prompts):
        for k in [0] + list(splits):
            primer = p['prompt'] if k == 0 else p['prompt'][:-k]
            completion(url, primer, p['json_schema'], 1, True, 0, seed)
            r = completion(url, p['prompt'], p['json_schema'], p['n_predict'], True, n_probs, seed)
            r['regime'] = 'cached_full' if k == 0 else f'cached_split:{k}'
            results[i]['cached'].append(r)
    # Comparison against the first uncached response.
    for res in results:
        ref = res['uncached'][0]
        res['reference_content'] = ref['content']
        res['reference_decision_margin'] = ref['decision_margin']
        res['uncached_comparisons'] = [compare(ref, o) for o in res['uncached'][1:]]
        res['cached_comparisons'] = [{'regime': o['regime'], 'fresh_prompt_n': o['timings']['prompt_n'], **compare(ref, o)} for o in res['cached']]
    verdict = all(c['tokens_identical'] and c['logprobs_identical'] for res in results for c in res['uncached_comparisons'])
    cached_token_flips = sum(not c['tokens_identical'] for res in results for c in res['cached_comparisons'])
    cached_logprob_changes = sum(not c['logprobs_identical'] for res in results for c in res['cached_comparisons'] if c['logprobs_identical'] is not None)
    # Saved form: per-token arrays are replaced by a digest so identity stays verifiable without megabytes of numbers.
    for res in results:
        for r in res['uncached'] + res['cached']:
            r['top_logprobs_sha256'] = hashlib.sha256(json.dumps(r['top_logprobs']).encode()).hexdigest()
            r['generated_tokens'] = len(r['tokens'] or [])
            del r['top_logprobs'], r['tokens']
    return {'verdict': 'pass' if verdict else 'fail', 'prompts': len(prompts), 'repetitions': reps, 'splits': list(splits), 'n_probs': n_probs,
            'uncached_token_mismatches': sum(not c['tokens_identical'] for res in results for c in res['uncached_comparisons']),
            'uncached_logprob_mismatches': sum(not c['logprobs_identical'] for res in results for c in res['uncached_comparisons']),
            'cached_token_flips': cached_token_flips, 'cached_logprob_changes': cached_logprob_changes,
            'cached_comparisons_total': sum(len(res['cached_comparisons']) for res in results),
            'min_reference_decision_margin': min((res['reference_decision_margin'] for res in results if res['reference_decision_margin'] is not None), default=None),
            'results': results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', default='http://127.0.0.1:18973')
    ap.add_argument('--rollouts')
    ap.add_argument('--prompt-file', help='JSON list of {prompt, json_schema, n_predict}')
    ap.add_argument('--messages-file', help='JSON list of {messages, json_schema, n_predict}; rendered through the server chat template')
    ap.add_argument('--n', type=int, default=8)
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--splits', default='37,118,300', help='character cut lengths for cached_split regimes')
    ap.add_argument('--seed', type=int, default=9082026)
    ap.add_argument('--n-probs', type=int, default=10)
    ap.add_argument('--out', required=True)
    ap.add_argument('--model-note', default='')
    a = ap.parse_args()
    if a.rollouts:
        prompts = prompts_from_rollouts(a.rollouts, a.n, a.seed)
    elif a.messages_file:
        prompts = [{'prompt': post(a.url, 'apply-template', {'messages': m['messages']})['prompt'], 'json_schema': m['json_schema'], 'n_predict': m.get('n_predict', 192)}
                   for m in json.loads(pathlib.Path(a.messages_file).read_text())[:a.n]]
    else:
        prompts = json.loads(pathlib.Path(a.prompt_file).read_text())[:a.n]
    assert prompts, 'no prompts'
    try:
        with urllib.request.urlopen(a.url.rstrip('/') + '/props', timeout=30) as r:
            props = json.load(r)
    except Exception as e:  # noqa: BLE001 - provenance only
        props = {'error': str(e)}
    summary = run(a.url, prompts, [int(x) for x in a.splits.split(',') if x], a.reps, a.seed, a.n_probs)
    summary['server_props'] = {k: props.get(k) for k in ['model_path', 'total_slots', 'build_info', 'default_generation_settings', 'chat_template']} if isinstance(props, dict) else props
    summary['model_note'] = a.model_note
    summary['utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    summary['source'] = a.rollouts or a.messages_file or a.prompt_file
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=1) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ['results', 'server_props']}, indent=2))


if __name__ == '__main__':
    main()
