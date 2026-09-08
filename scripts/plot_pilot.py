"""Scientific figure of a descriptive, censored-follow-up reproduction."""
import csv
import os
from pathlib import Path
import tempfile

os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='hf-mpl-'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / 'data/processed/metr_cohort_followup.csv').open()))
rows = [r for r in rows if r['horizon_hours'] == '1']
fig, ax = plt.subplots(figsize=(9, 5.4))
for i, row in enumerate(rows):
    lo, hi = float(row['recorded_onset_lower_bound']), float(row['recorded_onset_upper_bound'])
    ax.plot([i, i], [lo*100, hi*100], color='#244b65', lw=3)
    ax.scatter(i, lo*100, color='#244b65', s=40)
    ax.scatter(i, hi*100, facecolor='white', edgecolor='#244b65', s=40, zorder=3)
ax.set_xticks(range(len(rows)), [r['board_read_day_utc'][5:]+'\nn='+r['risk_rows'] for r in rows])
ax.set_ylim(-3, 103)
ax.set_ylabel('Recorded onset within 1 hour (%)')
ax.set_xlabel('First recorded board-read date (2026, UTC); n = eligible plotted rows')
ax.set_title('Hugging Face activity after first recorded board read', loc='left', fontsize=14)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', alpha=.2)
fig.text(.12,.025,'Source: METR published agent-timeline asset, retrieved September 6, 2026.\n'
         'Filled = observed onsets / eligible rows. Open = all early-ended follow-ups also become onsets.\n'
         'Ranges address early follow-up endings only; they are not confidence intervals. Reconstructed timestamps,\n'
         'AI-classified events, and selected board users. Descriptive reproduction, not a causal effect.',fontsize=8)
fig.subplots_adjust(bottom=.29)
fig.savefig(root/'results/recruitment-pilot.png', dpi=180)
fig.savefig(root/'results/recruitment-pilot.pdf')
