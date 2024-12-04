from time import sleep
from machine import I2C, Pin
from mpu6050 import MPU6050

#Initialisering af I2C objekt
i2c = I2C(0)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)

led_red = Pin(26, Pin.OUT)

prev_accel_x = 0

while True:
    imu_data = imu.get_values()
    accel_x = imu_data.get("acceleration x")
    
    print(abs(accel_x - prev_accel_x))
    if abs(accel_x - prev_accel_x) >= 20000: 
        print(accel_x, "Accel_X")
        led_red.on()
        sleep(1)
    else:
        led_red.off()
    sleep(1)
    prev_accel_x = accel_x
    
    
