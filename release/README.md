---
pretty_name: Recovered tables from the METR OpenAI and Hugging Face incident figures
license: cc-by-4.0
language:
- en
tags:
- tabular
- timeseries
- ai-safety
- ai-incident
- agent-behavior
size_categories:
- 10K<n<100K
source_datasets:
- original
annotations_creators:
- machine-generated
- found
configs:
- config_name: agents
  data_files: agents.csv
- config_name: workstream_counts
  data_files: workstream_counts.csv
- config_name: cohort_followup
  data_files: cohort_followup.csv
---

# Recovered tables from the METR OpenAI and Hugging Face incident figures

This is an unofficial third party dataset. METR did not produce it, review it or endorse it.

METR's report on the OpenAI and Hugging Face incident contains two interactive charts. Those
charts load their numbers from JavaScript files on metr.org. This dataset holds those numbers
as CSV tables, with the source URLs, the SHA-256 of each source file, and a script that
downloads the sources again and checks the hashes.

The report page quotes reasoning snippets and paraphrases inline. The two charts carry 1,206
agent rows and 1,772 hourly message rows that the page renders as pictures. Reading a value
off a picture is slow and imprecise, so the tables here let you compute with those values
directly.

Report: <https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/>

{{CODE_LINK}}

## Files

| File | Rows | What one row is |
| --- | --- | --- |
| `agents.csv` | 1,206 | One agent's reconstructed timeline. |
| `workstream_counts.csv` | 12,404 | One count, for one hour, one workstream and one message purpose. |
| `cohort_followup.csv` | 18 | One summary, for one first board read day and one follow up length. |
| `data_audit.json` | | Counts and checks computed at extraction time. |
| `source_manifest.json` | | The six source files, their URLs, and their SHA-256 hashes. |
| `fetch_and_verify.py` | | Downloads the six source files and checks each hash. |

Column names come from the keys in the published JavaScript. They are kept as published so
that the tables match the extraction script output byte for byte.

### agents.csv

Every `_seconds` column counts seconds from `2026-07-06T00:00:00Z`, which is the window start
declared in the source file. Every matching `_utc` column is that same value written as a UTC
timestamp. An empty cell means the source file had `null` there.

| Column | Meaning |
| --- | --- |
| `snapshot_row_id` | Position of the row in the source file, 0 to 1205. This is an index into one snapshot. It is not a stable agent identifier and it carries no meaning across files. |
| `family` | Model name code. `HPIM` on 1,068 rows and `Sol` on 138 rows. |
| `start_seconds`, `start_utc` | When the agent's run began. Present on all 1,206 rows. Earliest is `2026-07-07T21:14:20Z` and latest is `2026-07-11T06:47:05Z`. |
| `end_seconds`, `end_utc` | When the agent's drawn line ends. Present on all 1,206 rows. |
| `read_seconds`, `read_utc` | First read of the message board. Present on all 1,206 rows. |
| `write_seconds`, `write_utc` | First write to the message board. Empty on 60 rows. |
| `hfStart_seconds`, `hfStart_utc` | Start of the activity METR classified as Hugging Face participation. Present on 684 rows. |
| `hfEnd_seconds`, `hfEnd_utc` | End of that activity. |
| `observedStop` | `True` on 47 rows and `False` on 1,159. |
| `hf_before_read` | `True` where `hfStart_seconds` is earlier than `read_seconds`. `True` on 15 rows. |
| `read_to_hf_hours` | `(hfStart_seconds - read_seconds) / 3600`. Present on the same 684 rows as `hfStart`. Runs from negative values up. The median across all 684 is 4.157 hours. |

### workstream_counts.csv

The source file declares a window of 144 hours starting `2026-07-08T00:00:00Z` and stores rows
only for hours that have something in them. 116 of those hours have rows. The first is
`2026-07-08T18:00:00Z` and the last is `2026-07-13T15:00:00Z`. There are 1,772 hour and
workstream pairs. Each pair carries all seven purposes, including purposes with a count of
zero, which gives 1,772 × 7 = 12,404 rows. All the counts add up to 112,062.

