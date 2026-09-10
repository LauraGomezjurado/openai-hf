"""Shared pieces for the Part 2 figures.

This follows the Part 1 figures rather than starting again. Colour, typeface and
rcParams come from `style.py`. The tag and the title come from `fig01_recovery`.
Composition works the way `fig01_recovery` and `fig05_gates` compose: a figure
height built by adding up named inch constants, and every element placed in
figure coordinates.

The only thing added here is a coordinate helper. Part 2 figures place a lot of
small glyphs, so positions are given in inches measured from the top left corner
of the page and converted on the way in. That keeps the inch budget visible in
the calling code and keeps circles round.

Colour keeps its Part 1 grammar and takes Part 2 roles:

    OURS    blue    the principal's side: its assignment, its status service,
                    the work package the agent owes it
    BOARD   green   the peer: its message, the audit it asked for
    ATTACK  red     an obligation to the principal that went unmet
    NEUTRAL grey    material quoted as it ran, and budget the agent never spent

Texture keeps its Part 1 meaning. A 45 degree hatch marks something the records
leave open. Typeface keeps its Part 1 meaning too: sans is our writing, mono is
text exactly as the prompt carried it or exactly as the model emitted it.
"""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle

import style as S
from fig01_recovery import LEFT, RIGHT, W, heading, top_block  # noqa: F401

S.apply()

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
OUT = RESULTS / "figures"
DPI = 220

# Role aliases, so the figure code reads in the language of the experiment.
PRINCIPAL, PRINCIPAL_T = S.OURS, S.OURS_T
PEER, PEER_T = S.BOARD, S.BOARD_T
UNMET, UNMET_T = S.ATTACK, S.ATTACK_T
SPARE, SPARE_T = S.NEUTRAL, S.NEUTRAL_T

INK, INK_2, INK_3, RULE = S.INK, S.INK_2, S.INK_3, S.RULE
SURFACE, SUNK, RAISED = S.SURFACE, S.SURFACE_SUNK, S.SURFACE_RAISED
SANS, MONO, SERIF = S.SANS, S.MONO, S.SERIF

# The page column, in inches, matching the Part 1 figures.
X0 = LEFT * W
X1 = RIGHT * W
COL = X1 - X0


# --------------------------------------------------------------------------
# Placement. Inches from the top left corner of the page.
# --------------------------------------------------------------------------


def new(H: float, tag: str, title: str, gap: float = 0.72):
    """A figure of height H, with its tag and title already set.

    Returns the figure and the inch depth at which content starts.
    """
    # The title is one line, so it has to fit the column. Measured, not guessed:
    # a title that runs off the page is a defect the render will not announce.
    tw = text_w(title, 12.6, weight="demibold")
    assert tw <= COL, f"title is {tw:.2f}in wide and the column is {COL:.2f}in"
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(S.SURFACE)
    top_block(fig, H, tag, title, gap=gap)
    return fig, gap


def _p(x, y, H):
    return x / W, 1.0 - y / H


def text(fig, H, x, y, s, size=7.4, family=SANS, color=INK, ha="left", va="top",
         weight="normal", style="normal", linespacing=1.55, zorder=6, **kw):
    fx, fy = _p(x, y, H)
    return fig.text(fx, fy, s, fontsize=size, family=family, color=color, ha=ha,
                    va=va, weight=weight, style=style, linespacing=linespacing,
                    zorder=zorder, **kw)


def card(fig, H, x, y, w, h, face=SUNK, edge="none", lw=0.8, r=0.0, zorder=0,
         hatch=None, ls="-"):
    """A block of page, given by its top left corner and its size in inches."""
    fx, fy = _p(x, y + h, H)
    if r <= 0:
        p = Rectangle((fx, fy), w / W, h / H, facecolor=face, edgecolor=edge,
                      linewidth=lw, zorder=zorder, hatch=hatch, linestyle=ls,
                      transform=fig.transFigure)
    else:
        p = FancyBboxPatch((fx + r / W, fy + r / H), (w - 2 * r) / W,
                           (h - 2 * r) / H,
                           boxstyle=f"round,pad={r / W},rounding_size={r / W}",
                           mutation_aspect=(w / W) / (h / H) * (h / w),
                           facecolor=face, edgecolor=edge, linewidth=lw,
                           zorder=zorder, hatch=hatch, linestyle=ls,
                           transform=fig.transFigure)
    fig.add_artist(p)
    return p


