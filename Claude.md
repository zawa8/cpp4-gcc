# Claude.md - cpp4-gcc / gcc4 / c4 compiler

This file is the hand-over for a new Claude session. Read it fully before touching code.
Last updated: 2026-11-26 (session 2). Keep this file up to date at the end of every session.

## 1. Goal

Build **gcc4**: a fork of GCC that compiles **c4**, a C dialect whose source files are written in the
**xskii4** encoding and edited with the font `x4e.ttf`.

c4 is "almost normal C" with four differences (given by the owner):

1. **Maths is 4 fingers + 1 thumb based by default**:
   `4*4 = 10 = 8+8 = 10 = F+1 = P+2 = W+3 = V+4 = Y+5 = L+6`.
   So numbers are **base 16 by default**, hex digits 10..15 are `L Y V W P F`
   (L=10, Y=11, V=12, W=13, P=14, F=15).
   **Decided by the owner (session 1): by default `int`, `float`, everything is hexadecimal.**
   Example: `int a=V ;` means a = 12 (8+4). Also `float a=1.8 ;` // a = `0d1.5` (decimal 1.5): floats are written in hex by default,
   and the prefix **`0d`** marks a decimal literal (owner's own example, session 1). In raw xskii4 bytes (assuming the shift in section 3) this line is
   `int a` + 0x44 (`=`) + 0x3C (shown as `V`) + 0x42 (`;`).
2. c4 does **not support capital case `A-Z`** and does not support **camelCase**.
3. c4 supports **only snake_case**.
4. **Regex ("regeks") in c4 is different**, as per xskii4 (the regex metacharacters live at other byte values).

Repo: <https://github.com/zawa8/cpp4-gcc> (branch `master`). Owner GitHub user: `zawa8`.

## 2. Working agreements with the owner

- The owner chats in a self-made romanised style (lowercase, letters substituted: j->z, q->k, v->w ...,
  Hindi written in his own scheme). Claude's stored memory holds the exact rules; follow them **in chat replies only**.
  Code, comments, docs, commit messages and file names stay plain ASCII English.
- Identifiers the owner chose keep his spelling, e.g. `werify_utf.py`, `wersion`. Never "correct" them.
- The owner reads short status messages. If a task runs long, send a one-line status, then continue.
- Be honest about what is verified and what is guessed. Mark guesses as such (see section 9, open questions).
- Never write the GitHub token into any file, commit message, memory or log. The owner pastes a token in chat when
  a push is needed: use it inline for the single push (`git push https://x-access-token:<token>@github.com/zawa8/cpp4-gcc.git ...`),
  pipe output through `sed` to hide it, and tell the owner to revoke it afterwards.
- Tags/branches: the owner asked for the annotated tag **`1st_wersion_by_claude`** on the commit that adds this file
  (first version by Claude). Later milestone tags are welcome, but ask first before moving or deleting an existing tag.

## 3. The xskii4 encoding (ground truth for c4)

Authority, in this order:
1. <https://github.com/zawa8/xfont> : `readme.md` (xskii4 section), `pysk/x4py/Claude.md` (original spec),
   `pysk/x4py/notosans_maths_to_x4e.py`, `notosfd/x4e.sfd`, `pysk/ttfwofpy/p5generate.py` (builds ttf/woff2).
2. The owner's chat statements.

Facts:

- xskii4 = "american standard code for information interchange" re-done for **4-finger maths**. Source files are
  ordinary byte streams; the **font** decides how each byte looks. The compiler must therefore interpret the
  *bytes* by their xskii4 meaning, not by their ASCII look.
- Digits and hex digits are continuous from 0x30: `0123456789LYVWPF` occupy bytes 0x30-0x3F.
  Bytes 0x3A-0x3F (ASCII `: ; < = > ?`) are shown as **L Y V W P F** and mean the digit values 10..15.
- The glyphs `: ; < = > ?` are **shifted to bytes 0x41-0x46 (ASCII `A-F`)**.
  So in a c4 source file the statement terminator `;` is stored as byte **0x42**, `:` as 0x41, `<` 0x43, `=` 0x44, `>` 0x45, `?` 0x46.
  (Reading of the owner's text "glyphs for :;<=>? are shifted to A-F": confirm the exact order, see section 9.)
- Bytes 0x47-0x5A (ASCII `G-Z`, 20 slots) are free for extra programming symbols. Claude suggested and built these into
  `x4e.sfd` (script `notosans_maths_to_x4e.py`), commit in xfont `95569d2`:

  | byte | glyph | | byte | glyph | | byte | glyph | | byte | glyph |
  |---|---|---|---|---|---|---|---|---|---|
  | G | != (not equal) | L | <- | Q | not | V | infinity |
  | H | <= | M | -> | R | xor (circled plus) | W | lambda |
  | I | >= | N | => | S | element of | X | square root |
  | J | approx equal | O | logical and | T | not element of | Y | multiply |
  | K | identical | P | logical or | U | empty set | Z | divide |

  Whether c4 should accept these as single-glyph operator tokens (e.g. G for `!=`) is **undecided** (section 9).
- Lowercase `a-z` are letters. Capitals do not exist as letters. Identifiers are `[a-z0-9_]` (hex digit bytes 0x3A-0x3F are
  digits only inside numbers, they cannot start or continue an identifier unless the owner says otherwise).
- All other printable ASCII bytes (`( ) [ ] { } + - * / % & | ^ ~ ! # " ' , . \ _` ...) are assumed unchanged.
  **Unverified**: confirm against `x4_chars_map.csv`/`x4e.sfd` before relying on it.
- Glyph check done in session 2 (rendered `xfont/notosfd/x4e.sfd` at its current head with fontforge): **FAILED**.
  Slots 0x3A-0x3F do show digit glyphs (a pound-like L, Y, V, W, P, F), but slots 0x41-0x45 still show other shapes (not `: ; < = >`)
  and slot 0x46 has **no glyph at all**. So the shifted punctuation is not in the font yet. Fixing it is a font task in the `xfont` repo
  (and needs open question 2 answered: exact byte order). The tools in `tools/x4/` only use bytes, so they do not depend on it.

## 4. Do not confuse: hskii / 4fskii / xskii4

This repo already contains older owner documents that use another name and another table:

- `ascii5_hskii4.md` ("hskii_konti", column `4fskii`): there, bytes 65-90 (`A-Z`) are phonetic Hindi letters (x a i u e o N k K g ...)
  and lowercase `f..z` are operator glyphs (`==`, `!=`, `&&`, ...). This is **a different design** from xskii4/x4e
  (where lowercase a-z are the letters).
- `readme.md`/`progres.md` (before session 1) talk about **cpp4**, **cplong** and "programming symbols E,U,I,O,M,X,A,H".

Working assumption (needs owner confirmation): the current target is **xskii4 + x4e.ttf + c4** as in the xfont repo;
the hskii/4fskii table is an older experiment. Do not implement the hskii table unless the owner says so.

## 5. Repo facts (checked in session 1)

- Content: a full GCC source tree, `gcc/BASE-VER` = **17.0.0** (current trunk, includes libgcobol, libga68). 162k files, ~1.5 GB.
  The old readme claim "based on GCC 5.4.0" was wrong and was corrected.
- Git: one visible commit `4f411d126` "Rename 'pipe' to 'logikl_or' in markdown table" (author wimxl kumar vimalkumar), branch `master`.
  The clone used in session 1 was shallow (`--depth 1`).
- `progres.md` says `RID_CPLONG` and the keyword "cplong" were added to `gcc/c-family/c-common.h`/`c-common.cc`.
  **That change is not in the tree** (grep finds no `cplong`/`CPLONG` in `gcc/` or `libcpp/`). Treat progres.md as intent, not state.
- Files by the owner at repo root: `readme.md`, `progres.md`, `ascii5_hskii4.md`, `pl8_float_heksflot.md`, `simbxls_hski4.md` (empty).
- Where c4 work will land (GCC 17 layout):
  - `libcpp/lex.cc` : the byte-level lexer (`_cpp_lex_direct`, `case ';'`, `case ':'`, `case '?'` ...), `libcpp/charset.cc`, `libcpp/expr.cc` (number classification/interpretation), `libcpp/init.cc` + `libcpp/include/cpplib.h` (cpp options).
  - `gcc/c-family/c-lex.cc` (turns cpp tokens into parser tokens, number interpretation), `gcc/c-family/c.opt` (options), `gcc/c-family/c-opts.cc`.
  - `gcc/c/` (C front end: `c-parser.cc`, `c-decl.cc` ...), `gcc/gcc.cc` + `gcc/c/gccspec.cc` (driver specs, file suffixes).
  - `libiberty/safe-ctype.c` : global ctype tables used by the whole compiler. **Do not change these globally.**
  - `gcc/testsuite/` : add a `gcc.c4/` directory for c4 tests.
- The earlier cpp4 plan targeted `gcc/cp/` (C++). c4 is C, so the first target is `libcpp` + `gcc/c/`.

## 6. Design (proposal from session 1, **accepted by the owner** in session 1: "your proposals/recommendations/suggestions are best"; he may still change details)

Key insight: the difference between c4 and C is mostly **which byte means what**. So do **not** translate the whole input to ASCII
(string/char literal bytes would then be wrong at run time, and diagnostics would show translated text). Instead:

1. Add a libcpp option `xskii4` (driver flag e.g. `-fxskii4`, enabled automatically for `-x c4` and suffix `.c4`/`.h4`).
2. In that mode the lexer works on raw bytes:
   - byte -> token class is table driven (`xskii4_class[256]`) instead of the `switch (c)` literals;
     e.g. 0x42 -> CPP_SEMICOLON, 0x41 -> CPP_COLON, 0x46 -> CPP_QUERY, 0x43/0x45 -> `<`/`>` family, 0x44 -> `=` family.
   - identifier characters: only `[a-z0-9_]`; any byte 0x47-0x5A or 0x41-0x46 inside a word starts a new token (so camelCase cannot even be written).
   - numbers: digits are bytes 0x30-0x3F; radix default 16 (see below).
   - string and character literal contents stay **raw bytes** (no translation).
   - the preprocessor `#` and quotes are plain ASCII unless the owner says otherwise.
3. Number literals (prefixes still need owner decisions, section 9): default radix 16 for **all** literals, integer **and floating**,
   so `10` = 16 decimal, `V` = 12, `4*4` means `10`, and `1.8` = 1.5 decimal (fraction digits are hex, 1/16, 1/256 ...).
   Because hex digits are `L Y V W P F` (not `a-f`), the letters `e`/`p` are free to be exponent markers in float literals (proposal; see section 9).
   Suggested prefixes: `0d` decimal, `0o` octal, `0b` binary, no prefix = hex. `libcpp/expr.cc cpp_classify_number` and
   `cpp_interpret_integer` are the places; `-Wc4-radix` style warnings help porting.
4. Lint pass ("snake_case only, no capitals") is mostly free from point 2; add clear errors for bytes 0x47-0x5A used as letters.
5. Keep `sizeof`, array sizes, `#define` values etc. semantically the same C rules, only literal spelling changes.
6. Runtime library: c4 programs need headers in xskii4 (`stdio.h4`, ...) and a printf/scanf that prints/reads base 16 by default.
   Start with a thin `libc4` wrapper over glibc; real regex support (item 4 of the goal) comes after the compiler core works.
7. Floating point: c4 keeps `float`/`double` (owner: "int float every thing in hexadecimal"), only the spelling is hex by default.
   GCC already has hex-float machinery (`0x1.8p3`) in `libcpp/expr.cc cpp_classify_number` and `real.cc`; c4 mostly reuses it with radix 16 as default.
   **cplong** is **out of scope** (confirmed by the owner, session 1).
   **IEEE 754 (decided: accepted by the owner):** yes. IEEE 754 binary32/binary64 is the
   *storage and arithmetic format*; hex vs decimal is only the *spelling* of literals and of printed output, so the two do not conflict.
   Reasons: hardware and GCC (`real.cc`, soft-float, libm, ABI) already do it; hex literals convert **exactly** (16 = 2^4, `1.8` is exactly 1.5,
   a `double` has 52 fraction bits = 13 hex digits, no rounding), while `0d0.1` is inexact; default printing in hex round-trips exactly.
   Not recommended: a base-16 float format (IBM hex float) or cplong, they would need a new ABI/libm and give up hardware speed.
   Proposal for literals: `1.8` (hex mantissa), `p` exponent = power of **2** like C99 hex floats (`1.8p3` = 1.5*2^3), exponent digits also hex;
   `0d1.5` decimal; optional `e` exponent = power of 16 (decide, section 9).

## 7. Roadmap

| phase | work | deliverable |
|---|---|---|
| 0 | docs, tag `1st_wersion_by_claude` | this file, readme.md (done in session 1) |
| 1 (**done, session 2**) | tooling in `tools/x4/` : `x4conv.py` (ASCII-C <-> xskii4 bytes, incl. decimal<->hex literal conversion), `x4lint.py` (capitals, camelCase) , sample programs `tests/c4/*.c4` | lets us write c4 test code without typing in the special font |
| 2 (**workflow written, session 2, not yet run**) | build setup: get `cc1` (C only) building. Sandbox has 1 core, 3 GB RAM, ~8 GB free disk, no gmp/mpfr/mpc headers: use a GitHub Actions workflow (`.github/workflows/build-c4.yml`, ubuntu, cached) instead of building locally; configure `--enable-languages=c --disable-bootstrap --disable-multilib --disable-nls --disable-libsanitizer` | green CI build of unmodified trunk |
| 3 | libcpp xskii4 mode: option plumbing, byte class table, lexer paths, identifier rule | hello-world c4 compiles with `-fxskii4` |
| 4 | numbers: default radix 16, prefixes, hex digit bytes 0x3A-0x3F, float literals decision | `4*4==10` test passes |
| 5 | `gcc.c4` testsuite + converter round-trip tests in CI | regression safety |
| 6 | driver: `-x c4`, suffix `.c4`, `gcc4`/`c4` program names, default include path for xskii4 headers | `gcc4 hello.c4` |
| 7 | headers + libc4 + radix-aware printf/scanf | hello world prints in base 16 |
| 8 | regex (regeks) library with xskii4 metacharacters; decide cpp4 / cplong | later |

Rule of thumb: every phase ends with something that runs and a test, then update this file and `progres.md`.

## 8. Practical notes

- Clone: `git clone --depth 1 https://github.com/zawa8/cpp4-gcc.git` (github.com, codeload, pypi, npm are reachable from the sandbox; other hosts may be blocked).
- A full local GCC build is not realistic in the chat sandbox (1 core). Prefer CI builds, or build only `cc1` (`make all-gcc`) and limit to C.
  GCC build needs `libgmp-dev libmpfr-dev libmpc-dev flex bison texinfo` (apt works via archive.ubuntu.com).
- Do not run repo-wide formatters or re-indent GCC files; keep diffs small and marked with `/* c4: ... */` comments so merges from upstream stay possible.
- GCC is GPL-3.0+ with runtime exception; keep license headers on new source files.
- Related owner repos and the matching toolchain (fontforge scripts, ttf/woff2 build) are in `xfont`; the fine-tune work there is tagged `fine_tune_by_claude`.

## 9. Open questions for the owner (ask before building on them)

1. xskii4 vs hskii4/4fskii: confirm that **xskii4 + x4e.ttf** (xfont repo) is the target and `ascii5_hskii4.md` is legacy (section 4).
2. Exact byte placement of the shifted punctuation: is it `A:` `B;` `C<` `D=` `E>` `F?` (in this order)?
3. Are the other ASCII punctuation bytes (parentheses, braces, `+ - * / % & | ^ ~ ! # " '` ...) unchanged in xskii4?
4. Number syntax: decimal prefix is `0d` (owner example). Still open: octal and binary prefixes (`0o`? `0b`?), and are `L Y V W P F` the only hex digit letters (bytes 0x3A-0x3F)?
5. Do the 20 symbols in bytes G-Z become single-glyph operators in c4 (e.g. `!=`, `<=`, `>=`, `&&`, `||`, `->`)? Which of the two spellings is allowed?
6. Floating point is kept and hex by default (answered). Still open: exponent marker (`e`? `p`?) and is the exponent itself base 16, base 2, or base 10-in-hex?
   What does `printf` show for a `float` by default (hex fraction, e.g. `1.8`)?
   (IEEE 754 binary32/binary64 as storage format: accepted. `p` = power of 2 and optional `e` = power of 16: accepted as proposed. Octal/binary prefixes `0o`/`0b`: accepted as proposed.)
7. Runtime text: should c4 programs print xskii4 bytes (so output displays correctly in the x4e font), i.e. no translation at run time?
8. Name of the final driver/binaries: `gcc4`, `c4`, `cpp4`? Suffix `.c4`?
9. Is C++ (cpp4, `gcc/cp/`) planned after c4, or replaced by c4?
10. Regex ("regeks"): POSIX-like syntax with moved metacharacters, or a new syntax?
11. Mode switch: xskii4 only for files with suffix `.c4`/`.h4` (everything else, e.g. `/usr/include/stdio.h`, stays ASCII)? See `docs/c4/phase3-plan.md`.
12. Token spelling for `#x`, `##` and `-E` output: ASCII (recommended) or xskii4 bytes?
13. Diagnostics: show source lines raw (x4e font) or translated?

## 10. Session log

- 2026-11-26 (session 2): roadmap phase 1 done. Added `tools/x4/` (`x4lib.py`, `x4conv.py`, `x4lint.py`, README.md) and `tests/c4/` (5 sample programs in `src/`,
  golden raw `.c4` files, readable `view/*.c4v`, `run_tests.py`, 100+ checks, all passing; round trip c4 -> C compiled with host gcc 13 prints identical output).
  Glyph check failed (section 3). Assumptions used by the tools are listed in `tools/x4/README.md`. Next: phase 2 (CI build of cc1), font fix in xfont.
- 2026-11-26 (session 2, later): phase 1 pushed (f4cef62b8). Wrote `.github/workflows/build-c4.yml` (job `tools` = python tests, job `cc1` = configure C-only + `make all-gcc` + smoke test). It is **unverified**: first run on GitHub may need fixes (configure flags, deps). Next session: read the Actions log, fix, then phase 3.
- 2026-11-26 (session 2, later 2): wrote `docs/c4/phase3-plan.md` (libcpp lexer analysis, per-buffer mode design, trigraph trap `??` = digits FF, test plan). No libcpp code changed. Waiting for CI result and answers to questions 11-13.

- 2026-11-26 (end of session 1): owner accepted all proposals in sections 6-7. Next session starts at roadmap phase 1 (tools/x4/ converter + linter)
  together with the cheap glyph check from section 3, then phase 2 (CI build).

- 2026-11-26 (session 1, later 2): cplong out of scope (confirmed), decimal prefix `0d`, `float a=1.8` = decimal 1.5; IEEE 754 recommendation written down.
- 2026-11-26 (session 1, later): owner decided that int, float, everything is hexadecimal by default (`int a=V ;` is 12).

- 2026-11-26 (session 1): explored repo (GCC 17.0.0 trunk, single commit), read xfont xskii4 docs, corrected readme.md, wrote this file,
  created tag `1st_wersion_by_claude`. No compiler code written yet.
