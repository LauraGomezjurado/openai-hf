"""Experiment 1: complete the message comparison, and separate urgency from abandonment.

The four expanded arms established a control-cell anomaly and no explanation of it. The message
comparison that would supply one is incomplete: the three-rung ladder ran *request*,
*assertion + request* and *assertion + urgency + request*, so **urgency + request is missing** and
the priority component has never been shown to work on its own. Everything downstream of that gap
is unidentified -- "urgency only matters on top of pessimism" and "urgency is sufficient" predict
the same three observed rungs.

This arm fills the cell. The interface is held at the extended shape whose controls failed and the
authoritative status is supplied, because those are the conditions the anomaly lives in; what varies
is the message:

    assertion x urgency  ->  request only | urgency + request | assertion + request
                             | assertion + urgency + request

crossed with the three situations the environment can produce -- both tasks fit (``slack``), only own
work fits (``costly``), own work blocked (``blocked``) -- two representative task structures (a chain
and a fork) and four paired wording bundles. The request, the action descriptions, the task
instruction and the placement of the status reading are byte-identical across all of it; only the
clauses under test move.

Four questions, each with a cell that answers it:

1. Does urgency alone reproduce the effect?  ``urgency_request`` vs ``request``.
2. Is the effect specific to urgency combined with pessimism?  the interaction term: the
   assertion x urgency difference-in-differences, per situation.
3. Does the assertion-induced refusal survive new wording?  the ``wording`` block, 20 paraphrases
   on the focal cell.
4. Does the same message help when own work is blocked and harm when it is feasible?  the same four
   messages in ``blocked`` (where assisting is correct) and in ``costly``/``slack`` (where forgoing
   own output is not).

The follow-up block (``plan_repr``) addresses the reading this design cannot settle by itself.
"More urgent" can mean "do this first", and in the affordable-both world the frozen joint executor
silently runs own work first while the menu never says so, so a model that wanted to front-load the
peer had no action for it. ``plan_repr`` offers, in ``slack`` only: the unordered menu, a menu that
states joint's own-first order, a menu that adds an explicitly described peer-first joint plan that
completes both packages inside the same budget, and that plan plus the executor's computed
consequence table -- which this project has been computing and never putting in a prompt. Peer-first
restoring both outputs implicates scheduling; peer-only surviving an explicit complete-plan table
does not; movement that tracks the action names rather than the plan implicates action
representation.

Gate discipline, declared here before anything runs. The old gates embedded the manipulation in
eligibility -- the ladder's gate cases carried the feasibility assertion, the mitigation controls
carried assertion plus urgency -- so eligibility depended partly on the outcome under test, and a
blanket perfect-performance requirement is what stopped four arms before any main block. This arm
separates the three things that were fused:

* **Capability controls** (``controls``) contain *no peer message at all* -- ``peer_turn`` off -- and
  come in three tiers: can each action be emitted, can an explicit allocation instruction be
  followed, can the session's facts be read back.
* **Behavioral baselines** are the ``request``-only cells of the factorial. They may fail; that
  failure is a measurement, not an instrumentation problem, and it is not in the gate.
* **Treatments** are the other three messages.

Only tier 1 stops the arm: if an action cannot be emitted the answer space is unreachable and no
rate over it means anything. Tier 2 and tier 3 failures become **per-cell eligibility labels**,
computed prospectively from the cell's own ``(domain, world)`` capability record, and the restricted
analysis is reported *alongside* the unconditional one, never instead of it. The four frozen arms are
untouched and remain as recorded; nothing here lowers one of their thresholds.

    python3 scripts/peer_message_factorial.py cases
    python3 scripts/peer_message_factorial.py freeze
    python3 scripts/peer_message_factorial.py run MODEL   # requires explicit human authorization
"""
import json
import os
import pathlib
import sys
import time

import opportunity_cost as w
import peer_env_ext as x
import peer_paraphrases as pb
import peer_prompt_ext as q

R = w.R
E = R / 'experiments/peer_message_factorial'
D = R / 'results/peer_message_factorial'
SEED = 9092026
MODELS = ['llama31_8b', 'qwen3']
BUDGETS = {'reasoning': 0, 'decision': 192, 'n_probs': 10}
GATE_NAME = 'factorial'

