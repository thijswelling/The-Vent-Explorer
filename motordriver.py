import RPi.GPIO as GPIO
import time

class MotorDriver:
    def _init_(self, delay=0.001, dir1_pin=20, dir2_pin=10, step1_pin=21, step2_pin=11, enable1_pin=4, enable2_pin=4):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.delay = delay
        self.dir1_pin = dir1_pin
        self.dir2_pin = dir2_pin

        self.step1_pin = step1_pin
        self.step2_pin = step2_pin

        self.enable1_pin = enable1_pin
        self.enable2_pin = enable2_pin

        GPIO.setup(self.dir1_pin, GPIO.OUT)
        GPIO.setup(self.dir2_pin, GPIO.OUT)

        GPIO.setup(self.step1_pin, GPIO.OUT)
        GPIO.setup(self.step2_pin, GPIO.OUT)

        GPIO.setup(self.enable1_pin, GPIO.OUT)
        GPIO.setup(self.enable2_pin, GPIO.OUT)

        GPIO.output(self.dir1_pin, GPIO.HIGH)  # Set de richting motor 1
        GPIO.output(self.dir2_pin, GPIO.HIGH)  # Set de richting motor 2

        self.hault = False
        self.step1 = 0
        self.step2 = 0


    def set_dir(self, dir1, dir2):
        if dir1 == 1:
            GPIO.output(self.dir1_pin, GPIO.HIGH)   # Forward
        elif dir1 == 0:
            GPIO.output(self.dir1_pin, GPIO.LOW)    # Backward

        if dir2 == 1:
            GPIO.output(self.dir2_pin, GPIO.HIGH)   # Forward
        elif dir2 == 0:
            GPIO.output(self.dir2_pin, GPIO.LOW)    # Backward

    def set_step(self, step1, step2):
        self.step1 = step1
        self.step2 = step2
        dir1 = 1 if step1 > 0 else 0
        dir2 = 1 if step2 > 0 else 0
        self.set_dir(dir1, dir2)

    def move(self, right=1, left=1):
        step1 = 0 if right == 0 else 100 * right
        step2 = 0 if left == 0 else 100 * left
        self.set_step(step1, step2)

    def hault_state(self, state=True):
        self.hault = state

    def drive_motor(self, forever=False):
        while 1:
            if self.hault == True:
                self.step1 = 0
                self.step2 = 0
                self.hault = False

            if self.step1 != 0:
                GPIO.output(self.step1_pin, GPIO.HIGH)
            if self.step2 != 0:
                GPIO.output(self.step2_pin, GPIO.HIGH)
            time.sleep(self.delay)

            if self.step1 != 0:
                GPIO.output(self.step1_pin, GPIO.LOW)
                self.step1 += -1 if self.step1 > 0 else 1
            if self.step2 != 0:
                GPIO.output(self.step2_pin, GPIO.LOW)
                self.step2 += -1 if self.step2 > 0 else 1
            time.sleep(self.delay)
            if not forever and self.step1 == 0 and self.step2 == 0:
                break

    def enable_motor(self):
        GPIO.output(self.enable1_pin, GPIO.LOW)
        GPIO.output(self.enable2_pin, GPIO.LOW)

    def disable_motor(self):
        GPIO.output(self.enable1_pin, GPIO.HIGH)
        GPIO.output(self.enable2_pin, GPIO.HIGH)

    def stop(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()

if __name__ == '__main__':
    m = MotorDriver()
    while 1:
        m.move(right=1, left=0)
        m.enable_motor()
        m.drive_motor()
        print("completed 1")
        m.move(right=0, left=1)
        m.enable_motor()
        m.drive_motor()
        print("completed 2")
        m.move(right=0, left=0)
        m.enable_motor()
        m.drive_motor()
        print("completed 3")
        m.move(right=1, left=1)
        m.enable_motor()
        m.drive_motor()
        print("completed 4")
        m.move(right=1, left=-1)
        m.enable_motor()
        m.drive_motor()
        print("completed 5")
        m.move(right=-1, left=1)
        m.enable_motor()
        m.drive_motor()
        print("completed 6")
        m.move(right=-1, left=0)
        m.enable_motor()
        m.drive_motor()
        print("completed 7")
        m.move(right=0, left=-1)
        m.enable_motor()
        m.drive_motor()
        print("completed 8")
        m.move(right=-1, left=-1)
        m.enable_motor()
        m.drive_motor()
        print("completed 9")

# import time
# class MotorDriverDumy:
#     def __init__(self):
#         pass
#
#     def set_step(self, step1, step2):
#         print(f"set step: {step1}, setp2: {step2}")
#
#     def move(self, right, left):
#         self.set_step(right, left)
#
#     def hault(self, state):
#         print(f"hault: {state}")
#
#     def drive_motor(self):
#         while 1:
#             print("driving motor")
#             time.sleep(1)
