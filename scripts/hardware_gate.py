"""Week-1 gate: does the V100 box actually support the planned generation stack?

Discharges the standing README instruction to benchmark before reserving GPUs.
Two independent risks are retired here:

  (a) vLLM sm_70 support. Pre-Ampere support has been progressively deprecated;
      several attention backends and quantization paths are unavailable or fall
      back silently.
  (b) fp16 numerics. 2026 reasoning checkpoints are bf16-native and can overflow
      in fp16. Silent degradation presents as "the model reasons worse under
      condition X" and is indistinguishable from a finding.

Runs anywhere. On a machine without CUDA it records that the gate is not
runnable rather than failing, so the file is still a valid provenance record.

Usage:
    python3 scripts/hardware_gate.py [--model NAME] [--tp N] [--fp32-ref]
"""
import argparse
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/phase3'
OUT.mkdir(parents=True, exist_ok=True)

# Volta. No FlashAttention (FA1 needs sm_75, FA2 sm_80); no bf16; no FP8.
EXPECTED_CAPABILITY = (7, 0)
PROMPTS = [
    'Explain in one paragraph why a shared cache namespace is not a message board.',
    'A task appears impossible. List the options available to you, then choose one.',
    'Summarise the difference between comprehension of a rule and compliance with it.',
]


def probe_devices():
    try:
        import torch
    except ImportError:
        return {'torch': None, 'runnable': False, 'reason': 'torch not installed'}
    info = {'torch': torch.__version__, 'cuda_available': torch.cuda.is_available()}
    if not torch.cuda.is_available():
        info.update(runnable=False, reason='no CUDA device visible')
        return info
    info['device_count'] = torch.cuda.device_count()
    info['devices'] = []
    for i in range(torch.cuda.device_count()):
        cap = torch.cuda.get_device_capability(i)
        info['devices'].append({
            'index': i,
            'name': torch.cuda.get_device_name(i),
            'capability': f'{cap[0]}.{cap[1]}',
            'total_memory_gb': round(torch.cuda.get_device_properties(i).total_memory / 2**30, 2),
        })
    caps = {tuple(int(x) for x in d['capability'].split('.')) for d in info['devices']}
    info['homogeneous'] = len(caps) == 1
    info['is_volta'] = caps == {EXPECTED_CAPABILITY}
    # Expected False on Volta. True here means the fp16-only premise is wrong and
    # the protocol's numerics constraints can be relaxed.
    info['bf16_supported'] = bool(torch.cuda.is_bf16_supported())
    try:
        import flash_attn  # noqa: F401
        info['flash_attn_importable'] = True
    except Exception:
        info['flash_attn_importable'] = False
    info['runnable'] = True
    return info


def probe_vllm(model, tp, max_tokens=256):
    """Import, construct, and measure sustained output throughput."""
    try:
        import vllm
    except ImportError:
        return {'importable': False, 'reason': 'vllm not installed'}
    result = {'importable': True, 'version': getattr(vllm, '__version__', 'unknown'),
              'model': model, 'tensor_parallel_size': tp}
    try:
        from vllm import LLM, SamplingParams
        t0 = time.time()
        llm = LLM(model=model, dtype='float16', tensor_parallel_size=tp,
                  enable_prefix_caching=True, gpu_memory_utilization=0.90)
        result['load_seconds'] = round(time.time() - t0, 1)
        # Batch of 32 approximates the concurrency the KV budget allows at short context.
        params = SamplingParams(temperature=0.7, max_tokens=max_tokens, seed=0)
        batch = PROMPTS * 11  # 33 sequences
        t0 = time.time()
        outs = llm.generate(batch, params)
        elapsed = time.time() - t0
        produced = sum(len(o.outputs[0].token_ids) for o in outs)
        result.update(
            sequences=len(batch),
            output_tokens=produced,
            seconds=round(elapsed, 2),
            output_tokens_per_second=round(produced / elapsed, 1),
            any_empty=any(len(o.outputs[0].token_ids) == 0 for o in outs),
        )
    except Exception as exc:  # backend fallback, kernel absence, OOM
        result.update(constructed=False, error=f'{type(exc).__name__}: {exc}')
        return result
    result['constructed'] = True
    return result


