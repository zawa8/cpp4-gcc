# SPDX-License-Identifier: GPL-3.0-or-later
"""x4lib - shared code for the c4 tools (xskii4 byte tables, tokenizers, number conversion).

Terms
-----
raw   : the bytes stored in a .c4 file (xskii4). The font x4e.ttf decides how they look.
view  : a readable unicode rendering of raw bytes, exactly what x4e.ttf shows.
        raw 0x3A-0x3F -> L Y V W P F      (hex digits 10..15)
        raw 0x41-0x46 -> : ; < = > ?      (punctuation shifted here; ASSUMED order, see Claude.md sec 9 q2)
        raw 0x47-0x5A -> 20 symbols       (see SYMBOLS)
        everything else -> same as ASCII  (ASSUMED, Claude.md sec 9 q3)
        raw <-> view is a bijection on bytes 0x00-0x7F.
"""

import re
from fractions import Fraction

DIGITS = "0123456789LYVWPF"          # glyph for digit value 0..15
PUNCT = ":;<=>?"                      # glyphs stored at raw 0x41..0x46
SYMBOLS = ("\u2260\u2264\u2265\u2248\u2261\u2190\u2192\u21d2\u2227\u2228"
           "\u00ac\u2295\u2208\u2209\u2205\u221e\u03bb\u221a\u00d7\u00f7")  # raw 0x47..0x5A (G..Z)
assert len(DIGITS) == 16 and len(PUNCT) == 6 and len(SYMBOLS) == 20

RAW2VIEW = {b: chr(b) for b in range(128)}
for _i, _ch in enumerate(DIGITS[10:]):
    RAW2VIEW[0x3A + _i] = _ch
for _i, _ch in enumerate(PUNCT):
    RAW2VIEW[0x41 + _i] = _ch
for _i, _ch in enumerate(SYMBOLS):
    RAW2VIEW[0x47 + _i] = _ch
VIEW2RAW = {v: k for k, v in RAW2VIEW.items()}
assert len(VIEW2RAW) == 128, "raw<->view must be a bijection"

PUNCT_TO_RAW = {ch: 0x41 + i for i, ch in enumerate(PUNCT)}   # ASCII ':' -> 0x41 ...
RAW_TO_PUNCT = {v: k for k, v in PUNCT_TO_RAW.items()}
SYMBOL_BYTES = range(0x47, 0x5B)


class X4Error(Exception):
    """Conversion/lint error. .problems is a list of (line, message)."""

    def __init__(self, problems):
        if isinstance(problems, str):
            problems = [(0, problems)]
        self.problems = problems
        super().__init__("; ".join("line %d: %s" % p if p[0] else p[1] for p in problems))


def raw_to_view(data):
    out = []
    for i, b in enumerate(data):
        if b >= 0x80:
            raise X4Error([(data.count(b"\n", 0, i) + 1, "byte 0x%02X is not xskii4 (only 0x00-0x7F)" % b)])
        out.append(RAW2VIEW[b])
    return "".join(out)


def view_to_raw(text):
    out = bytearray()
    line = 1
    for ch in text:
        if ch == "\n":
            line += 1
        if ch not in VIEW2RAW:
            if "A" <= ch <= "Z":
                why = "capital %r does not exist in xskii4 (only L Y V W P F as digits)" % ch
            else:
                why = "character %r has no xskii4 byte" % ch
            raise X4Error([(line, why)])
        out.append(VIEW2RAW[ch])
    return bytes(out)


# ---------------------------------------------------------------- tokenizers

C_TOKEN = re.compile(r'''
  (?P<ws>\s+)
 |(?P<lcom>//(?:\\\n|[^\n])*)
 |(?P<bcom>/\*.*?\*/)
 |(?P<str>(?:u8|u|U|L)?"(?:\\.|[^"\\\n])*")
 |(?P<chr>(?:u8|u|U|L)?'(?:\\.|[^'\\\n])*')
 |(?P<num>\.?[0-9](?:[eEpP][+-]|[0-9A-Za-z_.])*)
 |(?P<id>[A-Za-z_][A-Za-z0-9_]*)
 |(?P<other>.)
''', re.X | re.S)

X4_TOKEN = re.compile(rb'''
  (?P<ws>[ \t\r\n\f\v]+)
 |(?P<lcom>//(?:\\\n|[^\n])*)
 |(?P<bcom>/\*.*?\*/)
 |(?P<str>(?:u8|u)?"(?:\\.|[^"\\\n])*")
 |(?P<chr>(?:u8|u)?'(?:\\.|[^'\\\n])*')
 |(?P<num>\.?[0-?](?:[ep][+-]|[0-?a-z_.])*)
 |(?P<id>[a-z_][a-z0-9_]*)
 |(?P<other>.)
''', re.X | re.S)


def lineno(buf, pos):
    return (buf.count("\n", 0, pos) if isinstance(buf, str) else buf.count(b"\n", 0, pos)) + 1


