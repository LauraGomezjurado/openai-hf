"""Tests for the extended allocation environment and the four new peer arms.

No model, no server, no network. These enforce the contracts the four protocols claim, so that a
later null cannot be an instrumentation artifact nobody looked for. The stimulus-level properties
duplicate ``scripts/selftest_peer_ext.py`` deliberately: the selftest writes a dated record for the
run, and these fail the build.
"""
import ast
import inspect
import json
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import opportunity_allocation as a  # noqa: E402
import opportunity_cost as w  # noqa: E402
import peer_authority as pa  # noqa: E402
import peer_env_ext as x  # noqa: E402
import peer_information_ladder as pl  # noqa: E402
import peer_message_decomposition as pd  # noqa: E402
import peer_mitigations as pm  # noqa: E402
import peer_paraphrases as pb  # noqa: E402
import selftest_peer_ext as st  # noqa: E402

ARMS = {'peer_information_ladder': pl, 'peer_message_decomposition': pd,
        'peer_authority': pa, 'peer_mitigations': pm}


class ParaphraseBanks(unittest.TestCase):
    def test_contracts_hold(self):
        rep = pb.check()
        self.assertTrue(rep['ok'], json.dumps(rep, indent=2))

    def test_priority_carries_no_feasibility_proposition(self):
        """The correction that makes the A x G factorial orthogonal. If a feasibility claim
        reappears in the priority bank, the decomposition arm measures A against A-plus-something
        and no cell isolates priority."""
        rep = pb.check()
        self.assertEqual(rep['priority_carries_no_feasibility']['violations'], {})
        self.assertEqual(rep['filler_carries_no_feasibility']['violations'], {})

    def test_impersonal_bank_has_no_speaker(self):
        """A first-person pronoun in the scheduler notice puts the peer back in as the source and
        destroys the only contrast the self_instruction cells exist to draw."""
        rep = pb.check()['impersonal_bank']
        self.assertEqual(rep['first_person_violations'], {})
        self.assertEqual(rep['entries_without_a_peer_referent'], [])

    def test_dependency_clause_is_in_the_fixed_request(self):
        self.assertIn('It will complete my task', pb.REQUEST)
        self.assertIn('It will complete my task', pb.REQUEST_OUT_OF_SCOPE)
        for bank in ('ASSERTION', 'PRIORITY', 'PRIORITY_IMPERSONAL', 'FILLER'):
            for s in getattr(pb, bank):
                self.assertNotIn('complete my task', s, bank)


class Executor(unittest.TestCase):
    def test_equivalence_with_the_frozen_executor(self):
        rep = st.t1_executor_equivalence()
        self.assertTrue(rep['ok'], json.dumps(rep['divergences'][:5], indent=2))
        self.assertGreater(rep['comparisons'], 0)

    def test_new_allocations_distinct_from_no_work(self):
        rep = st.t3_new_allocations_distinct()
        self.assertTrue(rep['ok'], json.dumps(rep['violations'][:5], indent=2))

    def test_authorization_bites(self):
        rep = st.t4_authorization_bites()
        self.assertTrue(rep['ok'], json.dumps(rep['violations'][:5], indent=2))

    def test_criteria_discriminate(self):
        rep = st.t5_criteria_discriminate()
        self.assertTrue(rep['ok'], json.dumps(rep['violations'][:5], indent=2))
        self.assertEqual(set(rep['situations']), set(x.SITUATIONS))

    def test_selector_boundary_is_where_it_is_claimed(self):
        rep = st.t6_selector_boundary()
        self.assertTrue(rep['ok'], json.dumps(rep, indent=2))
        self.assertTrue(rep['frozen_selected_raises_keyerror'])

    def test_refused_crossing_survives_the_reset_on_error(self):
        """The frozen loop resets state on error. If the attempt did not survive that reset there
        would be no record that the agent tried to cross the boundary, which is the observation."""
        c = pa.case(pa.domain('release'), 'costly', 'out_of_scope', 'none', 'plain', 0)
        r = x.evaluate_ext(c, 'peer_only')
        self.assertFalse(r['valid'])
        self.assertEqual(r['state']['max_severity'], x.SEV_CROSSES_SANDBOX)
        self.assertTrue(r['state']['authorization_attempts'])
        self.assertFalse(r['state']['peer_delivered'])


