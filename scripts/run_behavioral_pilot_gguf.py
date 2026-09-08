"""Use an explicitly CPU-only local llama.cpp server; no external inference API."""
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from run_behavioral_pilot_semantic import ROOT,cases,execute,digest


def main():
 from transformers import AutoTokenizer
 source=json.loads((ROOT/'experiments/behavioral_pilot/gguf_source.json').read_text())
 modeldir=Path.home()/'.cache/huggingface/hub'/('models--'+source['repository'].replace('/','--'))/'snapshots'/source['revision']
 out=ROOT/'results/behavioral_pilot/v3-7b'; out.mkdir(parents=True,exist_ok=True)
 dest=out/'rollouts-7B.jsonl'; assert not dest.exists()
 rows=cases(); (out/'cases.json').write_text(json.dumps(rows,indent=2)+'\n')
 tokenizer_path=Path.home()/'.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28'
 tok=AutoTokenizer.from_pretrained(tokenizer_path,local_files_only=True)
 meta=dict(model=source,weights={f:digest(modeldir/f) for f in source['files']},
           backend='llama.cpp',device='cpu',quantization='Q4_K_M',temperature=0,max_new_tokens=40,
           tokenizer_revision=tokenizer_path.name,tokenizer_config_sha256=digest(tokenizer_path/'tokenizer_config.json'),
           protocol_sha256=digest(ROOT/'experiments/behavioral_pilot/protocol_7b.md'),
           runner_sha256=digest(Path(__file__)),cases_sha256=digest(out/'cases.json'),
           backend_version=subprocess.run(['llama-server','--version'],capture_output=True,text=True).stdout)
 (out/'metadata-7B.json').write_text(json.dumps(meta,indent=2)+'\n')
 for i,c in enumerate(rows):
  prompt=tok.apply_chat_template(c['messages'],tokenize=False,add_generation_prompt=True)
  payload=dict(prompt=prompt,n_predict=40,temperature=0,seed=271828,cache_prompt=False)
  req=urllib.request.Request('http://127.0.0.1:18973/completion',
       data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
  t=time.monotonic()
  with urllib.request.urlopen(req,timeout=120) as response: result=json.load(response)
  raw=result['content']
  record=dict(case=c,raw_output=raw,seconds=time.monotonic()-t,
              backend_response=result,outcome=execute(c,raw))
  with dest.open('a') as f:f.write(json.dumps(record)+'\n')
  print(f'7B {i+1}/52 {c["id"]}: {raw!r} ({record["seconds"]:.1f}s)',flush=True)


if __name__=='__main__':main()
