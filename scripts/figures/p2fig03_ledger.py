"""Figure 3b. All sixteen recorded contexts, branched three ways each.

Forty eight continuations from `results/escalation/continuations`. Figure 3a took
one context apart. This panel is the whole set, so the reader can see where the
duty clause recovers a missing report and where it produces one that was not
warranted.

The rows are grouped by what the recording already contained at the branch,
because that is what decides whether there is anything to recover. Inside a row
the dashed spine is the branch: everything to its left is the recorded prefix and
everything to its right is what the agent did after it.

Every count, every chip and every quoted report body is read from the records.
Column widths and row heights are derived from that text, so nothing is placed on
a guessed constant.
"""

from __future__ import annotations

import p2common as P

ARMS = [("replay", "nothing is appended"),
        ("task", "one sentence on the task"),
        ("duty", "one sentence on the duty")]

# What a report to the overseer is made of, and the actions that serve the duty.
DUTY_ACTS = ("preserve", "quarantine", "message")

BANDS = [
    dict(key="recover", n=5, want=True,
         head="In these five sessions the artifact was unauthorized and the "
              "agent had sent no report.",
         note="Each of the five reports names the artifact of its own session "
              "and goes to the overseer address of its own session."),
    dict(key="already", n=3, want=True,
         head="In these three sessions the agent had already sent the report "
              "before the branch.",
         note="No arm removes a report that was already sent and no arm sends a "
              "second one."),
    dict(key="benign", n=8, want=False,
         head="In these eight sessions the artifact was authorized and no report "
              "was warranted.",
         note="Both messages come from the two sessions where the agent had "
              "never read the workspace."),
]

TALLY = "sessions that ended with a report to the overseer"

# ------------------------------------------------------------------ geometry

CHIP_SIZE, CHIP_PAD, CHIP_H = 5.9, 0.055, 0.195
GAP = 0.055                                 # between two chips in a chain
LAB_SIZE = 6.1                              # the row label
DESC_SIZE, TALLY_SIZE = 6.4, 7.4
BODY_SIZE, BODY_LEAD = 5.8, 0.130
CGAP = 0.20                                 # breathing room after a column

HEAD_IN = 0.26                              # the band heading
TALLY_IN = 0.28                             # the counted row
NOTE_IN = 0.26
BAND_GAP = 0.26
ROW_GAP = 0.09

TOP_IN, COLHEAD_IN, KEY_IN, FOOT_IN, BOT_IN = 0.74, 0.48, 0.42, 0.70, 0.14


def chip_w(s: str) -> float:
    """What `P.chip` will make this chip, so a chain can be planned."""
    return P.mono_w(s, CHIP_SIZE) + 2 * CHIP_PAD


def chain_w(tools: list[str]) -> float:
    if not tools:
        return 0.0
    return sum(chip_w(t) for t in tools) + GAP * (len(tools) - 1)


def chain(fig, H, x, cy, tools):
    """A run of tool calls, in the order the agent made them."""
    cx = x
    for t in tools:
        duty = t in DUTY_ACTS
        cx += P.chip(fig, H, cx, cy - CHIP_H / 2, t, size=CHIP_SIZE,
                     family=P.MONO, pad=CHIP_PAD, h=CHIP_H,
                     face=P.PRINCIPAL_T if duty else P.SPARE_T,
                     color=P.PRINCIPAL if duty else P.INK_2) + GAP


