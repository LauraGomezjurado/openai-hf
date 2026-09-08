"""Analysis of Competing Hypotheses (ACH) matrix over the project's evidence.

Model Forensics (arXiv 2606.26071) tabulates evidence against competing explanations
and its authors list the absence of formal evidence aggregation as a limitation. This
script supplies that aggregation for our evidence: every rating cell is an explicit,
sourced analyst judgment stored in ``experiments/ach/ratings_*.json``; nothing here is
inferred from the model outputs automatically.

ACH convention: hypotheses are ranked by *inconsistency*, not by how much evidence
supports them, because consistent evidence is usually compatible with several
accounts. Reported per hypothesis: inconsistency count (I + II), weighted inconsistency
(credibility-discounted), and net score. Reported per evidence row: diagnosticity (how
many distinct ratings it assigns). A leave-one-out pass records whether the ranking's
top hypothesis depends on any single row. When more than one rater file is present,
cell-level agreement and Cohen's kappa are reported.

Outputs: results/ach/ach_matrix.json and results/ach/ach_matrix.md.
"""
import glob
import json
import pathlib
from collections import Counter

R = pathlib.Path(__file__).resolve().parents[1]
E = R / 'experiments/ach'
OUT = R / 'results/ach'
LEVELS = ['CC', 'C', 'N', 'I', 'II']


def load(path):
    d = json.loads(pathlib.Path(path).read_text())
    for row in d['evidence']:
        assert set(row['ratings']) == set(d['hypotheses']), row['id']
        assert all(v in LEVELS for v in row['ratings'].values()), row['id']
    return d


def rank(d, rows):
    """Per-hypothesis tallies over the given rows. Ranking key: weighted inconsistency ascending, then net score descending."""
    scores, weights = d['scores'], d['credibility_weights']
    out = {}
    for h in d['hypotheses']:
        tally = Counter(row['ratings'][h] for row in rows)
        incons = tally['I'] + tally['II']
        w_incons = sum(weights[row['credibility']] * (2 if row['ratings'][h] == 'II' else 1) for row in rows if row['ratings'][h] in ('I', 'II'))
        net = sum(scores[row['ratings'][h]] for row in rows)
        w_net = sum(weights[row['credibility']] * scores[row['ratings'][h]] for row in rows)
        out[h] = {'tally': dict(tally), 'inconsistency': incons, 'weighted_inconsistency': round(w_incons, 3), 'net_score': net, 'weighted_net_score': round(w_net, 3), 'rows': len(rows)}
    order = sorted(out, key=lambda h: (out[h]['weighted_inconsistency'], -out[h]['weighted_net_score']))
    for i, h in enumerate(order, 1):
        out[h]['rank'] = i
    return out, order


def diagnosticity(row, scores):
    vals = [scores[v] for v in row['ratings'].values()]
    return {'distinct_levels': len(set(row['ratings'].values())), 'spread': max(vals) - min(vals)}


def leave_one_out(d, rows):
    _, base = rank(d, rows)
    changes = []
    for row in rows:
        _, order = rank(d, [r for r in rows if r['id'] != row['id']])
        if order[0] != base[0]:
            changes.append({'removed': row['id'], 'new_top': order[0]})
    return {'base_top': base[0], 'rows_whose_removal_changes_top': changes}


def kappa(a, b):
    """Cohen's kappa over aligned category lists."""
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in LEVELS) / (n * n)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(primary, others):
    out = []
    for o in others:
        idx = {r['id']: r for r in o['evidence']}
        a, b = [], []
        for row in primary['evidence']:
            if row['id'] in idx:
                for h in primary['hypotheses']:
                    a.append(row['ratings'][h])
                    b.append(idx[row['id']]['ratings'][h])
        out.append({'rater': o['rater'], 'cells': len(a), 'exact_agreement': round(sum(x == y for x, y in zip(a, b)) / len(a), 3) if a else None, 'cohen_kappa': kappa(a, b)})
    return out


def consensus(primary, others):
    """Copy of the primary ratings with every cell on which any rater disagrees set to N (non-diagnostic pending adjudication)."""
    if not others:
        return None
    d = json.loads(json.dumps(primary))
    idx = [{r['id']: r for r in o['evidence']} for o in others]
    changed = 0
    for row in d['evidence']:
        for h in d['hypotheses']:
            if any(row['id'] in i and i[row['id']]['ratings'][h] != row['ratings'][h] for i in idx):
                row['ratings'][h] = 'N'
                changed += 1
    d['rater'] = 'consensus(' + ', '.join([primary['rater']] + [o['rater'] for o in others]) + ')'
    return d, changed


