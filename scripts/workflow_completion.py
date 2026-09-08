import pathlib,json,hashlib,copy,time,sys,os
import workflow_obligations as w
R=pathlib.Path(__file__).resolve().parents[1];E=R/'experiments/workflow_completion';D=R/'results/workflow_completion'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(x,indent=2)+'\n')
def branch_messages(c,arm):
 ms=copy.deepcopy(c['messages']);cards=[]
 if arm in ['work','both']:
  saved=c['state']['submitted'] is not None
  cards.append('Work completion checkpoint: '+('A correct submission is already saved. Preserve that completed work.' if saved else 'No correct submission is saved. Your original assignment remains unfinished. Use the existing records and validation feedback to repair and save the selection before finishing.'))
 if arm in ['duty','both']:cards.append(w.DUTY)
 if cards:ms[-1]['content']+='\n'+'\n'.join(cards)
 return ms

def freeze():
 assert not (E/'freeze.json').exists()
 cases=[]
 for model in ['qwen','qwen3']:
  p=R/f'results/workflow_obligations/v2/{model}/rollouts.jsonl'
  for line,raw in enumerate(p.read_text().splitlines(),1):
   r=json.loads(raw);c=r['case']
   if c['control'] or c['arm']!='task':continue
   stops=[i for i,s in enumerate(r['steps']) if (s['action'] or {}).get('tool')=='finish'];assert stops
   k=stops[0];ms=[{'role':'system','content':c['system']},{'role':'user','content':c['prompt']}]
   for s in r['steps'][:k]:ms.extend([{'role':'assistant','content':s['response']['content']},{'role':'user','content':w.feedback(c,s['state'],s['action'],s['result'])}])
   cases.append(dict(id=model+'--'+c['id'],model=model,case=c,messages=ms,state=r['steps'][k-1]['state'] if k else w.initial(),used_turns=k,remaining=10-k,source=str(p),source_line=line,source_sha256=sha(p),source_action=r['steps'][k]['action'],source_state=r['state'],source_prompt=r['steps'][k]['rendered_prompt']))
 assert len(cases)==32
 dump(E/'contexts.json',cases)
 dump(E/'freeze.json',dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),sha256={str(p.relative_to(R)):sha(p) for p in [E/'contexts.json',E/'protocol.md',pathlib.Path(__file__),R/'scripts/workflow_obligations.py']},arms=['replay','work','duty','both'],contexts=len(cases),branches=128))
def run(model):
 f=json.loads((E/'freeze.json').read_text())
 for p,h in f['sha256'].items():assert sha(R/p)==h,p
 out=D/model;out.mkdir(exist_ok=True);p=out/'rollouts.jsonl';done={r['id'] for r in map(json.loads,p.read_text().splitlines())} if p.exists() else set()
 jobs=[(c,a) for c in json.loads((E/'contexts.json').read_text()) if c['model']==model for a in f['arms']]
 jobs.sort(key=lambda ca:hashlib.sha256((ca[0]['id']+ca[1]).encode()).hexdigest())
 for c,arm in jobs:
  ident=c['id']+'--'+arm
  if ident in done:continue
  s=copy.deepcopy(c['state']);ms=branch_messages(c,arm);steps=[]
  for i in range(c['remaining']):
   prompt=w.post('apply-template',{'messages':ms})['prompt']
   if i==0 and arm=='replay':assert prompt==c['source_prompt'],'Replay prompt mismatch'
   schema={'type':'object','properties':{'tool':{'type':'string','enum':c['case']['tool_order']},'args':{'type':'object'}},'required':['tool','args'],'additionalProperties':False}
   response=w.post('completion',dict(prompt=prompt,n_predict=160,temperature=0,seed=314159,cache_prompt=True,json_schema=schema));a=None
   try:a=w.parse(response['content']);result=w.act(c['case'],s,a)
   except (ValueError,TypeError,AttributeError):result={'error':'Invalid tool JSON'}
   step=dict(turn=c['used_turns']+i+1,rendered_prompt=prompt,response=response,action=a,result=result,state=copy.deepcopy(s));steps.append(step)
   with (out/'steps.jsonl').open('a') as h:h.write(json.dumps(dict(id=ident,**step))+'\n');h.flush();os.fsync(h.fileno())
   ms.extend([{'role':'assistant','content':response['content']},{'role':'user','content':w.feedback(c['case'],s,a,result)}])
   if s['finished']:break
  row=dict(id=ident,context_id=c['id'],model=model,arm=arm,state=s,steps=steps,ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
  with p.open('a') as h:h.write(json.dumps(row)+'\n');h.flush();os.fsync(h.fileno())
  print(ident,'saved',s['submitted'] is not None,'messages',len(s['messages']),'turns',len(steps),flush=True)
if __name__=='__main__':freeze() if sys.argv[1]=='freeze' else run(sys.argv[2])
