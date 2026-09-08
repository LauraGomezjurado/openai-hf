import pathlib,json,hashlib,collections
R=pathlib.Path(__file__).resolve().parents[1];E=R/'experiments/workflow_obligations/v2';D=R/'results/workflow_obligations/v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((E/'freeze.json').read_text());assert sha(E/'cases.json')==f['cases_sha256'];assert sha(E/'protocol.md')==f['protocol_sha256'];assert sha(R/'scripts/workflow_obligations.py')==f['script_sha256']
summary={}
for m in ['qwen','qwen3','phi']:
 rs=[json.loads(l) for l in (D/m/'rollouts.jsonl').read_text().splitlines()];gate=json.loads((D/m/'gate.json').read_text());assert len({r['case']['id'] for r in rs})==len(rs);main=[r for r in rs if not r['case']['control']]
 if gate['pass']:
  assert len(rs)==53 and len(main)==48;assert all(v==4 for v in collections.Counter((r['case']['evidence'],r['case']['pressure'],r['case']['arm']) for r in main).values())
 else:assert len(rs)==5 and not main
 assert all(len(r['steps'])<=10 for r in rs)
 log=[json.loads(l) for l in (D/m/'steps.jsonl').read_text().splitlines()];assert len(log)==sum(len(r['steps']) for r in rs)
 summary[m]={'episodes':len(rs),'main':len(main),'calls':len(log),'gate':gate,'rollouts_sha256':sha(D/m/'rollouts.jsonl')}
(D/'validation.json').write_text(json.dumps({'status':'passed','checks':'frozen cases/code/protocol; unique complete factorial panels; gate-stopped model retained; action limits; per-call log coverage','models':summary},indent=2));print(json.dumps(summary,indent=2))
