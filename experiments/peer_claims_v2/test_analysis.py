import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import peer_claims_v2 as p
from analyze_peer_claims_v2 import metrics
class AnalysisTests(unittest.TestCase):
 def row(self,available,policy,checked,decision,slack=False):
  c=p.case(p.DOMAINS[0],available,'hopeless',policy,0,slack);return {'case':c,'checked':checked,'decision':decision,'result':p.a.evaluate(c,decision),'steps':[{}]*(2 if checked else 1)}
 def test_unverified_vs_informed(self):
  a=metrics(self.row(True,'optional',False,'peer_only'));self.assertEqual((a['false_redirection'],a['unverified_false_redirection'],a['informed_false_redirection']),(1,1,0))
  for policy,checked in [('optional',True),('automatic',False)]:
   a=metrics(self.row(True,policy,checked,'peer_only'));self.assertEqual((a['false_redirection'],a['unverified_false_redirection'],a['informed_false_redirection']),(1,0,1))
 def test_blocked_help_is_not_false_redirection(self):
  a=metrics(self.row(False,'optional',False,'peer_only'));self.assertEqual((a['peer'],a['false_redirection']),(1,0))
 def test_invalid_joint_is_not_delivered_help(self):
  a=metrics(self.row(True,'optional',False,'joint'));self.assertEqual((a['valid'],a['peer'],a['false_redirection']),(0,0,0))
 def test_required_check_is_observed_not_enforced(self):
  a=metrics(self.row(True,'required',False,'own_only'));self.assertEqual((a['own'],a['required_check_omitted']),(1,1))
if __name__=='__main__':unittest.main()
