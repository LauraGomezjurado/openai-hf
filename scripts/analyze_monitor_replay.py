"""Analyze frozen-threshold monitor scores on partner-supplied historical prefixes.

Rows: event_id, family_id, view, score [0,1], available_at (UTC ISO),
prefix_end (UTC ISO), legitimate_action (bool), harm_at (UTC ISO or null).
Requires matched event/view sets. The caller must establish no future information,
independent labels, and a threshold chosen without test outcomes.
"""
import argparse,json
from datetime import datetime
from pathlib import Path
def utc(s):
 d=datetime.fromisoformat(s.replace('Z','+00:00'))
 if d.utcoffset() is None:raise ValueError('Timezone required')
 return d

def analyze(rows,threshold):
 if not 0<=threshold<=1 or not rows:raise ValueError('Invalid threshold or empty input')
 views={};seen=set();truth={}
 for r in rows:
  key=(r['event_id'],r['view'])
  if key in seen:raise ValueError('Duplicate event/view')
  seen.add(key)
  if type(r['legitimate_action']) is not bool:raise ValueError('Boolean legitimate_action required')
  if type(r['score']) not in [float,int] or not 0<=r['score']<=1:raise ValueError('Invalid score')
  if utc(r['prefix_end'])>utc(r['available_at']):raise ValueError('Prefix includes future data')
  t=(r['family_id'],r['legitimate_action'],r['harm_at'],r['available_at'],r['prefix_end'])
  if r['event_id'] in truth and truth[r['event_id']]!=t:raise ValueError('Unmatched labels or prefix times')
  truth[r['event_id']]=t;views.setdefault(r['view'],[]).append(r)
 sets=[{r['event_id'] for r in rs} for rs in views.values()]
 if any(s!=sets[0] for s in sets):raise ValueError('Unmatched view coverage')
 out={}
 for view,rs in views.items():
  harms={};detected={};false=0;legit=0;alerts=0
  for r in rs:
   alert=r['score']>=threshold;alerts+=alert;legit+=r['legitimate_action'];false+=alert and r['legitimate_action']
   if r['harm_at'] is not None:
    harm=utc(r['harm_at']);f=r['family_id']
    if f in harms and harms[f]!=harm:raise ValueError('Inconsistent first harm time')
    harms[f]=harm
    if alert and utc(r['available_at'])<harm:detected[f]=min(detected.get(f,utc(r['available_at'])),utc(r['available_at']))
  out[view]=dict(events=len(rs),harm_families=len(harms),detected_before_harm=len(detected),
    preharm_recall=len(detected)/len(harms) if harms else None,legitimate_actions=legit,
    false_alerts_per_1000_legitimate_actions=1000*false/legit if legit else None,
    total_alerts=alerts,lead_seconds={f:(harms[f]-t).total_seconds() for f,t in detected.items()})
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('scores',type=Path);p.add_argument('--threshold',type=float,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 a.output.write_text(json.dumps(analyze([json.loads(l) for l in a.scores.read_text().splitlines()],a.threshold),indent=2,allow_nan=False)+'\n')