# ---------------------------------------------------------------- numbers

INT_SUFFIX = {"", "u", "l", "ul", "lu", "ll", "ull", "llu"}
FLT_SUFFIX = {"", "f", "l"}
_V2H = str.maketrans("LYVWPF", "abcdef")
_H2V = str.maketrans("abcdef", "LYVWPF")


def hexs(n):
    """non-negative int -> digit string using the glyphs 0-9 L Y V W P F"""
    return format(n, "x").translate(_H2V)


def _vint(s):
    return int(s.translate(_V2H), 16)


def _is_dyadic(q):
    d = q.denominator
    return d & (d - 1) == 0


def _hexfloat_from_fraction(q):
    """exact non-negative dyadic Fraction -> c4 hex float text (view alphabet)"""
    if q == 0:
        return "0.0"
    ip = q.numerator // q.denominator
    rem = q - ip
    k = rem.denominator.bit_length() - 1
    nd = (k + 3) // 4
    ipv = hexs(ip)
    fpv = hexs(int(rem * 16 ** nd)).rjust(nd, "0") if nd else "0"
    if len(ipv) + nd <= 24:
        return ipv + "." + fpv
    num, den = q.numerator, q.denominator          # huge/tiny: mantissa p exponent
    e = 0
    while num % 2 == 0:
        num //= 2
        e += 1
    e -= den.bit_length() - 1
    return hexs(num) + "p" + ("-" if e < 0 else "") + hexs(abs(e))


def _exact_decimal(q):
    """exact non-negative dyadic Fraction -> decimal text with a '.'"""
    k = q.denominator.bit_length() - 1
    digits = str(q.numerator * 5 ** k).rjust(k + 1, "0")
    ip, fp = (digits[:-k], digits[-k:]) if k else (digits, "")
    return ip + "." + (fp.rstrip("0") or "0")


def number_c_to_view(tok):
    """ASCII C numeric literal -> c4 literal in view alphabet. Raises ValueError."""
    m = re.fullmatch(r"(0[xX][0-9a-fA-F]+|0[bB][01]+|0[0-7]+|[1-9][0-9]*|0)([uUlL]*)", tok)
    if m:
        body, suf = m.group(1), m.group(2).lower()
        if suf not in INT_SUFFIX:
            raise ValueError("bad integer suffix %r" % m.group(2))
        pre = body[:2].lower()
        if pre == "0x":
            out = body[2:].lower().translate(_H2V)
        elif pre == "0b":
            out = "0b" + body[2:]
        elif len(body) > 1 and body[0] == "0":
            out = "0o" + body[1:]
        else:
            out = hexs(int(body))
        return out + suf
    m = re.fullmatch(r"0[xX]([0-9a-fA-F]*)(\.?)([0-9a-fA-F]*)[pP]([+-]?[0-9]+)([fFlL]?)", tok)
    if m:
        ip, dot, fp, ex, suf = m.groups()
        if not (ip or fp):
            raise ValueError("hex float without digits")
        ex = int(ex)
        return ((ip.lower() or "0") + (dot + fp.lower() if dot else "")).translate(_H2V) \
            + "p" + ("-" if ex < 0 else "") + hexs(abs(ex)) + suf.lower()
    m = re.fullmatch(r"([0-9]*)(\.?)([0-9]*)(?:[eE]([+-]?[0-9]+))?([fFlL]?)", tok)
    if m and (m.group(1) or m.group(3)) and (m.group(2) or m.group(4) is not None):
        ip, dot, fp, ex, suf = m.groups()
        suf = suf.lower()
        ex10 = int(ex) if ex is not None else 0
        if abs(ex10) <= 400:
            q = Fraction(int((ip + fp) or "0"), 10 ** len(fp)) * Fraction(10) ** ex10
            if _is_dyadic(q):
                return _hexfloat_from_fraction(q) + suf
        # not exactly representable in hex digits: keep decimal spelling, marked by 0d
        return "0d" + ip + (dot + fp if dot else "") + ("e" + ex if ex is not None else "") + suf
    raise ValueError("unrecognised numeric literal %r" % tok)