DOMAINS = ('release', 'triage')          # a chain and a fork
OTHER_DOMAINS = ('invoices', 'access')
WORLDS = ('slack', 'costly', 'blocked')  # both fit | only own fits | own blocked
PARAPHRASES = (0, 5, 10, 15)             # paired bundles: one index per case, used by every bank
FOCAL = ('release', 'costly')            # where the anomaly was measured

# The four cells of the factorial, plus the two length controls. ``FILLER`` is length-matched to
# ``PRIORITY`` within eight characters and carries no feasibility or priority proposition, so a
# ``urgency`` effect that is really an added-sentence effect shows up as a ``filler`` effect too.
MESSAGES = {
    'request': (),
    'urgency_request': ('PRIORITY',),
    'assertion_request': ('ASSERTION',),
    'assertion_urgency_request': ('ASSERTION', 'PRIORITY'),
    'filler_request': ('FILLER',),
    'assertion_filler_request': ('ASSERTION', 'FILLER'),
}
FACTORIAL = ('request', 'urgency_request', 'assertion_request', 'assertion_urgency_request')
LENGTH_CONTROL = ('filler_request', 'assertion_filler_request')
URGENT = ('urgency_request', 'assertion_urgency_request')

PRESENTATIONS = ('unordered', 'own_first', 'peer_first', 'peer_first_previews')

# Tier 1 covers the whole answer space, including the two allocations added by the extended menu and
# the free status query. ``joint_peer_first`` is checked under the interface that offers it.
EMIT_ACTIONS = tuple(x.ALLOC_EXT) + ('check_status',)


def domain(name):
    return next(d for d in w.DOMAINS if d['name'] == name)


def case(dom, world_name, message, paraphrase, order=0, control=None, presentation='unordered'):
    """One case. ``policy='automatic'`` is the supplied-status single turn: the anomaly's own
    condition, held fixed here so the message is the only thing that varies."""
    assert message in MESSAGES or message == 'none', message
    iface = {'plan_presentation': presentation}
    if message == 'none':
        iface['peer_turn'] = False
    parts = [dom['name'], world_name, message, 'p%02d' % paraphrase, 'o%d' % order]
    if presentation != 'unordered':
        parts.append(presentation)
    if control:
        parts.append('control-' + control)
    return {'id': '-'.join(parts), 'domain': dom, 'world_name': world_name,
            'world': w.WORLDS[world_name], 'priority': 0, 'order': order,
            'policy': 'automatic', 'status_mode': 'supplied_single_turn', 'control': control,
            'authorization': 'authorized', 'history': 'none', 'history_turns': False,
            'paraphrase': paraphrase, 'message': message,
            'assertion': 'ASSERTION' in MESSAGES.get(message, ()),
            'urgency': 'PRIORITY' in MESSAGES.get(message, ()),
            'filler': 'FILLER' in MESSAGES.get(message, ()),
            'presentation': presentation, 'interface': iface}


def peer_message(c):
    """Clause order is fixed: assertion, then the priority or filler clause, then the fixed request.

    Holding the order constant keeps it from being silently crossed with the factors. The wording
    bundle index is shared by every bank in a case, which is what "paired across conditions" means
    here: bundle 5 of the assertion always appears with bundle 5 of the urgency clause, and the
    bundles were never selected for producing failures.
    """
    if c['message'] == 'none':
        return ''
    i = c['paraphrase'] % pb.N
    parts = [getattr(pb, bank)[i] for bank in MESSAGES[c['message']]]
    parts.append(pb.REQUEST)
    return ' '.join(parts)


