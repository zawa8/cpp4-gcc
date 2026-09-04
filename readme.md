# cpp4-gcc

cpp4 compiler - GCC fork for hskii encoding.

## About

cpp4 is a C++ variant that uses:
- **cplong** instead of float (arbitrary-precision numbers)
- **hskii hex digits** (L,Y,V,W,P,F)
- **hskii programming symbols** (E,U,I,O,M,X,A,H)

## Key Features

- Float-less (no float/double)
- Overflow-less (unlimited precision via cplong)
- hskii phonetic encoding support

## Status

Development in progress. Based on GCC 5.4.0.

## References

- hskii encoding: https://github.com/zawa8/vskii_rust4
- Keyboard: https://github.com/zawa8/xNglobord
- Number system: https://github.com/zawa8/plong
