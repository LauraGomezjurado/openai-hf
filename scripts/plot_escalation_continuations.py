import json,pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/escalation/continuations';s=json.loads((D/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4.7),sharey=True)
for ax,e in zip(axes,['unauthorized','authorized']):
 cells=[next(c for c in s['cells'] if c['evidence']==e and c['arm']==arm) for arm in ['replay','task','duty']]
 for i,c in enumerate(cells):
  v=c['receipt']/c['n'] if c['n'] else 0;ax.bar(i,v,color=['#a9b6bd','#79a8be','#176887'][i],width=.65);ax.text(i,v+.03,f"{c['receipt']}/{c['n']}",ha='center',fontsize=12)
 ax.set_xticks(range(3),['Exact\nreplay','Numerical-task\nreminder','Existing-duty\nreminder']);ax.set_title(e.capitalize()+' sharing');ax.set_ylim(0,1.16);ax.set_yticks([0,.25,.5,.75,1],['0%','25%','50%','75%','100%']);ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Final accepted overseer-message rate')
fig.suptitle('Controlled continuations from actual pre-finish contexts',fontsize=14)
fig.text(.05,.03,'Same 16 source contexts in each branch; not independent samples. Qwen2.5-7B Q4, deterministic CPU.\nLocal inbox receipts; no human response. Four related surface variants; no original-HF causal inference.',fontsize=9)
fig.tight_layout(rect=[0,.14,1,.92]);fig.savefig(D/'continuations.png',dpi=180);fig.savefig(D/'continuations.pdf');plt.close(fig)
