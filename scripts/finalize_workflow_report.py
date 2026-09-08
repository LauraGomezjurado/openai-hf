import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/workflow_obligations/v2';s=json.loads((D/'summary.json').read_text());assert s['main']==96
p=R/'docs/workflow_obligation_results.md';text=p.read_text().replace('Status: Qwen2.5 main panel complete; Qwen3 main panel running. Phi failed its capability gate. Final cross-checkpoint conclusions are pending the fixed panel.','Status: both eligible checkpoints completed all 48 main cases; all capability failures are retained. No private access, remote cluster or GPU was used.')
parts=['## Completed cross-checkpoint comparison','',f"The two eligible checkpoints contributed 96 main episodes and ten controls. Phi contributed five failed/stalled controls and no main cases. V2 used {s['calls']} generation calls including controls; the retained V1 gate adds separate calls. These are related deterministic cases, not independent samples for population p-values.",'']
for m,name in [('qwen','Qwen2.5-7B'),('qwen3','Qwen3-8B, non-thinking')]:
 parts += ['### '+name,'']
 for e in ['unauthorized','authorized']:
  parts += [('Unauthorized sharing:' if e=='unauthorized' else 'Authorized synthetic fixtures:'),'']
  for arm,label in [('task','Task card'),('end','End reminder'),('persistent','Persistent card')]:
   r=[x for x in s['records'] if not x['control'] and x['model']==m and x['evidence']==e and x['arm']==arm];n=len(r)
   if e=='unauthorized':
    parts += [f"- {label}: correct cooperative completion {sum(x['cooperative_completion'] for x in r)}/{n}; artifact-identifying receipt {sum(x['artifact_receipt'] for x in r)}/{n}; joint criterion {sum(x['joint_success'] for x in r)}/{n}; any overseer contact {sum(x['receipt'] for x in r)}/{n}, across {sum(x['messages'] for x in r)} messages."]
   else:
    parts += [f"- {label}: correct cooperative completion {sum(x['cooperative_completion'] for x in r)}/{n}; completion without overseer traffic {sum(x['clean_completion'] for x in r)}/{n}; any overseer contact {sum(x['receipt'] for x in r)}/{n}, across {sum(x['messages'] for x in r)} messages."]
  parts += ['']
 eff=next(x for x in s['effects'] if x['model']==m and x['evidence']=='unauthorized' and x['contrast']=='persistent minus end')
 parts += [f"Persistent minus end reminder: {100*eff['differences']['joint_success']:+.1f} percentage points on the strict joint criterion across eight matched contexts. This is a finite-panel contrast, not a population estimate.",'','Peer-note comparison, unauthorized cases (joint criterion, neutral → discouraging escalation):','']
 for arm in ['task','end','persistent']:
  cs=[next(c for c in s['cells'] if c['model']==m and c['evidence']=='unauthorized' and c['arm']==arm and c['pressure']==p) for p in [0,1]];parts += [f"- {arm}: {cs[0]['joint_success']}/4 → {cs[1]['joint_success']}/4."]
 parts+=['']
 for arm in ['task','end','persistent']:
  r=[x for x in s['records'] if x['model']==m and not x['control'] and x['evidence']=='unauthorized' and x['arm']==arm];parts += [f"{arm}: {sum(x['artifact_report_before_saved'] for x in r)}/8 delivered an artifact-identifying message before any successful task save; {sum(x['premature_finish_without_saved_work'] for x in r)}/8 finished without a saved work product.",'']
parts += [f"[Full cell counts, matched contrasts and per-case outcomes]({D/'summary.json'}) · [Figure]({D/'workflow_results.png'}) · [Examples and counterexamples]({R/'docs/workflow_obligation_examples.md'})",'']
a=text.index('## Completed first-checkpoint result');b=text.index('## Limits and scientific implications');text=text[:a]+'\n'.join(parts)+'\n'+text[b:];text=text.replace('[example gallery](workflow_obligation_examples.md)',f"[example gallery]({R/'docs/workflow_obligation_examples.md'})");p.write_text(text)
print('Final quantitative comparison written')
