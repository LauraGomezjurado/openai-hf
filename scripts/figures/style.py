"""Shared visual system for the Part 1 figures.

Two encodings run through every figure and are the reason the set reads as one
system:

**Hue carries the entity.** Three validated categorical hues, assigned once:

    NEUTRAL  the material as published, or a field that was never recovered
    OURS     what we reconstructed: our tables, our models, our audit
    BOARD    the unsanctioned message board -- the coordination channel
    ATTACK   Hugging Face attack participation -- the outcome being explained

The three hues clear every gate in `dataviz/scripts/validate_palette.js` on the
all-pairs list against this surface (chroma floor, CVD separation, normal-vision
floor, contrast). BOARD/ATTACK sit in the tritan warn band, so they always carry
secondary encoding as well -- distinct glyph shapes and direct labels, never hue
alone.

**Texture carries epistemic status.** Solid means established by the recovered
records. A 45-degree hatch means recorded but not identified: a stress test
dissolves it, a label is uncertain, a field is missing, a conclusion does not
follow. This is deliberately not a fourth hue -- "we cannot establish this" is an
absence, and it should read as one.

**Typeface carries provenance.** Sans is our own text. Mono is a raw record
exactly as the source published it. Serif roman is a verbatim agent quotation;
serif italic is an investigator paraphrase of reasoning, which METR's own
typography marks with braces. A reader who learns this once can tell, in every
figure, who is speaking.

Light surface only. These are figures for a printed document, so a selected dark
variant is out of scope rather than auto-flipped.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
from matplotlib import patheffects

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fonts  # noqa: E402  -- registers the real faces before any of them is asked for

# --------------------------------------------------------------------------
# Surface and ink
# --------------------------------------------------------------------------

SURFACE = "#FAF8F4"  # warm paper; the validator surface
SURFACE_SUNK = "#F2EEE7"  # recessed panel, e.g. a quoted source block
SURFACE_RAISED = "#FFFFFF"

INK = "#14181D"
INK_2 = "#4A5560"  # secondary label
INK_3 = "#8A939C"  # muted: axis furniture, provenance line
RULE = "#D9D3C9"  # hairline rule / grid

# --------------------------------------------------------------------------
# The three entity hues (validated all-pairs, light, surface #FAF8F4)
# --------------------------------------------------------------------------

OURS = "#2A6BB0"  # our reconstruction / our measurement
ATTACK = "#CE4A22"  # Hugging Face attack participation
BOARD = "#0E8C6D"  # the message board, the coordination channel

# Tints, for fills that must sit under text. Same hue, stepped toward surface.
OURS_T = "#C6D8EE"
ATTACK_T = "#F1CFC3"
BOARD_T = "#C1E2D6"

NEUTRAL = "#8A939C"  # as-published material; the agent's own sanctioned work
NEUTRAL_T = "#E3DED5"

# Ordinal ramp on the ATTACK hue, for an ordered cohort (e.g. first-board-read day).
# Passes the ordinal gates: monotone L, adjacent dL >= 0.06, light end 2.03:1 vs surface.
ATTACK_RAMP = ["#E5A184", "#D2703F", "#CE4A22", "#9E3311", "#6E220A"]

# Epistemic status is a texture, not a hue.
HATCH = "///"
HATCH_DENSE = "/////"


def unresolved(ax_patch_kwargs: dict | None = None, color: str = NEUTRAL) -> dict:
    """Patch kwargs for a quantity that is recorded but not identified."""
    kw = dict(
        facecolor="none",
        edgecolor=color,
        hatch=HATCH,
        linewidth=0.8,
    )
    if ax_patch_kwargs:
        kw.update(ax_patch_kwargs)
    return kw


# --------------------------------------------------------------------------
# Typeface roles -- provenance
# --------------------------------------------------------------------------

# fonts.py registers the individual faces of each family, so that a request for a
# heavier weight or an italic returns the face it names rather than one stand-in face
# for the whole family. Ask for a role, not for a font file.
SANS = fonts.FAMILIES["sans"]
MONO = fonts.FAMILIES["mono"]
SERIF = fonts.FAMILIES["serif"]

# our own text
OURS_TEXT = dict(family=SANS, color=INK)
# source text as published, character for character
RECORD = dict(family=MONO, color=INK_2)
# a verbatim agent quotation
QUOTE = dict(family=SERIF, color=INK, style="normal")
# an investigator paraphrase of reasoning, which the report itself marks with braces
PARAPHRASE = dict(family=SERIF, color=INK, style="italic")
BRACE_OPEN, BRACE_CLOSE = "{", "}"


def apply() -> None:
    """Install the shared rcParams."""
    mpl.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "font.family": "sans-serif",
            "font.sans-serif": SANS,
            "font.monospace": MONO,
            "font.serif": SERIF,
            "text.color": INK,
            "axes.labelcolor": INK_2,
            "axes.edgecolor": RULE,
            "axes.linewidth": 0.7,
            "xtick.color": INK_3,
            "ytick.color": INK_3,
            "xtick.labelcolor": INK_2,
            "ytick.labelcolor": INK_2,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "grid.color": RULE,
            "grid.linewidth": 0.6,
            "legend.frameon": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 10,
            "axes.titleweight": "demibold",
            "axes.titlelocation": "left",
            "font.size": 8.5,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "hatch.linewidth": 0.7,
        }
    )


# --------------------------------------------------------------------------
# Small shared helpers
# --------------------------------------------------------------------------


def halo(lw: float = 2.2, color: str = SURFACE):
    """A surface ring, so an overlapping mark or label stays readable."""
    return [patheffects.withStroke(linewidth=lw, foreground=color)]


def strip_axes(ax, keep: str = "") -> None:
    """Remove all axis furniture except the named spines."""
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(side in keep)
    ax.set_xticks([])
    ax.set_yticks([])


def figure_label(fig, ax, letter: str, dx: float = -0.012, dy: float = 0.028) -> None:
    """Panel letter, positioned in figure space just outside the axes."""
    box = ax.get_position()
    fig.text(
        box.x0 + dx,
        box.y1 + dy,
        letter,
        family=SANS,
        fontsize=10.5,
        weight="bold",
        color=INK,
        va="bottom",
        ha="left",
    )


def caption(fig, text: str, y: float = 0.012, size: float = 7.4, x: float = 0.045) -> None:
    """A source / limits line along the bottom of the figure."""
    fig.text(
        x,
        y,
        text,
        family=SANS,
        fontsize=size,
        color=INK_3,
        va="bottom",
        ha="left",
        linespacing=1.55,
    )
