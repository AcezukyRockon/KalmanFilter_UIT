"""
Connect a resistor and LED to board pin 8 and run this script.
Whenever you say "stop", the LED should flash briefly
"""

import sounddevice as sd
from filterpy.kalman import KalmanFilter
import numpy as np
import scipy.signal
import timeit
import python_speech_features
import RPi.GPIO as GPIO

from tflite_runtime.interpreter import Interpreter

# Parameters
debug_time = 0
debug_acc = 0
led_pin = 8
word_threshold = 0.98
rec_duration = 0.5
window_stride = 0.5
sample_rate = 48000
resample_rate = 8000
num_channels = 1
num_mfcc = 16
#model_path = 'wake_word_stop_lite.tflite'
model_path = 'model_lite_softmax.tflite'

# Kalman filter parameters
f = KalmanFilter (dim_x=2, dim_z=1)             # First construct the object with the required dimensionality
f.x = np.array([[2.],[0.]])                     # Assign the initial value for the state
f.F = np.array([[1.,1.],[0.,1.]])               # state transition matrix
f.H = np.array([[1.,0.]])                       # Define the measurement function
f.P = np.array([[1000.,0.],[0., 1000.] ])       # Define the covariance matrix
f.R = np.array([[5.]])                          # Assign the measurement noise (dimension 1x1)
from filterpy.common import Q_discrete_white_noise
f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

# Sliding window
window = np.zeros(int(rec_duration * resample_rate) * 2)

# GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Load model (interpreter)
interpreter = Interpreter(model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)

# Decimate (filter and downsample)
def decimate(signal, old_fs, new_fs):
    
    # Check to make sure we're downsampling
    if new_fs > old_fs:
        print("Error: target sample rate higher than original")
        return signal, old_fs
    
    # We can only downsample by an integer factor
    dec_factor = old_fs / new_fs
    if not dec_factor.is_integer():
        print("Error: can only decimate by integer factor")
        return signal, old_fs

    # Do decimation
    resampled_signal = scipy.signal.decimate(signal, int(dec_factor))

    return resampled_signal, new_fs

# This gets called every 0.5 seconds
def sd_callback(rec, frames, time, status):
    GPIO.output(led_pin, GPIO.LOW)
    print('loop counter: --------------------------------------------------------------------------')
    # print('rec original: ',rec)
    # print("np shape rec: ", np.shape(rec))
            
    # Start timing for testing
    start = timeit.default_timer()
    
    # Notify if errors
    if status:
        print('Error:', status)
    
    # Remove 2nd dimension from recording sample
    rec = np.squeeze(rec)
    
    # Resample
    rec, new_fs = decimate(rec, sample_rate, resample_rate)
    # print('new rec and fs: ',rec,' ',new_fs)

    # Save recording onto sliding window
    window[:len(window)//2] = window[len(window)//2:]
    window[len(window)//2:] = rec
    print('window: ',window)
    print("type window: ", type(window))
    print("shape window: ", np.shape(window))
    
    # kalman filter process
#    window_kalman = np.zeros((np.shape(window)[0]))
#    for i in range(np.shape(window)[0]):
#        z = window[i]
#        # print(i, " ", z)
#        f.predict()
#        f.update(z)
#        window_kalman[i]=z - f.x[0][0]
#    print(window_kalman)
#    print("np shape window_kalman: ", np.shape(window_kalman))

    # Compute features
    mfccs = python_speech_features.base.mfcc(window, 
                                        samplerate=new_fs,
                                        winlen=0.256,
                                        winstep=0.050,
                                        numcep=num_mfcc,
                                        nfilt=26,
                                        nfft=2048,
                                        preemph=0.0,
                                        ceplifter=0,
                                        appendEnergy=False,
                                        winfunc=np.hanning)
    # print('mfcc before transpose: ',mfccs)
    mfccs = mfccs.transpose()
    # print('mfcc after transpose: ',mfccs)

    # Make prediction from model
    in_tensor = np.float32(mfccs.reshape(1, mfccs.shape[0], mfccs.shape[1], 1))
    # print('in_tensor: ',in_tensor)
    interpreter.set_tensor(input_details[0]['index'], in_tensor)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print('output_data: ',output_data)
    val_forward = output_data[0][0]
    val_yes = output_data[0][1]
    val_one = output_data[0][2]
    val_learn = output_data[0][3]
    val_right = output_data[0][4]
    val_go = output_data[0][5]
    val_backward = output_data[0][6]
    val_no = output_data[0][7]
    val_stop = output_data[0][8]
    val_left = output_data[0][9]

    if val_forward > word_threshold:
        print('forward')
        GPIO.output(led_pin, GPIO.HIGH)

    if val_yes > word_threshold:
        print('yes')

    if val_one > word_threshold:
        print('one')

    if val_learn > word_threshold:
        print('learn')

    if val_right > word_threshold:
        print('right')

    if val_go > word_threshold:
        print('go')

    if val_backward > word_threshold:
        print('backward')

    if val_no > word_threshold:
        print('no')

    if val_stop > word_threshold:
        print('stop')

    if val_left > word_threshold:
        print('left')

    if debug_acc:
        print(val)
    
    if debug_time:
        print(timeit.default_timer() - start)

# Start streaming from microphone
with sd.InputStream(channels=num_channels,
                    samplerate=sample_rate,
                    blocksize=int(sample_rate * rec_duration),
                    callback=sd_callback):
    while True:
        pass
