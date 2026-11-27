#include <stdio.h>

/* lexer test: every operator, preprocessor forms, only single-digit numbers */
#define str(x) #x
#define cat(a, b) a ## b
#define twice(x) ((x) + (x))
#if 1
static int sel = 1;
#else
static int sel = 2;
#endif
#ifdef never_defined
static int dead = 3;
#endif

struct node { int val; struct node *next; };

static int ops(int a, int b)
{
    int r = 0;
    r += a; r -= b; r *= 2; r /= 3; r %= 5;
    r &= 7; r |= 1; r ^= 3; r <<= 1; r >>= 1;
    r = a << 1 | b >> 1 & 3 ^ 5;
    r = (a < b) + (a > b) + (a <= b) + (a >= b) + (a == b) + (a != b);
    r = (a && b) + (a || b) + !a + ~b;
    r = a ? b : sel;
    r++; --r;
    return r;
}

int main(void)
{
    struct node n = { 4, 0 };
    struct node *p = &n;
    int arr[3] = { 1, 2, 3 };
    int i = cat(1, 2) > 0 ? 5 : 6;
    char c1 = ':', c2 = ';', c3 = '<', c4 = '=', c5 = '>', c6 = '?';
    const char *s = "capitals ABC and punctuation :;<=>? stay raw";
    /* comment with ABC and :;<=>? */
    // line comment ABC :;<=>? \
       continued ABC
    printf("%s %d %d %d\n", str(a<b), twice(i), p->val, ops(arr[1], arr[2]));
    printf("%s %c%c%c%c%c%c\n", s, c1, c2, c3, c4, c5, c6);
    return arr[0] - 1;
}
