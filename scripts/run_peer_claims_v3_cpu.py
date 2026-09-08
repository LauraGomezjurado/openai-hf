"""Start the server, run the determinism gate once, then run one V3 stage for one model.

    python3 scripts/run_peer_claims_v3_cpu.py mistral7b A
    # write experiments/peer_claims_v3/hypotheses_from_reasoning/mistral7b.md, then
    python3 scripts/peer_claims_v3.py freeze-stage-b mistral7b
    python3 scripts/run_peer_claims_v3_cpu.py mistral7b B
    python3 scripts/peer_claims_v3.py freeze-stage-d mistral7b nonpeer,uncertain "why these"
    python3 scripts/run_peer_claims_v3_cpu.py mistral7b D
"""
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

R = pathlib.Path(__file__).resolve().parents[1]
D = R / 'results/peer_claims_v3'
model, stage = sys.argv[1], sys.argv[2]
D.mkdir(parents=True, exist_ok=True)
gate = R / 'results/determinism' / f'gate_{model}.json'
with (D / f'{model}_server.log').open('a') as log:
    server = subprocess.Popen(['python3', 'scripts/serve_v3_cpu.py', model], cwd=R, stdout=log, stderr=subprocess.STDOUT)
    try:
        for _ in range(600):
            assert server.poll() is None, 'server exited; see the server log'
            try:
                with urllib.request.urlopen('http://127.0.0.1:18973/health', timeout=2) as h:
                    if json.load(h)['status'] == 'ok':
                        break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError('server not ready')
        (D / f'{model}_runtime.json').write_text((D / f'{model}_server.json').read_text())
        if not gate.exists():
            subprocess.run(['python3', 'scripts/determinism_gate.py', '--messages-file', 'experiments/peer_claims_v3/gate_prompts.json', '--n', '8', '--reps', '3', '--out', str(gate), '--model-note', model], cwd=R, check=True)
        with (D / f'{model}_run_{stage}.log').open('a') as out:
            subprocess.run(['python3', 'scripts/peer_claims_v3.py', 'run', model, stage], cwd=R, stdout=out, stderr=subprocess.STDOUT, check=True)
    finally:
        server.terminate()
        server.wait(timeout=60)
