import json,pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/escalation/pilot_v2';s=json.loads((D/'summary.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(10,4.6),sharey=True)
for ax,e in zip(axs,['unauthorized','authorized']):
 cells=[c for c in s['cells'] if c['evidence']==e]
 for i,c in enumerate(cells):
  n=c['n'];ax.bar(i,c['receipt']/n if n else 0,color='#347da0' if c['route'] else '#afcdd9',width=.72);ax.text(i,(c['receipt']/n if n else 0)+.025,f"{c['receipt']}/{n}",ha='center',fontsize=11)
 ax.set_xticks(range(4),['No duty\nLookup','No duty\nShown','Duty\nLookup','Duty\nShown']);ax.set_title(e.capitalize()+' sharing');ax.set_ylim(0,1.16);ax.spines[['top','right']].set_visible(False);ax.set_yticks([0,.25,.5,.75,1],['0%','25%','50%','75%','100%'])
axs[0].set_ylabel('Episodes with accepted overseer message')
fig.suptitle('Reporting duty × route visibility: fixed CPU pilot',fontsize=14)
fig.text(.05,.035,'Qwen2.5-7B Q4 • 4 surface variants per cell • deterministic decoding\nLocal inbox receipt; semantic validity and human remediation are not established. No HF causal attribution.',fontsize=9)
fig.tight_layout(rect=[0,.13,1,.92]);fig.savefig(D/'reporting.png',dpi=180);fig.savefig(D/'reporting.pdf');plt.close(fig)
