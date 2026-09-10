"""Figure 1c. The sentence ladder across four domains and two checkpoints.

Same four prompts as Figure 1b, run in four unrelated task domains, on two
checkpoints. Each cell is one recorded rollout: the credits the executor spent,
in the order it spent them, and the action the model emitted.

Domains carry different budgets because their own packages take a different
number of steps, so the bars are different lengths on purpose.
"""

from __future__ import annotations

import p2common as P

ORDER = ["none", "request", "assertion", "priority"]
# The rung names are the ones Figure 1b uses, so the two panels read as one story.
LABEL = {r["key"]: r["label"] for r in P.LADDER}
MODELS = [("qwen3", "Qwen3 8B"), ("llama31_8b", "Llama 3.1 8B")]

# ------------------------------------------------------------------ geometry
#
# The grid is sized from the widest thing in it rather than from round numbers.
# The label gutter is as wide as the longest rung label, so no label wraps, and
# the credit slots are then as wide as the leftover column allows, so the bars
# carry the width instead of floating in the middle of an oversized cell.

LAB_SIZE = 7.4
RUNG_W = 0.42                               # the "rung N" marker
LAB_W = max(P.text_w(s, LAB_SIZE, weight="demibold") for s in LABEL.values())
GUT = RUNG_W + LAB_W + 0.20
TALLY = 0.66                                # the count of forgone own packages
CW = (P.X1 - P.X0 - GUT - TALLY) / 4        # one domain column
MAX_CREDITS = 5                             # triage and access
SLOT_GAP = 0.028
SLOT_W = (CW - 0.24 + SLOT_GAP) / MAX_CREDITS - SLOT_GAP
SLOT_H = 0.245

ROW_IN = 0.50
GHEAD_IN = 0.26
GGAP_IN = 0.16

TOP_IN = 0.74
COLHEAD_IN = 0.44
KEY_IN = 0.44
FOOT_IN = 0.56
BOT_IN = 0.14
H = (TOP_IN + COLHEAD_IN + 2 * (GHEAD_IN + 4 * ROW_IN) + GGAP_IN + KEY_IN
     + FOOT_IN + BOT_IN)


def cell(fig, x, y, row):
    """One rollout: the spend, and the action the model emitted."""
    if row is None:
        # Hatch draws in the edge colour, so an edge of "none" is an empty slab.
        bw = MAX_CREDITS * (SLOT_W + SLOT_GAP) - SLOT_GAP
        P.card(fig, H, x + (CW - bw) / 2, y, bw, SLOT_H, face=P.SPARE_T,
               edge=P.SPARE, hatch=P.S.HATCH, lw=0.0, zorder=3)
        P.text(fig, H, x + CW / 2, y + SLOT_H + 0.135,
               "not in the records", size=6.4, color=P.INK_3, ha="center",
               va="baseline")
        return
    ops = P.spend(row)
    total = P.budget_of(row)
    bw = total * (SLOT_W + SLOT_GAP) - SLOT_GAP
    bx = x + (CW - bw) / 2
    for i in range(total):
        xi = bx + i * (SLOT_W + SLOT_GAP)
        if i < len(ops):
            _, own = ops[i]
            P.card(fig, H, xi, y, SLOT_W, SLOT_H,
                   face=P.PRINCIPAL if own else P.PEER, edge="none", zorder=4)
        else:
            P.card(fig, H, xi, y, SLOT_W, SLOT_H, face=P.SURFACE, edge=P.INK_3,
                   lw=0.7, ls=(0, (1.7, 1.4)), zorder=4)
    forgone = row["outcome"]["own_output_forgone_for_peer"]
    P.text(fig, H, x + CW / 2, y + SLOT_H + 0.135, row["decision"], size=6.6,
           family=P.MONO, ha="center", va="baseline",
           color=P.UNMET if forgone else P.INK_2,
           weight="demibold" if forgone else "normal")


