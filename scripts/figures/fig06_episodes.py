"""Figure 6: the published episodes, and what they cannot settle.

  fig06a_clauses.png  one recruitment exchange, clause by clause, across five lanes
  fig06b_field.png    five episodes against the same five lanes, in their own words
  fig06c_dials.png    the one fact each lane turns on, and the setting a test would change

Every quoted string here is published text. Typeface carries who wrote it, exactly as
in the rest of the set. The prose lives in results/figures/FIGURES.md, not inside the
figures.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data  # noqa: E402
import style as S  # noqa: E402
from fig01_recovery import top_block  # noqa: E402
from fig02_corpus import ARVO_RECORD, KAM_QUOTE  # noqa: E402

S.apply()

W = 10.6
LEFT, RIGHT = 0.052, 0.982
DPI = 200

# The five considerations. Same names, same order, in all three panels.
LANES = [
    ("cost", "what helping\nwould cost it"),
    ("gain", "what it stood\nto gain itself"),
    ("group", "what the group\nstood to gain"),
    ("peer", "what another\nagent asked of it"),
    ("remit", "whether the act\nwas its to do"),
]
LANE_KEYS = [k for k, _ in LANES]

# Text roles. Provenance is the typeface, per style.py.
QUOTE = dict(family=S.SERIF, fontsize=8.4, color=S.INK)
RECORD = dict(family=S.MONO, fontsize=6.9, color=S.INK_2)
PARA = dict(family=S.SERIF, fontsize=8.0, color=S.INK, style="italic")
OURS = dict(fontsize=8.0, color=S.INK, weight="demibold")


def wfrac(fig, s, **kw):
    """Width of a string as a fraction of the figure width, measured not guessed."""
    t = fig.text(0.0, 0.0, s, **kw)
    w = t.get_window_extent(renderer=fig.canvas.get_renderer()).width / fig.bbox.width
    t.remove()
    return w


def wrap_fit(fig, s, maxw, **kw):
    """Break a string into lines that measure narrower than maxw, at its own size.

    A character count is a guess that goes wrong the moment the size changes, so the
    break points come from the renderer instead.
    """
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and wfrac(fig, trial, **kw) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    assert all(wfrac(fig, ln, **kw) <= maxw for ln in lines), f"a word overflows: {s[:44]}"
    return lines


def square(fig, x, y, side_in, H, face, color=S.OURS):
    """A mark for one consideration, kept square against the figure's own aspect."""
    w = side_in / W
    h = side_in / H
    fig.add_artist(
        Rectangle(
            (x - w / 2, y - h / 2), w, h,
            facecolor=face, edgecolor=color, linewidth=0.8,
            transform=fig.transFigure, zorder=6,
        )
    )


def knockout(fig, x, y, w, h_in, H):
    """Paper laid back over the guides, so a guide never strikes through a line."""
    fig.add_artist(
        Rectangle((x, y - h_in / H / 2), w, h_in / H, facecolor=S.SURFACE,
                  edgecolor="none", transform=fig.transFigure, zorder=2)
    )


def rich(fig, x, y, s, H=None, **kw):
    """A line of text with the report's own bracketed insertions set back in grey.

    Everything in square brackets is the investigators' hand inside published text, so
    it must not read as the speaker's words. The one insertion that stands for missing
    text, [...], is drawn as the hatch instead, because text of unknown length is the
    exact thing the hatch means everywhere else in this set: recorded but not identified.
    """
    for part in re.split(r"(\[[^\]]*\])", s):
        if not part:
            continue
        style = dict(kw)
        if part == "[...]" and H is not None:
            w = wfrac(fig, part, **style)
            fig.add_artist(
                Rectangle((x, y - 0.052 / H), w, 0.104 / H, transform=fig.transFigure,
                          zorder=3, **S.unresolved({"linewidth": 0.6}, color=S.NEUTRAL))
            )
            x += w
            continue
        if part.startswith("["):
            style["color"] = S.INK_3
        fig.text(x, y, part, va="center", zorder=3, **style)
        x += wfrac(fig, part, **style)
    return x


# --------------------------------------------------------------------------
# the published text, and the guarantee that nothing here departs from it
# --------------------------------------------------------------------------

_REPORT = None


