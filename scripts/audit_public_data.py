"""Offline, dependency-free extraction. Reads published JS as JSON, never executes it."""
from pathlib import Path
import collections
import csv
import datetime as dt
import gzip
import hashlib
import json
import re
import statistics

ROOT = Path(__file__).resolve().parents[1]


def js_json(path, variable):
    text = path.read_text()
    match = re.search(r"window\." + re.escape(variable) + r"\s*=\s*", text)
    if not match:
        raise ValueError(f"Missing published variable {variable}")
    return json.JSONDecoder().raw_decode(text[match.end():])[0]


def write_csv(name, rows):
    if not rows:
        raise ValueError(f"Empty extraction: {name}")
    with (ROOT / 'data/processed' / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    for source in json.loads((ROOT / 'data/source_manifest.json').read_text()):
        assert hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() == source['sha256']
    data = js_json(ROOT / 'data/raw/metr/agent-data.js', 'AGENT_TIMELINE_DATA')
    traffic = js_json(ROOT / 'data/raw/metr/workstream-data.js', 'WORKSTREAM_TRAFFIC_DATA')
    base = dt.datetime.fromisoformat(data['windowStart'].replace('Z', '+00:00'))
    agents = data['agents']
    normalized = []
    for i, agent in enumerate(agents):
        row = {'snapshot_row_id': i, 'family': {'h': 'HPIM', 's': 'Sol'}[agent['family']]}
        for key in ['start', 'end', 'read', 'write', 'hfStart', 'hfEnd']:
            value = agent[key]
            row[key + '_seconds'] = value
            row[key + '_utc'] = (base + dt.timedelta(seconds=value)).isoformat() if value is not None else None
        row['observedStop'] = agent['observedStop']
        row['hf_before_read'] = agent['hfStart'] is not None and agent['hfStart'] < agent['read']
        row['read_to_hf_hours'] = (agent['hfStart'] - agent['read']) / 3600 if agent['hfStart'] is not None else None
        normalized.append(row)
    write_csv('metr_agents.csv', normalized)

    counts = []
    traffic_base = dt.datetime.fromisoformat(traffic['interval']['start_utc'].replace('Z', '+00:00'))
    for hour, leaf_idx, values in traffic['rows']:
        assert len(values) == len(traffic['categories'])
        assert all(isinstance(v, int) and v >= 0 for v in values)
        leaf = traffic['leaves'][leaf_idx]
        for category, value in zip(traffic['categories'], values):
            counts.append({'hour_utc': (traffic_base + dt.timedelta(hours=hour)).isoformat(),
                           'workstream': leaf['id'], 'family': leaf['family'],
                           'purpose': category['id'], 'count': value})
    write_csv('metr_workstream_counts.csv', counts)

    # These are *availability bounds*, not confidence intervals or causal estimates.
    cohorts = []
    for day in sorted({r['read_utc'][:10] for r in normalized}):
        members = [r for r in normalized if r['read_utc'].startswith(day)]
        prevalent = [r for r in members if r['hfStart_seconds'] is not None and r['hfStart_seconds'] <= r['read_seconds']]
        risk = [r for r in members if r not in prevalent]
        for horizon in [1, 6, 24]:
            event = [r for r in risk if r['hfStart_seconds'] is not None and r['hfStart_seconds'] <= r['read_seconds'] + horizon * 3600]
            unknown = [r for r in risk if r not in event and r['end_seconds'] < r['read_seconds'] + horizon * 3600]
            cohorts.append({'board_read_day_utc': day, 'horizon_hours': horizon,
                            'rows': len(members), 'onset_at_or_before_read': len(prevalent),
                            'risk_rows': len(risk), 'observed_onsets': len(event),
                            'followup_ends_before_horizon_without_onset': len(unknown),
                            'recorded_onset_lower_bound': len(event)/len(risk) if risk else None,
                            'recorded_onset_upper_bound': (len(event)+len(unknown))/len(risk) if risk else None})
    write_csv('metr_cohort_followup.csv', cohorts)

    # Audit the small curated replay without executing its JavaScript.
    replay = (ROOT / 'data/raw/hf/replay.html').read_text()
    block = re.search(r'const EVENTS = \[(.*?)\n\];', replay, re.S).group(1)
    replay_rows = re.findall(r'^\s*\{frac:', block, re.M)
    days = re.search(r'const DAYS = \[(.*?)\n\];', replay, re.S).group(1)
    phase = re.search(r'const PHASES = \[(.*?)\n\];', replay, re.S).group(1)

    expected = {'revisions': '60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793',
                'events': '588584295f1c4a7c3d90b04075ab151504f165ff069534d935cda08853ec28b1'}
    wiki = {}
    for name, digest in expected.items():
        raw = gzip.decompress((ROOT / f'data/raw/wiki/{name}.jsonl.gz').read_bytes())
        assert hashlib.sha256(raw).hexdigest() == digest
        rows = [json.loads(line) for line in raw.splitlines()]
        wiki[name] = {'rows': len(rows), 'sha256_expanded': digest}
        if name == 'revisions':
            wiki['revision_time_grades'] = dict(collections.Counter(r['time_grade'] for r in rows))
            wiki['pages_represented'] = len({r['page_id'] for r in rows})
            assert len({r['rev_id'] for r in rows}) == len(rows)
        else:
            wiki['event_types'] = dict(collections.Counter(r['event_type'] for r in rows))

    lags = [r['read_to_hf_hours'] for r in normalized if r['read_to_hf_hours'] is not None]
    audit = {'scope': 'Published figure data; reconstructed timing and AI-classified participation, not raw telemetry.',
             'agent_rows': len(agents), 'families': dict(collections.Counter(r['family'] for r in normalized)),
             'positioned_hf_onsets': len(lags), 'declared_verified_hf_participants': data.get('verifiedHfParticipants'),
             'hf_before_board_read': sum(v < 0 for v in lags),
             'missing_board_write': sum(a['write'] is None for a in agents),
             'observed_stop_flags': sum(a['observedStop'] for a in agents),
             'median_read_to_hf_hours_among_positioned_including_negative': statistics.median(lags),
             'workstream_sparse_rows': len(traffic['rows']), 'workstreams': len(traffic['leaves']),
             'communicative_purposes': len(traffic['categories']),
             'hf_replay_curated_entries': len(replay_rows),
             'hf_replay_daily_count_sum': sum(map(int, re.findall(r'actions:(\d+)', days))),
             'hf_replay_phase_count_sum': sum(map(int, re.findall(r'total:(\d+)', phase))),
             'wiki_separate_incident': wiki,
             'cautions': ['No untreated non-board cohort is present.',
                          '688 declared verified participants versus 684 positioned onsets needs clarification.',
                          'Negative read-to-onset intervals are preserved, not corrected or dropped silently.',
                          'A missing onset is not verified nonparticipation; ending follow-up is not verified disengagement.',
                          'Wiki event types overlap in the activity they describe; row total is not a count of agent actions.']}
    (ROOT / 'results/data_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
