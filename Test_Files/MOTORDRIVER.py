import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

CW=1
CCW=0
Dir=20
Stp = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(Dir, GPIO.OUT)
GPIO.setup(Stp, GPIO.OUT)

GPIO.output(Dir, CW)

while True:
    GPIO.output(Stp, GPIO.HIGH)
    time.sleep(.0001)
    GPIO.output(Stp, GPIO.LOW)
    time.sleep(.0001)