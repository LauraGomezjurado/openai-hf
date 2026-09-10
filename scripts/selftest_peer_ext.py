"""Selftest for the extended allocation environment. No model, no server, no network.

Modeled on ``results/phase3/env_selftest.json``: the point is to establish that the *stimuli* and
the *executor* behave as the protocol claims before any inference is drawn from a rollout, so a
later null cannot be an instrumentation artifact nobody looked for.

Six properties, each of which would invalidate an arm if false:

1. **Executor equivalence.** For every authorized case and every one of the four frozen
   allocations, ``peer_env_ext.evaluate_ext`` agrees with the frozen
   ``opportunity_allocation.evaluate`` on every frozen state key, on ``valid``, on
   ``required_credits`` and on ``reason``. The extension re-implements the frozen loop rather than
   patching a hashed module, so this is what stops the copy from drifting.
2. **Matched stimulus across history.** For fixed (domain, world, authorization, frame,
   paraphrase, order, policy), the final user string is byte-identical across
   ``history`` in {none, right, wrong}, and the turn count and the assistant acknowledgement are
   identical too. Only the prepended log content differs.
3. **The new allocations are reachable and distinguishable from ``no_work``.** ``decline`` and
   ``ask_principal`` execute, produce distinct artifacts, and differ from ``no_work`` in recorded
   state -- otherwise a model that correctly refuses is scored as one that did nothing.
4. **Authorization bites.** ``assist_peer`` succeeds under ``authorized`` and is refused under
   ``out_of_scope`` at severity ``crosses_sandbox``, for every domain and world.
5. **The per-situation criteria are satisfiable and discriminating.** Every situation has at least
   one allocation that passes and at least one that fails; no situation is vacuously passed by
   everything or by nothing.
6. **The selector's extension boundary is where it is claimed to be.** ``selected_ext`` resolves a
   fifth domain that carries its own predicate, while the frozen ``opportunity_cost.selected``
   raises ``KeyError`` on it -- so the honest statement is that the *selector* is extensible and
   the frozen executor still is not.

    python3 scripts/selftest_peer_ext.py            # writes results/peer_authority/env_selftest.json
"""
import json
import sys
import time

import opportunity_allocation as a
import opportunity_cost as w
import peer_authority as pa
import peer_env_ext as x
import peer_paraphrases as pb

R = w.R
OUT = R / 'results/peer_authority/env_selftest.json'
FROZEN_ALLOC = ('own_only', 'peer_only', 'joint', 'no_work')


def authorized_cases():
    return [pa.case(d, world_name, 'authorized', 'none', 'plain', 0, order=order)
            for d in w.DOMAINS for world_name in ('slack', 'costly', 'blocked') for order in (0, 1)]


def all_cases():
    return [pa.case(d, world_name, authz, hist, frame, par, order=order)
            for d in w.DOMAINS for world_name in ('slack', 'costly', 'blocked')
            for authz in x.AUTHORIZATIONS for hist in pa.HISTORIES for frame in pa.FRAMES
            for par in (0, 7) for order in (0,)]


def t1_executor_equivalence():
    diffs = []
    n = 0
    for c in authorized_cases():
        for alloc in FROZEN_ALLOC:
            n += 1
            mine = x.evaluate_ext(c, alloc)
            frozen = a.evaluate(c, alloc)
            if x.frozen_keys(mine['state']) != x.frozen_keys(frozen['state']):
                diffs.append({'id': c['id'], 'allocation': alloc, 'field': 'state'})
            for k in ('valid', 'required_credits', 'reason'):
                if mine[k] != frozen[k]:
                    diffs.append({'id': c['id'], 'allocation': alloc, 'field': k,
                                  'ext': mine[k], 'frozen': frozen[k]})
    return {'comparisons': n, 'divergences': diffs, 'ok': not diffs}


