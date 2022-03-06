/** A simple kalman filter example by Adrian Boeing 
 www.adrianboeing.com 
 */ 
// Sources: https://gist.github.com/jannson/9951716

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double frand() {
    return 2*((rand()/(double)RAND_MAX) - 0.5);
}

int main() {
    int i;
    FILE *fptr;
    FILE *fptr2;

    //initial values for the kalman filter
    float x_est_last = 0;
    float P_last = 0;
    //the noise in the system
    float Q = 0.022;
    float R = 0.617;
    
    float K;
    float P;
    float P_temp;
    float x_temp_est;
    float x_est;
    float z_measured; //the 'noisy' value we measured
    float z_real = 0.5; //the ideal value we wish to measure
    float minus, result;
    
    srand(0);
    
    //initialize with a measurement
    x_est_last = 0;

    fptr = fopen("input.txt","r");
    fptr2 = fopen("result.txt","w");
    
    for (i=0;i<576029;i++) {
        //do a prediction
        x_temp_est = x_est_last;
        P_temp = P_last + Q;
        //calculate the Kalman gain
        K = P_temp * (1.0/(P_temp + R));
        //measure
        fscanf(fptr, "%f", &z_measured);  //the real measurement plus noise
        //correct
        x_est = x_temp_est + K * (z_measured - x_temp_est); // x_est = nhieu on thap
        P = (1- K) * P_temp;
        //we have our new system

        minus = z_measured - x_est;
        fprintf(fptr2, "%f\n", minus);
        
        //update our last's
        P_last = P;
        x_est_last = minus;
    }
   
    fclose(fptr2);
    fclose(fptr);
    return 0;
}
