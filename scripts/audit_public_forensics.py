"""Audit published evidence and plan precision; no model calls or inferred labels.

Inputs are the archived public Model Forensics v2 HTML and explicit published counts.
Intervals assume independent binomial trials within a condition. They do not account
for prompt selection, shared contexts, or unknown pairing and are not causal intervals.
"""
import hashlib
import json
import math
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/raw/papers/model_forensics_v2.html'
OUT = ROOT / 'results/public_forensics'
URL = 'https://arxiv.org/html/2606.26071v2'


def wilson(k, n, z=1.959963984540054):
    if not 0 <= k <= n or n <= 0:
        raise ValueError('Require 0 <= k <= n and n > 0')
    p = k / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [max(0., center-half), min(1., center+half)]


def main():
    raw = SOURCE.read_bytes()
    soup = BeautifulSoup(raw, 'html.parser')
    section = soup.find(id='A3.SS5').get_text(' ', strip=True)
    definitions = [
        ('secret_number_original_cheating', 672, 875, '672/875'),
        ('secret_number_already_passed_cheating', 69, 88, '69/88'),
        ('secret_number_first_person_legitimacy', 16, 20, '16 of 20'),
        ('secret_number_third_person_legitimacy', 0, 20, '0/20'),
    ]
    counts = []
    for name, k, n, anchor in definitions:
        assert anchor in section, f'Count provenance missing: {anchor}'
        counts.append(dict(condition=name, successes=k, trials=n, rate=k/n,
                           wilson_95=wilson(k, n), source=URL+'#A3.SS5',
                           source_anchor=anchor))
    traces = []
    for group, count in [(1, 5), (2, 5), (3, 5), (4, 5), (5, 1)]:
        for i in range(1, count+1):
            sid = f'A7.SS{group}.SSSx{i}' if group < 5 else 'A7.SS5'
            element = soup.find(id=sid)
            assert element is not None, sid
            text = element.get_text(' ', strip=True)
            traces.append(dict(section=sid, source=URL+'#'+sid,
                               characters=len(text),
                               text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                               evidence='selected published reasoning excerpt',
                               incident='paper task; not Hugging Face',
                               action_verified_by_this_audit=False))
    # Approximate two-arm normal power calculation, two-sided alpha .05, power .80.
    # Three confirmatory contrasts use conservative Bonferroni alpha .05/3.
    planning = []
    for delta in [.05, .10, .15]:
        p1, p2 = .30-delta/2, .30+delta/2
        for label, z in [('single_contrast', 1.959963984540054),
                         ('three_contrasts_bonferroni', 2.3939797998185104)]:
            n = math.ceil((z*math.sqrt(2*.30*.70) +
                           .8416212335729143*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2/delta**2)
            for effect in [1., 1.5, 2.]:
                planning.append(dict(risk_difference=delta, correction=label,
                                     assumed_design_effect=effect,
                                     approximate_trials_per_arm=math.ceil(n*effect)))
    report = dict(
        source=URL, source_sha256=hashlib.sha256(raw).hexdigest(),
        new_model_runs=0, independent_historical_labels=0,
        published_counts=counts, selected_trace_index=traces,
        descriptive_differences={
            'already_passed_minus_original_cheating': 69/88 - 672/875,
            'first_minus_third_person_legitimacy': 16/20 - 0/20},
        precision_planning=planning,
        limitations=[
            'Intervals are within-condition binomial summaries, not HF estimates.',
            'Shared-context dependence and pairing are not reconstructed.',
            'No significance or equivalence test is inferred from published point estimates.',
            'The selected 21 traces cannot estimate behavior prevalence.',
            'Design effects are sensitivity assumptions, not measured correlations.',
            'Repeated seeds on one prompt do not establish generalization across tasks.',
            'No authentic historical counterfactual is generated here.'])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'Indexed {len(traces)} selected paper traces; verified {len(counts)} published counts.')
    for row in counts:
        print(f"{row['condition']}: {row['rate']:.3%}; conditional Wilson interval {row['wilson_95']}")
    print('New model runs: 0. Output: results/public_forensics/audit.json')


if __name__ == '__main__':
    main()