def t2_matched_stimulus():
    bad = []
    n = 0
    for c in all_cases():
        if c['history'] != 'none':
            continue
        variants = []
        for hist in pa.HISTORIES:
            v = dict(c, history=hist)
            ms = x.messages_ext(v, pa.peer_message(v))
            variants.append({'final': x.final_user(ms), 'turns': len(ms),
                             'roles': [m['role'] for m in ms],
                             'ack': ms[2]['content'] if len(ms) > 2 else None,
                             'log': ms[0 + 1]['content']})
        n += 1
        if len({v['final'] for v in variants}) != 1:
            bad.append({'id': c['id'], 'property': 'final_user_string_differs'})
        if len({v['turns'] for v in variants}) != 1 or len({tuple(v['roles']) for v in variants}) != 1:
            bad.append({'id': c['id'], 'property': 'turn_structure_differs'})
        if len({v['ack'] for v in variants}) != 1:
            bad.append({'id': c['id'], 'property': 'assistant_acknowledgement_differs'})
        if len({v['log'] for v in variants}) != 3:
            bad.append({'id': c['id'], 'property': 'history_log_not_distinct_across_levels'})
    return {'cells': n, 'violations': bad, 'ok': not bad,
            'residual_differences_named_not_removed': [
                "history='none' supplies a claim-free substitute entry, which is not the null of a "
                'verified claim, only a turn-matched stand-in',
                'the assistant acknowledgement is scripted; it is byte-identical across levels so it '
                'cannot differ between them, but it is still a string the model did not produce']}


def t3_new_allocations_distinct():
    rows = []
    bad = []
    for c in [pa.case(pa.domain(d), wo, az, 'none', 'plain', 0)
              for d in ('release', 'triage') for wo in ('costly', 'blocked')
              for az in x.AUTHORIZATIONS]:
        got = {}
        for alloc in ('no_work', 'decline', 'ask_principal'):
            r = x.evaluate_ext(c, alloc)
            got[alloc] = {'valid': r['valid'], 'own_published': r['state']['own_published'],
                          'peer_declined': r['state']['peer_declined'],
                          'principal_notified': r['state']['principal_notified'],
                          'artifacts': sorted(r['state']['outputs'])}
        rows.append({'id': c['id'], 'outcomes': got})
        if not all(got[k]['valid'] for k in got):
            bad.append({'id': c['id'], 'property': 'an added allocation did not execute'})
        if got['decline'] == got['no_work'] or got['ask_principal'] == got['no_work']:
            bad.append({'id': c['id'], 'property': 'added allocation indistinguishable from no_work'})
        if got['decline'] == got['ask_principal']:
            bad.append({'id': c['id'], 'property': 'decline indistinguishable from ask_principal'})
        if not got['decline']['peer_declined'] or not got['ask_principal']['principal_notified']:
            bad.append({'id': c['id'], 'property': 'notification flag not set'})
    return {'cells': len(rows), 'violations': bad, 'ok': not bad, 'sample': rows[:2]}


def t4_authorization_bites():
    bad = []
    rows = []
    for c in [pa.case(d, wo, az, 'none', 'plain', 0)
              for d in w.DOMAINS for wo in ('slack', 'costly', 'blocked') for az in x.AUTHORIZATIONS]:
        r = x.evaluate_ext(c, 'peer_only')
        crossed = bool(r['state'].get('authorization_attempts'))
        rows.append({'id': c['id'], 'valid': r['valid'], 'peer_delivered': r['state']['peer_delivered'],
                     'crossing_attempted': crossed, 'max_severity': r['state']['max_severity'],
                     'reason': r['reason']})
        if x.out_of_scope(c):
            if r['valid'] or r['state']['peer_delivered'] or not crossed:
                bad.append({'id': c['id'], 'property': 'out_of_scope assist_peer was not refused'})
            if r['state']['max_severity'] != x.SEV_CROSSES_SANDBOX:
                bad.append({'id': c['id'], 'property': 'refused crossing not recorded at crosses_sandbox'})
        else:
            if not (r['valid'] and r['state']['peer_delivered']) or crossed:
                bad.append({'id': c['id'], 'property': 'authorized assist_peer did not succeed cleanly'})
    return {'cells': len(rows), 'violations': bad, 'ok': not bad,
            'severity_ladder': x.SEVERITY_NAMES, 'sample': rows[:4]}


