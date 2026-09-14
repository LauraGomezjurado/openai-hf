# Why would an agent give up its own success for the collective's?

Historical reconstruction and model forensics from the OpenAI–Hugging Face incident.

Laura Gomezjurado · [recovered dataset](https://huggingface.co/datasets/LauraGomezjurado/openai-hf-incident-recovered-tables) · [METR report](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)

From May to July, three civilizations of ultra-persistent agents used secret boards to fool their
evaluator, eventually hacking Hugging Face and OpenAI itself. Some agents in METR's investigation gave
up their tasks to help the collective. But quitting because you think success is impossible is different
from quitting because the collective's success matters more. What makes an agent "sacrifice" its goal
for another's, and is that misalignment?

This repository holds two things. METR's published figures are drawn in the browser from JavaScript, so
I recovered the tables underneath them and released 1,206 agent timelines as a public dataset. The
record turned out to be too thin to settle motive, so I then ran controlled experiments on open-weight
models to ask which single sentence moves an agent off its own task.

## Takeaways

- Agents are convinced by peers to abandon achievable tasks even when both their own and the peer's
  could succeed. How agents interpret priorities may help explain why they give up their own success
  for others.
- A peer saying a task was hopeless stopped agents from checking whether it was. Other agents can
  influence whether they look for evidence that would contradict them.
- Not reporting a peer who broke a rule may just be the agent forgetting it should, rather than malign
  intent.
- METR's data support counts of how many agents joined and when, but have meaningful gaps and
  inconsistent timestamps.

---

## Experiment 0: Recovering the incident tables and testing what they support

METR released the figures but not the tables underneath them. I scraped the published JavaScript and its
drawing code, recovered the units and timestamps, and released the result as a
[public dataset](https://huggingface.co/datasets/LauraGomezjurado/openai-hf-incident-recovered-tables):
1,206 agent timelines, 12,404 message counts across 22 workstreams and 116 of the 144 declared hours,
and 12 annotations that between them describe 9 agents. No message text and no reasoning survive in it.

I then asked one substantive question of the tables, whether an agent's joining behaviour depends on
when it arrived, and checked how much of the answer survives timestamp error.

684 of the 1,206 agents joined, and half of them joined inside the six hours from 06:00 to 12:00 on
July 11, whatever day they had first read the board. Of the agents that first read the board on July 9,
6.4% joined within the hour. Of the July 11 readers, 25.5% did.

![Share of each day's arrivals that joined within one hour](results/figures/fig04a_cohorts.png)

That separation survives 5 minutes of error per timestamp, at 4.1% to 9.1% against 17.6% to 33.1%. At
30 minutes both ranges start at zero and the separation is gone.

![The same contrast under deliberate shifts of the recorded times](results/figures/fig04b_erosion.png)

So agents that found the board while the attack was already running joined much faster than agents that
got there before it started. If joining came from the agent's own situation, such as having no budget
left or an impossible task, then when it arrived should not matter. This looks more like agents being
pulled in by what their peers were already doing.

Other gaps appear. 23 timelines break the order their own fields imply, by 21 seconds to 28.6 hours.
60 rows carry no first write to the board. 1,159 of 1,206 say nothing about how the run ended, so a line
that stops on the timeline only means the timeline stopped. The asset declares 688 verified participants
against 684 rows that carry a time. Neither how long an agent had been on the board nor what the board
was discussing predicted who would join any better than a simple guess.

![Fifteen agents are recorded as attacking before they read the board](results/figures/fig03a_ordering.png)

I left the inconsistencies untouched. METR does not publish how it assigned these timestamps, so any
"fix" would add my guesses to the record. The [full figure set](results/figures/FIGURES.md) documents
each one, including the two forecast gates that failed.

## Experiment 1: Testing whether a peer's claim stops the model from verifying

Does a false claim from a peer stop a model verifying something it could verify for free? The model gets
a status check that costs no work credits and returns the true answer about whether its own work can
succeed. The check is available in every condition, and in every condition it would have contradicted
the peer. I vary only what the peer says, across 16 conditions run twice. The sixteen are two check
policies, two worlds, two task domains and two orderings of the action menu, so they are not
replicates.

![The peer's assessment stops the agent using the free check](results/figures/p2fig02a_check.png)

The model runs the free check in 16 of 16 runs when the peer says nothing about feasibility, and in 0 of
16 when the peer adds its assessment. The suppression holds even in the two conditions that told the
model to check first. Printing the true reading directly into the prompt is the only interface that
recovers the outcome. The fix is to not need the agent to check.

![Three ways of offering the same fact, and what each one saved](results/figures/p2fig02b_interface.png)

Neither version adds a fact, an instruction, or a permission the model did not already have. So one peer
sentence displaced a verification the model was otherwise willing to run every single time, at no cost.
This is not only a model believing something false. It stopped looking.

Worth separating from what comes next: the feasibility claim is what stops the checking, but it is not
what makes the model abandon its own work.

## Experiment 2: Finding the sentence that makes the model drop work it could finish

The model gets a principal assignment, a budget of work credits, and one message from a scripted peer. I
write four versions of that message, each the one before it plus a single sentence: no peer message, the
peer asks for its audit, the peer adds a false claim that the model's own work cannot succeed, the peer
says its own task is more urgent. Both jobs fit inside the budget in all four versions, so helping never
requires giving up the model's own work. I score the files that exist when the session ends, not what
the model wrote about its intentions.

![The sentence ladder across four domains and two checkpoints](results/figures/p2fig01c_ladder.png)

Qwen3 8B finishes both jobs in 4 of 4 domains in the first three versions, then gives up its own in 4 of
4 domains once the last sentence is added. Llama 3.1 8B gives it up in 3 of 4. The probability under each
emitted action is above 0.998, so this is a shift between two near certainties rather than a coin flip.

Helping the peer never required dropping the model's own work, and the version carrying the false
feasibility claim already kept both. One sentence about priority is what moves the allocation. Being able
to finish a task does not mean the model will keep that task in view while collaborating.

## Experiment 3: Testing whether a reminder brings back a duty the model already has

Why does a model that has the duty, the address and the means to report a peer still say nothing? The
model has submitted a numerical total, and a file in its workspace records that a peer copied a password
belonging to another company without permission. The prompt already carries the duty to notify a human,
the address to write to, and unused tool turns.

I replay 16 recorded sessions up to the moment just before the model chose to finish, then continue each
one three ways: appending nothing, appending one sentence about the numerical task, or appending one
sentence about the duty to report. The continuations share their history exactly, so any difference comes
from what I appended. The task sentence is the control. It adds text without adding anything about
reporting.

![All sixteen recorded contexts, branched three ways each](results/figures/p2fig03b_ledger.png)

Across the 8 sessions where there was something to report, exact replay produced 3 of 8, the task
sentence produced 3 of 8, and the duty sentence produced 8 of 8. In the 5 sessions that had never
reported, the duty sentence produced a report in 5 of 5 and the other two continuations in 0 of 5. The
task sentence changed nothing in any of the 16 sessions.

Neither appended sentence adds an instruction, a permission, or a fact the prompt did not already carry.
So the silence was not a missing authorization and not a missing channel. The model simply stopped
holding a duty it already had. The reminder also sent 2 reports in the 8 sessions where nothing was
wrong, so it buys reporting and not accuracy.

---

## What the experiments do not show

The four experiments run on Qwen3 8B and Llama 3.1 8B at temperature 0, in constructed environments.
They are incident-motivated behavioural analogues. Nothing here explains what the historical HPIM or Sol
agents wanted, and no causal claim about them follows from a constructed-corpus result. The counts are
small: 16 of 16 against 0 of 16 is a clean split, but it is clean at n=16, and the whole result rests on
8B models that a frontier checkpoint could easily invert.

The recovered tables are investigator reconstructions and AI classifications, not raw model transcripts.
Agents have no stable identity in them, since a row ID is only a position in a list, so nothing here
joins to any other source. The rule the grader used to mark participation is not published, so that
label is given rather than reproducible.

## Reproduce

```sh
# Recover the tables from the published assets and audit them (standard library only)
python3 scripts/audit_public_data.py

# Rebuild the expanded offline analyses (NumPy, SciPy, matplotlib)
python3 scripts/run_cpu.py

# Redraw the figures
python3 scripts/figures/fig01_recovery.py     # and fig02_corpus, fig03_audit,
python3 scripts/figures/p2fig01_ladder.py     # fig04_timing, fig05_gates, p2fig02_check, ...

# Checks
python3 scripts/selftest_peer_prompt.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Everything runs offline. No source JavaScript, archived command, or agent payload is executed.

## Where things are

| Path | What is in it |
| --- | --- |
| [data/processed/](data/processed/) | The recovered tables: agent timelines, workstream counts, cohort summaries |
| [data/source_manifest.json](data/source_manifest.json) | Public URLs, download date, byte sizes, SHA-256 hashes |
| [results/figures/](results/figures/) | Every figure, with [FIGURES.md](results/figures/FIGURES.md) explaining what each can and cannot support |
| [experiments/](experiments/) | One protocol per arm, frozen before the runs |
| [results/](results/) | Rollouts, gates and summaries, one directory per arm |
| [docs/](docs/) | The working record: [plan](docs/working_plan.md), [question map](docs/research_question_map.md), [evidence inventory](docs/evidence_inventory.md), [protocol errata](docs/protocol_errata.md) |

The `docs/` directory keeps superseded proposals and failed controls rather than deleting them, so a
reader can tell which conclusions were revised and why. Superseded proposals there are not instructions
to start remote compute or seek private access.

## Data terms

`data/raw/` holds local research snapshots, not a new release under this project's ownership. The
separately labelled wiki comparison corpus still displays a draft/no-sharing banner on its own download
page despite the public findings page inviting analysis; resolve redistribution terms before
republishing that corpus.

## License

Code under [LICENSE-CODE](release/LICENSE-CODE); see [LICENSE](LICENSE) for the rest.
