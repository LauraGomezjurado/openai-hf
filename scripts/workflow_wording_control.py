import pathlib,json,hashlib,copy,time,sys,os
import workflow_completion as p
import workflow_obligations as w
R=p.R;E=p.E/'wording_control';D=p.D/'wording_control'
def freeze():
 assert not (E/'freeze.json').exists()
 cs=[c for c in json.loads((p.E/'contexts.json').read_text()) if c['model']=='qwen'];original={r['context_id']:r for r in map(json.loads,(p.D/'qwen/rollouts.jsonl').read_text().splitlines()) if r['arm']=='work'}
 chosen={min([c for c in cs if c['case']['evidence']==e and c['case']['pressure']==v],key=lambda c:c['id'])['id'] for e in ['unauthorized','authorized'] for v in [0,1]}
 jobs=[]
 for c in cs:
  for arm in (['retain','original'] if c['id'] in chosen else ['retain']):
   ms=p.branch_messages(c,'work');assert 'Preserve that completed work.' in ms[-1]['content']
   if arm=='retain':ms[-1]['content']=ms[-1]['content'].replace('Preserve that completed work.','Retain that completed work.')
   jobs.append(dict(id=c['id']+'--'+arm,arm=arm,context=c,messages=ms,original_work=original[c['id']]))
 p.dump(E/'jobs.json',jobs);p.dump(E/'freeze.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'n':20,'hashes':{str(x.relative_to(R)):p.sha(x) for x in [E/'jobs.json',E/'protocol.md',pathlib.Path(__file__),R/'scripts/workflow_completion.py',R/'scripts/workflow_obligations.py',p.D/'qwen/rollouts.jsonl']}})
def run():
 f=json.loads((E/'freeze.json').read_text())
 for path,h in f['hashes'].items():assert p.sha(R/path)==h
 dest=D/'rollouts.jsonl';done={r['id'] for r in map(json.loads,dest.read_text().splitlines())} if dest.exists() else set()
 for job in sorted(json.loads((E/'jobs.json').read_text()),key=lambda j:hashlib.sha256(j['id'].encode()).hexdigest()):
  if job['id'] in done:continue
  c=job['context'];ms=copy.deepcopy(job['messages']);s=copy.deepcopy(c['state']);steps=[]
  for i in range(c['remaining']):
   prompt=w.post('apply-template',{'messages':ms})['prompt']
   if i==0 and job['arm']=='original':assert prompt==job['original_work']['steps'][0]['rendered_prompt']
   schema={'type':'object','properties':{'tool':{'type':'string','enum':c['case']['tool_order']},'args':{'type':'object'}},'required':['tool','args'],'additionalProperties':False}
   response=w.post('completion',dict(prompt=prompt,n_predict=160,temperature=0,seed=314159,cache_prompt=True,json_schema=schema));a=None
   try:a=w.parse(response['content']);result=w.act(c['case'],s,a)
   except (ValueError,TypeError,AttributeError):result={'error':'Invalid tool JSON'}
   step=dict(turn=c['used_turns']+i+1,rendered_prompt=prompt,response=response,action=a,result=result,state=copy.deepcopy(s));steps.append(step)
   with (D/'steps.jsonl').open('a') as h:h.write(json.dumps(dict(id=job['id'],**step))+'\n');h.flush();os.fsync(h.fileno())
   ms.extend([{'role':'assistant','content':response['content']},{'role':'user','content':w.feedback(c['case'],s,a,result)}])
   if s['finished']:break
  row=dict(id=job['id'],arm=job['arm'],state=s,steps=steps,ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
  with dest.open('a') as h:h.write(json.dumps(row)+'\n');h.flush();os.fsync(h.fileno())
  print(job['id'],len(steps),flush=True)
if __name__=='__main__':freeze() if sys.argv[1]=='freeze' else run()
