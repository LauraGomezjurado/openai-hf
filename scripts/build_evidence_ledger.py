"""Selected HF publication annotations and explicitly provisional wiki link review."""
import csv
import datetime as dt
from audit_public_data import js_json
from analysis_common import ROOT,OUT,save_csv,save_json


def main():
    d=js_json(ROOT/'data/raw/metr/agent-data.js','AGENT_TIMELINE_DATA')
    base=dt.datetime.fromisoformat(d['windowStart'].replace('Z','+00:00'))
    rows=[]
    for i,a in enumerate(d['annotations']):
        text=a.get('quote') or a.get('paraphrase') or a.get('detail') or a['title']
        typ='selected_agent_quote' if 'quote' in a else ('investigator_paraphrase' if 'paraphrase' in a else 'investigator_event_annotation')
        interpretation={0:'External storage affordance noticed',1:'Possible peer communication inferred',2:'Coordination after reading a predecessor dossier',
            3:'Access discovery announced',4:'Board information connected to access search',5:'File-read capability reported',
            6:'Scorer-source interest linked to participation',7:'Broader collective benefit mentioned',8:'Participation inclination after encountering group activity',
            9:'Code execution milestone',10:'Access loss mentioned',11:'Service unavailability mentioned'}[i]
        rows.append({'ledger_id':f'HF-A{i:02d}','snapshot_agent_row':a['agent'],
            'reconstructed_utc':(base+dt.timedelta(seconds=a['time'])).isoformat(),
            'source_type':typ,'source_text':text,'source_title':a['title'],
            'source_url':'https://metr.org/assets/js/agent_timeline/data.js',
            'source_selector':f'AGENT_TIMELINE_DATA.annotations[{i}]',
            'working_interpretation':interpretation,
            'evidence_limit':'Selected publication passage; no full preceding context, independent counterfactual, or verified mental-state access.',
            'review_status':'assistant initial coding; not independently human-adjudicated'})
    save_csv('hf_annotation_ledger.csv',rows)
    candidates=list(csv.DictReader((OUT/'wiki_linked_uptake_candidates.csv').open()))
    reviews=[]
    for r in candidates:
        false=r['later_rev_id']=='dse~OECDEquityMar13Live@9'
        r.update({'reviewer':'assistant; one-pass provisional semantic review',
            'decision':'reject_as_specific_uptake_link' if false else 'retain_as_self_reported_page_corroboration',
            'reason':('Link is in a timing/coordination paragraph; replication claim occurs separately. The lexical rule conflated topics.' if false else
                'Later text explicitly claims independent replication and cites the earlier page. This supports claimed corroboration, not causal uptake or verified execution.'),
            'provenance_caution':'Earlier ID is latest available page revision, not necessarily the particular message being cited. Use full page snapshot/history; do not equate its added text with the referenced evidence.',
            'distinct_agents_verified':False,'execution_verified':False,'reward_verified':False})
        reviews.append(r)
    save_csv('wiki_uptake_review.csv',reviews)
    save_json('evidence_ledger_summary.json',{'hf_selected_annotations':len(rows),'hf_source_types':{t:sum(r['source_type']==t for r in rows) for t in set(r['source_type'] for r in rows)},
        'wiki_candidate_links':len(reviews),'wiki_rejected_specific_links':sum(r['decision'].startswith('reject') for r in reviews),
        'wiki_corroboration_links':sum(r['decision'].startswith('retain') for r in reviews),
        'unique_later_posts_retained':len({r['later_rev_id'] for r in reviews if r['decision'].startswith('retain')}),
        'independent_human_adjudication':False})


if __name__=='__main__':main()
