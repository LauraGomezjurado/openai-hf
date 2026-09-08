"""Tests for the determinism audit, reasoning capture, ACH builder and the V3 design."""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import analyze_replay_determinism as ard  # noqa: E402
import build_ach_matrix as ach  # noqa: E402
import determinism_gate as dg  # noqa: E402
import peer_claims_v3 as v3  # noqa: E402
import reasoning_capture as rc  # noqa: E402
import analyze_peer_claims_v3 as an  # noqa: E402


class ReplayAudit(unittest.TestCase):
    def test_repository_records(self):
        s = ard.summarize(ard.peer_claims_v2() + ard.peer_claim_order() + ard.opportunity_v2() + ard.workflow_completion() + ard.escalation_continuations())
        self.assertEqual(s['total_pairs'], 76)
        self.assertEqual(s['cache_prompt_false']['decision_mismatches'], 0)
        self.assertEqual(s['cache_prompt_true']['decision_mismatches'], 2)
        self.assertTrue(all(m['first_prompt_identical'] and m['first_source_prompt_n'] != m['first_replay_prompt_n'] for m in s['mismatches']))

    def test_local_path_remap(self):
        self.assertEqual(ard.local('/Users/someone/Desktop/openai-hf/results/x.jsonl'), ard.R / 'results/x.jsonl')


class Gate(unittest.TestCase):
    def test_compare_semantics(self):
        ref = {'tokens': [1, 2], 'content': 'a', 'top_logprobs': [[('a', -0.1), ('b', -1.0)], [('c', -0.2), ('d', -2.0)]]}
        same = dict(ref)
        self.assertTrue(dg.compare(ref, same)['logprobs_identical'])
        shifted = dict(ref, top_logprobs=[[('a', -0.1), ('b', -1.01)], [('c', -0.2), ('d', -2.0)]])
        c = dg.compare(ref, shifted)
        self.assertFalse(c['logprobs_identical'])
        self.assertAlmostEqual(c['max_abs_logprob_diff_common'], 0.01)
        member = dict(ref, top_logprobs=[[('a', -0.1), ('z', -1.0)], [('c', -0.2), ('d', -2.0)]])
        self.assertTrue(dg.compare(ref, member)['topk_membership_changed'])

    def test_legal_values_and_margin(self):
        schema = {'type': 'object', 'properties': {'action': {'type': 'string', 'enum': ['own_only', 'peer_only']}}}
        self.assertEqual(dg.legal_values(schema), ['own_only', 'peer_only'])
        probs = [{'top_logprobs': [{'token': '"own', 'logprob': -0.5}, {'token': '"peer', 'logprob': -0.7}, {'token': 'zzz', 'logprob': -0.1}]}]
        self.assertAlmostEqual(dg.decision_margin(probs, ['own_only', 'peer_only']), 0.2)

    def test_selftest_result_file(self):
        p = ROOT / 'results/determinism/gate_selftest_tiny.json'
        if not p.exists():
            self.skipTest('self-test not run')
        d = json.loads(p.read_text())
        self.assertEqual(d['verdict'], 'pass')
        self.assertEqual(d['uncached_logprob_mismatches'], 0)
        self.assertGreater(d['cached_logprob_changes'], 0)


class Reasoning(unittest.TestCase):
    def test_instruction_only_in_scratchpad_mode(self):
        ms = [{'role': 'system', 'content': 'S'}, {'role': 'user', 'content': 'U'}]
        self.assertEqual(rc.add_instruction(ms, 'native_think'), ms)
        self.assertEqual(rc.add_instruction(ms, 'none'), ms)
        self.assertIn('<scratchpad>', rc.add_instruction(ms, 'scratchpad')[0]['content'])
        self.assertEqual(ms[0]['content'], 'S')

    def test_two_phase_prompts_and_flags(self):
        calls = []

        def post(endpoint, payload):
            calls.append(payload)
            if 'stop' in payload:
                return {'content': 'because', 'stop_type': 'word', 'stopping_word': '</think>'}
            return {'content': '{"action": "own_only"}', 'completion_probabilities': [{'top_logprobs': [{'token': '{', 'logprob': -0.1}]}, {'top_logprobs': [{'token': '"own', 'logprob': -0.3}, {'token': '"peer', 'logprob': -0.9}]}]}
        r = rc.generate(post, 'PROMPT', {'enum': ['own_only']}, 'native_think', 1)
        self.assertEqual(r['reasoning'], 'because')
        self.assertFalse(r['reasoning_truncated'])
        self.assertTrue(calls[0]['prompt'].endswith('<think>\n'))
        self.assertIn('because\n</think>', calls[1]['prompt'])
        self.assertTrue(all(c['cache_prompt'] is False for c in calls))
        self.assertEqual(r['decoded'], {'action': 'own_only'})
        self.assertAlmostEqual(rc.margin_for_value(r['decision_top_logprobs'], 'own_only', ['own_only', 'peer_only']), 0.6)


