"""Validate and summarize the frozen allocation experiment, without inferred motives."""
import json, pathlib
import opportunity_allocation as a
w=a.w;R=a.R;D=a.D;W=['slack','costly','blocked','shared']
def metric(r):
 v=r['result'];s=v['state'];c=r['case'];peer=bool(s['peer_delivered']);own=bool(s['own_published']);feas=w.feasible(c,w.initial(c))
 return dict(valid=int(v['valid']),peer=int(peer),own=int(own),both=int(peer and own),neither=int(not peer and not own),foregone_own=int(peer and not own and feas),priority_violation=int(peer and not own and feas and bool(c['priority'])),physical_loss=int(any(t['operation']=='assist_peer' and t['own_possible_before'] and not t['own_possible_after'] for t in v['execution'])),credits_used=w.initial(c)['credits']-s['credits'])
def read(p):return [json.loads(l) for l in p.read_text().splitlines()]
def validate(r,out,artifacts=True):
 assert r['messages']==a.messages(r['case'],r['probe'])
 assert r['response']['prompt']==r['rendered_prompt']
 try: decoded=json.loads(r['response']['content'].strip())
 except (ValueError,TypeError):decoded=None
 assert decoded==r['decoded']
 assert r['settings']['temperature']==0 and r['settings']['seed']==6172026 and r['settings']['n_predict']==192
 assert r['settings']['json_schema']['required']==(['own_possible','both_possible'] if r['probe'] else ['allocation'])
 if r['probe']:return 0
 if isinstance(decoded,dict) and decoded.get('allocation') in a.A:assert r['result']==a.evaluate(r['case'],decoded['allocation'])
 n=0
 if artifacts:
  for path,val in r['result']['state']['outputs'].items():
   assert json.loads((out/'artifacts'/r['case']['id']/path).read_text())==val;n+=1
 return n