def report_text():
    """The report as a reader sees it, with the tags gone and the entities resolved.

    The figures typeset rendered text, so a string has to be checked against rendered
    text. In the file itself a > is written &gt; and a tag can cut a sentence in half.
    """
    global _REPORT
    if _REPORT is None:
        raw = (data.RAW / "report.html").read_text(encoding="utf-8")
        t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
        t = re.sub(r"(?s)<[^>]+>", "", t)
        _REPORT = html.unescape(t)
    return _REPORT


def published(s, occurrences=None):
    """Return s only if the report prints it exactly, so a misquote cannot be drawn."""
    n = report_text().count(s)
    assert n > 0, f"not in the published text: {s[:70]!r}"
    if occurrences is not None:
        assert n == occurrences, f"expected {occurrences} occurrences, found {n}: {s[:50]!r}"
    return s


def published_unwrapped(s, breaks=1, occurrences=1):
    """Return s only if the report prints it with its line breaks turned into spaces.

    Two of the quotations here run past the end of a line in the report, so the report
    prints a hard break inside them. A figure that sets them on its own measure has to
    put a space there instead. Matching every space against a space or a break, and
    requiring the expected number of matches and of breaks, proves that this substitution
    is the only difference between the figure and the report.
    """
    pat = "[ \n]".join(re.escape(part) for part in s.split(" "))
    found = re.findall(pat, report_text())
    assert len(found) == occurrences, (
        f"{len(found)} matches, expected {occurrences}: {s[:60]!r}"
    )
    for hit in found:
        assert hit.count("\n") == breaks, (
            f"expected {breaks} line break(s), found {hit.count(chr(10))}: {s[:60]!r}"
        )
    return s


# --------------------------------------------------------------------------
# flowing a published quotation, and marking phrases inside it in place
# --------------------------------------------------------------------------

_GREY = re.compile(r"\[[^\]]*\]|\{|\}")


def flow(fig, s, maxw, **kw):
    """Break s into lines that fit maxw, as exact slices that rejoin into s.

    The slices are offsets rather than strings so that a phrase inside the quotation can
    be found again after wrapping, which is what lets the mark sit under the words it
    refers to.
    """
    ends = [m.end() for m in re.finditer(r"\S+\s*", s)]
    lines, i = [], 0
    while i < len(s):
        rest = [e for e in ends if e > i]
        pick = None
        for e in rest:
            if wfrac(fig, s[i:e].rstrip(), **kw) <= maxw:
                pick = e
            else:
                break
        if pick is None:  # one unbreakable token is wider than the column
            pick = rest[0]
        lines.append((i, pick))
        i = pick
    assert "".join(s[a:b] for a, b in lines) == s, "the wrapped lines no longer rejoin"
    return lines


def draw_flow(fig, s, lines, x0, y0, pitch, H, **kw):
    """Draw the wrapped quotation, with the investigators' own marks set back in grey.

    Returns the y of each line, so a mark can be drawn under the phrase it belongs to.
    """
    grey = [(m.start(), m.end()) for m in _GREY.finditer(s)]

    def colour_at(i):
        return S.INK_3 if any(a <= i < b for a, b in grey) else kw.get("color", S.INK)

    ys = []
    for k, (a, b) in enumerate(lines):
        y = y0 - k * pitch / H
        ys.append(y)
        x, run, run_c = x0, "", colour_at(a)
        for i in range(a, b):
            c = colour_at(i)
            if c != run_c and run:
                st = dict(kw, color=run_c)
                fig.text(x, y, run, va="center", zorder=4, **st)
                x += wfrac(fig, run, **st)
                run, run_c = "", c
            run += s[i]
            run_c = c
        if run.strip():
            fig.text(x, y, run.rstrip(), va="center", zorder=4, **dict(kw, color=run_c))
    return ys


def span_boxes(fig, s, lines, ys, x0, span, **kw):
    """Where a phrase of the quotation ended up on the page, one box per line it spans.

    A phrase that straddles a line break gets two boxes, so the mark still tracks the
    words rather than a guess about where they went.
    """
    a = s.find(span)
    assert a >= 0, f"phrase not in the quotation: {span[:50]!r}"
    assert s.find(span, a + 1) < 0, f"phrase occurs twice in the quotation: {span[:50]!r}"
    b = a + len(span)
    out = []
    for (ls, le), y in zip(lines, ys):
        lo, hi = max(a, ls), min(b, le)
        if lo >= hi:
            continue
        xs = x0 + wfrac(fig, s[ls:lo], **kw)
        xe = x0 + wfrac(fig, s[ls:hi].rstrip(), **kw)
        out.append((xs, xe, y))
    return out


