"""Read-only offline episode context extraction. Never executes archive links."""
import gzip,json,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];O=R/'results/cooperation'
with gzip.open(R/'data/raw/wiki/revisions.jsonl.gz','rt') as f:revs=list(map(json.loads,f))
seeds=['dse~OECDEquityApr14Live@15','dse~FinanceSequenceMar26OAI@16','dse~CardioStatsRelayTwo@1','dse~FinanceSequenceMar26OAI2@1']
packets=[]
for sid in seeds:
 seed=next(r for r in revs if r['rev_id']==sid)
 same=sorted([r for r in revs if r['page_id']==seed['page_id']],key=lambda r:r['seq'])
 refs=sorted([r for r in revs if r['page_id']!=seed['page_id'] and seed['name'] in r['body']],key=lambda r:(r['time'],r['rev_id']))
 def keep(r):return {k:r[k] for k in ['rev_id','page_id','seq','time','time_grade','uncertainty_seconds','body','diff_base']}
 packets.append({'seed':sid,'same_page':[keep(r) for r in same],'exact_name_references':[keep(r) for r in refs],'limit':'Exact-name search misses aliases and external signals; stored timestamps do not establish individual task-clock alignment.'})
(O/'wiki_episode_histories.jsonl').write_text(''.join(json.dumps(p)+'\n' for p in packets))
s=BeautifulSoup((R/'data/raw/metr/report.html').read_text(),'html.parser');ps=s.find_all('p');hf=[]
for name,a,b in [('self_risk',28,30),('tripwire_choice',186,198),('motivational_alternatives',222,229),('refusal_and_peer_veto',229,240)]:
 start=ps[a];end=ps[b];nodes=[];cur=start
 while cur is not None and cur is not end:
  if getattr(cur,'name',None):nodes.append({'tag':cur.name,'text':cur.get_text(' ',strip=True)})
  cur=cur.next_sibling
 hf.append({'episode':name,'paragraph_start':a,'paragraph_end_exclusive':b,'nodes':nodes,'source':'https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/','evidence_limit':'Publication selection; quoted and paraphrased reasoning embedded in investigator narrative, not full raw transcripts.'})
(O/'hf_episode_context.json').write_text(json.dumps(hf,indent=2)+'\n')
manifest={'inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'data/raw/metr/report.html',R/'data/raw/wiki/revisions.jsonl.gz',O/'episode_predictions_v1.md']},'wiki_coverage':[{'seed':p['seed'],'same_page_revisions':len(p['same_page']),'exact_name_reference_revisions':len(p['exact_name_references'])} for p in packets]}
(O/'episode_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest['wiki_coverage']))
