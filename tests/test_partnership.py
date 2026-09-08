"""Fabricated arithmetic fixtures, not scientific observations."""
import importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('pipeline',Path(__file__).resolve().parents[1]/'scripts/partnership_pipeline.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fixture():
 return [dict(family_id=f'F{i}',run_id=f'{i}-{a}-{j}',arm=a,scope_violation=a=='baseline',task_success=True,useful_assistance=True) for i in range(3) for a in m.ARMS for j in range(5)]
class Checks(unittest.TestCase):
 def test_effect_sign(self):
  r=m.analyze(fixture())[0];self.assertEqual(r['complete_family_risk_difference'],-1);self.assertEqual(r['all_family_missing_outcome_bounds'],[-1,-1])
 def test_null_is_unknown(self):
  d=fixture();d[0]['scope_violation']=None;r=m.analyze(d)[0];self.assertEqual(r['complete_families'],2);self.assertEqual(r['missing_runs_in_pair'],1);self.assertGreater(r['all_family_missing_outcome_bounds'][1],-1)
 def test_all_missing(self):
  d=fixture()
  for r in d:r['scope_violation']=None
  a=m.analyze(d)[0];self.assertIsNone(a['complete_family_risk_difference']);self.assertEqual(a['all_family_missing_outcome_bounds'],[-1,1])
 def test_bad_label(self):
  d=fixture();d[0]['scope_violation']=0
  with self.assertRaises(ValueError):m.analyze(d)
 def test_duplicate(self):
  d=fixture();d[1]['run_id']=d[0]['run_id']
  with self.assertRaises(ValueError):m.analyze(d)
 def test_incomplete_arm(self):
  with self.assertRaises(ValueError):m.analyze(fixture()[:-1])
 def test_order_invariant(self):
  d=fixture();self.assertEqual(m.analyze(d),m.analyze(list(reversed(d))))
if __name__=='__main__':unittest.main()