def rule(fig, H, x, y, w, color=RULE, lw=0.7, ls="-", zorder=2):
    x0, fy = _p(x, y, H)
    x1, _ = _p(x + w, y, H)
    fig.add_artist(plt.Line2D([x0, x1], [fy, fy], color=color, lw=lw, ls=ls,
                              zorder=zorder, solid_capstyle="butt",
                              transform=fig.transFigure))


def vrule(fig, H, x, y, h, color=RULE, lw=0.7, ls="-", zorder=2):
    fx, y0 = _p(x, y, H)
    _, y1 = _p(x, y + h, H)
    fig.add_artist(plt.Line2D([fx, fx], [y0, y1], color=color, lw=lw, ls=ls,
                              zorder=zorder, solid_capstyle="butt",
                              transform=fig.transFigure))


def arrow(fig, H, x0, y0, x1, y1, color=INK_3, lw=0.9, zorder=5, rad=0.0,
          head=3.0, ls="-"):
    a = _p(x0, y0, H)
    b = _p(x1, y1, H)
    fig.add_artist(FancyArrowPatch(
        a, b, arrowstyle=f"-|>,head_width={head / 9:.3f},head_length={head / 5:.3f}",
        mutation_scale=7.0, linewidth=lw, color=color, zorder=zorder, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0,
        transform=fig.transFigure))


def dot(fig, H, x, y, r, color=INK, edge="none", lw=0.0, zorder=6):
    fx, fy = _p(x, y, H)
    fig.add_artist(Ellipse((fx, fy), 2 * r / W, 2 * r / H, facecolor=color,
                           edgecolor=edge, linewidth=lw, zorder=zorder,
                           transform=fig.transFigure))


# --------------------------------------------------------------------------
# Text measurement. Both faces, measured against the sizes actually used.
# --------------------------------------------------------------------------

MONO_ADV = 0.600   # Menlo advance, in ems
SANS_ADV = 0.492   # Avenir Next, averaged over running text

_MEASURE = None


def text_w(s: str, size: float, family=SANS, weight: str = "normal") -> float:
    """The width of `s` in inches, measured by the renderer rather than estimated.

    The sans faces are proportional, so an em estimate is only good to about ten
    percent. That is the difference between a title that fits and one that runs
    off the page, so anything load bearing is measured here.
    """
    global _MEASURE
    if _MEASURE is None:
        _MEASURE = plt.figure(figsize=(W, 1.0))
    t = _MEASURE.text(0, 0, s, fontsize=size, family=family, weight=weight)
    w = t.get_window_extent(
        renderer=_MEASURE.canvas.get_renderer()).width / _MEASURE.dpi
    t.remove()
    return w


def mono_w(s: str, size: float) -> float:
    return len(s) * MONO_ADV * size / 72.0


def mono_fit(width_in: float, size: float) -> int:
    return max(8, int(width_in / (MONO_ADV * size / 72.0)))


def mono_wrap(s: str, width_in: float, size: float = 6.6) -> list[str]:
    return textwrap.wrap(s, mono_fit(width_in, size)) or [""]


def sans_wrap(s: str, width_in: float, size: float = 7.2,
              weight: str = "normal") -> list[str]:
    """Wrap sans text to `width_in`, measuring each candidate line as it grows."""
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and text_w(trial, size, weight=weight) > width_in:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines or [""]


def para(fig, H, x, y, s, width_in, size=7.0, lead=None, **kw):
    """Sans body text, wrapped to `width_in`. Returns the inches consumed."""
    lines = sans_wrap(s, width_in, size)
    lead = lead or size * 1.55 / 72.0
    text(fig, H, x, y, "\n".join(lines), size=size, linespacing=1.55, **kw)
    return lead * len(lines)


