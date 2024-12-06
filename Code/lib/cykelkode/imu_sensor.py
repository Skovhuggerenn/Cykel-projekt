from time import sleep
from machine import I2C, Pin
from mpu6050 import MPU6050

class IMU:
    def __init__(self):
        i2c = I2C(0)
        self.imu = MPU6050(i2c)
        self.led_red = Pin(26, Pin.OUT)
        prev_accel_x = 0
        
    def getIMUData(self):
        return self.imu.get_values()
    
    def breakCheck(self):
        imu_data = self.imu.get_values()
        accel_x = imu_data.get("acceleration x")
        
        if abs(accel_x - self.prev_accel_x) >= 20000: 
            return True
        else:
            return False
        self.prev_accel_x = accel_x
        
    def imu_stop_test(self):
        if gps_data:    
            if counter == 10:
                print("3 min has passed and i have not moved")
                #print(gps_data)
                print("Diff x", abs(accel_x - prev_accel_x), "Diff y ", abs(accel_y - prev_accel_y), "Diff z", abs(accel_z - prev_accel_z))
                if (abs(accel_x - prev_accel_x) > 1500) or (abs(accel_y - prev_accel_y) > 1500) or (abs(accel_z - prev_accel_z) > 1500):
                    counter = 0
                    print("We moving again after minutes")
            else:
                print("Diff x", abs(accel_x - prev_accel_x), "Diff y ", abs(accel_y - prev_accel_y), "Diff z", abs(accel_z - prev_accel_z))

                if (abs(accel_x - prev_accel_x) <= 1500) and (abs(accel_y - prev_accel_y) <= 1500) and (abs(accel_z - prev_accel_z) <= 1500):
                    print("Same location increase counter")
                    counter += 1     
                else:
                    print("Stil moving!")
                    counter = 0
                    prev_accel_x = accel_x
                    prev_accel_y = accel_y
                    prev_accel_z = accel_z
                
                print(gps_data) 
                if gps_data:   
                        telemetry = {'latitude': str(gps_data[0]), 'longitude': str(gps_data[1]), 'speed_gps': str(gps_data[2]), 'course_gps': str(gps_data[3])}
                        client.send_telemetry(telemetry)
            
    
