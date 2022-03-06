#include <stdio.h>
#include <stdlib.h>

int main(){
    float num;
    int i;
    FILE *fptr;
    FILE *fptr2;

    // use appropriate location if you are using MacOS or Linux
    fptr = fopen("input.txt","r");
    fptr2 = fopen("result.txt","w");

    for (i = 0; i < 16; i++){
        fscanf(fptr, "%f", &num);
        fprintf(fptr2, "%f\n", num);
    }

    fclose(fptr2);
    fclose(fptr);

    return 0;
}