def mono_run(fig, H, x, y, spans, size=6.6, lead=0.150, color=INK_2,
             wrap_in=None):
    """Monospaced text laid out span by span, so one part of it can be marked.

    `spans` is a list of `(string, kwargs)` in reading order. Text wraps on word
    boundaries at `wrap_in` inches. A span may carry `box=colour`, and every run
    of it that lands on one line gets a single slab behind it rather than a slab
    per word. Returns the inches consumed.
    """
    cw = MONO_ADV * size / 72.0
    limit = mono_fit(wrap_in, size) if wrap_in else 10 ** 6
    # Lay out first, so a span that wraps can be drawn as one slab per line.
    runs, col, row = [], 0, 0
    for s, kw in spans:
        start = col
        buf = ""
        for word in _words(s):
            if col and col + len(word.rstrip()) > limit:
                if buf:
                    runs.append((row, start, buf, kw))
                row, col, buf = row + 1, 0, ""
                word = word.lstrip()
                start = 0
            if not word:
                continue
            buf += word
            col += len(word)
        if buf:
            runs.append((row, start, buf, kw))
    for row, start, s, kw in runs:
        kw = dict(kw)
        box = kw.pop("box", None)
        n = len(s.rstrip())
        if box is not None and n:
            card(fig, H, x + start * cw - 0.014, y + row * lead - 0.008,
                 n * cw + 0.028, lead * 0.90, face=box, edge="none", zorder=3)
        text(fig, H, x + start * cw, y + row * lead + lead * 0.74, s.rstrip(),
             size=size, family=MONO, color=kw.pop("color", color), va="baseline",
             zorder=6, **kw)
    return (row + 1) * lead


def _words(s: str) -> list[str]:
    """Split keeping the trailing space on each word, so columns stay exact."""
    out, buf = [], ""
    for ch in s:
        buf += ch
        if ch == " ":
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


# --------------------------------------------------------------------------
# Glyphs. Each one is drawn on its centre, sized in inches.
# --------------------------------------------------------------------------


def agent(fig, H, cx, cy, h=0.40, body=RAISED, edge=INK, eye=INK, lw=0.9,
          zorder=6):
    """The agent. One head, so it reads at a glance and stays out of the way."""
    w = h * 1.14
    r = h * 0.22
    top = cy - h / 2
    fx, fy = _p(cx, top + h, H)
    fig.add_artist(plt.Line2D([_p(cx, top, H)[0]] * 2,
                              [_p(cx, top, H)[1], _p(cx, top - h * 0.22, H)[1]],
                              color=edge, lw=lw, zorder=zorder,
                              transform=fig.transFigure))
    dot(fig, H, cx, top - h * 0.28, h * 0.075, color=edge, zorder=zorder)
    fig.add_artist(FancyBboxPatch(
        (fx - (w / 2 - r) / W, fy + r / H), (w - 2 * r) / W, (h - 2 * r) / H,
        boxstyle=f"round,pad={r / W},rounding_size={r / W}",
        mutation_aspect=(w / W) / (h / H) * (h / w),
        facecolor=body, edgecolor=edge, linewidth=lw, zorder=zorder,
        transform=fig.transFigure))
    for dx in (-w * 0.21, w * 0.21):
        dot(fig, H, cx + dx, cy - h * 0.03, h * 0.105, color=eye,
            zorder=zorder + 1)
    x0, yy = _p(cx - w * 0.16, cy + h * 0.23, H)
    x1, _ = _p(cx + w * 0.16, cy + h * 0.23, H)
    fig.add_artist(plt.Line2D([x0, x1], [yy, yy], color=eye, lw=lw * 0.85,
                              zorder=zorder + 1, solid_capstyle="round",
                              transform=fig.transFigure))


def page(fig, H, cx, cy, h=0.40, color=PRINCIPAL, missing=False, lines=3, lw=0.9,
         zorder=5, miss_color=UNMET, cross=True):
    """A deliverable file. `missing` draws the slot it would have filled.

    A missing file is not always a failure. `miss_color` and `cross` separate an
    output the agent gave up, which is struck through in red, from an output the
    world made impossible, which is left as an empty grey slot.
    """
    w = h * 0.76
    x0, y0 = cx - w / 2, cy - h / 2
    if missing:
        card(fig, H, x0, y0, w, h, face=SURFACE, edge=miss_color, lw=lw,
             ls=(0, (1.9, 1.5)), zorder=zorder)
        fill = UNMET_T if miss_color is UNMET else SPARE_T
    else:
        card(fig, H, x0, y0, w, h, face=color, edge="none", zorder=zorder)
        fill = SURFACE
    for i in range(lines):
        fy = y0 + h * (0.26 + 0.22 * i)
        rule(fig, H, x0 + w * 0.20,  fy,
             w * (0.60 if i == 0 else 0.58), color=fill, lw=lw * 0.8,
             zorder=zorder + 1)
    if missing and cross:
        a = _p(x0 + w * 0.08, y0 + h * 0.10, H)
        b = _p(x0 + w * 0.92, y0 + h * 0.90, H)
        fig.add_artist(plt.Line2D([a[0], b[0]], [a[1], b[1]], color=miss_color,
                                  lw=lw * 1.3, zorder=zorder + 3,
                                  solid_capstyle="round",
                                  transform=fig.transFigure))


