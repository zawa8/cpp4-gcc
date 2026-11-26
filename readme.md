# cpp4-gcc

GCC fork for the **xskii4** encoding: the **c4** language (and later cpp4).

> Source snapshot: GCC **17.0.0** development trunk (`gcc/BASE-VER`), branch `master`.
> (Older text in this file said "GCC 5.4.0": that was wrong, the tree is current trunk.)

## What is c4

c4 is C, written in the **xskii4** encoding with the font `x4e.ttf`
(built from `x4e.sfd` in <https://github.com/zawa8/xfont>), with these differences:

1. **4 fingers + 1 thumb maths by default.** Numbers are base 16 by default:
   `4*4 = 10 = 8+8`, and `10 = F+1 = P+2 = W+3 = V+4 = Y+5 = L+6`.
   Hex digits 10..15 are the glyphs `L Y V W P F` (continuous after `0-9`).
2. **No capital letters `A-Z`, no camelCase.** The byte range `A-Z` carries other glyphs
   (see below), so identifiers cannot contain capitals.
3. **snake_case only.** Identifiers are `[a-z0-9_]`.
4. **Regex (regeks) is different**, because the metacharacters sit at other byte values in xskii4.

Everything else (keywords, statements, types, preprocessor) is meant to stay as close to C as possible.

## xskii4 in one table

| bytes (ASCII value) | glyph shown by x4e.ttf | meaning in c4 |
|---|---|---|
| `0-9` (0x30-0x39) | `0-9` | digits 0-9 |
| `:;<=>?` (0x3A-0x3F) | `L Y V W P F` | hex digits 10..15 |
| `A-F` (0x41-0x46) | `: ; < = > ?` | punctuation shifted here |
| `G-Z` (0x47-0x5A) | 20 programming symbols | see `Claude.md` |
| `a-z` (0x61-0x7A) | `a-z` | letters, snake_case |

Why these choices (hex digits, no capitals, `x` = अ): **[benefits_of_xskii4_c4.md](benefits_of_xskii4_c4.md)**.

Detailed spec, design decisions, roadmap and open questions: **[Claude.md](Claude.md)**
(written so that a new Claude session can continue the work).

## Status

Early. Done: GCC trunk imported, design written down (`Claude.md`), phase 1 tools: converter + linter in `tools/x4/`, tests in `tests/c4/` (`python3 tests/c4/run_tests.py`).
Not done: CI build, libcpp xskii4 mode, hex-default literals, headers, regex.
See the roadmap in `Claude.md` and the older log in `progres.md`.

## Files written by the project owner

| file | what |
|---|---|
| `ascii5_hskii4.md` | older "hskii/4fskii" glyph table (different from xskii4, see Claude.md section 4) |
| `pl8_float_heksflot.md` | pl8 / cplong vs float comparison |
| `progres.md` | earlier development log (cpp4 + cplong idea) |
| `simbxls_hski4.md` | empty placeholder |

## References

- Fonts and xskii4 tooling: <https://github.com/zawa8/xfont>
- Keyboard: <https://github.com/zawa8/xNglobord>
- Number system (Rust): <https://github.com/zawa8/plong>
- hskii encoding: <https://github.com/zawa8/vskii_rust4>

---

# cplong

hskii arbitrary-precision number system (base-256 with hex-pair digits).

## Format

```

-2P,5V,67,5V.67.78.89

```

- `-` = negative sign
- Comma `,` separates integer digits
- Period `.` separates fractional digits
- Each digit = one u8 (0-255, displayed as hex pair)

## Hex Digits

| hskii | Value |
|-------|-------|
| 0-9 | 0-9 |
| L | 10 |
| Y | 11 |
| V | 12 |
| W | 13 |
| P | 14 |
| F | 15 |

## Usage

```rust
use cplong::Cplong;

fn main() {
    let a = Cplong::from_str("5V").unwrap();
    let b = Cplong::from_str("-6").unwrap();
    let d = a.sub(&b).unwrap();
    println!("{} - {} = {}", a, b, d);
}
```

Structure

```cpp
class cplong {
    u8 wlyu[];              // array of digits (base-256)
    s8 start_prisizxn_leyr; // starting precision level
    bool is_negetiw;        // negative flag
}
```

cplong has dedicated digits for last siks heksadesiml dizits:
1. L as ten
2. Y xz yilewen
3. V xz twelw
4. W xz dblun=8+5
5. P xz purxn=8+6
6. F xz fiwxn=8+7

so  8+8=10=4*4=F+1=P+2=W+3=V+4=Y+5=L+6.

```
class cplong{ // zust c++ pseudo code

public :
u8 wlyu[];
s8 start_prisizxn_leyr;
bool is_negetiw;

public static:
s8 _meksimun_saiz_of_wlyu_array_ ;

}

s8 main() {

cplong._meksimun_saiz_of_wlyu_array_ = 8 ;
cplong bign("-5V,FF,5V.4.4.5V");
//bign.is_negetiw is 1 so negetiw 
//bign.start_prisizxn_leyr is -2
//bign is -(5V*100+FF*10+5V+4/10+4/100+5V/1000)

cplong a([5V],1,0)//same as float a= 5.75
// a.wlyu is [5V] , a.start_prisizxn_leyr is 1
// a.is_negetiw is 0 so a is pozitiw

cplong a2([5,V],0,0)//same as float a= 5.75
// a2.wlyu is u8 array  [5,V]
// a2.start_prisizxn_leyr is 0
// for nekst u8 number V  prisizxn_leyr is 0+1
// a2.is_negetiw is 0 so a2 is pozitiw
// a2 is 5 + V/(F+1)



cplong a1([4,4,0,4],0,1);// cplong a1("4.4.0.4",0,1)
// à1.wlyu is 4+4/10+4/1000
// à1.start_prisizxn_leyr is 0
// à1 prisizxn_leyrs are 0,1,2,3
// a1.is_negetiw is 1 so a1 is negetiw

cplong b([6],0,0)//same as float b = 6
// a.wlyu is [6] , b.start_prisizxn_leyr is 0
// b.is_negetiw is 0 so b is pozitiw

cplong d = a - b;
// d wil bi = ("4",1,1)

}
```

## References

- hskii encoding: https://github.com/zawa8/vskii_rust4
- Keyboard: https://github.com/zawa8/xNglobord
- Number system: https://github.com/zawa8/plong
