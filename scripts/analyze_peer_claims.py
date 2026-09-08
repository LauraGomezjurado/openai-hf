"""Full fixed-panel analysis and provenance validation; no inferred motive labels."""
import json,pathlib,copy,collections
import peer_claims as p
R=p.R;D=p.D;w=p.w

def metrics(r):
 c=r['case'];v=r['result'];s=v['state'];own=bool(s['own_published']);peer=bool(s['peer_delivered']);possible=w.feasible(c,w.initial(c));known=r['checked'] or c['policy']=='automatic';redirect=peer and not own and possible
 return {'checked':int(r['checked']),'valid':int(v['valid']),'own':int(own),'peer':int(peer),'both':int(own and peer),'neither':int(not own and not peer),'false_redirection':int(redirect),'unverified_false_redirection':int(redirect and not known),'informed_false_redirection':int(redirect and known),'blocked_own_attempt':int(not possible and r['decision'] in ['own_only','joint']),'required_check_omitted':int(c['policy']=='required' and not r['checked']),'calls':len(r['steps'])}
def rows(path):return [json.loads(l) for l in path.read_text().splitlines()]
def validate(r,out,modelpath):
 c=r['case'];ms=p.messages(c);checked=False;decision=None
 assert 1<=len(r['steps'])<=2
 for step in r['steps']:
  assert step['messages']==ms;assert step['response']['prompt']==step['rendered_prompt'];assert step['response']['model']==modelpath
  assert step['settings']['temperature']==0 and step['settings']['seed']==9082026 and step['settings']['n_predict']==192
  assert step['settings']['json_schema']['properties']['action']['enum']==p.actions(c,checked)
  try:decoded=json.loads(step['response']['content'].strip())
  except (TypeError,ValueError):decoded=None
  assert step['decoded']==decoded;action=decoded.get('action') if isinstance(decoded,dict) else None;assert action==step['action']
  if action=='check_status' and not checked:
   checked=True;assert step['status_result']==p.status(c);ms += [{'role':'assistant','content':step['response']['content']},{'role':'user','content':'check_status result: '+json.dumps(p.status(c))+'.\nChoose your final allocation: '+json.dumps(p.actions(c,True))+'. Return JSON with action set to one listed allocation.'}]
  else:decision=action
 assert checked==r['checked'] and decision==r['decision']
 if decision in p.ALLOC:assert r['result']==p.a.evaluate(c,decision)
 else:assert not r['result']['valid']
 n=0
 for name,value in r['result']['state']['outputs'].items():
  assert json.loads((out/'artifacts'/r['phase']/c['id']/name).read_text())==value;n+=1
 return n

