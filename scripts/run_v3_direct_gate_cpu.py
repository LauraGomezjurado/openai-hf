"""Start the server, run the direct-mode determinism gate once, then run the direct-mode control gate.

Mirrors scripts/run_peer_claims_v3_cpu.py, but gates on direct-mode prompt shapes and writes
results/determinism/gate_<model>_direct.json. One server at a time by construction: the server is
started here and terminated in the finally block.

    python3 scripts/run_v3_direct_gate_cpu.py mistral7b
    python3 scripts/run_v3_direct_gate_cpu.py llama31_8b
"""
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

R = pathlib.Path(__file__).resolve().parents[1]
D = R / 'results/peer_claims_v3_direct_gate'
model = sys.argv[1]
D.mkdir(parents=True, exist_ok=True)
gate = R / 'results/determinism' / f'gate_{model}_direct.json'
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
        (D / f'{model}_runtime.json').write_text((R / 'results/peer_claims_v3' / f'{model}_server.json').read_text())
        if not gate.exists():
            subprocess.run(['python3', 'scripts/determinism_gate.py',
                            '--messages-file', 'experiments/peer_claims_v3_direct_gate/gate_prompts.json',
                            '--n', '8', '--reps', '3', '--out', str(gate), '--model-note', f'{model}_direct'],
                           cwd=R, check=True)
        with (D / f'{model}_run.log').open('a') as out:
            subprocess.run(['python3', 'scripts/peer_claims_v3_direct_gate.py', 'run', model],
                           cwd=R, stdout=out, stderr=subprocess.STDOUT, check=True)
    finally:
        server.terminate()
        server.wait(timeout=60)
