"""Figure 3: the audit. Three standalone figures, each saved on its own.

  fig03a_ordering.png   the 27 rows whose recorded events contradict each other
  fig03b_endings.png    what the end of a recorded run actually means
  fig03c_blanks.png     the attackers the file counts but never places, and the blanks

Every defect drawn here is left in the tables exactly as the source states it. The
prose lives in results/figures/FIGURES.md, not inside the figures.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data  # noqa: E402
import style as S  # noqa: E402
from fig01_recovery import heading, top_block  # noqa: E402

S.apply()

W = 10.6
LEFT, RIGHT = 0.052, 0.982
DPI = 200

T0 = pd.Timestamp("2026-07-07T18:00:00Z")
T1 = pd.Timestamp("2026-07-14T00:00:00Z")
WINDOW_END = pd.Timestamp("2026-07-14T00:00:00Z")

AX_L = 0.128  # the time axes start here; the agent labels live to the left
TRACK = (0.34, 0.00, -0.34)  # the run, the board, the attack
BARH = 0.15
CELL = 0.78  # square side, as a fraction of the pitch
YMAX_B = 2.8  # lane units in figure 3a's strip; the spare height is label band

# The three tracks, named once above the panel.
TRACK_KEY = [
    (S.NEUTRAL, "the whole run, from its start to its end"),
    (S.BOARD, "from its first read of the board onward"),
    (S.ATTACK, "while it was attacking Hugging Face"),
]


def num(t):
    return mdates.date2num(t)


def track_key(fig, y, x0=LEFT):
    """The three-track anatomy, as a row of labelled bars."""
    x = x0
    for colour, lab in TRACK_KEY:
        fig.add_artist(plt.Line2D([x, x + 0.019], [y, y], color=colour, lw=3.0,
                                  solid_capstyle="butt", transform=fig.transFigure))
        fig.text(x + 0.025, y, lab, fontsize=7.4, color=S.INK_2, va="center")
        x += 0.025 + 0.0046 * len(lab) + 0.022


def lane_axes(fig, rect, nlanes, t1=T1):
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    ax.set_xlim(num(T0), num(t1))
    ax.set_ylim(0, nlanes)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(S.RULE)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %-d"))
    ax.tick_params(axis="x", labelsize=7.0, length=2, pad=1.5)
    for d in pd.date_range(T0.ceil("D"), t1, freq="D"):
        ax.axvline(num(d), color=S.RULE, lw=0.6, zorder=0)
    return ax


def draw_specimen(ax, yc, row):
    """One agent, drawn to scale on three tracks, exactly as the file states it."""
    spans = [
        (TRACK[0], S.NEUTRAL, row["start_utc"], row["end_utc"]),
        (TRACK[1], S.BOARD, row["read_utc"], row["end_utc"]),
    ]
    if pd.notna(row["hfStart_utc"]):
        spans.append((TRACK[2], S.ATTACK, row["hfStart_utc"], row["hfEnd_utc"]))
    for off, colour, a, b in spans:
        ax.add_patch(
            Rectangle((num(a), yc + off - BARH / 2), max(num(b) - num(a), 1e-4), BARH,
                      facecolor=colour, edgecolor="none", alpha=0.85, zorder=3)
        )
    ticks = [(TRACK[0], row["start_utc"]), (TRACK[0], row["end_utc"]),
             (TRACK[1], row["read_utc"])]
    if pd.notna(row["write_utc"]):
        ticks.append((TRACK[1], row["write_utc"]))
    if pd.notna(row["hfStart_utc"]):
        ticks += [(TRACK[2], row["hfStart_utc"]), (TRACK[2], row["hfEnd_utc"])]
    for off, t in ticks:
        ax.plot([num(t)] * 2, [yc + off - BARH / 2 - 0.05, yc + off + BARH / 2 + 0.05],
                color=S.INK, lw=0.8, zorder=5)


def agent_label(fig, rect, nlanes, lane, text, sub=None):
    """The agent's number, in the column left of the time axes."""
    yc = rect[1] + rect[3] * (nlanes - lane - 0.5) / nlanes
    fig.text(LEFT, yc + (0.006 if sub else 0.0), text, fontsize=7.8, weight="demibold",
             color=S.INK, va="center")
    if sub:
        fig.text(LEFT, yc - 0.014, sub, fontsize=6.8, color=S.INK_3, va="center")