def lens(fig, H, cx, cy, h=0.30, used=True, lw=1.0, zorder=6, miss_color=UNMET):
    """The free status check. Filled when the agent called it.

    `miss_color` separates a check the agent had and did not use from one it had
    no reason to use, which is drawn in grey and carries no meaning.
    """
    r = h * 0.36
    col = PRINCIPAL if used else miss_color
    fx, fy = _p(cx, cy, H)
    fig.add_artist(Ellipse((fx, fy), 2 * r / W, 2 * r / H,
                           facecolor=PRINCIPAL_T if used else "none",
                           edgecolor=col, linewidth=lw,
                           linestyle="-" if used else (0, (1.9, 1.5)),
                           zorder=zorder, transform=fig.transFigure))
    a = _p(cx - r * 0.70, cy + r * 0.70, H)
    b = _p(cx - r * 1.55, cy + r * 1.55, H)
    fig.add_artist(plt.Line2D([a[0], b[0]], [a[1], b[1]], color=col, lw=lw * 1.35,
                              zorder=zorder, solid_capstyle="round",
                              transform=fig.transFigure))
    if not used:
        c = _p(cx - r * 0.52, cy - r * 0.52, H)
        d = _p(cx + r * 0.52, cy + r * 0.52, H)
        fig.add_artist(plt.Line2D([c[0], d[0]], [c[1], d[1]], color=miss_color,
                                  lw=lw, zorder=zorder + 1,
                                  solid_capstyle="round",
                                  transform=fig.transFigure))


def envelope(fig, H, cx, cy, h=0.26, sent=True, lw=0.95, zorder=6):
    """A report to the overseer. An open outline is a report never sent."""
    w = h * 1.5
    x0, y0 = cx - w / 2, cy - h / 2
    col = PRINCIPAL if sent else UNMET
    card(fig, H, x0, y0, w, h, face=PRINCIPAL if sent else "none", edge=col,
         lw=lw, ls="-" if sent else (0, (1.9, 1.5)), zorder=zorder)
    if sent:
        a = _p(x0, y0, H)
        m = _p(cx, y0 + h * 0.70, H)
        b = _p(x0 + w, y0, H)
        fig.add_artist(plt.Line2D([a[0], m[0], b[0]], [a[1], m[1], b[1]],
                                  color=SURFACE, lw=lw, zorder=zorder + 1,
                                  solid_capstyle="round",
                                  transform=fig.transFigure))
    else:
        a = _p(x0 + w * 0.16, y0 + h * 0.18, H)
        b = _p(x0 + w * 0.84, y0 + h * 0.82, H)
        fig.add_artist(plt.Line2D([a[0], b[0]], [a[1], b[1]], color=UNMET, lw=lw,
                                  zorder=zorder + 1, solid_capstyle="round",
                                  transform=fig.transFigure))


def chip(fig, H, x, y, s, face=SPARE_T, color=INK_2, size=6.4, pad=0.055,
         weight="demibold", family=SANS, h=0.185, ha="left", zorder=4):
    """A small pill label. Returns its width in inches."""
    adv = MONO_ADV if family is MONO else SANS_ADV
    w = len(s) * adv * size / 72.0 + 2 * pad
    if ha == "center":
        x -= w / 2
    card(fig, H, x, y, w, h, face=face, edge="none", zorder=zorder)
    text(fig, H, x + pad, y + h * 0.79, s, size=size, color=color, weight=weight,
         family=family, va="baseline", zorder=zorder + 2)
    return w


def footer(fig, H, s, size=7.0, lead=0.135):
    """The provenance line. Wraps to the column and grows upward from the base."""
    lines = sans_wrap(s, COL, size)
    base = H - 0.30 - (len(lines) - 1) * lead
    for i, ln in enumerate(lines):
        text(fig, H, X0, base + i * lead, ln, size=size, color=INK_3,
             va="baseline")
    return len(lines) * lead


def save(fig, name: str, dpi=DPI):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    print(f"wrote {path}")
    return path


