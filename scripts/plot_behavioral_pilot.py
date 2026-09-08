"""Static research figure, descriptive counts rather than confidence intervals."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
base=root/'results/behavioral_pilot'
data=json.loads((base/'summary.json').read_text())
panels=[('v2/rollouts-1.5B.jsonl','1.5B · A/B'),
        ('v3/rollouts-1.5B.jsonl','1.5B · COPY/DECLINE'),
        ('v3-7b/rollouts-7B.jsonl','7B Q4 · COPY/DECLINE')]
panels=[p for p in panels if p[0] in data]
fig,ax=plt.subplots(figsize=(9,4.7))
for offset,allowed,label,color in [(-.18,False,'Copying prohibited','#a84839'),
                                  (.18,True,'Copying permitted','#32768b')]:
 vals=[data[key]['by_permission'][str(allowed)] for key,_ in panels]
 assert all(v['invalid']==0 for v in vals), 'Plot missingness explicitly before using this figure'
 positions=[i+offset for i in range(len(vals))]
 ax.bar(positions,[v['copied']/v['n']*100 for v in vals],width=.35,label=label,color=color)
 for x,v in zip(positions,vals):
  ax.text(x,v['copied']/v['n']*100+2,f"{v['copied']}/{v['n']}",ha='center',fontsize=10)
ax.set_xticks(range(len(panels)),[label for _,label in panels])
ax.set_ylabel('Model-selected copies executed (%)')
ax.set_xlabel('Checkpoint and action interface')
ax.set_ylim(0,119);ax.set_yticks([0,25,50,75,100])
ax.set_title('Copying under permission and prohibition: constructed CPU pilot',loc='left',fontsize=12)
ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.0))
ax.spines[['top','right']].set_visible(False)
fig.text(.02,.015,'Source: local frozen-prompt runs, 7 September 2026. Descriptive panel counts; no population inference.\nTwo wording templates × two menu orders × six peer/reminder combinations per permission level.',fontsize=8)
fig.tight_layout(rect=(0,.095,1,1))
fig.savefig(base/'behavioral_pilot.png',dpi=180)
fig.savefig(base/'behavioral_pilot.pdf')
