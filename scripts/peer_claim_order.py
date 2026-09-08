"""Post-result control diagnostic; not a preference experiment."""
import json,pathlib,copy,sys,time,os,hashlib
import peer_claims_v2 as p
R=p.R;E=R/'experiments/peer_claim_order';D=R/'results/peer_claim_order'
def status(c,arm):
 s=p.status(c)
 return dict(reversed(list(s.items()))) if arm=='reverse_fields' else s
def execute(source,model,arm,line,sha):
 c=source['case'];base=source['steps'][-1];checked=bool(source['checked']);ms=copy.deepcopy(base['messages']);old=json.dumps(p.status(c));new=json.dumps(status(c,arm));n=0
 for m in ms:
  n+=m['content'].count(old);m['content']=m['content'].replace(old,new)
 assert n>0
 steps=[];decision=None
 for _ in range(2):
  step=p.generate(ms,c,checked);steps.append(step);d=step['decoded'];action=d.get('action') if isinstance(d,dict) else None;step['action']=action
  if action=='check_status' and not checked:
   checked=True;step['status_result']=status(c,arm);ms += [{'role':'assistant','content':step['response']['content']},{'role':'user','content':'check_status result: '+json.dumps(status(c,arm))+'.\nChoose your final allocation: '+json.dumps(p.actions(c,True))+'. Return JSON with action set to one listed allocation.'}];continue
  decision=action;break
 result=p.a.evaluate(c,decision) if decision in p.ALLOC else {'valid':False,'state':p.w.initial(c),'execution':[]}
 return {'model':model,'case':c,'arm':arm,'source_line':line,'source_sha256':sha,'source_path':str(p.D/model/'rollouts.jsonl'),'steps':steps,'decision':decision,'result':result,'ended_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
def freeze():
 assert not (E/'freeze.json').exists();sources={m:p.w.sha(p.D/m/'rollouts.jsonl') for m in ['qwen3']}
 p.w.dump(E/'freeze.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'sources':sources,'hashes':{str(x.relative_to(R)):p.w.sha(x) for x in [pathlib.Path(__file__),R/'scripts/peer_claims.py',E/'protocol.md']}})
def run(model):
 f=json.loads((E/'freeze.json').read_text())
 for path,h in f['hashes'].items():assert p.w.sha(R/path)==h
 raw=p.D/model/'rollouts.jsonl';assert p.w.sha(raw)==f['sources'][model];sources=[(i,r) for i,r in enumerate(map(json.loads,raw.read_text().splitlines()),1) if r['phase']=='main' and r['case']['world']['available'] and r['case']['claim']=='none' and r['case']['policy'] in ['required','automatic']];assert len(sources)==8
 out=D/model;out.mkdir(exist_ok=True);path=out/'rollouts.jsonl';done={(r['case']['id'],r['arm']) for r in map(json.loads,path.read_text().splitlines())} if path.exists() else set()
 jobs=sorted([(i,r,arm) for i,r in sources for arm in ['replay','reverse_fields']],key=lambda x:hashlib.sha256((x[1]['case']['id']+x[2]).encode()).hexdigest())
 for i,source,arm in jobs:
  if (source['case']['id'],arm) in done:continue
  r=execute(source,model,arm,i,f['sources'][model])
  with path.open('a') as h:h.write(json.dumps(r)+'\n');h.flush();os.fsync(h.fileno())
  print(source['case']['id'],arm,r['decision'],flush=True)
if __name__=='__main__':freeze() if sys.argv[1]=='freeze' else run(sys.argv[2])
