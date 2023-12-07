    import RPi.GPIO as GPIO
    import time

    # GPIO-pinnen voor de stepper motor
    Dir_Motor1 = 20  # GPIO-pin voor de richting van motor 1
    Stp_Motor1 = 21  # GPIO-pin voor de stap van motor 1
    En_Motor1 = 4    # GPIO-pin voor de enable van motor 2


    Dir_Motor2 = 10  # GPIO-pin voor de richting van motor 2
    Stp_Motor2 = 11  # GPIO-pin voor de stap van motor 2
    En_Motor2 = 4    # GPIO-pin voor de enable van motor 2

    # Setup GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Instellingen voor motor 1
    GPIO.setup(Dir_Motor1, GPIO.OUT)
    GPIO.setup(Stp_Motor1, GPIO.OUT)
    GPIO.setup(En_Motor1, GPIO.OUT)
    GPIO.output(Dir_Motor1, GPIO.HIGH)  # Set de richting

    # Instellingen voor motor 2
    GPIO.setup(Dir_Motor2, GPIO.OUT)
    GPIO.setup(Stp_Motor2, GPIO.OUT)
    GPIO.setup(En_Motor2, GPIO.OUT)
    GPIO.output(Dir_Motor2, GPIO.HIGH)  # Set de richting

    # Functie om de motoren te laten draaien
    def drive_motors(steps, delay):
        for _ in range(steps):
            # Stapmotor 1
            GPIO.output(Stp_Motor1, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(Stp_Motor1, GPIO.LOW)
            time.sleep(delay)

            # Stapmotor 2
            GPIO.output(Stp_Motor2, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(Stp_Motor2, GPIO.LOW)
            time.sleep(delay)

    # Loop voor gebruikersinput
    while True:
        user_input = input("Voer 'w' in voor vooruit, 's' voor achteruit, 'q' om te stoppen: ")

        if user_input == 'w':
            drive_motors(steps=200, delay=0.001)
        elif user_input == 's':
            drive_motors(steps=200, delay=0.001)
        elif user_input == 'q':
            break

    # GPIO opschonen bij het beëindigen van het programma
    GPIO.cleanup()

