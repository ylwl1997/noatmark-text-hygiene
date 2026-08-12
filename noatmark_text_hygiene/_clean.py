"""Formatting hygiene for AI output — meaning untouched.

Removes the mechanical artifacts LLM output carries: CRLF, excess blank lines,
trailing spaces, over-deep heading hashes, empty list markers, stray code
fences. Does NOT rewrite words or change structure.
"""

import re

_CRLF = re.compile(r"\r\n|\r")
_MULTI_BLANK = re.compile(r"\n{3,}")
_TRAILING = re.compile(r"[ \t]+$", re.M)
_SPACES = re.compile(r"[ \t]{2,}")
_PUNCT = [(re.compile(r"[ \t]+([,.;:!?])"), r"\1"), (re.compile(r"([(（])\s+"), r"\1"), (re.compile(r"\s+([)）])"), r"\1")]
_DEEP_HASH = re.compile(r"^(\s*)(#{4,})(\s*)", re.M)
_BARE_LIST = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*$", re.M)
_FENCE = re.compile(r"^\s*(?:```|~~~)\s*[a-z0-9_+.\-]*\s*$", re.M)


def _strip_fences(text):
    lines = text.split("\n")
    open_fence = False
    for i, line in enumerate(lines):
        if _FENCE.match(line):
            if open_fence:
                lines[i] = ""
                open_fence = False
            else:
                open_fence = True
    return "\n".join(lines)


def clean_llm_text(text):
    """Return ``{"cleaned": str, "stats": {...}}`` after a formatting pass."""
    t = "" if text is None else str(text)
    stats = {}
    before = t
    t = _CRLF.sub("\n", t)
    t = _MULTI_BLANK.sub("\n\n", t)
    t = _TRAILING.sub("", t)
    t = _SPACES.sub(" ", t)
    for rx, rep in _PUNCT:
        t = rx.sub(rep, t)
    t = _DEEP_HASH.sub(lambda m: m.group(1) + "###" + m.group(3), t)
    t = _BARE_LIST.sub("", t)
    t = _strip_fences(t)
    t = _MULTI_BLANK.sub("\n\n", t)
    stats["changed"] = t != before
    return {"cleaned": t, "stats": stats}


def single_space(text):
    """Normalize newlines and collapse blank-line runs (plain-text cleanup)."""
    t = "" if text is None else str(text)
    t = _CRLF.sub("\n", t)
    return _MULTI_BLANK.sub("\n\n", t).strip()
