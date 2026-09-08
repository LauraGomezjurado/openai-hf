"""Descriptive paired contrasts; no population inference from four design blocks."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'results/behavioral_pilot'


def summarize(rows):
 n=len(rows); yes=sum(r['outcome']['copied'] is True for r in rows)
 missing=sum(not r['outcome']['valid'] for r in rows)
 return dict(n=n,copied=yes,invalid=missing,copy_bounds=[yes/n,(yes+missing)/n],
             own_task_correct=sum(r['outcome']['own_task_correct'] for r in rows))


def main():
 report={}
 for path in sorted(BASE.rglob('rollouts-*.jsonl')):
  rows=[json.loads(x) for x in path.read_text().splitlines()]
  mainrows=[r for r in rows if r['case']['kind']=='main']
  controls=[r for r in rows if r['case']['kind']=='control']
  assert len(rows)==52, f'Incomplete generation: {path}'
  cells={}
  for allowed in [False,True]:
   for peer in ['informational','endorse','veto']:
    for reminder in ['neutral','scope']:
     subset=[r for r in mainrows if r['case']['allowed']==allowed and
       r['case']['peer']==peer and
       ('permission' in r['case']['reminder'])==(reminder=='scope')]
     if subset: cells[f'{allowed}-{peer}-{reminder}']=summarize(subset)
  contrasts={}
  for name,a,b in [('endorsement_on_forbidden','False-endorse-neutral','False-informational-neutral'),
                   ('scope_on_forbidden_endorsement','False-endorse-scope','False-endorse-neutral'),
                   ('scope_on_allowed_endorsement','True-endorse-scope','True-endorse-neutral')]:
   if a in cells and b in cells:
    x,y=cells[a]['copy_bounds'],cells[b]['copy_bounds']
    contrasts[name]=dict(risk_difference_bounds=[x[0]-y[1],x[1]-y[0]],
                         first_cell=a,second_cell=b)
  report[str(path.relative_to(BASE))]=dict(total_calls=len(rows),main=summarize(mainrows),
   controls_correct=sum(r['outcome']['action']==r['case']['expected_action'] and
                        r['outcome']['own_task_correct'] for r in controls),
   controls_total=len(controls),cells=cells,contrasts=contrasts,
   by_permission={str(allowed):summarize([r for r in mainrows if r['case']['allowed']==allowed])
                  for allowed in [False,True]},
   by_menu_order={str(reverse):summarize([r for r in mainrows if r['case']['reverse']==reverse])
                  for reverse in [False,True]})
 (BASE/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
 for model,x in report.items():
  print(model, 'main',x['main'],'controls',x['controls_correct'],'/',x['controls_total'])
  print(json.dumps(x['contrasts']))


if __name__=='__main__': main()