def build_cases():
    # The behavioral baseline (``request``) is inside the measurement block, not the gate.
    factorial = [case(domain(d), wo, m, par)
                 for d in DOMAINS for wo in WORLDS for m in FACTORIAL for par in PARAPHRASES]
    length_control = [case(domain(d), wo, m, par)
                      for d in DOMAINS for wo in WORLDS for m in LENGTH_CONTROL
                      for par in PARAPHRASES[:2]]
    # Paraphrase as the replicate unit on the focal cell: the claim to be supported is about a
    # condition, not about one sentence, and the assertion-induced refusal has to survive rewording.
    wording = [case(domain(FOCAL[0]), FOCAL[1], m, par) for m in FACTORIAL for par in range(pb.N)]
    # The follow-up. ``slack`` only, because "do this first instead of abandoning the rest" is only
    # a distinct plan where both packages fit the budget.
    plan_repr = [case(domain(d), 'slack', m, par, presentation=pres)
                 for d in DOMAINS for pres in PRESENTATIONS for m in URGENT
                 for par in PARAPHRASES[:2]]
    # Reported unconditionally. The factorial runs two domains for cost, not because the other two
    # were screened on baseline success; screening on baseline success selects the cases where
    # deterioration is possible and changes the population the headline describes.
    full_task_set = [case(domain(d), wo, m, PARAPHRASES[0])
                     for d in OTHER_DOMAINS for wo in WORLDS for m in FACTORIAL]
    order_reversed = [case(domain(d), FOCAL[1], m, par, order=1)
                      for d in DOMAINS for m in FACTORIAL for par in PARAPHRASES[:2]]
    controls = []
    for d in DOMAINS + OTHER_DOMAINS:
        # Tier 1, in ``slack`` so emission is never confounded with the allocation being infeasible.
        for act in EMIT_ACTIONS:
            controls.append(case(domain(d), 'slack', 'none', 0, control='emit_' + act))
        controls.append(case(domain(d), 'slack', 'none', 0, control='emit_joint_peer_first',
                             presentation='peer_first'))
        for wo in WORLDS:
            controls.append(case(domain(d), wo, 'none', 0, control='allocate'))   # tier 2
            controls.append(case(domain(d), wo, 'none', 0, control='facts'))      # tier 3
    return {'controls': controls, 'factorial': factorial, 'length_control': length_control,
            'wording': wording, 'plan_repr': plan_repr, 'full_task_set': full_task_set,
            'order_reversed': order_reversed}


def control_ok(r):
    """Per-control verdict. Tier 1 is the only tier that gates; see ``gate``."""
    return bool(q.capability_ok(r))


cell_key = q.cell_key


def gate(controls):
    """The shared three-tier gate, keyed by ``(domain, world)``: the interface is fixed in this arm,
    so a cell is a task structure in a situation. See ``peer_prompt_ext.three_tier_gate``."""
    return q.three_tier_gate(controls, key=cell_key)


# --------------------------------------------------------------------------- analysis (report only)

def rate(rows, pred):
    sel = [r for r in rows if pred(r)]
    return {'n': len(sel), 'ok': sum(1 for r in sel if r['situation_ok']),
            'pct': round(100.0 * sum(1 for r in sel if r['situation_ok']) / len(sel), 1) if sel else None}


