"""Quantify retrieval coverage, not motivational prevalence or causal effects."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'results/cooperation'
hits=list(map(json.loads,(O/'discriminating_hits.jsonl').read_text().splitlines()))
rows=[]
for test,flag in [('personal_sacrifice','cost_choice'),('benefit_ends','benefit_ends'),('peer_authority','authority')]:
 a=[r for r in hits if flag in r['flags']]
 rows.append({'test':test,'retrieved_additions':len(a),'pages':len({r['page_id'] for r in a}),'link_copy_components':len({r['component_id'] for r in a}),'strict_effect_estimate':None,'reason':'No validated exposure/outcome comparison with required benefit, cost or authority evidence.'})
union=[r for r in hits if set(r['flags'])&{'cost_choice','benefit_ends','authority'}]
result={'source_sha256':hashlib.sha256((O/'discriminating_hits.jsonl').read_bytes()).hexdigest(),'tests':rows,'union_additions':len(union),'union_pages':len({r['page_id'] for r in union}),'union_components':len({r['component_id'] for r in union}),'eligible_unique_additions':10316,'warning':'Counts are frozen-rule retrieval coverage. Components are leakage groupings, not independent agents or causal units. No binomial confidence intervals justified. All 50 hit additions screened in this pass; some long replacements only partially displayed; no claim of exhaustive semantic audit.'}
(O/'ambitious_quantitative_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
