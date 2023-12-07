import RPi.GPIO as GPIO
import time

# GPIO-pin voor de servo
servo_pin = 12

# Initialisatie van de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Frequentie van de PWM (meestal 50 Hz)
pwm_freq = 50
pwm = GPIO.PWM(servo_pin, pwm_freq)

# Functie om de servo naar een bepaalde hoek te draaien
def set_servo_angle(angle):
    duty_cycle = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Wacht om de servo de tijd te geven om te draaien

try:
    pwm.start(0)  # Start het PWM-signaal met een duty cycle van 0 (servo uit)
    
    while True:
        user_input = input("Druk op '0' om naar 0 graden te draaien of '9' om naar 90 graden te draaien: ")
        
        if user_input == '0':
            set_servo_angle(0)
            time.sleep(1)  # Wacht even voordat het PWM-signaal wordt gestopt
            pwm.ChangeDutyCycle(0)  # Stop het PWM-signaal (servo uit)
        elif user_input == '9':
            set_servo_angle(90)
            time.sleep(1)  # Wacht even voordat het PWM-signaal wordt gestopt
            pwm.ChangeDutyCycle(0)  # Stop het PWM-signaal (servo uit)
        else:
            print("Ongeldige invoer. Druk op '0' of '9'.")

except KeyboardInterrupt:
    print("\nProgramma gestopt.")
finally:
    pwm.stop()
    GPIO.cleanup()