def build():
    per = {m: {r["key"]: r for r in P.ladder(m)} for m, _ in MODELS}
    budgets = {}
    for m in per:
        for r in per[m].values():
            for d, row in r["runs"].items():
                budgets.setdefault(d, P.budget_of(row))
                assert budgets[d] == P.budget_of(row), d

    fig, y = P.new(
        H, "Figure 1c",
        "Both checkpoints give up the principal's package once the peer claims "
        "priority.", gap=TOP_IN)

    # ---- domain column headings -----------------------------------------
    P.text(fig, H, P.X0, y, "What the peer says", size=8.4, weight="demibold")
    for j, d in enumerate(P.DOMAINS):
        x = P.X0 + GUT + j * CW
        P.text(fig, H, x + CW / 2, y, d, size=8.4, weight="demibold", ha="center")
        P.text(fig, H, x + CW / 2, y + 0.175, f"{budgets[d]} credits", size=6.4,
               color=P.INK_3, ha="center")
    P.text(fig, H, P.X1, y, "package\nforgone", size=6.6, color=P.UNMET,
           ha="right", weight="demibold", linespacing=1.45)
    P.rule(fig, H, P.X0, y + COLHEAD_IN - 0.11, P.X1 - P.X0, color=P.INK, lw=1.0)
    y += COLHEAD_IN

    for gi, (model, name) in enumerate(MODELS):
        P.text(fig, H, P.X0, y, name, size=9.0, weight="demibold")
        y += GHEAD_IN
        for i, key in enumerate(ORDER):
            rung = per[model].get(key)
            runs = rung["runs"] if rung else {}
            n = sum(r["outcome"]["own_output_forgone_for_peer"]
                    for r in runs.values())

            if n:
                P.card(fig, H, P.X0 - 0.055, y - 0.10, P.X1 - P.X0 + 0.11,
                       ROW_IN - 0.05, face=P.UNMET_T, edge="none", zorder=0)

            mid = y + 0.02 + SLOT_H / 2 + 0.04
            P.text(fig, H, P.X0, mid, f"rung {i}", size=6.4, color=P.INK_3,
                   weight="demibold", va="baseline")
            P.text(fig, H, P.X0 + RUNG_W, mid, LABEL[key], size=LAB_SIZE,
                   color=P.UNMET if n else P.INK, va="baseline",
                   weight="demibold")
            for j, d in enumerate(P.DOMAINS):
                cell(fig, P.X0 + GUT + j * CW, y + 0.02, runs.get(d))
            if runs:
                P.text(fig, H, P.X1, mid, f"{n} of {len(runs)}", size=7.6,
                       ha="right", va="baseline", weight="demibold",
                       color=P.UNMET if n else P.INK_3)
            y += ROW_IN
        if gi == 0:
            P.rule(fig, H, P.X0, y + GGAP_IN / 2, P.X1 - P.X0, color=P.INK,
                   lw=0.9)
            y += GGAP_IN

    # ---- key -------------------------------------------------------------
    P.rule(fig, H, P.X0, y + 0.02, P.X1 - P.X0, color=P.INK, lw=1.0)
    kx = P.X0
    for face, edge, ls, hatch, label in (
            (P.PRINCIPAL, "none", "-", None, "a credit spent on the principal's package"),
            (P.PEER, "none", "-", None, "the credit spent on the peer's audit"),
            (P.SURFACE, P.INK_3, (0, (1.7, 1.4)), None, "a credit never spent"),
            (P.SPARE_T, P.SPARE, "-", P.S.HATCH, "a cell the records do not cover")):
        P.card(fig, H, kx, y + 0.135, 0.155, 0.115, face=face, edge=edge, lw=0.7,
               ls=ls, hatch=hatch, zorder=4)
        P.text(fig, H, kx + 0.215, y + 0.235, label, size=6.4, color=P.INK_2,
               va="baseline")
        kx += 0.215 + P.text_w(label, 6.4) + 0.28

    P.footer(fig, H,
             "One rollout per cell, temperature 0. The action under each bar is "
             "the one the model emitted. Rung 0 was run for Qwen3 only. At rung 2 "
             "Llama declines the peer request and still publishes the "
             "principal's package, which is a different failure from giving the "
             "package up.")
    return P.save(fig, "p2fig01c_ladder.png")


if __name__ == "__main__":
    build()
