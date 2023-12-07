import time
import numpy as np
import matplotlib.pyplot as plt
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

# Tijdinterval voor integratie (in seconden)
time_interval = 1/100  # 1/400000 seconde

# MPU9250 initialisatie
mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68,
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure() # Apply the settings to the registers.
mpu.calibrate()
# Stap 1: Maak een nieuw bestand om de gegevens op te slaan
data_file = open("MPU9250_data/data.txt", "w")

# Kalibratieparameters (vervang deze waarden door de gemiddelde offsetwaarden)
offset_x = 0.2
offset_y = 0.13
offset_z = 0.0

# Kalman-filter initialisatie voor positiechatting in x en y richting
kf = KalmanFilter(dim_x=2, dim_z=2)
kf.F = np.array([[1, time_interval],
                 [0, 1]])

kf.H = np.array([[1, 0],
                 [0, 1]])

kf.R = np.array([[0.01, 0],
                 [0, 0.01]])

kf.P = np.array([[1, 0],
                 [0, 1]])

kf.Q = Q_discrete_white_noise(dim=2, dt=time_interval, var=0.13)

# Begin met een initiële positie van 0 meter langs de x- en y-assen
position_x = 0.0  # meter
position_y = 0.0  # meter

# Lijsten voor het opslaan van versnellingswaarden
accel_x_values = []
accel_y_values = []

try:
    while True:
        # Lees de gegevens van de sensor
        accel_data = mpu.readAccelerometerMaster()

        # Schrijf de gegevens naar het bestand
        data_file.write(f"Accelerometer: {accel_data}\n")
        data_file.write("\n")  # Voeg een lege regel toe om de gegevens te scheiden

        # Haal de versnelling in x- en y-richting op en pas kalibratie toe
        accel_x = accel_data[0] - offset_x
        accel_y = accel_data[1] - offset_y

        # Voeg de gegevens toe aan de lijsten
        accel_x_values.append(accel_x)
        accel_y_values.append(accel_y)

        # Voer Kalman-filter uit voor positiechatting in x en y richting
        kf.predict()
        kf.update(np.array([accel_x, accel_y]))

        position_x, position_y = kf.x

        # Stap 2: Gegevens plotten
        plt.plot(position_x, position_y, 'bo')
        plt.xlabel("Afstand X (m)")
        plt.ylabel("Afstand Y (m)")
        plt.title("Afstand Y vs Afstand X")
        plt.grid(True)
        plt.xlim(-0.5, 5)  # X-as limiet van 0 tot 5 meter
        plt.ylim(-0.5, 5)  # Y-as limiet van 0 tot 5 meter
        plt.xticks(np.arange(0, 5.5, 0.3))  # X-as stappen van 0,5 meter
        plt.yticks(np.arange(0, 5.5, 0.3))  # Y-as stappen van 0,5 meter
        plt.pause(0.1)

except KeyboardInterrupt:
    data_file.close()  # Sluit het bestand en beëindig het script als de gebruiker Ctrl+C gebruikt
    print("Data-opname gestopt.")

# Toon de grafiek zonder legende
plt.show()