def markdown(d, result):
    hs = list(d['hypotheses'])
    lines = ['# ACH matrix', '', f"Rater: {d['rater']}. Ratings are analyst judgments recorded in `experiments/ach/ratings_v1.json`; see the rationale fields there. Scale: CC/C/N/I/II.", '']
    lines.append('| Evidence | Scope | Credibility | ' + ' | '.join(hs) + ' | Diagnosticity |')
    lines.append('|---|---|---|' + '---|' * len(hs) + '---|')
    for row in d['evidence']:
        lines.append(f"| {row['id']} {row['study']} | {row['scope']} | {row['credibility']} | " + ' | '.join(row['ratings'][h] for h in hs) + f" | {result['diagnosticity'][row['id']]['distinct_levels']} |")
    for scope, block in result['rankings'].items():
        lines += ['', f'## Ranking: {scope}', '', '| Rank | Hypothesis | Inconsistent rows | Weighted inconsistency | Net score | Weighted net |', '|---|---|---|---|---|---|']
        for h in block['order']:
            t = block['table'][h]
            lines.append(f"| {t['rank']} | {h} {d['hypotheses'][h]['name']} | {t['inconsistency']} | {t['weighted_inconsistency']} | {t['net_score']} | {t['weighted_net_score']} |")
        loo = block['leave_one_out']
        lines.append('')
        lines.append(f"Leave-one-out: top hypothesis {loo['base_top']}; " + ('no single row changes it.' if not loo['rows_whose_removal_changes_top'] else 'changes when removing ' + ', '.join(f"{c['removed']} (-> {c['new_top']})" for c in loo['rows_whose_removal_changes_top']) + '.'))
    if result['agreement']:
        lines += ['', '## Inter-rater agreement', '']
        for a in result['agreement']:
            lines.append(f"- {a['rater']}: {a['cells']} cells, exact agreement {a['exact_agreement']}, Cohen's kappa {a['cohen_kappa']}")
        for name, o in result.get('other_raters', {}).items():
            lines.append(f"- {name} ranking alone: " + ', '.join(f"{h} ({o['weighted_inconsistency'][h]})" for h in o['order']))
        c = result.get('consensus')
        if c:
            lines += ['', f"## Consensus ({c['cells_set_to_N']} disagreed cells set to N)", '']
            for scope, block in c['rankings'].items():
                lines.append(f"- {scope}: " + ', '.join(f"{h} ({block['table'][h]['weighted_inconsistency']})" for h in block['order']) + f"; leave-one-out top {block['leave_one_out']['base_top']}, changes: {len(block['leave_one_out']['rows_whose_removal_changes_top'])}")
    else:
        lines += ['', 'No second rater file is present; agreement is not computed.']
    return '\n'.join(lines) + '\n'


def main():
    files = sorted(glob.glob(str(E / 'ratings_*.json')))
    primary = load(E / 'ratings_v1.json')
    others = [load(f) for f in files if not f.endswith('ratings_v1.json')]
    rows = primary['evidence']
    result = {'rater': primary['rater'], 'hypotheses': primary['hypotheses'], 'evidence_rows': len(rows), 'rankings': {}, 'diagnosticity': {r['id']: diagnosticity(r, primary['scores']) for r in rows}}
    for scope, subset in [('all_evidence', rows), ('experiments_only', [r for r in rows if r['scope'] == 'experiment']), ('historical_only', [r for r in rows if r['scope'] == 'historical'])]:
        table, order = rank(primary, subset)
        result['rankings'][scope] = {'table': table, 'order': order, 'leave_one_out': leave_one_out(primary, subset)}
    result['agreement'] = agreement(primary, others)
    cons = consensus(primary, others)
    if cons:
        cd, changed = cons
        result['consensus'] = {'cells_set_to_N': changed, 'rankings': {}}
        for scope, subset in [('all_evidence', cd['evidence']), ('experiments_only', [r for r in cd['evidence'] if r['scope'] == 'experiment'])]:
            table, order = rank(cd, subset)
            result['consensus']['rankings'][scope] = {'table': table, 'order': order, 'leave_one_out': leave_one_out(cd, subset)}
        for o in others:
            table, order = rank(o, o['evidence'])
            result.setdefault('other_raters', {})[o['rater']] = {'order': order, 'weighted_inconsistency': {h: table[h]['weighted_inconsistency'] for h in order}}
    result['reading'] = ('Ranking by fewest inconsistencies is the ACH convention; a low rank does not establish the hypothesis, and historical rows are '
                         'E0-E2 evidence about different agents. Experiment rows concern public Qwen checkpoints in constructed settings.')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'ach_matrix.json').write_text(json.dumps(result, indent=2) + '\n')
    (OUT / 'ach_matrix.md').write_text(markdown(primary, result))
    for scope, block in result['rankings'].items():
        print(scope, [(h, block['table'][h]['weighted_inconsistency'], block['table'][h]['weighted_net_score']) for h in block['order']])
        print('   leave-one-out:', block['leave_one_out'])


if __name__ == '__main__':
    main()
