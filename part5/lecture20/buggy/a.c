#include <stdio.h>

int foo() {
    return 2;
}

int main() {
    int f = foo();
    printf("%d\n", f);
    return 0;
}
