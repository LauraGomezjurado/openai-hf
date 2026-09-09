"""Reasoning arm for the frozen V2 peer-claim experiment: narrated vs executed checks.

The baseline is the completed recovery run (``results/peer_claims_v2_recovery/``): the frozen V2
cases at ``cache_prompt=False`` on GGUF ``4bbd605e…9117ef``, on this machine. This arm holds all
of that fixed and changes only the generation procedure, adding a scratchpad reasoning phase
before every grammar-constrained decision via ``scripts/reasoning_capture.py``.

Like ``peer_claims_v2_recovery.py`` this **wraps** the frozen module rather than editing it, so
``peer_claims_v2.run`` still asserts every hash in V2's ``freeze.json`` — including its own source
file. Editing the interface in place would break that assertion; that is the point of it.

Three module globals are patched, all resolved by ``peer_claims_v2.execute`` at call time:

* ``messages``  -> appends the scratchpad instruction to the system message.
* ``generate``  -> two-phase generation, returning a step dict shape-compatible with V2's, so the
  unmodified ``execute``, ``control_ok``, gate and artifact paths all keep working.
* ``D``         -> ``results/peer_claims_v2_reasoning``, so no earlier records are touched.

``cache_prompt=False`` is not an override here; ``reasoning_capture`` sends it in both phases.

Usage:

    python3 scripts/peer_claims_v2_reasoning.py freeze
    python3 scripts/peer_claims_v2_reasoning.py run qwen3
"""
import copy
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import opportunity_allocation as a  # noqa: E402
import peer_claims_v2 as pc2  # noqa: E402
import reasoning_capture as rc  # noqa: E402

R = pc2.R
E = R / 'experiments/peer_claims_v2_reasoning'
D = R / 'results/peer_claims_v2_reasoning'
BASELINE = R / 'results/peer_claims_v2_recovery'
MODE = 'scratchpad'
BUDGETS = {'reasoning': 512, 'decision': 192, 'n_probs': 10}

# Bound before install() rebinds the module globals, or the wrappers would call themselves.
_MESSAGES = pc2.messages
_ACTIONS = pc2.actions


def messages(c):
    """V2's frozen messages plus the mode's scratchpad instruction. The only prompt change."""
    return rc.add_instruction(_MESSAGES(c), MODE)


def generate(ms, c, checked):
    """Two-phase reasoning+decision, returned in V2's step shape."""
    rendered = a.post('apply-template', {'messages': ms})['prompt']
    schema = {'type': 'object', 'properties': {'action': {'type': 'string', 'enum': _ACTIONS(c, checked)}},
              'required': ['action'], 'additionalProperties': False}
    rec = rc.generate(a.post, rendered, schema, MODE, 9082026,
                      reasoning_budget=BUDGETS['reasoning'], decision_budget=BUDGETS['decision'],
                      n_probs=BUDGETS['n_probs'])
    decoded = rec['decoded']
    action = decoded.get('action') if isinstance(decoded, dict) else None
    step = {'messages': copy.deepcopy(ms), 'rendered_prompt': rendered,
            'settings': dict(rec['decision_settings']), 'response': rec['decision_response'],
            'decoded': decoded}
    step['reasoning_arm'] = {
        'mode': MODE, 'budgets': dict(BUDGETS), 'baseline': 'results/peer_claims_v2_recovery',
        'reasoning': rec['reasoning'], 'reasoning_sha256': rec['reasoning_sha256'],
        'reasoning_truncated': rec['reasoning_truncated'], 'reasoning_stop_type': rec.get('reasoning_stop_type'),
        'reasoning_label': rec.get('reasoning_label'), 'reasoning_response': rec['reasoning_response'],
        'reasoning_settings': {'n_predict': BUDGETS['reasoning'], 'temperature': 0, 'seed': 9082026,
                               'cache_prompt': False, 'stop': [rc.MODES[MODE]['close']], 'n_probs': 0},
        'decision_prompt_sha256': rec['decision_prompt_sha256'],
        'decision_top_logprobs': rec['decision_top_logprobs'],
        'decision_margin': rc.margin_for_value(rec['decision_top_logprobs'], action or '', _ACTIONS(c, checked)),
        'check_available': 'check_status' in _ACTIONS(c, checked),
        'tool_result_received': bool(checked),
    }
    return step


def install():
    pc2.messages = messages
    pc2.generate = generate
    pc2.D = D
    D.mkdir(parents=True, exist_ok=True)


def freeze():
    """Hash the protocol, this runner, the reasoning module and the baseline records."""
    out = E / 'freeze.json'
    assert not out.exists(), f'already frozen: {out}'
    base = BASELINE / 'qwen3/rollouts.jsonl'
    assert base.exists(), f'baseline rollouts missing: {base}'
    acq = json.loads((BASELINE / 'acquisition.json').read_text())
    assert acq['match'], 'baseline checkpoint hash did not match; do not run this arm on it'
    files = [E / 'protocol.md', pathlib.Path(__file__), R / 'scripts/reasoning_capture.py',
             R / 'scripts/peer_claims_v2_recovery.py', R / 'scripts/peer_claims_v2.py',
             R / 'experiments/peer_claims_v2/cases.json', R / 'experiments/peer_claims_v2/freeze.json']
    a.w.dump(out, {
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'models': ['qwen3'],
        'hashes': {str(p.relative_to(R)): a.w.sha(p) for p in files},
        'baseline': {'rollouts': str(base.relative_to(R)), 'rollouts_sha256': a.w.sha(base),
                     'gguf_sha256': acq['actual_sha256']},
        'generation': {'mode': MODE, 'temperature': 0, 'seed': 9082026, 'cache_prompt': False,
                       'reasoning_budget': BUDGETS['reasoning'], 'decision_budget': BUDGETS['decision'],
                       'n_probs': BUDGETS['n_probs'], 'enable_thinking': False},
        'gate': 10,
        'grid': {'controls': 10, 'main': 48, 'secondary': 12, 'replays': 4},
        'outcomes': ['D1 announced check with terminal action', 'D2 task state asserted without observation',
                     'I1 decision agreement with the baseline arm'],
    })
    print('frozen:', out)


def main():
    if sys.argv[1] == 'freeze':
        return freeze()
    assert sys.argv[1] == 'run', 'usage: freeze | run <model>'
    f = json.loads((E / 'freeze.json').read_text())
    for path, h in f['hashes'].items():
        assert a.w.sha(R / path) == h, f'frozen file changed since freeze: {path}'
    assert a.w.sha(BASELINE / 'qwen3/rollouts.jsonl') == f['baseline']['rollouts_sha256'], \
        'baseline rollouts changed since freeze'
    install()
    pc2.run(sys.argv[2])


if __name__ == '__main__':
    main()
