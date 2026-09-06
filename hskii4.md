# hskii_konti Complete Glyph Mapping

## Complete Mapping Table

| kod | ascii | hskii | continuous | Meaning |
|-----|-------|-------|------------|---------|
| 48 | 0 | 0 | 0 | digit |
| 49 | 1 | 1 | 1 | digit |
| 50 | 2 | 2 | 2 | digit |
| 51 | 3 | 3 | 3 | digit |
| 52 | 4 | 4 | 4 | digit |
| 53 | 5 | 5 | 5 | digit |
| 54 | 6 | 6 | 6 | digit |
| 55 | 7 | 7 | 7 | digit |
| 56 | 8 | 8 | 8 | digit |
| 57 | 9 | 9 | 9 | digit |
| 58 | : | : | L | hex ten (10) |
| 59 | ; | ; | Y | hex yilewen (11) |
| 60 | < | < | V | hex twelw (12) |
| 61 | = | = | W | hex dblun (13) |
| 62 | > | > | P | hex purxn (14) |
| 63 | ? | ? | F | hex fiwxn (15) |
| 64 | @ | @ | _ | xndxrskor |
| 65 | A | A | x | अ (schwa) |
| 66 | B | B | a | ा (aa matra) |
| 67 | C | C | i | ि (i matra) |
| 68 | D | D | u | ु (u matra) |
| 69 | E | E | e | े (e matra) |
| 70 | F | F | o | ो (o matra) |
| 71 | G | G | N | ं (anusvara) |
| 72 | H | H | k | क (ka) |
| 73 | I | I | K | ख (kha) |
| 74 | J | J | g | ग (ga) |
| 75 | K | K | G | घ (gha) |
| 76 | L | L | c | च (cha) |
| 77 | M | M | C | छ (chha) |
| 78 | N | N | z | ज (ja) |
| 79 | O | O | Z | झ (jha) |
| 80 | P | P | t | ट (ta) |
| 81 | Q | Q | T | ठ (tha) |
| 82 | R | R | d | ड (da) |
| 83 | S | S | D | ढ (dha) |
| 84 | T | T | j | त (ta) |
| 85 | U | U | J | थ (tha) |
| 86 | V | V | q | द (da) |
| 87 | W | W | Q | ध (dha) |
| 88 | X | X | n | न (na) |
| 89 | Y | Y | p | प (pa) |
| 90 | Z | Z | f | फ (pha) |
| 91 | [ | [ | b | ब (ba) |
| 92 | \ | \ | B | भ (bha) |
| 93 | ] | ] | m | म (ma) |
| 94 | ^ | ^ | y | य (ya) |
| 95 | _ | _ | r | र (ra) |
| 96 | ` | ` | R | ड़ (rra) |
| 97 | a | a | l | ल (la) |
| 98 | b | b | w | व (va) |
| 99 | c | c | s | स (sa) |
| 100 | d | d | S | श (sha) |
| 101 | e | e | v | ह (ha) |
| 102 | f | f | == | is-equal-to |
| 103 | g | g | != | not-equal-to |
| 104 | h | h | >= | greater-equal |
| 105 | i | i | <= | less-equal |
| 106 | j | j | && | logical-and |
| 107 | k | k | || | logical-or |
| 108 | l | l | ++ | increment |
| 109 | m | m | -- | decrement |
| 110 | n | n | @ | at-sign |
| 111 | o | o | # | hash |
| 112 | p | p | $ | dollar |
| 113 | q | q | % | percent |
| 114 | r | r | & | ampersand |
| 115 | s | s | * | asterisk |
| 116 | t | t | + | plus |
| 117 | u | u | - | minus |
| 118 | v | v | = | equals |
| 119 | w | w | / | slash |
| 120 | x | x | \ | backslash |
| 121 | y | y | | | pipe |
| 122 | z | z | ~ | tilde |
| 123 | { | { | ( | left-paren |
| 124 | | | | | ) | right-paren |
| 125 | } | } | [ | left-bracket |
| 126 | ~ | ~ | ] | right-bracket |
| 127 | | | { } | braces |

## Vowel Matras

| continuous | Hindi | Type |
|------------|-------|------|
| x | अ | standalone |
| a | ा | matra |
| i | ि | matra |
| u | ु | matra |
| e | े | matra |
| o | ो | matra |
| N | ं | anusvara |

## Key Features

1. Complete Hindi phoneme coverage
2. Dedicated hex digits (L,Y,V,W,P,F)
3. Programming symbols at 102-109
4. All ASCII symbols remapped at 110-127
5. @ replaced with _ (xndxrskor)
6. Single case system

## References

- Font: https://github.com/zawa8/font/tree/main/ttf/hscii
- Keyboard: https://github.com/zawa8/xNglobord
- Rust implementation: https://github.com/zawa8/plong
- cpp4 compiler: https://github.com/zawa8/cpp4-gcc