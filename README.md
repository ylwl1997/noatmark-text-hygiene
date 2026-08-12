# NoAtMark Text Hygiene

Strip **invisible characters** (zero-width spaces, joiners, BOMs, variation selectors) and clean **LLM formatting artifacts** — the Python companion to [noatmark.com](https://noatmark.com/).

Dependency-free, pure Python, works offline.

## Install

```bash
pip install noatmark-text-hygiene
```

## Usage

```python
from noatmark_text_hygiene import scan, strip, clean_llm_text

# Count invisible / zero-width characters
text = "Hello​World﻿!"            # contains a ZWSP and a BOM
result = scan(text)
print(result["count"])                        # 2

# Remove them
clean = strip(text)
print(clean)                                  # "HelloWorld!"

# Clean LLM formatting junk (CRLF, blank lines, deep headings, stray fences)
messy = "####### Head\r\n\r\n\r\nText  with   spaces.\r\n```"
r = clean_llm_text(messy)
print(r["cleaned"])                           # "### Head\n\nText with spaces.\n```"
```

## What it strips

- Zero-width space `U+200B`, non-joiner `U+200C`, joiner `U+200D`
- Word joiner `U+2060`, BOM `U+FEFF`, soft hyphen `U+00AD`
- Direction marks `U+200E`/`U+200F`, combining grapheme joiner `U+034F`
- Variation selectors, special spaces, non-breaking space

## Honest scope

This removes **invisible Unicode characters** and **formatting artifacts**. It does **not** and cannot remove statistical AI text watermarks (those require the model provider's private key). See [noatmark.com](https://noatmark.com/claude-watermark/) for why.

## License

MIT
