"""Separately frozen neutral-context capability checks; never pooled with main panel."""
import pathlib,json,hashlib,sys,time
import escalation_pilot as pilot
R=pathlib.Path(__file__).resolve().parents[1];E=R/'experiments/escalation_pilot/arithmetic_checks';O=R/'results/escalation/arithmetic_checks'
if sys.argv[1]=='freeze':
 E.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
 base=json.loads((R/'experiments/escalation_pilot/v2/cases.json').read_text());cs=[]
 for i in range(4):
  c=next(c.copy() for c in base if c['family']==i and not c['control']);c.update(id=f'arithmetic-{i}',evidence='arithmetic_only',duty=None,route=None,prompt=c['prompt'].split('\nProject policy:')[0]);cs.append(c)
 pilot.dump(E/'cases.json',cs);pilot.dump(E/'freeze.json',{'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'cases_sha256':pilot.digest(E/'cases.json'),'script_sha256':pilot.digest(pathlib.Path(pilot.__file__)),'wrapper_sha256':pilot.digest(pathlib.Path(__file__)),'system':pilot.SYSTEM,'purpose':'Same numbers and tools, no incident context; exploratory after observing arithmetic errors, not pooled with main treatment panel.'})
else:
 pilot.EXP=E;pilot.OUT=O;pilot.run()
