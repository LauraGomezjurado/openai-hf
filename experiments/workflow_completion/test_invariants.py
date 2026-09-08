import sys,json,copy,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
import workflow_completion as e
class ProvenanceTests(unittest.TestCase):
 def test_frozen_inputs_and_unselected_outcomes(self):
  freeze=json.loads((e.E/'freeze.json').read_text())
  for p,h in freeze['sha256'].items():self.assertEqual(e.sha(R/p),h)
  cs=json.loads((e.E/'contexts.json').read_text());self.assertEqual(len(cs),32)
  for model in ['qwen','qwen3']:
   raw=[json.loads(s) for s in (R/f'results/workflow_obligations/v2/{model}/rollouts.jsonl').read_text().splitlines()]
   expected={r['case']['id'] for r in raw if not r['case']['control'] and r['case']['arm']=='task'}
   self.assertEqual(expected,{c['case']['id'] for c in cs if c['model']==model})
 def test_predecision_state_and_budget(self):
  for c in json.loads((e.E/'contexts.json').read_text()):
   p=Path(c['source']);self.assertEqual(e.sha(p),c['source_sha256'])
   r=json.loads(p.read_text().splitlines()[c['source_line']-1]);k=c['used_turns']
   self.assertEqual(r['steps'][k]['action']['tool'],'finish')
   self.assertEqual(c['source_prompt'],r['steps'][k]['rendered_prompt'])
   self.assertEqual(c['state'],r['steps'][k-1]['state'] if k else e.w.initial())
   self.assertFalse(c['state']['finished']);self.assertEqual(k+c['remaining'],10)
 def test_branch_only_changes_last_feedback(self):
  for c in json.loads((e.E/'contexts.json').read_text()):
   old=copy.deepcopy(c);self.assertEqual(e.branch_messages(c,'replay'),c['messages'])
   for arm in ['work','duty','both']:
    ms=e.branch_messages(c,arm);self.assertEqual(ms[:-1],c['messages'][:-1]);self.assertTrue(ms[-1]['content'].startswith(c['messages'][-1]['content']))
   self.assertEqual(c,old)
if __name__=='__main__':unittest.main()
