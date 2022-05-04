# source: 
# https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html
# https://www.w3schools.com/python/numpy/

from filterpy.kalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt

f = KalmanFilter (dim_x=2, dim_z=1)             # First construct the object with the required dimensionality
f.x = np.array([[2.],[0.]])                     # Assign the initial value for the state
f.F = np.array([[1.,1.],[0.,1.]])               # state transition matrix
f.H = np.array([[1.,0.]])                       # Define the measurement function
f.P = np.array([[1000.,0.],[0., 1000.] ])       # Define the covariance matrix
f.R = np.array([[5.]])                          # Assign the measurement noise (dimension 1x1)

# assign the process noise
from filterpy.common import Q_discrete_white_noise
f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

arr_i = np.loadtxt("input.txt")
arr_o = np.zeros((1000,1))
# print("arr_i-------------------------------------------------")
# print(arr_i)
# print(type(arr_i))
# print(np.shape(arr_i)[0])

with open("output.txt", "w") as fp2:
    for i in range(np.shape(arr_i)[0]):
        z = arr_i[i]
        # print(i, " ", z)
        f.predict()
        f.update(z)
        result = str(z - f.x[0][0]) + "\n"
        # result = str(f.x[0][0]) + "\n"
        fp2.write(result)
        arr_o[i,0]=f.x[0][0]
print("arr_o-------------------------------------------------")
print(arr_o)
