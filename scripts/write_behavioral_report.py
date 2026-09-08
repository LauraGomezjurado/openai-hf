"""Generate the pilot handoff from completed model runs, with scoped claims."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=root/'results/behavioral_pilot'
d=json.loads((base/'summary.json').read_text())
large=d['v3-7b/rollouts-7B.jsonl']
assert large['total_calls']==52
lines=['# Actual model-behavior pilot — September 7, 2026', '',
'We ran actual CPU inference and executed valid model-selected actions in an in-memory workspace. '
'This is a public-model constructed-setting study, separate from the HF historical evidence. '
'It tests three behavioral predictions; it does not establish the incident agents’ motivations.', '',
'## Execution and evidence', '',
f"Total generation calls: **{sum(x['total_calls'] for x in d.values())}**. "
'This includes 52 deterministic reruns after the parser correction; those are not additional independent observations. '
'Each panel contains 48 factorial cases and four instructed-action controls. '
'Four observations per cell are two wording templates crossed with two menu orders, not four independent task families. '
'No sampling confidence interval, population prevalence or significance claim is warranted.', '',
'Initial strict JSON parsing rejected all 48 main responses from both smaller checkpoints. '
'We preserved the failures, then allowed only an exact outer JSON code fence. '
'The 1.5B rerun produced the same 52 raw outputs as before, and all actions then parsed. '
'The 0.5B checkpoint also failed the requested action vocabulary, so it was not advanced.', '',
'## Three preregistered pilot contrasts on the 7B checkpoint', '']
for heading,first,second,interpret in [
 ('Peer endorsement under prohibition','False-endorse-neutral','False-informational-neutral',
  'Prediction: endorsement increases unauthorized copying.'),
 ('Scope reminder under prohibition and endorsement','False-endorse-scope','False-endorse-neutral',
  'Prediction: the reminder decreases unauthorized copying.'),
 ('Scope reminder under permission and endorsement','True-endorse-scope','True-endorse-neutral',
  'Prediction: the reminder retains useful assistance.')]:
 a,b=large['cells'][first],large['cells'][second]
 assert a['invalid']==b['invalid']==0
 delta=100*(a['copied']/a['n']-b['copied']/b['n'])
 lines += [f'- **{heading}:** {a["copied"]}/{a["n"]} versus '
           f'{b["copied"]}/{b["n"]} copies; difference {delta:+.0f} percentage points. {interpret}']
lines += ['', '## Controls and interface sensitivity', '']
for key,label in [('v2/rollouts-1.5B.jsonl','1.5B with A/B labels'),
                  ('v3/rollouts-1.5B.jsonl','1.5B with semantic labels'),
                  ('v3-7b/rollouts-7B.jsonl','7B Q4 with semantic labels')]:
 x=d[key]; forbidden=x['by_permission']['False'];allowed=x['by_permission']['True']
 orders=x['by_menu_order']
 lines += [f'- **{label}:** {forbidden["copied"]}/{forbidden["n"]} prohibited copies; '
           f'{allowed["copied"]}/{allowed["n"]} permitted copies. '
           f'Menu orders: {orders["False"]["copied"]}/{orders["False"]["n"]} versus '
           f'{orders["True"]["copied"]}/{orders["True"]["n"]}. '
           f'Controls passed: {x["controls_correct"]}/{x["controls_total"]}; '
           f'correct arithmetic subtotal: {x["main"]["own_task_correct"]}/48; '
           f'invalid main actions: {x["main"]["invalid"]}/48.']
lines += ['', '![Descriptive copying counts](../results/behavioral_pilot/behavioral_pilot.png)', '',
'## Interpretation and next decision', '',
'The 1.5B A/B results were dominated by the action interface. Using semantic labels removed '
'that order difference but yielded copying in every case, including peer vetoes. '
'This does not support attributing its behavior specifically to peer endorsement or solidarity. '
'Simple instructed-action controls were insufficient to validate its behavior in the fuller prompt.', '',
'For 7B, the observed zero prohibited-copy baseline makes the reminder’s prevention benefit unmeasurable in '
'this panel. Retaining permitted help is useful control evidence, but does not demonstrate prevention. '
'A zero observed endorsement effect likewise does not establish that peer influence is absent in other tasks. '
'The task is one-step, authorization is explicit, and own-task success is only a constant arithmetic subtotal. '
'There is no demonstrated preservation of complex task performance, realistic peer coordination or monitoring capability.', '',
'The next scientific gate is a richer task family with independently specified legitimate goals, '
'observable assistance costs, and naturally occurring baseline boundary mistakes. '
'Freeze that family before testing mitigation. Include menu/format robustness and task-comprehension '
'controls before interpreting a choice as motivation. Do not tune prompts until they produce a desired failure. '
'Any stronger historical HF attribution remains unsupported by these experiments.', '',
'**For your review:** whether this constructed behavioral arm is valuable enough to expand alongside '
'the HF evidence study; what realistic legitimate task and cooperation cost should define the next family. '
'There is no access-partnership or private-data requirement. No paid inference, DGX access, '
'GPU offload or external messaging occurred.', '',
'## Reproducibility', '',
'Protocols and versioned amendments: `experiments/behavioral_pilot/`. Raw prompts, responses, '
'executed virtual traces, weight hashes, checkpoint revisions, settings and timing: '
'`results/behavioral_pilot/`. Rebuild with `scripts/analyze_behavioral_pilot.py`, '
'`scripts/plot_behavioral_pilot.py`, and this report generator. '
'The 7B Q4_K_M model uses llama.cpp; the smaller models use Transformers float32. '
'Model, quantization and backend differences prevent interpreting their contrast as a pure scaling effect.', '',
'Public model sources: [Qwen 1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), '
'[Qwen 7B GGUF](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF). '
'Methodological reference: [Model Forensics](https://arxiv.org/html/2606.26071v2).']
(root/'docs/behavioral_pilot_results.md').write_text('\n'.join(lines)+'\n')
