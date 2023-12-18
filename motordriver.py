import time
import platform


if 'windows' in platform.system().lower():  # for testing on windows GPIO class

    class PWMPIN:
        def start(self, *args):
            pass

        def ChangeDutyCycle(self, *args):
            pass

    class RPIGPIO:
        def __init__(self):
            self.BCM = None
            self.HIGH = None
            self.LOW = None
            self.OUT = None
        def setwarnings(self, *args):
            pass

        def setmode(self, *args):
            pass

        def setup(self, *args):
            pass

        def output(self, *args):
            pass

        def cleanup(self, *args):
            pass

        def PWM(self, pin, frequency) -> PWMPIN:
            return PWMPIN()

    GPIO = RPIGPIO()
else:
    import RPi.GPIO as GPIO


class MotorDriver:
    def __init__(self, delay=0.001, dir1_pin=20, dir2_pin=10, step1_pin=21, step2_pin=11,
                 enable1_pin=4, enable2_pin=4, servo_pin=23, led_pin=22):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.delay = delay
        self.dir1_pin = dir1_pin
        self.dir2_pin = dir2_pin

        self.step1_pin = step1_pin
        self.step2_pin = step2_pin

        self.enable1_pin = enable1_pin
        self.enable2_pin = enable2_pin

        self.servo_pin = servo_pin
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.servo_pin, 50)
        self.servo_duty = 0
        self.servo_pwm.start(self.servo_duty)

        self.led_pin = led_pin
        GPIO.setup(self.led_pin, GPIO.OUT)
        self.led_pwm = GPIO.PWM(self.led_pin, 600)
        self.led_duty = 0
        self.led_pwm.start(self.led_duty)

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

    def move_cam(self, dir):
        self.servo_duty += dir * 1/10
        self.servo_duty = self.servo_duty if self.servo_duty > 0 else 0
        self.servo_duty = self.servo_duty if self.servo_duty < 99 else 99
        self.servo_pwm.ChangeDutyCycle(int(self.servo_duty))

    def set_led(self, percent):
        percent = percent if percent >= 0 else 0
        percent = percent if percent < 66 else 0
        self.led_pwm.ChangeDutyCycle(percent)

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
        m.set_led(0)
        m.move_cam()
        print("completed 1")
        m.move(right=0, left=1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(10)
        m.move_cam(5)
        print("completed 2")
        m.move(right=0, left=0)
        m.enable_motor()
        m.drive_motor()
        m.set_led(20)
        m.move_cam(10)
        print("completed 3")
        m.move(right=1, left=1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(30)
        m.move_cam(15)
        print("completed 4")
        m.move(right=1, left=-1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(40)
        m.move_cam(20)
        print("completed 5")
        m.move(right=-1, left=1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(50)
        m.move_cam(25)
        print("completed 6")
        m.move(right=-1, left=0)
        m.enable_motor()
        m.drive_motor()
        m.set_led(60)
        m.move_cam()
        print("completed 7")
        m.move(right=0, left=-1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(70)
        m.move_cam(40)
        print("completed 8")
        m.move(right=-1, left=-1)
        m.enable_motor()
        m.drive_motor()
        m.set_led(80)
        m.move_cam(40)
        print("completed 9")