#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""c4 phase 3 tests: xskii4 mode of libcpp, needs a built gcc4 driver.

  python3 tests/c4/run_lexer_tests.py build/gcc/xgcc -B build/gcc/

Differential test: for each sample, preprocess the raw .c4 golden file with -fxskii4 and the ASCII
source normally; the token streams (-E -P) must be identical (the xskii4 mode spells tokens in ASCII).
Then a compile smoke test and negative tests.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CC = sys.argv[1:] or ["gcc"]
fails = []


def check(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond:
        fails.append(what)


def run(args):
    return subprocess.run(CC + args, capture_output=True)


def main():
    for name in ("hello", "snake", "lexer"):
        c4 = os.path.join(HERE, name + ".c4")
        src = os.path.join(HERE, "src", name + ".c")
        a = run(["-x", "c", "-fxskii4", "-E", "-P", c4])
        b = run(["-x", "c", "-E", "-P", src])
        check(a.returncode == 0, "%s.c4: -E -fxskii4 succeeds %s" % (name, a.stderr.decode()[:200]))
        check(a.stdout == b.stdout and len(a.stdout) > 100, "%s: xskii4 token stream == ASCII token stream" % name)

    with tempfile.TemporaryDirectory() as tmp:
        s = os.path.join(tmp, "hello.s")
        r = run(["-x", "c", "-fxskii4", "-S", "-o", s, os.path.join(HERE, "hello.c4")])
        check(r.returncode == 0 and os.path.exists(s) and b"hello c4" in open(s, "rb").read(),
              "hello.c4 compiles to assembly containing the string %s" % r.stderr.decode()[:200])
        # negative tests: raw bytes written by hand
        cases = [
            ("symbol byte (0x48 'H' slot)", b"int a" + bytes([0x44]) + b"1" + bytes([0x42]) + b" int b" + bytes([0x48]) + bytes([0x42]) + b"\n", b"stray"),
            ("hex digit glued to name", b"int ab" + bytes([0x3C]) + bytes([0x42]) + b"\n", b"glued"),
        ]
        for what, data, word in cases:
            p = os.path.join(tmp, "neg.c4")
            open(p, "wb").write(data)
            r = run(["-x", "c", "-fxskii4", "-fsyntax-only", p])
            check(r.returncode != 0 and word in r.stderr, "negative: %s is an error" % what)
        # ASCII files must not be touched by -fxskii4 only through suffix: a .c file
        # that is not the main file keeps ASCII meaning (hello.c4 includes <stdio.h>, already covered above)
    print("\n%d failure(s)" % len(fails) if fails else "\nall lexer tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
