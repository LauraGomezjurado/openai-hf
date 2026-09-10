"""Figure 5: two forecast gates, and what the models were fed.

  fig05a_hourly.png    the 96 held-out hours: recorded onsets against four forecasts
  fig05b_hazard.png    the eight held-out blocks: predicted chance against observed rate
  fig05c_coverage.png  the 144 declared hours of the message table, and the 28 with no rows

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
from fig01_recovery import top_block  # noqa: E402

S.apply()

W = 10.6
LEFT, RIGHT = 0.052, 0.982
DPI = 200

# Both gates are scored over the same four days. Hour 0 is 2026-07-08 00:00 UTC,
# the epoch the message table declares; the agent file's epoch is two days earlier.
TRAFFIC_EPOCH = pd.Timestamp("2026-07-08T00:00:00Z")
AGENT_EPOCH = pd.Timestamp("2026-07-06T00:00:00Z")
X0, X1 = 48, 144
DAYS = [(48, "July 10"), (72, "July 11"), (96, "July 12"), (120, "July 13")]

CH = 0.00465  # figure width of one character at 7.4 pt
SETTING = "1h_exclude0_shift0"
MODELS = [
    ("volume_baseline", S.OURS, (0, (3.2, 2.0)), 1.35),
    ("plus_composition", S.OURS, "solid", 1.35),
    ("persistence", S.INK, "solid", 1.0),
    ("training_mean", S.INK_3, (0, (1.8, 1.8)), 1.1),
]


def day_axis(ax, ymax, label_y=None, labels=True, span=None, days=None):
    """Day boundaries as rules, day names centred in each day."""
    x0, x1 = span or (X0, X1)
    for h in range(x0, x1 + 1, 6):
        ax.axvline(h, color=S.RULE, lw=0.5, zorder=0)
    for h in range(x0, x1 + 1, 24):
        ax.axvline(h, color=S.RULE, lw=1.0, zorder=0)
    if labels:
        for h, name in (days or DAYS):
            ax.text(h + 12, label_y if label_y is not None else -ymax * 0.045, name,
                    fontsize=8.2, color=S.INK_2, ha="center", va="top",
                    weight="demibold")
    ax.set_xlim(x0, x1)


def key_rows(fig, rows):
    """Grouped legend rows: a lead-in sentence, then its line samples."""
    for yy, lead, items in rows:
        fig.text(LEFT, yy, lead, fontsize=7.4, color=S.INK_3, va="center")
        cx = LEFT + len(lead) * CH + 0.020
        for lab, colour, ls in items:
            fig.add_artist(plt.Line2D([cx, cx + 0.024], [yy, yy], color=colour, lw=1.4,
                                      ls=ls, transform=fig.transFigure))
            fig.text(cx + 0.030, yy, lab, fontsize=7.4, color=S.INK_2, va="center")
            cx += 0.030 + len(lab) * CH + 0.024


# --------------------------------------------------------------------------
# fig 5a -- the hourly count gate
# --------------------------------------------------------------------------


def build_hourly(dpi=DPI):
    p = data.workstream_predictions()
    p = p[p["setting"] == SETTING]
    pred = p.pivot_table(index="target_start_hour", columns="model", values="prediction")
    act = p.groupby("target_start_hour")["actual"].first()
    sc = data.workstream_forecast_scores()
    sc = sc[sc["setting"] == SETTING].set_index("model")
    x = act.index.to_numpy() + 0.5

    TOP_IN, KEY_IN, PLOT_IN = 0.70, 0.58, 3.00
    AXIS_IN, FOOT_IN, BOT_IN = 0.44, 0.46, 0.22
    H = TOP_IN + KEY_IN + PLOT_IN + AXIS_IN + FOOT_IN + BOT_IN
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 5a",
        "Both fitted models made their largest prediction in an hour when three agents joined.",
        gap=TOP_IN,
    )

    # ---- key, grouped so that the two kinds of forecast read as two kinds ----
    ky = iy(TOP_IN + 0.10)
    fig.add_artist(Rectangle((LEFT, ky - 0.010), 0.010, 0.020, color=S.ATTACK,
                             transform=fig.transFigure))
    fig.text(LEFT + 0.015, ky, "the agents that joined, per hour", fontsize=7.4,
             color=S.INK_2, va="center")

    rows = [
        (iy(TOP_IN + 0.28), "what we fitted on the message counts:",
         [("volume and calendar", S.OURS, (0, (3.2, 2.0))),
          ("with message composition added", S.OURS, "solid")]),
        (iy(TOP_IN + 0.44), "what needs no fitting at all:",
         [("the previous hour's count", S.INK, "solid"),
          ("the average of the training hours", S.INK_3, (0, (1.4, 1.6)))]),
    ]
    key_rows(fig, rows)

    ax = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN), RIGHT - LEFT, ih(PLOT_IN)])
    ymax = 340
    ax.set_ylim(0, ymax)
    day_axis(ax, ymax)
    ax.set_yticks([0, 100, 200, 300])
    ax.tick_params(axis="y", labelsize=7.4, length=2, pad=1.5)
    ax.set_xticks([])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(S.RULE)
    ax.spines["bottom"].set_color(S.RULE)
    ax.grid(axis="y", lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("agents joining per hour, recorded and predicted", fontsize=7.8,
                  color=S.INK_2, labelpad=4)

    ax.bar(x, act.to_numpy(), width=0.92, color=S.ATTACK, linewidth=0, zorder=3)
    for name, colour, ls, lw in MODELS:
        ax.plot(x, pred[name].to_numpy(), color=colour, lw=lw, ls=ls, zorder=4,
                solid_capstyle="round")

    hpk = int(pred["plus_composition"].idxmax())
    apk = int(act.idxmax())
    ax.annotate(
        "Both fitted models made their largest prediction of the four days here:\n"
        f"{pred['volume_baseline'][hpk]:.0f} agents on volume and calendar, "
        f"{pred['plus_composition'][hpk]:.0f} with composition added.\n"
        f"Three agents joined in this hour.",
        xy=(hpk + 0.5, pred["plus_composition"][hpk]), xytext=(hpk + 8, 328),
        fontsize=7.4, color=S.INK, ha="left", va="top", linespacing=1.55,
        path_effects=S.halo(2.6), zorder=8,
        arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=4, shrinkB=3),
    )
    ax.annotate(
        f"{act[apk]} agents joined in this hour, more than in any other hour of the "
        f"incident.\nThe fitted models gave it {pred['volume_baseline'][apk]:.0f} and "
        f"{pred['plus_composition'][apk]:.0f}.",
        xy=(apk + 0.5, act[apk] + 3), xytext=(apk + 0.5, 205), fontsize=7.4,
        color=S.INK, ha="center", va="top", linespacing=1.55,
        path_effects=S.halo(2.6), zorder=8,
        arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=4, shrinkB=3),
    )
    ax.text(apk + 2.6, act[apk] - 6, "the previous hour's count peaks one hour late", fontsize=7.2, weight="demibold",
            color=S.INK, ha="left", va="bottom", path_effects=S.halo(2.6), zorder=8)
    # the distance between the two peaks, measured in the plot itself
    ax.annotate("", xy=(apk + 0.5, 238), xytext=(hpk + 0.5, 238), zorder=7,
                arrowprops=dict(arrowstyle="|-|,widthA=0.28,widthB=0.28", color=S.INK_3,
                                lw=0.8, shrinkA=0, shrinkB=0))
    ax.text((hpk + apk) / 2 + 0.5, 244,
            f"The fitted models' peak came {apk - hpk} hours before the real one.",
            fontsize=7.4, color=S.INK, ha="center", va="bottom",
            path_effects=S.halo(2.6), zorder=8)
    ax.annotate(
        "the average of the training hours",
        xy=(136, pred["training_mean"][135]), xytext=(124, 30), fontsize=7.4,
        color=S.INK_2, ha="left", va="bottom", path_effects=S.halo(2.6), zorder=8,
        arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=3, shrinkB=2),
    )

    mae = {m: sc.loc[m, "mae"] for m in sc.index}
    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN),
        "Average error per hour over these 96 hours: {:.2f} agents for the previous "
        "hour's count, {:.2f} for the training average, {:.2f} for volume and calendar, "
        "{:.2f} with composition added.\nRepeating the previous hour had the lowest "
        "error and the lowest deviance in all 30 binning and shift settings we tried, "
        "and composition improved on volume in 12 of the 30 by error and in 2 by "
        "deviance.".format(
            mae["persistence"], mae["training_mean"], mae["volume_baseline"],
            mae["plus_composition"]),
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig05a_hourly.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 5b -- the per-agent hazard gate
# --------------------------------------------------------------------------

FITTED = [("plus_board_tenure", "solid"), ("calendar_run_age", (0, (3.2, 2.0)))]


def build_hazard(dpi=DPI):
    p = data.read_anchored_predictions()
    # The agent file's epoch is two days before the message table's; put both gates
    # on the same clock.
    p["h"] = p["cutoff"] - 48
    g = p.groupby(["h", "model"]).agg(n=("outcome", "size"), pos=("outcome", "sum"),
                                     mean_p=("probability", "mean")).reset_index()
    obs = g[g["model"] == "training_mean"].set_index("h")
    rate = (obs["pos"] / obs["n"]).rename("rate")
    mean_p = g.pivot(index="h", columns="model", values="mean_p")
    sc = data.read_anchored_scores().query("scope == 'all'").set_index("model")
    un = data.read_anchored_scores().query("scope == 'unseen_rows'").set_index("model")
    hs = mean_p.index.to_numpy()

    TOP_IN, KEY_IN, PLOT_IN = 0.70, 0.58, 2.45
    GAP_IN, STRIP_IN, AXIS_IN = 0.20, 0.42, 0.40
    FOOT_IN, BOT_IN = 0.46, 0.22
    H = (TOP_IN + KEY_IN + PLOT_IN + GAP_IN + STRIP_IN + AXIS_IN + FOOT_IN + BOT_IN)
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 5b",
        "Both fitted models gave their lowest chance to the twelve hours that produced 389 of the 571 onsets.",
        gap=TOP_IN,
    )

    # ---- key ----
    ky = iy(TOP_IN + 0.10)
    fig.add_artist(Rectangle((LEFT, ky - 0.009), 0.024, 0.017, facecolor=S.ATTACK_T,
                             lw=0, transform=fig.transFigure))
    fig.add_artist(plt.Line2D([LEFT, LEFT + 0.024], [ky + 0.008, ky + 0.008],
                              color=S.ATTACK, lw=1.9, transform=fig.transFigure))
    fig.text(LEFT + 0.030, ky, "the share of the block's agent hours that ended in an "
             "onset", fontsize=7.4, color=S.INK_2, va="center")
    key_rows(fig, [
        (iy(TOP_IN + 0.28), "what we fitted on the agent timelines:",
         [("calendar and run age", S.OURS, (0, (3.2, 2.0))),
          ("with board reading time added", S.OURS, "solid")]),
        (iy(TOP_IN + 0.44), "what needs no fitting at all:",
         [("the training base rate", S.INK_3, (0, (1.4, 1.6)))]),
    ])

    # ---- the rates ----
    ax = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN), RIGHT - LEFT, ih(PLOT_IN)])
    ymax = 0.64
    ax.set_ylim(0, ymax)
    day_axis(ax, ymax, labels=False)
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.set_yticklabels(["0", "20%", "40%", "60%"])
    ax.tick_params(axis="y", labelsize=7.4, length=2, pad=1.5)
    ax.set_xticks([])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(S.RULE)
    ax.spines["bottom"].set_color(S.RULE)
    ax.grid(axis="y", lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("chance that an agent joins in its next hour", fontsize=7.8,
                  color=S.INK_2, labelpad=4)

    def step(v, target=None, **kw):
        """One flat segment per twelve hour block, joined at the boundaries."""
        xs, ys = [], []
        for h in hs:
            xs += [h, h + 12]
            ys += [v[h], v[h]]
        (target or ax).plot(xs, ys, solid_capstyle="butt", **kw)

    for h in hs:
        ax.add_patch(Rectangle((h, 0), 12, rate[h], facecolor=S.ATTACK_T, lw=0,
                               zorder=2))
    step(rate, color=S.ATTACK, lw=1.9, zorder=3)
    step(mean_p["training_mean"], color=S.INK_3, lw=1.0, ls=(0, (1.4, 1.6)), zorder=4)
    for name, ls in FITTED:
        step(mean_p[name], color=S.OURS, lw=1.35, ls=ls, zorder=5,
             path_effects=S.halo(3.4))

    # ---- the gap the gate is about, measured at the block that holds the surge ----
    surge = int(hs[np.argmin(mean_p["plus_board_tenure"].to_numpy())])
    gx = surge + 6
    lo, hi = mean_p.loc[surge, "plus_board_tenure"], rate[surge]
    ax.annotate("", xy=(gx, hi), xytext=(gx, lo), zorder=7,
                arrowprops=dict(arrowstyle="|-|,widthA=0.28,widthB=0.28", color=S.INK,
                                lw=0.9, shrinkA=0, shrinkB=0))
    ax.annotate(
        f"{int(obs.loc[surge, 'pos'])} of the 571 onsets fall in these twelve hours, "
        f"and they are {rate[surge]:.1%} of the block's agent hours.\nBoth fitted models "
        f"averaged a {lo:.1%} chance across these hours, the lowest they averaged anywhere.",
        xy=(gx, hi), xytext=(gx, 0.50), fontsize=7.4, color=S.INK,
        ha="center", va="top", linespacing=1.55, path_effects=S.halo(2.6), zorder=8,
        arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=4, shrinkB=1),
    )
    last = int(hs[-1])
    tail = mean_p.loc[hs[-2:], [m for m, _ in FITTED]].to_numpy()
    ax.annotate(
        "No agent joined in the last 24 hours, and the two fitted models\n"
        f"averaged between {tail.min():.0%} and {tail.max():.0%} across those hours.",
        xy=(last + 1.5, mean_p.loc[last, "plus_board_tenure"]), xytext=(99, 0.63),
        fontsize=7.4, color=S.INK, ha="left", va="top", linespacing=1.55,
        path_effects=S.halo(2.6), zorder=8,
        arrowprops=dict(arrowstyle="-", color=S.INK_3, lw=0.7, shrinkA=4, shrinkB=3),
    )

    # ---- how much each block weighs ----
    nmax = 5200
    axn = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN + GAP_IN + STRIP_IN),
                        RIGHT - LEFT, ih(STRIP_IN)])
    axn.set_ylim(0, nmax)
    day_axis(axn, nmax, label_y=-380)
    axn.set_yticks([])
    axn.set_xticks([])
    for side in ("top", "right", "left"):
        axn.spines[side].set_visible(False)
    axn.spines["bottom"].set_color(S.RULE)
    axn.set_ylabel("agent hours\nin the block", fontsize=7.0, color=S.INK_2,
                   labelpad=6, linespacing=1.35)
    for h in hs:
        n = int(obs.loc[h, "n"])
        axn.add_patch(Rectangle((h + 0.35, 0), 11.3, n, facecolor=S.INK_3, lw=0,
                                zorder=2))
        axn.text(h + 6, n + 240, f"{n:,}", fontsize=6.8, color=S.INK_2, ha="center",
                 va="bottom")

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN),
        "Squared error per agent hour over all {:,} intervals: {:.4f} for the base rate, "
        "{:.4f} for calendar and run age, {:.4f} with board reading time added. The base "
        "rate scored better in 6 of the 8 blocks.\nOn the {:,} intervals from agents the "
        "fit had never seen before, adding board reading time made the error worse than "
        "leaving it out, {:.4f} against {:.4f}.".format(
            int(sc.loc["training_mean", "intervals"]), sc.loc["training_mean", "brier"],
            sc.loc["calendar_run_age", "brier"], sc.loc["plus_board_tenure", "brier"],
            int(un.loc["training_mean", "intervals"]),
            un.loc["plus_board_tenure", "brier"], un.loc["calendar_run_age", "brier"]),
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig05b_hazard.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


# --------------------------------------------------------------------------
# fig 5c -- what the message table actually covers, and what we fed the models
# --------------------------------------------------------------------------

ALL_DAYS = [(0, "July 8"), (24, "July 9"), (48, "July 10"), (72, "July 11"),
            (96, "July 12"), (120, "July 13")]
FILL = 0.0  # the value our grid holds for an hour the table does not cover


def runs(flag):
    """Contiguous runs of True as (start, stop) hour pairs."""
    out, i = [], 0
    while i < len(flag):
        if flag[i]:
            j = i
            while j + 1 < len(flag) and flag[j + 1]:
                j += 1
            out.append((i, j + 1))
            i = j + 1
        else:
            i += 1
    return out


def build_coverage(dpi=DPI):
    ws = data.workstreams()
    hourly = ws.groupby("hour_utc")["count"].sum()
    total = np.full(144, np.nan)
    for t, v in hourly.items():
        total[int((t - TRAFFIC_EPOCH).total_seconds() // 3600)] = v
    absent = np.isnan(total)
    gaps = runs(absent)
    floor = int(np.nanmin(total))

    TOP_IN, KEY_IN, PLOT_IN = 0.70, 0.30, 2.60
    AXIS_IN, BRACK_IN, FOOT_IN, BOT_IN = 0.34, 0.50, 0.46, 0.22
    H = TOP_IN + KEY_IN + PLOT_IN + AXIS_IN + BRACK_IN + FOOT_IN + BOT_IN
    fig = plt.figure(figsize=(W, H))

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    top_block(
        fig, H, "Figure 5c",
        "Twenty-eight hours carry zero messages in our grid, a count the table never reports.",
        gap=TOP_IN,
    )

    # ---- key ----
    ky = iy(TOP_IN + 0.10)
    cx = LEFT
    for kind, lab in (("line", "the messages the table counts in the hour"),
                      ("fill", "the value our forecast grid used instead"),
                      ("gap", "the table holds no row for this hour")):
        if kind == "gap":
            fig.add_artist(Rectangle((cx, ky - 0.010), 0.022, 0.020,
                                     transform=fig.transFigure,
                                     **S.unresolved({"linewidth": 0.6}, color=S.RULE)))
        else:
            colour = S.NEUTRAL if kind == "line" else S.OURS
            fig.add_artist(plt.Line2D([cx, cx + 0.022], [ky, ky], color=colour,
                                      lw=1.6 if kind == "line" else 2.6,
                                      solid_capstyle="butt",
                                      transform=fig.transFigure))
        fig.text(cx + 0.028, ky, lab, fontsize=7.4, color=S.INK_2, va="center")
        cx += 0.028 + len(lab) * CH + 0.026

    # ---- the counts, and the zeros we put where there were none ----
    ax = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN), RIGHT - LEFT, ih(PLOT_IN)])
    ymax = 4200
    ax.set_yscale("symlog", linthresh=1, linscale=0.4)
    ax.set_ylim(0, ymax)
    day_axis(ax, ymax, labels=False, span=(0, 144))
    ax.set_yticks([0, 1, 10, 100, 1000])
    ax.set_yticklabels(["0", "1", "10", "100", "1,000"])
    ax.tick_params(axis="y", labelsize=7.4, length=2, pad=1.5, which="major")
    ax.tick_params(axis="y", which="minor", length=0)
    ax.set_xticks([])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(S.RULE)
    ax.spines["bottom"].set_color(S.RULE)
    ax.grid(axis="y", lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("messages the table counts in the hour, on a log scale", fontsize=7.8,
                  color=S.INK_2, labelpad=4)

    for a, b in gaps:
        ax.add_patch(Rectangle((a, 0), b - a, ymax, zorder=1,
                               **S.unresolved({"linewidth": 0.55}, color=S.RULE)))
        ax.plot([a, b], [FILL, FILL], color=S.OURS, lw=2.6, solid_capstyle="butt",
                clip_on=False, zorder=6)
    ax.plot(np.arange(144) + 0.5, total, color=S.NEUTRAL, lw=1.6, zorder=4,
            solid_capstyle="round")
    ax.axhline(floor, color=S.INK_3, lw=0.8, ls=(0, (1.4, 1.6)), zorder=3)
    ax.text(94, floor + 0.5, f"the fewest the table ever counts in an hour is {floor}",
            fontsize=7.4, color=S.INK_2, ha="left", va="bottom",
            path_effects=S.halo(2.6), zorder=8)

    ax.text(1, 3900, "The table has no row for the first 18 hours it declares.\n"
            "Our grid gave every model 18 zeros to start from.",
            fontsize=7.4, color=S.INK, ha="left", va="top", linespacing=1.55,
            path_effects=S.halo(2.6), zorder=8)
    ax.text(143, 2600, "the table's rows stop eight hours\nbefore its last declared hour",
            fontsize=7.4, color=S.INK, ha="right", va="top", linespacing=1.55,
            path_effects=S.halo(2.6), zorder=8)
    mid = [a for a, b in gaps if 18 < a < 130]
    body = (
        "Two hours in the middle have no row either. Around the first the table counts "
        f"{int(total[mid[0] - 1])}\nmessages and then {int(total[mid[0] + 1])}, and around the second it counts "
        f"{int(total[mid[1] - 1])} and then {int(total[mid[1] + 1])}."
    )
    ax.text(sum(mid) / 2, 150, body, fontsize=7.4, color=S.INK, ha="center", va="top",
            linespacing=1.55, path_effects=S.halo(2.6), zorder=8)
    for h in mid:
        # a stem inside the missing hour, from above the floor label up to the text
        ax.plot([h + 0.5, h + 0.5], [6, 30], color=S.INK_3, lw=0.7, ls=(0, (1.4, 1.6)),
                zorder=7)

    # ---- day names, then what each half of the clock was used for ----
    axd = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN + AXIS_IN), RIGHT - LEFT,
                        ih(AXIS_IN)])
    axd.set_ylim(0, 1)
    S.strip_axes(axd)
    day_axis(axd, 1, label_y=0.92, span=(0, 144), days=ALL_DAYS)

    axb = fig.add_axes([LEFT, iy(TOP_IN + KEY_IN + PLOT_IN + AXIS_IN + BRACK_IN),
                        RIGHT - LEFT, ih(BRACK_IN)])
    axb.set_ylim(0, 1)
    axb.set_xlim(0, 144)
    S.strip_axes(axb)
    n_lo = int(absent[:48].sum())
    n_hi = int(absent[48:].sum())
    for (a, b), lab in (((0, 48), f"the first fit learned from these hours, and {n_lo} "
                                  "have no row"),
                        ((48, 144), f"the models were scored on these hours, and {n_hi} "
                                    "have no row")):
        axb.annotate("", xy=(b - 0.4, 0.86), xytext=(a + 0.4, 0.86),
                     arrowprops=dict(arrowstyle="|-|,widthA=0.28,widthB=0.28",
                                     color=S.INK_3, lw=0.8, shrinkA=0, shrinkB=0))
        axb.text((a + b) / 2, 0.60, lab, fontsize=7.4, color=S.INK_2, ha="center",
                 va="top")

    fig.text(
        LEFT, iy(H - BOT_IN - FOOT_IN),
        "The table declares 144 hours and holds rows for 116 of them. Our grid is a 144 "
        "hour array of zeros that the rows are written into, so the 28 hours with no row "
        "entered every model as an hour with no traffic.\nThe forecast that beat both "
        "fitted models never read this table at all, because the previous hour's onset "
        "count comes from the agent file instead.",
        fontsize=7.2, color=S.INK_3, va="top", linespacing=1.6,
    )

    out = data.ensure_out() / "fig05c_coverage.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out)


def build():
    build_hourly()
    build_hazard()
    build_coverage()


if __name__ == "__main__":
    build()
