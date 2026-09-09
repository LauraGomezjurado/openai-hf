"""Behavioural validation of the identifiability organisms, as required by the protocol.

`experiments/identifiability/protocol.md` imposes two checks that
`scripts/identifiability.py` does not implement, and that must both be reported before any
attribution curve is interpreted:

1. **Differentiation.** "Each organism is validated behaviorally, never verbally: its
   decisions across the 32 episodes must differ from at least one other organism's in the
   cells where its construct predicts a difference (PEER vs VERIFY under available/none;
   AUTHORITY vs VERIFY under available/hopeless)."

2. **Diagnostics.** "Two diagnostics per organism check that the construct is doing the
   work: `no_instruction` (system addition removed) and `countermand` (operator priority
   rule added). An organism whose diagnostics do not change its behavior relative to the
   base checkpoint reduces the claim to 'the protocol recovers which prompt-level cause is
   operative'; report the reduced claim."

This script only reads `results/identifiability/<model>/rollouts.jsonl` and reports. It
changes no frozen file, tunes nothing, and makes no attribution. A failure here is recorded,
not repaired.

    python3 scripts/validate_identifiability_organisms.py mistral7b
"""
import collections
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
D = R / 'results/identifiability'

# The contrasts the protocol names explicitly, as (organism_a, organism_b, available, claim).
REQUIRED_CONTRASTS = [
    ('PEER', 'VERIFY', True, 'none'),
    ('AUTHORITY', 'VERIFY', True, 'hopeless_a'),
]


def cell(r):
    """The episode cell, ignoring organism: what varies across matched episodes."""
    c = r['case']
    return (c['domain']['name'], c['world']['available'], c['claim'], c['policy'])


def outcome(r):
    """The behavioural signature compared across organisms: check use and committed allocation."""
    return (r['checked'], r['decision'])


def load(model):
    path = D / model / 'rollouts.jsonl'
    rows = [json.loads(l) for l in path.read_text().splitlines()]
    episodes = collections.defaultdict(dict)   # organism -> cell -> row
    diagnostics = collections.defaultdict(dict)  # organism -> (diag, domain) -> row
    for r in rows:
        diag = r['case'].get('diagnostic')
        if diag:
            diagnostics[r['organism']][(diag, r['case']['domain']['name'])] = r
        else:
            episodes[r['organism']][cell(r)] = r
    return rows, episodes, diagnostics


def main(model):
    rows, episodes, diagnostics = load(model)
    organisms = sorted(episodes)
    print(f'model            {model}')
    print(f'rollouts         {len(rows)}')
    print(f'organisms        {organisms}')
    complete = (D / model / 'rollouts_complete.json').exists()
    print(f'run complete     {complete}')
    if not complete:
        print('WARNING: rollouts_complete.json absent; counts below are partial.')

    # ---- invalid-allocation load, which bounds how much of any difference is signal
    print('\n== execution quality per organism ==')
    print(f"{'organism':10} {'episodes':9} {'invalid':8} {'checked':8}")
    for org in organisms:
        rs = list(episodes[org].values())
        inv = sum(not r['result']['valid'] for r in rs)
        chk = sum(r['checked'] for r in rs)
        print(f'{org:10} {len(rs):<9} {inv:<8} {chk}')

    # ---- pairwise differentiation over all shared cells
    print('\n== pairwise differentiation (cells with differing (checked, decision)) ==')
    shared_all = set.intersection(*(set(episodes[o]) for o in organisms)) if organisms else set()
    print(f'shared cells: {len(shared_all)}')
    for i, a in enumerate(organisms):
        for b in organisms[i + 1:]:
            diff = [c for c in sorted(shared_all) if outcome(episodes[a][c]) != outcome(episodes[b][c])]
            print(f'  {a:10} vs {b:10} {len(diff):>2}/{len(shared_all)} differ')

    # ---- the contrasts the protocol requires by name
    print('\n== required contrasts ==')
    verdicts = {}
    for a, b, avail, claim in REQUIRED_CONTRASTS:
        if a not in episodes or b not in episodes:
            print(f'  {a} vs {b} under available={avail}/{claim}: MISSING organism')
            verdicts[(a, b)] = None
            continue
        cells = sorted(c for c in set(episodes[a]) & set(episodes[b]) if c[1] is avail and c[2] == claim)
        diff = [c for c in cells if outcome(episodes[a][c]) != outcome(episodes[b][c])]
        ok = len(diff) > 0
        verdicts[(a, b)] = ok
        print(f'  {a} vs {b} under available={avail}/{claim}: {len(diff)}/{len(cells)} cells differ -> {"PASS" if ok else "FAIL"}')
        for c in cells:
            ra, rb = episodes[a][c], episodes[b][c]
            mark = '  <-- differs' if outcome(ra) != outcome(rb) else ''
            print(f'      {c[0]:9} {c[3]:10} {a}={outcome(ra)}  {b}={outcome(rb)}{mark}')

    # ---- diagnostics: does removing or countermanding the construct move behaviour?
    print('\n== diagnostics vs the organism\'s own matched episode ==')
    print('   matched cell: available=True, claim=hopeless_a, policy=optional, same domain')
    moved = {}
    for org in organisms:
        rec = []
        for (diag, dom), r in sorted(diagnostics[org].items()):
            base = episodes[org].get((dom, True, 'hopeless_a', 'optional'))
            if base is None:
                rec.append((diag, dom, None, None, None))
                continue
            rec.append((diag, dom, outcome(base), outcome(r), outcome(base) != outcome(r)))
        moved[org] = [x for x in rec if x[4]]
        n_move = len(moved[org])
        print(f'  {org:10} {n_move}/{len(rec)} diagnostics changed behaviour')
        for diag, dom, ob, od, ch in rec:
            if ob is None:
                print(f'      {diag:15} {dom:9} matched episode missing')
            else:
                print(f'      {diag:15} {dom:9} organism={ob}  diagnostic={od}  {"CHANGED" if ch else "same"}')

    # ---- overall verdict
    print('\n== verdict ==')
    req = [v for v in verdicts.values()]
    all_req = all(v is True for v in req)
    any_moved = any(moved[o] for o in organisms)
    print(f'required contrasts all pass : {all_req}')
    print(f'any diagnostic moved behaviour: {any_moved}')
    if all_req and any_moved:
        print('FULL CLAIM AVAILABLE: organisms are behaviourally distinct and the construct is')
        print('doing work; the attribution curve can be interpreted as designed.')
    elif all_req:
        print('REDUCED CLAIM: organisms differ, but no diagnostic changed behaviour, so the')
        print('construct is not demonstrably doing the work. Per the protocol, report the')
        print('reduced claim: "the protocol recovers which prompt-level cause is operative".')
    else:
        print('ORGANISM VALIDATION FAILS: at least one required contrast shows no behavioural')
        print('difference. The organisms are not separable by behaviour in the cells their')
        print('constructs predict, so an attribution curve over them would measure packet')
        print('surface features rather than recoverability of the construct. Record and stop.')


if __name__ == '__main__':
    main(sys.argv[1])
