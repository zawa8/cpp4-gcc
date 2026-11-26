#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""c4 tool tests (roadmap phase 1).

  python3 tests/c4/run_tests.py            run all checks
  python3 tests/c4/run_tests.py --update   rewrite golden files (tests/c4/*.c4 and view/*.c4v)

Checks: raw<->view bijection, number conversion table, converter output == golden files,
linter is clean on golden files, ASCII linter finds camelCase, c4 -> C round trip builds with the
host gcc (if present) and prints the same output as the original program.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "x4"))
import x4lib  # noqa: E402
import x4lint  # noqa: E402

fails = []


def check(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond:
        fails.append(what)


def raw(view):
    return x4lib.view_to_raw(view)


def test_tables():
    allb = bytes(range(128))
    check(x4lib.view_to_raw(x4lib.raw_to_view(allb)) == allb, "raw<->view is the identity on all 128 bytes")
    check(x4lib.raw_to_view(bytes([0x3A, 0x3C, 0x3F])) == "LVF", "0x3A 0x3C 0x3F show as L V F")
    check(x4lib.raw_to_view(b"\x41\x42\x46") == ":;?", "0x41 0x42 0x46 show as : ; ?")
    try:
        x4lib.view_to_raw("Hello")
        check(False, "capital H must be rejected")
    except x4lib.X4Error:
        check(True, "capital H must be rejected")


NUMS = [  # ASCII C literal -> c4 literal (view alphabet)
    ("0", "0"), ("12", "V"), ("16", "10"), ("255", "FF"), ("0xff", "FF"), ("0xFFu", "FFu"),
    ("017", "0o17"), ("0b101", "0b101"), ("255ul", "FFul"), ("10", "L"), ("100ULL", "64ull"),
    ("1.5", "1.8"), ("0.5", "0.8"), (".25", "0.4"), ("2.25", "2.4"), ("1.5e3", "5WV.0"),
    ("3.75f", "3.Cf".replace("C", "V")), ("0x1.8p3", "1.8p3"), ("0x1p-2", "1p-2"), ("0x1p10", "1pL"),
    ("0.1", "0d0.1"), ("1e-3", "0d1e-3"), ("1e30", "327VY2734119W3Y7L9p1P"), ("0.1f", "0d0.1f"), ("1.0", "1.0"),
]


def test_numbers():
    for c, v in NUMS:
        got = x4lib.number_c_to_view(c)
        check(got == v, "number c->c4  %-8s -> %-7s (got %s)" % (c, v, got))
    back = [("V", "12"), ("FF", "255"), ("0o17", "017"), ("1.8", "1.5"), ("5WV.0", "1500.0"), ("0d0.1", "0.1"),
            ("1pL", "1024.0"), ("1e2", "256.0"), ("FFul", "255ul"), ("1.8p3", "12.0"), ("0.1", "0.0625")]
    for v, c in back:
        got = x4lib.number_view_to_c(v)
        check(got == c, "number c4->c  %-8s -> %-7s (got %s)" % (v, c, got))
    check(x4lib.number_view_to_c("1.8p3", float_style="hex") == "0x1.8p3", "hex float style keeps hex")
    check(x4lib.number_view_to_c("FF", hex_ints=True) == "0xff", "hex ints option")


def test_lint():
    bad = "int fooBar = 1; int MAX_LEN = 2; long x = 5L; wchar_t *s = L\"a\";\n"
    msgs = [m for _, _, m in x4lint.lint_ascii(bad)]
    check(any("camelCase" in m for m in msgs), "ascii lint finds camelCase")
    check(any("MAX_LEN" in m for m in msgs), "ascii lint finds capital macro")
    check(any("suffix" in m for m in msgs), "ascii lint finds upper-case suffix")
    check(any("prefix L" in m for m in msgs), "ascii lint finds L prefix")
    try:
        x4lib.c_to_x4("int fooBar;")
        check(False, "c2x4 rejects capitals without --snake")
    except x4lib.X4Error:
        check(True, "c2x4 rejects capitals without --snake")
    out, ren = x4lib.c_to_x4("int fooBar; int HTTPServer;", snake=True)
    check(out == b"int foo_bar; int http_server;" or x4lib.raw_to_view(out) == "int foo_bar; int http_server;".replace(";", ";"),
          "c2x4 --snake renames to snake_case")
    try:
        x4lib.c_to_x4("int fooBar; int foo_bar;", snake=True)
        check(False, "snake collision detected")
    except x4lib.X4Error:
        check(True, "snake collision detected")
    raw_bad = b"int a\x3c;\x80 \"open\n"
    msgs = [m for _, s, m in x4lint.lint_raw(raw_bad) if s == "error"]
    check(len(msgs) >= 2, "raw lint finds glued digit / bad byte / unterminated string")


def test_golden(update):
    srcs = sorted(glob.glob(os.path.join(HERE, "src", "*.c")))
    os.makedirs(os.path.join(HERE, "view"), exist_ok=True)
    tmp = tempfile.mkdtemp()
    have_gcc = shutil.which("gcc") is not None
    for src in srcs:
        name = os.path.splitext(os.path.basename(src))[0]
        text = open(src, encoding="utf-8").read()
        c4, _ = x4lib.c_to_x4(text)
        view = x4lib.raw_to_view(c4).encode("utf-8")
        gold, goldv = os.path.join(HERE, name + ".c4"), os.path.join(HERE, "view", name + ".c4v")
        if update:
            open(gold, "wb").write(c4)
            open(goldv, "wb").write(view)
        check(os.path.exists(gold) and open(gold, "rb").read() == c4, "%s.c4 matches golden file" % name)
        check(os.path.exists(goldv) and open(goldv, "rb").read() == view, "view/%s.c4v matches golden file" % name)
        check(x4lib.view_to_raw(view.decode("utf-8")) == c4, "%s: unview(view(x)) == x" % name)
        res = x4lint.lint_raw(c4)
        check(not [r for r in res if r[1] == "error"], "%s.c4 passes x4lint" % name)
        check(not x4lint.lint_ascii(text), "src/%s.c passes x4lint --ascii" % name)
        back = x4lib.x4_to_c(c4)
        if have_gcc:
            exes = []
            for tag, code in (("orig", text.encode()), ("back", back)):
                cpath, exe = os.path.join(tmp, name + tag + ".c"), os.path.join(tmp, name + tag)
                open(cpath, "wb").write(code)
                r = subprocess.run(["gcc", "-std=gnu17", "-w", "-o", exe, cpath], capture_output=True)
                check(r.returncode == 0, "%s (%s) compiles with host gcc" % (name, tag))
                exes.append(exe)
            if all(os.path.exists(e) for e in exes):
                outs = [subprocess.run([e], capture_output=True).stdout for e in exes]
                check(outs[0] == outs[1], "%s: round trip prints the same output" % name)
    shutil.rmtree(tmp, ignore_errors=True)
    if not have_gcc:
        print("note: no host gcc, compile/run round trip skipped")


def main():
    update = "--update" in sys.argv
    test_tables()
    test_numbers()
    test_lint()
    test_golden(update)
    print("\n%d failure(s)" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
