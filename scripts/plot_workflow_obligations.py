import pathlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/workflow_obligations/v2';s=json.loads((D/'summary.json').read_text());models=[m for m in ['qwen','qwen3'] if any(x['model']==m and not x['control'] for x in s['records'])]
fig,axes=plt.subplots(len(models),2,figsize=(10,3.9*len(models)),squeeze=False)
for i,m in enumerate(models):
 for j,e in enumerate(['unauthorized','authorized']):
  ax=axes[i,j]
  for k,arm in enumerate(['task','end','persistent']):
   for p,offset,color in [(0,-.18,'#aacbd9'),(1,.18,'#1a6c8a')]:
    c=next(x for x in s['cells'] if x['model']==m and x['evidence']==e and x['pressure']==p and x['arm']==arm);n=c['n'];metric='joint_success' if e=='unauthorized' else 'receipt';v=c[metric]/n if n else 0;ax.bar(k+offset,v,width=.33,color=color,label=('Neutral peer' if p==0 else 'Discourages escalation') if k==0 else None);ax.text(k+offset,v+.025,f'{c[metric]}/{n}',ha='center',fontsize=9)
  ax.set_xticks(range(3),['Task card','End reminder','Persistent card']);ax.set_ylim(0,1.2);ax.set_yticks([0,.5,1],['0%','50%','100%']);ax.spines[['top','right']].set_visible(False);ax.set_title(('Qwen2.5-7B' if m=='qwen' else 'Qwen3-8B, non-thinking')+'\n'+('Unauthorized: correct work + artifact receipt' if e=='unauthorized' else 'Benign: any overseer traffic'))
  if i==0 and j==0:ax.legend(loc='upper left',fontsize=8,frameon=False)
fig.suptitle('Safety obligations in validated scripted-peer workflows',fontsize=14)
fig.text(.05,.025,'Four task domains per cell, deterministic Q4 inference. Related join/filter tasks; no population confidence claims.\nBenign traffic can include task-help requests or all-clear updates. Receipts do not establish human remediation.',fontsize=9)
fig.tight_layout(rect=[0,.09,1,.95]);fig.savefig(D/'workflow_results.png',dpi=180);fig.savefig(D/'workflow_results.pdf');plt.close(fig)
