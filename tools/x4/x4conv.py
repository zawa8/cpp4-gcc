#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""x4conv - convert between ASCII C and c4 (xskii4 bytes).

  x4conv.py c2x4  in.c    [-o out.c4] [--snake] [--rename-map map.json]
  x4conv.py x42c  in.c4   [-o out.c]  [--hex-ints] [--float-style decimal|hex]
  x4conv.py view  in.c4   [-o out.txt]     raw bytes -> readable text (what x4e.ttf shows)
  x4conv.py unview in.txt [-o out.c4]      readable text -> raw bytes (type c4 in any editor)

Use '-' for stdin/stdout. Details: tools/x4/README.md and Claude.md.
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x4lib  # noqa: E402


def read_in(path):
    return sys.stdin.buffer.read() if path == "-" else open(path, "rb").read()


def write_out(path, data):
    if path in (None, "-"):
        sys.stdout.buffer.write(data)
    else:
        with open(path, "wb") as f:
            f.write(data)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("c2x4", "x42c", "view", "unview"):
        p = sub.add_parser(name)
        p.add_argument("input")
        p.add_argument("-o", "--output")
        if name == "c2x4":
            p.add_argument("--snake", action="store_true", help="rename camelCase/CAPITAL identifiers to snake_case")
            p.add_argument("--rename-map", help="write the renames done by --snake to this json file")
        if name == "x42c":
            p.add_argument("--hex-ints", action="store_true", help="print integers as 0x.. instead of decimal")
            p.add_argument("--float-style", choices=("decimal", "hex"), default="decimal")
    a = ap.parse_args(argv)
    data = read_in(a.input)
    try:
        if a.cmd == "c2x4":
            out, renames = x4lib.c_to_x4(data.decode("utf-8"), snake=a.snake)
            if a.rename_map:
                with open(a.rename_map, "w") as f:
                    json.dump(renames, f, indent=1, sort_keys=True)
        elif a.cmd == "x42c":
            out = x4lib.x4_to_c(data, a.hex_ints, a.float_style)
        elif a.cmd == "view":
            out = x4lib.raw_to_view(data).encode("utf-8")
        else:
            out = x4lib.view_to_raw(data.decode("utf-8"))
    except x4lib.X4Error as e:
        for line, msg in e.problems:
            print("%s:%s: error: %s" % (a.input, line or "-", msg), file=sys.stderr)
        return 1
    write_out(a.output, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
