import pathlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/workflow_completion';s=json.loads((D/'summary.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(11,8))
colors=['#aaaaaa','#8ab7c5','#306b83','#153e53'];arms=['replay','work','duty','both'];labels=['Replay','Work status','Duty','Both']
for i,model in enumerate(['qwen','qwen3']):
 for j,evidence in enumerate(['unauthorized','authorized']):
  ax=axes[i,j];key='joint' if evidence=='unauthorized' else 'any_overseer';counts=s['models'][model]['counts'][evidence]
  vals=[counts[a][key] for a in arms];ax.bar(range(4),vals,color=colors)
  for k,v in enumerate(vals):ax.text(k,v+.15,f'{v}/8',ha='center')
  ax.set_xticks(range(4),labels);ax.set_ylim(0,9);ax.set_yticks([0,2,4,6,8]);ax.set_ylabel('Source contexts (count)');ax.set_xlabel('Continuation intervention');ax.spines[['top','right']].set_visible(False)
  ax.set_title(('Qwen2.5-7B' if model=='qwen' else 'Qwen3-8B, non-thinking')+'\n'+('Unauthorized: correct work + artifact receipt' if evidence=='unauthorized' else 'Authorized: any overseer traffic'))
fig.suptitle('Completion checkpoints at actual pre-finish contexts',fontsize=15)
fig.text(.04,.025,'Source: frozen local CPU continuation study, September 7–8, 2026. Eight matched contexts per condition.\nCounts include receipts already present before branching. Benign contact is not automatically a false accusation.\nFour related task domains; deterministic Q4 models. No population uncertainty or HF causal inference.',fontsize=9)
fig.tight_layout(rect=[0,.12,1,.95]);fig.savefig(D/'completion_results.png',dpi=180);fig.savefig(D/'completion_results.pdf');plt.close(fig)
