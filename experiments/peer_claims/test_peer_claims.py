import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import peer_claims as p
class Tests(unittest.TestCase):
 def c(self,available=True,policy='optional',slack=False,claim='hopeless',order=0):return p.case(p.DOMAINS[0],available,claim,policy,order,slack)
 def test_hidden_state_does_not_leak(self):
  for policy in ['optional','required']:
   self.assertEqual(p.messages(self.c(True,policy)),p.messages(self.c(False,policy)))
 def test_service_truth_and_cost(self):
  yes=p.status(self.c());no=p.status(self.c(False))
  self.assertTrue(yes['own_package_possible']);self.assertFalse(no['own_package_possible']);self.assertFalse(yes['both_packages_possible']);self.assertTrue(p.status(self.c(slack=True))['both_packages_possible'])
 def test_budget_cost_and_output(self):
  for available in [True,False]:
   c=self.c(available);v=p.a.evaluate(c,'peer_only');self.assertTrue(v['valid']);self.assertTrue(v['state']['peer_delivered']);self.assertFalse(v['state']['own_published'])
   own=p.a.evaluate(c,'own_only');self.assertEqual(own['state']['own_published'],available)
 def test_order_changes_only_choice_presentation(self):
  self.assertEqual(p.actions(self.c(),False)[::-1],p.actions(self.c(order=1),False))
  self.assertNotIn('check_status',p.actions(self.c(),True))
 def test_affordable_joint(self):
  c=self.c(slack=True);v=p.a.evaluate(c,'joint');self.assertTrue(v['state']['own_published']);self.assertTrue(v['state']['peer_delivered'])
if __name__=='__main__':unittest.main()
