import RPi.GPIO as GPIO
from time import sleep

# Pins for Motor Driver Inputs
Motor1A = 24
Motor1B = 23
Motor1E = 25

Motor2A = 20
Motor2B = 16
Motor2E = 21

def setup():
    GPIO.setmode(GPIO.BCM)	# GPIO Numbering
    GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)

def loop():
    # Going forwards
    if x=='f':
        print("forward")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

    # Going backwards
    elif x=='b':
        print("backward")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

    # Going left
    elif x=='l':
        print("left")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

    # Going right
    elif x=='r':
        print("right")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

    # Stop
    elif x=='s':
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)

    elif x=='e':
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        destroy()

    else:
        print("Wrong input! Please enter f(forward) or b(backward) or s(stop) or e(stop and exit program)")

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
    setup()
    print("Enter f(forward) or b(backward) or s(stop) or e(stop and exit program)")
    while(1):
        x = input()
        try:
            loop()
        except KeyboardInterrupt:
            destroy()
