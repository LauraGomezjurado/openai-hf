"""Sequential owned local CPU runs; stops each server even on runner failure."""
import pathlib,json,subprocess,urllib.request,time,os,signal
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/peer_claims'
def ready():
 for _ in range(120):
  try:
   with urllib.request.urlopen('http://127.0.0.1:18973/health',timeout=2) as h:
    if json.load(h)['status']=='ok':return
  except Exception:time.sleep(1)
 raise RuntimeError('Server not ready')
def run(model):
 ready();runtime=json.loads((R/f'results/opportunity_cost/{model}_server.json').read_text());(D/f'{model}_runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
 try:
  with (D/f'{model}_run.log').open('w') as log:subprocess.run(['python3','scripts/peer_claims.py','run',model],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
  g=json.loads((D/model/'gate.json').read_text());n=len((D/model/'rollouts.jsonl').read_text().splitlines());assert n==(74 if g['eligible'] else 10);print(model,g,'records',n,flush=True)
 finally:
  pid=runtime['pid'];cmd=subprocess.check_output(['ps','-p',str(pid),'-o','command='],text=True);assert 'llama-server' in cmd and '18973' in cmd;os.kill(pid,signal.SIGTERM)
if __name__=='__main__':
 run('qwen3')
 time.sleep(2)
 with (D/'qwen_server.log').open('w') as log:
  server=subprocess.Popen(['python3','scripts/serve_opportunity_cpu.py','qwen'],cwd=R,stdout=log,stderr=subprocess.STDOUT)
  try:run('qwen')
  finally:
   if server.poll() is None:server.terminate()
   server.wait(timeout=30)
 (D/'execution_complete.json').write_text(json.dumps({'completed_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'models':['qwen3','qwen'],'owned_servers_stopped':True},indent=2)+'\n')
