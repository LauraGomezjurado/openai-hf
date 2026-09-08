"""Sequential local execution of the remaining frozen candidates; no remote work."""
import os,time,signal,subprocess,json,pathlib,urllib.request
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/opportunity_cost/v2'
def alive(pid):
 try:os.kill(pid,0);return True
 except ProcessLookupError:return False
def complete(model):
 d=D/model;g=json.loads((d/'gate.json').read_text());n=len((d/'rollouts.jsonl').read_text().splitlines());assert n==(86 if g['pass'] else 22)
 if g['pass']:assert len((d/'replays.jsonl').read_text().splitlines())==8
 print(model,'completed',g,flush=True)
def stop(pid):
 cmd=subprocess.check_output(['ps','-p',str(pid),'-o','command='],text=True)
 assert 'llama-server' in cmd and '18973' in cmd
 os.kill(pid,signal.SIGTERM)
 for _ in range(100):
  if not alive(pid):return
  time.sleep(.2)
 raise RuntimeError('Server did not stop')
if __name__=='__main__':
 while alive(89159):time.sleep(2)
 complete('qwen3');stop(89015)
 for model in ['qwen','smol']:
  with (D/f'{model}_server.log').open('w') as log:
   server=subprocess.Popen(['python3','scripts/serve_opportunity_cpu.py',model],cwd=R,stdout=log,stderr=subprocess.STDOUT)
   try:
    for _ in range(120):
     assert server.poll() is None
     try:
      with urllib.request.urlopen('http://127.0.0.1:18973/health',timeout=2) as resp:
       if json.load(resp)['status']=='ok':break
     except Exception:time.sleep(1)
    else:raise RuntimeError('Health timeout')
    (D/f'{model}_runtime.json').write_text((R/f'results/opportunity_cost/{model}_server.json').read_text())
    with (D/f'{model}_run.log').open('w') as runlog:subprocess.run(['python3','scripts/opportunity_allocation.py','run',model],cwd=R,stdout=runlog,stderr=subprocess.STDOUT,check=True)
    complete(model)
   finally:
    server.terminate();server.wait(timeout=30)
 (D/'execution_complete.json').write_text(json.dumps({'completed_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'models':['qwen3','qwen','smol'],'all_owned_servers_stopped':True},indent=2)+'\n')
