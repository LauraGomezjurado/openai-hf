"""Amended sensitivity: include first hour after read, omitted by whole-hour landmarks."""
import numpy as np
from audit_public_data import js_json
from analysis_common import ROOT,save_csv,save_json,glm_predict,binary_scores


def main():
    agents=js_json(ROOT/'data/raw/metr/agent-data.js','AGENT_TIMELINE_DATA')['agents']
    rows=[]
    for i,a in enumerate(agents):
        read=a['read']/3600;end=a['end']/3600
        onset=a['hfStart']/3600 if a['hfStart'] is not None else None
        if onset is not None and onset<=read:continue
        for offset in range(int(np.ceil(end-read))):
            t=read+offset
            if onset is not None and onset<=t:break
            y=int(onset is not None and t<onset<=t+1)
            if end<t+1 and not y:continue
            rows.append([i,t,y,int(a['family']=='s'),np.log1p(t-a['start']/3600),np.log1p(offset)])
    z=np.array(rows);ids=z[:,0].astype(int);t=z[:,1];y=z[:,2]
    base=np.column_stack([t/24,np.sin(2*np.pi*t/24),np.cos(2*np.pi*t/24),z[:,3],z[:,4]])
    enhanced=np.column_stack([base,z[:,5]])
    preds=[];fits=[]
    first=int(np.ceil((t.min()+24)/12)*12)
    for cutoff in range(first,int(t.max())+1,12):
        train=t+1<=cutoff;test=(t>=cutoff)&(t<cutoff+12)
        if not test.any() or y[train].sum()<5:continue
        seen=set(ids[train])
        for model,x in [('calendar_run_age',base),('plus_board_tenure',enhanced),('training_mean',None)]:
            if x is None:p=np.full(test.sum(),y[train].mean());fit={'converged':True,'iterations':0,'max_abs_coefficient':0}
            else:p,fit=glm_predict(x[train],y[train],x[test],'logistic')
            fits.append({'cutoff':cutoff,'model':model,**fit})
            for j,prob in zip(np.where(test)[0],p):
                preds.append({'model':model,'cutoff':cutoff,'row_id':int(ids[j]),'hour':float(t[j]),'outcome':int(y[j]),'probability':float(prob),'unseen_row':ids[j] not in seen})
    save_csv('read_anchored_predictions.csv',preds);save_csv('read_anchored_fits.csv',fits)
    scores=[]
    for model in ['calendar_run_age','plus_board_tenure','training_mean']:
        for scope in ['all','unseen_rows']:
            p=[r for r in preds if r['model']==model and (scope=='all' or r['unseen_row'])]
            scores.append({'model':model,'scope':scope,'intervals':len(p),'positives':sum(r['outcome'] for r in p),**binary_scores(np.array([r['outcome'] for r in p]),np.array([r['probability'] for r in p]))})
    save_csv('read_anchored_scores.csv',scores)
    save_json('read_anchored_summary.json',{'reason_for_amendment':'Whole-hour landmarks omitted 99 post-read onsets before the next clock hour, plus 15 pre-read onsets. Read-anchored intervals retain all 669 positive-lag onsets.',
        'intervals':len(rows),'positive_intervals':int(y.sum()),'scores':scores,
        'limitations':'Same selected source, uncertain labels, repeated dependent intervals and informative followup endings. Retrospective diagnostic, not deployment evaluation.'})
    print('Read-anchored analysis:',scores)


if __name__=='__main__':main()
