#include <stdio.h>

/* every shifted punctuation byte  : ; < = > ?  appears outside strings */
static int pick(int x)
{
    switch (x) {
    case 1:
        return 10;
    default:
        break;
    }
    return x > 3 ? x << 1 : x >= 2 ? 7 : 0;
}

int main(void)
{
    int i = 0, total = 0;
    for (i = 0; i < 6; i++) {
        if (i != 4 && i <= 5)
            total += pick(i);
    }
loop:
    total -= 1;
    if (total > 100)
        goto loop;
    printf("total=%d ok:%s<>?;\n", total, "yes");
    return 0;
}