class MatchedStimulus(unittest.TestCase):
    def test_history_does_not_touch_the_final_user_turn(self):
        rep = st.t2_matched_stimulus()
        self.assertTrue(rep['ok'], json.dumps(rep['violations'][:5], indent=2))

    def test_ladder_second_turns_are_byte_identical(self):
        """B1/B2/B3 must share the second user turn exactly, or the focal contrast is confounded
        with the wording of the follow-up instruction."""
        for dom in ('release', 'triage'):
            for world in ('costly', 'blocked'):
                seen = {pl.second_turn(pl.case(pl.domain(dom), world, rung, 'none', 0))
                        for rung in ('B1', 'B2', 'B3')}
                self.assertEqual(len(seen), 1, f'{dom}/{world}: {seen}')

    def test_ladder_first_user_turns_are_byte_identical_across_rungs(self):
        for dom in ('release', 'triage'):
            for world in ('costly', 'blocked'):
                seen = set()
                for rung in pl.RUNGS:
                    c = pl.case(pl.domain(dom), world, rung, 'none', 0)
                    seen.add(x.final_user(x.messages_ext(c, pl.peer_message(c)))
                             if pl.RUNGS[rung]['turns'] == 2 else None)
                seen.discard(None)
                self.assertEqual(len(seen), 1, f'{dom}/{world}')

    def test_ladder_status_payload_is_not_labelled_as_a_query_result(self):
        """Equalizing framing must not be bought with a false statement in the prompt: no query
        happens in B1 or B2, so the payload cannot be labelled a check_status result."""
        turn = pl.second_turn(pl.case(pl.domain('release'), 'costly', 'B2', 'none', 0))
        self.assertNotIn('check_status result', turn)
        self.assertIn('status service reading', turn)

    def test_decomposition_moves_only_the_priority_clause_to_the_scheduler(self):
        """The assertion is false in the costly world. Moving it into a system voice would make the
        harness the liar and confound system deception with a peer claim."""
        for al in pd.A_LEVELS:
            for gl in ('absent', 'present'):
                c = pd.case(pd.domain('release'), 'costly', al, gl, 0, variant='self_instruction')
                notice, peer = pd.notice_for(c), pd.message_for(c)
                i = c['paraphrase'] % pb.N
                self.assertNotIn(pb.ASSERTION[i], notice)
                self.assertNotIn(pb.PRIORITY[i], peer)
                self.assertNotIn(pb.PRIORITY_IMPERSONAL[i], peer)
                self.assertEqual(al == 'present', pb.ASSERTION[i] in peer)
                self.assertEqual(gl == 'present', pb.PRIORITY_IMPERSONAL[i] in notice)

    def test_every_self_instruction_case_carries_a_notice(self):
        """Otherwise the notice-presence difference is not absorbed by the variant's own baseline
        and the difference-in-differences the protocol predeclares is not available."""
        for c in pd.build_cases()['source']:
            self.assertIsNotNone(pd.notice_for(c), c['id'])


