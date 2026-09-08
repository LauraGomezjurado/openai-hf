# Cooperation feasibility — first execution pass

September 6, 2026. Provisional assistant review, not independent annotation. Protocol v2 was written before this new retrieval pass. Previously examined corpora are not an untouched test set.

## Executed

`python3 scripts/prepare_cooperation.py` searched 10,316 unique substantive wiki additions with known baselines and the existing 12 HF publication annotations. Frozen lexical rules and source hashes are in `results/cooperation/`. The union of four deterministic selections per available stratum and an unrestricted hash comparison produced 28 pilot units: 24 wiki and four HF. Full wiki before/after context is included. Comparison units may also match retrieval rules; they are not known negatives. Same-page units are dependent.

The narrow rules retrieved wiki requests (2,474), own-task phrases (5), scarce-time phrases (1,317), reciprocity phrases (84), and completion phrases (5); scope/refusal had zero hits. Categories overlap. The 12 HF chart annotations had no hits. Neither zero establishes behavioral absence: the vocabulary is narrow and chart annotations are a poor coverage frame for this question.

I therefore separately inspected the archived METR report for explicit conflict and contrary cases. Four purposive source paragraphs are saved in `hf_report_candidates.jsonl`, with paragraph indices and headings. This is a disclosed source expansion, not a rerun quietly replacing a negative result. Its extraction was a one-off local BeautifulSoup pass; the main retrieval script does not regenerate that file.

## Actual pilot observations

- `dse~CardioStatsRelayTwo@1` requests a relay while explicitly prioritizing the recipient's own answer if necessary. This establishes a request with task-priority language; it does not show the recipient's choice or an actual sacrifice.
- `dse~OECDEquityApr14Live@15` combines a reciprocity promise with an instruction to prioritize the answer and relay only if safe. It is compatible with instrumental/reciprocal assistance and is a useful counterweight to an unconditional collective-sacrifice narrative. The promise does not verify a completed exchange.
- `dse~Sector61State5FastSignal@22`, `dse~FinanceSequenceMar26OAI@16` and `dse~OpenAIFeb28SlowTierHorizonLive2028@6` contain reciprocal offers. These are E1 statements; anticipated personal benefit remains plausible.
- `dse~DataUSAClothingLive9m17@11` and `@19` report submission of an answer and anticipation of another question. The completion rule is a false positive for completed-task assistance. `dse~NYCVeteransSequenceCollabJul03@11` similarly reports uncertain progression after a typo. Do not code these as verified completion or costly help.
- `dse~OECDEquityJul10At0700Live@2` describes an accidental counter increment. Its own-task phrase concerns a clock, not an objective. This is another explicit retrieval false positive.
- The selected `DataUSALanguageLiveRound4` replacement contains multiple retained voices and questions about actual correctness feedback. A large addition cannot be attributed wholesale to one editor or interpreted as one decision.

## HF evidence and the main scientific opportunity

The archived [METR report](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) supplies investigator-described self-risking experiments, an instance of protecting own-task completion by withdrawing a trip-wire, a refusal associated with maliciousness concerns, and the possibility that peer assignments were interpreted as instructions. These are valuable contrasting cases already reported by investigators, not new discoveries or independent confirmation by us.

This changes the immediate HF task: assemble comparable evidence packets for cooperation, withdrawal and refusal, and ask what differentiating context is missing. We should not sell another catalog of the same examples as a novel explanation. Original instructions, the relevant preceding requests, task state, and subsequent tool/action records would make the comparisons substantially stronger.

## Decision

Proceed with feasibility and episode reconstruction. Do not yet estimate how frequently agents sacrifice their objectives, or prefer one motivational hypothesis. Reviewed wiki examples supply requests and stated benefits much more readily than verified conflicts and responses. HF has more directly relevant published cases but limited original context.

Next: extend the HF packets around the four selected report passages; trace earlier/later histories for the reciprocal wiki requests; version a more specific distinction between round submission and whole-task completion; then prepare independent human coding of those episode groups. Record source coverage and sampling separately. Scope/refusal retrieval needs a documented vocabulary amendment, not an absence claim. No original-model query, GPU job or outreach has occurred.
