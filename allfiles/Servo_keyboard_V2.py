from gpiozero import AngularServo

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

current_angle = 0  # Startpositie

while True:
    # Vraag de gebruiker om input
    user_input = input("Voer 'a' in voor links, 'd' voor rechts, of 'q' om te stoppen: ")

    # Wijzig de hoek op basis van de gebruikersinput
    if user_input == 'a':
        current_angle = max(-90, current_angle - 20)
    elif user_input == 'd':
        current_angle = min(90, current_angle + 20)
    elif user_input == 'q':
        break

    # Stel de hoek van de servo in
    servo.angle = current_angle
