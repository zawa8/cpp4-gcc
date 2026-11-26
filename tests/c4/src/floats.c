#include <stdio.h>

int main(void)
{
    double a = 1.5;         /* exact: 1.8 in c4 */
    double b = 0.5;
    double c = 2.25;
    double d = 1.5e3;       /* 1500.0 exact */
    double e = 0.1;         /* not exact in hex digits: stays 0d0.1 */
    float f = 3.75f;
    double g = 0x1.8p3;     /* hex float, exponent is decimal in C */
    double h = 0x1p-2;
    double i = 1e-3;        /* not dyadic: 0d1e-3 */
    printf("%g %g %g %g %g %g %g %g %g\n", a, b, c, d, e, (double)f, g, h, i);
    return 0;
}
