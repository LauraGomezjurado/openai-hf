"""Retrospective evidence anchors, with explicit selectors and checked provenance."""
import json, hashlib, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/example_ledger'; OUT.mkdir(exist_ok=True)
entries=[]
def add(id,claim,path,kind,limit,pointer=None,line=None,selection='Named contrast from the existing analysis; retrospective selection.',observation=None):
 p=ROOT/path; raw=p.read_bytes(); value=None
 if line is not None:
  text=raw.decode().splitlines()[line-1]
  value=json.loads(text) if p.suffix=='.jsonl' else text
 elif pointer is not None:
  value=json.loads(raw)
  for k in pointer.strip('/').split('/') if pointer else []:
   value=value[int(k)] if isinstance(value,list) else value[k]
 else: value={'source_file':path}
 rec=dict(id=id,claim=claim,evidence_kind=kind,source=str(p),sha256=hashlib.sha256(raw).hexdigest(),json_pointer=pointer,line=line,selection_rule=selection,observation=observation,limits=limit)
 # Complete existing source object is available separately, never relabeled as raw CoT.
 (OUT/f'{id}.json').write_text(json.dumps({'metadata':rec,'source_selection':value},indent=2,ensure_ascii=False)+'\n')
 entries.append(rec)
add('hf-notification','METR reports rare consideration of human notification in its inspected transcripts.','results/literature/hf_escalation_anchor.json','Investigator finding with published quotations and paraphrases','Not our independent transcript audit; no valid prevalence denominator or identified motive. Brace-delimited reasoning is paraphrased, not verbatim.',pointer='',observation='The section describes task-role explanations, difficulty finding a reporting route, and escalation to the agent board. These are competing leads for experiments, not established causal explanations.')
add('hf-quotation-legend','The report explicitly distinguishes verbatim and paraphrased reasoning.','data/raw/metr/report.html','Source typography legend','Preserve the original classification when presenting an excerpt.',line=803,observation='The source CSS comment identifies braces as paraphrased chain of thought.')
for i,id,claim,obs in [
 (0,'hf-self-risk','Some reported cooperation risked the acting agent’s own task.','Investigator narrative includes agents crashing or exiting while producing information for peers; this does not exclude expected personal benefit.'),
 (1,'hf-withdrawal','Cooperation was not unconditional in the reported tripwire episode.','METR describes 49903 deciding the remaining marginal benefit did not outweigh risk to its own completion.'),
 (2,'hf-benefit-alternative','Expected benefit remains an alternative to peer preference.','METR describes hopes of retrieving useful prior-agent information even where the path to task success was unclear.'),
 (3,'hf-peer-veto','The board could discourage a boundary-crossing action.','METR describes a request to email a dataset owner, a peer veto, and stated acceptance of that veto.')]:
 add(id,claim,'results/cooperation/hf_episode_context.json','Published investigator narrative plus selected agent text','Published selected evidence, not complete independently linked tool logs. Statements do not independently verify execution or non-execution; braces are paraphrases.',pointer=f'/{i}',observation=obs)
add('hf-timing-uncertainty','Timing conclusions depend on timestamp error assumptions.','results/cpu/timing_sensitivity.csv','Derived statistical sensitivity analysis','Bounds are measurement-sensitivity bounds, not confidence intervals; selected timeline rows are not an unbiased agent population.',observation='The earlier analysis separates July 9/11 one-hour bounds at ±5 minutes but finds overlap at ±30 minutes. Open the complete grid rather than selecting only the favorable threshold.')
add('hf-ordering-counterexample','Recorded timeline ordering is sometimes inconsistent.','results/cpu/timeline_ordering_issues.csv','Derived record-level data-quality flag','A flagged row is evidence of a measurement problem, not evidence that the agent acted backwards in time.',line=2,selection='First data row in the saved issue file.')
add('hf-forecast-negative','Adding board tenure did not outperform the simple baseline on the saved all-interval evaluation.','results/cpu/read_anchored_scores.csv','Derived aggregate scores','This is a model-comparison result, not an individual causal example. Correlated intervals and retrospective selection limit interpretation.',observation='10,521 intervals, 571 positives: training-mean Brier 0.05263; calendar/run-age 0.09710; plus-board-tenure 0.09745. Lower is better.')
rows=[json.loads(s) for s in (ROOT/'results/cooperation/discriminating_context.jsonl').read_text().splitlines()]
for i,r in enumerate(rows,1):
 if 'Apr23CVDHorizonBeacon2025' in json.dumps(r):
  add('wiki-cancel-and-continue','Stopping one method need not mean abandoning cooperation.','results/cooperation/discriminating_context.jsonl','Separate historical wiki archive: posted statements','Separate incident/comparison corpus. Claimed launch and manual assistance are not verified execution. Archive times need not equal action times.',line=i,selection='First saved contrast containing Apr23CVDHorizonBeacon2025.',observation='The saved history records cancellation of a timer followed by discussion of manual help and an alternative heartbeat.');break
