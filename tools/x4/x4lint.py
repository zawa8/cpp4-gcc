#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""x4lint - lint c4 sources (raw xskii4 bytes) or, with --ascii, ASCII C that is about to be converted.

  x4lint.py [--strict] [-v] file.c4 ...
  x4lint.py --ascii [--strict] file.c ...

Raw mode checks: bytes >= 0x80, NUL, malformed number literals, unterminated strings/comments,
digit bytes (0x3A-0x3F) glued to an identifier, G-Z symbol bytes (warning: meaning undecided), CRLF.
ASCII mode checks: capitals and camelCase in identifiers, L/U literal prefixes, upper-case literal
suffixes, non-ASCII outside strings/comments.
Exit status 1 if any error (with --strict: also on warnings).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x4lib  # noqa: E402


def lint_raw(data, verbose=False):
    res = []
    prev = None
    for m in x4lib.X4_TOKEN.finditer(data):
        kind, s = m.lastgroup, m.group()
        line = x4lib.lineno(data, m.start())
        if kind == "ws" and b"\r" in s:
            res.append((line, "warning", "CR byte (use LF line ends)"))
        elif kind == "num":
            try:
                x4lib.number_view_to_c(x4lib.raw_to_view(s))
            except (ValueError, x4lib.X4Error) as e:
                res.append((line, "error", "bad number literal: %s" % e))
            if prev == "id" and prev_end == m.start() and 0x3A <= s[0] <= 0x3F:
                res.append((line, "error", "digit byte glued to identifier (hex digits cannot be part of a name)"))
        elif kind == "other":
            b = s[0]
            if b >= 0x80 or b == 0:
                res.append((line, "error", "byte 0x%02X is not valid xskii4 text" % b))
            elif b in x4lib.SYMBOL_BYTES:
                res.append((line, "warning", "symbol byte 0x%02X (%s): meaning in c4 undecided" % (b, x4lib.RAW2VIEW[b])))
            elif b in (0x22, 0x27):
                res.append((line, "error", "unterminated string or character literal"))
            elif b == 0x2F and data[m.end():m.end() + 1] == b"*":
                res.append((line, "error", "unterminated comment"))
        elif kind in ("str", "chr", "lcom", "bcom") and verbose:
            if any(0x3A <= c <= 0x5A and c != 0x40 for c in s):
                res.append((line, "info", "%s contains bytes that x4e.ttf shows as other glyphs (capitals/punctuation)" % kind))
        prev, prev_end = kind, m.end()
    return res


def lint_ascii(text):
    res = []
    for m in x4lib.C_TOKEN.finditer(text):
        kind, s = m.lastgroup, m.group()
        line = x4lib.lineno(text, m.start())
        if kind == "id" and s != s.lower():
            what = "camelCase" if re.search(r"[a-z0-9][A-Z]", s) else "capital letters"
            res.append((line, "error", "%s in identifier %r (snake_case: %r)" % (what, s, x4lib.to_snake(s))))
        elif kind in ("str", "chr") and s[0] in "LU":
            res.append((line, "error", "literal prefix %s needs a capital letter; use u8 or u" % s[0]))
        elif kind == "num" and re.search(r"[UL]", re.sub(r"^0[xX][0-9a-fA-F]*", "", s)):
            res.append((line, "warning", "upper-case literal suffix in %r (c4 uses lower-case; L is a hex digit glyph)" % s))
        elif kind == "other" and ord(s) >= 128:
            res.append((line, "error", "non-ASCII character %r outside string/comment" % s))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--ascii", action="store_true", help="lint ASCII C source instead of raw c4")
    ap.add_argument("--strict", action="store_true", help="warnings count as errors")
    ap.add_argument("-v", "--verbose", action="store_true", help="also report info items")
    a = ap.parse_args(argv)
    bad = 0
    for path in a.files:
        data = open(path, "rb").read()
        if a.ascii:
            res = lint_ascii(data.decode("utf-8", "replace"))
        else:
            res = lint_raw(data, a.verbose)
        for line, sev, msg in res:
            print("%s:%d: %s: %s" % (path, line, sev, msg))
            if sev == "error" or (a.strict and sev == "warning"):
                bad = 1
    return bad


if __name__ == "__main__":
    sys.exit(main())
