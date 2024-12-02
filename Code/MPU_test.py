from machine import I2C
from machine import Pin
from time import sleep
from mpu6050 import MPU6050
import sys

#Initialisering af I2C objekt
i2c = I2C(0)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)

while True:
    try:
        # printer hele dictionary som returneres fra get_values metoden
        values = imu.get_values()
        
        print(values.get("acceleration x"), values.get("acceleration y"), values.get("acceleration z"), values.get("temperature celsius"))
        
        
        sleep(1)
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit()

