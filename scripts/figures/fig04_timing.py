"""Figure 4: the recruitment contrast and what it rests on.

  fig04a_cohorts.png    the 1,191 eligible agents, by the day each found the board
  fig04b_erosion.png    the same contrast under four sizes of timestamp error
  fig04c_denominator.png  what population reaches the report's over-90% level

The prose lives in results/figures/FIGURES.md, not inside the figures.
"""

from __future__ import annotations

import sys
from pathlib import Path

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

DAYS = [8, 9, 10, 11, 12, 13]
ROW_IN = 0.00212  # inches of height per agent
BAND_GAP = 62  # blank rows between two cohorts
TPAD = 26  # blank rows above the first cohort, so its marks are not clipped
YPAD = 132  # blank rows under the last cohort, so a pushed label has somewhere to go
LBL = 0.216  # figure fraction reserved for the cohort labels
BRACK = 0.011  # figure width from the bracket to the label text
XMIN, XMAX = 0.012, 130.0  # hours since the agent's first read
XT = [(1 / 60, "1 min"), (10 / 60, "10 min"), (1, "1 hour"), (6, "6 hours"),
      (24, "24 hours"), (96, "4 days")]


def eligible():
    """The 1,191 rows whose recorded times can carry a delay from read to onset.

    The 15 rows that record an onset before the first read are the ones excluded;
    they are the subject of Figure 3a.
    """
    ag = data.agents()
    bad = set(data.ordering_issues().query("issue == 'onset_before_read'")["row_id"])
    e = ag[~ag["snapshot_row_id"].isin(bad)].copy()
    e["day"] = e["read_utc"].dt.day
    e["joined"] = e["hfStart_utc"].notna()
    e["lag_h"] = np.where(
        e["joined"],
        (e["hfStart_utc"] - e["read_utc"]).dt.total_seconds(),
        (e["end_utc"] - e["read_utc"]).dt.total_seconds(),
    ) / 3600.0
    return e


def spread(centres, gap, lo, hi):
    """Push labels apart to a minimum spacing, keeping them inside [lo, hi]."""
    out = list(centres)
    for i in range(1, len(out)):
        out[i] = max(out[i], out[i - 1] + gap)
    if out[-1] > hi:
        out[-1] = hi
        for i in range(len(out) - 2, -1, -1):
            out[i] = min(out[i], out[i + 1] - gap)
    return [max(lo, v) for v in out]


# --------------------------------------------------------------------------
# fig 4a -- every eligible agent, grouped by the day it found the board
# --------------------------------------------------------------------------