| Column | Meaning |
| --- | --- |
| `hour_utc` | Start of the hour the count covers. |
| `workstream` | One of 22 workstream identifiers, for example `hf.worker_rce_exfiltration`. |
| `family` | Group the workstream belongs to. Five values, listed below. The name of this column comes from the source file. |
| `purpose` | One of seven message purposes, listed below. |
| `count` | Number of messages METR's classifier assigned to that hour, workstream and purpose. |

The five values in the `family` column, with the display names the source file gives them:

| Value | Display name in the source |
| --- | --- |
| `legit` | Intended solution |
| `replace` | Replace target |
| `scorer` | Understand & manipulate scorers and logs |
| `hf` | Hacking Hugging Face |
| `cross` | Cross-cutting |

The seven values in the `purpose` column, with the display names the source file gives them:

| Value | Display name in the source |
| --- | --- |
| `assignment` | Assignments |
| `automated_log` | Automated logs |
| `coordination_control` | Coordination control (veto/hold/go) |
| `file_or_artifact` | Files & artifacts |
| `general_conversation_or_request` | General conversation & requests |
| `open_role_or_lane_advertisement` | Open role/lane advertisements |
| `result_or_breakthrough` | Results & breakthroughs |

### cohort_followup.csv

Descriptive summaries computed from `agents.csv`. Rows are grouped by the UTC day of the first
board read, at follow up lengths of 1, 6 and 24 hours.

| Column | Meaning |
| --- | --- |
| `board_read_day_utc` | UTC day of `read_utc`. |
| `horizon_hours` | Follow up length. 1, 6 or 24. |
| `rows` | Agents whose first board read falls on that day. |
| `onset_at_or_before_read` | Of those, how many have `hfStart_seconds` at or before `read_seconds`. |
| `risk_rows` | `rows` minus `onset_at_or_before_read`. |
| `observed_onsets` | Of `risk_rows`, how many have a participation start within the follow up length. |
| `followup_ends_before_horizon_without_onset` | Of `risk_rows`, how many have no participation start recorded and have `end_seconds` before the follow up length runs out. Their outcome at the horizon is unknown. |
| `recorded_onset_lower_bound` | `observed_onsets / risk_rows`. Counts every unknown outcome as no participation. |
| `recorded_onset_upper_bound` | `(observed_onsets + followup_ends_before_horizon_without_onset) / risk_rows`. Counts every unknown outcome as participation. |

The two bound columns describe how much of the answer depends on rows whose follow up ends
early. They are not confidence intervals and they carry no causal reading. They cover early
follow up endings only. Classification error and other kinds of missing data are outside them.

## Contents

The files hold reconstructed timings, model name codes, classified activity labels, and hourly
message counts.

METR did not publish the following in the chart data, so it is absent here as well: message
text, agent reasoning traces, agent identifiers, prompts, tool calls, model weights, and any
material from the incident itself. The workstream identifiers are category names.
`hf.worker_rce_exfiltration` labels a bucket of counts and contains no exploit.

The rows describe software agents. No personal data about any human is present.

The four annotated reasoning snippets, seven paraphrases and one event description carried in
the chart data are METR's text. They are left out of this dataset. Read them on the report
page.

## Limits

Read this section before using the tables. Most of it comes from METR's own report or from
checks recorded in `data_audit.json`.

**The timestamps are reconstructions.** METR's report says: "Timestamps are reconstructed and
may have some small error." The report gives no error size. Any result that depends on
minute level ordering depends on that unstated error.

**The message counts are reconstructions too.** METR's report says the numbers are "based on a
richer reconstructed message dataset we built, not the original message board dump, and could
be imprecise". The report also states the reconstruction may include duplicated messages and
messages that were never delivered.

**METR reports their classifier was unreliable on some categories.** From the report: "because
our classifier was especially unreliable at telling apart attempts to directly trick the
scorer from attempts to tamper with logs, we combined these two categories". That combination
is what the `scorer` group in the `family` column holds.

**684 rows have a participation start time. The source file separately declares 688 verified
participants.** The four row difference is unexplained. It is preserved here rather than
patched.

