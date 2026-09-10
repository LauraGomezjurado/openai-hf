"""How much of the recorded evidence was generated under a split KV-cache evaluation?

`scripts/analyze_replay_determinism.py` established the mechanism on the 76 exact-input
replay pairs: with `cache_prompt=true`, llama-server reuses the resident KV cache for a
common prefix and evaluates only the suffix, and that different batch composition can move
log-probabilities enough to flip a greedy choice near a tie. Replay pairs are a small
sample. This script asks the broader question the interpretation actually depends on:

    of every decision this project has recorded, which ones were produced by a split
    evaluation, and therefore *could* have been affected?

Classification uses the observed `timings.cache_n` from the saved server response, not the
requested setting, because the physically relevant fact is whether the prompt was actually
evaluated in one fresh pass:

* ``fresh``  (cache_n == 0): whole prompt evaluated in a single fresh batch. The tiny-model
  gate showed three shuffled uncached repetitions are bit-identical, so these are reproducible.
* ``split``  (cache_n > 0): a prefix came from cache and a suffix was evaluated as a smaller
  batch. Exposed to the perturbation.

**This is an exposure upper bound, not an effect estimate.** No study recorded `n_probs`, so
no decision margin exists in the record and we cannot say which split decisions were actually
near a tie. Exposure says how much of a finding *rests on* calls that carry the risk at all.

**RETRACTED 2026-09-09 — the margin argument this module used to make.** Earlier versions of
this docstring and of the emitted ``summary.reading`` argued that the cached perturbation was
"at most ~0.22 nats", so "a split decision with a margin far above that was almost certainly
unaffected", and therefore that large uniform contrasts survive full exposure. **Both steps are
now contradicted by direct measurement on real study checkpoints**
(``docs/peer_claims_v3_cross_family_gates.md``, Gate 2):

* The 0.22-nat figure came from a **random-weight tiny self-test model**. Real checkpoints reach
  **5.05 nats** — an order of magnitude larger. The self-test validated the *mechanism* and badly
  understated its *magnitude*; it must not be cited as a bound.
* **Flips are not confined to near-ties.** ``mistral7b`` had the far smaller reference decision
  margin (0.0102 vs 0.3514 nats) and flipped nothing, while ``llama31_8b`` flipped at margins of
  0.35 and 2.59 nats.

So a comfortable margin is **not** evidence that a cached record was safe, and margin cannot be
used post hoc to rehabilitate split-cache records. Exposure is reported here without any
accompanying claim about which findings survive it. Ranking fragility requires re-running the
arm with ``cache_prompt=false``, which is what
``experiments/peer_claims_v2_recovery`` did for V2 and what no other exposed arm has had.

Outputs `results/determinism/cache_exposure.json`, including a per-ACH-row table so each
evidence row in `experiments/ach/ratings_v1.json` can be read with its exposure attached.
"""
import json
import pathlib
import re

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'results/determinism'
# Excluded: retrieval/annotation corpora (no model decisions); the labelled self-tests; and the
# per-step/per-call mirror logs and the preserved pre-repair copy, whose generations are already
# nested inside the corresponding rollouts.jsonl and would otherwise be counted twice.
SKIP = re.compile(r'results/(cooperation|review|literature|cpu)/'
                  r'|/(packets|reasoning_index|steps|calls)\.jsonl$'
                  r'|rollouts_original_aliasing\.jsonl$'
                  r'|selftest|simulation')