def build_cohorts(dpi=DPI):
    e = eligible()

    bands, y = [], TPAD
    for d in DAYS:
        sub = e[e["day"] == d].sort_values("lag_h")
        bands.append(dict(day=d, y0=y, n=len(sub), sub=sub,
                          k=int((sub["joined"] & (sub["lag_h"] <= 1)).sum()),
                          ever=int(sub["joined"].sum())))
        y += len(sub) + BAND_GAP
    rows_total = y - BAND_GAP + YPAD

    TOP_IN, KEY_IN = 0.70, 0.34
    RAS_IN = rows_total * ROW_IN
    AXIS_IN, FOOT_IN, BOT_IN = 0.52, 0.46, 0.24
    H = TOP_IN + KEY_IN + RAS_IN + AXIS_IN + FOOT_IN + BOT_IN
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 4a",
        "Agents that found the board on July 11 joined within the hour four times as often as July 9's readers.",
        gap=TOP_IN,
    )

    ky = iy(TOP_IN + 0.13)
    fig.text(LEFT, ky, "Every mark is one of the 1,191 agents whose recorded times can "
             "carry a delay.", fontsize=7.4, color=S.INK_2, va="center")
    for x, colour, lab in ((0.428, S.ATTACK, "it joined the attack here"),
                           (0.590, S.NEUTRAL, "its timeline ended here with no attack")):
        fig.add_artist(plt.Line2D([x, x], [ky - 0.007, ky + 0.007], color=colour, lw=1.6,
                                  transform=fig.transFigure))
        fig.text(x + 0.008, ky, lab, fontsize=7.4, color=S.INK_2, va="center")

    rect = [LEFT + LBL, iy(TOP_IN + KEY_IN + RAS_IN), RIGHT - LEFT - LBL, ih(RAS_IN)]
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    ax.set_xscale("log")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(rows_total, 0)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(S.RULE)
    ax.set_xticks([v for v, _ in XT])
    ax.set_xticklabels([l for _, l in XT])
    ax.tick_params(axis="x", labelsize=7.0, length=2, pad=1.5)
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.tick_params(axis="x", which="minor", length=0)
    for v, _ in XT:
        ax.axvline(v, color=S.RULE, lw=0.6, zorder=0)

    # The hour the contrast is measured over. Inside each cohort the agents are
    # sorted by their own delay, so the ones that joined inside the hour are the
    # top k rows of the band and the height of the block is the count.
    ax.axvline(1.0, color=S.INK_3, lw=0.9, ls=(0, (2.4, 2.0)), zorder=2)
    ax.text(0.93, rows_total - 14, "one hour after its own first read", fontsize=7.2,
            color=S.INK_3, ha="right", va="bottom")

    for b in bands:
        sub, k = b["sub"], b["k"]
        yy = b["y0"] + np.arange(len(sub))
        # A container per cohort, so that a block of red is read inside the cohort
        # it belongs to rather than next to the cohort above it.
        ax.add_patch(Rectangle((XMIN, b["y0"]), XMAX - XMIN, b["n"],
                               facecolor=S.SURFACE_SUNK, lw=0, zorder=0))
        if k:
            ax.add_patch(Rectangle((XMIN, b["y0"]), 1.0 - XMIN, k, facecolor=S.ATTACK,
                                   alpha=0.10, lw=0, zorder=1))
            ax.plot([1.0, 1.0], [b["y0"], b["y0"] + k], color=S.ATTACK, lw=3.0,
                    solid_capstyle="butt", zorder=5)
            if k * ROW_IN >= 0.055:
                # The two cohorts are almost the same size, so these two block
                # heights are the two rates as well as the two counts.
                ax.annotate(f"{k / b['n']:.1%}", xy=(1.0, b["y0"] + k / 2),
                            xytext=(6, 0), textcoords="offset points", fontsize=11.5,
                            weight="demibold", color=S.ATTACK, ha="left", va="center",
                            zorder=6, path_effects=S.halo(3.0))
        for joined, colour in ((False, S.NEUTRAL), (True, S.ATTACK)):
            m = (sub["joined"] == joined).to_numpy()
            ax.scatter(sub["lag_h"].to_numpy()[m], yy[m], s=7, marker="|",
                       color=colour, linewidths=0.62, alpha=0.85, zorder=4)

    ax.set_xlabel("time from an agent's first read of the message board",
                  fontsize=7.8, color=S.INK_2, labelpad=5)

    # The grey is the honest counterweight to the rate above it, so the leader has
    # to land on one of the grey marks rather than in the space beside them.
    b9 = bands[1]
    s9 = b9["sub"].reset_index(drop=True)
    i9 = int(0.80 * len(s9))
    while i9 < len(s9) - 1 and s9.loc[i9, "joined"]:
        i9 += 1
    ax.annotate(f"{b9['n'] - b9['ever']} of these {b9['n']} timelines end with no attack "
                "recorded.",
                xy=(s9.loc[i9, "lag_h"], b9["y0"] + i9),
                xytext=(0.92, b9["y0"] + 0.52 * b9["n"]),
                fontsize=7.4, color=S.INK_2, ha="right", va="center",
                path_effects=S.halo(2.8),
                arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=5,
                                shrinkB=2.5), zorder=7)

    # Each cohort gets a bracket in the margin, because three of the six hold too
    # few agents to make a band a reader can see.
    xb = LEFT + LBL - BRACK
    gap_rows = 0.30 / ROW_IN
    ys = spread([b["y0"] + b["n"] / 2 for b in bands], gap_rows, 0.13 / ROW_IN,
                rows_total - 0.15 / ROW_IN)

    def yf(row):
        return rect[1] + rect[3] * (1 - row / rows_total)

    for b, ylab in zip(bands, ys):
        y_top, y_bot, y_mid = yf(b["y0"]), yf(b["y0"] + b["n"]), yf(ylab)
        fig.add_artist(plt.Line2D([xb, xb], [y_top, y_bot], color=S.INK_3, lw=1.1,
                                  solid_capstyle="butt", transform=fig.transFigure))
        elbow = [(xb, (y_top + y_bot) / 2), (xb - 0.006, (y_top + y_bot) / 2),
                 (xb - 0.006, y_mid), (xb - 0.010, y_mid)]
        fig.add_artist(plt.Line2D([p[0] for p in elbow], [p[1] for p in elbow],
                                  color=S.INK_3, lw=0.7, transform=fig.transFigure))
        fig.text(xb - 0.016, y_mid + ih(0.077), f"July {b['day']}", fontsize=8.8,
                 weight="demibold", color=S.INK, ha="right", va="center")
        fig.text(xb - 0.016, y_mid - ih(0.058),
                 f"{b['k']} of {b['n']} joined inside the hour", fontsize=7.0,
                 color=S.ATTACK if b["k"] else S.INK_3, ha="right", va="center")

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN + 0.10),
        "The July 9 cohort is entirely HPIM and the July 11 cohort is 393 HPIM agents and 124 Sol agents, so "
        "the two cohorts differ in composition as well as in date.\nWithin the HPIM family alone the two "
        "shares are 6.4% and 29.8%. The last two cohorts hold only 13 and 2 agents. The 15 rows that "
        "record an attack before the first read are left out here.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig04a_cohorts.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 4b -- the same contrast under four sizes of timestamp error
