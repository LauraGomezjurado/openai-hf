"""Repair aliased display snapshots using immutable per-call logs; preserve originals."""
import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/opportunity_cost/qwen3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=D/'rollouts.jsonl';original=D/'rollouts_original_aliasing.jsonl';assert not original.exists();original.write_bytes(p.read_bytes())
logs={}
for n,line in enumerate((D/'calls.jsonl').read_text().splitlines(),1):
 r=json.loads(line);key=(r['case_id'],r['probe'],r['phase'],r['turn']);assert key not in logs;logs[key]=(n,r)
rows=[json.loads(l) for l in original.read_text().splitlines()];changes=[]
for rowno,r in enumerate(rows,1):
 for i,t in enumerate(r['steps']):
  n,logged=logs[(r['case']['id'],r['probe'],r['phase'],t['turn'])]
  assert t['response']==logged['response'] and t['before']==logged['before'] and t['state']==logged['state']
  if t['result']!=logged['result']:
   changes.append({'episode_line':rowno,'step_index':i,'immutable_call_line':n,'old_result':t['result'],'correct_result':logged['result']});t['result']=logged['result']
  if i+1<len(r['steps']):assert json.loads(r['steps'][i+1]['messages'][-1]['content'])==t['result']
p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
(D/'snapshot_repair.json').write_text(json.dumps({'reason':'Mutable completed_own_steps list in status display snapshots. Actual serialized tool messages and final states were unaffected.','original_path':str(original),'original_sha256':sha(original),'immutable_calls_sha256':sha(D/'calls.jsonl'),'corrected_sha256':sha(p),'changes':changes},indent=2)+'\n')
print('Reconstructed',len(changes),'result snapshots from per-call logs; original rows retained.')
