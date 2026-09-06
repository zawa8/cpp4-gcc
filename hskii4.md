# hskii Continuous Glyph Mapping

## Overview

Ye file ASCII characters (48-127) ko hskii continuous glyphs me map karti
hai. Continuous glyphs handwriting/cursive style ke liye hain.

## Format

| Column | Meaning |
|--------|---------|
| kod | ASCII code point |
| ascii_glyph | Standard ASCII character |
| hskii_glyph | hskii font glyph |
| hskii_continuous_glyph | continuous handwriting glyph |

## Digits (48-57)

| kod | ascii | hskii | continuous |
|-----|-------|-------|------------|
| 48 | 0 | 0 | 0 |
| 49 | 1 | 1 | 1 |
| 50 | 2 | 2 | 2 |
| 51 | 3 | 3 | 3 |
| 52 | 4 | 4 | 4 |
| 53 | 5 | 5 | 5 |
| 54 | 6 | 6 | 6 |
| 55 | 7 | 7 | 7 |
| 56 | 8 | 8 | 8 |
| 57 | 9 | 9 | 9 |

## Hex Digits (58-63)

| kod | ascii | continuous | Meaning |
|-----|-------|------------|---------|
| 58 | : | L | ten (10) |
| 59 | ; | Y | yilewen (11) |
| 60 | < | V | twelw (12) |
| 61 | = | W | dblun (13) |
| 62 | > | P | purxn (14) |
| 63 | ? | F | fiwxn (15) |

## Vowels (65-73)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 65 | A | x | अ (schwa) |
| 66 | B | a | ा (aa matra) |
| 67 | C | i | ि (i matra) |
| 68 | D | u | ु (u matra) |
| 69 | E | e | े (e matra) |
| 70 | F | o | ो (o matra) |
| 71 | G | N | ं (anusvara) |
| 72 | H | k | क (ka) |
| 73 | I | K | ख (kha) |

## Velar Consonants (74-75)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 74 | J | g | ग (ga) |
| 75 | K | G | घ (gha) |

## Palatal Consonants (76-79)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 76 | L | c | च (cha) |
| 77 | M | C | छ (chha) |
| 78 | N | z | ज (ja) |
| 79 | O | Z | झ (jha) |

## Retroflex Consonants (80-83)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 80 | P | t | ट (ta) |
| 81 | Q | T | ठ (tha) |
| 82 | R | d | ड (da) |
| 83 | S | D | ढ (dha) |

## Dental Consonants (84-88)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 84 | T | j | त (ta) |
| 85 | U | J | थ (tha) |
| 86 | V | q | द (da) |
| 87 | W | Q | ध (dha) |
| 88 | X | n | न (na) |

## Labial Consonants (89-93)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 89 | Y | p | प (pa) |
| 90 | Z | f | फ (pha) |
| 91 | [ | b | ब (ba) |
| 92 | \ | B | भ (bha) |
| 93 | ] | m | म (ma) |

## Semivowels and Sibilants (94-101)

| kod | ascii | continuous | Hindi |
|-----|-------|------------|-------|
| 94 | ^ | y | य (ya) |
| 95 | _ | r | र (ra) |
| 96 | ` | R | ड़ (rra) |
| 97 | a | l | ल (la) |
| 98 | b | w | व (va) |
| 99 | c | s | स (sa) |
| 100 | d | S | श (sha) |
| 101 | e | v | ह (ha) |

## Special (64)

| kod | ascii | continuous | Meaning |
|-----|-------|------------|---------|
| 64 | @ | _ | spes |

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

1. Continuous glyphs hskii font me cursive/handwriting style ke liye
2. Hex digits L,Y,V,W,P,F dedicated hain
3. Vowels aur consonants ka complete mapping
4. @ ko _ se map kiya gaya hai (spes)

## References

- Font: https://github.com/zawa8/font/tree/main/ttf/hscii
- Keyboard: https://github.com/zawa8/xNglobord
- Rust implementation: https://github.com/zawa8/plong/tree/komawim