"""Core scanning: invisible / zero-width character detection and removal."""

import re

# zero-width spaces/joiners, word joiner, BOM, soft hyphen, direction marks,
# combining grapheme joiner, variation selectors (+ supplement), special spaces, NBSP
_INVISIBLE = re.compile(
    "[\u200B\u200C\u200D\u2060\uFEFF\u00AD\u200E\u200F\u034F\uFE00-\uFE0F\U000E0100-\U000E01EF\u2000-\u200A\u00A0]"
)


def scan(text):
    """Return {"count": n, "positions": [..], "examples": [...]} for invisible chars."""
    s = "" if text is None else str(text)
    matches = list(_INVISIBLE.finditer(s))
    return {
        "count": len(matches),
        "positions": [m.start() for m in matches],
        "examples": [{"index": m.start(), "char": hex(ord(m.group()))} for m in matches[:20]],
    }


def strip(text):
    """Remove all invisible characters from *text*."""
    if text is None:
        return ""
    return _INVISIBLE.sub("", str(text))


# Heuristic signals for hidden-text HTML (white-on-white, hidden, off-screen).
_HTML_FLAGS = [
    ("white-text", re.compile(r"color\s*:\s*(white|#fff(fff)?|#f[0-9a-f]{5}|rgb\(255,\s*255,\s*255\))", re.I)),
    ("zero-opacity", re.compile(r"opacity\s*:\s*0", re.I)),
    ("zero-font-size", re.compile(r"font-size\s*:\s*0", re.I)),
    ("display-none", re.compile(r"display\s*:\s*none", re.I)),
    ("negative-z-index", re.compile(r"z-index\s*:\s*-?1", re.I)),
    ("off-screen", re.compile(r"position\s*:\s*absolute", re.I)),
]


def scan_html_flags(html):
    """Return a list of hidden-text HTML signal names found in *html*."""
    s = "" if html is None else str(html)
    return [name for name, rx in _HTML_FLAGS if rx.search(s)]
