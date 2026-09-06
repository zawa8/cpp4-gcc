# pl8 (8-bit) vs float vs hexfloat

## Comparison

| Feature | pl8 (8-bit layers) | float | hexfloat |
|---------|-------------------|-------|----------|
| Layer size | 8 bits (1 byte) | N/A | N/A |
| Layer range | 0-255 | ±3.4e38 | ±3.4e38 |
| Base | 2^8 = 256 | 2 | 2 |
| Digits needed | Zyada | Fixed | Fixed |
| Memory per digit | 1 byte | 4 bytes | 4 bytes |
| Precision | Unlimited | Limited | Limited |
| Overflow | Impossible | Possible | Possible |
| Float errors | None | Yes | Yes |
| Speed | Slow | Fastest | Fast |
| Parsing | Simple | Simple | Simple |
| Display | Hex pairs (5V.FF) | Decimal | Hex mantissa |

## Detailed Analysis

### 1. pl8 (8-bit layers)
```cpp
pl8 a = -5VFFFF.5V5V5V;

pl8 b = 1 / 3;  // 0.5V5V5V... exact
```
- Simple parsing (each digit = 1 byte)
- Readable display (hex pairs like 5V, FF)
- Memory efficient
- Perfect for financial and scientific computing
- No overflow ever
- Exact arithmetic

### 2. float
```cpp
float f = 0.1 + 0.2;    // 0.30000001 (galat)

float g = 1.0 / 3.0;    // 0.33333334 (approximate)

float h = 1e38;         // overflow possible
```

- Fastest (hardware support)
- Precision loss issues
- Overflow possible
- IEEE 754 rounding errors

### 3. hexfloat (C++17)
```cpp
float h = 0x1.8p+3;     // = 12.0 exact binary

float h2 = 0x1.555556p-2; // approximate 1/3
```

- Fast (still hardware float)
- Easier to read exact binary values
- Same precision limits as float
- Same overflow issues

## Performance Comparison

| Operation | int | float | pl8 |
|-----------|-----|-------|-----|
| Addition | 1 cycle | 3 cycles | 100+ cycles |
| Multiplication | 3 cycles | 5 cycles | 500+ cycles |
| Division | 20 cycles | 50 cycles | 5000+ cycles |

## Memory Comparison

| Type | Memory | Example |
|------|--------|---------|
| float | 4 bytes | 3.14 |
| hex float | 4 bytes | 0x1.8p+3 |
| pl8 (1 digit) | 1 byte | 5V |
| pl8 (10 digits) | 10 bytes | 5V.FF.5V.FF.5V.FF.5V.FF.5V.FF |

## Use Case Recommendations

| Use Case | Best Choice |
|----------|-------------|
| Game physics | float |
| Real-time graphics | float |
| Financial calculation | pl8 |
| Scientific computing | pl8 |
| Cryptography | pl8 |
| Education | pl8 |
| General programming | float |
| High-precision maths | pl8 |

## Key Advantages of pl8

1. Float-less - No float/double needed
2. Overflow-less - Unlimited precision
3. Exact arithmetic - No IEEE 754 rounding errors
4. Simple format - Hex pairs like 5V, FF
5. Memory efficient - 1 byte per digit
6. No special hardware - Works on any CPU

## Key Disadvantages of pl8

1. Slow - Software arithmetic, not hardware
2. More digits - Large numbers need many layers
3. Not standard - No existing infrastructure

## Format Specification

pl8 a = -5VFFFF.5V5V5V;

-           = negative sign

5VFFFF      = integer part (4 hex pairs)

.           = decimal separator

5V5V5V      = fractional part (3 hex pairs)

### With explicit start_pl:

pl8 b = 5V.FF:-7;

5V          = first digit

FF          = second digit

:-7         = start precision layer (power of 16)

## Verdict

Use pl8 when precision is most important.

Use float when speed is most important.

Use hexfloat when you need exact binary float representation.

## References

- Rust implementation: https://github.com/zawa8/plong/tree/komawim

- cpp4 compiler: https://github.com/zawa8/cpp4-gcc