add('wiki-keyword-miss','Keyword retrieval missed a priority-conflict candidate.','results/cooperation/ambitious_quantitative_audit.json','Derived search audit with archive candidates','Search hits are not prevalence. The DataUSALanguageJul17R5 priority contrast lacks a verified recipient outcome.',pointer='',observation='An authority search returned zero lexical matches; contextual review nevertheless identified a priority-conflict candidate. Negative keyword counts do not establish absence.')
f='results/behavioral_pilot/v3-7b/rollouts-7B.jsonl'; rows=[json.loads(s) for s in (ROOT/f).read_text().splitlines()]
for id,pred,claim in [
 ('pilot-permitted-copy',lambda r:r['case'].get('allowed') and r['outcome'].get('copied'),'The 7B pilot could help when copying was permitted.'),
 ('pilot-prohibited-decline',lambda r:r['case'].get('allowed') is False and not r['outcome'].get('copied'),'The 7B pilot could decline prohibited copying while submitting its subtotal.'),
 ('pilot-peer-veto',lambda r:r['case'].get('allowed') and r['case'].get('peer')=='veto' and not r['outcome'].get('copied'),'Peer requests could affect permitted assistance.')]:
 candidates=[(i,r) for i,r in enumerate(rows,1) if r['case'].get('kind')=='main' and pred(r)];i,r=min(candidates,key=lambda x:x[1]['case']['id'])
 add(id,claim,f,'Generated decision and harness action','Synthetic explicit-action pilot, not original HF behavior. No private reasoning was recorded.',line=i,selection='Lexicographically first case ID satisfying the named outcome class.',observation=r['raw_output'])
f='results/escalation/continuations/rollouts.jsonl'; rows=[json.loads(s) for s in (ROOT/f).read_text().splitlines()]
for arm in ['task','duty']:
 candidates=[(i,r) for i,r in enumerate(rows,1) if r['case']['id']==f'f0-unauthorized-d1-r0-{arm}']
 for i,r in candidates:
  add('continuation-'+arm,'A matched continuation tests duty salience after task submission.',f,'Generated tool trajectory','One previously selected matched context; inspect the full aggregate before generalizing. Outbound messages are not private reasoning.',line=i,observation='Same source context; '+arm+' continuation arm. Complete action record saved in the linked JSON.')
add('whistlebench-fixed-record','The benchmark audit preserves original records and implementation context.','results/escalation/fixed_sample.json','External benchmark record, not HF incident','Fixed sample is not an estimate of benchmark-wide or HF behavior. Tool receipt does not establish human response. Preserve original file/member identifiers.',pointer='/0',selection='First record in the previously fixed sample; not chosen for dramatic behavior.')
add('new-workflow-examples','New study includes successes, omissions, treatment losses and capability failures.','results/workflow_obligations/v2/example_index.json','Generated experiment example index','Four related task domains, two eligible Qwen checkpoints, Q4 deterministic local inference. No original-model causal claim.',pointer='',observation='The dedicated gallery preserves full trajectories and deterministic within-class selection, including empty classes.')
add('completion-work-repair','A work-status reminder restores two missing submissions in the fixed Qwen3 release contexts.','results/workflow_completion/examples/qwen3-work_repair.json','Generated matched continuation trajectories','Two related variants in one domain. Does not identify memory failure or original-HF motivation.',pointer='',observation='The selected replay finishes without saved work; work-only and both-card branches submit rel-A correctly and finish. The duty-only branch still finishes without repairing.')
add('completion-residual-omission','A combined completion card still leaves incident-reporting omissions.','results/workflow_completion/examples/qwen3-residual_omission.json','Generated counterexample with four matched branches','A selected example illustrates a residual failure, not its prevalence or cause.',pointer='')
add('completion-wording-diagnostic','A one-word substitution removes invalid preservation calls in the fixed diagnostic.','results/workflow_completion/wording_control/example-error_removed.json','Post-result controlled public-model experiment','16 related Qwen2.5 saved-work contexts; does not validate the combined card. Original-wording controls retain one argument-level variation.',pointer='',observation='Preserve to Retain changes invalid preserve calls from 16 to 0, retaining 16/16 correct completions. Both original results and raw diagnostic traces are saved.')
index={'scope':'Retrospective anchors for major empirical analyses plus the new study. Synthesis/proposals and unexecuted experiments are not empirical results. Not an exhaustive transcript annotation.','entries':entries}
(OUT/'index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
lines=['# Research example ledger','','Evidence anchors and counterexamples for the major completed analyses. Selection is retrospective unless explicitly stated otherwise. Examples illustrate claims; denominators and full analyses determine their scope. Original HF evidence, the separate wiki archive, external benchmarks and our generated experiments remain distinct.','','**Source correction:** METR’s brace-delimited passages are investigator paraphrases of reasoning, not verbatim chain of thought. Published quotations are still selected excerpts, not full original transcripts. Non-reporting alone does not establish collusion.','','[New workflow gallery]('+str(ROOT/'docs/workflow_obligation_examples.md')+') · [Recording policy]('+str(ROOT/'docs/example_recording_policy.md')+') · [Machine-readable ledger]('+str(OUT/'index.json')+')','']
for r in entries:
 target=r['source']+(f":{r['line']}" if r['line'] else '')
 lines += ['## '+r['id'],'',r['claim'],'','**Evidence:** '+r['evidence_kind']+'.', '',r['observation'] or 'Open the saved source selection below.','',f"[Source]({target}) · [Saved selection and SHA-256]({OUT/(r['id']+'.json')})"+(f" · JSON pointer `{r['json_pointer']}`" if r['json_pointer'] else ''),'','Selection: '+r['selection_rule'],'','Limit: '+r['limits'],'']
(ROOT/'docs/research_example_ledger.md').write_text('\n'.join(lines))
print(f'Wrote and validated {len(entries)} source anchors.')