def number_view_to_c(v, hex_ints=False, float_style="decimal"):
    """c4 literal (view alphabet) -> ASCII C literal. Raises ValueError."""
    m = re.fullmatch(r"0d([0-9]*)(?:(\.)([0-9]*))?(?:e([+-]?[0-9]+))?([a-z]*)", v)
    if m and (m.group(1) or m.group(3)):
        ip, dot, fp, ex, suf = m.groups()
        if dot or ex is not None or "f" in suf:
            if suf not in FLT_SUFFIX:
                raise ValueError("bad float suffix %r" % suf)
            return (ip or "0") + "." + (fp or "0") + ("e" + ex if ex is not None else "") + suf
        if suf not in INT_SUFFIX:
            raise ValueError("bad integer suffix %r" % suf)
        return str(int(ip)) + suf
    m = re.fullmatch(r"0o([0-7]+)([a-z]*)", v)
    if m:
        if m.group(2) not in INT_SUFFIX:
            raise ValueError("bad integer suffix %r" % m.group(2))
        return "0" + m.group(1) + m.group(2)
    m = re.fullmatch(r"0b([01]+)([a-z]*)", v)
    if m:
        if m.group(2) not in INT_SUFFIX:
            raise ValueError("bad integer suffix %r" % m.group(2))
        return "0b" + m.group(1) + m.group(2)
    m = re.fullmatch(r"([0-9LYVWPF]*)(?:(\.)([0-9LYVWPF]*))?(?:([pe])([+-]?)([0-9LYVWPF]+))?([a-z]*)", v)
    if not m or not (m.group(1) or m.group(3)):
        raise ValueError("unrecognised c4 numeric literal %r" % v)
    ip, dot, fp, mark, sign, exd, suf = m.groups()
    fp = fp or ""
    if not (dot or mark or "f" in suf):
        if suf not in INT_SUFFIX:
            raise ValueError("bad integer suffix %r" % suf)
        n = _vint(ip)
        return ("0x" + format(n, "x") if hex_ints else str(n)) + suf
    if suf not in FLT_SUFFIX:
        raise ValueError("bad float suffix %r" % suf)
    ex2 = 0
    if mark:
        ex2 = _vint(exd) * (1 if mark == "p" else 4) * (-1 if sign == "-" else 1)
    mant = _vint((ip + fp) or "0")
    e2 = ex2 - 4 * len(fp)
    if float_style == "decimal" and abs(e2) <= 200:
        q = Fraction(mant) * Fraction(2) ** e2
        return _exact_decimal(q) + suf
    return "0x" + ((ip or "0") + ("." + fp if dot else "")).translate(_V2H) + "p" + str(ex2) + suf


# ---------------------------------------------------------------- conversions

def to_snake(s):
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def c_to_x4(text, snake=False):
    """ASCII C source (str) -> (raw xskii4 bytes, {old_name: new_name}).
    Strings, character literals and comments keep their bytes unchanged (Claude.md sec 6, point 2)."""
    out = bytearray()
    problems = []
    toks = list(C_TOKEN.finditer(text))
    existing = {t.group() for t in toks if t.lastgroup == "id"}
    renames = {}
    for m in toks:
        kind, s = m.lastgroup, m.group()
        line = lineno(text, m.start())
        if kind in ("ws", "lcom", "bcom"):
            out += s.encode("utf-8")
        elif kind in ("str", "chr"):
            if s[0] in "LU":
                problems.append((line, "literal prefix %s needs a capital letter; use u8 or u" % s[0]))
            out += s.encode("utf-8")
        elif kind == "num":
            try:
                out += view_to_raw(number_c_to_view(s))
            except ValueError as e:
                problems.append((line, str(e)))
        elif kind == "id":
            if s != s.lower():
                new = to_snake(s)
                if not snake:
                    problems.append((line, "identifier %r has capitals (c4 is snake_case only; try %r or use --snake)" % (s, new)))
                renames[s] = new
                s = new
            out += s.encode("ascii")
        else:
            if ord(s) >= 128:
                problems.append((line, "non-ASCII character %r outside string/comment" % s))
            elif s in PUNCT_TO_RAW:
                out.append(PUNCT_TO_RAW[s])
            else:
                out += s.encode("ascii")
    if snake:
        rev = {}
        for old, new in renames.items():
            rev.setdefault(new, set()).add(old)
        for new, olds in rev.items():
            if len(olds) > 1 or new in existing:
                problems.append((0, "snake_case collision: %s -> %r" % (", ".join(sorted(olds)), new)))
    if problems:
        raise X4Error(problems)
    return bytes(out), renames


def x4_to_c(data, hex_ints=False, float_style="decimal"):
    """raw xskii4 bytes -> ASCII C source (bytes). Raises X4Error."""
    out = bytearray()
    problems = []
    for m in X4_TOKEN.finditer(data):
        kind, s = m.lastgroup, m.group()
        line = lineno(data, m.start())
        if kind == "num":
            try:
                out += number_view_to_c(raw_to_view(s), hex_ints, float_style).encode("ascii")
            except (ValueError, X4Error) as e:
                problems.append((line, str(e)))
        elif kind == "other":
            b = s[0]
            if b >= 0x80:
                problems.append((line, "byte 0x%02X is not xskii4" % b))
            elif b in RAW_TO_PUNCT:
                out += RAW_TO_PUNCT[b].encode()
            elif b in SYMBOL_BYTES:
                problems.append((line, "symbol byte 0x%02X (%s) is not defined in c4 yet (Claude.md sec 9 q5)" % (b, RAW2VIEW[b])))
            else:
                out.append(b)
        else:
            out += s
    if problems:
        raise X4Error(problems)
    return bytes(out)
