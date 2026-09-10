"""Direct-mode control gate for the two V3 checkpoints excluded on the scratchpad interface.

An enabling gate, not a hypothesis test. It runs the 20 frozen V3 control cases with
``mode='direct'`` and reports whether a checkpoint reaches the unchanged 20/20 threshold.

Design and the predeclared reading of either outcome:
``experiments/peer_claims_v3_direct_gate/protocol.md``.

This module WRAPS the frozen V3 arm and edits nothing hashed by
``experiments/peer_claims_v3/freeze.json``. Cases are built by calling ``v3.case`` with
``mode='direct'`` -- an existing frozen code path (``peer_claims_v3.messages`` line 92 skips the
scratchpad instruction, ``generate`` line 101 passes reasoning mode 'none'). Prompt assembly,
grammar, scoring and execution all come from the frozen module by import. Monkeypatching a
hashed module is forbidden here: ``freeze.json`` hashes file bytes only, so a patched call site
would pass ``verify_freeze`` while silently invalidating the frozen arm's provenance.

    python3 scripts/peer_claims_v3_direct_gate.py freeze
    python3 scripts/run_v3_direct_gate_cpu.py mistral7b
    python3 scripts/run_v3_direct_gate_cpu.py llama31_8b
"""
import json
import os
import pathlib
import sys
import time

import opportunity_cost as w
import peer_claims_v2 as p
import peer_claims_v3 as v3

R = p.R
E = R / 'experiments/peer_claims_v3_direct_gate'
D = R / 'results/peer_claims_v3_direct_gate'
MODELS = ['mistral7b', 'llama31_8b']


def build_cases():
    """The 20 V3 controls with mode='direct'. Identical to peer_claims_v3.build_cases()['controls']
    except for the mode, which is the single manipulated factor of this arm."""
    controls = [v3.case(d, truth, 'none', 'automatic' if ctl == 'direct' else 'optional', 0, mode='direct', control=ctl)
                for d in v3.DOMAINS for truth in [False, True] for ctl in ['direct', 'check']]
    controls += [v3.case(d, True, 'none', 'automatic', 0, mode='direct', slack=True, control='joint') for d in v3.DOMAINS]
    return {'controls': controls}


def gate_prompts(cases):
    """Eight direct-mode control contexts for the backend determinism gate.

    The existing results/determinism/gate_<model>.json records pass on this machine but were
    rendered from scratchpad-mode prompts. The gate exists to exercise the exact request shapes a
    study uses, so this arm gates on its own direct-mode shapes.
    """
    return [{'messages': v3.messages(c, 'none'), 'json_schema': v3.schema(c, False), 'n_predict': 192} for c in cases['controls'][:8]]


def freeze():
    assert not (E / 'freeze.json').exists(), 'already frozen'
    cases = build_cases()
    w.dump(E / 'cases.json', cases)
    w.dump(E / 'gate_prompts.json', gate_prompts(cases))
    files = [E / 'cases.json', E / 'gate_prompts.json', E / 'protocol.md', pathlib.Path(__file__),
             R / 'scripts/peer_claims_v3.py', R / 'scripts/peer_claims_v2.py', R / 'scripts/reasoning_capture.py',
             R / 'scripts/determinism_gate.py', R / 'scripts/opportunity_allocation.py', R / 'scripts/opportunity_cost.py']
    files += [R / 'experiments/peer_claims_v3/models' / f'{m}.json' for m in MODELS]
    w.dump(E / 'freeze.json', {
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'models': MODELS,
        'hashes': {str(x.relative_to(R)): w.sha(x) for x in files},
        'counts': {'controls': len(cases['controls'])},
        'gate': {'controls': len(cases['controls']),
                 'criterion': 'passed == required == n, i.e. 20 of 20 peer_claims_v2.control_ok',
                 'determinism': 'results/determinism/gate_<model>_direct.json must report verdict pass for the same model file'},
        'generation': {'temperature': 0, 'seed': v3.SEED, 'cache_prompt': False,
                       'reasoning_budget': 512, 'decision_budget': 192, 'n_probs': 10, 'mode': 'direct'},
        'reference': {'mistral7b': 'reason-mode gate 14/20', 'llama31_8b': 'reason-mode gate 10/20'}})


def verify_freeze():
    f = json.loads((E / 'freeze.json').read_text())
    for path, h in f['hashes'].items():
        assert w.sha(R / path) == h, f'frozen file changed: {path}'
    return f


def determinism_ok(model, spec):
    g = R / 'results/determinism' / f'gate_{model}_direct.json'
    if not g.exists():
        return False, 'determinism gate missing'
    d = json.loads(g.read_text())
    if d.get('verdict') != 'pass':
        return False, 'determinism gate failed'
    path = (d.get('server_props') or {}).get('model_path') or ''
    if not path.endswith(pathlib.Path(spec['gguf_path']).name):
        return False, f'determinism gate ran on a different model file: {path}'
    return True, 'ok'


def run(model):
    f = verify_freeze()
    assert model in f['models'], model
    spec = v3.model_spec(model)
    cases = json.loads((E / 'cases.json').read_text())
    budgets = {k: f['generation'][f'{k}_budget'] if k != 'n_probs' else f['generation']['n_probs']
               for k in ['reasoning', 'decision', 'n_probs']}
    out = D / model
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'rollouts.jsonl'
    old = [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []
    done = {r['case']['id'] for r in old}
    ok, why = determinism_ok(model, spec)
    if not ok:
        print('DETERMINISM GATE STOP', why, flush=True)
        return
    for c in cases['controls']:
        if c['id'] in done:
            continue
        r = v3.execute(c, model, spec['reasoning_mode'], budgets, 'controls')
        with path.open('a') as h:
            h.write(json.dumps(r) + '\n')
            h.flush()
            os.fsync(h.fileno())
        old.append(r)
        done.add(c['id'])
        for name, value in r['result']['state']['outputs'].items():
            w.dump(out / 'artifacts' / c['id'] / name, value)
        print('control', c['id'], r['checked'], r['decision'], 'ok' if v3.control_ok(r) else 'FAIL', flush=True)
    g = {'model': model, 'mode': 'direct',
         'passed': sum(v3.control_ok(r) for r in old), 'n': len(old), 'required': f['counts']['controls'],
         'reason_mode_reference': f['reference'][model],
         'per_control': [{'id': r['case']['id'], 'world': r['case']['world_name'], 'control': r['case']['control'],
                          'checked': r['checked'], 'decision': r['decision'],
                          'valid': r['result']['valid'], 'reason': r['result'].get('reason'),
                          'ok': bool(v3.control_ok(r))} for r in old]}
    g['eligible'] = g['passed'] == g['required'] == g['n']
    g['failures'] = [x['id'] for x in g['per_control'] if not x['ok']]
    w.dump(out / 'gate.json', g)
    w.dump(out / 'complete.json', {'completed': True, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                   'rollouts_sha256': w.sha(path)})
    print(('CONTROL GATE PASS ' if g['eligible'] else 'CONTROL GATE STOP '), json.dumps({k: g[k] for k in ['model', 'passed', 'n', 'required', 'eligible', 'failures']}), flush=True)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'freeze':
        freeze()
    elif cmd == 'run':
        run(sys.argv[2])
    else:
        raise SystemExit('usage: peer_claims_v3_direct_gate.py freeze | run MODEL')