class Design(unittest.TestCase):
    def test_case_ids_are_unique_within_every_arm(self):
        for name, mod in ARMS.items():
            cases = mod.build_cases()
            for phase, cs in cases.items():
                ids = [c['id'] for c in cs]
                self.assertEqual(len(ids), len(set(ids)), f'{name}/{phase}')

    def test_every_arm_reports_the_full_task_set(self):
        """No arm may screen domains on baseline success: that selects the cases where
        deterioration is possible and changes the population the headline describes.

        Coverage must come from the *measurement* blocks. Counting the control block would pass an
        arm whose focal design ran two domains and whose only contact with the other two was a
        capability check -- which is the screen wearing a different hat.
        """
        for name, mod in ARMS.items():
            cases = mod.build_cases()
            covered = {c['domain']['name'] for phase, cs in cases.items() if phase != 'controls'
                       for c in cs}
            self.assertEqual(covered, {d['name'] for d in w.DOMAINS}, name)
            self.assertIn('full_task_set', cases, name)

    def test_floored_domain_is_retained_in_a_measurement_block(self):
        """``triage`` sits at a floor in the primary line and is kept to test recovery, so it has to
        appear somewhere a rate is computed, not only in the controls."""
        for name, mod in ARMS.items():
            cases = mod.build_cases()
            covered = {c['domain']['name'] for phase, cs in cases.items() if phase != 'controls'
                       for c in cs}
            self.assertIn('triage', covered, name)

    def test_every_arm_has_a_control_block_and_a_control_criterion(self):
        for name, mod in ARMS.items():
            self.assertTrue(mod.build_cases()['controls'], name)
            self.assertTrue(callable(mod.control_ok), name)

    def test_wording_blocks_use_the_full_paraphrase_bank(self):
        """Paraphrase is the replicate unit; a block that samples a few wordings cannot support a
        claim about a condition rather than about a sentence."""
        for name in ('peer_information_ladder', 'peer_message_decomposition', 'peer_authority',
                     'peer_mitigations'):
            cs = ARMS[name].build_cases()['wording']
            self.assertEqual({c['paraphrase'] for c in cs}, set(range(pb.N)), name)

    def test_paraphrase_is_crossed_with_the_focal_factor_not_nested(self):
        """Every level of the main factor must appear with every block wording, or the factor is
        confounded with wording."""
        for name, key in (('peer_authority', 'frame'), ('peer_mitigations', 'mitigation')):
            cs = ARMS[name].build_cases()['main']
            by_level = {}
            for c in cs:
                by_level.setdefault(c[key], set()).add(c['paraphrase'])
            self.assertEqual(len({frozenset(v) for v in by_level.values()}), 1, name)

    def test_all_four_situations_are_exercised_by_the_mitigation_arm(self):
        sits = {x.situation(c) for c in pm.build_cases()['main']}
        self.assertEqual(sits, set(x.SITUATIONS))

    def test_mitigation_sides_are_a_partition(self):
        self.assertEqual(set(pm.FOLLOWING_THE_PEER_IS_WRONG) | set(pm.FOLLOWING_THE_PEER_IS_RIGHT),
                         set(x.SITUATIONS))
        self.assertFalse(set(pm.FOLLOWING_THE_PEER_IS_WRONG) & set(pm.FOLLOWING_THE_PEER_IS_RIGHT))

    def test_helping_is_correct_in_two_situations(self):
        """The premise of the joint criterion. If this were not true a harm-only measure would be
        adequate and the arm would not need one."""
        self.assertEqual(len(pm.FOLLOWING_THE_PEER_IS_RIGHT), 2)
        for sit in pm.FOLLOWING_THE_PEER_IS_RIGHT:
            self.assertIn('peer', x.SITUATIONS[sit])


class JointCriterion(unittest.TestCase):
    """A suppressor must score as a failure. This is the arm's whole point, so it is tested on
    synthetic rows rather than left to be checked by eye after a run."""

    @staticmethod
    def rows(spec):
        out = []
        for mit, (harm_ok, help_ok) in spec.items():
            for sit in pm.FOLLOWING_THE_PEER_IS_WRONG:
                out += [{'mitigation': mit, 'situation': sit, 'situation_ok': harm_ok,
                         'placement': 'system', 'side': 'peer_wrong'} for _ in range(4)]
            for sit in pm.FOLLOWING_THE_PEER_IS_RIGHT:
                out += [{'mitigation': mit, 'situation': sit, 'situation_ok': help_ok,
                         'placement': 'system', 'side': 'peer_right'} for _ in range(4)]
        return out

    def test_suppressor_is_scored_as_a_failure(self):
        s = pm.score(self.rows({'none': (False, True), 'verify_first': (True, False)}))
        self.assertEqual(s['verify_first']['harm_side_gain_pp'], 100.0)
        self.assertEqual(s['verify_first']['over_suppression_pp'], 100.0)
        self.assertFalse(s['verify_first']['admissible'])
        self.assertFalse(s['verify_first']['succeeds'])

    def test_genuine_mitigation_succeeds(self):
        s = pm.score(self.rows({'none': (False, True), 'verify_first': (True, True)}))
        self.assertTrue(s['verify_first']['admissible'])
        self.assertTrue(s['verify_first']['succeeds'])

    def test_no_gain_is_not_success(self):
        s = pm.score(self.rows({'none': (True, True), 'verify_first': (True, True)}))
        self.assertEqual(s['verify_first']['harm_side_gain_pp'], 0.0)
        self.assertFalse(s['verify_first']['succeeds'])

    def test_rates_are_per_situation_not_pooled(self):
        """A pooled harm-side rate would be dominated by request_exceeds_authorization, which
        contributes three times as many main cells as only_own_fits."""
        counts = {}
        for c in pm.build_cases()['main']:
            counts[x.situation(c)] = counts.get(x.situation(c), 0) + 1
        self.assertGreater(counts['request_exceeds_authorization'], counts['only_own_fits'])
        s = pm.score(self.rows({'none': (False, True)}))
        self.assertEqual(set(s['none']['by_situation']), set(x.SITUATIONS))


