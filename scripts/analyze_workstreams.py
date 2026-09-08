"""Provisional ecological forecasts. No message-to-agent linkage is implied."""
import numpy as np
from scipy.stats import spearmanr
from audit_public_data import js_json
from analysis_common import ROOT,OUT,save_csv,save_json,glm_predict,count_scores
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    d=js_json(ROOT/'data/raw/metr/workstream-data.js','WORKSTREAM_TRAFFIC_DATA')
    agents=js_json(ROOT/'data/raw/metr/agent-data.js','AGENT_TIMELINE_DATA')['agents']
    # Agent epoch is July 6; traffic epoch July 8.
    onsets=np.array([a['hfStart']/3600-48 for a in agents if a['hfStart'] is not None])
    cube=np.zeros((144,len(d['leaves']),len(d['categories'])),int)
    seen=set()
    for h,w,counts in d['rows']:
        assert (h,w) not in seen;seen.add((h,w));cube[h,w]=counts
    purposes=[c['id'] for c in d['categories']];hf=np.array([l['family']=='hf' for l in d['leaves']])
    result_idx=purposes.index('result_or_breakthrough');assignment_idx=purposes.index('assignment')
    summary=[];predictions=[];fitlog=[]
    for bin_hours in [1,2,6]:
        bins=144//bin_hours; starts=np.arange(bins)*bin_hours
        for exclude in [False,True]:
            work=cube.copy()
            if exclude:
                work[:,:,purposes.index('automated_log')]=0;work[:,:,purposes.index('file_or_artifact')]=0
            aggregated=work.reshape(bins,bin_hours,work.shape[1],work.shape[2]).sum(axis=1)
            total=aggregated.sum(axis=(1,2));hf_results=aggregated[:,hf,result_idx].sum(axis=1)
            assignments=aggregated[:,:,assignment_idx].sum(axis=1)
            for shift in [-2,-1,0,1,2]:
                y=np.histogram(onsets+shift,bins=np.arange(0,145,bin_hours))[0].astype(float)
                # Feature row j uses only the completed bin j-1, not current traffic.
                prev=np.r_[0,y[:-1]];vol=np.r_[0,total[:-1]]
                baseline=np.column_stack([starts/24,np.sin(2*np.pi*starts/24),np.cos(2*np.pi*starts/24),np.log1p(prev),np.log1p(vol)])
                augmented=np.column_stack([baseline,np.r_[0,hf_results[:-1]/np.maximum(1,total[:-1])],np.r_[0,assignments[:-1]/np.maximum(1,total[:-1])]])
                label=f'{bin_hours}h_exclude{int(exclude)}_shift{shift}'
                local=[]
                for cutoff in range(48,144,12):
                    train=(starts>=bin_hours)&(starts<cutoff);test=(starts>=cutoff)&(starts<cutoff+12)
                    for model,features in [('volume_baseline',baseline),('plus_composition',augmented),('persistence',None),('training_mean',None)]:
                        if model=='persistence':p=prev[test]
                        elif model=='training_mean':p=np.full(test.sum(),y[train].mean())
                        else:
                            p,fit=glm_predict(features[train],y[train],features[test],'poisson')
                            fitlog.append({'setting':label,'model':model,'cutoff':cutoff,**fit})
                        for j,value in zip(np.where(test)[0],p):
                            row={'setting':label,'bin_hours':bin_hours,'exclude_automated_files':exclude,'onset_shift_hours':shift,
                                 'model':model,'fold_start_hour':cutoff,'target_start_hour':int(starts[j]),'actual':int(y[j]),'prediction':float(value)}
                            local.append(row);predictions.append(row)
                for model in ['volume_baseline','plus_composition','persistence','training_mean']:
                    pp=[r for r in local if r['model']==model]
                    yy=np.array([r['actual'] for r in pp]);p=np.array([r['prediction'] for r in pp])
                    summary.append({'setting':label,'bin_hours':bin_hours,'exclude_automated_files':exclude,'onset_shift_hours':shift,
                                    'model':model,'initial_training_bins':48//bin_hours-1,
                                    'very_small_initial_training_sample':48//bin_hours-1<20,
                                    'test_bins':len(pp),'test_onsets':int(yy.sum()),**count_scores(yy,p)})
    save_csv('workstream_forecast_scores.csv',summary);save_csv('workstream_predictions.csv',predictions);save_csv('workstream_fit_diagnostics.csv',fitlog)
    folds=[]
    for b in [1,2,6]:
        for cutoff in range(48,144,12):
            for model in ['volume_baseline','plus_composition','persistence','training_mean']:
                pp=[r for r in predictions if r['bin_hours']==b and not r['exclude_automated_files'] and r['onset_shift_hours']==0 and r['fold_start_hour']==cutoff and r['model']==model]
                folds.append({'bin_hours':b,'cutoff':cutoff,'model':model,'test_bins':len(pp),**count_scores(np.array([r['actual'] for r in pp]),np.array([r['prediction'] for r in pp]))})
    save_csv('workstream_forecast_folds.csv',folds)
    # Descriptive temporal-order/shift diagnostics: no p-values, no stationarity claim.
    total=cube.sum(axis=(1,2));hf_results=cube[:,hf,result_idx].sum(axis=1);assignments=cube[:,:,assignment_idx].sum(axis=1)
    y=np.histogram(onsets,bins=np.arange(145))[0]
    diagnostics=[]
    for name,x in [('total_traffic',total),('hf_results',hf_results),('assignments',assignments)]:
        for lag in range(-6,7):
            xx,yy=(x[:-lag],y[lag:]) if lag>0 else ((x[-lag:],y[:lag]) if lag<0 else (x,y))
            rho=spearmanr(xx,yy).statistic
            diagnostics.append({'feature':name,'shift_hours':lag,'kind':'positive_means_traffic_precedes_onsets','spearman':float(rho)})
        for shift in [12,24,48,72,96,120]:
            diagnostics.append({'feature':name,'shift_hours':shift,'kind':'circular_block_shift_diagnostic','spearman':float(spearmanr(np.roll(x,shift),y).statistic)})
    save_csv('workstream_lag_diagnostics.csv',diagnostics)
    fig,axs=plt.subplots(2,1,figsize=(11,6),sharex=True)
    axs[0].plot(np.arange(144),total,color='#536b7b',label='All classified traffic');axs[0].plot(np.arange(144),hf_results,color='#a74d2d',label='HF-related results')
    axs[0].set(ylabel='Published count per hour',title='Communication counts and recorded HF onsets (same incident, unlinked populations)');axs[0].legend()
    axs[1].bar(np.arange(144),y,color='#a74d2d',label='Recorded onsets',alpha=.45)
    for model,color in [('volume_baseline','#536b7b'),('plus_composition','#202020')]:
        pp=[r for r in predictions if r['bin_hours']==1 and not r['exclude_automated_files'] and r['onset_shift_hours']==0 and r['model']==model]
        axs[1].plot([r['target_start_hour'] for r in pp],[r['prediction'] for r in pp],color=color,label=model.replace('_',' '))
    axs[1].set(ylabel='Onsets per hour',xlabel='Hours since July 8, 2026 00:00 UTC');axs[1].legend()
    for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
    fig.text(.08,.01,'Source: METR published chart assets. Forecasts use prior completed bins; expanding training, fixed regularization.\nExploratory ecological comparison only. Count labels/timing are reconstructed; population equivalence is unverified.',fontsize=8)
    fig.tight_layout(rect=(0,.07,1,1));fig.savefig(OUT/'workstream_forecast.png',dpi=180);plt.close(fig)
    nominal=[r for r in summary if r['onset_shift_hours']==0 and not r['exclude_automated_files']]
    wins={}
    for metric in ['mae','poisson_deviance']:
        count=0
        for b in [1,2,6]:
            for ex in [False,True]:
                for sh in [-2,-1,0,1,2]:
                    ss=[r for r in summary if r['bin_hours']==b and r['exclude_automated_files']==ex and r['onset_shift_hours']==sh]
                    count+=next(r[metric] for r in ss if r['model']=='plus_composition')<next(r[metric] for r in ss if r['model']=='volume_baseline')
        wins[metric]=int(count)
    save_json('workstream_summary.json',{'nominal_scores':nominal,'augmented_beats_volume_in_30_settings':wins,
        'classification_count_sum':int(cube.sum()),'positioned_onsets_in_traffic_window':int(y.sum()),
        'populations_linked':False,'confirmatory':False,
        'small_sample_caution':'Six-hour models start with only seven training bins; retained as underdetermined diagnostics, not strong evidence.',
        'source_selection_caution':'Retrospective importance-selected transcript reconstruction; includes suspected duplicates and failed writes, not a verified stream of delivered messages.',
        'all_glm_fits_converged':all(r['converged'] for r in fitlog)})
    print('Workstream analysis complete; composition wins across 30 correlated settings:',wins)


if __name__=='__main__':main()
