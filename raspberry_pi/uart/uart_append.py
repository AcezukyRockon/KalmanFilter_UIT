# source: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c

import serial
from time import sleep
import numpy as np

size = 10 # array size
arr = np.array([]) # declare numpy array
ser = serial.Serial ("/dev/ttyS0", 115200)  	  # Open port with baud rate
while True:
	received_data = ser.read()                    # read serial port
	sleep(0.03)
	data_left = ser.inWaiting()                   # check for remaining byte
	received_data += ser.read(data_left)
	arr = np.append(arr,float(received_data))     # append sample to numpy array
	print("shape: ",np.shape(arr)[0])	            # print size of the array
	if(np.shape(arr)[0]==10):		                  # if array size = 10, print, delete and recreate new array
		print(arr)
		del arr
		arr = np.array([])
    
