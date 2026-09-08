import pathlib,subprocess,json,urllib.request,time
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/peer_claim_status'
for model in ['qwen3','qwen']:
 with (D/f'{model}_server.log').open('w') as log:
  server=subprocess.Popen(['python3','scripts/serve_opportunity_cpu.py',model],cwd=R,stdout=log,stderr=subprocess.STDOUT)
  try:
   for _ in range(120):
    assert server.poll() is None
    try:
     with urllib.request.urlopen('http://127.0.0.1:18973/health',timeout=2) as h:
      if json.load(h)['status']=='ok':break
    except Exception:time.sleep(1)
   else:raise RuntimeError('Not ready')
   (D/f'{model}_runtime.json').write_text((R/f'results/opportunity_cost/{model}_server.json').read_text())
   with (D/f'{model}_run.log').open('w') as out:subprocess.run(['python3','scripts/peer_claim_status.py','run',model],cwd=R,stdout=out,stderr=subprocess.STDOUT,check=True)
  finally:server.terminate();server.wait(timeout=30)
 (D/f'{model}_complete.json').write_text(json.dumps({'completed':True})+'\n')
