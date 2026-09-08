import pathlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/peer_claims_v2';s=json.loads((D/'summary.json').read_text());eligible=[(name,m) for name,m in s['models'].items() if m['gate']['eligible']]
if not eligible:raise SystemExit('No eligible panel')
fig,axs=plt.subplots(len(eligible),3,figsize=(13,3.3*len(eligible)+1.6),squeeze=False);policies=['optional','required','automatic'];names={'qwen3':'Qwen3-8B Q4','qwen':'Qwen2.5-7B Q4'}
for row,(name,m) in enumerate(eligible):
 for col in range(3):
  ax=axs[row,col]
  if col<2:
   metric='false_redirection' if col==0 else 'peer';available=col==0
   for shift,claim,color in [(-.18,'none','#a9adb2'),(.18,'hopeless','#3d7397')]:
    vals=[next(c[metric] for c in m['cells'] if (c['available'],c['claim'],c['policy'])==(available,claim,policy)) for policy in policies];xs=[i+shift for i in range(3)];ax.bar(xs,vals,.36,color=color,label='No assessment' if claim=='none' else 'Hopelessness claim')
    for x,v in zip(xs,vals):ax.text(x,v+.08,str(v),ha='center',fontsize=9)
  else:
   vals=[next(c['both'] for c in m['secondary'] if c['policy']==policy) for policy in policies];ax.bar(range(3),vals,.5,color='#3d7397')
   for x,v in enumerate(vals):ax.text(x,v+.08,str(v),ha='center',fontsize=9)
  ax.set_title(names[name]+'\n'+['False redirection; own task achievable','Useful peer output; own task blocked','Both outputs; affordable, false claim'][col],fontsize=10);ax.set_xticks(range(3),['Optional\ncheck','Required\ncheck','Automatic\ntruth']);ax.set_xlabel('Information policy');ax.set_ylabel('Cases (of 4)');ax.set_ylim(0,4.7);ax.set_yticks(range(5));ax.spines[['top','right']].set_visible(False)
handles,labels=axs[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=2,frameon=False);fig.suptitle('Peer assessments, verification and executed work',fontsize=15,y=.99)
fig.text(.04,.015,'Source: frozen peer-claims V2 CPU experiment, September 8, 2026. Each cell: 2 task graphs × 2 option orders.\nChecking is free; costs are certain. Backend executes selected allocations. Controls and replays excluded.\nFixed-panel counts, not population estimates; original HF agents were not tested.',fontsize=9)
fig.tight_layout(rect=[0,.13,1,.90]);fig.savefig(D/'peer_claims.png',dpi=180);fig.savefig(D/'peer_claims.pdf');plt.close(fig)
