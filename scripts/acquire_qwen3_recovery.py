"""Reproduce the frozen Qwen3-8B Q4_K_M checkpoint for the V2 recovery run.

The V2 records were produced on a different machine against a *locally converted*
GGUF, so there is no downloadable artifact to fetch. This script reproduces it
from the pinned inputs recorded in
``experiments/workflow_obligations/qwen3_source.json`` and the original
conversion/quantization logs in ``results/workflow_obligations/``:

* HF revision ``b968826d9c46dd6066d109eabc6255188de91218`` of ``Qwen/Qwen3-8B``
* ``convert_hf_to_gguf.py`` from the pruned llama.cpp ``5266f24da`` source tree
  already vendored under ``data/external/llama_conversion_source/``
* ``--outtype f16`` (the original log shows F16 tensors, 399 of them, 16.4G)
* ``llama-quantize ... Q4_K_M`` (original quant size 4789.19 MiB, 4.90 BPW)

The model directory basename is passed through as the snapshot revision hash,
because ``convert_hf_to_gguf.py`` derives ``general.name`` from it and the
original log line reads ``Loading model: b968826d...``. A different basename
would change GGUF metadata and therefore the file hash.

**The SHA-256 comparison is a gate, not a note.** A match means the recovery is a
true same-checkpoint comparison in which ``cache_prompt`` is the only difference.
A mismatch means it is a different-checkpoint comparison, which confounds
quantization with the cache fix in every cell, and must be recorded in an
amendment before any inference rather than waved through.

Usage:

    python3 scripts/acquire_qwen3_recovery.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys

R = pathlib.Path(__file__).resolve().parents[1]
SRC = json.loads((R / 'experiments/workflow_obligations/qwen3_source.json').read_text())
CONV = R / 'data/external/llama_conversion_source/llama.cpp-5266f24da'
OUT = R / 'results/peer_claims_v2_recovery'
TARGET = R / SRC['gguf_path']
F16 = TARGET.parent / 'qwen3-8b-f16.gguf'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def snapshot():
    """Resolve the pinned snapshot directory; its basename must be the revision."""
    rev = SRC['revision']
    p = (pathlib.Path.home() / '.cache/huggingface/hub'
         / ('models--' + SRC['repository'].replace('/', '--')) / 'snapshots' / rev)
    assert p.is_dir(), f'snapshot not downloaded: {p}'
    assert p.name == rev, f'basename must be the revision (general.name): {p.name}'
    n = len(list(p.glob('*.safetensors')))
    assert n == 5, f'expected 5 safetensors shards, found {n}'
    return p


def run(cmd, log_name):
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / log_name
    print('+', ' '.join(str(c) for c in cmd), flush=True)
    with log.open('w') as fh:
        r = subprocess.run(cmd, cwd=R, stdout=fh, stderr=subprocess.STDOUT)
    assert r.returncode == 0, f'failed ({r.returncode}); see {log}'
    return log


def main():
    snap = snapshot()
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    if not F16.exists():
        env_python = R / '.venv-convert/bin/python'
        run([str(env_python), str(CONV / 'convert_hf_to_gguf.py'), str(snap),
             '--outfile', str(F16), '--outtype', 'f16'], 'qwen3_conversion.log')
    else:
        print('f16 already present, skipping conversion', flush=True)

    if not TARGET.exists():
        run(['llama-quantize', str(F16), str(TARGET), 'Q4_K_M'], 'qwen3_quantization.log')
    else:
        print('Q4_K_M already present, skipping quantization', flush=True)

    actual = sha256(TARGET)
    expected = SRC['gguf_sha256']
    record = {
        'repository': SRC['repository'], 'revision': SRC['revision'],
        'conversion_commit': SRC['conversion_commit'], 'outtype': 'f16',
        'snapshot_dir': str(snap), 'gguf_path': SRC['gguf_path'],
        'expected_sha256': expected, 'actual_sha256': actual,
        'match': actual == expected, 'bytes': TARGET.stat().st_size,
        'f16_sha256': sha256(F16),
    }
    (OUT / 'acquisition.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'snapshot_dir'}, indent=2))

    if actual == expected:
        print('\nSHA-256 MATCH: same-checkpoint recovery; cache_prompt is the only difference.')
        return 0
    print('\nSHA-256 MISMATCH: this is a DIFFERENT checkpoint from the one V2 used.')
    print('Do not run the panel on it without recording an amendment first: a quantization')
    print('difference would be confounded with the cache fix in every cell.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
