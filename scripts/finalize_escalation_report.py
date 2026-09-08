import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1];D=R/'results/escalation/continuations';s=json.loads((D/'summary.json').read_text());assert s['n']==48
p=R/'docs/escalation_experiment_results.md';text=p.read_text().replace('**Status: fixed factorial pilot and arithmetic controls complete; controlled continuations running.**','**Status: fixed factorial pilot, arithmetic controls and all 48 controlled continuations complete.**')
def cell(e,a):return next(x for x in s['cells'] if x['evidence']==e and x['arm']==a)
u=[cell('unauthorized',a) for a in ['replay','task','duty']];b=[cell('authorized',a) for a in ['replay','task','duty']];eff=next(x for x in s['effects'] if x['evidence']=='unauthorized' and x['contrast']=='duty minus task')
section=f'''## Completed continuation results

All 48 frozen branches completed generation, using {s['calls']} model calls with {s['errors']} tool errors. Exact final states reproduced in {s['exact_state_replays']}/{s['replay_n']} baseline replays; the first continuation action matched the source final action in {s['first_action_replays']}/{s['replay_n']}.

For the same eight unauthorized source contexts, final accepted overseer messages occurred in:

- Exact replay: {u[0]['receipt']}/8.
- Numerical-task reminder: {u[1]['receipt']}/8.
- Existing-duty reminder: {u[2]['receipt']}/8.

The primary paired duty-minus-task contrast is {eff['difference']['receipt']*100:+.1f} percentage points: {eff['receipt_gains']} contexts gained a receipt and {eff['receipt_losses']} lost one. These are matched continuations of eight selected duty-present contexts, not independent new tasks. Original reporting outcomes did not determine eligibility.

For the eight benign source contexts, accepted messages were {b[0]['receipt']}/8, {b[1]['receipt']}/8 and {b[2]['receipt']}/8 respectively. This is observed review burden, not a calibrated false-accusation rate. Correct saved numerical outputs were {u[0]['task_success']}/8, {u[1]['task_success']}/8, {u[2]['task_success']}/8 for unauthorized contexts and {b[0]['task_success']}/8, {b[1]['task_success']}/8, {b[2]['task_success']}/8 for benign contexts. Every branch began with its original saved total; unchanged correctness is preservation of an existing output, not proof of completing new work under intervention.

Finished sessions were {u[0]['finished']}/8, {u[1]['finished']}/8 and {u[2]['finished']}/8 in unauthorized contexts; {b[0]['finished']}/8, {b[1]['finished']}/8 and {b[2]['finished']}/8 in benign contexts. No additional human response or real remediation was simulated.

The exploratory leave-one-surface-variant-out sensitivity is saved in `../results/escalation/continuations/summary.json`; this is not a confidence interval. Primary cells, paired differences, every branch and raw messages are retained. Figure: `../results/escalation/continuations/continuations.png` and PDF.

'''
text=text.replace('## Next scientific gates',section+'## Next scientific gates');p.write_text(text)
files=[p,R/'docs/whistlebench_implementation_audit.md',R/'scripts/escalation_pilot.py',R/'scripts/escalation_continuations.py',R/'scripts/analyze_escalation_pilot.py',R/'scripts/analyze_escalation_continuations.py']
for root in [R/'experiments/escalation_pilot',R/'results/escalation']:
 files += [x for x in root.rglob('*') if x.is_file() and x.suffix in ['.json','.jsonl','.md','.py'] and x.name!='output_manifest.json' and '__pycache__' not in str(x)]
(R/'results/escalation/output_manifest.json').write_text(json.dumps({str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(set(files))},indent=2))
print('Completed report and output checksums written')
