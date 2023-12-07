import time
import numpy as np
import matplotlib.pyplot as plt
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# MPU9250 initialisatie
mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x69 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure() # Apply the settings to the registers.

# Stap 1: Maak een nieuw bestand om de gegevens op te slaan
data_file = open("MPU9250_data/data.txt", "w")

try:
    while True:
        # Lees de gegevens van de sensor
        accel_data = mpu.readAccelerometerMaster()
        gyro_data = mpu.readGyroscopeMaster()
        mag_data = mpu.readMagnetometerMaster()
        temperature = mpu.readTemperatureMaster()

        # Schrijf de gegevens naar het bestand
        data_file.write(f"Accelerometer: {accel_data}\n")
        data_file.write(f"Gyroscope: {gyro_data}\n")
        data_file.write(f"Magnetometer: {mag_data}\n")
        data_file.write(f"Temperature: {temperature}\n")
        data_file.write("\n")  # Voeg een lege regel toe om de gegevens te scheiden

        # Stap 2: Gegevens plotten
        timestamp = time.time()  # Tijdstempel voor de x-as van de grafiek
        accel_x = accel_data[0]
        gyro_x = gyro_data[0]
        mag_x = mag_data[0]
        plt.scatter(timestamp, accel_x, color='b', label='Accel X')
        plt.scatter(timestamp, gyro_x, color='g', label='Gyro X')
        plt.scatter(timestamp, mag_x, color='r', label='Mag X')
        plt.xlabel("Tijd (s)")
        plt.ylabel("Sensorwaarden")
        plt.title("Sensorwaarden over de tijd")
        plt.grid(True)
        plt.legend()
        plt.pause(0.1)  # Pauzeer voor 0.1 seconden om de grafiek bij te werken

except KeyboardInterrupt:
    data_file.close()  # Sluit het bestand en beëindig het script als de gebruiker Ctrl+C gebruikt
    print("Data-opname gestopt.")

# Toon de grafiek
plt.show()
