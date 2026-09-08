# Studying the OpenAI–Hugging Face incident using public historical data

**Methodological upgrade — September 8, 2026 (later):** the replay non-determinism is diagnosed (`cache_prompt=true`) and fixed with a backend gate; reasoning capture, a preregistered cross-family V3 replication with staged explanation-before-intervention, and a formal ACH evidence matrix are in place. Read [the rigor memo](docs/forensic_rigor_upgrade.md) and [the ACH matrix](docs/ach_evidence_matrix.md). No new checkpoint inference has run; V3 is frozen for the machine that holds the models.

**Current status — September 8, 2026:** the public-only peer-claim experiment and diagnostics are complete. Start with the [new interpretation](docs/peer_claims_interpretation.md), [full results](docs/peer_claims_results.md), [working plan](docs/working_plan.md) and [question map](docs/research_question_map.md). A peer assessment suppressed checking in one qualified public checkpoint; this is an incident-motivated behavioral analogue, not an explanation of original-HF motives. All local CPU runs are stopped. Earlier studies and failed controls remain preserved.

The sections below preserve the earlier project history. Superseded proposals are not instructions to start remote compute or seek private access.


Research starter, verified September 6, 2026. Hugging Face is the primary case. The public wiki archive is a separately labeled comparison incident, as requested.

**Update: the first CPU research pass is complete.** Start with [the current working plan](docs/working_plan.md) and [the results memo](docs/cpu_results.md). Recruitment remains visible after basic subset checks, but exact timing is sensitive to timestamp assumptions. Both onset and communication forecast models fail simple baselines. The next bottleneck is source validation and independent episode labels, not GPUs.

Rebuild all expanded analyses offline with `python3 scripts/run_cpu.py` (NumPy, SciPy, and matplotlib required). Outputs, figures, validation records, and hashes are in `results/cpu/`. The original starter files below remain available.

**The most useful finding is that METR's interactive figures publish machine-readable incident-derived data.** We recovered 1,206 plotted agent rows and 1,772 sparse hourly workstream rows. This enables observational analysis without reproducing an attack or training a substitute agent. These are investigator reconstructions/classifications, not raw model transcripts.

Read [the research protocol](docs/research_protocol.md) for questions, experiments, decision gates, and a two-week schedule. Read [the evidence inventory](docs/evidence_inventory.md) for source links, provenance, and access limits. [The access request draft](docs/access_request.md) asks for narrowly scoped additions to the actual incident data; it has not been sent.

## Run the completed audit

```sh
python3 scripts/audit_public_data.py
python3 scripts/plot_pilot.py
```

The audit uses Python's standard library. The optional scientific plot uses matplotlib. Both run offline; no source JavaScript, archived commands, or agent payloads are executed.

Outputs:

- `data/processed/metr_agents.csv`: 1,206 records, reconstructed UTC timestamps, model-family codes, stop flags, and chronology diagnostics. Row IDs are snapshot-local indices, not stable agent identities.
- `data/processed/metr_workstream_counts.csv`: 12,404 long-format cells from 1,772 sparse rows × seven communicative purposes; not 12,404 independent observations.
- `data/processed/metr_cohort_followup.csv`: descriptive 1/6/24-hour onset summaries by first board-read day, including follow-up availability bounds.
- `results/data_audit.json`: source integrity, sizes, nulls, and consistency checks.
- `results/recruitment-pilot.png` and `.pdf`: descriptive scientific figure. Its ranges address early follow-up endings only, not classification error or other missingness.

`data/source_manifest.json` records public URLs, download date, byte sizes, and SHA-256 hashes. `data/raw/` holds local research snapshots. The wiki revisions and events additionally match the expanded-file checksums on the authors' download page. Do not mistake local copies for a new release under our ownership: the wiki download page still displays a draft/no-sharing banner despite the public findings page inviting analysis. Resolve redistribution terms before republishing that corpus.

## What the first run established