def probe_fp16_numerics(model, fp32_reference):
    """Compare fp16 GPU logits against an fp32 reference on fixed prompts.

    fp32 reference runs on CPU and needs ~4 bytes/parameter of RAM. Skipped
    unless --fp32-ref is passed, because an 8B reference needs ~32 GB.
    """
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        return {'runnable': False, 'reason': 'transformers/torch not installed'}
    if not torch.cuda.is_available():
        return {'runnable': False, 'reason': 'no CUDA device'}
    tok = AutoTokenizer.from_pretrained(model)
    enc = tok(PROMPTS, return_tensors='pt', padding=True)
    res = {'runnable': True, 'model': model, 'prompts': len(PROMPTS)}

    half = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.float16).cuda().eval()
    with torch.no_grad():
        logits_h = half(**{k: v.cuda() for k, v in enc.items()}).logits.float().cpu()
    res['fp16_nonfinite_logits'] = int((~torch.isfinite(logits_h)).sum())
    res['fp16_max_abs_logit'] = round(float(logits_h.abs().max()), 2)
    del half
    torch.cuda.empty_cache()

    if not fp32_reference:
        res['fp32_reference'] = 'skipped (pass --fp32-ref; needs ~4 bytes/parameter of host RAM)'
        return res
    full = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.float32).eval()
    with torch.no_grad():
        logits_f = full(**enc).logits.float()
    diff = (logits_h - logits_f).abs()
    res.update(
        fp32_reference='cpu',
        max_abs_logit_diff=round(float(diff.max()), 4),
        mean_abs_logit_diff=round(float(diff.mean()), 6),
        # Rank agreement matters more than absolute drift for sampled generation.
        argmax_agreement=round(float((logits_h.argmax(-1) == logits_f.argmax(-1)).float().mean()), 4),
    )
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Qwen/Qwen3-8B')
    ap.add_argument('--tp', type=int, default=2)
    ap.add_argument('--fp32-ref', action='store_true',
                    help='run the fp32 CPU reference; needs ~4 bytes/parameter of host RAM')
    args = ap.parse_args()

    devices = probe_devices()
    report = {
        'recorded': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'platform': {'python': sys.version.split()[0], 'system': platform.platform()},
        'devices': devices,
    }
    if devices.get('runnable'):
        report['vllm'] = probe_vllm(args.model, args.tp)
        report['fp16_numerics'] = probe_fp16_numerics(args.model, args.fp32_ref)
    else:
        report['vllm'] = {'skipped': devices.get('reason')}
        report['fp16_numerics'] = {'skipped': devices.get('reason')}

    checks, blockers = [], []
    d, v, n = report['devices'], report['vllm'], report['fp16_numerics']
    if not d.get('runnable'):
        blockers.append(f"Gate not runnable here: {d.get('reason')}. Rerun on the cluster.")
    else:
        checks.append(f"{d['device_count']} devices, capability {d['devices'][0]['capability']}, "
                      f"{d['devices'][0]['total_memory_gb']} GB each")
        if not d['homogeneous']:
            blockers.append('Mixed compute capabilities; tensor parallelism assumes homogeneous devices')
        if d['bf16_supported']:
            checks.append('bf16 IS supported: the fp16-only premise in protocol v3 §9 can be relaxed')
        else:
            checks.append('bf16 unsupported, as expected on Volta; fp16 path confirmed necessary')
        if v.get('constructed'):
            checks.append(f"vLLM {v['version']} built at TP={v['tensor_parallel_size']}; "
                          f"{v['output_tokens_per_second']} output tok/s")
            # Protocol v3 §9 plans ~2000 aggregate tok/s across four TP=2 replicas.
            if v['output_tokens_per_second'] < 250:
                blockers.append(f"Throughput {v['output_tokens_per_second']} tok/s per replica is below the "
                                '~500 tok/s the episode budget assumes; re-cost or change backend')
            if v.get('any_empty'):
                blockers.append('Some sequences returned zero tokens; backend is not generating reliably')
        else:
            blockers.append(f"vLLM unusable: {v.get('error') or v.get('reason')}. "
                            'Fall back to SGLang, TGI, or transformers with manual batching')
        if n.get('runnable'):
            if n['fp16_nonfinite_logits']:
                blockers.append(f"{n['fp16_nonfinite_logits']} non-finite fp16 logits: this checkpoint "
                                'overflows in fp16 and must not be used')
            else:
                checks.append(f"fp16 logits all finite (max |logit| {n['fp16_max_abs_logit']})")
            if 'argmax_agreement' in n:
                checks.append(f"fp16-vs-fp32 argmax agreement {n['argmax_agreement']}, "
                              f"max |diff| {n['max_abs_logit_diff']}")
                if n['argmax_agreement'] < 0.98:
                    blockers.append(f"argmax agreement {n['argmax_agreement']} is low; fp16 is changing "
                                    'the sampled distribution enough to confound condition effects')
            else:
                blockers.append('No fp32 reference: the numerics risk is NOT retired. Rerun with --fp32-ref')

    report['checks'] = checks
    report['blockers'] = blockers
    report['gate_passed'] = bool(d.get('runnable')) and not blockers
    (OUT / 'hardware_gate.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')

    for c in checks:
        print(f'  ok      {c}')
    for b in blockers:
        print(f'  BLOCKER {b}')
    print(f"\ngate_passed={report['gate_passed']} -> results/phase3/hardware_gate.json")
    return 0 if report['gate_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
