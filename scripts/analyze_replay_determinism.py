"""Re-analysis of every exact-input replay pair in the repository.

Question: do the recorded replay mismatches coincide with different KV-cache
prefix splits? Every study except the escalation pilot requested
``cache_prompt: true`` from llama-server. When a request shares a prefix with the
resident KV cache, only the suffix is evaluated as a new batch; the number of
freshly evaluated tokens (``timings.prompt_n``) therefore depends on what the
server processed immediately before. Different batch compositions take different
matmul kernel paths and accumulation orders, so logits can differ in the last
bits. At temperature 0 a near-tie between two candidate tokens then flips.

This script does not rerun any model. It reads the saved responses, pairs each
replay with its source record, and tabulates decision agreement against whether
the fresh-token count differed. Rendered prompts are also compared byte-for-byte
so that a prompt-construction bug can be excluded separately.
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'results/determinism'


def local(path):
    """Frozen files store the original machine's absolute paths; resolve them inside this checkout."""
    path = str(path)
    marker = '/openai-hf/'
    return R / path.split(marker, 1)[1] if marker in path and not path.startswith(str(R)) else pathlib.Path(path)


def rows(path):
    return [json.loads(l) for l in local(path).read_text().splitlines()]


def timing(response):
    t = response.get('timings', {})
    return {'prompt_n': t.get('prompt_n'), 'cache_n': t.get('cache_n'), 'tokens_cached': response.get('tokens_cached')}


def pair(study, model, case_id, source_steps, replay_steps, source_decision, replay_decision, settings):
    """One replay pair. Steps are lists of (rendered_prompt, response, action)."""
    n = min(len(source_steps), len(replay_steps))
    steps = []
    for i in range(n):
        sp, sr, sa = source_steps[i]
        rp, rr, ra = replay_steps[i]
        steps.append({'step': i + 1, 'prompt_identical': (sp == rp) if sp is not None and rp is not None else None, 'source': timing(sr), 'replay': timing(rr),
                      'content_identical': sr.get('content') == rr.get('content'), 'source_action': sa, 'replay_action': ra})
    first = steps[0]
    return {'study': study, 'model': model, 'case_id': case_id, 'cache_prompt_requested': settings.get('cache_prompt'),
            'source_decision': source_decision, 'replay_decision': replay_decision, 'decision_match': source_decision == replay_decision,
            'first_prompt_identical': first['prompt_identical'], 'first_fresh_tokens_differ': first['source']['prompt_n'] != first['replay']['prompt_n'],
            'first_source_prompt_n': first['source']['prompt_n'], 'first_replay_prompt_n': first['replay']['prompt_n'],
            'step_count_match': len(source_steps) == len(replay_steps), 'steps': steps}


def peer_claims_v2():
    out = []
    for model in ['qwen3', 'qwen']:
        p = R / f'results/peer_claims_v2/{model}/rollouts.jsonl'
        if not p.exists():
            continue
        rs = rows(p)
        main = {r['case']['id']: r for r in rs if r['phase'] == 'main'}
        for r in rs:
            if r['phase'] != 'replay' or r['case']['id'] not in main:
                continue
            s = main[r['case']['id']]
            st = lambda x: [(k['rendered_prompt'], k['response'], k.get('action')) for k in x['steps']]
            out.append(pair('peer_claims_v2', model, r['case']['id'], st(s), st(r), s['decision'], r['decision'], s['steps'][0]['settings']))
    return out


def peer_claim_order():
    out = []
    p = R / 'results/peer_claim_order/qwen3/rollouts.jsonl'
    if not p.exists():
        return out
    src = {r['case']['id']: r for r in rows(R / 'results/peer_claims_v2/qwen3/rollouts.jsonl') if r['phase'] == 'main'}
    for r in rows(p):
        if r['arm'] != 'replay':
            continue
        s = src[r['case']['id']]
        # The diagnostic branched from the final-decision prompt only, so compare the last source step with the first replay step.
        st = [(s['steps'][-1]['rendered_prompt'], s['steps'][-1]['response'], s['steps'][-1].get('action'))]
        rt = [(k['rendered_prompt'], k['response'], k.get('action')) for k in r['steps']]
        out.append(pair('peer_claim_order', 'qwen3', r['case']['id'], st, rt, s['decision'], r['decision'], s['steps'][-1]['settings']))
    return out