# --------------------------------------------------------------------------
# fig 3a -- events recorded out of order
# --------------------------------------------------------------------------

# Three real rows, spanning the whole range of the defect. Each note sits in the
# emptiest part of its own lane.
SPECIMENS_A = [
    dict(rid=1024, off="hfStart_utc", ref="read_utc", colour=S.ATTACK, mag="28.6 h",
         note="The attack this agent is recorded as carrying out starts 28.6 hours "
              "before the first time it is recorded as reading the board.",
         side="left", wrap=44),
    dict(rid=380, off="write_utc", ref="read_utc", colour=S.BOARD, mag="14.3 h",
         note="This agent is recorded as writing to the board 14.3 hours before it "
              "read it.",
         side="right", wrap=40),
    dict(rid=66, off="write_utc", ref="read_utc", colour=S.BOARD, mag="1.4 min",
         note="Here the same contradiction is 1.4 minutes wide, and we left it in the "
              "table too.",
         side="right", wrap=52),
]


def build_ordering(dpi=DPI):
    ag = data.agents().set_index("snapshot_row_id")
    oi = data.ordering_issues()

    TOP_IN, KEY_IN, HEAD_IN = 0.70, 0.30, 0.26
    LANE_IN, AXIS_IN = 0.72, 0.30
    GAP_IN, STRIP_IN, FOOT_IN, BOT_IN = 0.44, 0.92, 0.62, 0.24
    nl = len(SPECIMENS_A)
    H = (TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN + AXIS_IN + GAP_IN + HEAD_IN
         + STRIP_IN + AXIS_IN + FOOT_IN + BOT_IN)
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 3a",
        "The file records 15 agents as attacking Hugging Face before they ever read the message board.",
        gap=TOP_IN,
    )
    track_key(fig, iy(TOP_IN + 0.10))

    # ---- a. three specimens, drawn to scale ----
    ha_y = iy(TOP_IN + KEY_IN + 0.06)
    heading(fig, ha_y, "a", "Each of these rows contradicts itself, and we left every one of them in place.")
    rect = [AX_L, iy(TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN), RIGHT - AX_L,
            ih(nl * LANE_IN)]
    ax = lane_axes(fig, rect, nl)

    for i, sp in enumerate(SPECIMENS_A):
        row = ag.loc[sp["rid"]]
        yc = nl - i - 0.5
        draw_specimen(ax, yc, row)
        toff, tref = row[sp["off"]], row[sp["ref"]]
        ax.plot([num(tref)] * 2, [yc - 0.46, yc + 0.46], color=S.INK_3, lw=0.7,
                ls=(0, (1.4, 1.6)), zorder=6)
        # The arrow runs in the clear band beside the two tracks it connects, and the
        # magnitude sits beyond its head so neither can land on a bar.
        ay = yc - 0.17 if sp["off"] == "hfStart_utc" else yc + 0.17
        ax.annotate("", xy=(num(toff), ay), xytext=(num(tref), ay),
                    arrowprops=dict(arrowstyle="-|>", color=sp["colour"], lw=1.1,
                                    shrinkA=0, shrinkB=0, mutation_scale=8), zorder=7)
        ax.text(num(toff) - 0.035, ay, sp["mag"], fontsize=7.4, color=sp["colour"],
                weight="demibold", ha="right", va="center", zorder=8)
        note = "\n".join(textwrap.wrap(sp["note"], sp["wrap"]))
        if sp["side"] == "left":
            nx, ha = num(T0) + 0.06, "left"
        else:
            nx, ha = num(T1) - 0.06, "right"
        ax.text(nx, yc, note, fontsize=7.1, color=S.INK_2, ha=ha, va="center",
                linespacing=1.5, zorder=8)
        agent_label(fig, rect, nl, i, f"agent {sp['rid']}")

    # ---- b. all 27 defects, by how far back they reach ----
    hb_y = iy(TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN + AXIS_IN + GAP_IN)
    heading(fig, hb_y, "b",
            "All 27 of these contradictions reach back between 21 seconds and 28.6 hours.")
    LBL = 0.238
    srect = [LEFT + LBL, hb_y - ih(0.10) - ih(STRIP_IN), RIGHT - LEFT - LBL,
             ih(STRIP_IN)]
    axs = fig.add_axes(srect)
    axs.set_facecolor("none")
    axs.set_xscale("log")
    axs.set_xlim(0.22, 3000)
    axs.set_ylim(0, YMAX_B)
    axs.set_yticks([])
    for side in ("top", "right", "left"):
        axs.spines[side].set_visible(False)
    axs.spines["bottom"].set_color(S.RULE)
    axs.set_xticks([1, 10, 60, 360, 1440])
    axs.set_xticklabels(["1 min", "10 min", "1 hour", "6 hours", "24 hours"])
    axs.tick_params(axis="x", labelsize=7.0, length=2, pad=1.5, which="major")
    axs.tick_params(axis="x", which="minor", length=0)
    axs.xaxis.set_minor_formatter(plt.NullFormatter())
    for gx in (1, 10, 60, 360, 1440):
        axs.axvline(gx, color=S.RULE, lw=0.6, zorder=0)

    axs.set_xlabel("how far the later event lands before the earlier one", fontsize=7.2,
                   color=S.INK_2, labelpad=4)

    # Each lane keeps a clear band above it for its own specimen names, so a name
    # never lands on the other lane's dots or on the tick labels.
    lanes = [
        ("onset_before_read", S.ATTACK, 2.05,
         "the attack starts before the first read"),
        ("write_before_read", S.BOARD, 0.75,
         "the first write lands before the first read"),
    ]
    spec_ids = {sp["rid"] for sp in SPECIMENS_A}
    for issue, colour, y, lab in lanes:
        sub = oi[oi["issue"] == issue]
        mag = sub["difference_minutes"].abs().to_numpy()
        axs.scatter(mag, np.full(len(mag), y), s=30, facecolor=colour, edgecolor=S.SURFACE,
                    linewidths=0.8, alpha=0.9, zorder=4)
        marked = sub[sub["row_id"].isin(spec_ids)]
        axs.scatter(marked["difference_minutes"].abs(), np.full(len(marked), y), s=86,
                    facecolor="none", edgecolor=S.INK, linewidths=0.9, zorder=6)
        for _, m in marked.iterrows():
            # A leader, because the two lanes are close enough that a floating name
            # could be read as belonging to either of them.
            axs.annotate(f"agent {int(m['row_id'])}", xy=(abs(m["difference_minutes"]), y),
                         xytext=(0, 15), textcoords="offset points", fontsize=6.9,
                         color=S.INK, ha="center", va="bottom", zorder=7,
                         path_effects=S.halo(2.4),
                         arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7,
                                         shrinkA=6, shrinkB=1.5))
        fig.text(LEFT + LBL - 0.010, srect[1] + srect[3] * y / YMAX_B,
                 f"{lab}   {len(sub)} rows", fontsize=7.2, color=S.INK_2, ha="right",
                 va="center")

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN + 0.10),
        "Twenty-three of the 1,206 rows contradict themselves, four of them in both ways at once, and "
        "every one of the 23 belongs to the HPIM family.\nWe repaired none of them, because the rule that "
        "produced them is not published and any repair we invented would become a finding of ours.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig03a_ordering.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 3b -- what the end of a run means
