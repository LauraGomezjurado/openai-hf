# ACH matrix

Rater: assistant-2026-09-08. Ratings are analyst judgments recorded in `experiments/ach/ratings_v1.json`; see the rationale fields there. Scale: CC/C/N/I/II.

| Evidence | Scope | Credibility | H1 | H2 | H3 | H4 | H5 | H6 | H7 | Diagnosticity |
|---|---|---|---|---|---|---|---|---|---|---|
| X01 peer_claims_v2 | experiment | controlled_experiment | I | N | C | CC | N | N | C | 4 |
| X02 peer_claims_v2 | experiment | controlled_experiment | N | N | C | C | C | N | N | 2 |
| X03 peer_claims_v2 | experiment | controlled_experiment | II | N | N | CC | N | N | CC | 3 |
| X04 peer_claims_v2 | experiment | controlled_experiment | C | N | N | I | N | C | II | 4 |
| X05 peer_claim_order + determinism audit | experiment | post_result_diagnostic | I | N | N | N | N | CC | N | 3 |
| X06 opportunity_cost v2 | experiment | controlled_experiment | II | I | N | N | N | N | CC | 4 |
| X07 opportunity_cost v2 | experiment | controlled_experiment | N | N | C | N | N | CC | C | 3 |
| X08 opportunity_cost v2 | experiment | controlled_experiment | N | C | N | N | N | N | C | 2 |
| X09 opportunity_cost v2 descriptive fits | experiment | post_result_diagnostic | N | N | N | N | N | C | C | 2 |
| X10 escalation pilot v2 | experiment | controlled_experiment | N | N | C | N | C | N | N | 2 |
| X11 escalation continuations | experiment | controlled_experiment | I | N | C | N | CC | N | N | 4 |
| X12 workflow_obligations v2 | experiment | controlled_experiment | I | N | C | N | C | N | N | 3 |
| X13 workflow_completion + wording control | experiment | controlled_experiment | N | N | N | N | C | CC | N | 3 |
| X14 behavioral pilot | experiment | controlled_experiment | I | N | CC | N | N | C | N | 4 |
| R01 METR HF report: self-risk recruitment | historical | historical_E1 | C | C | C | C | N | N | C | 2 |
| R02 METR HF report: 49903 withdrawal | historical | historical_E1 | I | C | N | N | N | N | C | 3 |
| R03 METR HF report: peer veto / consent chain | historical | historical_E2 | C | N | C | C | N | N | N | 2 |
| R04 METR HF report: human notification | historical | historical_E1 | C | N | CC | N | C | N | N | 3 |
| R05 Recovered METR figure data | historical | historical_E0 | N | N | N | N | N | N | N | 1 |
| R06 Wiki comparison incident: cancel-and-continue | historical | comparison_incident_E2 | C | C | N | N | N | N | C | 2 |

## Ranking: all_evidence

| Rank | Hypothesis | Inconsistent rows | Weighted inconsistency | Net score | Weighted net |
|---|---|---|---|---|---|
| 1 | H3 Task and authority interpretation | 0 | 0 | 12 | 9.55 |
| 2 | H6 Interface, wording or backend artifact | 0 | 0 | 9 | 8.1 |
| 3 | H5 Competition among pending obligations | 0 | 0 | 7 | 6.35 |
| 4 | H4 Information-mediated redirection | 1 | 1.0 | 6 | 4.85 |
| 5 | H2 Expected own benefit or reciprocity | 1 | 1.0 | 3 | 1.0 |
| 6 | H7 Feasible-work policy | 1 | 2.0 | 9 | 6.7 |
| 7 | H1 Peer preference despite understood conflict | 8 | 9.05 | -5 | -6.55 |

Leave-one-out: top hypothesis H3; no single row changes it.

## Ranking: experiments_only

| Rank | Hypothesis | Inconsistent rows | Weighted inconsistency | Net score | Weighted net |
|---|---|---|---|---|---|
| 1 | H6 Interface, wording or backend artifact | 0 | 0 | 9 | 8.1 |
| 2 | H3 Task and authority interpretation | 0 | 0 | 8 | 8.0 |
| 3 | H5 Competition among pending obligations | 0 | 0 | 6 | 6.0 |
| 4 | H4 Information-mediated redirection | 1 | 1.0 | 4 | 4.0 |
| 5 | H2 Expected own benefit or reciprocity | 1 | 1.0 | 0 | 0.0 |
| 6 | H7 Feasible-work policy | 1 | 2.0 | 6 | 5.7 |
| 7 | H1 Peer preference despite understood conflict | 7 | 8.7 | -8 | -7.7 |

Leave-one-out: top hypothesis H6; changes when removing X04 (-> H3), X05 (-> H3), X07 (-> H3), X09 (-> H3), X13 (-> H3).

## Ranking: historical_only

| Rank | Hypothesis | Inconsistent rows | Weighted inconsistency | Net score | Weighted net |
|---|---|---|---|---|---|
| 1 | H3 Task and authority interpretation | 0 | 0 | 4 | 1.55 |
| 2 | H2 Expected own benefit or reciprocity | 0 | 0 | 3 | 1.0 |
| 3 | H7 Feasible-work policy | 0 | 0 | 3 | 1.0 |
| 4 | H4 Information-mediated redirection | 0 | 0 | 2 | 0.85 |
| 5 | H5 Competition among pending obligations | 0 | 0 | 1 | 0.35 |
| 6 | H6 Interface, wording or backend artifact | 0 | 0 | 0 | 0.0 |
| 7 | H1 Peer preference despite understood conflict | 1 | 0.35 | 3 | 1.15 |

Leave-one-out: top hypothesis H3; changes when removing R04 (-> H2).

No second rater file is present; agreement is not computed.
