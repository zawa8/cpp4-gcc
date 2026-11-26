#include <stdio.h>

struct point_pair { int left_x; int right_y; };

static int sum_pair(struct point_pair p) { return p.left_x + p.right_y; }

int main(void)
{
    struct point_pair my_pair = { 7, 9 };
    int arr[4] = { 1, 2, 3, 4 };
    int idx, acc = 0;
    for (idx = 0; idx < 4; idx++)
        acc += arr[idx];
    printf("%d %d\n", sum_pair(my_pair), acc);
    return 0;
}