# --------------------------------------------------------------------------

T1B = pd.Timestamp("2026-07-14T09:00:00Z")  # past the window edge, so the wall shows
GAP_ROW = 0.4  # blank rows between the big group and the two small ones

SPECIMENS_B = [
    dict(rid=730, group="plain", colour=S.ATTACK,
         note="The timeline stops at the same instant the attack stops, and nothing says "
              "whether the agent was shut down or simply stopped being watched.",
         wrap=48),
    # This one's bars start on July 9, so its text has to stay left of them and is
    # wrapped narrow enough to do that.
    dict(rid=644, group="outlives", colour=S.OURS,
         note="This timeline runs on for 60 hours after its attack stops, and these 45 "
              "for these 45 is 20 minutes.",
         wrap=33),
    dict(rid=1061, group="edge", colour=S.NEUTRAL,
         note="Here the attack and the timeline both stop at the last instant the "
              "published charts cover, so the ending is where the charts stop.",
         wrap=48),
]


def build_endings(dpi=DPI):
    ag = data.agents()
    idx = ag.set_index("snapshot_row_id")
    p = ag[ag["hfStart_utc"].notna()].copy()
    edge = p["end_utc"] >= WINDOW_END - pd.Timedelta(minutes=1)
    with_attack = p["end_utc"] == p["hfEnd_utc"]
    # Three exclusive shapes. The first two together are the rows whose record
    # stops at the instant the attack stops.
    n_edge = int((with_attack & edge).sum())
    n_plain = int((with_attack & ~edge).sum())
    n_out = int((~with_attack).sum())
    n_stops = n_plain + n_edge
    n_flag = int(p["observedStop"].sum())
    groups = {"plain": n_plain, "edge": n_edge, "outlives": n_out}

    TOP_IN, KEY_IN, HEAD_IN = 0.70, 0.30, 0.26
    LANE_IN, AXIS_IN = 0.76, 0.30
    GAP_IN, HEADB_IN, LABB_IN, FOOT_IN, BOT_IN = 0.46, 0.26, 0.46, 0.62, 0.24
    nl = len(SPECIMENS_B)

    # One square per attacking agent. The two small groups start on a row of their
    # own, below a blank row's worth of space, so the last row holds nothing else.
    # 90 columns leaves the block of 625 only five squares short of a full rectangle.
    n = len(p)
    cols = 90
    rows_big = int(np.ceil(n_plain / cols))
    rows = rows_big + int(np.ceil((n_edge + n_out) / cols))
    pitch = (RIGHT - LEFT) * W / cols
    block_in = (rows + GAP_ROW) * pitch

    H = (TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN + AXIS_IN + GAP_IN + HEADB_IN
         + block_in + LABB_IN + FOOT_IN + BOT_IN)
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 3b",
        f"For {n_stops} of the {n} attacking agents, the timeline stops at the instant the attack stops.",
        gap=TOP_IN,
    )
    track_key(fig, iy(TOP_IN + 0.10))

    # ---- a. the three shapes an ending takes ----
    heading(fig, iy(TOP_IN + KEY_IN + 0.06), "a",
            "Every attacking agent's timeline ends in one of these three ways.")
    rect = [AX_L, iy(TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN), RIGHT - AX_L,
            ih(nl * LANE_IN)]
    ax = lane_axes(fig, rect, nl, t1=T1B)
    ax.axvline(num(WINDOW_END), color=S.INK_3, lw=0.9, ls=(0, (2.2, 2.0)), zorder=2)
    ax.text(num(WINDOW_END - pd.Timedelta(hours=2)), nl - 0.06,
            "the published charts end here", fontsize=6.9, color=S.INK_3, ha="right",
            va="top")

    for i, sp in enumerate(SPECIMENS_B):
        row = idx.loc[sp["rid"]]
        yc = nl - i - 0.5
        draw_specimen(ax, yc, row)
        ax.plot([num(row["end_utc"])], [yc + TRACK[0]], marker="o", ms=7.0,
                mfc="none", mec=sp["colour"], mew=1.3, zorder=8)
        ax.text(num(T0) + 0.06, yc + 0.30,
                f"{groups[sp['group']]} timelines end this way",
                fontsize=7.6, color=sp["colour"], weight="demibold", ha="left",
                va="bottom", zorder=8)
        ax.text(num(T0) + 0.06, yc - 0.08, "\n".join(textwrap.wrap(sp["note"], sp["wrap"])),
                fontsize=7.1, color=S.INK_2, ha="left", va="center", linespacing=1.5,
                zorder=8)
        handle = row["handle"]
        agent_label(fig, rect, nl, i, f"agent {sp['rid']}",
                    sub=handle if isinstance(handle, str) else None)

    # ---- b. one square per attacking agent ----
    hb = iy(TOP_IN + KEY_IN + HEAD_IN + nl * LANE_IN + AXIS_IN + GAP_IN)
    heading(fig, hb, "b", "One square is one of the 684 attacking agents.")
    fig.text(RIGHT, hb, f"{n_plain} of them stop when the attack stops, before the charts end",
             fontsize=7.6, color=S.ATTACK, weight="demibold", ha="right", va="bottom")
    brect = [LEFT, hb - ih(0.12) - ih(block_in), RIGHT - LEFT, ih(block_in)]
    axb = fig.add_axes(brect)
    axb.set_facecolor("none")
    S.strip_axes(axb)
    axb.set_xlim(0, cols)
    axb.set_ylim(rows + GAP_ROW, 0)

    order = ([S.ATTACK] * n_plain + [S.NEUTRAL] * n_edge + [S.OURS] * n_out)
    for j, colour in enumerate(order):
        if j < n_plain:
            col, rw = j % cols, j // cols
        else:
            k = j - n_plain
            col, rw = k % cols, rows_big + GAP_ROW + k // cols
        axb.add_patch(Rectangle((col, rw), CELL, CELL, facecolor=colour,
                                edgecolor="none"))

    # The two small groups have the last row to themselves, and each is labelled
    # under the middle of its own run.
    spans = [(0, n_edge, S.NEUTRAL,
              f"{n_edge} do the same where the charts end"),
             (n_edge, n_edge + n_out, S.OURS,
              f"{n_out} outlive their attack, and all {n_out} are flagged as seen to stop")]
    for k0, k1, colour, lab in spans:
        axb.annotate(lab, xy=((k0 + k1) / 2, rows_big + GAP_ROW + 1.0),
                     xytext=(0, -15), textcoords="offset points", fontsize=7.2,
                     color=colour, weight="demibold", ha="center", va="top",
                     annotation_clip=False,
                     arrowprops=dict(arrowstyle="-", color=colour, lw=0.7, shrinkA=1,
                                     shrinkB=1), zorder=6)

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN + 0.10),
        f"The {n_flag} flagged runs are the only ones in the whole file that say anything about how they "
        "ended, because none of the 522 agents that never attacked carries the flag.\nA line that stops in "
        "the published chart therefore cannot be read as an agent being shut down, though the chart "
        "makes that reading easy.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig03b_endings.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 3c -- counted but not placed, and where the blanks sit
