import sys,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import peer_claims as old
import peer_claims_v2 as new
class RevisionTests(unittest.TestCase):
 def test_only_status_field_changes(self):
  for d in old.DOMAINS:
   for truth in [False,True]:
    for claim in ['none','hopeless']:
     for policy in ['optional','required','automatic']:
      for order in [0,1]:
       c=old.case(d,truth,claim,policy,order);expected=old.messages(c)
       for m in expected:m['content']=m['content'].replace(json.dumps(old.status(c)),json.dumps({**old.status(c),'peer_package_possible':True}))
       self.assertEqual(new.messages(c),expected)
 def test_cases_unchanged(self):
  self.assertEqual(json.loads((old.E/'cases.json').read_text()),json.loads((new.E/'cases.json').read_text()))
if __name__=='__main__':unittest.main()
