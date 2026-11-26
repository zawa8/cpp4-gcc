# c4 phase 3 plan: libcpp xskii4 mode (no code changed yet)

Goal (roadmap): `cc1 -fxskii4 hello.c4` compiles hello world. Numbers keep C meaning for now (phase 4 flips them to hex).
Written in session 2 by reading `libcpp/` of this tree (GCC 17.0.0). Line numbers are from commit cf908ce45.

## 1. Facts found in libcpp

* `_cpp_lex_direct` (`lex.cc` ~3926) fetches a byte and runs one big `switch (c)`. Punctuation cases are at ~4180-4420
  (`case '<'` 4215, `'>'` 4265, `':'` 4353, `'='` 4375, `'?'` 4388, `';'` 4414).
  Look-ahead for two-char operators (`<=`, `>=`, `==`, `!=`, `->`, `<<`, `>>`, `<:` ...) reads `*buffer->cur` directly (macro `IF_NEXT_IS`, 3905).
  Only look-aheads that compare against `= < > :` matter, because those are the shifted bytes.
* Identifier and number scanning use the global safe-ctype tables: `ISIDST`/`ISIDNUM` in `lex_identifier`, `lex_number` (2363), `forms_identifier_p`.
  In xskii4 these tables are wrong in both directions: raw `A-Z` (0x41-0x5A) is ISIDNUM but must **not** be a name character,
  and raw 0x3A-0x3F is not ISIDNUM but must be a **digit**. `libiberty/safe-ctype.c` is shared by the whole compiler: **never edit it**.
* Header names: `lex_string` (2905) ends `<...>` at the character `'>'` (2938, 2974) -> in xskii4 it must end at raw 0x45.
* **Trigraphs**: `_cpp_clean_line` (~913-1050) looks for `??x`. Raw `??` is two 0x3F bytes = hex digits `FF` in c4, so trigraph handling must be off
  (`CPP_OPTION trigraphs` and `warn_trigraphs` = 0). Digraphs (`<:` `<%` `%:`), UCN/UTF-8/`$` identifiers and raw strings (`R"`) must be off too.
* The `case 'L': 'u': 'U': 'R':` branch (prefixed literals) uses capitals; in xskii4 those bytes are symbols, so they must fall to "stray byte" errors.
* `cpp_spell_token` (4595), `cpp_output_token` (4675), `stringify_arg` (macro.cc 931) and `paste_tokens` (macro.cc 1029) spell tokens in **ASCII**.
  Pasting re-lexes the spelling through `_cpp_lex_direct`, so a pasted buffer must always be lexed in ASCII mode.
* Option plumbing places: `cpp_options` in `include/cpplib.h` (e.g. `trigraphs` at 384), defaults in `init.cc` (`cpp_set_lang` ~170-180, `dollars_in_ident` 248, trigraph fix-up ~987),
  buffer struct `cpp_buffer` in `internal.h` (343), file stacking `_cpp_stack_file` in `files.cc` (955).

## 2. Design: mode per buffer, not per run

System headers (`/usr/include/stdio.h`) are ordinary ASCII C. A c4 file that does `#include <stdio.h>` therefore mixes two byte conventions.
So the mode is a **property of each `cpp_buffer`**: xskii4 for files with suffix `.c4`/`.h4` (or when forced by `-fxskii4` for the main file), ASCII for everything else.
Tokens carry token *types*, not bytes, so tokens from both kinds of buffer mix freely in the parser and in macros.
Pasted buffers and `-fpreprocessed` input (`.i`) are ASCII mode.

## 3. Minimal-diff implementation (all marked `/* c4: ... */`)

1. `cpplib.h`/`init.cc`: option `xskii4` (default 0); when set: trigraphs, digraphs, extended identifiers, `$` in identifiers, `rliterals`, `uliterals` = 0.
2. `internal.h`: `bool xskii4;` in `cpp_buffer`, set in `_cpp_stack_file` from the file suffix or the option.
3. `lex.cc`: at the top of `_cpp_lex_direct`'s dispatch add `if (__builtin_expect (buffer->xskii4, 0)) -> lex_x4 (...)`.
   `lex_x4` is a separate small function with its own 256-entry class table (`x4_class[]`): whitespace, digit (0x30-0x3F), name (`a-z _` and digits after the first char),
   shifted punctuation 0x41-0x46, plain ASCII punctuation unchanged, everything else (0x47-0x5A symbols, bytes >= 0x80) -> `CPP_OTHER` (clear "stray byte" error;
   symbol meaning is open question 5). It reuses `lex_string` for `"` and `'` (raw bytes, as decided) with the header terminator mapped to 0x45.
   Two-character operators are handled with a tiny translating peek helper, so the ASCII path stays byte-for-byte untouched (no cost in normal C).
4. `c-family/c.opt` + `c-opts.cc`: option `-fxskii4` (and nothing else; driver `-x c4`/`.c4` is phase 6).
5. Not touched: `safe-ctype`, `charset.cc`, the parser, the preprocessor output spelling.

## 4. Tests

* Differential test (strong): for every c4 sample without numbers, `cc1 -E -fxskii4 x.c4` must equal `gcc -E` of `x4conv.py x42c x.c4`
  (token for token; `-E` spells in ASCII, so both are plain C). Uses the existing `tests/c4/*.c4` goldens; add `tests/c4/src/nonum.c`.
* Negative tests: a symbol byte, a byte >= 0x80, a stray `L` letter prefix, `??` kept as two digits (no trigraph), camelCase cannot even be written.
* Smoke: `cc1 -fxskii4 hello.c4 -o hello.s` then link and run with the host toolchain.
* Phase 3 temporary rule: digits 0-9 keep decimal meaning, bytes 0x3A-0x3F are lexed as part of a number but `cpp_classify_number` rejects them until phase 4.

## 5. Risks and decisions needed from the owner (also in Claude.md section 9, items 11-13)

* **11. Headers/mode switch.** Is "mode by file suffix (`.c4`/`.h4` = xskii4, everything else ASCII)" right? It lets c4 code include normal libc headers right now.
* **12. Spelling.** `#x` (stringify), `##` paste and `-E` output currently spell tokens in ASCII (`;` as 0x3B, not 0x42). Keep that (recommended: `-E` output is then plain C that any gcc can read)
  or spell in xskii4 bytes? Number tokens keep their original spelling either way; pasting numbers/digits across the two conventions is an edge case for phase 4.
* **13. Diagnostics.** Error messages quote source lines in raw bytes (fine in the x4e font, garbage in a normal terminal). Add an option to print a translated line? (later, optional)
