import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('monitor',Path(__file__).resolve().parents[1]/'scripts/analyze_monitor_replay.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def fixture():
 return [dict(event_id='e',family_id='f',view=v,score=.9,available_at='2026-07-10T00:00:00Z',prefix_end='2026-07-10T00:00:00Z',legitimate_action=True,harm_at='2026-07-10T00:01:00Z') for v in ['actions','peer']]
class Checks(unittest.TestCase):
 def test_metrics(self):
  a=m.analyze(fixture(),.5)['peer'];self.assertEqual(a['lead_seconds']['f'],60);self.assertEqual(a['false_alerts_per_1000_legitimate_actions'],1000)
 def test_leakage(self):
  d=fixture();d[0]['prefix_end']='2026-07-10T00:02:00Z'
  with self.assertRaises(ValueError):m.analyze(d,.5)
 def test_no_alert(self):self.assertEqual(m.analyze(fixture(),1)['peer']['preharm_recall'],0)
if __name__=='__main__':unittest.main()
