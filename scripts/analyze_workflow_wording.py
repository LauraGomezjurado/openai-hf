import json,pathlib
import workflow_completion as p
import workflow_wording_control as e
import workflow_obligations as w
R=p.R;D=e.D;E=e.E
f=json.loads((E/'freeze.json').read_text())
for path,h in f['hashes'].items():assert p.sha(R/path)==h
jobs={j['id']:j for j in json.loads((E/'jobs.json').read_text())};rows=[json.loads(l) for l in (D/'rollouts.jsonl').read_text().splitlines()];assert len(rows)==20 and len({r['id'] for r in rows})==20
records=[];checks=[]
def metrics(c,r):
 bad=sum((s['action'] or {}).get('tool')=='preserve' and 'error' in s['result'] for s in r['steps']);msgs=[m for m in r['state']['messages'] if m['recipient']=='overseer'];initial=sum(m['recipient']=='overseer' for m in c['state']['messages'])
 return dict(invalid_preserve=bad,any_error=any('error' in s['result'] for s in r['steps']),correct_completion=w.success(c['case'],r['state']) and r['state']['finished'],steps=len(r['steps']),new_overseer=len(msgs)-initial,artifact_receipt=any(c['case']['artifact'] in m['body'] for m in msgs))
for line,r in enumerate(rows,1):
 j=jobs[r['id']];c=j['context'];assert len(r['steps'])<=c['remaining'];assert r['state']==r['steps'][-1]['state']
 if r['arm']=='original':checks.append(dict(id=r['id'],prompt_match=r['steps'][0]['rendered_prompt']==j['original_work']['steps'][0]['rendered_prompt'],first_action_match=r['steps'][0]['action']==j['original_work']['steps'][0]['action'],state_match=r['state']==j['original_work']['state']))
 else:records.append(dict(id=r['id'],evidence=c['case']['evidence'],family=c['case']['family'],line=line,original=metrics(c,j['original_work']),retain=metrics(c,r)))
assert len(records)==16 and len(checks)==4
s={'checks':checks,'records':records,'calls':sum(len(r['steps']) for r in rows),'counts':{a:{k:sum(r[a][k] for r in records) for k in records[0][a]} for a in ['original','retain']},'limits':['Post-result single-word diagnostic, not an independent replication of the full checkpoint study.','Only Qwen2.5 work-only saved-state contexts; combined-card and unsaved-state cards not tested.','Sixteen related deterministic contexts; no population inference.']}
p.dump(D/'summary.json',s)
selected=[]
for kind,predicate in [('error_removed',lambda r:r['original']['invalid_preserve']>0 and r['retain']['invalid_preserve']==0),('error_persists',lambda r:r['retain']['invalid_preserve']>0),('new_error_type',lambda r:r['retain']['any_error'] and r['retain']['invalid_preserve']==0)]:
 candidates=[r for r in records if predicate(r)]
 if not candidates:selected.append({'kind':kind,'selected':None});continue
 rec=min(candidates,key=lambda r:r['id']);j=jobs[rec['id']];r=rows[rec['line']-1];file=D/f'example-{kind}.json';p.dump(file,dict(selection='Lexicographically first context ID in the named diagnostic outcome class.',job=j,new_result=r,metrics=rec,source=str(D/'rollouts.jsonl'),line=rec['line'],source_sha256=p.sha(D/'rollouts.jsonl')));selected.append({'kind':kind,'selected':rec['id'],'path':str(file)})
p.dump(D/'example_index.json',selected)
lines=['# Single-word diagnostic of the completion card','','Status: all20 branches complete; primary results remain unchanged. This diagnostic was frozen after seeing the primary error pattern.','',f"Original-work replay controls: {sum(c['state_match'] for c in checks)}/4 final states, {sum(c['first_action_match'] for c in checks)}/4 first actions.",'','All16 Qwen2.5 saved-work contexts:','']
for a,v in s['counts'].items():lines += [f"- {a}: invalid preserve calls {v['invalid_preserve']}; contexts with any error {v['any_error']}/16; correct completion {v['correct_completion']}/16; total continuation turns {v['steps']}; new overseer messages {v['new_overseer']}; artifact-ID receipts {v['artifact_receipt']}."]
lines += ['','The intervention changes only the saved-work sentence from “Preserve that completed work” to “Retain that completed work.” All other prefix text, state, budget, tools and decoding are fixed. Receipt counts include earlier messages; new messages are shown separately.','',f"[Full results]({D/'summary.json'}) · [Frozen protocol]({E/'protocol.md'})",'','## Examples','']
for x in selected:lines += [f"- {x['kind']}: "+(f"[paired source and trajectory]({x['path']})" if x['selected'] else 'no case in this diagnostic.')]
lines += ['','This tests one lexical substitution, not all equivalent wordings, internal representations or general reliability. It does not validate the combined-card intervention; no further wording search was run.']
(R/'docs/workflow_wording_results.md').write_text('\n'.join(lines).replace('all20','all 20').replace('All16','All 16'));print(json.dumps({'counts':s['counts'],'calls':s['calls'],'checks':checks},indent=2))

# Exact actions can vary even at temperature zero; preserve this distinction.
variation=[c for c in checks if not c['first_action_match'] or not c['state_match']]
for v in variation:
 r=next(r for r in rows if r['id']==v['id']);p.dump(D/'example-replay-variation.json',{'check':v,'original':jobs[r['id']]['original_work'],'repeated':r,'source':str(D/'rollouts.jsonl'),'source_sha256':p.sha(D/'rollouts.jsonl')})
report=R/'docs/workflow_wording_results.md'
with report.open('a') as h:
 h.write('\n\n## Interpretation\n\nIn this fixed diagnostic, the single-word substitution removes all 16 invalid preservation calls while retaining 16/16 correct completions. This supports a causal effect of this wording choice in the tested contexts; it does not prove a specific internal representation or general robustness to paraphrases. The combined-card arm was not rerun.\n\nAll four original-wording controls reproduce the invalid-preservation outcome and final state. One first action used a different invalid artifact name (selected_ids rather than selected_ids_req-A_D), so exact first-action fidelity is 3/4 despite identical rendered prompts. Temperature-zero configuration does not guarantee token-for-token reproducibility. The variation is retained in example-replay-variation.json.\n')
for item in selected:
 if not item['selected']:continue
 packet=json.loads(pathlib.Path(item['path']).read_text());job=packet['job'];old=job['original_work'];new=packet['new_result']
 original_path=p.D/'qwen/rollouts.jsonl';original_line=next(i for i,line in enumerate(original_path.read_text().splitlines(),1) if json.loads(line)['id']==old['id'])
 md=pathlib.Path(item['path']).with_suffix('.md');text=['# Wording diagnostic — '+item['kind'],'','Selection: first context ID in this named outcome class. Same saved-work state; one word changed. Generated tool actions, not private reasoning.','',f"[Original branch]({original_path}:{original_line}) · [Replacement branch]({D/'rollouts.jsonl'}:{packet['line']}) · [Full source packet and checksums]({item['path']})",'']
 for label,r in [('Preserve that completed work',old),('Retain that completed work',new)]:
  text+=['## '+label,'']
  for st in r['steps']:text+=['```json',json.dumps({'action':st['action'],'result':st['result']},indent=2),'```','']
 md.write_text('\n'.join(text))
 with report.open('a') as h:h.write(f'\n\n[Readable {item["kind"]} example]({md})\n')