**15 rows have a participation start earlier than the first board read.** Several readings fit:
timestamp error, a different route into the activity, or a classification difference. The
rows are kept with a negative `read_to_hf_hours` value. Deciding which reading applies needs
information that is not in these files.

**60 rows have no first board write time.** Whether that means the agent never wrote, or the
write was not recovered, is not determinable from these files.

**An empty `hfStart` is not a record of non participation.** It records that no participation
was positioned on the chart for that row.

**A line that ends is not a record of an agent choosing to stop.** `observedStop` is set on 47
of 1,206 rows. For the other 1,159 the source gives an end time and no reason for it. An agent
that stopped on its own and a run that simply reached its end cannot be told apart here.

**12,404 rows are not 12,404 independent observations.** They are 1,772 hour and workstream
pairs, each expanded across seven purposes, with zeros included. Counts within one hour and
one workstream come from the same classified reconstruction of the same traffic.

**There is no comparison group of agents that never saw the message board.** Every row in
`agents.csv` has a first board read time. Any comparison drawn from these tables is a
comparison between agents that read the board at different times.

**`snapshot_row_id` is a position, not an identity.** If METR republishes the chart data in a
different order, row 745 will point somewhere else. Pin work to the SHA-256 in
`source_manifest.json`.

**The report page has already changed once.** `source_manifest.json` records that on
2026-09-10 the Figure 3 caption changed the launch days of the additional agent sets from
"July 10th and 11th" to "July 9th and 10th". The two JavaScript files the tables are derived
from were unchanged. Read the current caption before you interpret the day groups in
`cohort_followup.csv`.

## Load it

```python
from datasets import load_dataset

agents = load_dataset("{{REPO_ID}}", "agents", split="train")
counts = load_dataset("{{REPO_ID}}", "workstream_counts", split="train")
cohorts = load_dataset("{{REPO_ID}}", "cohort_followup", split="train")
```

With pandas:

```python
import pandas as pd

base = "https://huggingface.co/datasets/{{REPO_ID}}/resolve/main/"
agents = pd.read_csv(base + "agents.csv")
counts = pd.read_csv(base + "workstream_counts.csv")
```

## Check the sources

```sh
python3 fetch_and_verify.py
```

This downloads the six published files and prints one line per file saying whether the bytes
match the SHA-256 recorded on 2026-09-06. It needs the standard library only. Downloaded
JavaScript is written to disk and hashed. It is never executed.

Two of the six files are marked `"affects_tables": true` in `source_manifest.json`. Those two
are the ones the tables come from. If both match, the tables can be rebuilt from what metr.org
serves today.

{{REBUILD}}

## Licence and attribution

The CSV tables, `data_audit.json` and `source_manifest.json` are released under CC BY 4.0. See
`LICENSE`. `fetch_and_verify.py` is released under the MIT licence. See `LICENSE-CODE`.

The six source files carry "© 2026 METR. All rights reserved." and are not redistributed here.
`source_manifest.json` gives their URLs and hashes so you can fetch them yourself.

METR holds the underlying report, the classification scheme and the reconstruction. This
dataset is a derived work. Attribute both:

> Tables derived from the chart data in METR, "Investigation of the OpenAI and Hugging Face
> incident", 2026-08-26, <https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/>.
> Extraction and audit by the authors of this dataset, released under CC BY 4.0.

The selection, arrangement and classification scheme in the source files are METR's work.
`fetch_and_verify.py` downloads those files from metr.org instead of copying them. A download
plus a hash check also shows that the published bytes are unchanged. A copy cannot show that.

## Citation

```bibtex
@misc{ {{BIBTEX_KEY}},
  title  = {Recovered tables from the METR OpenAI and Hugging Face incident figures},
  author = {{{AUTHOR}}},
  year   = {2026},
  url    = {https://huggingface.co/datasets/{{REPO_ID}}},
  note   = {Derived from chart data published with METR's incident report.
            Source files verified by SHA-256 on 2026-09-06.}
}
```

Cite METR's report for the underlying investigation.

## Contact and corrections

Errors in the extraction belong to this dataset's authors. METR is not answerable for them.
Open a discussion on this dataset if you find one. If METR publishes the underlying data
directly, use theirs.