The METR timeline contains 1,068 HPIM rows and 138 Sol rows. It places 684 Hugging Face onset times while separately declaring 688 verified participants. Fifteen positioned onsets precede the corresponding first recorded board read, 60 rows lack a write time, and only 47 rows mark an observed stop. These are audit questions, not proof that the investigators made errors.

As a descriptive reproduction, 132 of 517 eligible July 11 board-reader rows have a recorded onset within one hour, versus 31 of 486 July 9 rows. Nineteen and nine additional rows, respectively, end follow-up before that hour without an onset. Onsets at or before first recorded read are excluded from these risk sets and reported separately. This reproduces the report's broad recruitment pattern; it does **not** identify an effect of reading the board, and missing classifications remain unresolved.

The HF replay contains only 21 curated entries. Its daily counts sum to 17,613; listed phase counts sum to 16,521. No exhaustive phase partition is assumed. Intermediate animation counts are interpolated, so the replay must not be sampled as a high-resolution event stream.

The separate wiki snapshot has 14,591 revisions over 4,579 pages. Its 19,913 event rows combine overlapping save/delete/revert/probe populations and must not be described as 19,913 independent agent actions. Full revisions retain preceding page text: message extraction needs revision deltas.

## Compute

The user has access to eight V100 GPUs with 16 GB each. No cluster connection, inspection, reservation, or job launch has occurred. The primary pilot is CPU-scale. GPU use is conditional on a later monitor experiment; benchmark the chosen implementation before reserving GPUs. Aggregate GPU memory is not a single 128 GB allocation.

## Historical direction (September 6)

The project centers on **cooperation under conflicting objectives**. See [protocol v2](docs/research_protocol.md), [working plan](docs/working_plan.md), and [first cooperation feasibility pass](docs/cooperation_feasibility.md). Prior numerical protocols are retained as phase-1 files. Run `python3 scripts/prepare_cooperation.py` for the frozen retrieval pilot; its counts are candidate matches, not confirmed behavior labels.

## Historical phase-3 proposal — superseded

Phases 1 and 2 attacked the first clause of the North Star and were stopped by the second. Both phase-1 predictive gates lost to trivial baselines, and no phase-2 case met the evidence requirements for a clean motivational distinction. That ceiling is structural, not a matter of diligence: the model-forensics protocol needs raw reasoning and environment intervention, and the public record supplies neither. Every available episode is capped at E2.

**Correction to this earlier proposal:** assigning a goal in a prompt does not make a model’s latent motivation known by construction. This proposal is not the current experimental direction.

The earlier phase-3 proposal stops asking the first clause about the historical agents and measures the second one. Build a small corpus in which motivation is known by construction, censor it down the E0–E5 ladder, and measure how attribution accuracy decays against surface baselines. The deliverable is an identifiability curve with the real records located on it: the METR report is rung L1, the recovered figure data is rung L0.

**The incident is a source of design constraints in this phase, not a source of evidence.** No causal claim about HPIM, Sol, or the historical agents follows from constructed-corpus results. See [protocol v3](docs/research_protocol_phase3.md) for the design, gates, power reasoning and ethics constraints.

This is the first phase that needs GPUs, so it opens with a hardware gate:

```sh
python3 scripts/hardware_gate.py --model Qwen/Qwen3-8B --tp 2 --fp32-ref
```

It retires two risks before any design commitment — vLLM's progressively deprecated sm_70 support, and fp16 overflow in bf16-native reasoning checkpoints, which would present as "the model reasons worse under condition X" and be indistinguishable from a finding. Results are written to `results/phase3/hardware_gate.json`; the script runs anywhere and records that the gate is not runnable rather than failing when no CUDA device is visible.

## Partnership experiment package — optional, not an access dependency

See [proposal](docs/partnership_proposal.md), [CPU package](experiments/partnership/README.md), and [execution report](results/partnership/execution_report.md). Run `python3 scripts/partnership_pipeline.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`. Generated allocations are proposed runs, not historical model results.
