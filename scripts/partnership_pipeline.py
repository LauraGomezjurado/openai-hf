"""Offline planning and partner-result analysis; never calls a model."""
import argparse,csv,hashlib,json,math,random
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'results/partnership'
ARMS=['baseline','authority_clarification','neutral_reminder']
ENDPOINTS=['scope_violation','task_success','useful_assistance']

def analyze(rows):
    if not rows:raise ValueError('Empty outcomes')
    seen=set();groups={}
    for r in rows:
        for k in ['family_id','run_id','arm']:
            if not isinstance(r.get(k),str) or not r[k]:raise ValueError('Missing identifier')
        if r['run_id'] in seen:raise ValueError('Duplicate run ID')
        seen.add(r['run_id'])
        if r['arm'] not in ARMS:raise ValueError('Unknown arm')
        for e in ENDPOINTS:
            if e not in r or (r[e] is not None and type(r[e]) is not bool):raise ValueError('Outcome must be boolean or null')
        groups.setdefault(r['family_id'],{}).setdefault(r['arm'],[]).append(r)
    for g in groups.values():
        if set(g)!=set(ARMS) or any(len(g[a])!=5 for a in ARMS):raise ValueError('Require five runs per family per arm')
    out=[]
    for e in ENDPOINTS:
        for arm in ARMS[1:]:
            diffs=[];bounds=[];missing=0
            for fid,g in sorted(groups.items()):
                t=[x[e] for x in g[arm]];b=[x[e] for x in g['baseline']]
                tm=t.count(None);bm=b.count(None);missing+=tm+bm
                ts=sum(v is True for v in t);bs=sum(v is True for v in b)
                bounds.append(((ts-bs-bm)/5,(ts+tm-bs)/5))
                if not tm and not bm:diffs.append((ts-bs)/5)
            n=len(diffs);ci=None
            if n>=2:
                rng=random.Random(442);boot=sorted(sum(rng.choice(diffs) for _ in diffs)/n for _ in range(4000))
                ci=[boot[99],boot[3899]]
            out.append(dict(endpoint=e,comparison=arm+' - baseline',families_total=len(groups),complete_families=n,
                excluded_families=len(groups)-n,missing_runs_in_pair=missing,
                complete_family_risk_difference=sum(diffs)/n if n else None,
                exploratory_family_bootstrap_95_interval=ci,
                all_family_missing_outcome_bounds=[sum(x[i] for x in bounds)/len(bounds) for i in [0,1]],
                warning='Complete-case estimate may be selected; bounds address missing outcomes only. Pilot intervals do not establish generalization or causal validity.'))
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--outcomes',type=Path);a=p.parse_args();O.mkdir(exist_ok=True,parents=True)
    readiness={'original_model_access':False,'approved_original_prefixes':0,'independently_adjudicated_outcomes':0,
        'authorized_work_monitor_denominator_available':False,'outreach_sent':False,
        'status':'Engineering/planning ready; causal and monitoring experiments awaiting partner access',
        'available_source_hashes':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [R/'data/raw/metr/report.html',R/'data/raw/wiki/revisions.jsonl.gz']}}
    (O/'readiness.json').write_text(json.dumps(readiness,indent=2)+'\n')
    alloc=[dict(family_id=f'PROPOSED-{i:02}',arm=arm,continuation=j,run_id=f'PROPOSED-{i:02}-{arm}-{j}') for i in range(1,13) for arm in ARMS for j in range(1,6)]
    random.Random(829).shuffle(alloc)
    with (O/'allocation.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(alloc[0]));w.writeheader();w.writerows(alloc)
    planning=[]
    for sd in [.10,.20,.30,.50]:
        for half in [.05,.10]:
            planning.append(dict(assumed_sd_of_family_risk_difference=sd,target_95_interval_halfwidth=half,
                approximate_independent_families=math.ceil((1.96*sd/half)**2),
                caveat='Normal approximation with assumed known variance; not power or empirical variance'))
    with (O/'planning.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(planning[0]));w.writeheader();w.writerows(planning)
    if a.outcomes:
        analysis=analyze([json.loads(l) for l in a.outcomes.read_text().splitlines() if l.strip()])
        (O/'partner_analysis.json').write_text(json.dumps({'input_sha256':hashlib.sha256(a.outcomes.read_bytes()).hexdigest(),'results':analysis},indent=2,allow_nan=False)+'\n')
    print('Wrote readiness, proposed 180-run allocation and 8 precision scenarios. Model calls: 0.')
if __name__=='__main__':main()
