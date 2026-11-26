# Benefits of xskii4 / c4

Short list of why xskii4 (the encoding) and c4 (the language written in it) are designed the way they are.
Written at the request of the owner (session 2). Plain ASCII English on purpose; the owner's own spelling style is in chat only.

## 1. Default 4-finger + 1-thumb maths (base 16) with `0123456789LYVWPF` continuous from hex 0x30

`4*4 = 10 = 8+8`, and `10 = F+1 = P+2 = W+3 = V+4 = Y+5 = L+6`. The 16 digit glyphs sit in one unbroken run, bytes 0x30-0x3F.

* **Digit value = byte minus 0x30.** No special case for letters. In ASCII there is a gap between `9` (0x39) and `A`/`a` (0x41/0x61),
  so every hex conversion needs a branch or a lookup table. In xskii4 it is `byte & 0x0F`.
* **Printing a digit is `value + 0x30`.** Same for all 16 values, no table, no branch.
* **"Is this a digit?" is one test:** `(byte & 0xF0) == 0x30`. Digit order equals numeric order, so sorting digit strings sorts numbers.
* **One digit = 4 bits = one nibble; one byte = exactly 2 digits.** Masks, addresses, colours, bit fields and memory dumps read directly.
  16 = 4*4 and halving is easy (8+8), which suits counting on 4 fingers plus a thumb marker.
* **No `0x` prefix and no case confusion.** Hex digits are not letters, so there is no `a` vs `A`, no `0xff` vs `0xFF` vs `0XFF`.
* **Letters stay free for real letters.** Because hex digits are not `a-f`, the lower-case letters `e`, `p`, `b`, `d`, `f` can be float exponents, prefixes and suffixes
  (`1.8p3`, `0d1.5`, `0b101`, `255ul`, `1.8f`) without clashing with digits.
* **Exact floats.** Hex float literals are exact in IEEE 754 (`1.8` is exactly 1.5), so literals do not round the way `0.1` does.
* **Easy to teach.** The pattern `L+6 = Y+5 = V+4 = W+3 = P+2 = F+1 = 10` is a counting rule, not a table to memorise.

## 2. Only small case + snake_case: no capital letters, no camelCase

Identifiers are `[a-z0-9_]`. There is nothing else to type.

* **No shift key.** Faster typing, fewer typos and fewer shift/caps-lock slips.
* **One spelling per name.** No `fooBar` vs `foobar` vs `FooBar` vs `FOOBAR` bugs, no style arguments, no naming-convention linter needed.
  The language itself enforces it (camelCase cannot even be written).
* **Easier search and tooling.** `grep`, completion and rename need no case-folding rules; there is no case-sensitivity trap between systems
  (case-insensitive file systems, case-insensitive languages, URLs, SQL).
* **No look-alike letters.** Capital `I`, lower-case `l` and digit `1` (and `O` vs `0`) cannot be mixed up.
* **Word breaks are visible.** `http_server_port` shows its words; `HTTPServerPort` makes the reader guess where they split.
* **Simpler lexer.** An identifier rule of `[a-z_][a-z0-9_]*` is smaller and faster to scan than Unicode or mixed-case rules.
* **It pays for the rest of the design.** Freeing the 26 capital slots (0x41-0x5A) is what makes room for the shifted punctuation `: ; < = > ?`
  (so the digits can be continuous) and for 20 extra programming symbols.

## 3. `x = A` (the sound of Devanagari अ) instead of `x = ks`

In English spelling `x` means `ks` (or `gz`, or `z`): it is a spare letter that can always be written another way (`six` -> `siks`).
xskii4/xnglo gives it a job that is missing in Latin spelling: the short open vowel **अ** (the "uh/a" sound, the inherent vowel of Indian scripts).
Then `x` = अ, `xa` = आ.

* **Spellings follow the spoken sound.** Words that start with or contain that sound become somewhat more phonetically correct for readers who think in Indian-language sounds:

  | normal English spelling | xskii4/xnglo spelling (owner's) |
  |---|---|
  | America | xmerika |
  | Canada | kxnxda (or cxnxda) |
  | Australia | austrelia |

  (The vowel in these words is the neutral "uh" sound, so a dedicated letter for it fits better than `a`, `e` or `u`, which English uses for it inconsistently.)
* **No loss of letters.** The old job of `x` is still writable: `ks` (`six` -> `siks`), `xks` (`x-ray` -> `xksre`), `z` (`xylophone` -> `zailofon`).
* **One letter per sound, same sound every time.** `x` is always अ; the reader does not guess between `a`, `u` and `e`.
* **Fits the Indic mapping.** Devanagari to Latin becomes one letter per akshar/swar (`अ=x`, `आ=xa`), which keeps romanised Hindi short and reversible.
* **Free in code.** `x` is a lower-case letter and works in snake_case identifiers (`xmount`, `x_index`) like any other letter.

## Honest trade-offs (so the benefits are read in context)

* The encoding is **not ASCII**: files need the x4e font (or the `tools/x4` converter) to look right; normal editors, terminals and diffs show shifted glyphs.
* Strings and comments keep raw bytes, so capitals and `: ; < = > ?` inside them look wrong in the x4e font (open question 7 in `Claude.md`).
* Hex-by-default is a break from every other language: existing C code and libraries need conversion (`tools/x4/x4conv.py` does this for literals).
* The phonetic benefit of `x = A` depends on the reader's accent and mother tongue; it is "somewhat" better, not exact.