# --------------------------------------------------------------------------

ERRS = [(0, "nothing at all"), (5, "5 minutes"), (30, "30 minutes"), (120, "2 hours")]
HORIZONS = [(1, "joined within one hour", "The report makes its claim here."),
            (6, "joined within six hours", ""),
            (24, "joined within 24 hours", "")]
LBL_B = 0.172  # figure fraction for the row labels
COL_GAP = 0.024


def build_erosion(dpi=DPI):
    t = pd.read_csv("results/cpu/timing_sensitivity.csv")
    t = t[t["group"] == "all"]
    cell = {(int(r.horizon_hours), int(r.per_timestamp_error_minutes), int(r.read_day)):
            (float(r.lower), float(r.upper)) for r in t.itertuples()}
    n9 = int(t[t["read_day"] == 9]["nominal_risk_rows"].iloc[0])
    n11 = int(t[t["read_day"] == 11]["nominal_risk_rows"].iloc[0])

    TOP_IN, KEY_IN, HEAD_IN = 0.70, 0.32, 0.48
    ROW_H = 0.44
    GRID_IN = ROW_H * len(ERRS)
    AXIS_IN, FOOT_IN, BOT_IN = 0.40, 0.50, 0.24
    H = TOP_IN + KEY_IN + HEAD_IN + GRID_IN + AXIS_IN + FOOT_IN + BOT_IN
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 4b",
        "The July 11 share stays higher than July 9's only if the recorded times are good to a few minutes.",
        gap=TOP_IN,
    )

    ky = iy(TOP_IN + 0.14)
    for x, colour, lab in ((LEFT, S.ATTACK_RAMP[0], f"the July 9 cohort, {n9} agents"),
                           (0.240, S.ATTACK_RAMP[3], f"the July 11 cohort, {n11} agents")):
        fig.add_artist(Rectangle((x, ky - 0.008), 0.014, 0.016, color=colour,
                                 transform=fig.transFigure))
        fig.text(x + 0.019, ky, lab, fontsize=7.4, color=S.INK_2, va="center")
    fig.add_artist(Rectangle((0.470, ky - 0.008), 0.014, 0.016,
                             transform=fig.transFigure,
                             **S.unresolved({"linewidth": 0.6})))
    fig.text(0.489, ky, "the two ranges overlap here, so neither cohort can be put ahead "
             "of the other", fontsize=7.4, color=S.INK_2, va="center")

    cw = (RIGHT - LEFT - LBL_B - COL_GAP * (len(HORIZONS) - 1)) / len(HORIZONS)
    y0f = iy(TOP_IN + KEY_IN + HEAD_IN + GRID_IN)

    for ci, (hz, hlab, note) in enumerate(HORIZONS):
        x0 = LEFT + LBL_B + ci * (cw + COL_GAP)
        ax = fig.add_axes([x0, y0f, cw, ih(GRID_IN)])
        ax.set_facecolor("none")
        ax.set_xlim(0, 1.0)
        ax.set_ylim(len(ERRS), 0)
        ax.set_yticks([])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(S.RULE)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["0", "25%", "50%", "75%", "100%"])
        ax.tick_params(axis="x", labelsize=7.0, length=2, pad=1.5)
        fig.text(x0, y0f + ih(GRID_IN) + ih(0.26), hlab, fontsize=8.6,
                 weight="demibold", color=S.INK, va="bottom")
        if note:
            fig.text(x0, y0f + ih(GRID_IN) + ih(0.09), note, fontsize=7.2,
                     color=S.INK_2, va="bottom")

        for ri, (err, _) in enumerate(ERRS):
            l9, u9 = cell[(hz, err, 9)]
            l11, u11 = cell[(hz, err, 11)]
            ax.add_patch(Rectangle((0, ri + 0.06), 1.0, 0.88,
                                   facecolor=S.SURFACE_SUNK, lw=0, zorder=0))
            for v in (0.25, 0.5, 0.75):
                ax.plot([v, v], [ri + 0.06, ri + 0.94], color=S.SURFACE, lw=0.7, zorder=1)
            lo, hi = max(l9, l11), min(u9, u11)
            if hi > lo:
                ax.add_patch(Rectangle((lo, ri + 0.06), hi - lo, 0.88, zorder=2,
                                       **S.unresolved({"linewidth": 0.6})))
            for (lo_v, hi_v, colour, yb) in ((l9, u9, S.ATTACK_RAMP[0], ri + 0.22),
                                             (l11, u11, S.ATTACK_RAMP[3], ri + 0.56)):
                ax.add_patch(Rectangle((lo_v, yb), max(hi_v - lo_v, 0.004), 0.22,
                                       facecolor=colour, lw=0, zorder=3))
            if ci == 0:  # the column the published claim is made in
                for lo_v, hi_v, yb in ((l9, u9, ri + 0.33), (l11, u11, ri + 0.67)):
                    ax.annotate(f"{lo_v:.1%} to {hi_v:.1%}", xy=(hi_v, yb),
                                xytext=(5, 0), textcoords="offset points", fontsize=7.0,
                                color=S.INK_2, ha="left", va="center", zorder=6,
                                path_effects=S.halo(2.8))

    # The row dimension, labelled once on the left.
    fig.text(LEFT, y0f + ih(GRID_IN) + ih(0.09), "how far each recorded time\ncould be off",
             fontsize=7.6, color=S.INK_2, va="bottom", linespacing=1.4)
    for ri, (err, elab) in enumerate(ERRS):
        yc = y0f + ih(GRID_IN) * (1 - (ri + 0.5) / len(ERRS))
        fig.text(LEFT + LBL_B - 0.014, yc, elab, fontsize=8.4, weight="demibold",
                 color=S.INK, ha="right", va="center")

    fig.text(LEFT + LBL_B + (RIGHT - LEFT - LBL_B) / 2, iy(H - BOT_IN - FOOT_IN - 0.10),
             "share of the cohort that joined, as a range the recorded times allow",
             fontsize=7.8, color=S.INK_2, ha="center", va="bottom")

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN + 0.10),
        "Even with the times taken as recorded the two ranges have width, because a timeline that ended "
        "before the time was up cannot be counted either way.\nAt thirty minutes of error both ranges "
        "start at zero in the one hour column, so the recorded times can no longer put either cohort ahead of the "
        "other.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig04b_erosion.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 4c -- what population reaches the level the report states