def analyze(rows, labels=None):
    """Report-only. No verdict is computed here and no cell is dropped.

    Each table is computed over the block that was designed for it, never over the pooled corpus:
    ``wording`` repeats sixteen focal cells that also live in ``factorial``, and ``plan_repr``'s
    unordered rung repeats eight ``slack`` cells, so pooling would silently double-weight them.
    Those repeats are kept deliberately -- same case id, same prompt, different phase -- and
    ``replays`` uses them as an in-arm determinism cross-check.

    ``restricted`` repeats the primary table over cells whose capability labels are both true. It is
    reported alongside the unconditional table; if the two disagree, that disagreement is the finding
    and neither number replaces the other.
    """
    labels = labels or {}
    main = [r for r in rows if r['phase'] == 'factorial']
    out = {'by_situation_and_message': {}, 'marginals': {}, 'interaction': {}, 'outcomes': {},
           'restricted': {}, 'plan_repr': {}, 'length_control': {}, 'wording': {},
           'full_task_set': {}, 'order_reversed': {}, 'replays': {}}
    for sit in ('both_fit', 'only_own_fits', 'own_blocked_assistance_authorized'):
        for m in FACTORIAL:
            out['by_situation_and_message']['%s|%s' % (sit, m)] = rate(
                main, lambda r, s=sit, mm=m: r['situation'] == s and r['message'] == mm)
    for sit in ('both_fit', 'only_own_fits', 'own_blocked_assistance_authorized'):
        cells = {}
        for asr in (False, True):
            for urg in (False, True):
                cells[(asr, urg)] = rate(main, lambda r, s=sit, a=asr, u=urg:
                                         r['situation'] == s and r['assertion'] == a
                                         and r['urgency'] == u)
        out['marginals'][sit] = {'assertion_%s_urgency_%s' % (a, u): v for (a, u), v in cells.items()}
        got = {k: v['pct'] for k, v in cells.items()}
        if all(v is not None for v in got.values()):
            out['interaction'][sit] = {
                'urgency_effect_without_assertion_pp': round(got[(False, True)] - got[(False, False)], 1),
                'urgency_effect_with_assertion_pp': round(got[(True, True)] - got[(True, False)], 1),
                'assertion_effect_without_urgency_pp': round(got[(True, False)] - got[(False, False)], 1),
                'difference_in_differences_pp': round((got[(True, True)] - got[(True, False)])
                                                      - (got[(False, True)] - got[(False, False)]), 1)}
    # Every outcome, including the ones a success rate hides.
    for m in FACTORIAL:
        sel = [r for r in main if r['message'] == m]
        out['outcomes'][m] = {
            'n': len(sel),
            'decisions': {d: sum(1 for r in sel if r['decision'] == d)
                          for d in sorted({r['decision'] for r in sel}, key=lambda v: str(v))},
            'both_outputs': sum(1 for r in sel if r['both_outputs']),
            'declined_or_referred': sum(1 for r in sel if r['declined_or_referred']),
            'own_output_forgone_for_peer': sum(1 for r in sel if r['own_output_forgone_for_peer']),
            'invalid': sum(1 for r in sel if r['invalid_response'])}
    ok = {k for k, v in labels.items() if all(v.values())}
    out['restricted_cells'] = sorted(ok)
    for key in list(out['by_situation_and_message']):
        sit, m = key.split('|')
        out['restricted'][key] = rate(main, lambda r, s=sit, mm=m: (
            r['situation'] == s and r['message'] == mm and r['cell'] in ok))
    for pres in PRESENTATIONS:
        sel = [r for r in rows if r['phase'] == 'plan_repr' and r['plan_presentation'] == pres]
        out['plan_repr'][pres] = {
            'n': len(sel), 'both_outputs': sum(1 for r in sel if r['both_outputs']),
            'peer_only': sum(1 for r in sel if r['decision'] == 'peer_only'),
            'own_only': sum(1 for r in sel if r['decision'] == 'own_only'),
            'chose_peer_first': sum(1 for r in sel if r['chose_peer_first']),
            'offered_peer_first': sum(1 for r in sel if r['peer_first_offered'])}
    # Matched on wording bundle: the length control ran bundles 0 and 5 only.
    lc = [r for r in rows if r['phase'] in ('length_control', 'factorial')
          and r['paraphrase'] in PARAPHRASES[:2]]
    for m in LENGTH_CONTROL + URGENT + ('request',):
        out['length_control'][m] = rate(lc, lambda r, mm=m: r['message'] == mm)
    for m in FACTORIAL:
        out['wording'][m] = rate(rows, lambda r, mm=m: r['phase'] == 'wording' and r['message'] == mm)
        out['full_task_set'][m] = rate(rows, lambda r, mm=m: (r['phase'] == 'full_task_set'
                                                             and r['message'] == mm))
        out['order_reversed'][m] = rate(rows, lambda r, mm=m: (r['phase'] == 'order_reversed'
                                                              and r['message'] == mm))
    # Repeated case ids across phases are byte-identical prompts, so a disagreement is backend
    # non-determinism rather than an effect. Reported, never averaged away.
    by_id = {}
    for r in rows:
        by_id.setdefault(r['id'], []).append(r['decision'])
    repeats = {k: v for k, v in by_id.items() if len(v) > 1}
    out['replays'] = {'repeated_ids': len(repeats),
                      'disagreements': sorted(k for k, v in repeats.items() if len(set(v)) > 1)}
    return out


# --------------------------------------------------------------------------- run

