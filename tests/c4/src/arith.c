#include <stdio.h>

/* 4 fingers + 1 thumb: 4*4 = 10 (hex) = 16 (decimal) */
int main(void)
{
    int a = 4 * 4;      /* 16 decimal, 10 in c4 */
    int b = 12;         /* V in c4 */
    int c = 0xff;       /* FF in c4 */
    int d = 017;        /* 0o17 in c4 */
    int e = 0b101;
    unsigned long f = 255ul;
    printf("%d %d %d %d %d %lu\n", a, b, c, d, e, f);
    printf("%d\n", a + b * 2 - (c >> 4));
    return 0;
}
