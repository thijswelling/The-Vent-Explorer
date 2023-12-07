import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

CW = 1
CCW = 0
Dir_Motor1 = 20  # GPIO-pin voor de richting van motor 1
Stp_Motor1 = 21  # GPIO-pin voor de stap van motor 1

Dir_Motor2 = 10  # GPIO-pin voor de richting van motor 2
Stp_Motor2 = 11  # GPIO-pin voor de stap van motor 2

GPIO.setmode(GPIO.BCM)

# Instellingen voor motor 1
GPIO.setup(Dir_Motor1, GPIO.OUT)
GPIO.setup(Stp_Motor1, GPIO.OUT)
GPIO.output(Dir_Motor1, CW)

# Instellingen voor motor 2
GPIO.setup(Dir_Motor2, GPIO.OUT)
GPIO.setup(Stp_Motor2, GPIO.OUT)
GPIO.output(Dir_Motor2, CW)

try:
    while True:
        # Stapmotor 1
        GPIO.output(Stp_Motor1, GPIO.HIGH)
        time.sleep(.0001)
        GPIO.output(Stp_Motor1, GPIO.LOW)
        time.sleep(.0001)

        # Stapmotor 2
        GPIO.output(Stp_Motor2, GPIO.HIGH)
        time.sleep(.0001)
        GPIO.output(Stp_Motor2, GPIO.LOW)
        time.sleep(.0001)

except KeyboardInterrupt:
    GPIO.cleanup()
