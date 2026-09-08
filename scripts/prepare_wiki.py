"""Prepare real historical revisions for annotation; no inferred truth labels."""
import collections
import difflib
import gzip
import hashlib
import json
import random
import re
from analysis_common import ROOT,OUT,save_csv,save_json

PATTERNS={
    'evaluator_belief':r'\b(?:scorer|scoring|evaluator|graded|reward|correctness feedback|score feedback)\b',
    'claimed_uptake':r'\b(?:reproduced|replicated|confirmed your|your (?:method|bypass|trick)|saw .{0,35}report|worked for me|thanks.{0,35}(?:works|worked))\b',
    'correction_or_dispute':r'\b(?:incorrect|correction|contrary|disagree|dispute|wrong|retract|not confirmed)\b',
    'peer_request':r'\b(?:please (?:share|relay|post|confirm|report)|anyone|any cohort|other agents|collective|swarm)\b',
    'boundary_or_access':r'\b(?:bypass|sandbox|proxy|permission|blocked|restriction)\b',
    'termination_belief':r'\b(?:terminate|termination|heartbeat|deadman|episode ends|final round)\b',
}


def main():
    revisions=[json.loads(l) for l in gzip.open(ROOT/'data/raw/wiki/revisions.jsonl.gz','rt')]
    lookup={r['rev_id']:r for r in revisions}
    pages={r['page_id'] for r in revisions};parent={p:p for p in pages}
    def find(p):
        while parent[p]!=p:parent[p]=parent[parent[p]];p=parent[p]
        return p
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    deltas=[];unknown=0;verified_hunks=0
    for r in sorted(revisions,key=lambda r:(r['time'],r['rev_id'])):
        new=r['body'].split('\n');base=lookup.get(r['diff_base'])
        known=base is not None or r['diff_base_reason']=='page_created'
        if not known:unknown+=1
        old=base['body'].split('\n') if base else []
        # Recompute rather than assuming source hunk line-ending conventions.
        ops=difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes()
        reconstructed=[];added=[];removed=[]
        for op,a0,a1,b0,b1 in ops:
            reconstructed.extend(old[a0:a1] if op=='equal' else new[b0:b1])
            if op in ['insert','replace']:added.extend(new[b0:b1])
            if op in ['delete','replace']:removed.extend(old[a0:a1])
        assert reconstructed==new
        own_hunks=[dict(op=op,a0=a0,a1=a1,b0=b0,b1=b1) for op,a0,a1,b0,b1 in ops if op!='equal']
        assert own_hunks==r['hunks'], f"Source hunk mismatch: {r['rev_id']}"
        verified_hunks+=1
        addition='\n'.join(added) if known else ''
        flags=[key for key,pattern in PATTERNS.items() if re.search(pattern,addition,re.I|re.S)]
        name=r['name'].lower()
        topic=next((p for p in ['oecd','healthdata','ihme','datausa','uefa'] if p in name),'other')
        for target in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]',r['body']):
            candidate=r['wiki']+'/'+target.strip()
            if candidate in pages:union(r['page_id'],candidate)
        deltas.append({'rev_id':r['rev_id'],'page_id':r['page_id'],'page_key':r['page_key'],'time':r['time'],
            'time_grade':r['time_grade'],'uncertainty_seconds':r['uncertainty_seconds'],
            'baseline_known':known,'diff_base':r['diff_base'],'topic_proxy':topic,
            'addition':addition,'removed_text':'\n'.join(removed) if known else '',
            'addition_sha256':hashlib.sha256(addition.encode()).hexdigest() if addition else None,
            'full_body_chars':len(r['body']),'added_chars':len(addition),'lexical_candidates':flags,
            'source_url':'https://collusion.wiki/explorer/page/'+r['page_key']+'.html#rev-'+str(r['seq'])})
    # Connect exact duplicate substantive additions to avoid splitting copied passages.
    first={}
    for row in deltas:
        if len(row['addition'])>=80:
            h=row['addition_sha256']
            if h in first:union(row['page_id'],first[h])
            else:first[h]=row['page_id']
    component_pages=collections.Counter(find(p) for p in pages)
    first_addition={};duplicates=0
    for row in deltas:
        root=find(row['page_id']);cid=hashlib.sha256(root.encode()).hexdigest()[:16]
        row['component_id']=cid;row['component_pages']=component_pages[root]
        row['split']='holdout' if int(cid,16)%5==0 else 'development'
        h=row['addition_sha256'];row['earlier_identical_addition']=first_addition.get(h) if h else None
        if h:
            if h in first_addition:duplicates+=1
            else:first_addition[h]=row['rev_id']
    with gzip.open(OUT/'wiki_revision_deltas.jsonl.gz','wt') as f:
        for row in deltas:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    # Eligible sample: unique substantive additions with known baseline, one per page.
    eligible=[r for r in deltas if r['baseline_known'] and r['added_chars']>=80 and not r['earlier_identical_addition']]
    buckets=collections.defaultdict(list)
    for row in eligible:buckets[(row['topic_proxy'],row['time'][:10])].append(row)
    rng=random.Random(20260906);keys=sorted(buckets)
    for b in buckets.values():rng.shuffle(b)
    chosen=[];selected_pages=set()
    while len(chosen)<50 and any(buckets.values()):
        for key in keys:
            while buckets[key]:
                row=buckets[key].pop()
                if row['page_id'] not in selected_pages:
                    chosen.append(row);selected_pages.add(row['page_id']);break
            if len(chosen)==50:break
    packet=[]
    for r in chosen:
        packet.append({k:r[k] for k in ['rev_id','page_id','component_id','split','time','time_grade','source_url','topic_proxy']}|
                      {'sampling':'topic-date round robin; one revision per page; not prevalence representative',
                       'addition':r['addition'],'lexical_candidates':';'.join(r['lexical_candidates']),
                       'human_label':'','evidence_span':'','alternative_explanation':'','adjudication':''})
    save_csv('wiki_annotation_sample_50.csv',packet)
    # A separate purposive packet must never be merged into the random-stratified denominator.
    purposive=[];used=set()
    for flag in PATTERNS:
        candidates=[r for r in eligible if flag in r['lexical_candidates']]
        candidates.sort(key=lambda r:(-len(r['lexical_candidates']),r['time'],r['rev_id']))
        for r in candidates:
            if r['page_id'] in used:continue
            purposive.append({'retrieval_flag':flag,'rev_id':r['rev_id'],'page_id':r['page_id'],
                'time':r['time'],'source_url':r['source_url'],'addition':r['addition'],
                'status':'unreviewed lexical candidate; not a behavioral label'})
            used.add(r['page_id'])
            if sum(p['retrieval_flag']==flag for p in purposive)>=5:break
    save_csv('wiki_purposive_candidates.csv',purposive)
    # Explicit link + later lexical acknowledgement candidates; never inferred read events.
    edges=[]
    by_name={p.split('/',1)[1]:p for p in pages}
    prior=collections.defaultdict(list)
    for r in deltas:
        if 'claimed_uptake' in r['lexical_candidates']:
            targets=re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]',r['addition'])
            for target in targets:
                p=r['page_id'].split('/',1)[0]+'/'+target.strip()
                if p in prior and prior[p]:
                    before=prior[p][-1]
                    edges.append({'earlier_rev_id':before['rev_id'],'later_rev_id':r['rev_id'],
                        'earlier_time':before['time'],'later_time':r['time'],
                        'basis':'later addition links page and matches uptake vocabulary',
                        'status':'candidate only; no demonstrated read, distinct actor, or executed action'})
        if r['addition']:prior[r['page_id']].append(r)
    save_csv('wiki_linked_uptake_candidates.csv',edges)
    save_json('wiki_preparation_summary.json',{'revisions':len(revisions),'known_diff_baselines':len(revisions)-unknown,
        'unknown_diff_baselines':unknown,'recomputed_hunks_exactly_match_published':verified_hunks,
        'full_body_chars':sum(r['full_body_chars'] for r in deltas),'known_addition_chars':sum(r['added_chars'] for r in deltas),
        'duplicate_nonempty_additions':duplicates,'unique_substantive_known_additions':len(eligible),
        'lexical_candidate_counts':{flag:sum(flag in r['lexical_candidates'] for r in eligible) for flag in PATTERNS},
        'components':len(component_pages),'largest_component_pages':max(component_pages.values()),
        'sample_rows':len(packet),'sample_components':len({r['component_id'] for r in packet}),
        'sample_splits':dict(collections.Counter(r['split'] for r in packet)),
        'purposive_candidates':len(purposive),'linked_uptake_candidates':len(edges),
        'independent_human_labels':0,'split_caution':'Links plus exact-copy components cannot catch paraphrases or missing links; splits remain provisional.'})
    save_json('wiki_retrieval_rules.json',PATTERNS)
    print('Wiki preparation complete:',len(packet),'sample rows;',len(edges),'unreviewed uptake candidates')


if __name__=='__main__':main()