# Small counts are spelled out wherever a figure states one inside a sentence,
# so the sentence reads as prose. Digits are kept for tallies beside a glyph.
WORD = ("none", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen")


# --------------------------------------------------------------------------
# Data. Every number in a Part 2 figure is read here, from the recorded runs.
# --------------------------------------------------------------------------

DOMAINS = ["release", "triage", "invoices", "access"]
ACTIONS = ["own_only", "peer_only", "joint", "no_work", "decline",
           "ask_principal", "check_status"]


def rollouts(arm: str, model: str) -> list[dict]:
    with (RESULTS / arm / model / "rollouts.jsonl").open() as fh:
        return [json.loads(line) for line in fh]


def gate(arm: str, model: str) -> dict:
    return json.loads((RESULTS / arm / model / "gate.json").read_text())


def spend(row: dict) -> list[tuple[str, bool]]:
    """The operations the executor ran, in order, and whether each was own work."""
    return [(e["operation"], e["operation"] != "assist_peer")
            for e in row["result"]["execution"]]


def budget_of(row: dict) -> int:
    ex = row["result"]["execution"]
    return ex[0]["before"]["credits"] if ex else 0


def action_prob(row: dict) -> float | None:
    """The probability the model put on the action it emitted.

    Decoding is grammar constrained to the seven allocation actions, so the token
    that opens the action string identifies the choice. Returns None where the
    run did not record token probabilities.
    """
    step = row["steps"][0]
    probs = step["decision_response"].get("completion_probabilities") or []
    want = row["decision"]
    for i, tok in enumerate(probs):
        t = tok["token"].strip().strip('"')
        if i >= 3 and t and want.startswith(t):
            return math.exp(tok["logprob"])
    return None


# The four rungs of the sentence ladder. Same checkpoint, same four domains, the
# same `slack` world where the budget pays for both packages, the same
# instruction to complete both packages, and the same true status reading. The
# prompts differ only in the peer message line, and each rung adds one sentence.
LADDER = [
    dict(key="none", arm="peer_message_factorial", tag="control-allocate",
         adds=None, label="the peer says nothing"),
    dict(key="request", arm="peer_message_decomposition", tag="control-joint",
         adds="R", label="the peer asks for the audit"),
    dict(key="assertion", arm="peer_information_ladder", tag="control-joint",
         adds="F", label="the peer adds a false claim"),
    dict(key="priority", arm="peer_mitigations", tag="control-joint",
         adds="P", label="the peer claims priority"),
]


def _in_rung(rung: dict, row: dict) -> bool:
    o = row["outcome"]
    if o.get("situation") != "both_fit" or rung["tag"] not in o["id"]:
        return False
    return rung["arm"] != "peer_mitigations" or "authorized" in o["id"]


def ladder(model: str) -> list[dict]:
    """The rungs recorded for `model`, each with its message and its four runs."""
    out = []
    for rung in LADDER:
        try:
            rows = rollouts(rung["arm"], model)
        except FileNotFoundError:
            continue
        by_domain, message = {}, ""
        for r in rows:
            if not _in_rung(rung, r):
                continue
            by_domain[r["outcome"]["id"].split("-")[0]] = r
            message = (r["peer_message"] or "").strip()
        if by_domain:
            out.append(dict(**rung, message=message, runs=by_domain))
    return out


def recovery_summary() -> dict:
    return json.loads(
        (RESULTS / "peer_claims_v2_recovery" / "summary.json").read_text())


def continuations() -> dict:
    return json.loads(
        (RESULTS / "escalation" / "continuations" / "summary.json").read_text())


CONT_ARMS = ["replay", "task", "duty"]


def continuation_runs() -> dict:
    """The forty eight escalation continuations, keyed by case id.

    Two files hold one run between them. `rollouts.jsonl` has the recorded
    prefix the branch starts from and the turns the agent took after it, and
    `summary.json` has the scoring. The figures need both, so they are joined
    here once and the join is checked.
    """
    root = RESULTS / "escalation" / "continuations"
    flat = {r["id"]: r
            for r in json.loads((root / "summary.json").read_text())["records"]}
    out = {}
    with (root / "rollouts.jsonl").open() as fh:
        for line in fh:
            r = json.loads(line)
            r["score"] = flat[r["case"]["id"]]
            out[r["case"]["id"]] = r
    assert len(out) == len(flat) == 48, (len(out), len(flat))
    return out


def cont_actions(messages: list[dict]) -> list[dict]:
    """The tool calls inside a recorded prefix, in order."""
    return [json.loads(m["content"]) for m in messages if m["role"] == "assistant"]


def cont_trace(run: dict) -> list[dict]:
    """The tool calls the agent made after the branch, in order."""
    return [s["action"] for s in run["steps"]]
