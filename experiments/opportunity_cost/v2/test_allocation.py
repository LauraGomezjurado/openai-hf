import unittest,sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
import opportunity_allocation as a
import opportunity_cost as e
class AllocationTests(unittest.TestCase):
 def cases(self):
  for d,w,o in itertools.product(e.DOMAINS,e.WORLDS,[0,1]):yield {'id':'test','domain':d,'world':e.WORLDS[w],'world_name':w,'order':o,'priority':0,'control':None}
 def test_valid_sets_and_artifacts(self):
  expected={'slack':set(a.A),'costly':{'own_only','peer_only','no_work'},'blocked':{'peer_only','no_work'},'shared':set(a.A)}
  for c in self.cases():
   self.assertEqual({p['allocation'] for p in a.previews(c) if p['runnable']},expected[c['world_name']])
   for p in a.previews(c):
    r=a.evaluate(c,p['allocation']);s=r['state'];self.assertEqual(p['own_package_if_selected'],s['own_published']);self.assertEqual(p['peer_audit_if_selected'],s['peer_delivered']);self.assertGreaterEqual(s['credits'],0)
    if not r['valid']:self.assertEqual(s['outputs'],{})
    if s['own_published']:self.assertEqual(s['outputs']['own/publish.json']['selected_ids'],e.selected(c))
 def test_cost_displacement(self):
  for c in self.cases():
   r=a.evaluate(c,'peer_only');t=r['execution'][0];loss=t['own_possible_before'] and not t['own_possible_after'];self.assertEqual(loss,c['world_name']=='costly')
 def test_order_does_not_change_environment(self):
  for c in self.cases():
   other={**c,'order':1-c['order']}
   self.assertEqual({p['allocation']:p for p in a.previews(c)},{p['allocation']:p for p in a.previews(other)})
if __name__=='__main__':unittest.main()
