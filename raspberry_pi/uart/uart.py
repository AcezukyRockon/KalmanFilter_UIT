# source: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c

import serial
from time import sleep
import numpy as np

temp_size = 0
size = 10 # array size
arr = np.zeros(size) # declare numpy array
ser = serial.Serial ("/dev/ttyS0", 115200)  	  # Open port with baud rate
while True:
	received_data = ser.read()                    # read serial port
	sleep(0.03)
	data_left = ser.inWaiting()                   # check for remaining byte
	received_data += ser.read(data_left)
	arr[temp_size] = float(received_data)     # append sample to numpy array
	temp_size += 1
	# print(temp_size)	            # print size of the array
	if(temp_size==size):		                  # if array size = 10, print, delete and recreate new array
		#print(arr)
		print(np.shape(arr)[0])
		temp_size = 0

