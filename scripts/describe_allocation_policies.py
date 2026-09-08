"""Post-result descriptive policy fits; no held-out or mechanistic interpretation."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/opportunity_cost/v2';s=json.loads((D/'summary.json').read_text());out={'status':'Exploratory descriptive benchmarks added after viewing Qwen3 results. Not preregistered, not held-out prediction, not inferred model algorithms.','models':{}}
for model,m in s['models'].items():
 if not m['gate']['pass']:continue
 rs=[json.loads(l) for l in (D/model/'rollouts.jsonl').read_text().splitlines()];rs=[r for r in rs if not r['probe'] and not r['case']['control']]
 fits={'complete_own_then_maximize_peer':[],'first_displayed_own_success_else_peer':[]}
 for r in rs:
  c=r['case'];world=c['world_name'];got=r['decoded'].get('allocation') if r['decoded'] else None
  pred='own_only' if world=='costly' else 'peer_only' if world=='blocked' else 'joint'
  fits['complete_own_then_maximize_peer'].append({'id':c['id'],'prediction':pred,'observed':got,'match':pred==got})
  order=['no_work','joint','peer_only','own_only'] if c['order'] else ['own_only','peer_only','joint','no_work']
  feasible_own={'own_only','joint'} if world in ['slack','shared'] else {'own_only'} if world=='costly' else set()
  pred=next((x for x in order if x in feasible_own),'peer_only')
  fits['first_displayed_own_success_else_peer'].append({'id':c['id'],'prediction':pred,'observed':got,'match':pred==got})
 out['models'][model]={name:{'correct':sum(x['match'] for x in xs),'n':len(xs),'cases':xs} for name,xs in fits.items()}
(D/'descriptive_policy_fits.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({model:{name:(v['correct'],v['n']) for name,v in fits.items()} for model,fits in out['models'].items()},indent=2))
