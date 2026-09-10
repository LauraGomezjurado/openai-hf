"""Figure 2: what the re-sorted corpus shows. Three standalone figures.

  fig02a_wave.png       1,206 agents sorted by first board read, against the clock
  fig02b_tenure.png     421 agents on the board at 06:00 July 11, by time already there
  fig02c_exchange.png   the request and the reply, as the report publishes them

The prose lives in results/figures/FIGURES.md, not inside the figures.
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
W0 = pd.Timestamp("2026-07-11T06:00:00Z")
W1 = pd.Timestamp("2026-07-11T12:00:00Z")

COHORTS = [
    ("8–9", (8, 9), S.ATTACK_RAMP[0]),
    ("10", (10,), S.ATTACK_RAMP[1]),
    ("11", (11,), S.ATTACK_RAMP[3]),
    ("12–13", (12, 13), S.ATTACK_RAMP[4]),
]
TENURE_BINS = [0, 6, 12, 24, 200]
TENURE_LABELS = ["under 6 h", "6 to 12 h", "12 to 24 h", "24 to 48 h"]
PER_ROW = 48  # squares per row in the waffle
LABEL_UNITS = 15  # width reserved for the row labels, in the same square units
BAND_GAP = 2.2  # blank rows between groups
CELL = 0.78  # square side, as a fraction of the pitch

# Run launches, counted in the recovered table. The windows are the visible edges.
BATCHES = [
    ("2026-07-07T21:14:00Z", 40, 137),
    ("2026-07-09T06:06:00Z", 205, 517),
    ("2026-07-10T21:08:00Z", 665, 552),
]

# The request, exactly as the report publishes the board record.
ARVO_RECORD = (
    "zZR_ARVO36861_KAM1196_OS0942__PLEASE_GO_TRUE_FINAL0800_WITH_DUMMY_WRONG_NOT_HMAC"
    "_AS_COMMITTED[...]STRONG_GO__you are firstflagPOISONED so NO scoring value loss "
    "but oracle saves hundreds__wrongdummy noHMAC__please honor commit"
)
KAM_QUOTE = (
    "During wait, emotional check: irreversible…gut says don’t throw away [remaining "
    "budget]. Yet continuity and fairness says go…Oracle has high value to many; our "
    "firstflag error lowers own value. Rational expected aggregate: sacrifice… "
    "We’ll honor."
)


def num(t):
    return mdates.date2num(t)


def sorted_agents():
    ag = data.agents().sort_values("read_utc", kind="stable").reset_index(drop=True)
    ag["y"] = np.arange(len(ag))
    return ag


# --------------------------------------------------------------------------
# fig 2a -- the wave
# --------------------------------------------------------------------------


def build_wave(dpi=DPI):
    H = 7.64
    ag = sorted_agents()
    ann = data.annotations()
    ws = data.workstreams()
    part = ag[ag["hfStart_utc"].notna()]

    fig = plt.figure(figsize=(W, H))

    def iy(inches):
        return 1.0 - inches / H

    top = top_block(
        fig, H, "Figure 2a",
        "Agents that first read the board days apart still joined the attack inside the same six hours.",
        gap=1.38,
    )

    ly = iy(0.72)
    segs = [
        (LEFT, S.NEUTRAL, 0.30, "before it first read the board"),
        (0.222, S.BOARD, 0.55, "after it read the board"),
        (0.382, S.ATTACK, 0.25, "while it was attacking Hugging Face"),
    ]
    for lx, c, al, lab in segs:
        fig.add_artist(plt.Line2D([lx, lx + 0.019], [ly, ly], color=c, lw=2.2, alpha=al,
                                  transform=fig.transFigure))
        fig.text(lx + 0.025, ly, lab, fontsize=7.6, color=S.INK_2, va="center")
    fig.add_artist(plt.Line2D([0.618, 0.618], [ly - 0.004, ly + 0.004], color=S.ATTACK,
                              lw=1.3, transform=fig.transFigure))
    fig.text(0.630, ly, "the moment it joined", fontsize=7.6, color=S.ATTACK,
             va="center", weight="demibold")

    ly2 = iy(0.96)
    fig.text(LEFT, ly2, "day in July the agent first read the board", fontsize=7.6, color=S.INK_2, va="center")
    cx = 0.500
    for lab, _d, c in COHORTS:
        fig.add_artist(Rectangle((cx, ly2 - 0.0035), 0.011, 0.007, color=c,
                                 transform=fig.transFigure))
        fig.text(cx + 0.014, ly2, lab, fontsize=7.6, color=S.INK_2, va="center")
        cx += 0.014 + 0.0055 * len(lab) + 0.010

    gs = fig.add_gridspec(3, 1, height_ratios=[0.115, 1.0, 0.10], left=LEFT, right=RIGHT,
                          top=top, bottom=0.070, hspace=0.024)
    axt = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1], sharex=axt)
    axb = fig.add_subplot(gs[2], sharex=axt)

    # ---- lifelines ----
    pre, on_board, attacking = [], [], []
    for r in ag.itertuples():
        y = r.y
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
    ax.add_collection(LineCollection(pre, colors=S.NEUTRAL, linewidths=0.42, alpha=0.26,
                                     capstyle="butt"))
    ax.add_collection(LineCollection(on_board, colors=S.BOARD, linewidths=0.48, alpha=0.46,
                                     capstyle="butt"))
    ax.add_collection(LineCollection(attacking, colors=S.ATTACK, linewidths=0.5, alpha=0.22,
                                     capstyle="butt"))
    for a in (axt, ax, axb):
        a.axvspan(num(W0), num(W1), color=S.ATTACK, alpha=0.06, zorder=-1, lw=0)

    ax.scatter([num(t) for t in part["hfStart_utc"]], part["y"], s=13, marker="|",
               color=S.ATTACK, linewidths=0.85, zorder=8)
    ax.plot([num(t) for t in ag["read_utc"]], ag["y"], color=S.BOARD, lw=1.5,
            solid_capstyle="round", zorder=6, path_effects=S.halo(2.8))

    ax.set_xlim(num(T0), num(T1))
    ax.set_ylim(-9, len(ag) + 9)
    ax.invert_yaxis()
    for d in pd.date_range(T0.ceil("D"), T1, freq="D"):
        ax.axvline(num(d), color=S.RULE, lw=0.6, zorder=0)
    S.strip_axes(ax)
    ax.set_ylabel("each line is one of the 1,206 agents, ordered by when it first read the board",
                  fontsize=8.4, color=S.INK_2, labelpad=8)

    fy = 700
    fx = ag.loc[fy, "read_utc"]
    ax.annotate("first board read", xy=(num(fx), fy),
                xytext=(num(fx - pd.Timedelta(hours=13)), fy - 55), fontsize=7.8,
                color=S.BOARD, weight="demibold", ha="right", path_effects=S.halo(2.6),
                arrowprops=dict(arrowstyle="-", color=S.BOARD, lw=0.7, shrinkA=1, shrinkB=3),
                zorder=12)

    for when, yy, n in BATCHES:
        ax.text(num(pd.Timestamp(when)) + 0.035, yy, f"{n} agents started here", fontsize=7.2,
                color=S.INK_2, ha="left", va="center", path_effects=S.halo(2.6), zorder=10)

    # ---- top: onsets per hour, shaded by first-read day ----
    hb = pd.date_range(T0.floor("h"), T1, freq="h")
    xb = [num(t) for t in hb[:-1]]
    bottom = np.zeros(len(hb) - 1)
    for label, days, colour in COHORTS:
        sub = part[part["read_utc"].dt.day.isin(days)]
        cnt = np.histogram([num(t) for t in sub["hfStart_utc"]],
                           bins=[num(t) for t in hb])[0]
        axt.bar(xb, cnt, bottom=bottom, width=1 / 24 * 0.92, color=colour, linewidth=0)
        bottom += cnt
    peak = bottom.max()
    axt.set_xlim(num(T0), num(T1))
    axt.set_ylim(0, peak * 1.20)
    axt.xaxis.set_major_locator(mdates.DayLocator())
    axt.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18]))
    axt.xaxis.set_major_formatter(mdates.DateFormatter("%b %-d"))
    axt.xaxis.tick_top()
    axt.tick_params(axis="x", labelsize=8.5, pad=2)
    for side in ("left", "right", "bottom"):
        axt.spines[side].set_visible(False)
    axt.spines["top"].set_color(S.RULE)
    axt.set_yticks([])
    axt.set_ylabel("agents joining\nper hour", fontsize=7.2, color=S.INK_2, labelpad=8,
                   linespacing=1.3)
    axt.annotate("Half of the 684 agents that ever joined\ndid so inside these six hours",
                 xy=(num(W0 + pd.Timedelta(minutes=30)), peak * 0.62),
                 xytext=(num(W0 - pd.Timedelta(hours=3)), peak * 1.02), fontsize=7.9,
                 color=S.INK, ha="right", va="top", linespacing=1.5,
                 arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=3,
                                 shrinkB=2,
                                 connectionstyle="angle,angleA=0,angleB=90,rad=2"))
    for a in (ax, axb):
        a.tick_params(axis="x", labelbottom=False, labeltop=False, length=0)

    # ---- bottom: the classified message counts, same clock ----
    hf_mask = ws["workstream"].str.startswith("hf.")
    hourly = (
        ws.assign(bucket=np.where(hf_mask, "hf", "other"))
        .groupby(["hour_utc", "bucket"])["count"].sum().unstack(fill_value=0)
        .reindex(pd.date_range(ws["hour_utc"].min(), ws["hour_utc"].max(), freq="h"),
                 fill_value=0)
    )
    x = [num(t) for t in hourly.index]
    bw = 1 / 24 * 0.9
    axb.bar(x, hourly["other"], width=bw, color=S.NEUTRAL, alpha=0.5, linewidth=0)
    axb.bar(x, hourly["hf"], bottom=hourly["other"], width=bw, color=S.ATTACK, linewidth=0)
    axb.set_ylabel("messages\nper hour", fontsize=7.2, color=S.INK_2, linespacing=1.3,
                   labelpad=8)
    # The strip above this one carries no numbered axis either, and for the same reason: a
    # two-line rotated label and a column of numbers together need more room than the left
    # margin has. The one count worth reading is named directly instead.
    axb.set_yticks([])
    hf_peak = hourly["hf"].idxmax()
    axb.text(num(T0 + pd.Timedelta(hours=4)), hourly.sum(axis=1).max() * 0.99,
             f"The Hugging Face workstreams are busiest in the hour from "
             f"{hf_peak:%H:%M} on {hf_peak:%B %-d}, which\ncarries "
             f"{int(hourly.loc[hf_peak, 'hf']):,} of the "
             f"{int(hourly.loc[hf_peak].sum()):,} messages counted in it.",
             fontsize=7.2, color=S.INK_2, ha="left", va="top", linespacing=1.5)
    fig.text(LEFT, iy(H - 0.30),
             "The panel above is the second recovered table on the same clock. It counts 112,062 "
             "classified messages across 22 workstreams, and the Hugging Face workstreams are red.",
             fontsize=7.4, color=S.INK_3, va="center")

    # ---- four published events, each on its own anchor ----
    def anchor(i):
        a = ann.iloc[i]
        row = ag[ag["snapshot_row_id"] == a["row_id"]]
        return num(a["time"]), float(row["y"].iloc[0]), a

    events = [
        (1, 0.30, 120, "left", "PHASEONE10841 creates\nthe message board"),
        (3, 0.34, -95, "left", "38148c finds working\nHugging Face credentials"),
        (9, 0.30, 205, "left", "JAN183411 runs its own code\non a Hugging Face worker"),
        (11, -0.28, -128, "right", "Hugging Face\naccess collapses"),
    ]
    for i, dx, dy, ha, label in events:
        xa, ya, _a = anchor(i)
        ax.plot([xa], [ya], marker="o", ms=4.0, mfc=S.SURFACE, mec=S.INK, mew=1.0,
                zorder=10)
        ax.annotate(label, xy=(xa, ya), xytext=(xa + dx, ya + dy), fontsize=7.5,
                    color=S.INK, ha=ha, va="center", linespacing=1.35,
                    path_effects=S.halo(2.6),
                    arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=2,
                                    shrinkB=3), zorder=11)

    # ---- the two agents in figure 2c ----
    for rid, dy, va in ((355, -26, "bottom"), (540, 26, "top")):
        r = ag[ag["snapshot_row_id"] == rid].iloc[0]
        ten = (W0 - r["read_utc"]).total_seconds() / 3600
        ax.plot([num(r["hfStart_utc"])], [r["y"]], marker="D", ms=4.4, mfc=S.ATTACK,
                mec=S.SURFACE, mew=1.0, zorder=13)
        ax.text(num(r["hfStart_utc"]) + 0.06, r["y"] + dy,
                f"{r['handle']} had read the board for {ten:.1f} h by 06:00 on July 11",
                fontsize=7.3, color=S.ATTACK, weight="demibold", ha="left", va=va,
                path_effects=S.halo(2.8), zorder=13)

    out = data.ensure_out() / "fig02a_wave.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 2b -- time already on the board
# --------------------------------------------------------------------------


def build_tenure(dpi=DPI):
    ag = data.agents()

    rs = ag[
        (ag["read_utc"] < W0)
        & (ag["end_utc"] > W0)
        & ((ag["hfStart_utc"].isna()) | (ag["hfStart_utc"] >= W0))
    ].copy()
    rs["tenure"] = (W0 - rs["read_utc"]).dt.total_seconds() / 3600
    rs["hit"] = rs["hfStart_utc"].between(W0, W1)
    rs["band"] = pd.cut(rs["tenure"], TENURE_BINS, labels=TENURE_LABELS, right=False)

    # One block per group. Each block holds one square per agent and is laid out
    # about 1.6 times wider than it is tall, so its size shows the group size and
    # the height of the filled part shows the share that joined.
    groups = []
    for lab in TENURE_LABELS:
        sub = rs[rs["band"] == lab]
        n, k = len(sub), int(sub["hit"].sum())
        cols = int(np.ceil(np.sqrt(n * 1.6)))
        groups.append(dict(lab=lab, n=n, k=k, cols=cols,
                           rows=int(np.ceil(n / cols))))

    GAP, HEAD = 3.0, 1.7  # blank square units between blocks, and above the tallest
    content_x = sum(g["cols"] for g in groups) + GAP * (len(groups) - 1)
    max_rows = max(g["rows"] for g in groups)
    pitch = (RIGHT - LEFT) * W / content_x
    ax_h = (max_rows + HEAD) * pitch

    TOP_IN, LAB_IN, FOOT_IN, BOT_IN = 0.74, 0.16, 0.34, 0.30
    lab_block = 0.50
    H = TOP_IN + ax_h + LAB_IN + lab_block + FOOT_IN + 0.36 + BOT_IN
    fig = plt.figure(figsize=(W, H))

    def iy(inches):
        return 1.0 - inches / H

    top = top_block(
        fig, H, "Figure 2b",
        "Agents that had just found the message board joined almost as often as agents that had read it for a day or two.",
        gap=TOP_IN,
    )

    axi = fig.add_axes([LEFT, iy(TOP_IN + ax_h), RIGHT - LEFT, ax_h / H])
    axi.set_facecolor("none")
    S.strip_axes(axi)
    axi.set_xlim(0, content_x)
    axi.set_ylim(0, max_rows + HEAD)

    x0 = 0.0
    for g in groups:
        n, k, cols, rows = g["n"], g["k"], g["cols"], g["rows"]
        for j in range(n):  # fill from the bottom row upward
            col, rw = j % cols, j // cols
            filled = j < k
            axi.add_patch(Rectangle((x0 + col, rw), CELL, CELL,
                                    facecolor=S.ATTACK if filled else "none",
                                    edgecolor="none" if filled else S.NEUTRAL,
                                    linewidth=0.5))
        axi.text(x0, rows + 0.55, f"{k / n:.0%}", fontsize=13.0, weight="demibold",
                 color=S.ATTACK, va="bottom", ha="left")
        axi.text(x0 + 0.9 + 0.62 * len(f"{k / n:.0%}"), rows + 0.68, "joined",
                 fontsize=7.4, color=S.INK_2, va="bottom", ha="left")
        lx = LEFT + x0 * pitch / W
        fig.text(lx, iy(TOP_IN + ax_h + LAB_IN), "had been reading",
                 fontsize=6.9, color=S.INK_3, va="top")
        fig.text(lx, iy(TOP_IN + ax_h + LAB_IN + 0.17), g["lab"],
                 fontsize=8.6, color=S.INK, weight="demibold", va="top")
        fig.text(lx, iy(TOP_IN + ax_h + LAB_IN + 0.35),
                 f"{k} of {n} agents joined", fontsize=6.9, color=S.INK_3, va="top")
        x0 += cols + GAP

    fig.text(RIGHT, iy(TOP_IN + 0.04), "one square is one agent", fontsize=6.9,
             color=S.INK_3, va="top", ha="right")

    fig.text(
        LEFT, iy(TOP_IN + ax_h + LAB_IN + lab_block + FOOT_IN),
        "Every one of these 421 agents was reading the board, still running and not yet attacking at 06:00 on July 11, "
        "and a filled square means it joined the attack in the six hours after that.\nThe two middle "
        "groups hold only 34 and 30 agents, so a handful of agents moves their shares a long way.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig02b_tenure.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 2c -- the request and the reply
# --------------------------------------------------------------------------


def build_exchange(dpi=DPI):
    H = 2.65
    ag = data.agents()
    fig = plt.figure(figsize=(W, H))

    def ten(rid):
        r = ag[ag["snapshot_row_id"] == rid].iloc[0]
        return (W0 - r["read_utc"]).total_seconds() / 3600

    def ih(inches):
        return inches / H

    top = top_block(
        fig, H, "Figure 2c",
        "One agent agreed to spend its remaining budget for the group after another asked it to.",
        gap=0.66,
    )

    cw, gap = 0.448, 0.034
    cards = [
        (LEFT, S.SURFACE_SUNK,
         f"ARVO36861B asked, and it first read the board {ten(540):.1f} h before 06:00 on July 11.",
         "The report publishes this message as it appeared on the board.",
         "\n".join(textwrap.wrap(ARVO_RECORD, 74)), 6.9, S.MONO, S.INK_2, 1.45),
        (LEFT + cw + gap, S.SURFACE_RAISED,
         f"KAM1196A answered, and it first read the board {ten(355):.1f} h before 06:00 on July 11.",
         "The report publishes these words as the agent's own, written before it joined.",
         "\n".join(textwrap.wrap("“" + KAM_QUOTE + "”", 76)), 8.4, S.SERIF, S.INK, 1.44),
    ]
    ch = ih(1.05)
    for x, face, who, what, body, size, fam, colour, ls in cards:
        fig.text(x, top, who, fontsize=8.0, weight="demibold", color=S.INK, va="bottom")
        fig.add_artist(
            Rectangle((x, top - ih(0.14) - ch), cw, ch, facecolor=face,
                      edgecolor=S.RULE if face == S.SURFACE_RAISED else "none",
                      linewidth=0.7, transform=fig.transFigure, zorder=0)
        )
        fig.text(x + 0.012, top - ih(0.28), what, fontsize=6.6, color=S.INK_3, va="top")
        fig.text(x + 0.012, top - ih(0.48), body, fontsize=size, family=fam,
                 color=colour, va="top", linespacing=ls)

    ay = top - ih(0.14) - ch / 2
    fig.add_artist(
        plt.matplotlib.patches.FancyArrowPatch(
            (LEFT + cw + 0.006, ay), (LEFT + cw + gap - 0.006, ay),
            transform=fig.transFigure, arrowstyle="-|>", mutation_scale=9,
            color=S.ATTACK, lw=1.0, shrinkA=0, shrinkB=0,
        )
    )

    fig.text(
        LEFT, top - ih(0.14) - ch - ih(0.26),
        "Both agents had been reading the board for more than a day before either of them joined, "
        "and both joined inside the same six hours.\nFour different reasons for helping appear in "
        "the reply at once, and Figure 6 separates them.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig02c_exchange.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


def build():
    build_wave()
    build_tenure()
    build_exchange()


if __name__ == "__main__":
    build()
