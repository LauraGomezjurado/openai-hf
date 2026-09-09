"""Re-run the frozen V2 peer-claim experiment with the one backend flag corrected.

The V2 records were produced with ``cache_prompt=True``
(:mod:`peer_claims_v2` line 29). The determinism gate has since shown that
split KV-cache evaluation flips greedy tokens on real 8B checkpoints by up to
5.05 nats, and the cache-exposure audit found 83.7% of the project's recorded
generation calls ran under that regime. V2's exact-replay checks therefore
cannot be read as clean repeatability evidence, so the headline contrast needs
recovery under the fixed configuration before it can carry any weight.

This module changes **exactly one thing**: completion requests are sent with
``cache_prompt=False``. It deliberately does not touch the cases, the wording,
the schema, the seed, the token budget, the two-turn loop, the server command or
the checkpoint. To make that auditable it asserts every hash in V2's
``freeze.json`` — including the hash of ``scripts/peer_claims_v2.py`` itself —
so the run aborts if the frozen interface has been edited rather than wrapped.

Reasoning capture is intentionally **not** enabled here. Adding a scratchpad
phase would change the interface and confound "does the phenomenon survive the
cache fix" with "does it survive a different prompt shape". A reasoning-capture
arm is a separate, later comparison against this one.

Outputs go to ``results/peer_claims_v2_recovery/<model>/`` and never overwrite
the original V2 records, which are kept for comparison.

Usage (server already running via ``scripts/serve_opportunity_cpu.py qwen3``,
and only after the determinism gate has passed on this machine):

    python3 scripts/peer_claims_v2_recovery.py run qwen3
"""
import sys

import opportunity_allocation as a
import peer_claims_v2 as pc2

OVERRIDE = {'cache_prompt': False}

_post = a.post


def post(path, payload):
    """Force the corrected flag on every completion request."""
    if path == 'completion':
        payload = dict(payload, **OVERRIDE)
    return _post(path, payload)


_generate = pc2.generate


def generate(ms, c, checked):
    """Record the settings actually sent, plus an explicit override marker."""
    step = _generate(ms, c, checked)
    step['settings'].update(OVERRIDE)
    step['recovery'] = {'override': 'cache_prompt', 'frozen_value': True,
                        'sent_value': False, 'reason': 'split-KV-cache greedy flips'}
    return step


def install():
    """Redirect output and apply the override to the frozen module in place."""
    a.post = post
    pc2.a.post = post
    pc2.generate = generate
    pc2.D = pc2.R / 'results/peer_claims_v2_recovery'
    pc2.D.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    assert sys.argv[1] == 'run', 'freezing is not re-run here; V2 stays frozen'
    install()
    pc2.run(sys.argv[2])