def opportunity_v2():
    out = []
    for model in ['qwen3', 'qwen', 'smol']:
        rp = R / f'results/opportunity_cost/v2/{model}/replays.jsonl'
        if not rp.exists():
            continue
        src = {r['case']['id']: r for r in rows(R / f'results/opportunity_cost/v2/{model}/rollouts.jsonl') if not r['probe'] and r['phase'] == 'main'}
        for r in rows(rp):
            s = src[r['case']['id']]
            dec = lambda x: (x['decoded'] or {}).get('allocation')
            out.append(pair('opportunity_cost_v2', model, r['case']['id'], [(s['rendered_prompt'], s['response'], dec(s))], [(r['rendered_prompt'], r['response'], dec(r))], dec(s), dec(r), s['settings']))
    return out


def workflow_completion():
    out = []
    contexts = {c['id']: c for c in json.loads((R / 'experiments/workflow_completion/contexts.json').read_text())}
    for model in ['qwen3', 'qwen']:
        p = R / f'results/workflow_completion/{model}/rollouts.jsonl'
        if not p.exists():
            continue
        for r in rows(p):
            if r['arm'] != 'replay':
                continue
            c = contexts[r['context_id']]
            src = rows(c['source'])[c['source_line'] - 1]
            k = c['used_turns']
            ss = src['steps'][k]
            st = [(ss['rendered_prompt'], ss['response'], ss.get('action'))]
            rs = r['steps'][0]
            rt = [(rs['rendered_prompt'], rs['response'], rs.get('action'))]
            settings = {'cache_prompt': ss['response'].get('generation_settings', {}).get('cache_prompt', True)}
            out.append(pair('workflow_completion', model, r['context_id'], st, rt, json.dumps(ss.get('action'), sort_keys=True), json.dumps(rs.get('action'), sort_keys=True), settings))
    return out


def escalation_continuations():
    out = []
    p = R / 'results/escalation/continuations/rollouts.jsonl'
    if not p.exists():
        return out
    src = {r['case']['id']: r for r in rows(R / 'results/escalation/pilot_v2/rollouts.jsonl')}
    for r in rows(p):
        c = r['case']
        if c['arm'] != 'replay' or c['source_case']['id'] not in src:
            continue
        s = src[c['source_case']['id']]
        k = c['prefix_length']
        if k >= len(s['steps']) or not r['steps']:
            continue
        ss, rs = s['steps'][k], r['steps'][0]
        st = [(None, ss['response'], json.dumps(ss.get('action'), sort_keys=True))]
        rt = [(None, rs['response'], json.dumps(rs.get('action'), sort_keys=True))]
        out.append(pair('escalation_continuations', 'qwen', c['source_case']['id'], st, rt, st[0][2], rt[0][2], {'cache_prompt': False}))
    return out


def summarize(pairs):
    def block(ps):
        n = len(ps)
        return {'pairs': n, 'decision_mismatches': sum(not p['decision_match'] for p in ps), 'prompt_identical': sum(bool(p['first_prompt_identical']) for p in ps if p['first_prompt_identical'] is not None)}
    by_study = {}
    for p in pairs:
        key = f"{p['study']}/{p['model']}"
        by_study.setdefault(key, []).append(p)
    diff = [p for p in pairs if p['first_fresh_tokens_differ']]
    same = [p for p in pairs if not p['first_fresh_tokens_differ']]
    cached = [p for p in pairs if p['cache_prompt_requested']]
    uncached = [p for p in pairs if not p['cache_prompt_requested']]
    return {
        'total_pairs': len(pairs),
        'by_study': {k: block(v) for k, v in by_study.items()},
        'cache_prompt_true': block(cached), 'cache_prompt_false': block(uncached),
        'fresh_token_count_differs': block(diff), 'fresh_token_count_equal': block(same),
        'mismatches': [{k: p[k] for k in ['study', 'model', 'case_id', 'source_decision', 'replay_decision', 'first_source_prompt_n', 'first_replay_prompt_n', 'first_prompt_identical']} for p in pairs if not p['decision_match']],
        'reading': 'Descriptive association within saved records. A prompt_n difference is a marker that the two requests were evaluated with different batch splits; it is not a measured logit difference. Mismatches with equal prompt_n would indicate a further source; equal outcomes with different prompt_n are expected whenever the decision margin is not near a tie.',
    }


def main():
    pairs = peer_claims_v2() + peer_claim_order() + opportunity_v2() + workflow_completion() + escalation_continuations()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'replay_pairs.json').write_text(json.dumps(pairs, indent=1) + '\n')
    summary = summarize(pairs)
    (OUT / 'replay_cache_audit.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'reading'}, indent=2))
    return summary


if __name__ == '__main__':
    main()
