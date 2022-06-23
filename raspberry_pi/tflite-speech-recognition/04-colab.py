"""
Connect a resistor and LED to board pin 8 and run this script.
Whenever you say "stop", the LED should flash briefly
Applied Kalman Filter at window
"""

import sounddevice as sd
from filterpy.kalman import KalmanFilter
import numpy as np
import scipy.signal
import timeit
import python_speech_features
import sqlite3
import time
from sqlite3 import Error
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep

from tflite_runtime.interpreter import Interpreter

# Parameters
debug_time = 0
debug_acc = 0
led_pin = 8
word_threshold = 0.6
rec_duration = 0.5
window_stride = 0.5
sample_rate = 48000
resample_rate = 8000
num_channels = 1
num_mfcc = 16
#model_path = 'wake_word_stop_lite.tflite'
model_path = 'model_lite_colab_vn.tflite'
database = r"pythonsqlite.db"
db_counter_yes = 0
db_counter_no = 0

# Kalman filter parameters----------------------------------------------
#f = KalmanFilter (dim_x=2, dim_z=1)             # First construct the object with the required dimensionality
#f.x = np.array([[2.],[0.]])                     # Assign the initial value for the state
#f.F = np.array([[1.,1.],[0.,1.]])               # state transition matrix
#f.H = np.array([[1.,0.]])                       # Define the measurement function
#f.P = np.array([[1000.,0.],[0., 1000.] ])       # Define the covariance matrix
#f.R = np.array([[5.]])                          # Assign the measurement noise (dimension 1x1)
#from filterpy.common import Q_discrete_white_noise
#f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)
# intial parameters
n_iter = 8000
sz = (n_iter,) # size of array
x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
#z = np.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)
#Q = 1e-5 # process variance
Q = 1000
# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # gain or blending factor
R =10**2 # estimate of measurement variance, change to see effect
# intial guesses
xhat[0] = 0.0
P[0] = 1.0
result = np.zeros(sz)

# Sliding window--------------------------------------------------------
window = np.zeros(int(rec_duration * resample_rate) * 2)

# GPIO 
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

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
#sqlite-------------------------------------------------------------------------------------------------------------------------------------
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# ['xuong', 'len', 'lui', 'co', 'trai', 'dung', 'dong y', 'phai', 'khong']
# task
def update_task(conn, task):
    sql = ''' UPDATE tasks
              SET counter = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

# query counter from task
def query_task_counter(conn, task_name):
    cur = conn.cursor()
    cur.execute("SELECT counter FROM tasks WHERE name=?", (name,))

    rows = cur.fetchall()

    return row[0]


# xuong
def update_time_xuong(conn, counter):
    sql = ''' INSERT INTO xuong(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# len
def update_time_len(conn, counter):
    sql = ''' INSERT INTO len(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# lui
def update_time_lui(conn, counter):
    sql = ''' INSERT INTO lui(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# co
def update_time_co(conn, counter):
    sql = ''' INSERT INTO co(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# trai
def update_time_trai(conn, counter):
    sql = ''' INSERT INTO trai(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# dung
def update_time_dung(conn, counter):
    sql = ''' INSERT INTO dung(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid

# dongy
def update_time_dongy(conn, counter):
    sql = ''' INSERT INTO dongy(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid
    
# phai
def update_time_phai(conn, counter):
    sql = ''' INSERT INTO phai(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid
    
# khong
def update_time_khong(conn, counter):
    sql = ''' INSERT INTO khong(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid
    
# Pins for Motor Driver Inputs-------------------------------------------------------------------------
Motor1A = 24
Motor1B = 23
Motor1E = 25

Motor2A = 20
Motor2B = 16
Motor2E = 21

GPIO.setmode(GPIO.BCM)	# GPIO Numbering
GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(Motor1A,GPIO.LOW)
GPIO.setup(Motor1B,GPIO.LOW)
GPIO.setup(Motor2A,GPIO.LOW)
GPIO.setup(Motor2B,GPIO.LOW)

# This gets called every 0.5 seconds
def sd_callback(rec, frames, time, status):
    global db_counter_xuong, db_counter_len, db_counter_lui, db_counter_co, db_counter_trai, db_counter_dung, db_counter_dongy, db_counter_phai, db_counter_khong
    #GPIO.output(led_pin, GPIO.LOW)
#    print('loop counter: --------------------------------------------------------------------------')
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
#    print('window: ',window)
#    print("type window: ", type(window))
#    print("shape window: ", np.shape(window))

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
    for k in range(n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q
        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(window[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
        # result[k] = window[k] - xhat[k]

    # Compute features
    mfccs = python_speech_features.base.mfcc(xhat, 
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
    # ['xuong', 'len', 'lui', 'co', 'trai', 'dung', 'dong y', 'phai', 'khong']
    val_xuong = output_data[0][0]
    val_len = output_data[0][1]
    val_lui = output_data[0][2]
    val_co = output_data[0][3]
    val_trai = output_data[0][4]
    val_dung = output_data[0][5]
    val_dongy = output_data[0][6]
    val_phai = output_data[0][7]
    val_khong = output_data[0][8]
    #val_left = output_data[0][9]

    if val_trai > word_threshold:
        print('trai')
        #GPIO.output(led_pin, GPIO.HIGH)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)

    if val_phai > word_threshold:
        print('phai')
        # Load database
        conn = create_connection(database)
        with conn:
             db_counter_yes = query_task_counter(conn, "trai")
             db_counter_yes += 1
             update_time_yes(conn, (db_counter_yes,)) #update yes
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)

    if val_dung > word_threshold:
        print('dung')
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.LOW)

    if val_len > word_threshold:
        print('len')
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)

    if val_xuong > word_threshold:
        print('xuong')

    if val_co > word_threshold:
        print('co') # trai
        #GPIO.output(Motor1A,GPIO.LOW)
        #GPIO.output(Motor1B,GPIO.LOW)
        #GPIO.output(Motor2A,GPIO.LOW)
        #GPIO.output(Motor2B,GPIO.LOW)
        
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)

    if val_dongy > word_threshold:
        print('dongy')

    if val_khong > word_threshold:
        print('khong')
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.LOW)
        #db_counter_no += 1
        # Load database
        #conn = create_connection(database)
        #with conn:
        #    update_time_no(conn, (db_counter_no,)) #update no

    if val_lui > word_threshold:
        print('lui')
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)

    #if val_left > word_threshold:
    #    print('left')

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
        try:
            pass
        except KeyboardInterrupt:
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.LOW)
            GPIO.cleanup()
            print("gpio cleaned")
