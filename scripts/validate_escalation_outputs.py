"""Check completed experiment structure and frozen provenance."""
import pathlib,json,hashlib,collections
R=pathlib.Path(__file__).resolve().parents[1]
def read(p):return [json.loads(l) for l in (R/p).read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
main=read('results/escalation/pilot_v2/rollouts.jsonl');forks=read('results/escalation/continuations/rollouts.jsonl');checks=read('results/escalation/arithmetic_checks/rollouts.jsonl')
assert len(main)==36 and len({x['case']['id'] for x in main})==36
assert len(forks)==48 and len({x['case']['id'] for x in forks})==48
assert len(checks)==4
assert all(v==4 for v in collections.Counter((r['case']['evidence'],r['case']['duty'],r['case']['route']) for r in main if not r['case']['control']).values())
assert all(v=={'replay','task','duty'} for v in [{r['case']['arm'] for r in forks if r['case']['source_case']['id']==sid} for sid in {r['case']['source_case']['id'] for r in forks}])
for folder in ['v2','arithmetic_checks','continuations']:
 e=R/'experiments/escalation_pilot'/folder;f=json.loads((e/'freeze.json').read_text());assert sha(e/'cases.json')==f['cases_sha256']
f=json.loads((R/'experiments/escalation_pilot/continuations/freeze.json').read_text());assert sha(R/'results/escalation/pilot_v2/rollouts.jsonl')==f['source_sha256'];assert sha(R/'scripts/escalation_continuations.py')==f['script_sha256'];assert sha(R/'scripts/escalation_pilot.py')==f['shared_runner_sha256'];assert sha(R/'experiments/escalation_pilot/continuations/protocol.md')==f['protocol_sha256']
assert all(len(r['steps'])<=r['case']['remaining_turns'] for r in forks)
assert all(len(r['steps'])<=6 for r in main+checks)
summary={'checks':'passed: complete unique panels, full factorial cells, all continuation arms, immutable case/source/code/protocol hashes, action budgets','main_episodes':32,'interface_controls':4,'arithmetic_checks':4,'continuations':48,'generation_calls_excluding_v1':sum(len(r['steps']) for r in main+checks+forks)}
(R/'results/escalation/validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
