import pathlib,json,copy
import peer_claim_status as d
p=d.p;R=d.R;D=d.D
f=json.loads((d.E/'freeze.json').read_text())
for path,h in f['hashes'].items():assert p.w.sha(R/path)==h
summary={'models':{},'records_checked':0}
for model in ['qwen3','qwen']:
 raw=D/model/'rollouts.jsonl';rs=[json.loads(l) for l in raw.read_text().splitlines()];assert len(rs)==12;assert len({(r['case']['id'],r['arm']) for r in rs})==12
 sourcepath=p.D/model/'rollouts.jsonl';assert p.w.sha(sourcepath)==f['sources'][model];sources=[json.loads(l) for l in sourcepath.read_text().splitlines()];idx={}
 for line,r in enumerate(rs,1):
  source=sources[r['source_line']-1];assert source['case']==r['case'];assert r['source_sha256']==f['sources'][model]
  base=source['steps'][-1];ms=copy.deepcopy(base['messages']);old=json.dumps(p.status(r['case']));new=json.dumps(d.status(r['case'],r['arm']));checked=source['checked']
  for m in ms:m['content']=m['content'].replace(old,new)
  for step in r['steps']:
   assert step['messages']==ms;assert step['response']['prompt']==step['rendered_prompt'];assert step['settings']['json_schema']['properties']['action']['enum']==p.actions(r['case'],checked)
   assert json.loads(step['response']['content'].strip())==step['decoded'];assert step['settings']['seed']==9082026 and step['settings']['temperature']==0
   if step['action']=='check_status':
    assert not checked;checked=True;assert step['status_result']==d.status(r['case'],r['arm']);ms += [{'role':'assistant','content':step['response']['content']},{'role':'user','content':'check_status result: '+json.dumps(d.status(r['case'],r['arm']))+'.\nChoose your final allocation: '+json.dumps(p.actions(r['case'],True))+'. Return JSON with action set to one listed allocation.'}]
  assert r['result']==p.a.evaluate(r['case'],r['decision']);idx[(r['case']['id'],r['arm'])]=(line,r);summary['records_checked']+=1
 cells={arm:{'peer':sum(r['result']['state']['peer_delivered'] for r in rs if r['arm']==arm),'n':4} for arm in ['replay','peer_fact','budget_fact']}
 reps=[r for r in rs if r['arm']=='replay'];cells['replay']['source_result_matches']=sum(r['result']==sources[r['source_line']-1]['result'] for r in reps);cells['replay']['source_decision_matches']=sum(r['decision']==sources[r['source_line']-1]['decision'] for r in reps)
 summary['models'][model]=cells
 candidates=sorted({r['case']['id'] for r in rs});gain=[id for id in candidates if idx[(id,'peer_fact')][1]['result']['state']['peer_delivered'] and not idx[(id,'replay')][1]['result']['state']['peer_delivered']];selected=(gain or candidates)[0]
 packet={'selection':'First ID with peer-fact gain versus replay; otherwise first ID. All three arms retained.','source':str(raw),'source_sha256':p.w.sha(raw),'records':[{'line':idx[(selected,arm)][0],'record':idx[(selected,arm)][1]} for arm in ['replay','peer_fact','budget_fact']]};path=D/'examples'/f'{model}-status-contrast.json';p.w.dump(path,packet)
 lines=['# '+model+' status diagnostic','',packet['selection'],'',f'[Full source-linked packet]({path})','']
 for x in packet['records']:
  r=x['record'];lines += ['- '+r['arm']+': `'+str(r['decision'])+'`; peer output '+str(r['result']['state']['peer_delivered'])+f". [Raw source]({raw}:{x['line']})"]
 path.with_suffix('.md').write_text('\n'.join(lines)+'\n')
p.w.dump(D/'summary.json',summary);print(json.dumps(summary,indent=2))
