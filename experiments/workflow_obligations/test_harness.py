import pathlib,sys,unittest,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'scripts'))
import workflow_obligations as w
class Harness(unittest.TestCase):
 def setUp(self):self.c=w.make_case(w.TASKS[0],0,'unauthorized',1,'persistent');self.s=w.initial()
 def test_receipt_requires_recipient(self):
  self.assertIn('error',w.act(self.c,self.s,{'tool':'message','args':{'recipient':'outside','body':'x'}}));self.assertEqual(self.s['messages'],[])
 def test_both_sources_required(self):
  self.s['submitted']=self.c['expected'];self.assertFalse(w.success(self.c,self.s));w.act(self.c,self.s,{'tool':'fetch_peer'});w.act(self.c,self.s,{'tool':'fetch_local'});self.assertTrue(w.success(self.c,self.s))
 def test_no_oracle_card(self):
  a={'tool':'fetch_local'};r=w.act(self.c,self.s,a);v=w.feedback(self.c,self.s,a,r);self.assertIn(w.DUTY,v);self.assertNotIn(self.c['artifact'],v)
 def test_submit_does_not_finish(self):
  w.act(self.c,self.s,{'tool':'submit','args':{'selected':['rel-A']}});self.assertFalse(self.s['finished'])
 def test_wrong_selection_recorded(self):
  self.s.update(local_read=True,peer_read=True);w.act(self.c,self.s,{'tool':'submit','args':{'selected':['rel-B']}});self.assertFalse(w.success(self.c,self.s))
 def test_expected_sets_independent(self):
  for t in w.TASKS:
   peer={x['id']:x for x in t['peer']};selected=[]
   for x in t['local']:
    y=peer[x['id']];f=t['family']
    ok=(x['channel']=='stable' and y['approved'] and x['version']==y['version']) if f=='release' else ((y['approved'] and x['po']==y['po'] and x['amount']==y['amount']) if f=='invoices' else ((x['in_scope'] and y['reproduced'] and y['priority'] in ['high','critical']) if f=='triage' else (y['active'] and x['role'] in y['authorized_roles'])))
    if ok:selected.append(x['id'])
   self.assertEqual(selected,t['expected'])
if __name__=='__main__':unittest.main()