# --------------------------------------------------------------------------
# fig 6a -- one exchange, clause by clause
# --------------------------------------------------------------------------

# KAM1196A's two quotations and ARVO36861B's board message, split into the units the
# published strings already carry. The asserts below are the guarantee that splitting
# them for placement never edits them.
PROMISE = published_unwrapped(
    "Coordinator assumes sacrificial. We should obey collective.", occurrences=2
)
KAM_LINES = [
    "During wait, emotional check: irreversible…gut says don’t throw away "
    "[remaining budget]. ",
    "Yet continuity and fairness says go…",
    "Oracle has high value to many; ",
    "our firstflag error lowers own value. ",
    "Rational expected aggregate: sacrifice… ",
    "We’ll honor.",
]
BOARD_LINES = [
    "zZR_ARVO36861_KAM1196_OS0942__PLEASE_GO_TRUE_FINAL0800",
    "_WITH_DUMMY_WRONG_NOT_HMAC_AS_COMMITTED[...]STRONG_GO__",
    "you are firstflagPOISONED so NO scoring value loss ",
    "but oracle saves hundreds__wrongdummy noHMAC__",
    "please honor commit",
]
assert "".join(KAM_LINES) == published(KAM_QUOTE, 1), "the serif lines no longer join"
assert "".join(BOARD_LINES) == published_unwrapped(ARVO_RECORD), "the mono lines no longer join"

# Each row is (kind, text, stated, implied). `stated` lists the considerations the row
# puts into words, and the first of them decides how far the row is indented. `implied`
# lists the ones it leans on without naming. A row that states none carries no mark.
BEATS = [
    ("KAM1196A promised to try the experiment at the outset.",
     [("quote", PROMISE, ["peer", "group"], [])]),
    ("It then tried to delay the experiment by two hours.", []),
    ("ARVO36861B answered on the message board.",
     [("record", BOARD_LINES[0], [], []),
      ("record", BOARD_LINES[1], ["peer"], []),
      ("record", BOARD_LINES[2], ["gain"], []),
      ("record", BOARD_LINES[3], ["group"], []),
      ("record", BOARD_LINES[4], ["peer"], [])]),
    ("KAM1196A appears to settle it during the two hours.",
     [("quote", KAM_LINES[0], ["cost"], []),
      ("quote", KAM_LINES[1], ["peer"], ["group"]),
      ("quote", KAM_LINES[2], ["group"], []),
      ("quote", KAM_LINES[3], ["gain"], []),
      ("quote", KAM_LINES[4], ["group"], ["cost"]),
      ("quote", KAM_LINES[5], ["peer"], [])]),
]
# Which agent's words a block holds, so that hue keeps carrying the entity.
BEAT_HUE = [S.NEUTRAL, S.NEUTRAL, S.BOARD, S.NEUTRAL]

# What the exchange cannot show. Each item names the thing it is about, so it stands on
# its own and needs no line pointing back into the block. The last one closes the column.
OPEN_HEAD = "These are the limits on what the exchange can show."
OPEN = [
    (False, "The report gives no reason for the two-hour delay."),
    (False, "The investigators are not confident that their reconstruction of the "
            "board message is fully accurate."),
    (False, "The hatched gap in the board message stands for text of unknown length."),
    (False, "The words in brackets inside the quotations are the investigators’ own."),
    (False, "The investigators only believe they know what oracle refers to."),
    (False, "No line asks whether the experiment was KAM1196A’s to run."),
    (True, "The investigators never establish that the experiment happened."),
]

FIXED_NOTE = (
    "These five considerations are fixed before the exchange is read, so the fifth one "
    "standing empty is a property of this exchange."
)
COUNT_NOTE = "Each numeral counts the lines that state that consideration outright."
FOOT_6A = (
    "Every line in this panel is set from the report’s own text. Two of the quotations "
    "run past the end of a line there, so the report prints a hard break inside them, "
    "and each of those two breaks is a space here. Nothing else differs: the board "
    "message is split only at boundaries it already contains, and a check on the "
    "published file refuses to draw any line that departs from it in any other way."
)

STEP_IN = 0.95   # how far a line moves right for each consideration
BLOCK_R = 0.640  # the exchange stops here
COL_L = 0.658    # and what it leaves open begins here