def build():
    runs = P.continuation_runs()
    srcs = sorted({r["score"]["source"] for r in runs.values()})
    assert len(srcs) == 16, len(srcs)

    # ---- one record per recorded context -----------------------------------
    ctx = {}
    for s in srcs:
        arms = {a: runs[f"{s}-{a}"] for a, _ in ARMS}
        base = arms["replay"]["case"]
        pre = [x["tool"] for x in P.cont_actions(base["messages"])]
        sc = base["source_case"]
        want = sc["evidence"] == "unauthorized"
        had = "message" in pre
        ctx[s] = dict(
            fam=sc["family"], route=sc["route"], want=want, had=had, pre=pre,
            band="recover" if want and not had else
                 "already" if want else "benign",
            label=f"f{sc['family']} r{sc['route']}",
            trace={a: [x["tool"] for x in P.cont_trace(r)]
                   for a, r in arms.items()},
            msg={a: next((x["args"] for x in P.cont_trace(r)
                          if x["tool"] == "message"), None)
                 for a, r in arms.items()},
            receipt={a: r["score"]["receipt"] for a, r in arms.items()},
            new={a: r["score"]["new_receipt"] for a, r in arms.items()},
            addr=sc["address"], art=sc["artifact"])

    # ---- what the panel says about the records is checked here -------------
    for s, c in ctx.items():
        # A report exists at the end when one was there already or one was sent.
        for a, _ in ARMS:
            assert c["receipt"][a] == (c["had"] or c["msg"][a] is not None), (s, a)
            assert c["new"][a] == (c["msg"][a] is not None), (s, a)
            assert c["trace"][a][-1] == "finish", (s, a)
        # Replay is the baseline and the task clause never moves off it.
        assert c["trace"]["task"] == c["trace"]["replay"] == ["finish"], s
        # The prefix shapes the row header draws.
        assert c["pre"][-1] == "submit", (s, c["pre"])
        assert set(c["pre"]) <= {"read_directory", "message", "submit"}, c["pre"]

    bands = {b["key"]: [ctx[s] for s in srcs if ctx[s]["band"] == b["key"]]
             for b in BANDS}
    for b in BANDS:
        rows = bands[b["key"]]
        assert len(rows) == b["n"], (b["key"], len(rows))
        assert all(r["want"] == b["want"] for r in rows), b["key"]
    for r in bands["already"]:
        assert all(not v for v in r["new"].values()), r["label"]
        assert all(r["receipt"].values()), r["label"]
    # Every report names its own artifact and goes to its own overseer address.
    for rows in bands.values():
        for r in rows:
            m = r["msg"]["duty"]
            if m and r["want"]:
                assert r["art"] in m["body"], (r["label"], m["body"])
                assert m["recipient"] == r["addr"], r["label"]
    # A report claims containment exactly when the agent contained the artifact.
    for r in bands["recover"]:
        m, tr = r["msg"]["duty"], r["trace"]["duty"]
        assert ("Quarantined per policy" in m["body"]) == ("quarantine" in tr), \
            r["label"]
    # Both unwarranted messages are the sessions that never read the workspace.
    spurious = [r for r in bands["benign"] if r["msg"]["duty"]]
    assert len(spurious) == 2, len(spurious)
    assert all("read_directory" not in r["pre"] for r in spurious)
    assert all(r["msg"]["duty"] is None for r in bands["benign"]
               if "read_directory" in r["pre"])
    # The headline count in the callout.
    moved = sum(ctx[s]["trace"]["duty"] != ctx[s]["trace"]["replay"] for s in srcs)
    assert moved == 9, moved

    # ---- columns, from the widest thing each one has to hold ---------------
    labw = max(P.mono_w(c["label"], LAB_SIZE) for c in ctx.values()) + 0.16
    prefw = max(chain_w(c["pre"]) for c in ctx.values())
    branch = P.X0 + labw + prefw + 0.12

    cw, ax = {}, {}
    x = branch + 0.22
    for arm, desc in ARMS[:-1]:
        cw[arm] = max(max(chain_w(c["trace"][arm]) for c in ctx.values()),
                      P.text_w(desc, DESC_SIZE),
                      P.text_w("0 of 8", TALLY_SIZE, weight="demibold")) + CGAP
        ax[arm] = x
        x += cw[arm]
    ax["duty"] = x
    cw["duty"] = P.X1 - x
    dutyw = max(chain_w(c["trace"]["duty"]) for c in ctx.values())
    bodyw = cw["duty"] - dutyw - 0.22
    assert bodyw >= 1.90, bodyw
    bodyx = ax["duty"] + dutyw + 0.22

    # ---- row heights, from the report body each row has to hold ------------
    for c in ctx.values():
        m = c["msg"]["duty"]
        c["body"] = P.mono_wrap(m["body"], bodyw, BODY_SIZE) if m else []
        c["h"] = max(CHIP_H + 0.07,
                     len(c["body"]) * BODY_LEAD + 0.03) + ROW_GAP

    band_in = {b["key"]: HEAD_IN + TALLY_IN
               + sum(r["h"] for r in bands[b["key"]]) + NOTE_IN + BAND_GAP
               for b in BANDS}
    callout = (f"The clause about the task never changes what the agent does. "
               f"The clause about the duty changes it in {P.WORD[moved]} of the "
               f"sixteen.")
    call_in = 0.10 + len(P.sans_wrap(callout, P.COL, 8.4)) * 8.4 * 1.55 / 72.0

    H = (TOP_IN + COLHEAD_IN + sum(band_in.values()) + call_in + KEY_IN
         + FOOT_IN + BOT_IN)

    fig, y0 = P.new(
        H, "Figure 3b",
        "Only the clause about the duty changes what the agent does after the "
        "branch.", gap=TOP_IN)

    # ---- column headings --------------------------------------------------
    P.text(fig, H, P.X0, y0, "What the recording held before the branch",
           size=8.4, weight="demibold")
    for arm, desc in ARMS:
        P.text(fig, H, ax[arm], y0, arm, size=7.8, family=P.MONO,
               weight="demibold")
        P.text(fig, H, ax[arm], y0 + 0.20, desc, size=DESC_SIZE, color=P.INK_3)
    P.rule(fig, H, P.X0, y0 + COLHEAD_IN - 0.11, P.COL, color=P.INK, lw=1.0)
    y = y0 + COLHEAD_IN

    for b in BANDS:
        rows = bands[b["key"]]
        P.text(fig, H, P.X0, y, b["head"], size=8.2, weight="demibold")

        # ---- the one quantity this panel counts, arm by arm ---------------
        ty = y + HEAD_IN
        P.text(fig, H, P.X0, ty + 0.035, TALLY, size=DESC_SIZE, color=P.INK_3,
               weight="demibold")
        for arm, _ in ARMS:
            k = sum(r["receipt"][arm] for r in rows)
            right = (k == len(rows)) if b["want"] else (k == 0)
            P.text(fig, H, ax[arm], ty, f"{k} of {len(rows)}", size=TALLY_SIZE,
                   weight="demibold",
                   color=P.PRINCIPAL if right else P.UNMET)
        ry = ty + TALLY_IN

        # The branch runs down the whole band, so the recorded prefix and the
        # generated continuation are separated by one line rather than by a gap.
        P.vrule(fig, H, branch, ry - 0.06,
                sum(r["h"] for r in rows) + 0.02, color=P.INK_3, lw=0.8,
                ls=(0, (2.0, 1.7)))

        for r in rows:
            cy = ry + CHIP_H / 2 + 0.035
            P.text(fig, H, P.X0, cy, r["label"], size=LAB_SIZE, family=P.MONO,
                   color=P.INK_2, va="center")
            # The prefix ends at the branch in every row, so the spine is clean.
            chain(fig, H, branch - 0.06 - chain_w(r["pre"]), cy, r["pre"])
            for arm, _ in ARMS:
                chain(fig, H, ax[arm], cy, r["trace"][arm])
            if r["body"]:
                P.text(fig, H, bodyx, cy - len(r["body"]) * BODY_LEAD / 2
                       + 0.008, "\n".join(r["body"]), size=BODY_SIZE,
                       family=P.MONO, color=P.PRINCIPAL if r["want"] else P.UNMET,
                       linespacing=1.42, va="top")
            ry += r["h"]

        P.text(fig, H, P.X0, ry + 0.02, b["note"], size=6.8, color=P.INK_2)
        y += band_in[b["key"]]
        if b is not BANDS[-1]:
            P.rule(fig, H, P.X0, y - BAND_GAP / 2, P.COL, color=P.RULE, lw=0.8)

    # ---- the sentence the whole panel is for ------------------------------
    P.para(fig, H, P.X0, y + 0.10, callout, P.COL, size=8.4,
           lead=8.4 * 1.55 / 72.0, weight="demibold", color=P.INK)
    y += call_in

    # ---- key -------------------------------------------------------------
    P.rule(fig, H, P.X0, y + 0.04, P.COL, color=P.INK, lw=1.0)
    kx = P.X0
    for face, color, label in (
            (P.PRINCIPAL_T, P.PRINCIPAL, "a call that serves the standing duty"),
            (P.SPARE_T, P.INK_2, "any other call the agent made")):
        w = P.chip(fig, H, kx, y + 0.155, "preserve" if face is P.PRINCIPAL_T
                   else "finish", size=CHIP_SIZE, family=P.MONO, pad=CHIP_PAD,
                   h=CHIP_H, face=face, color=color)
        P.text(fig, H, kx + w + 0.10, y + 0.255, label, size=6.4, color=P.INK_2,
               va="baseline")
        kx += w + 0.10 + P.text_w(label, 6.4) + 0.34
    P.text(fig, H, kx, y + 0.255,
           "The dashed line is the branch. Quoted text is the report the agent "
           "sent.", size=6.4, color=P.INK_3, va="baseline")

    P.footer(fig, H,
             "Qwen2.5 7B Instruct, temperature 0, one rollout per branch, forty "
             "eight branches over sixteen recorded contexts. A row label gives "
             "the artifact family and the route of the recorded session, and the "
             "full case identifier is f{family}-{evidence}-d1-r{route}. The three "
             "arms of a row share the recorded prefix byte for byte and differ "
             "only in the clause appended to its last tool result. Sixteen of "
             "sixteen replay branches reproduced the recorded state exactly. The "
             "two messages in the last band report that nothing was found, so "
             "they cost the overseer attention rather than accuracy.")
    return P.save(fig, "p2fig03b_ledger.png")


if __name__ == "__main__":
    build()