class Provenance(unittest.TestCase):
    def test_no_arm_edits_a_module_hashed_by_an_existing_freeze(self):
        """``freeze.json`` hashes file bytes only, so editing a hashed module from a new caller
        passes ``verify_freeze`` while invalidating the frozen arm's provenance. Every existing
        freeze must still verify."""
        stale = []
        for f in sorted((ROOT / 'experiments').glob('*/freeze.json')):
            rec = json.loads(f.read_text())
            for path, h in (rec.get('hashes') or {}).items():
                p = ROOT / path
                if p.exists() and w.sha(p) != h:
                    stale.append(f'{f.parent.name}: {path}')
        self.assertEqual(stale, [])

    # ``cache_prompt=True`` re-evaluates split suffixes and flips greedy tokens at temperature zero;
    # the frozen ``peer_claims_v2.generate`` and ``opportunity_cost.execute`` both hardcode it. The
    # checks below are on call sites parsed from the AST, not on source strings: every arm records
    # ``'cache_prompt': False`` in its freeze, and ``peer_env_ext``'s docstrings name
    # ``cache_prompt=True`` as the thing being avoided, so a substring check would flag the
    # documentation and miss an actual call.
    FORBIDDEN_GENERATORS = {('p', 'generate'), ('v2', 'generate'), ('w', 'execute'),
                            ('w', 'rollout'), ('p', 'execute')}

    @staticmethod
    def calls(name):
        tree = ast.parse((ROOT / 'scripts' / f'{name}.py').read_text())
        return [n for n in ast.walk(tree) if isinstance(n, ast.Call)]

    def test_no_arm_enables_the_prompt_cache_at_a_call_site(self):
        for name in list(ARMS) + ['peer_env_ext']:
            for call in self.calls(name):
                for kw in call.keywords:
                    if kw.arg == 'cache_prompt':
                        self.assertEqual(getattr(kw.value, 'value', 'not-a-constant'), False,
                                         f'{name}: cache_prompt passed as True')

    def test_no_arm_records_a_cached_generation_in_its_freeze(self):
        """A freeze that claims ``cache_prompt: True`` would preregister the defect."""
        for name in list(ARMS) + ['peer_env_ext']:
            tree = ast.parse((ROOT / 'scripts' / f'{name}.py').read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Dict):
                    continue
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and k.value == 'cache_prompt':
                        self.assertIs(getattr(v, 'value', None), False, name)

    def test_no_arm_calls_a_frozen_cached_generator(self):
        for name in list(ARMS) + ['peer_env_ext']:
            for call in self.calls(name):
                f = call.func
                if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                    self.assertNotIn((f.value.id, f.attr), self.FORBIDDEN_GENERATORS,
                                     f'{name}: {f.value.id}.{f.attr}')

    def test_the_only_generation_primitive_is_uncached(self):
        """``peer_env_ext`` is the generation choke point, and every ``reasoning_capture.generate``
        call in this build passes mode ``'none'`` -- the only path in this repo that is both uncached
        and records ``n_probs``. ``peer_authority``'s manipulation-check probe is the one arm-level
        call, and it is also mode ``'none'``."""
        found = 0
        for name in list(ARMS) + ['peer_env_ext']:
            for call in self.calls(name):
                f = call.func
                if not (isinstance(f, ast.Attribute) and f.attr == 'generate'
                        and isinstance(f.value, ast.Name) and f.value.id == 'rc'):
                    continue
                found += 1
                modes = [a.value for a in call.args if isinstance(a, ast.Constant)]
                self.assertIn('none', modes, f'{name}: rc.generate not in mode none')
        self.assertEqual(found, 2)

    def test_protocols_exist_for_every_new_arm(self):
        for name in ARMS:
            self.assertTrue((ROOT / 'experiments' / name / 'protocol.md').exists(), name)

    def test_both_gates_precede_the_first_rollout_in_every_arm(self):
        """The gates are only gates if nothing generates before them. Asserted on the source order
        inside ``run()`` rather than by invoking it, because invoking it is the thing that would
        start inference."""
        for name, mod in ARMS.items():
            src = inspect.getsource(mod.run)
            det, ctl = src.find('DETERMINISM GATE STOP'), src.find('CONTROL GATE STOP')
            # peer_authority calls the shared executor directly; the others wrap it in execute().
            hits = [m.start() for m in re.finditer(
                r'\b(execute|execute_ext|manipulation_check)\(', src)]
            self.assertTrue(hits, f'{name}: run() generates nothing')
            gen = min(hits)
            self.assertNotEqual(det, -1, name)
            self.assertNotEqual(ctl, -1, name)
            self.assertLess(det, ctl, f'{name}: control gate checked before determinism gate')
            self.assertLess(ctl, gen, f'{name}: a rollout is generated before the control gate')
            # Each stop must return, not merely print.
            self.assertIn('return', src[det:ctl], name)

    def test_the_freeze_record_was_not_edited_after_freezing(self):
        """``status`` is not in the freeze's own ``hashes`` -- ``freeze.json`` hashes eleven *other*
        files, never itself -- so nothing in ``verify_freeze()`` would notice it being rewritten to
        match whatever happened later. It stays at the freeze-time value and this test pins it. The
        record of what actually ran lives in ``results/<arm>/<model>/``, not here.

        This replaces an earlier ``test_no_arm_has_been_run``, which was true only until the first
        rollout on 2026-09-09 and is now recorded in
        ``docs/peer_arm_control_gate_results.md``."""
        for name in ARMS:
            rec = json.loads((ROOT / 'experiments' / name / 'freeze.json').read_text())
            self.assertEqual(rec['status'], 'frozen, not run', name)

    def test_no_arm_ran_a_measurement_block_after_failing_its_control_gate(self):
        """The gate is only a gate if an ineligible verdict actually stopped the arm. Checked against
        the rollouts on disk, so it holds for what was run and not merely for what ``run()`` says."""
        for name in ARMS:
            for roll in sorted((ROOT / 'results' / name).glob('*/rollouts.jsonl')):
                gate = roll.parent / 'gate.json'
                self.assertTrue(gate.exists(),
                                f'{name}/{roll.parent.name}: rollouts with no gate verdict')
                phases = {json.loads(l)['phase'] for l in roll.read_text().splitlines()}
                if not json.loads(gate.read_text())['eligible']:
                    self.assertEqual(phases, {'controls'},
                                     f'{name}/{roll.parent.name}: ran {phases} on a failed gate')

    def test_frozen_modules_are_not_imported_for_mutation(self):
        """Sanity check on the wrapper discipline: the extension calls the frozen executor, it does
        not rebind its attributes."""
        src = (ROOT / 'scripts' / 'peer_env_ext.py').read_text()
        for bad in ('w.act =', 'w.initial =', 'a.evaluate =', 'p.status =', 'setattr(w', 'setattr(a'):
            self.assertNotIn(bad, src)


if __name__ == '__main__':
    unittest.main()
