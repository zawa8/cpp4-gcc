# tools/x4 - c4 source tools (roadmap phase 1)

Pure python3 (no dependencies). Lets us write and test c4 without typing in the x4e font.

| file | what |
|---|---|
| `x4lib.py` | xskii4 tables, tokenizers, number conversion (shared code) |
| `x4conv.py` | `c2x4` ASCII C -> raw c4, `x42c` raw c4 -> ASCII C, `view` raw -> readable text, `unview` readable text -> raw |
| `x4lint.py` | lint raw c4, or `--ascii` ASCII C before conversion (capitals, camelCase, L/U prefixes) |

Three forms of the same program:

* **ASCII C** - normal C, snake_case, used to port/test (`tests/c4/src/*.c`).
* **raw c4** - the bytes in a `.c4` file (`tests/c4/*.c4`). `=` is byte 0x44, `;` is 0x42, digit 12 is 0x3C ...
* **view** - readable text of the raw bytes, what x4e.ttf shows (`tests/c4/view/*.c4v`). You can type c4 in this form in any
  editor and convert it with `x4conv.py unview`: `L Y V W P F` are digits 10..15, `: ; < = > ?` are the shifted punctuation,
  the 20 symbols (`!= <= >= ...`) are shown as unicode. There are no other capitals.

```
python3 tools/x4/x4conv.py c2x4 tests/c4/src/arith.c -o /tmp/arith.c4
python3 tools/x4/x4conv.py view /tmp/arith.c4
python3 tools/x4/x4conv.py x42c /tmp/arith.c4 | gcc -x c -o /tmp/arith -
python3 tools/x4/x4lint.py --ascii my_port.c
python3 tests/c4/run_tests.py
```

## Conversion rules (decided in Claude.md, plus marked assumptions)

* ASCII `: ; < = > ?` outside strings/comments become bytes 0x41-0x46 (**assumed order**, Claude.md sec 9 q2).
* Every integer is rewritten in hex digits `0-9 L Y V W P F`: `12` -> `V`, `255` -> `FF`, `0xff` -> `FF`, `017` -> `0o17`, `0b101` stays.
* Floats: exact binary values become hex literals (`1.5` -> `1.8`, `1.5e3` -> `5WV.0`, `0x1.8p3` -> `1.8p3`; `p` = power of 2, exponent digits hex);
  values that are not exact in hex digits stay decimal with the prefix `0d` (`0.1` -> `0d0.1`).
* Literal suffixes are lower case (`ul`, `ll`, `f`). Prefix `L`/`U` on strings does not exist (no capitals): use `u8`/`u`.
* Strings, character literals and comments keep their **raw bytes** (Claude.md sec 6): the program prints the same bytes at run time,
  but the x4e font shows capitals/punctuation inside them as other glyphs. (Open question 7.)
* Identifiers with capitals are an error; `--snake` renames (`fooBar` -> `foo_bar`, `MAX_LEN` -> `max_len`, `--rename-map` saves the list) and reports collisions.
* Bytes 0x47-0x5A (the 20 symbols) are not accepted by `x42c` yet and give a lint warning (open question 5).
