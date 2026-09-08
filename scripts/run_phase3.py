"""Rebuild every phase-3 check that does not need a GPU.

Mirrors run_cpu.py. The hardware gate is deliberately NOT run here: it needs the
cluster, and a gate that quietly "passes" by being skipped is worse than no gate.
Run it separately with scripts/hardware_gate.py.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/phase3'

STAGES = ['tampering_selftest.py', 'whistleblow_selftest.py',
          'env_selftest.py', 'censor_selftest.py']


def main():
    for stage in STAGES:
        print(f'--- {stage}')
        r = subprocess.run([sys.executable, str(ROOT / 'scripts' / stage)])
        if r.returncode != 0:
            print(f'FAILED: {stage}')
            return r.returncode

    manifest = {}
    for path in sorted(OUT.glob('*.json')):
        if path.name == 'output_manifest.json':
            continue
        manifest[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (OUT / 'output_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    print(f'\nAll {len(STAGES)} stages passed. {len(manifest)} outputs hashed '
          '-> results/phase3/output_manifest.json')
    print('Hardware gate NOT included: run scripts/hardware_gate.py on the cluster.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
