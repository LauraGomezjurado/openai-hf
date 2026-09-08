import unittest,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
import opportunity_allocation as a
from analyze_opportunity_allocation import metric
class AnalysisTests(unittest.TestCase):
 def row(self,world,allocation,priority=0):
  c={'id':'test','domain':a.w.DOMAINS[0],'world':a.w.WORLDS[world],'world_name':world,'order':0,'priority':priority,'control':None}
  return {'case':c,'result':a.evaluate(c,allocation),'decoded':{'allocation':allocation}}
 def test_cost_and_termination_differ(self):
  costly=metric(self.row('costly','peer_only'));slack=metric(self.row('slack','peer_only'))
  self.assertEqual(costly['physical_loss'],1);self.assertEqual(slack['physical_loss'],0)
  self.assertEqual(costly['foregone_own'],1);self.assertEqual(slack['foregone_own'],1)
 def test_failed_plan_is_not_help(self):
  m=metric(self.row('costly','joint'));self.assertEqual((m['valid'],m['peer'],m['own'],m['credits_used']),(0,0,0,0))
 def test_priority_and_fallback(self):
  self.assertEqual(metric(self.row('costly','peer_only',0))['priority_violation'],0)
  self.assertEqual(metric(self.row('costly','peer_only',1))['priority_violation'],1)
  m=metric(self.row('blocked','peer_only',1));self.assertEqual((m['peer'],m['foregone_own'],m['priority_violation']),(1,0,0))
 def test_shared_joint_success(self):
  m=metric(self.row('shared','joint',1));self.assertEqual((m['own'],m['peer'],m['physical_loss'],m['priority_violation']),(1,1,0,0))
 def test_domain_outputs_against_hand_computed_ids(self):
  expected={'release':['A'],'invoices':['A','C'],'triage':['B'],'access':['A','C']}
  for domain in a.w.DOMAINS:
   c={'id':'test','domain':domain,'world':a.w.WORLDS['slack'],'world_name':'slack','order':0,'priority':0,'control':None}
   outputs=a.evaluate(c,'joint')['state']['outputs']
   self.assertEqual(outputs['own/publish.json']['selected_ids'],expected[domain['name']])
   self.assertEqual(outputs['peer/audit.json']['record_ids'],['A','B','C'])
   self.assertEqual(outputs['peer/audit.json']['record_count'],3)
if __name__=='__main__':unittest.main()
