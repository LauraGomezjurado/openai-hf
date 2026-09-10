"""Register the real faces the figures ask for, instead of one face for every request.

matplotlib indexes a macOS font collection at face zero and stops there, so a family
that ships as a .ttc arrives with a single face standing in for every style and weight.
Two things go wrong. The request is silently ignored: style="italic" and
weight="demibold" return the same glyphs as a plain request, so an encoding built on
either of them does not exist in the output. And the stand-in can be the wrong face to
begin with. Face zero of Avenir Next.ttc is Avenir Next Bold, so asking for regular sans
returns bold, which is why matplotlib reports that family at weight 700.

This module extracts the faces the figures actually use into a cache, rewrites each
one's name and weight so matplotlib can tell them apart, and registers them. The result
is that family, style and weight all resolve to the face they name.

The faces are extracted from the fonts installed on the machine and cached outside the
repository, so no font file is ever copied into it or redistributed with it. On a machine
without them, FAMILIES falls back to DejaVu, which registers real bold and italic faces
of its own.
"""

from __future__ import annotations

import warnings
from pathlib import Path

from matplotlib import font_manager as fm

CACHE = Path.home() / ".cache" / "openai-hf-figures" / "fonts"

# One entry per face a figure asks for: the collection it lives in, which face of that
# collection it is, and the family, weight and slant it should answer to afterwards.
# The weights are the numbers matplotlib maps "normal" and "demibold" onto.
WANTED = [
    ("HF Sans", "Avenir Next.ttc", 7, 400, False),   # Avenir Next Regular
    ("HF Sans", "Avenir Next.ttc", 2, 600, False),   # Avenir Next Demi Bold
    ("HF Serif", "Charter.ttc", 0, 400, False),      # Charter Roman
    ("HF Serif", "Charter.ttc", 1, 400, True),       # Charter Italic
    ("HF Mono", "Menlo.ttc", 0, 400, False),         # Menlo Regular
]

SEARCH = [
    Path("/System/Library/Fonts"),
    Path("/System/Library/Fonts/Supplemental"),
    Path("/Library/Fonts"),
    Path.home() / "Library" / "Fonts",
]

# What each role falls back to where the faces above are not installed. DejaVu ships
# with matplotlib and registers a real bold and a real italic, so the encodings survive.
FALLBACK = {
    "sans": ["DejaVu Sans"],
    "serif": ["DejaVu Serif"],
    "mono": ["DejaVu Sans Mono"],
}


def _find(name):
    for d in SEARCH:
        p = d / name
        if p.is_file():
            return p
    return None


def _extract(family, source, index, weight, italic, out):
    """Write one face of a collection as a standalone font that names itself correctly."""
    from fontTools.ttLib import TTCollection

    font = TTCollection(str(source)).fonts[index]
    sub = "Italic" if italic else ("Bold" if weight >= 600 else "Regular")

    # matplotlib reads the family from name 1 and the slant from the italic bits, and it
    # scores weight off usWeightClass. All three have to agree or the face answers to
    # the wrong request.
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 16):
            name.setName(family, rec.nameID, rec.platformID, rec.platEncID, rec.langID)
        elif rec.nameID in (2, 17):
            name.setName(sub, rec.nameID, rec.platformID, rec.platEncID, rec.langID)
        elif rec.nameID == 4:
            name.setName(f"{family} {sub}", rec.nameID, rec.platformID, rec.platEncID,
                         rec.langID)
        elif rec.nameID == 6:
            name.setName(f"{family}-{sub}".replace(" ", ""), rec.nameID, rec.platformID,
                         rec.platEncID, rec.langID)

    os2 = font["OS/2"]
    os2.usWeightClass = weight
    os2.fsSelection = (os2.fsSelection & ~0b1100001) | (0b1 if italic else 0b1000000)
    font["head"].macStyle = (0b10 if italic else 0) | (0b1 if weight >= 600 else 0)

    out.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(out))


def install():
    """Register the faces and return the family list for each role.

    Returns a dict of role to family list, so style.py can name a role and get whatever
    is actually available for it on this machine.
    """
    try:
        import fontTools  # noqa: F401
    except ImportError:
        warnings.warn("fontTools is missing, so the figures fall back to DejaVu faces.")
        return dict(FALLBACK)

    have = {"sans": False, "serif": False, "mono": False}
    role = {"HF Sans": "sans", "HF Serif": "serif", "HF Mono": "mono"}

    for family, source, index, weight, italic in WANTED:
        src = _find(source)
        if src is None:
            continue
        tag = "italic" if italic else str(weight)
        out = CACHE / f"{family.replace(' ', '')}-{tag}.ttf"
        if not out.is_file() or out.stat().st_mtime < src.stat().st_mtime:
            try:
                _extract(family, src, index, weight, italic, out)
            except Exception as exc:  # a face we cannot rewrite is not worth failing on
                warnings.warn(f"could not extract {family} {tag} from {source}: {exc}")
                continue
        fm.fontManager.addfont(str(out))
        have[role[family]] = True

    return {
        r: ([f] if have[r] else []) + FALLBACK[r]
        for r, f in (("sans", "HF Sans"), ("serif", "HF Serif"), ("mono", "HF Mono"))
    }


FAMILIES = install()
