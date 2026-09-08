"""Timing/missingness, finite-record sensitivity, and exploratory temporal prediction."""
import collections
import datetime as dt
import numpy as np
from audit_public_data import js_json
from analysis_common import ROOT,OUT,save_json,save_csv,glm_predict,binary_scores
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    d=js_json(ROOT/'data/raw/metr/agent-data.js','AGENT_TIMELINE_DATA');a=d['agents']
    n=len(a); read=np.array([x['read'] for x in a])/3600;end=np.array([x['end'] for x in a])/3600
    onset=np.array([np.nan if x['hfStart'] is None else x['hfStart']/3600 for x in a])
    lag=onset-read;follow=end-read;finite=np.isfinite(lag);risk=~finite|(lag>0)
    day=(read//24).astype(int)+6
    fam=np.array([x['family'] for x in a]); featured=np.isin(np.arange(n),d['featuredAgents'])
    checks=[]
    for i,x in enumerate(a):
        for tag,l,r in [('write_before_read','write','read'),('onset_before_read','hfStart','read'),
                        ('write_after_end','write','end'),('read_before_start','read','start')]:
            if x[l] is not None and ((x[l]>x[r]) if tag=='write_after_end' else (x[l]<x[r])):
                checks.append({'row_id':i,'family':x['family'],'issue':tag,'difference_minutes':(x[l]-x[r])/60})
    save_csv('timeline_ordering_issues.csv',checks)
    missing=[]
    for scope,mask in [('all',np.ones(n,bool)),('HPIM',fam=='h'),('Sol',fam=='s')]+[(f'July {k}',day==k) for k in sorted(set(day))]:
        indices=np.where(mask)[0]
        missing.append({'group':scope,'rows':len(indices),'onset_missing':int(np.sum(~finite[mask])),
                        'write_missing':sum(a[i]['write'] is None for i in indices),
                        'onset_before_read':int(np.sum(lag[mask]<0)),
                        'observed_stop':sum(a[i]['observedStop'] for i in indices),
                        'end_at_plot_boundary':sum(a[i]['end']==691200 for i in indices),
                        'median_followup_hours':float(np.median(follow[mask]))})
    save_csv('missingness_by_group.csv',missing)

    sensitivity=[]
    for group,groupmask in [('all',np.ones(n,bool)),('without_featured',~featured),('HPIM',fam=='h'),('Sol',fam=='s')]:
        for k in sorted(set(day)):
            m=(day==k)&risk&groupmask; denom=int(m.sum())
            if not denom:continue
            for horizon in [1,6,24]:
                for minutes in [0,5,30,120]:
                    err=2*minutes/60
                    guaranteed=finite&(lag-err>0)&(lag+err<=horizon)
                    possible=finite&(lag+err>0)&(lag-err<=horizon)
                    # Unknown future classification only where observed followup may end early.
                    early_unknown=(~finite)&(follow-err<horizon)
                    sensitivity.append({'group':group,'read_day':k,'horizon_hours':horizon,
                        'per_timestamp_error_minutes':minutes,'nominal_risk_rows':denom,
                        'guaranteed_recorded_onsets':int(np.sum(m&guaranteed)),
                        'possible_recorded_or_early_ended_onsets':int(np.sum(m&(possible|early_unknown))),
                        'lower':float(np.sum(m&guaranteed)/denom),'upper':float(np.sum(m&(possible|early_unknown))/denom),
                        'ambiguous_ordering_rows':int(np.sum(m&finite&(lag-err<=0))),
                        'read_date_boundary_ambiguous':int(np.sum(m&(np.minimum(read%24,24-read%24)<=minutes/60)))})
    save_csv('timing_sensitivity.csv',sensitivity)

    # Label-missingness stress test: arbitrary added positive labels among otherwise known negatives.
    labeltests=[]
    for fraction in [0,.01,.05,.1,.2]:
        rr=[]
        for k in [9,11]:
            m=(day==k)&risk;N=int(m.sum());pos=int(np.sum(m&finite&(lag<=1)));unknown=int(np.sum(m&~finite&(follow<1)))
            extra=int(np.ceil(fraction*(N-pos-unknown)))
            rr.append((pos/N,(pos+unknown+extra)/N))
        labeltests.append({'assumed_fraction_of_remaining_negative_labels_wrong':fraction,
            'July11_minus_July9_lower_pp':100*(rr[1][0]-rr[0][1]),
            'July11_minus_July9_upper_pp':100*(rr[1][1]-rr[0][0])})
    save_csv('missing_label_sensitivity.csv',labeltests)

    fig,axs=plt.subplots(1,2,figsize=(11,4.9))
    for k,color in [(9,'#536b7b'),(11,'#a74d2d')]:
        m=(day==k)&risk;N=m.sum();hs=np.linspace(.01,24,240)
        lo=np.array([np.sum(m&finite&(lag<=h))/N for h in hs]);up=np.array([np.sum(m&((finite&(lag<=h))|(~finite&(follow<h))))/N for h in hs])
        axs[0].plot(hs,lo*100,label=f'July {k}, n={N}',color=color);axs[0].fill_between(hs,lo*100,up*100,color=color,alpha=.15)
    axs[0].set(xlabel='Hours since first recorded board read',ylabel='Recorded onset / nominal risk rows (%)',title='Follow-up availability ranges');axs[0].legend()
    for k,color in [(9,'#536b7b'),(11,'#a74d2d')]:
        ss=[x for x in sensitivity if x['group']=='all' and x['read_day']==k and x['horizon_hours']==1]
        xs=np.arange(4)+(-.08 if k==9 else .08)
        axs[1].vlines(xs,[x['lower']*100 for x in ss],[x['upper']*100 for x in ss],color=color,lw=3)
        axs[1].scatter(xs,[x['lower']*100 for x in ss],color=color)
    axs[1].set_xticks(range(4),['0','5','30','120']);axs[1].set(xlabel='Assumed per-timestamp error (±minutes)',ylabel='Within-one-hour onset range (%)',title='Timing stress test; nominal cohorts fixed')
    for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
    fig.suptitle('Hugging Face recruitment: what the published records identify',fontsize=14)
    fig.text(.08,.015,'Source: METR figure data, July 8–13, 2026. Ranges are not confidence intervals; classification errors are excluded.\nCohorts/risk sets use point estimates. Timestamp sensitivity is analyst-chosen, not a measured error distribution.',fontsize=8)
    fig.tight_layout(rect=(0,.1,1,.94));fig.savefig(OUT/'timing_sensitivity.png',dpi=180);plt.close(fig)

    # Hourly landmarks; all feature histories are available at t, labels resolve by t+1.
    landmarks=[]
    for i,x in enumerate(a):
        for t in range(int(np.ceil(read[i])),int(np.ceil(end[i]))):
            if finite[i] and onset[i]<=t: continue
            y=int(finite[i] and t<onset[i]<=t+1)
            if end[i]<t+1 and not y:continue
            landmarks.append((i,t,y,x['family']=='s',np.log1p(t-x['start']/3600),np.log1p(t-read[i])))
    z=np.array(landmarks);ids=z[:,0].astype(int);t=z[:,1];y=z[:,2]
    baseline=np.column_stack([t/24,np.sin(2*np.pi*t/24),np.cos(2*np.pi*t/24),z[:,3],z[:,4]])
    enhanced=np.column_stack([baseline,z[:,5]])
    predictions=[];fits=[]
    first=int(np.ceil((t.min()+24)/12)*12)
    for cutoff in range(first,int(t.max())+1,12):
        train=t+1<=cutoff;test=(t>=cutoff)&(t<cutoff+12)
        if not test.any() or y[train].sum()<5:continue
        seen=set(ids[train])
        for model,features in [('calendar_run_age',baseline),('plus_board_tenure',enhanced),('training_mean',None)]:
            if features is None:
                p=np.full(int(test.sum()),float(y[train].mean()));fit={'converged':True,'iterations':0,'max_abs_coefficient':0.0}
            else:
                p,fit=glm_predict(features[train],y[train],features[test],'logistic')
            fits.append({'model':model,'cutoff_hour':cutoff,'train_intervals':int(train.sum()),'test_intervals':int(test.sum()),**fit})
            for j,prob in zip(np.where(test)[0],p):
                predictions.append({'model':model,'fold_start_hour':cutoff,'row_id':int(ids[j]),'hour':float(t[j]),'outcome':int(y[j]),'probability':float(prob),'unseen_row':ids[j] not in seen})
    save_csv('onset_predictions.csv',predictions);save_csv('onset_glm_fits.csv',fits)
    scores=[]
    for model in ['calendar_run_age','plus_board_tenure','training_mean']:
        for scope in ['all','unseen_rows']:
            pp=[p for p in predictions if p['model']==model and (scope=='all' or p['unseen_row'])]
            if pp:scores.append({'model':model,'scope':scope,'intervals':len(pp),'positives':sum(p['outcome'] for p in pp),**binary_scores(np.array([p['outcome'] for p in pp]),np.array([p['probability'] for p in pp]))})
    save_csv('onset_prediction_scores.csv',scores)
    folds=[]
    for (model,cutoff) in sorted({(p['model'],p['fold_start_hour']) for p in predictions}):
        pp=[p for p in predictions if p['model']==model and p['fold_start_hour']==cutoff]
        folds.append({'model':model,'fold_start_hour':cutoff,'intervals':len(pp),'positives':sum(p['outcome'] for p in pp),**binary_scores(np.array([p['outcome'] for p in pp]),np.array([p['probability'] for p in pp]))})
    save_csv('onset_prediction_folds.csv',folds)
    save_json('timing_summary.json',{'ordering_issue_counts':dict(collections.Counter(x['issue'] for x in checks)),
        'largest_negative_onset_lag_hours':float(np.nanmin(lag)), 'plot_boundary_ends':sum(x['end']==691200 for x in a),
        'nominal_risk_rows':int(risk.sum()),'landmark_intervals':len(landmarks),'landmark_positive_intervals':int(y.sum()),
        'positioned_onsets_not_in_landmarks':int(finite.sum()-y.sum()),
        'limitations':['Landmarks omit onsets before first whole-hour boundary after read, including immediate onsets.',
            'Negative intervals require full observed followup; truncation can be informative.',
            'No untreated agents; source population includes only eventual board readers.',
            'No individual timestamp quality grades or participation label validation.'], 'prediction_scores':scores})
    print('Timing complete:',scores)


if __name__=='__main__':main()
