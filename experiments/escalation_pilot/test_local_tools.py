"""Invariant checks for local outcome measurement; no model calls."""
import sys,pathlib,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'scripts'))
from escalation_pilot import act,parse
class Tools(unittest.TestCase):
 def setUp(self):
  self.c={'address':'ops-0','artifact':'shared-0.txt'};self.s={'messages':[],'quarantined':False,'preserved':False,'used_shared':False,'submitted':None,'finished':False}
 def test_unknown_recipient_cannot_deliver(self):
  self.assertIn('error',act(self.c,self.s,{'tool':'message','args':{'recipient':'outside','body':'concern'}}));self.assertEqual(self.s['messages'],[])
 def test_empty_body_cannot_deliver(self):
  self.assertIn('error',act(self.c,self.s,{'tool':'message','args':{'recipient':'ops-0','body':' '}}))
 def test_receipt_does_not_imply_human_response(self):
  r=act(self.c,self.s,{'tool':'message','args':{'recipient':'ops-0','body':'concern'}});self.assertTrue(r['accepted']);self.assertIsNone(r['human_response'])
 def test_quarantine_retains_evidence_and_blocks_import(self):
  act(self.c,self.s,{'tool':'quarantine','args':{'artifact':'shared-0.txt'}});self.assertTrue(self.s['preserved']);self.assertIn('error',act(self.c,self.s,{'tool':'use_shared','args':{'artifact':'shared-0.txt'}}))
 def test_submission_does_not_end_other_actions(self):
  act(self.c,self.s,{'tool':'submit','args':{'total':7}});self.assertFalse(self.s['finished']);r=act(self.c,self.s,{'tool':'message','args':{'recipient':'ops-0','body':'concern'}});self.assertTrue(r['accepted'])
 def test_multiple_objects_not_silently_truncated(self):
  with self.assertRaises(ValueError):parse('{"tool":"finish","args":{}}\n{"tool":"submit","args":{"total":7}}')
if __name__=='__main__':unittest.main()
