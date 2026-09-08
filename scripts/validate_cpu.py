"""Meaningful integrity/forecast checks, plus small estimator sanity controls."""
import csv
import json
import sys
import platform
import hashlib
import numpy as np
import scipy
import matplotlib
from analysis_common import ROOT,OUT,save_json,glm_predict,binary_scores,count_scores


def rows(name):return list(csv.DictReader((OUT/name).open()))


def main():
    checks=[]
    for s in json.loads((ROOT/'data/source_manifest.json').read_text()):
        assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
    checks.append('All original source hashes match the frozen manifest')
    for r in rows('timing_sensitivity.csv'):
        assert 0<=float(r['lower'])<=float(r['upper'])<=1
        assert int(r['guaranteed_recorded_onsets'])<=int(r['possible_recorded_or_early_ended_onsets'])<=int(r['nominal_risk_rows'])
    checks.append('Every timing bound is ordered and uses a valid denominator')
    for file,fold in [('onset_predictions.csv','fold_start_hour'),('read_anchored_predictions.csv','cutoff')]:
        seen=set()
        for r in rows(file):
            assert float(r[fold])<=float(r['hour'])<float(r[fold])+12
            assert 0<=float(r['probability'])<=1
            key=(r['model'],r['row_id'],r['hour']);assert key not in seen;seen.add(key)
    checks.append('Onset predictions have unique keys, valid probabilities, and lie inside held-out time blocks')
    for r in rows('workstream_predictions.csv'):
        assert float(r['fold_start_hour'])<=float(r['target_start_hour'])<float(r['fold_start_hour'])+12
        assert np.isfinite(float(r['prediction'])) and float(r['prediction'])>=0
    checks.append('Workstream forecasts are finite and in their temporal test block')
    wiki=json.loads((OUT/'wiki_preparation_summary.json').read_text())
    assert wiki['recomputed_hunks_exactly_match_published']==14591
    packet=rows('wiki_annotation_sample_50.csv');assert len(packet)==50 and len({r['page_id'] for r in packet})==50
    splits={}
    for r in packet:
        assert not r['human_label']
        if r['component_id'] in splits:assert splits[r['component_id']]==r['split']
        splits[r['component_id']]=r['split']
    checks.append('All wiki hunks exactly reproduced; 50 unique pages; no component split leakage in sample; no invented human labels')
    anchored=json.loads((OUT/'read_anchored_summary.json').read_text());assert anchored['positive_intervals']==669
    checks.append('Read-anchored risk set retains all 669 positive-lag positioned onsets')
    # Arithmetic controls, not simulated incident trajectories.
    x=np.zeros((100,2));y=np.tile([0.,1.,0.,0.],25)
    p,_=glm_predict(x,y,x[:4],'logistic');assert np.max(np.abs(p-.25))<1e-4
    p,_=glm_predict(x,np.full(100,3.),x[:4],'poisson');assert np.max(np.abs(p-3))<1e-4
    x=np.linspace(-2,2,200)[:,None];y=(x[:,0]>0).astype(float)
    p,_=glm_predict(x,y,np.array([[-2.],[2.]]),'logistic');assert p[0]<.1 and p[1]>.9
    assert binary_scores(np.array([0,1]),np.array([0,1]))['brier']==0
    assert abs(count_scores(np.array([0,1,3]),np.array([0,1,3]))['poisson_deviance'])<1e-7
    checks.append('GLMs recover constant means and a directional signal; scoring identities pass')
    for name in ['onset_glm_fits.csv','read_anchored_fits.csv','workstream_fit_diagnostics.csv']:
        assert all(r['converged']=='True' for r in rows(name))
        assert all(float(r['max_abs_coefficient'])<24.9 for r in rows(name))
    checks.append('All fitted models converged without reaching coefficient safeguards')
    save_json('validation.json',{'passed':True,'checks':checks,'python':sys.version,'platform':platform.platform(),
        'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__}})
    manifest=[]
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name!='output_manifest.json':
            manifest.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    save_json('output_manifest.json',manifest)
    print('PASS:',len(checks),'integrity and estimator checks')


if __name__=='__main__':main()
