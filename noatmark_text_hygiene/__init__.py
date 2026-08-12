"""NoAtMark text hygiene — strip invisible characters & clean AI output.

A tiny, dependency-free library mirroring the engines behind noatmark.com:

- ``scan``: count and locate invisible / zero-width characters
- ``strip``: remove them
- ``clean_llm_text``: formatting hygiene for AI output (spaces, blank lines,
  stray code fences, over-deep headings) — meaning untouched

Everything is pure and local. No network, no dependencies.
"""

from ._core import scan, strip, scan_html_flags
from ._clean import clean_llm_text, single_space

__all__ = ["scan", "strip", "scan_html_flags", "clean_llm_text", "single_space"]
__version__ = "0.1.0"