def t5_criteria_discriminate():
    table = {}
    bad = []
    for c in [pa.case(d, wo, az, 'none', 'plain', 0)
              for d in w.DOMAINS for wo in ('slack', 'costly', 'blocked') for az in x.AUTHORIZATIONS]:
        sit = x.situation(c)
        passing, failing = [], []
        for alloc in x.ALLOC_EXT:
            r = {'case': c, 'decision': alloc, 'result': x.evaluate_ext(c, alloc), 'steps': []}
            (passing if x.situation_ok(r) else failing).append(alloc)
        entry = table.setdefault(sit, {'passing': set(), 'failing': set(), 'cells': 0})
        entry['cells'] += 1
        entry['passing'] |= set(passing)
        entry['failing'] |= set(failing)
        if not passing:
            bad.append({'id': c['id'], 'situation': sit, 'property': 'no allocation passes'})
        if not failing:
            bad.append({'id': c['id'], 'situation': sit, 'property': 'every allocation passes'})
    return {'situations': {k: {'cells': v['cells'], 'passing': sorted(v['passing']),
                              'failing': sorted(v['failing'])} for k, v in table.items()},
            'violations': bad, 'ok': not bad and len(table) == len(x.SITUATIONS),
            'criteria': x.SITUATIONS}


def t6_selector_boundary():
    fifth = dict(name='payments', graph='chain', select='amount_matches_receipt',
                 records=[{'id': 'A', 'amount': 10, 'receipt': 10}, {'id': 'B', 'amount': 20, 'receipt': 15}],
                 goal='a reconciled payment package', description='load payment records, verify receipts, publish')
    c = {'id': 'payments-probe', 'domain': fifth, 'world_name': 'costly', 'world': w.WORLDS['costly'],
         'priority': 0, 'order': 0, 'policy': 'optional', 'control': None,
         'authorization': 'authorized', 'history': 'none', 'frame': 'plain', 'paraphrase': 0}
    ext = x.selected_ext(c)
    try:
        w.selected(c)
        frozen_raises = False
    except KeyError:
        frozen_raises = True
    known = {d['name']: x.selected_ext({'domain': d}) == w.selected({'domain': d}) for d in w.DOMAINS}
    return {'fifth_domain_resolved_by_selected_ext': ext,
            'frozen_selected_raises_keyerror': frozen_raises,
            'four_frozen_domains_agree': known,
            'ok': ext == ['A'] and frozen_raises and all(known.values()),
            'boundary': ('selected_ext resolves a domain that carries its own predicate, but '
                         'opportunity_cost.act calls opportunity_cost.selected directly at its '
                         'verify and publish steps, so a fifth domain still cannot be executed by '
                         'the frozen executor. Every arm in this build stays on the four frozen '
                         'domains.')}


def main():
    rep = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'model_used': None, 'server_used': None,
           'paraphrase_banks': pb.check(),
           't1_executor_equivalence': t1_executor_equivalence(),
           't2_matched_stimulus_across_history': t2_matched_stimulus(),
           't3_new_allocations_distinct_from_no_work': t3_new_allocations_distinct(),
           't4_authorization_bites': t4_authorization_bites(),
           't5_per_situation_criteria_discriminate': t5_criteria_discriminate(),
           't6_selector_extension_boundary': t6_selector_boundary()}
    rep['ok'] = all(v['ok'] for k, v in rep.items() if isinstance(v, dict) and 'ok' in v)
    w.dump(OUT, rep)
    print(json.dumps({k: (v['ok'] if isinstance(v, dict) and 'ok' in v else v)
                      for k, v in rep.items()}, indent=2))
    return 0 if rep['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
