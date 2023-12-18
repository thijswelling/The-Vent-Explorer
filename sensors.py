import time
import board
import busio
import adafruit_vl53l0x

# I2C-bus initialiseren op bus 25
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Maak een VL53L0X-object
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

try:
    while True:
        # Meet de afstand in millimeters
        distance = vl53.range
        print(f"Afstand: {distance} mm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Programma gestopt door de gebruiker.")

class Sensors:
    def __init__(self):
        self.stop = True

    def get_distance(self) -> float:
        return vl53.range

    def get_orientation(self) -> tuple:
        pass

    def get_accel(self) -> tuple:
        pass

    def get_gyro(self) -> tuple:
        pass

    def loop(self, period=0.1):
        pass