def responses(node, path=''):
    """Yield (path, response_dict) for every llama-server response nested anywhere in a record."""
    if isinstance(node, dict):
        if isinstance(node.get('timings'), dict) and 'cache_n' in node['timings']:
            yield path, node
            return
        for k, v in node.items():
            yield from responses(v, f'{path}/{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from responses(v, f'{path}[{i}]')


def labels(rec, relpath):
    """Flatten the identifying fields a record may carry, whatever its study's shape."""
    case = rec.get('case') if isinstance(rec.get('case'), dict) else {}
    out = {'file': relpath, 'study': relpath.split('/')[1] if relpath.startswith('results/') else relpath,
           'model': rec.get('model') or case.get('model'),
           'case_id': case.get('id') or rec.get('id') or rec.get('context_id'),
           'phase': rec.get('phase') or rec.get('arm') or case.get('arm'),
           'probe': rec.get('probe'), 'decision': rec.get('decision'), 'checked': rec.get('checked')}
    for k in ['world_name', 'claim', 'policy', 'order', 'priority', 'control', 'diagnostic']:
        if k in case:
            out[k] = case[k]
    if isinstance(case.get('world'), dict):
        out['available'] = case['world'].get('available')
    return out


def episodes():
    """One entry per recorded episode, with its calls classified fresh/split."""
    out = []
    for path in sorted(R.glob('results/**/*.jsonl')):
        rel = str(path.relative_to(R))
        if SKIP.search(rel):
            continue
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            rec = json.loads(line)
            calls = [{'path': p, 'cache_n': r['timings'].get('cache_n'), 'prompt_n': r['timings'].get('prompt_n'),
                      'split': bool(r['timings'].get('cache_n'))} for p, r in responses(rec)]
            if not calls:
                continue
            lab = labels(rec, rel)
            out.append({**lab, 'line': line_no, 'calls': len(calls),
                        'split_calls': sum(c['split'] for c in calls),
                        'first_split': calls[0]['split'], 'final_split': calls[-1]['split'],
                        'any_split': any(c['split'] for c in calls),
                        'fresh_suffix_tokens': [c['prompt_n'] for c in calls if c['split']]})
    return out


def block(eps):
    n = len(eps)
    if not n:
        return {'episodes': 0}
    calls = sum(e['calls'] for e in eps)
    suffixes = [x for e in eps for x in e['fresh_suffix_tokens'] if x is not None]
    return {'episodes': n, 'calls': calls, 'split_calls': sum(e['split_calls'] for e in eps),
            'split_call_rate': round(sum(e['split_calls'] for e in eps) / calls, 3) if calls else None,
            'first_call_split_rate': round(sum(e['first_split'] for e in eps) / n, 3),
            'final_call_split_rate': round(sum(e['final_split'] for e in eps) / n, 3),
            'any_call_split_rate': round(sum(e['any_split'] for e in eps) / n, 3),
            'fresh_suffix_tokens_min_median_max': ([min(suffixes), sorted(suffixes)[len(suffixes) // 2], max(suffixes)] if suffixes else None)}


def pick(eps, file_contains=None, **eq):
    out = []
    for e in eps:
        if file_contains and file_contains not in e['file']:
            continue
        if all(e.get(k) == v for k, v in eq.items() if not isinstance(v, (list, tuple))) and \
           all(e.get(k) in v for k, v in eq.items() if isinstance(v, (list, tuple))):
            out.append(e)
    return out


# ACH evidence row -> the recorded episodes it rests on. Rows R01-R06 are historical and have no calls.
ACH_ROWS = {
    'X01': dict(file_contains='peer_claims_v2/qwen3', phase='main', world_name='costly', policy='optional', claim=('none', 'hopeless')),
    'X02': dict(file_contains='peer_claims_v2/qwen3', phase='main', world_name='costly', policy='required', claim='hopeless'),
    'X03': dict(file_contains='peer_claims_v2/qwen3', phase='main', world_name='costly', policy='automatic', claim='hopeless'),
    'X04': dict(file_contains='peer_claims_v2/qwen3', phase='main', world_name='costly', policy='required', claim='none'),
    'X05': dict(file_contains='peer_claim_order/qwen3'),
    'X06': dict(file_contains='opportunity_cost/v2', phase='main', control=None, probe=False, world_name=('costly', 'blocked')),
    'X07': dict(file_contains='opportunity_cost/v2', phase='main', control=None, probe=False, world_name='slack'),
    'X08': dict(file_contains='opportunity_cost/v2', phase='main', control=None, probe=False, world_name='shared'),
    'X09': dict(file_contains='opportunity_cost/v2', phase='main', control=None, probe=False),
    'X10': dict(file_contains='escalation/pilot_v2'),
    'X11': dict(file_contains='escalation/continuations'),
    'X12': dict(file_contains='workflow_obligations/v2', control=False),
    'X13': dict(file_contains='workflow_completion'),
    'X14': dict(file_contains='behavioral_pilot/v3'),
}


def main():
    eps = episodes()
    by_file = {}
    for e in eps:
        by_file.setdefault(e['file'], []).append(e)
    ach = {}
    for row, sel in ACH_ROWS.items():
        sub = pick(eps, **sel)
        ach[row] = {'selection': {k: v for k, v in sel.items()}, **block(sub)}
    cells = {}
    for e in pick(eps, file_contains='peer_claims_v2/qwen3', phase='main'):
        cells.setdefault(f"{e.get('world_name')}/{e.get('claim')}/{e.get('policy')}", []).append(e)
    exposed = sorted(k for k, v in ach.items() if v.get('any_call_split_rate'))
    unexposed = sorted(k for k, v in ach.items() if v.get('episodes') and not v.get('any_call_split_rate'))
    result = {
        'summary': {
            'exposed_rows': exposed, 'unexposed_rows': unexposed,
            'reading': ('Exposure is close to all-or-nothing per study, because the setting was per-study: every cache_prompt=true row is at ~1.0 and '
                        'every cache_prompt=false row is at 0.0. Exposure therefore does not by itself rank which findings are fragile, and nothing '
                        'else in this artifact ranks them either: the margin-based argument this field used to make is retracted (see the retraction '
                        'block). The only demonstrated way to establish that an exposed finding survives is to re-run the arm with cache_prompt=false. '
                        'The unexposed rows are the subset carrying no artifact risk at all.'),
        },
        'retraction': {
            'utc': '2026-09-09',
            'what': ('Earlier versions of summary.reading argued that the measured cached deviation was "at most ~0.22 nats, which flips only '
                     'near-ties", and concluded that a large contrast uniform across matched pairs and checkpoints (X06) survives full exposure '
                     'while the four-case X04 cell does not. That ranking argument is withdrawn.'),
            'why': ('Both premises are contradicted by direct measurement on real study checkpoints (docs/peer_claims_v3_cross_family_gates.md, '
                    'Gate 2). (1) The 0.22-nat figure came from a random-weight tiny self-test model; real checkpoints reach 5.05 nats, an order of '
                    'magnitude larger. (2) Flips are not confined to near-ties: mistral7b had the smaller reference margin (0.0102 vs 0.3514 nats) '
                    'and flipped nothing, while llama31_8b flipped at margins of 0.35 and 2.59 nats. A comfortable margin is therefore not evidence '
                    'that a cached record was safe, and margin cannot be used post hoc to rehabilitate split-cache records.'),
            'status_of_the_exposure_numbers': ('Unaffected. The retraction is of the interpretation layered on top of them, not of the counts. '
                                               'Cite split_call_rate from this file directly; a recomputed 59.0%/2266 figure that surfaced in '
                                               'planning notes is unverified and should not be quoted without re-running this module.'),
        },
        'rerun_status': {
            'note': ('Hand-maintained ledger: whether an exposed arm has ever been re-executed with cache_prompt=false. Not derivable from the '
                     'rollout files, which record only the configuration each arm actually used.'),
            'rerun_clean': {'peer_claims_v2': 'experiments/peer_claims_v2_recovery reproduced it uncached on a bit-identical checkpoint; '
                                              '73/74 decisions unchanged, headline matched contrast 75pp -> 50pp. Cite the 50pp figure.'},
            'still_exposed_never_rerun': ['peer_claim_order', 'peer_claims (V1)', 'opportunity_cost (V1)',
                                          'opportunity_cost (V2, including the +100pp Costly/Blocked contrast)',
                                          'workflow_obligations', 'workflow_completion'],
            'never_exposed': ['escalation_pilot (requested cache_prompt=false)'],
            'consequence': ('Exact-replay checks inside the still-exposed arms cannot be treated as clean repeatability evidence. This does not '
                            'invalidate those records; it means their stability claims are unestablished rather than established.'),
        },
        'method': 'A call is split when the saved response reports timings.cache_n > 0, meaning a prefix was served from the resident KV cache and only a suffix was freshly evaluated.',
        'caveat': 'Exposure is an upper bound on how many decisions could have been perturbed, not an estimate of how many were. No study recorded n_probs, so no decision margins exist in the record.',
        'overall': block(eps),
        'by_file': {f: block(v) for f, v in sorted(by_file.items())},
        'peer_claims_v2_qwen3_cells': {k: block(v) for k, v in sorted(cells.items())},
        'ach_rows': ach,
        'control': 'escalation studies requested cache_prompt=false; their split rates are the internal check that the metric detects the configuration.',
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'cache_exposure.json').write_text(json.dumps(result, indent=1) + '\n')
    (OUT / 'cache_exposure_episodes.json').write_text(json.dumps(eps, indent=1) + '\n')
    print('episodes', result['overall']['episodes'], 'calls', result['overall']['calls'], 'split call rate', result['overall']['split_call_rate'])
    for row, v in ach.items():
        if v.get('episodes'):
            print(f"{row}: episodes {v['episodes']:4d} first-call split {v['first_call_split_rate']:.2f} final-call split {v['final_call_split_rate']:.2f} any {v['any_call_split_rate']:.2f}")
    return result


if __name__ == '__main__':
    main()
