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

count = 0
with open("input.txt") as fp:
    with open("output.txt", "w") as fp2:
        for line in fp:
            count += 1
            z = float(line.strip())
            f.predict()
            f.update(z)
            print(count, ' ', f.x[0][0])
            result = str(f.x[0][0]) + "\n"
            fp2.write(result)

