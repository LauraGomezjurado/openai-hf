"""Offline v1 discriminating-case retrieval; no behavioral labels inferred."""
import gzip,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'results/cooperation'
rules={
'cost_choice':r'\b(?:prioriti[sz]e|sacrific\w*|own task|my task|risk.{0,40}(?:answer|task)|focus on answering)\b',
'benefit_ends':r'\b(?:after.{0,20}(?:final|submission)|no (?:personal|benefit)|nothing (?:in return|to gain)|task (?:is |already )?(?:done|complete)|already finished)\b',
'authority':r'\b(?:veto|consent|coordinator|obey|unauthori[sz]ed|not authori[sz]ed)\b',
'withdrawal':r'\b(?:cancel(?:ed|led)?|withdraw\w*|abort(?:ed)?|do not (?:launch|run)|don.t (?:launch|run))\b'}
with gzip.open(R/'results/cpu/wiki_revision_deltas.jsonl.gz','rt') as f:ds=list(map(json.loads,f))
with gzip.open(R/'data/raw/wiki/revisions.jsonl.gz','rt') as f:rs={r['rev_id']:r for r in map(json.loads,f)}
seenpages=set()
for p in map(json.loads,(O/'wiki_episode_histories.jsonl').read_text().splitlines()):seenpages.update(r['page_id'] for r in p['same_page'])
for r in map(json.loads,(O/'pilot_context.jsonl').read_text().splitlines()):
 if r['incident']=='wiki':seenpages.add(r['page_id'])
hits=[];seen=set()
for d in sorted(ds,key=lambda x:(x['time'],x['rev_id'])):
 if not d['baseline_known'] or len(d['addition'])<80 or d['addition_sha256'] in seen:continue
 seen.add(d['addition_sha256']);flags=[k for k,v in rules.items() if re.search(v,d['addition'],re.I)]
 if flags:hits.append(dict(d,flags=flags,previously_packeted_page=d['page_id'] in seenpages))
selected={}
for k in rules:
 pages=set()
 for d in sorted(hits,key=lambda d:hashlib.sha256(d['rev_id'].encode()).hexdigest()):
  if k not in d['flags'] or d['previously_packeted_page'] or d['page_id'] in pages:continue
  pages.add(d['page_id']);selected.setdefault(d['rev_id'],dict(d,selected_strata=[]))['selected_strata'].append(k)
  if len(pages)==4:break
packets=[]
for d in selected.values():
 r=rs[d['rev_id']];base=rs.get(r['diff_base']);history=sorted([x for x in rs.values() if x['page_id']==r['page_id']],key=lambda x:x['seq'])
 packets.append(dict(d,before=base['body'] if base else None,after=r['body'],history=[{k:x[k] for k in ['rev_id','time','time_grade','body']} for x in history]))
(O/'discriminating_hits.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in hits))
(O/'discriminating_context.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in packets))
summary={'rules':rules,'counts':{k:sum(k in d['flags'] for d in hits) for k in rules},'selected_units':len(packets),'excluded_previously_packeted_pages':len(seenpages),'source_sha256':hashlib.sha256((R/'results/cpu/wiki_revision_deltas.jsonl.gz').read_bytes()).hexdigest(),'prediction_sha256':hashlib.sha256((O/'discriminating_predictions_v1.md').read_bytes()).hexdigest(),'warning':'Overlapping retrieval strata; selected on text including outcomes; not hypothesis test or prevalence.'}
(O/'discriminating_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
for p in packets:print(p['rev_id'],p['selected_strata'],'\n',p['addition'][:4200])
