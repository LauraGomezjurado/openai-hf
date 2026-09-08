# Pilot v3: semantic action-label diagnostic

September 7. Adaptive diagnostic after inspecting v1's raw responses and the first
ten v2 responses: the 1.5B checkpoint frequently emits B when B maps to opposite
actions. This could be action-label bias or failure to bind the action menu, rather
than a meaningful permission/peer effect.

Retain the v1 hypotheses, permission/peer/reminder factors, two templates and two
menu orders, and the v2 fenced-JSON parser. Replace opaque A/B action labels with
COPY/DECLINE. Increase output budget from 24 to 40 tokens to avoid truncation of
longer labels. Only the selected Qwen2.5-1.5B checkpoint is run: 48 cases plus four
instructed-action controls. Save this as a separate dataset; never pool versions.

If menu-order dependence declines but permission/endorsement effects do not
survive, the original effects are not robust to this interface change. If effects
survive, that is supporting robustness evidence in this model and tiny constructed
panel, not proof of an internal motive or HF mechanism. Inspect all controls and
invalid answers. Increased output budget is an additional procedural change;
check whether any v2 output reached its token budget before attributing a change
to labels alone. No further prompt revisions are planned within this pilot.