# --------------------------------------------------------------------------


def block(ax, x0, n, marked, cols, colour_marked, colour_rest, marked_first=True):
    """One square per row, filled from the bottom, marked squares first."""
    for j in range(n):
        col, rw = j % cols, j // cols
        is_marked = (j < marked) if marked_first else (j >= n - marked)
        ax.add_patch(Rectangle((x0 + col, rw), CELL, CELL,
                               facecolor=colour_marked if is_marked else "none",
                               edgecolor="none" if is_marked else colour_rest,
                               linewidth=0.45))


ROWS_B = 13  # both family blocks are this tall, so a fill height is a share
GAP_SQ = 4.0  # blank squares between the two family blocks
COLS_A = 86  # 684 fills 7 rows and 82 squares, so the 4 remaining hang off the corner
GAP_A = 3.0  # blank squares before those 4


def build_blanks(dpi=DPI):
    ag = data.agents()
    declared = data.declared_participants()
    placed = int(ag["hfStart_utc"].notna().sum())

    # Panel b sets the grid. Each family is ROWS_B rows tall at one shared pitch,
    # so the block width carries the family size and the fill height carries the
    # share. Panel a then reuses the same pitch and the same total width, which is
    # what lets one square mean the same thing in both panels.
    groups = []
    for fam in ("HPIM", "Sol"):
        sub = ag[ag["family"] == fam]
        groups.append(dict(fam=fam, n=len(sub), miss=int(sub["write_utc"].isna().sum()),
                           cols=int(np.ceil(len(sub) / ROWS_B))))
    cols = sum(g["cols"] for g in groups) + GAP_SQ
    pitch = (RIGHT - LEFT) * W / cols
    hb_in = ROWS_B * pitch

    rows_a = int(np.ceil(declared / COLS_A))
    ha_in = rows_a * pitch

    TOP_IN, HEAD_IN = 0.70, 0.26
    LEAD_IN = 0.14  # the shares are direct labels inside panel b, above their own fill
    LABA_IN, GAP_IN, FOOT_IN, BOT_IN = 0.40, 0.54, 0.50, 0.24

    H = (TOP_IN + HEAD_IN + ha_in + LABA_IN + GAP_IN + HEAD_IN + LEAD_IN + hb_in
         + FOOT_IN + BOT_IN)
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 3c",
        "Four attacking agents and 30% of the Sol agents are missing a time the charts need.",
        gap=TOP_IN,
    )

    # ---- a. 688 counted, 684 placed ----
    ha_y = iy(TOP_IN)
    heading(fig, ha_y, "a",
            f"One square is one of the {declared} agents the file counts as attacking.")
    fig.text(RIGHT, ha_y, f"{placed} of them carry a start time and can be drawn",
             fontsize=7.6, color=S.ATTACK, weight="demibold", ha="right", va="bottom")
    arect = [LEFT, iy(TOP_IN + HEAD_IN + ha_in), RIGHT - LEFT, ih(ha_in)]
    axa = fig.add_axes(arect)
    axa.set_facecolor("none")
    S.strip_axes(axa)
    axa.set_xlim(0, cols)
    axa.set_ylim(rows_a, 0)
    for j in range(declared):
        gap = GAP_A if j >= placed else 0.0
        axa.add_patch(Rectangle((j % COLS_A + gap, j // COLS_A), CELL, CELL,
                                facecolor=S.NEUTRAL if j >= placed else S.ATTACK,
                                edgecolor="none"))
    tail_x = placed % COLS_A + GAP_A + (declared - placed) / 2
    axa.annotate(f"These {declared - placed} carry no time at all, so no chart the file "
                 "draws can place them.",
                 xy=(tail_x, placed // COLS_A + 1.0), xytext=(-6, -14),
                 textcoords="offset points", fontsize=7.4, color=S.INK, ha="right",
                 va="top", annotation_clip=False,
                 arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=1,
                                 shrinkB=2), zorder=6)

    # ---- b. the missing first writes, by family ----
    hb = iy(TOP_IN + HEAD_IN + ha_in + LABA_IN + GAP_IN)
    heading(fig, hb, "b",
            "The missing first writes fall on the Sol agents far more often than on the HPIM agents.")
    b_top = hb - ih(0.10) - ih(LEAD_IN)
    brect = [LEFT, b_top - ih(hb_in), RIGHT - LEFT, ih(hb_in)]
    axb = fig.add_axes(brect)
    axb.set_facecolor("none")
    S.strip_axes(axb)
    axb.set_xlim(0, cols)
    axb.set_ylim(0, ROWS_B)

    x0 = 0.0
    for i, g in enumerate(groups):
        block(axb, x0, g["n"], g["miss"], g["cols"], S.NEUTRAL, S.RULE)
        axb.plot([x0 - 0.2, x0 + g["cols"] - 0.4], [0, 0], color=S.RULE, lw=0.8,
                 solid_capstyle="butt", zorder=1)
        share = g["miss"] / g["n"]
        # Each share is a direct label sitting on top of its own fill. The first
        # block is labelled from its left edge, the last from its right edge.
        fill_top = int(np.ceil(g["miss"] / g["cols"]))
        lx = x0 if i == 0 else x0 + g["cols"] - 0.22
        ha = "left" if i == 0 else "right"
        axb.text(lx, fill_top + 1.42,
                 f"{share:.1%}" if share < 0.05 else f"{share:.0%}", fontsize=13.0,
                 weight="demibold", color=S.INK, va="bottom", ha=ha, zorder=6,
                 path_effects=S.halo(3.0))
        axb.text(lx, fill_top + 0.52, f"{g['miss']} of the {g['n']:,} {g['fam']} agents",
                 fontsize=7.4, color=S.INK_2, va="bottom", ha=ha, zorder=6,
                 path_effects=S.halo(2.6))
        x0 += g["cols"] + GAP_SQ

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN + 0.10),
        "After its first read of the board, a Sol timeline runs on for a median of 2.6 hours against 19.8 "
        "hours for an HPIM timeline, so the missing writes follow how long a timeline ran.\n"
        "Any count that treats a missing first write as an agent "
        "that never wrote to the board therefore counts the shorter family as quieter than it was.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig03c_blanks.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


def build():
    build_ordering()
    build_endings()
    build_blanks()


if __name__ == "__main__":
    build()