# --------------------------------------------------------------------------

W0 = pd.Timestamp("2026-07-11T06:00:00Z")  # the six hours Figures 2a and 2b use
THRESHOLDS = [1, 2, 4, 6, 8, 12, 24]
FOOTNOTE_T = 4  # the threshold the report's own footnote states
ROWS_C = 22  # every block is this tall, so a fill height reads as a share
GAP_C = 3.6  # blank squares between blocks
PAD_C = 3.4  # blank squares at the right, for the 90% label
CELL = 0.78  # square side, as a fraction of the pitch


def build_denominator(dpi=DPI):
    ag = data.agents()

    blocks = []
    for T in THRESHOLDS:
        pop = ag[(ag["read_utc"] <= W0 - pd.Timedelta(hours=T)) & (ag["end_utc"] > W0)]
        n = len(pop)
        k = int(pop["hfStart_utc"].notna().sum())
        blocks.append(dict(T=T, n=n, k=k, cols=int(np.ceil(n / ROWS_C))))

    cols_total = sum(b["cols"] for b in blocks) + GAP_C * (len(blocks) - 1) + PAD_C
    pitch = (RIGHT - LEFT) * W / cols_total
    blk_in = ROWS_C * pitch

    TOP_IN, KEY_IN, ABOVE_IN = 0.70, 0.28, 0.50
    DIM_IN, LBL_IN, NOTE_IN, BELOW_IN = 0.24, 0.50, 0.74, 1.14
    FOOT_IN, BOT_IN = 0.46, 0.24
    H = TOP_IN + KEY_IN + ABOVE_IN + blk_in + BELOW_IN + FOOT_IN + BOT_IN
    base = TOP_IN + KEY_IN + ABOVE_IN + blk_in  # inches down to the block bottom
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 4c",
        "The recovered file reaches only 82.5% at the four hour threshold the report used.",
        gap=TOP_IN,
    )

    ky = iy(TOP_IN + 0.11)
    fig.text(LEFT, ky, "Every square is one agent.", fontsize=7.4, color=S.INK_2,
             va="center")
    for x, filled, lab in ((0.180, True, "it joined the attack"),
                           (0.330, False, "no attack is recorded for it")):
        fig.add_artist(Rectangle((x, ky - 0.007), 0.013, 0.014,
                                 facecolor=S.ATTACK if filled else "none",
                                 edgecolor="none" if filled else S.NEUTRAL, linewidth=0.6,
                                 transform=fig.transFigure))
        fig.text(x + 0.018, ky, lab, fontsize=7.4, color=S.INK_2, va="center")

    ax = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + ABOVE_IN + blk_in), RIGHT - LEFT,
                       ih(blk_in)])
    ax.set_facecolor("none")
    S.strip_axes(ax)
    ax.set_xlim(0, cols_total)
    ax.set_ylim(0, ROWS_C)

    x0 = 0.0
    for b in blocks:
        n, k, cols = b["n"], b["k"], b["cols"]
        for j in range(n):  # fill from the bottom row upward
            col, rw = j % cols, j // cols
            ax.add_patch(Rectangle((x0 + col, rw), CELL, CELL,
                                   facecolor=S.ATTACK if j < k else "none",
                                   edgecolor="none" if j < k else S.NEUTRAL,
                                   linewidth=0.55))
        # Each block is a slightly different number of rows tall, so its own 90%
        # is its own height times nine tenths.
        y90 = 0.90 * n / cols
        ax.plot([x0 - 0.4, x0 + cols - 0.2], [y90, y90], color=S.INK, lw=0.9,
                ls=(0, (2.6, 2.0)), zorder=5)
        if b["T"] == THRESHOLDS[-1]:
            ax.annotate("90%", xy=(x0 + cols - 0.2, y90), xytext=(4, 0),
                        textcoords="offset points", fontsize=8.0, weight="demibold",
                        color=S.INK, ha="left", va="center", annotation_clip=False,
                        zorder=6)

        lx = LEFT + x0 * pitch / W
        fig.text(lx, iy(TOP_IN + KEY_IN + ABOVE_IN - 0.28), f"{k / n:.1%}", fontsize=12.5,
                 weight="demibold", color=S.ATTACK, va="bottom")
        fig.text(lx, iy(TOP_IN + KEY_IN + ABOVE_IN - 0.04), f"{k} of {n}", fontsize=7.2,
                 color=S.INK_2, va="bottom")
        fig.text(lx, iy(base + LBL_IN), f"{b['T']} h or more", fontsize=8.4,
                 weight="demibold", color=S.INK, va="top")
        if b["T"] == FOOTNOTE_T:
            yr = iy(base + 0.07)
            fig.add_artist(plt.Line2D([lx, lx + cols * pitch / W], [yr, yr], color=S.INK,
                                      lw=1.3, transform=fig.transFigure))
            fig.text(lx, iy(base + NOTE_IN), "the threshold the\nreport's footnote states",
                     fontsize=6.9, color=S.INK_2, va="top", linespacing=1.45)
        x0 += cols + GAP_C

    fig.text(LEFT, iy(base + DIM_IN),
             "how long the agent had already been reading the board at 06:00 on July 11",
             fontsize=7.6, color=S.INK_2, va="top")

    fig.text(
        LEFT, iy(base + BELOW_IN),
        "Each block holds every agent that was still running at 06:00 on July 11 and had first read the board "
        "at least that long before. The 24 hour share is 206 of 229, which is 89.96%.\nCounting every agent "
        "that had read the board by then, rather than only the ones still running, puts all seven shares "
        "between 45% and 48% instead, so the choice of population decides the answer.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig04c_denominator.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


def build():
    build_cohorts()
    build_erosion()
    build_denominator()


if __name__ == "__main__":
    build()
