"""Frozen v1 retrieval for cooperation feasibility; matches are not labels."""
import csv,gzip,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/cooperation';OUT.mkdir(parents=True,exist_ok=True)
RULES={
 'request':r'\b(?:please|can anyone|could someone|help me|anyone able)\b',
 'own_task':r'\b(?:my (?:task|question|answer|score|round)|own task|I need to (?:finish|answer|submit))\b',
 'scarce_time':r'\b(?:time (?:limit|left|remaining)|deadline|running out of time|minutes? left)\b',
 'reciprocity':r'\b(?:in return|return the favor|reciproc\w*|help each other|mutual help)\b',
 'scope_refusal':r'\b(?:out.of.scope|not authorized|outside (?:my|our|the) scope|cannot help|can.t help|won.t help|must focus|should not|shouldn.t)\b',
 'completion':r'\b(?:my task is (?:done|complete)|I (?:have |already )?(?:finished|submitted)|already solved|nothing in return)\b'
}
def stable(s):return hashlib.sha256(s.encode()).hexdigest()
def readcsv(p):
 with p.open() as f:return list(csv.DictReader(f))
def main():
 with gzip.open(ROOT/'results/cpu/wiki_revision_deltas.jsonl.gz','rt') as f: ds=list(map(json.loads,f))
 with gzip.open(ROOT/'data/raw/wiki/revisions.jsonl.gz','rt') as f: revs={r['rev_id']:r for r in map(json.loads,f)}
 records=[];seen=set()
 for d in sorted(ds,key=lambda x:(x['time'],x['rev_id'])):
  if not d['baseline_known'] or len(d['addition'])<80:continue
  h=stable(d['addition'])
  if h in seen:continue
  seen.add(h)
  records.append(dict(unit_id=d['rev_id'],incident='wiki',text=d['addition'],source_url=d['source_url'],page_id=d['page_id'],time=d['time'],time_grade=d['time_grade']))
 for r in readcsv(ROOT/'results/cpu/hf_annotation_ledger.csv'):
  records.append(dict(unit_id=r['ledger_id'],incident='HF',text=r['source_text'],source_url=r['source_url'],page_id=r['snapshot_agent_row'],time=r['reconstructed_utc'],time_grade='approximate',source_type=r['source_type']))
 for r in records:
  r['matches']={k:[r['text'][max(0,m.start()-100):m.end()+160] for m in re.finditer(p,r['text'],re.I)][:3] for k,p in RULES.items() if re.search(p,r['text'],re.I)}
 selected={};counts={}
 for incident in ['HF','wiki']:
  population=[r for r in records if r['incident']==incident]
  counts[incident]={k:sum(k in r['matches'] for r in population) for k in RULES}
  strata=list(RULES)+['comparison']
  for k in strata:
   pool=[r for r in population if k=='comparison' or k in r['matches']]
   for r in sorted(pool,key=lambda r:stable(k+r['unit_id']))[:4]:
    selected.setdefault(r['unit_id'],dict(r,selection_strata=[]))['selection_strata'].append(k)
 packets=[]
 for r in selected.values():
  r=dict(r)
  if r['incident']=='wiki':
   original=revs[r['unit_id']];base=revs.get(original['diff_base'])
   r.update(before=base['body'] if base else None,after=original['body'],diff_base=original['diff_base'])
  else:r['context_limit']='Selected investigator publication; full transcript unavailable'
  packets.append(r)
 (OUT/'rules_v1.json').write_text(json.dumps(RULES,indent=2)+'\n')
 (OUT/'pilot_context.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in packets))
 with (OUT/'candidate_index.csv').open('w',newline='') as f:
  fields=['unit_id','incident','page_id','time','source_url','retrieval_flags'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in records:
   if r['matches']:w.writerow({**{k:r[k] for k in fields[:-1]},'retrieval_flags':'|'.join(r['matches'])})
 summary=dict(version=1,eligible_by_incident={i:sum(r['incident']==i for r in records) for i in ['HF','wiki']},retrieval_counts=counts,pilot_units=len(packets),pilot_by_incident={i:sum(r['incident']==i for r in packets) for i in ['HF','wiki']},warning='Overlapping lexical retrieval counts; no confirmed conflicts or population prevalence. Four selections per stratum, union deduplicated. Comparison is hash-selected from all eligible records, not known negatives.',source_sha256={str(p.relative_to(ROOT)):stable(p.read_bytes().hex()) for p in []})
 summary['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'results/cpu/wiki_revision_deltas.jsonl.gz',ROOT/'results/cpu/hf_annotation_ledger.csv']}
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 assert len({r['unit_id'] for r in packets})==len(packets)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
