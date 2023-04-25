#include <stdio.h>
    int main()
{
        int a = 42;
        int* p_a = &a;
        int b = *p_a; 

        int c = b + 1;
        printf("%ld", (long int)p_a);
        return 0;
    }