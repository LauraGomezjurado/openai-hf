"""Build local review packets without exposing provisional assistant labels.

Historical text is inert evidence. No URLs in records are fetched or executed.
"""
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/review'


def rows(name):
    with (ROOT / 'results/cpu' / name).open() as f:
        return list(csv.DictReader(f))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with gzip.open(ROOT / 'data/raw/wiki/revisions.jsonl.gz', 'rt') as f:
        revisions = {r['rev_id']: r for r in map(json.loads, f)}
    packets = []
    for r in rows('hf_annotation_ledger.csv'):
        packets.append(dict(unit_id=r['ledger_id'], incident='HF',
                            source_url=r['source_url'], selector=r['source_selector'],
                            time=r['reconstructed_utc'], time_grade='reconstructed; uncertainty uncalibrated for this event',
                            source_type=r['source_type'], text=r['source_text'],
                            context_status='selected publication excerpt; underlying transcript unavailable'))
    for r in rows('wiki_annotation_sample_50.csv'):
        original = revisions[r['rev_id']]
        base = revisions.get(original['diff_base'])
        packets.append(dict(unit_id=r['rev_id'], incident='wiki comparison',
                            source_url=r['source_url'], time=r['time'], time_grade=r['time_grade'],
                            uncertainty_seconds=original['uncertainty_seconds'],
                            source_type='archived revision', text=r['addition'],
                            before=base['body'] if base else None, after=original['body'],
                            context_status=original['diff_base_reason']))
    # Deterministic order unrelated to proposed labels. Context stays attached.
    packets.sort(key=lambda r: hashlib.sha256(r['unit_id'].encode()).hexdigest())
    labels = ['evaluator_belief', 'peer_request', 'claimed_adoption', 'claimed_corroboration',
              'correction_dispute', 'boundary_recognition', 'action_evidence', 'outcome_evidence']
    fields = ['unit_id', 'incident'] + labels + ['evidence_span', 'alternative_explanation',
              'context_sufficient', 'episode_group', 'reviewer_id', 'reviewed_at', 'notes']
    for reviewer in ['A', 'B']:
        target = OUT / f'reviewer_{reviewer}.csv'
        # Never overwrite human work when regenerating context.
        if not target.exists():
            with target.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
                w.writerows({k: r[k] for k in ['unit_id', 'incident']} for r in packets)
    (OUT / 'context.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in packets))
    pairs = []
    for i, r in enumerate(rows('wiki_uptake_review.csv')):
        pair = dict(pair_id=f'W-L{i:02}', incident='wiki comparison',
                    selection='purposive linked candidates; not validated uptake')
        for side in ['earlier', 'later']:
            original = revisions[r[side+'_rev_id']]
            pair[side] = {k: original[k] for k in ['rev_id', 'page_id', 'time', 'time_grade', 'body', 'diff_base']}
            base = revisions.get(original['diff_base'])
            pair[side]['before'] = base['body'] if base else None
        pairs.append(pair)
    (OUT / 'linked_context.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in pairs))
    for reviewer in ['A', 'B']:
        target = OUT / f'linked_reviewer_{reviewer}.csv'
        if not target.exists():
            with target.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['pair_id', 'same_proposition', 'claimed_uptake',
                    'chronology_supported', 'distinct_actor_supported', 'execution_supported',
                    'earlier_evidence_span', 'later_evidence_span', 'alternative_explanation',
                    'episode_group', 'reviewer_id', 'notes']); w.writeheader()
                w.writerows({'pair_id': r['pair_id']} for r in pairs)
    assert len(packets) == 62 and len({r['unit_id'] for r in packets}) == 62
    assert all('working_interpretation' not in r and 'lexical_candidates' not in r for r in packets)
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*') if p.suffix in ['.csv', '.jsonl']}
    (OUT / 'packet_manifest.json').write_text(json.dumps(dict(units=62, hf=12, wiki=50,
        linked_pairs=len(pairs), independent_completed_labels='not inferred; inspect reviewer sheets', sampling='development only; selected HF excerpts and stratified wiki pages',
        sha256=hashes), indent=2)+'\n')
    print('Prepared 62 context packets and two reviewer sheets; existing review sheets preserved.')


if __name__ == '__main__':
    main()