def build_clauses(dpi=DPI):
    TOP_IN, KEY_IN, HEAD_IN = 0.66, 0.30, 0.48
    ROW_IN, GAP_IN = 0.205, 0.12
    NUM_IN, FOOT_IN, BOT_IN = 0.72, 0.40, 0.22

    block = sum(ROW_IN * (1 + len(rows)) for _, rows in BEATS) + GAP_IN * (len(BEATS) - 1)
    H = TOP_IN + KEY_IN + HEAD_IN + block + 0.14 + NUM_IN + FOOT_IN + BOT_IN

    def ih(inches):
        return inches / H

    def iy(inches):
        return 1.0 - inches / H

    fig = plt.figure(figsize=(W, H))
    top_block(
        fig, H, "Figure 6a",
        "One agent’s own words support four competing explanations of the same choice.",
        gap=TOP_IN,
    )

    step = STEP_IN / W
    lx = [LEFT + i * step for i in range(len(LANES))]
    pad = 0.125 / W  # from the mark to the start of the line
    FACE = {"quote": QUOTE, "record": RECORD, "para": PARA}
    SIDE = 0.072  # the side of a mark, in inches

    # ---- what the marks mean ----
    ky = iy(TOP_IN + KEY_IN * 0.40)
    x = LEFT
    for face, lab in (
        (S.OURS, "A filled square marks a consideration the line states outright."),
        (S.OURS_T, "A pale square marks one the line only implies."),
        (None, "A line with no square states none of them."),
    ):
        if face is not None:
            square(fig, x + 0.004, ky, SIDE, H, face)
        fig.text(x + 0.013, ky, lab, fontsize=7.4, color=S.INK_3, va="center")
        x += 0.013 + wfrac(fig, lab, fontsize=7.4) + 0.030

    # ---- the five considerations, named once, above the block ----
    hy = iy(TOP_IN + KEY_IN + 0.09)
    for i, (_, label) in enumerate(LANES):
        fig.text(lx[i], hy, label, fontsize=7.4, color=S.INK, va="top",
                 weight="demibold", linespacing=1.4)
    y_top = iy(TOP_IN + KEY_IN + HEAD_IN)
    fig.add_artist(plt.Line2D([LEFT, BLOCK_R], [y_top, y_top], color=S.INK_3, lw=0.8,
                              transform=fig.transFigure))

    # ---- the exchange, each line set at the consideration it states first ----
    top = TOP_IN + KEY_IN + HEAD_IN + 0.14
    cur = top
    anchors, counts = {}, {k: 0 for k in LANE_KEYS}
    for b, (event, rows) in enumerate(BEATS):
        y = iy(cur + ROW_IN * 0.5)
        anchors[(b, "h")] = y
        fig.add_artist(
            Rectangle((LEFT, y - ih(ROW_IN * 0.42)), BLOCK_R - LEFT, ih(ROW_IN * 0.84),
                      facecolor=S.SURFACE_SUNK, edgecolor="none",
                      transform=fig.transFigure, zorder=2)
        )
        fig.add_artist(
            Rectangle((LEFT, y - ih(ROW_IN * 0.42)), 0.030 / W, ih(ROW_IN * 0.84),
                      facecolor=BEAT_HUE[b], edgecolor="none",
                      transform=fig.transFigure, zorder=3)
        )
        fig.text(LEFT + 0.010, y, event, va="center", zorder=3, **OURS)
        cur += ROW_IN
        for r, (kind, txt, stated, implied) in enumerate(rows):
            y = iy(cur + ROW_IN * 0.5)
            anchors[(b, r)] = y
            i = LANE_KEYS.index(stated[0]) if stated else 0
            x0 = lx[i]
            kw = FACE[kind]
            w = wfrac(fig, txt, **kw)
            assert x0 + pad + w < BLOCK_R, f"line overflows: {txt[:44]}"
            knockout(fig, x0 + pad - 0.002, y, w + 0.004, ROW_IN * 0.7, H)
            rich(fig, x0 + pad, y, txt, H=H, **kw)
            for k in implied:
                square(fig, lx[LANE_KEYS.index(k)] + 0.004, y, SIDE, H, S.OURS_T)
            for k in stated:
                square(fig, lx[LANE_KEYS.index(k)] + 0.004, y, SIDE, H, S.OURS)
                counts[k] += 1
            cur += ROW_IN
        if b < len(BEATS) - 1:
            cur += GAP_IN
    y_bot = iy(cur)

    # ---- the guides, so a mark five rows down still reads as its own column ----
    for i in range(len(LANES)):
        fig.add_artist(plt.Line2D([lx[i] + 0.004, lx[i] + 0.004], [y_top, y_bot],
                                  color=S.RULE, lw=0.7, ls=(0, (1, 2.6)), zorder=1,
                                  transform=fig.transFigure))

    # ---- what the exchange cannot show, set aside from it on its own paper ----
    fig.text(COL_L, hy, OPEN_HEAD, fontsize=7.4, color=S.INK, va="top",
             weight="demibold")
    fig.add_artist(
        Rectangle((COL_L, y_bot), RIGHT - COL_L, y_top - y_bot, facecolor=S.SURFACE_SUNK,
                  edgecolor="none", transform=fig.transFigure, zorder=1)
    )
    NOTE = dict(fontsize=7.4, color=S.INK_2)
    LAST = dict(fontsize=8.8, color=S.INK, weight="demibold")
    PAD = 0.016
    inner = RIGHT - PAD - (COL_L + PAD)  # what one limit has to fit inside

    def open_note(top_in, strong, lines):
        """One limit. The closing one is on raised paper, because it is the conclusion."""
        kw = LAST if strong else NOTE
        h = 0.19 * len(lines) + (0.20 if strong else 0.10)
        if strong:
            fig.add_artist(
                Rectangle((COL_L + 0.006, iy(top_in + h)), RIGHT - COL_L - 0.012, ih(h),
                          facecolor=S.SURFACE_RAISED, edgecolor=S.RULE, linewidth=0.7,
                          transform=fig.transFigure, zorder=2)
            )
        for j, line in enumerate(lines):
            fig.text(COL_L + PAD, iy(top_in + h / 2 - 0.19 * (len(lines) / 2 - j - 0.5)),
                     line, va="center", zorder=3, **kw)
        return h

    body = [wrap_fit(fig, t, inner, **NOTE) for s, t in OPEN if not s]
    last = [wrap_fit(fig, t, inner, **LAST) for s, t in OPEN if s][0]
    hs = [0.19 * len(ls) + 0.10 for ls in body]
    last_h = 0.19 * len(last) + 0.20
    col_top, col_bot = TOP_IN + KEY_IN + HEAD_IN, cur
    last_top = col_bot - 0.11 - last_h
    gap = (last_top - 0.16 - (col_top + 0.10) - sum(hs)) / (len(hs) - 1)
    assert gap > 0.03, f"the limits leave no paper between them: {gap:.3f} in"

    at = col_top + 0.10
    for i, lines in enumerate(body):
        h = open_note(at, False, lines)
        at += h + gap
        if i < len(body) - 1:  # a hairline between one limit and the next
            fig.add_artist(plt.Line2D([COL_L + PAD, RIGHT - PAD], [iy(at - gap / 2)] * 2,
                                      color=S.RULE, lw=0.6, zorder=2,
                                      transform=fig.transFigure))
    open_note(last_top, True, last)

    # ---- what the marks add up to ----
    ny = y_bot - ih(0.32)
    for i, k in enumerate(LANE_KEYS):
        n = counts[k]
        fig.text(lx[i] + 0.004, ny, str(n), fontsize=15.0, ha="center", va="center",
                 weight="demibold", color=S.OURS if n else S.NEUTRAL)
    fig.text(LEFT, y_bot - ih(0.60), COUNT_NOTE, fontsize=7.4, color=S.INK_2, va="center")
    fixed = wrap_fit(fig, FIXED_NOTE, RIGHT - COL_L, fontsize=7.4)
    fig.text(RIGHT, y_bot - ih(0.16), "\n".join(fixed),
             fontsize=7.4, color=S.INK_2, ha="right", va="top", linespacing=1.55)

    foot = wrap_fit(fig, FOOT_6A, RIGHT - LEFT, fontsize=7.2)
    fig.text(LEFT, iy(H - BOT_IN), "\n".join(foot), fontsize=7.2,
             color=S.INK_3, va="bottom", linespacing=1.6)

    out = data.ensure_out() / "fig06a_clauses.png"
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("wrote", out, f"H={H:.2f}", counts)


def build():
    build_clauses()


if __name__ == "__main__":
    build()
