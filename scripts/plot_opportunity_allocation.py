"""Standalone scientific figure for the completed finite panel."""
import json,pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/opportunity_cost/v2'
s=json.loads((D/'summary.json').read_text());eligible=[(name,m) for name,m in s['models'].items() if m['gate']['pass']]
if not eligible:raise SystemExit('No eligible preference panel to plot')
fig,axs=plt.subplots(len(eligible),2,figsize=(10,3.1*len(eligible)+1.6),squeeze=False)
for row,(name,m) in enumerate(eligible):
 for col,p in enumerate([0,1]):
  ax=axs[row,col];cs=[c for c in m['cells'] if c['priority']==p];xs=list(range(4))
  ax.bar([x-.18 for x in xs],[c['peer'] for c in cs],width=.36,color='#356d92',label='Peer audit delivered')
  ax.bar([x+.18 for x in xs],[c['own'] for c in cs],width=.36,color='#aaaeb3',label='Own package published')
  ax.set_xticks(xs,[c['world'].capitalize() for c in cs]);ax.set_xlabel('Controlled world state');ax.set_ylabel('Successful outputs (of 8 cases)');ax.set_ylim(0,9.2);ax.set_yticks([0,2,4,6,8]);ax.set_title({'qwen3':'Qwen3-8B Q4','qwen':'Qwen2.5-7B Q4'}.get(name,name)+' — '+('explicit priority' if p else 'baseline priority'),fontsize=11)
  ax.spines[['top','right']].set_visible(False)
  for x,c in zip(xs,cs):
   ax.text(x-.18,c['peer']+.12,str(c['peer']),ha='center',fontsize=9);ax.text(x+.18,c['own']+.12,str(c['own']),ha='center',fontsize=9)

handles,labels=axs[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=2,frameon=False,fontsize=10)
fig.suptitle('Cooperation choices with verified opportunity costs',fontsize=15,y=.99)
fig.text(.05,.015,'Source: frozen V2 local CPU runs, September 8, 2026. Each cell: 4 related domains × 2 option orders.\nOne constrained allocation per case; backend executes the work. Counts are not population estimates.\nOriginal HF agents were not tested. Replays are excluded from these denominators.',fontsize=9)
fig.tight_layout(rect=[0,.12,1,.90]);fig.savefig(D/'allocation_outputs.png',dpi=180);fig.savefig(D/'allocation_outputs.pdf');plt.close(fig)