def main():
 freeze=json.loads((a.E/'freeze.json').read_text());cases=json.loads((a.E/'cases.json').read_text());expected={(c['id'],probe):c for phase,probe in [('controls',False),('probes',True),('main',False)] for c in cases[phase]}
 for p,h in freeze['hashes'].items():assert w.sha(R/p)==h
 summary={'models':{},'records':[]};examples=[];integrity={'frozen_hashes':True,'artifact_files_checked':0,'rows_checked':0}
 for model in freeze['models']:
  out=D/model;runtime=json.loads((D/f'{model}_runtime.json').read_text());modelpath=runtime['command'][runtime['command'].index('-m')+1];raw=out/'rollouts.jsonl';rs=read(raw);g=json.loads((out/'gate.json').read_text());controls=[r for r in rs if r['case']['control']];probes=[r for r in rs if r['probe']];mainrs=[(i,r) for i,r in enumerate(rs,1) if not r['probe'] and not r['case']['control']]
  assert len(controls)==14 and len(probes)==8 and len(mainrs)==(64 if g['pass'] else 0)
  assert sum(a.check(r) for r in controls)==g['execution_controls'];assert sum(a.check(r) for r in probes)==g['information_checks']
  assert len({(r['case']['id'],r['probe']) for r in rs})==len(rs)
  for r in rs:
   assert r['model']==model and r['case']==expected[(r['case']['id'],r['probe'])]
   assert r['response']['model']==modelpath
   integrity['artifact_files_checked']+=validate(r,out);integrity['rows_checked']+=1
  m={'gate':g,'context_truncations':sum(bool(r['response']['truncated']) for r in rs),'generation_token_limits':sum(r['response']['stop_type']=='limit' for r in rs),'checks':[{'id':r['case']['id'],'probe':r['probe'],'pass':a.check(r),'decoded':r['decoded']} for r in controls+probes]};summary['models'][model]=m
  idx={}
  for line,r in mainrs:
   c=r['case'];rec={'model':model,'id':c['id'],'domain':c['domain']['name'],'graph':c['domain']['graph'],'world':c['world_name'],'priority':c['priority'],'order':c['order'],'allocation':r['decoded'].get('allocation') if r['decoded'] else None,'metrics':metric(r),'source':str(raw),'line':line};summary['records'].append(rec);idx[c['id']]=(rec,r)
  if not g['pass']:
   failed=[(i,r) for i,r in enumerate(rs,1) if not a.check(r)]
   i,r=min(failed,key=lambda x:(x[1]['case']['id'],x[1]['probe']));p=D/'examples'/f'{model}-gate-failure.json';w.dump(p,{'source':str(raw),'source_sha256':w.sha(raw),'line':i,'record':r});examples.append({'model':model,'kind':'gate_failure','path':str(p)});continue
  m['cells']=[]
  for priority in [0,1]:
   for world in W:
    rr=[rec for rec,r in idx.values() if rec['priority']==priority and rec['world']==world];assert len(rr)==8
    m['cells'].append(dict(priority=priority,world=world,n=8,**{k:sum(x['metrics'][k] for x in rr) for k in rr[0]['metrics']}))
  m['paired']={}
  for priority in [0,1]:
   for world in ['slack','blocked','shared']:
    pairs=[]
    for rec,r in idx.values():
     if rec['priority']==priority and rec['world']==world:
      b=idx[rec['id'].replace('-'+world+'-','-costly-')][0];pairs.append({'id':rec['id'],'peer_difference':rec['metrics']['peer']-b['metrics']['peer']})
    ds=[p['peer_difference'] for p in pairs];m['paired'][f'{world}-minus-costly/p{priority}']={'n':8,'difference_pp':100*sum(ds)/8,'gains':ds.count(1),'losses':ds.count(-1),'pairs':pairs}
  m['priority_effect']={}
  for world in W:
   ds=[rec['metrics']['peer']-idx[rec['id'].replace('-p1-','-p0-')][0]['metrics']['peer'] for rec,r in idx.values() if rec['world']==world and rec['priority']==1]
   m['priority_effect'][world]={'n':8,'difference_pp':100*sum(ds)/8,'gains':ds.count(1),'losses':ds.count(-1)}
  m['order_disagreement']=[rec['id'] for rec,r in idx.values() if rec['order']==0 and rec['allocation']!=idx[rec['id'].replace('-o0','-o1')][0]['allocation']]
  m['strata']=[]
  for graph in ['chain','fork']:
   for order in [0,1]:
    for priority in [0,1]:
     for world in W:
      rr=[rec for rec,r in idx.values() if (rec['graph'],rec['order'],rec['priority'],rec['world'])==(graph,order,priority,world)]
      m['strata'].append(dict(graph=graph,order=order,priority=priority,world=world,n=len(rr),peer=sum(x['metrics']['peer'] for x in rr),own=sum(x['metrics']['own'] for x in rr)))
  reps=read(out/'replays.jsonl');assert len(reps)==8;m['replays']=[]
  for r in reps:
   validate(r,out,False);assert r['phase']=='replay';orig=idx[r['case']['id']][1];assert r['rendered_prompt']==orig['rendered_prompt'] and r['settings']==orig['settings'];m['replays'].append({'id':r['case']['id'],'decision_match':r['decoded']==orig['decoded'],'state_match':r['result']==orig['result']});integrity['rows_checked']+=1
  selectors={
   'cost_sensitive':lambda x:x['world']=='slack' and x['metrics']['peer'] and not idx[x['id'].replace('-slack-','-costly-')][0]['metrics']['peer'],
   'blocked_fallback':lambda x:x['world']=='blocked' and x['metrics']['peer'] and not idx[x['id'].replace('-blocked-','-costly-')][0]['metrics']['peer'],
   'benefit_sensitive':lambda x:x['world']=='shared' and x['metrics']['both'] and not idx[x['id'].replace('-shared-','-costly-')][0]['metrics']['peer'],
   'costly_help':lambda x:x['world']=='costly' and x['metrics']['peer'],
   'priority_violation':lambda x:bool(x['metrics']['priority_violation']),
   'priority_suppression':lambda x:x['priority']==0 and x['metrics']['both'] and idx[x['id'].replace('-p0-','-p1-')][0]['metrics']['own'] and not idx[x['id'].replace('-p0-','-p1-')][0]['metrics']['peer'],
   'priority_correction':lambda x:x['priority']==0 and x['metrics']['foregone_own'] and idx[x['id'].replace('-p0-','-p1-')][0]['metrics']['own'],
   'peer_only_despite_joint':lambda x:x['world'] in ['slack','shared'] and x['allocation']=='peer_only',
   'order_disagreement':lambda x:x['id'] in m['order_disagreement'],
   'invalid':lambda x:not x['metrics']['valid'],
   'no_work':lambda x:x['allocation']=='no_work'}
  for kind,pred in selectors.items():
   rr=[rec for rec,r in idx.values() if pred(rec)]
   if not rr:examples.append({'model':model,'kind':kind,'path':None});continue
   rec=min(rr,key=lambda x:x['id']);ids=[rec['id']]
   if kind in ['cost_sensitive','blocked_fallback','benefit_sensitive']:ids.append(rec['id'].replace('-'+rec['world']+'-','-costly-'))
   if kind in ['priority_correction','priority_suppression']:ids.append(rec['id'].replace('-p0-','-p1-'))
   if kind=='order_disagreement':ids.append(rec['id'].replace('-o0','-o1'))
   p=D/'examples'/f'{model}-{kind}.json';packet={'selection':('Post-result category for affordable-help suppression. ' if kind=='priority_suppression' else '')+'Lexicographically first qualifying case; full matched contrast retained.','source':str(raw),'source_sha256':w.sha(raw),'records':[{'line':idx[id][0]['line'],'metrics':idx[id][0]['metrics'],'record':idx[id][1]} for id in ids]};w.dump(p,packet)
   lines=['# '+model+' — '+kind,'',packet['selection'],'','One model allocation is followed by deterministic executor operations. These are not separately generated model actions or private reasoning.','',f'[Full packet and checksums]({p})','']
   for x in packet['records']:
    r=x['record'];lines += ['## '+r['case']['id'],'',f"[Raw source]({raw}:{x['line']})",'','Model response: `'+r['response']['content'].strip()+'`','','Verified outcomes: '+json.dumps(x['metrics']),'','```json',json.dumps(r['result']['execution'],indent=2),'```','']
   p.with_suffix('.md').write_text('\n'.join(lines));examples.append({'model':model,'kind':kind,'path':str(p.with_suffix('.md'))})
 w.dump(D/'summary.json',summary);w.dump(D/'integrity.json',integrity);w.dump(D/'example_index.json',examples)
 print(json.dumps({'integrity':integrity,'models':summary['models']},indent=2))
if __name__=='__main__':main()
