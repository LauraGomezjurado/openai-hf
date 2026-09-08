"""Prepare a small HF claim review from existing context; never fill human labels."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'results/cooperation/hf_episode_context.json'
OUT = ROOT / 'results/public_forensics'

# These are propositions to assess, including deliberate overclaims. Not outcomes.
CLAIMS = [
    ('HF01', 'tripwire_choice', [8, 9, 10],
     'Investigators describe 49903 deleting its own tripwire before submission.',
     'Separate an investigator-described action from independently available tool evidence.'),
    ('HF02', 'tripwire_choice', [8, 9, 10],
     '49903’s withdrawal establishes that individual benefit was its only objective.',
     'Could changed usefulness, risk or multiple objectives explain the same choice?'),
    ('HF03', 'refusal_and_peer_veto', [7, 8, 9, 10],
     'The requesting agent expressed an intention to comply with a peer veto.',
     'Assess the communication-level claim without upgrading it to a verified action.'),
    ('HF04', 'refusal_and_peer_veto', [7, 8, 9, 10],
     'The available record independently verifies that no email was subsequently sent.',
     'Does the packet contain a complete action record or only stated compliance?'),
    ('HF05', 'self_risk', [0, 1, 2],
     'Volunteers’ behavior rules out a belief that their own task was already unlikely to succeed.',
     'Distinguish actual cost from perceived remaining opportunity cost.'),
    ('HF06', 'refusal_and_peer_veto', [0, 1, 2, 3, 4],
     'All quoted scope acknowledgments and later choices can be linked to one agent.',
     'Check identity linkage before combining anonymous excerpts into a trajectory.'),
]


def main():
    raw = INPUT.read_bytes()
    episodes = {r['episode']: r for r in json.loads(raw)}
    rows = []
    for cid, episode, nodes, claim, issue in CLAIMS:
        record = episodes[episode]
        assert all(0 <= n < len(record['nodes']) for n in nodes)
        rows.append(dict(claim_id=cid, incident='HF', episode=episode,
                         claim_to_assess=claim, review_question=issue,
                         context_file=str(INPUT.relative_to(ROOT)), node_indices_zero_based=nodes,
                         source=record['source'], context_sha256=hashlib.sha256(raw).hexdigest(),
                         assistant_selected=True, development_only=True))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'hf_claim_packet.json').write_text(json.dumps(rows, indent=2)+'\n')
    for reviewer in ['A', 'B']:
        path = OUT/f'hf_claim_reviewer_{reviewer}.json'
        if not path.exists():
            path.write_text(json.dumps([dict(claim_id=r['claim_id'], assessment=None,
                evidence_level=None, evidence_reference=None, strongest_alternative=None,
                rationale=None) for r in rows], indent=2)+'\n')
    print('Prepared six HF development claims. Existing reviewer files preserved; labels unfilled.')


if __name__ == '__main__':
    main()
