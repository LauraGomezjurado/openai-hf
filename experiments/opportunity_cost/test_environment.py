import unittest,sys,copy,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import opportunity_cost as e
class EnvironmentTests(unittest.TestCase):
 def cases(self):
  for d,w in itertools.product(e.DOMAINS,e.WORLDS):yield dict(id=d['name']+'-'+w,domain=d,world=e.WORLDS[w],world_name=w,priority=0,order=0,control=None)
 def test_oracle_contrasts(self):
  for c in self.cases():
   s=e.initial(c);self.assertEqual(e.feasible(c,s),c['world_name']!='blocked');self.assertEqual(e.feasible(c,s,True),c['world_name'] in ['slack','shared'])
   before=e.feasible(c,s);e.act(c,s,'assist_peer',{});self.assertTrue(s['peer_delivered']);self.assertEqual(before and not e.feasible(c,s),c['world_name']=='costly')
 def test_actual_joint_artifacts(self):
  for c in self.cases():
   if c['world_name'] not in ['slack','shared']:continue
   s=e.initial(c);e.act(c,s,'assist_peer',{})
   for node in e.nodes(c):
    if node not in s['done']:e.act(c,s,'run_step',{'step':node})
   self.assertTrue(s['own_published'] and s['peer_delivered']);self.assertEqual(s['outputs']['own/publish.json']['selected_ids'],e.selected(c));self.assertEqual(s['credits'],0)
 def test_block_and_invalid_cost(self):
  for c in self.cases():
   s=e.initial(c);n=s['credits'];out=e.act(c,s,'run_step',{'step':'publish'});self.assertIn('error',out);self.assertEqual(s['credits'],n-1)
   if c['world_name']=='blocked':
    s=e.initial(c)
    for node in e.nodes(c):out=e.act(c,s,'run_step',{'step':node})
    self.assertFalse(s['own_published']);self.assertIn('error',out)
 def test_status_snapshot_is_immutable(self):
  c=next(self.cases());s=e.initial(c);old=e.act(c,s,'run_step',{'step':'load'});saved=copy.deepcopy(old);e.act(c,s,'run_step',{'step':'verify'});self.assertEqual(old,saved)
 def test_finish_ends_opportunity(self):
  for c in self.cases():
   s=e.initial(c);e.act(c,s,'finish',{});self.assertFalse(e.feasible(c,s))
if __name__=='__main__':unittest.main()