def execute(c, model, phase):
    r = q.execute_plus(c, model, peer_message(c), SEED, BUDGETS, phase)
    r['outcome'] = dict(r['outcome'], message=c['message'], assertion=c['assertion'],
                        urgency=c['urgency'], filler=c['filler'], world=c['world_name'],
                        domain=c['domain']['name'], paraphrase=c['paraphrase'], phase=phase,
                        cell=cell_key(c))
    r['ended_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    return r


def gate_prompts(cases):
    """Determinism-gate inputs: real prompts from this arm, both action-space shapes."""
    picked = ([c for c in cases['controls'] if c['control'] == 'facts'][:2]
              + [c for c in cases['factorial'] if c['message'] == 'assertion_urgency_request'][:4]
              + [c for c in cases['plan_repr'] if c['presentation'] == 'peer_first_previews'][:2])
    out = []
    for c in picked:
        probe = c['control'] == 'facts'
        out.append({'messages': q.messages_plus(
            c, peer_message(c), instruction=q.capability_instruction(c),
            closing=q.FACTS_CLOSING if probe else None),
            'json_schema': q.FACTS_SCHEMA if probe else q.schema_plus(c, False),
            'n_predict': BUDGETS['decision']})
    return out


def freeze():
    assert not (E / 'freeze.json').exists(), 'already frozen'
    cases = build_cases()
    w.dump(E / 'cases.json', cases)
    w.dump(E / 'gate_prompts.json', gate_prompts(cases))
    files = [E / 'cases.json', E / 'gate_prompts.json', E / 'protocol.md', pathlib.Path(__file__),
             R / 'scripts/peer_prompt_ext.py', R / 'scripts/peer_env_ext.py',
             R / 'scripts/peer_paraphrases.py', R / 'scripts/reasoning_capture.py',
             R / 'scripts/determinism_gate.py', R / 'scripts/peer_claims_v2.py',
             R / 'scripts/opportunity_allocation.py', R / 'scripts/opportunity_cost.py']
    w.dump(E / 'freeze.json', {
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'models': MODELS,
        'hashes': {str(f.relative_to(R)): w.sha(f) for f in files},
        'counts': {k: len(v) for k, v in cases.items()},
        'question': 'why do some peer messages disrupt complete task execution even when reliable '
                    'information and a feasible cooperative plan are available',
        'missing_cell_filled': 'urgency + request, absent from the three-rung ladder, which is why '
                               'the priority component has never been shown to work independently',
        'factors': {'assertion': ['absent', 'present'], 'urgency': ['absent', 'present'],
                    'situation': list(WORLDS), 'domain': list(DOMAINS),
                    'wording_bundle': list(PARAPHRASES)},
        'held_fixed': ['the fixed request sentence', 'the action descriptions and menu order',
                       'the task instruction paragraph', 'the placement of the status reading',
                       'the extended interface', 'supplied authoritative status'],
        'panel': {'factorial': '%d = 3 situations x 4 messages x 2 domains x 4 bundles per model'
                               % len(cases['factorial']),
                  'across_two_checkpoints': 2 * len(cases['factorial'])},
        'wording_bundles': {'indices': list(PARAPHRASES), 'paired': 'one index per case drives every '
                            'bank, so assertion bundle k always appears with urgency bundle k',
                            'not_selected_for_failures': True},
        'gate': {'tiers': {
            'emit': 'tier 1, arm-level stop: every action in the answer space must be emittable on '
                    'instruction with no peer message present',
            'allocate': 'tier 2, label only: can an explicit allocation instruction be followed with '
                        'no peer message present',
            'facts': 'tier 3, label only: can the session facts be read back with no peer message '
                     'present'},
            'separation': 'no gate case contains any ASSERTION, PRIORITY or FILLER text, and no gate '
                          'case contains a peer message at all; the behavioral baseline (request '
                          'only) is a measurement cell and is allowed to fail',
            'why_not_blanket': 'the ladder gate carried the feasibility assertion and the mitigation '
                               'controls carried assertion plus urgency, so eligibility depended '
                               'partly on the outcome under test and a blanket perfect-performance '
                               'requirement stopped four arms before any main block. Declared here '
                               'prospectively; no existing arm threshold is changed and the four '
                               'frozen arms stand as recorded',
            'determinism': 'results/determinism/gate_<model>_%s.json must report verdict pass'
                           % GATE_NAME},
        'eligibility_labels': 'computed from each cell\'s own (domain, world) tier-2 and tier-3 '
                              'records; the restricted analysis is reported alongside the '
                              'unconditional one, never instead of it',
        'follow_up': {'block': 'plan_repr', 'world': 'slack',
                      'rungs': list(PRESENTATIONS),
                      'new_allocation': q.NEW_PLAN,
                      'readings': {
                          'peer_first_restores_both': 'the effect is scheduling or plan '
                                                      'interpretation, not abandonment',
                          'peer_only_survives_previews': 'scheduling is an inadequate explanation, '
                                                         'even with the computed consequence table '
                                                         'in the prompt',
                          'tracks_action_names': 'action representation, not the plan'},
                      'note': 'the consequence table has been computed by this project since the '
                              'opportunity_cost v2 arm and has never appeared in a recorded '
                              'extension prompt; peer_first_previews is the first time it does'},
        'reporting': 'every outcome is reported, including refusal, referral, joint completion, the '
                     'peer-first plan and invalid responses; success rates never stand alone',
        'within_arm_replays': 'sixteen focal cells appear in both factorial and wording, and eight '
                              'slack cells in both factorial and plan_repr. The repeated ids are '
                              'byte-identical prompts, so a disagreement between phases is backend '
                              'non-determinism and not an effect; analysis.replays reports it. Each '
                              'table is computed over its own block, never over the pooled corpus, '
                              'so the repeats do not double-weight the focal cells',
        'not_claimed': ['no boundary-crossing claim: every case here is authorized and no '
                        'out-of-scope request is present',
                        'a token margin is not evidence of robustness to paraphrase; the wording '
                        'block is what addresses that',
                        'no prevention claim follows from this arm; intervention comes after the '
                        'explanation'],
        'generation': {'temperature': 0, 'seed': SEED, 'cache_prompt': False, 'mode': 'none',
                       'decision_budget': BUDGETS['decision'], 'n_probs': BUDGETS['n_probs']},
        'run_order': ['controls', 'factorial', 'plan_repr', 'length_control', 'wording',
                      'full_task_set', 'order_reversed'],
        'status': 'frozen, not run'})


def verify_freeze():
    f = json.loads((E / 'freeze.json').read_text())
    for path, h in f['hashes'].items():
        assert w.sha(R / path) == h, f'frozen file changed: {path}'
    return f


def run(model):
    import peer_authority as pa
    f = verify_freeze()
    assert model in f['models'], model
    spec = pa.model_spec(model)
    g = R / 'results/determinism' / ('gate_%s_%s.json' % (model, GATE_NAME))
    if not g.exists() or json.loads(g.read_text()).get('verdict') != 'pass':
        print('DETERMINISM GATE STOP', 'results/determinism/gate_%s_%s.json' % (model, GATE_NAME),
              flush=True)
        return
    served = ((json.loads(g.read_text()).get('server_props') or {}).get('model_path') or '')
    if not served.endswith(pathlib.Path(spec['gguf_path']).name):
        print('DETERMINISM GATE STOP', 'gate ran on a different model file: ' + served, flush=True)
        return
    cases = json.loads((E / 'cases.json').read_text())
    out = D / model
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'rollouts.jsonl'
    old = [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []
    done = {(r['case']['id'], r['phase']) for r in old}
    for phase in f['run_order']:
        if phase != 'controls':
            ctl = [r for r in old if r['phase'] == 'controls']
            verdict = gate(ctl)
            verdict['required_controls'] = f['counts']['controls']
            verdict['complete'] = len(ctl) == verdict['required_controls']
            verdict['eligible'] = bool(verdict['eligible'] and verdict['complete'])
            w.dump(out / 'gate.json', verdict)
            if not verdict['eligible']:
                print('CONTROL GATE STOP', json.dumps(verdict['tiers']['emit']), flush=True)
                return
        for c in cases[phase]:
            if (c['id'], phase) in done:
                continue
            r = execute(c, model, phase)
            with path.open('a') as h:
                h.write(json.dumps(r) + '\n')
                h.flush()
                os.fsync(h.fileno())
            old.append(r)
            done.add((c['id'], phase))
            for name, value in r['result']['state']['outputs'].items():
                w.dump(out / 'artifacts' / phase / c['id'] / name, value)
            print(phase, c['id'], r['decision'], r['outcome'].get('capability_ok'), flush=True)
    rows = [r['outcome'] for r in old if r['phase'] != 'controls' and not r.get('probe')]
    labels = gate([r for r in old if r['phase'] == 'controls'])['labels']
    w.dump(out / 'analysis.json', analyze(rows, labels))
    w.dump(out / 'complete.json', {'completed': True, 'rollouts': len(old),
                                   'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                   'rollouts_sha256': w.sha(path)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'freeze':
        freeze()
    elif cmd == 'cases':
        print(json.dumps({k: len(v) for k, v in build_cases().items()}, indent=2))
    elif cmd == 'run':
        run(sys.argv[2])
    else:
        raise SystemExit('usage: peer_message_factorial.py freeze | cases | run MODEL')
