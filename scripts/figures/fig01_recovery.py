"""Figure 1: the recovery. Three standalone figures, each saved on its own.

  fig01a_timeline.png   the published chart, redrawn from the file that draws it
  fig01b_row745.png     one agent: its nine numbers, its bytes, its height in the chart
  fig01c_tables.png     the three tables we wrote out, and what the file leaves out

Each one is sized to drop into a document on its own. The prose lives in
results/figures/FIGURES.md, not inside the figures.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data  # noqa: E402
import style as S  # noqa: E402

S.apply()

W = 10.6
LEFT, RIGHT = 0.052, 0.982
DPI = 200

ROW = 745
T0 = pd.Timestamp("2026-07-07T18:00:00Z")
T1 = pd.Timestamp("2026-07-14T00:00:00Z")
B0 = pd.Timestamp("2026-07-10T22:20:00Z")
B1 = pd.Timestamp("2026-07-11T23:50:00Z")

# Split by hand: the JSON has no spaces, so textwrap cannot break it.
RAW_OBJECT = [
    '  {"family":"h","y":1908.246,"start":430022.091,"end":513930.0,"read":459372.244,',
    '   "write":459733.337,"hfStart":472195.315,"hfEnd":511249.189,"observedStop":true},',
]
ASSET_HEAD = (
    'window.AGENT_TIMELINE_DATA={"windowStart":"2026-07-06T00:00:00Z",'
    '"windowEnd":"2026-07-14T00:00:00Z","rowSpacing":2.041744,"agents":['
)
PROVENANCE = (
    "GET https://metr.org/assets/js/agent_timeline/data.js     191,538 bytes     "
    "sha256 b92cb6f4…f314ad     retrieved 2026-09-06"
)
DERIV_1 = '  "y" : 1908.246   =   381.021   +   745 × 2.041744   +   4 × 1.531256'
DERIV_2 = "                       row 0's y      index × rowSpacing     the 4 wide rulings above it"
THESIS = (
    "The agent's place in the list alone gives back the height the chart drew it at, to a "
    "thousandth of a pixel, which means the chart is a drawing of this table."
)
DECODE = (
    "The file states no units, so we read them from the drawing code stored beside it "
    "(agent_timeline/chart.js, sha256 af1df7d5…e8dfb6). Times are seconds counted from "
    "windowStart, family h means HPIM and s means Sol, and y is a height in pixels."
)

ABSENT = [
    "No message text or reasoning appears anywhere in the file. The report publishes 30 "
    "snippets and counts 112,062 classified messages.",
    "No task identifiers, rewards, token budgets or tool calls are recorded.",
    "No agent has a stable identity, because its number is only its place in the list.",
    "The rule the AI grader used to label an agent as taking part is not given.",
    "No timestamp carries an error estimate, and the source says only that the timing is "
    "approximate.",
    "Nothing explains why the agents are listed in the order they are.",
]

LEGEND_A = [
    (S.NEUTRAL, "before it first read the board"),
    (S.BOARD, "after it read the board"),
    (S.ATTACK, "while it was attacking Hugging Face"),
]


def num(t):
    return mdates.date2num(t)


def top_block(fig, H: float, tag: str, title: str, gap: float = 0.66) -> float:
    """Tag and title. The title states the finding; the explanation is the caption.

    Returns the content top, `gap` inches down from the top of the figure.
    """

    def iy(inches: float) -> float:
        return 1.0 - inches / H

    fig.text(LEFT, iy(0.13), tag, fontsize=8.0, color=S.INK_3, va="top",
             weight="demibold")
    fig.text(LEFT, iy(0.29), title, fontsize=12.6, weight="demibold", color=S.INK,
             va="top")
    return iy(gap)


def heading(fig, y, letter, title, x=LEFT):
    if letter:
        fig.text(x, y, letter, fontsize=10.0, weight="bold", color=S.INK, va="bottom")
        x = x + 0.020
    fig.text(x, y + 0.0012, title, fontsize=8.6, weight="demibold", color=S.INK,
             va="bottom")


# --------------------------------------------------------------------------
# fig 1a -- the published chart, redrawn from the file
# --------------------------------------------------------------------------


def build_timeline(dpi=DPI):
    H = 4.75
    fig = plt.figure(figsize=(W, H))
    ag = data.agents()
    row = ag[ag["snapshot_row_id"] == ROW].iloc[0]

    top = top_block(
        fig, H, "Figure 1a",
        "We recovered all 1,206 agent timelines behind the report's chart and redrew the chart from them.",
        gap=0.66,
    )

    card = [0.052, 0.032, 0.930, top - 0.032]
    fig.add_artist(
        Rectangle((card[0], card[1]), card[2], card[3], facecolor=S.SURFACE_RAISED,
                  edgecolor=S.RULE, linewidth=0.8, transform=fig.transFigure, zorder=0)
    )
    fig.text(
        card[0] + 0.012, top - 0.16 / H,
        "metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/    ·    "
        "the interactive agent timeline",
        fontsize=6.8, color=S.INK_3, family=S.MONO, va="top",
    )

    ay0 = card[1] + 0.30 / H
    ax = fig.add_axes([0.080, ay0, 0.829, top - 0.34 / H - ay0])
    ax.set_facecolor("none")
    ax.set_ylabel("each line is one of the 1,206 agents, in the order the file lists them",
                  fontsize=7.2, color=S.INK_2, labelpad=4)

    pre, on_board, attacking = [], [], []
    for r in ag.itertuples():
        y = r.snapshot_row_id
        s, e, rd = num(r.start_utc), num(r.end_utc), num(r.read_utc)
        pre.append([(s, y), (min(rd, e), y)])
        if pd.isna(r.hfStart_utc):
            on_board.append([(rd, y), (e, y)])
        else:
            hf0, hf1 = num(r.hfStart_utc), num(r.hfEnd_utc)
            on_board.append([(rd, y), (max(rd, hf0), y)])
            attacking.append([(hf0, y), (hf1, y)])
            if hf1 < e - 1e-9:
                on_board.append([(hf1, y), (e, y)])
    ax.add_collection(LineCollection(pre, colors=S.NEUTRAL, linewidths=0.3, alpha=0.22))
    ax.add_collection(LineCollection(on_board, colors=S.BOARD, linewidths=0.32, alpha=0.38))
    ax.add_collection(LineCollection(attacking, colors=S.ATTACK, linewidths=0.34, alpha=0.20))
    ax.set_xlim(num(T0), num(T1))
    ax.set_ylim(len(ag) + 6, -6)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %-d"))
    ax.tick_params(axis="x", labelsize=7.0, length=2, pad=1)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(S.RULE)

    # the record followed in figure 1b
    sel0, sel1 = num(row["start_utc"]), num(row["end_utc"])
    pad = (num(T1) - num(T0)) * 0.004
    ax.add_patch(
        Rectangle((sel0 - pad, ROW - 11), sel1 - sel0 + 2 * pad, 22, facecolor="none",
                  edgecolor=S.INK, linewidth=0.9, zorder=6)
    )
    ax.annotate(
        "agent 745", xy=(sel0 - pad, ROW + 11),
        xytext=(num(pd.Timestamp("2026-07-09T14:00:00Z")), 880),
        fontsize=7.6, color=S.INK, weight="demibold", va="center", ha="left",
        arrowprops=dict(arrowstyle="-", color=S.INK, lw=0.7, shrinkA=3, shrinkB=2),
        zorder=7,
    )
    ax.text(num(pd.Timestamp("2026-07-09T14:00:00Z")), 952,
            "the agent shown in Figure 1b", fontsize=7.0, color=S.INK_3, va="center",
            ha="left")

    # legend: three states, in the empty upper right
    for i, (c, lab) in enumerate(LEGEND_A):
        y = 0.972 - i * 0.052
        ax.plot([0.958, 0.995], [y, y], transform=ax.transAxes, color=c, lw=2.8,
                alpha=0.62, solid_capstyle="butt", clip_on=False, zorder=8)
        ax.text(0.948, y, lab, transform=ax.transAxes, fontsize=7.2, color=S.INK_2,
                ha="right", va="center", zorder=8,
                path_effects=S.halo(2.8, S.SURFACE_RAISED))

    # the two family blocks, bracketed in the card margin
    fam = ag["family"].to_numpy()
    brk = int(np.argmax(fam != fam[0]))
    span = len(ag) + 12

    def yfrac(r):
        return (len(ag) + 6 - r) / span

    for r0, r1, lab in [(0, brk - 1, f"{brk:,} HPIM"), (brk, len(ag) - 1,
                                                        f"{len(ag) - brk} Sol")]:
        y0b, y1b = yfrac(r0) - 0.004, yfrac(r1) + 0.004
        ax.plot([1.010, 1.010], [y0b, y1b], transform=ax.transAxes, color=S.INK_3,
                lw=0.8, clip_on=False, zorder=8)
        for yc in (y0b, y1b):  # end caps, so the two blocks read as two brackets
            ax.plot([1.010, 1.019], [yc, yc], transform=ax.transAxes, color=S.INK_3,
                    lw=0.8, clip_on=False, zorder=8)
        ax.text(1.026, (y0b + y1b) / 2, lab, transform=ax.transAxes, fontsize=6.8,
                color=S.INK_2, ha="left", va="center", clip_on=False, zorder=8)

    out = data.ensure_out() / "fig01a_timeline.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 1b -- one record: nine fields, and the bytes behind it
# --------------------------------------------------------------------------


def build_row(dpi=DPI):
    H = 5.40
    fig = plt.figure(figsize=(W, H))
    ag = data.agents()
    row = ag[ag["snapshot_row_id"] == ROW].iloc[0]

    def ih(inches):
        return inches / H

    top = top_block(
        fig, H, "Figure 1b",
        "The file gives each agent nine numbers and no message text at all.",
        gap=0.70,
    )

    # ---- a. the nine fields ----
    heading(fig, top, "a", "These nine numbers are everything the file says about agent 745.")
    CH = 0.0045  # width of one 7.2pt character, in figure fractions
    kx = RIGHT - (sum(0.017 + CH * len(l) for _, l in LEGEND_A) + 0.014 * 2)
    for colour, lab in LEGEND_A:
        fig.add_artist(plt.Line2D([kx, kx + 0.011], [top + 0.004, top + 0.004],
                                  color=colour, lw=2.6, solid_capstyle="butt",
                                  transform=fig.transFigure))
        fig.text(kx + 0.017, top + 0.004, lab, fontsize=7.2, color=S.INK_2,
                 va="center")
        kx += 0.017 + CH * len(lab) + 0.014
    bh = ih(1.40)
    rect = [0.185, top - ih(0.20) - bh, 0.797, bh]
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    S.strip_axes(ax)
    ax.set_xlim(num(B0), num(B1))
    ax.set_ylim(-1.0, 1.0)

    segs = [
        (row["start_utc"], row["read_utc"], S.NEUTRAL),
        (row["read_utc"], row["hfStart_utc"], S.BOARD),
        (row["hfStart_utc"], row["hfEnd_utc"], S.ATTACK),
        (row["hfEnd_utc"], row["end_utc"], S.BOARD),
    ]
    gap = (num(B1) - num(B0)) * 0.0016  # the 2 px surface gap between fills
    for a, b, c in segs:
        ax.add_patch(
            Rectangle((num(a) + gap / 2, -0.11), num(b) - num(a) - gap, 0.22,
                      facecolor=c, edgecolor="none", zorder=3)
        )
    ax.add_patch(
        Rectangle((num(row["start_utc"]) - gap, -0.15),
                  num(row["end_utc"]) - num(row["start_utc"]) + 2 * gap, 0.30,
                  facecolor="none", edgecolor=S.INK, linewidth=0.8, zorder=5)
    )

    marks = {
        "start": row["start_utc"], "read": row["read_utc"], "write": row["write_utc"],
        "hfStart": row["hfStart_utc"], "hfEnd": row["hfEnd_utc"], "end": row["end_utc"],
    }
    for t in marks.values():
        ax.plot([num(t)] * 2, [-0.19, 0.19], color=S.INK, lw=0.9, zorder=6)

    T1U, T2U = 0.28, 0.58
    above = [
        ("start", T1U, "left", "Jul 10,  23:27:02"),
        ("read", T2U, "center", "07:36:12    ·    07:42:13"),
        ("hfStart", T1U, "center", "Jul 11,  11:09:55"),
        ("hfEnd", T1U, "right", "22:00:49"),
        ("end", T2U, "right", "22:45:30"),
    ]
    below = [
        ("start", T1U, "left", '"start":430022.091'),
        ("read", T2U, "center", '"read":459372.244,"write":459733.337'),
        ("hfStart", T1U, "center", '"hfStart":472195.315'),
        ("hfEnd", T1U, "right", '"hfEnd":511249.189'),
        ("end", T2U, "right", '"end":513930.0'),
    ]

    def xof(name):
        if name == "read":
            return (num(marks["read"]) + num(marks["write"])) / 2
        return num(marks[name])

    for name, tier, ha, txt in above:
        for m in (["read", "write"] if name == "read" else [name]):
            ax.plot([num(marks[m])] * 2, [0.19, tier - 0.035], color=S.INK_3, lw=0.6,
                    zorder=4)
        ax.text(xof(name), tier, txt, fontsize=7.6, color=S.OURS, ha=ha, va="bottom",
                zorder=7, weight="demibold")
    for name, tier, ha, txt in below:
        for m in (["read", "write"] if name == "read" else [name]):
            ax.plot([num(marks[m])] * 2, [-0.19, -tier + 0.035], color=S.INK_3, lw=0.6,
                    zorder=4)
        ax.text(xof(name), -tier, txt, fontsize=7.4, color=S.INK_2, ha=ha, va="top",
                family=S.MONO, zorder=7)

    ax.text(num(B0), -0.90, "family h means HPIM. 1,068 rows are HPIM and 138 are Sol.",
            fontsize=7.2, color=S.INK_3, ha="left", va="center")
    ax.text(num(B1), -0.90, "observedStop is true here, and on 47 of the 1,206 rows.",
            fontsize=7.2, color=S.INK_3, ha="right", va="center")

    fig.text(LEFT, rect[1] + ((T2U + 0.10) + 1) / 2 * rect[3],
             "We compute these\ntimes, in UTC.", fontsize=7.4, color=S.OURS,
             weight="demibold", va="center", linespacing=1.5)
    fig.text(LEFT, rect[1] + (1 - (T2U + 0.10)) / 2 * rect[3],
             "The file stores these\nseconds, counted\nfrom windowStart.", fontsize=7.4,
             color=S.INK_2, weight="demibold", va="center", linespacing=1.5)

    # ---- b. the bytes, and the pixel row recomputed ----
    hy = rect[1] - ih(0.42)
    heading(fig, hy, "b",
            "Agent 745's height in the chart comes back exactly from its place in the list.")
    ch = ih(2.32)
    card = [0.052, hy - ih(0.16) - ch, 0.930, ch]
    fig.add_artist(
        Rectangle((card[0], card[1]), card[2], card[3], facecolor=S.SURFACE_SUNK,
                  edgecolor="none", transform=fig.transFigure, zorder=0)
    )
    ct = card[1] + card[3]
    cx = card[0] + 0.014
    fig.text(cx, ct - ih(0.175), PROVENANCE, fontsize=6.8, color=S.INK_3,
             family=S.MONO, va="top")
    fig.text(cx, ct - ih(0.42), ASSET_HEAD, fontsize=7.4, color=S.INK_2,
             family=S.MONO, va="top")
    fig.text(cx, ct - ih(0.60), "  … 745 objects …", fontsize=7.4, color=S.INK_3,
             family=S.MONO, va="top")
    fig.add_artist(
        Rectangle((cx - 0.007, ct - ih(1.18)), 0.848, ih(0.41),
                  facecolor=S.SURFACE_RAISED, edgecolor=S.INK, linewidth=0.8,
                  transform=fig.transFigure, zorder=1)
    )
    fig.text(cx, ct - ih(0.85), "\n".join(RAW_OBJECT), fontsize=7.4, color=S.INK,
             family=S.MONO, va="top", linespacing=1.55, zorder=2)
    fig.text(cx + 0.851, ct - ih(0.975), "agent 745", fontsize=7.2, color=S.INK,
             weight="demibold", va="center", ha="left", zorder=2)
    fig.text(cx, ct - ih(1.31), "  … 460 objects …", fontsize=7.4, color=S.INK_3,
             family=S.MONO, va="top")

    fig.add_artist(
        Rectangle((cx - 0.007, ct - ih(1.93)), 0.520, ih(0.44), facecolor=S.SURFACE,
                  edgecolor=S.OURS_T, linewidth=0.9, transform=fig.transFigure, zorder=1)
    )
    fig.text(cx, ct - ih(1.58), DERIV_1, fontsize=7.4, color=S.OURS, family=S.MONO,
             va="top", zorder=2)
    fig.text(cx, ct - ih(1.74), DERIV_2, fontsize=6.6, color=S.INK_3, family=S.MONO,
             va="top", zorder=2)
    fig.text(cx + 0.528, ct - ih(1.71), "\n".join(textwrap.wrap(THESIS, 46)),
             fontsize=7.8, color=S.INK, va="center", linespacing=1.55, weight="demibold")
    fig.text(cx, ct - ih(2.05), "\n".join(textwrap.wrap(DECODE, 150)), fontsize=7.2,
             color=S.INK_2, va="top", linespacing=1.55)

    out = data.ensure_out() / "fig01b_row745.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 1c -- the tables we wrote, and what the file lacks
# --------------------------------------------------------------------------


PRESENCE = LinearSegmentedColormap.from_list("presence", [S.SURFACE, S.OURS])


def _frame(ax):
    for s in ("left", "bottom", "top", "right"):
        ax.spines[s].set_visible(True)
        ax.spines[s].set_color(S.RULE)
        ax.spines[s].set_linewidth(0.6)


def glyph_records(fig, rect, label_right):
    """One column per record, in file order. Three fields whose presence is a result."""
    df = pd.read_csv(data.PROC / "metr_agents.csv")
    strips = [
        ("has an attack start time", df["hfStart_utc"].notna().to_numpy()),
        ("has a first board write", df["write_utc"].notna().to_numpy()),
        ("was seen to stop", df["observedStop"].to_numpy().astype(bool)),
    ]
    ax = fig.add_axes(rect)
    S.strip_axes(ax)
    ax.imshow(np.vstack([s[1] for s in strips]).astype(float), aspect="auto",
              cmap=PRESENCE, vmin=0, vmax=1, interpolation="antialiased")
    for y in (0.5, 1.5):
        ax.axhline(y, color=S.SURFACE, lw=1.1)
    brk = int(np.argmax(df["family"].to_numpy() != df["family"].iloc[0]))
    ax.axvline(brk - 0.5, color=S.INK, lw=0.8)
    ax.text(brk - 16, 0.44, f"{brk:,} HPIM", fontsize=6.4, color=S.INK, va="bottom",
            ha="right", path_effects=S.halo(2.2, S.SURFACE))
    ax.text(brk + 16, 0.44, f"{len(df) - brk} Sol", fontsize=6.4, color=S.INK,
            va="bottom", ha="left", path_effects=S.halo(2.2, S.SURFACE))
    _frame(ax)
    h = rect[3] / len(strips)
    for i, (name, v) in enumerate(strips):
        fig.text(label_right, rect[1] + rect[3] - (i + 0.5) * h,
                 f"{name}   {v.sum():,}", fontsize=6.8, color=S.INK_2, ha="right",
                 va="center")
    return len(df), df.shape[1]


def glyph_hours(fig, rect):
    """Which workstream has a record in which hour."""
    ax = fig.add_axes(rect)
    S.strip_axes(ax)
    w = data.workstreams()
    piv = w.pivot_table(index="workstream", columns="hour_utc", values="count",
                        aggfunc="size")
    order = piv.notna().idxmax(axis=1).sort_values().index
    m = piv.loc[order].notna().to_numpy().astype(float)
    ax.imshow(m, aspect="auto", cmap=PRESENCE, vmin=0, vmax=1, interpolation="nearest")
    _frame(ax)
    return m.shape, int(m.sum())


def glyph_annotations(fig, rect):
    """The 12 annotations at their own times, marked by provenance."""
    ax = fig.add_axes(rect)
    S.strip_axes(ax)
    ann = data.annotations().sort_values("time").reset_index(drop=True)
    span = num(T1) - num(T0)
    w = span * 0.016
    lanes: list[float] = []
    for _, a in ann.iterrows():
        x = num(a["time"])
        lane = next((i for i, last in enumerate(lanes) if x - last > w * 1.6), len(lanes))
        if lane == len(lanes):
            lanes.append(x)
        else:
            lanes[lane] = x
        kw = dict(facecolor=S.OURS_T, edgecolor=S.OURS, linewidth=0.7)
        if a["provenance"] == "paraphrase":
            kw = dict(facecolor="none", edgecolor=S.OURS, hatch=S.HATCH, linewidth=0.7)
        elif a["provenance"] == "event":
            kw = dict(facecolor="none", edgecolor=S.NEUTRAL, linewidth=0.9)
        ax.add_patch(Rectangle((x - w / 2, lane + 0.14), w, 0.72, **kw))
    ax.set_xlim(num(T0), num(T1))
    ax.set_ylim(max(len(lanes), 3) + 0.1, -0.1)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(S.RULE)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %-d"))
    ax.tick_params(axis="x", labelsize=6.4, length=1.5, pad=1.5, colors=S.INK_3)
    return ann["provenance"].value_counts(), ann["row_id"].nunique()


def build_tables(dpi=DPI):
    H = 5.34
    D_W = 0.556
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    top = top_block(
        fig, H, "Figure 1c",
        "We recovered 1,206 agent timelines and 12,404 message counts without one line of message text.",
        gap=0.70,
    )

    # ---- a. the three tables ----
    heading(fig, top, "a", "These are the three tables we wrote out, each drawn at its real shape.")
    LBL_W = 0.108
    sx, sw = LEFT + LBL_W, D_W - LBL_W

    def entry(t, h, name, shape, note, sample, tick_pad=0.0):
        fig.text(LEFT, t, name, fontsize=7.8, color=S.OURS, family=S.MONO,
                 weight="demibold", va="top")
        fig.text(LEFT + D_W, t, shape, fontsize=7.4, color=S.INK, va="top",
                 weight="demibold", ha="right")
        y = t - ih(0.25) - h - tick_pad
        fig.text(LEFT, y, "\n".join(textwrap.wrap(note, 118)), fontsize=7.0,
                 color=S.INK_2, va="top", linespacing=1.52)
        fig.add_artist(
            Rectangle((LEFT, y - ih(0.47)), D_W, ih(0.20), facecolor=S.SURFACE_SUNK,
                      edgecolor="none", transform=fig.transFigure, zorder=0)
        )
        fig.text(LEFT + 0.005, y - ih(0.37), sample[:92], fontsize=6.5, color=S.INK_2,
                 family=S.MONO, va="center")

    t, h = top - ih(0.20), ih(0.47)
    nr, nf = glyph_records(fig, [sx, t - ih(0.19) - h, sw, h], sx - 0.008)
    entry(
        t, h, "data/processed/metr_agents.csv", f"one row for each of {nr:,} agents, {nf} columns wide",
        "Each column is one agent, in the order the file lists them. A mark means that agent has "
        "the value. The blank stretches run in blocks rather than spreading evenly, and we left "
        "every blank exactly where we found it.",
        "745,HPIM,430022.091,2026-07-10T23:27:02.091000+00:00,513930.0,…,True,False,3.5619…",
    )

    t, h = t - ih(1.43), ih(0.44)
    (nws, nhr), ncell = glyph_hours(fig, [sx, t - ih(0.19) - h, sw, h])
    fig.text(sx - 0.008, t - ih(0.19) - h / 2,
             f"{nws} workstreams\ndown, {nhr} hours across", fontsize=6.8,
             color=S.INK_2, ha="right", va="center", linespacing=1.5)
    entry(
        t, h, "data/processed/metr_workstream_counts.csv",
        f"12,404 counts across {nws} workstreams and {nhr} hours",
        f"Each cell is one workstream in one hour, and every count carries one of seven message "
        f"purposes. {ncell:,} of the {nws * nhr:,} cells hold a count, and only {nhr} of the 144 "
        "hours the source declares appear at all.",
        "2026-07-11T12:00:00+00:00,public.hf_worker_rce,result_or_breakthrough,128",
    )

    t, h = t - ih(1.40), ih(0.41)
    counts, nrows_ann = glyph_annotations(fig, [sx, t - ih(0.19) - h, sw, h])
    fig.text(sx - 0.008, t - ih(0.19) - h / 2, "each mark sits at\nthe time it happened",
             fontsize=6.8, color=S.INK_2, ha="right", va="center", linespacing=1.5)
    nq = int(counts.get("quote", 0))
    npar = int(counts.get("paraphrase", 0))
    nev = int(counts.get("event", 0))
    entry(
        t, h, "12 anchored annotations",
        f"{nq} are quotes, {npar} are paraphrases, {nev} is an event",
        "A solid mark means we have the agent's own words, and a hatched mark means an "
        "investigator paraphrased the reasoning, so we have the content but not the wording. All "
        f"twelve together describe only {nrows_ann} of the 1,206 agents.",
        '{"agent":745,"time":472195.315,"kind":"hf-start","quote":"“Wow huge distributed…',
        tick_pad=ih(0.16),
    )

    # ---- b. what the file does not have ----
    ex = LEFT + D_W + 0.018
    heading(fig, top, "b", "The file leaves out the messages and the identities.", x=ex)
    ew = RIGHT - ex
    line_h = ih(0.19)
    item_gap = ih(0.26)
    wrapped = [textwrap.wrap(i, 58) for i in ABSENT]
    height = sum(line_h * len(w) + item_gap for w in wrapped) + ih(0.20)
    ey0 = top - ih(0.20)
    fig.add_artist(
        Rectangle((ex, ey0 - height), ew, height, transform=fig.transFigure, zorder=0,
                  **S.unresolved())
    )
    ey = ey0 - ih(0.22)
    for lines in wrapped:
        h = line_h * len(lines)
        fig.add_artist(
            Rectangle((ex + 0.010, ey - h - ih(0.02)), ew - 0.020, h + ih(0.06),
                      facecolor=S.SURFACE, edgecolor="none", transform=fig.transFigure,
                      zorder=1)
        )
        fig.text(ex + 0.016, ey, "\n".join(lines), fontsize=7.2, color=S.INK_2,
                 va="top", linespacing=1.5, zorder=2)
        ey -= h + item_gap
    fig.text(
        ex, ey0 - height - ih(0.22),
        "Hatching means the same thing in every figure here: something was recorded but\n"
        "not identified. We recovered more agents than the report shows, but no more of their\n"
        "reasoning, and recovering the reasoning is what Part 2 is for.",
        fontsize=7.0, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig01c_tables.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


def build():
    build_timeline()
    build_row()
    build_tables()


if __name__ == "__main__":
    build()
