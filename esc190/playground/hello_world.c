/*
2. Implement a function that performs Insertion Sort https://en.wikipedia.org/wiki/Insertion_sort#Algorithm
   The function should take in an array of integers, and modify the array so that it's 
   sorted in increasing order.
*/

// Library imports
#include <stdio.h>
#include <stdlib.h>

void seq_replace(int *arr, unsigned long arr1_sz, int *arr2, unsigned long arr2_sz){
    int i, j;
    for (i = 0; i < arr1_sz; i++){
        int match = 0;
        for (j = 0; j < arr2_sz; j++){
            if (arr[i+j] == arr2[j]){
                match++;
            }
        }
        if (match == arr2_sz){
            for (j = 0; j < arr2_sz; j++){
                arr[i+j] = 0;
            }
        }
    }
}

int main(){
   int a[] = {5, 6, 7, 8, 6, 7};
   int b[] = {6,7};
   int *ptr_a;
   int *ptr_b;
   ptr_a = a;
   ptr_b = b;
   size_t size = sizeof(a)/sizeof(a[0]);

   for(int i = 0; i < size; i++){
      printf("%d ", a[i]);
   }
   printf("\n");

   seq_replace(a,6,b,2);

   for(int i = 0; i < size; i++){
      printf("%d ", a[i]);
   }
   printf("\n");
   printf("%zu\n", size);
}