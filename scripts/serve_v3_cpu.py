"""Launch llama-server for a peer-claims V3 model key with the fixed repeatability settings.

Differences from serve_opportunity_cpu.py: a single slot, explicit batch sizes, no
enable_thinking=false for native-thinking checkpoints (reasoning is captured instead),
and the runtime record includes the resolved model hash so the determinism gate can be
matched to the file it ran on. Thread counts come from V3_THREADS (default 6).
"""
import hashlib
import json
import os
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
key = sys.argv[1]
spec = json.loads((R / 'experiments/peer_claims_v3' / ('models_selftest' if key.startswith('selftest_') else 'models') / f'{key}.json').read_text())
model = R / spec['gguf_path']
assert model.exists(), f'model file missing: {model}; see {spec.get("acquisition")}'
digest = hashlib.sha256(model.read_bytes()).hexdigest()
if spec.get('gguf_sha256'):
    assert digest == spec['gguf_sha256'], 'model file hash does not match the frozen source record'
threads = os.environ.get('V3_THREADS', '6')
cmd = ['llama-server', '-m', str(model), '--device', 'none', '-ngl', '0', '--no-op-offload', '--no-kv-offload', '--fit', 'off', '-c', '8192', '-np', '1', '-b', '2048', '-ub', '512',
       '-t', threads, '-tb', threads, '--host', '127.0.0.1', '--port', '18973', '--jinja']
if spec['reasoning_mode'] != 'native_think' and spec.get('template_kwargs'):
    cmd += ['--chat-template-kwargs', json.dumps(spec['template_kwargs'])]
out = R / 'results/peer_claims_v3'
out.mkdir(parents=True, exist_ok=True)
(out / f'{key}_server.json').write_text(json.dumps({'pid': os.getpid(), 'command': cmd, 'source': spec, 'resolved_gguf_sha256': digest}, indent=2) + '\n')
os.execvp(cmd[0], cmd)