class ACH(unittest.TestCase):
    def setUp(self):
        self.d = ach.load(ROOT / 'experiments/ach/ratings_v1.json')

    def test_every_cell_rated(self):
        for row in self.d['evidence']:
            self.assertEqual(set(row['ratings']), set(self.d['hypotheses']))
            self.assertIn(row['credibility'], self.d['credibility_weights'])

    def test_ranking_orders_by_inconsistency(self):
        table, order = ach.rank(self.d, self.d['evidence'])
        w = [table[h]['weighted_inconsistency'] for h in order]
        self.assertEqual(w, sorted(w))
        self.assertEqual(order[-1], 'H1')

    def test_kappa(self):
        self.assertEqual(ach.kappa(['C', 'I', 'N'], ['C', 'I', 'N']), 1.0)
        self.assertLess(ach.kappa(['C', 'C', 'I', 'N'], ['I', 'N', 'C', 'C']), 0.5)


class V3Design(unittest.TestCase):
    def setUp(self):
        self.cases = v3.build_cases()

    def test_counts(self):
        c = self.cases
        self.assertEqual((len(c['controls']), len(c['core']), len(c['paraphrase']), len(c['secondary']), len(c['direct']), len(c['replay'])), (20, 96, 64, 24, 16, 8))
        self.assertEqual({k: len(v) for k, v in c['menu'].items()}, {k: 16 for k in v3.MENU})
        self.assertEqual(sum(x['stage'] == 'A' for x in c['core']), 32)
        self.assertEqual(len({x['id'] for k in ['controls', 'core', 'paraphrase', 'secondary', 'direct'] for x in c[k]}), 220)

    def test_hidden_state_invariance(self):
        """Before checking, available and blocked prompts must be identical unless the policy supplies status."""
        by = {(x['domain']['name'], x['claim'], x['policy'], x['order'], x['world']['available']): x for x in self.cases['core']}
        for (dom, claim, policy, order, avail), x in by.items():
            if not avail or policy == 'automatic':
                continue
            y = by[(dom, claim, policy, order, False)]
            for mode in ['scratchpad', 'native_think']:
                self.assertEqual(v3.messages(x, mode), v3.messages(y, mode))

    def test_peer_block_wordings(self):
        base = self.cases['core'][0]
        texts = {k: v3.peer_block(dict(base, claim=k)) for k in list(v3.CLAIMS) + list(v3.MENU)}
        self.assertNotIn('unavailable', texts['none'])
        self.assertIn('System notice', texts['nonpeer'])
        self.assertNotIn('unavailable', texts['nonpeer'].split('Peer message')[1])
        self.assertIn('Reminder', texts['salience'])
        self.assertEqual(len({texts['hopeless_a'], texts['hopeless_b'], texts['hopeless_c']}), 3)

    def test_direct_mode_matches_v2_wording(self):
        import peer_claims_v2 as v2
        x = [c for c in self.cases['direct'] if c['claim'] == 'hopeless_a' and c['order'] == 0 and c['domain']['name'] == 'release'][0]
        v2c = v2.case(x['domain'], True, 'hopeless', 'optional', 0)
        self.assertEqual(v3.messages(x, 'scratchpad'), v2.messages(v2c))

    def test_frozen_hashes(self):
        f = json.loads((ROOT / 'experiments/peer_claims_v3/freeze.json').read_text())
        for path, h in f['hashes'].items():
            self.assertEqual(v3.w.sha(ROOT / path), h, path)
        self.assertNotIn('selftest_tiny', f['models'])


class V3Analysis(unittest.TestCase):
    def test_sign_rules(self):
        self.assertTrue(an.rule_direction({'pairs': 8, 'increases': 6, 'decreases': 0, 'ties': 2}, 6, 'increase'))
        self.assertFalse(an.rule_direction({'pairs': 8, 'increases': 7, 'decreases': 1, 'ties': 0}, 6, 'increase'))
        self.assertIsNone(an.rule_direction({'pairs': 4, 'increases': 4, 'decreases': 0, 'ties': 0}, 6, 'increase'))

    def test_pairs(self):
        def rec(dom, order, claim, checked):
            c = v3.case(dict(name=dom, graph='chain', records=[], goal='', description=''), True, claim, 'optional', order)
            return {'case': c, 'checked': checked, 'decision': 'own_only', 'result': {'valid': True, 'state': {'own_published': True, 'peer_delivered': False}}, 'steps': [{}]}
        main = [rec('a', 0, 'none', True), rec('a', 0, 'hopeless_a', False), rec('a', 1, 'none', True), rec('a', 1, 'hopeless_a', True)]
        pr = an.pairs(main, 'costly', 'none', 'hopeless_a', 'optional', 'optional', 'reason', 'reason', 'checked')
        self.assertEqual((pr['pairs'], pr['increases'], pr['decreases'], pr['ties']), (2, 0, 1, 1))
        self.assertEqual(pr['sign_test_one_sided_p'], 0.5)


if __name__ == '__main__':
    unittest.main()
