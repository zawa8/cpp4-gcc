# cpp4-gcc: Development Log

## Project Status

**Date:** 2026-09-04

## Current Progress

| # | Task | Status |
|---|------|--------|
| 1 | Fork GCC repository | ✅ Done |
| 2 | README.md updated | ✅ Done |
| 3 | RID_CPLONG added to c-common.h | ✅ Done |
| 4 | "cplong" keyword added to c-common.cc | ✅ Done |
| 5 | Commit and push to master | ✅ Done |

## Changes Made

### 1. `gcc/c-family/c-common.h` (Line 100)

Added `RID_CPLONG` between `RID_FLOAT` and `RID_DOUBLE`:

```cpp
RID_INT,     RID_CHAR,   RID_FLOAT,    RID_CPLONG,   RID_DOUBLE, RID_VOID,
```

## Next Steps

- [ ] parser.cc: Handle RID_CPLONG in type specifier parsing
- [ ] typeck.cc: Add cplong type checking logic
- [ ] Build system: Enable cpp4 as new language
- [ ] Lexical changes for hskii hex digits (L,Y,V,W,P,F)
- [ ] Programming symbols mapping (E,U,I,O,M,X,A,H)

## Key Files

| File | Purpose |
|------|---------|
| gcc/c-family/c-common.h | Keyword IDs (RID_*) |
| gcc/c-family/c-common.cc | Keyword string to RID mapping |
| gcc/cp/parser.cc | C++ parser |
| gcc/cp/typeck.cc | Type checking |

## cpp4 Features

- **Float-less:** No float/double - only cplong
- **Overflow-less:** Unlimited precision via cplong
- **hskii hex digits:** L,Y,V,W,P,F
- **hskii programming symbols:** E,U,I,O,M,X,A,H

## References

- Repo: <https://github.com/zawa8/cpp4-gcc>
- hskii encoding: <https://github.com/zawa8/vskii_rust4>
- Number system: <https://github.com/zawa8/plong>