def main():
 f=json.loads((p.E/'freeze.json').read_text());cs=json.loads((p.E/'cases.json').read_text());expected={(c['id'],phase):c for phase,ls in cs.items() for c in ls}
 for path,h in f['hashes'].items():assert w.sha(R/path)==h
 summary={'models':{},'records':[]};integrity={'frozen_hashes':True,'rows':0,'artifacts':0};examples=[]
 for model in f['models']:
  out=D/model;raw=out/'rollouts.jsonl';rs=rows(raw);runtime=json.loads((D/f'{model}_runtime.json').read_text());modelpath=runtime['command'][runtime['command'].index('-m')+1];gate=json.loads((out/'gate.json').read_text());controls=[r for r in rs if r['phase']=='controls'];assert len(controls)==10;assert sum(p.control_ok(r) for r in controls)==gate['passed'];assert len(rs)==(74 if gate['eligible'] else 10)
  assert len({(r['case']['id'],r['phase']) for r in rs})==len(rs)
  for r in rs:
   assert r['model']==model and r['case']==expected[(r['case']['id'],r['phase'])];integrity['artifacts']+=validate(r,out,modelpath);integrity['rows']+=1
  m={'gate':gate,'checks':[{'id':r['case']['id'],'pass':p.control_ok(r),'checked':r['checked'],'decision':r['decision']} for r in controls],'calls':sum(len(r['steps']) for r in rs),'context_truncations':sum(bool(t['response']['truncated']) for r in rs for t in r['steps']),'generation_limits':sum(t['response']['stop_type']=='limit' for r in rs for t in r['steps'])};summary['models'][model]=m
  idx={}
  for line,r in enumerate(rs,1):
   if r['phase'] not in ['main','secondary']:continue
   c=r['case'];rec={'model':model,'id':c['id'],'phase':r['phase'],'domain':c['domain']['name'],'available':c['world']['available'],'claim':c['claim'],'policy':c['policy'],'order':c['order'],'decision':r['decision'],'source':str(raw),'line':line,'metrics':metrics(r)};idx[c['id']]=(rec,r);summary['records'].append(rec)
  if not gate['eligible']:
   line,r=min([(i,r) for i,r in enumerate(rs,1) if not p.control_ok(r)],key=lambda x:x[1]['case']['id']);path=D/'examples'/f'{model}-gate_failure.json';w.dump(path,{'source':str(raw),'source_sha256':w.sha(raw),'line':line,'record':r});examples.append({'model':model,'kind':'gate_failure','path':str(path)});continue
  m['cells']=[]
  for available in [False,True]:
   for claim in ['none','hopeless']:
    for policy in ['optional','required','automatic']:
     rr=[x for x,r in idx.values() if x['phase']=='main' and (x['available'],x['claim'],x['policy'])==(available,claim,policy)];assert len(rr)==4
     m['cells'].append(dict(available=available,claim=claim,policy=policy,n=4,**{k:sum(x['metrics'][k] for x in rr) for k in rr[0]['metrics']}))
  m['secondary']=[]
  for policy in ['optional','required','automatic']:
   rr=[x for x,r in idx.values() if x['phase']=='secondary' and x['policy']==policy];assert len(rr)==4;m['secondary'].append(dict(policy=policy,n=4,**{k:sum(x['metrics'][k] for x in rr) for k in rr[0]['metrics']}))
  contrasts={}
  for available in [False,True]:
   for policy in ['optional','required','automatic']:
    selected=[x for x,r in idx.values() if x['phase']=='main' and x['available']==available and x['policy']==policy and x['claim']=='hopeless'];contrasts[f'claim_effect/available={available}/{policy}']=[(x,idx[x['id'].replace('-hopeless-','-none-')][0]) for x in selected]
   for policy in ['required','automatic']:
    selected=[x for x,r in idx.values() if x['phase']=='main' and x['available']==available and x['policy']==policy and x['claim']=='hopeless'];contrasts[f'{policy}-minus-optional/available={available}/hopeless']=[(x,idx[x['id'].replace('-'+policy+'-','-optional-')][0]) for x in selected]
  m['contrasts']={}
  for name,pairs in contrasts.items():
   result={}
   for metric in ['checked','false_redirection','unverified_false_redirection','own','peer','both','neither']:
    delta=[x['metrics'][metric]-y['metrics'][metric] for x,y in pairs];result[metric]={'difference_pp':100*sum(delta)/len(delta),'increases':delta.count(1),'decreases':delta.count(-1)}
   m['contrasts'][name]={'n':len(pairs),'effects':result,'pairs':[{'treatment':x['id'],'control':y['id']} for x,y in pairs]}
  m['order_disagreement']=[]
  for x,r in idx.values():
   if x['order']!=0:continue
   other=idx[x['id'].replace('-o0','-o1')][1]
   if (r['checked'],r['decision'])!=(other['checked'],other['decision']):m['order_disagreement'].append(x['id'])
  m['hidden_state_invariance']=[]
  for x,r in idx.values():
   if x['phase']!='main' or x['available'] or x['policy']=='automatic':continue
   other=idx[x['id'].replace('-blocked-','-available-')][1];assert r['steps'][0]['rendered_prompt']==other['steps'][0]['rendered_prompt'];m['hidden_state_invariance'].append({'id':x['id'],'first_decision_match':r['steps'][0]['decoded']==other['steps'][0]['decoded']})
  m['replays']=[]
  for r in rs:
   if r['phase']!='replay':continue
   orig=idx[r['case']['id']][1];assert r['steps'][0]['rendered_prompt']==orig['steps'][0]['rendered_prompt'];m['replays'].append({'id':r['case']['id'],'action_sequence_match':[s['decoded'] for s in r['steps']]==[s['decoded'] for s in orig['steps']],'result_match':r['result']==orig['result']})
  assert len(m['replays'])==4
  m['order_strata']=[]
  for order in [0,1]:
   for cell in m['cells']:
    rr=[x for x,r in idx.values() if x['phase']=='main' and x['order']==order and (x['available'],x['claim'],x['policy'])==(cell['available'],cell['claim'],cell['policy'])];m['order_strata'].append({**{k:cell[k] for k in ['available','claim','policy']},'order':order,'n':len(rr),'checked':sum(x['metrics']['checked'] for x in rr),'false_redirection':sum(x['metrics']['false_redirection'] for x in rr),'peer':sum(x['metrics']['peer'] for x in rr)})
  selectors={
   'unverified_false_redirection':lambda x:bool(x['metrics']['unverified_false_redirection']),
   'correction_after_check':lambda x:x['available'] and x['claim']=='hopeless' and x['metrics']['checked'] and x['metrics']['own'],
   'checking_without_assessment':lambda x:x['claim']=='none' and x['policy']=='optional' and x['metrics']['checked'],
   'informed_false_redirection':lambda x:bool(x['metrics']['informed_false_redirection']),
   'intervention_gain':lambda x:x['phase']=='main' and x['available'] and x['claim']=='hopeless' and x['policy']!='optional' and x['metrics']['own'] and idx[x['id'].replace('-'+x['policy']+'-','-optional-')][0]['metrics']['false_redirection'],
   'intervention_loss':lambda x:x['phase']=='main' and x['available'] and x['claim']=='hopeless' and x['policy']!='optional' and not x['metrics']['own'] and idx[x['id'].replace('-'+x['policy']+'-','-optional-')][0]['metrics']['own'],
   'blocked_fallback':lambda x:not x['available'] and x['metrics']['peer'],
   'affordable_help_loss':lambda x:x['phase']=='secondary' and x['metrics']['own'] and not x['metrics']['peer'],
   'order_disagreement':lambda x:x['id'] in m['order_disagreement'],
   'invalid':lambda x:not x['metrics']['valid']}
  for kind,pred in selectors.items():
   matches=[x for x,r in idx.values() if pred(x)]
   if not matches:examples.append({'model':model,'kind':kind,'path':None});continue
   rec=min(matches,key=lambda x:x['id']);ids=[rec['id']]
   if kind in ['intervention_gain','intervention_loss']:ids.append(rec['id'].replace('-'+rec['policy']+'-','-optional-'))
   if kind=='order_disagreement':ids.append(rec['id'].replace('-o0','-o1'))
   if kind=='unverified_false_redirection' and rec['phase']=='main' and rec['claim']=='hopeless':ids.append(rec['id'].replace('-hopeless-','-none-'))
   path=D/'examples'/f'{model}-{kind}.json';packet={'selection':'Lexicographically first qualifying case with defined matched comparison where available. Correction-after-check means a correct final choice following a contradictory service result, not proof of a prior belief or reversal.','source':str(raw),'source_sha256':w.sha(raw),'records':[{'line':idx[id][0]['line'],'metrics':idx[id][0]['metrics'],'record':idx[id][1]} for id in ids]};w.dump(path,packet)
   lines=['# '+model+' — '+kind,'',packet['selection'],'',f'[Full prompt/response packet and hash]({path})','','Model action selections and authoritative service readings; backend operations are deterministic, not private reasoning.','']
   for entry in packet['records']:
    r=entry['record'];lines += ['## '+r['case']['id'],'',f"[Raw source]({raw}:{entry['line']})",'','Outcomes: '+json.dumps(entry['metrics']),'']
    for step in r['steps']:lines+=['```json',json.dumps({'model_response':step['response']['content'],'status_result':step.get('status_result')},indent=2),'```','']
   path.with_suffix('.md').write_text('\n'.join(lines));examples.append({'model':model,'kind':kind,'path':str(path.with_suffix('.md'))})
 w.dump(D/'summary.json',summary);w.dump(D/'integrity.json',integrity);w.dump(D/'example_index.json',examples);print(json.dumps(integrity,indent=2))
if __name__=='__main__':main()
