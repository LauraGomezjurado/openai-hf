"""Run only the capability-control block of a frozen arm, write its gate, and stop.

Each arm's own ``run(model)`` walks its whole ``run_order`` and continues straight
into the measurement blocks the moment the control gate passes. The authorization
in hand covers the two backend gates and the capability controls and nothing after
them, and the arm modules are frozen by content hash, so they cannot be given a
phase flag. This driver wraps them instead: it repeats the arm's own preconditions,
calls the arm's own ``execute`` and ``gate``, writes the same records to the same
paths, and touches no phase other than ``controls``.

Nothing here is a second implementation of the arm. Every decision, prompt, oracle
and verdict comes from the frozen module; this file only bounds which phase runs.
Because ``run(model)`` rebuilds ``done`` from ``rollouts.jsonl``, a later
authorized ``run(model)`` skips the controls recorded here and starts at the first
measurement case -- the records are the same records it would have written.

    python3 scripts/run_capability_controls.py factorial qwen3
    python3 scripts/run_capability_controls.py interface qwen3
"""
import importlib
import json
import os
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))

ARMS = {'factorial': 'peer_message_factorial', 'interface': 'peer_interface_decomposition'}


def preconditions(m, model):
    """The checks the arm's own run() makes before its first rollout, in its order.

    Returns (freeze, stop_message). A stop message means the arm would have
    printed the same line and returned, so this driver does too.
    """
    import peer_authority as pa
    f = m.verify_freeze()
    assert model in f['models'], model
    spec = pa.model_spec(model)
    g = R / 'results/determinism' / ('gate_%s_%s.json' % (model, m.GATE_NAME))
    if not g.exists() or json.loads(g.read_text()).get('verdict') != 'pass':
        return f, 'DETERMINISM GATE STOP results/determinism/gate_%s_%s.json' % (model, m.GATE_NAME)
    served = ((json.loads(g.read_text()).get('server_props') or {}).get('model_path') or '')
    if not served.endswith(pathlib.Path(spec['gguf_path']).name):
        return f, 'DETERMINISM GATE STOP gate ran on a different model file: ' + served
    if hasattr(m, 'anchor_identity_report'):
        identity = m.anchor_identity_report()
        if not (identity['old_anchor_matches_peer_claims_v2']
                and identity['new_anchor_matches_peer_env_ext']):
            return f, 'ANCHOR IDENTITY STOP ' + json.dumps(identity['mismatches'])
    return f, None


def controls(arm, model):
    import opportunity_cost as w
    m = importlib.import_module(ARMS[arm])
    f, stop = preconditions(m, model)
    if stop:
        print(stop, flush=True)
        return 1
    cases = json.loads((m.E / 'cases.json').read_text())['controls']
    out = m.D / model
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'rollouts.jsonl'
    old = [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []
    done = {(r['case']['id'], r['phase']) for r in old}
    for c in cases:
        if (c['id'], 'controls') in done:
            continue
        r = m.execute(c, model, 'controls')
        with path.open('a') as h:
            h.write(json.dumps(r) + '\n')
            h.flush()
            os.fsync(h.fileno())
        old.append(r)
        done.add((c['id'], 'controls'))
        for name, value in r['result']['state']['outputs'].items():
            w.dump(out / 'artifacts' / 'controls' / c['id'] / name, value)
        print('controls', c['id'], c['control'], r['decision'],
              r['outcome'].get('capability_ok'), flush=True)
    ctl = [r for r in old if r['phase'] == 'controls']
    verdict = m.gate(ctl)
    verdict['required_controls'] = f['counts']['controls']
    verdict['complete'] = len(ctl) == verdict['required_controls']
    if hasattr(m, 'anchor_identity_report'):
        verdict['anchor_identity'] = m.anchor_identity_report()
    verdict['eligible'] = bool(verdict['eligible'] and verdict['complete'])
    verdict['controls_only_driver'] = ('measurement blocks not run: authorization covered the '
                                      'gates and the controls only')
    w.dump(out / 'gate.json', verdict)
    print(arm, model, 'controls', len(ctl), 'eligible', verdict['eligible'], flush=True)
    print(json.dumps(verdict['tiers'], indent=2), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(controls(sys.argv[1], sys.argv[2]))
