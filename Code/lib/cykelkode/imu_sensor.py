from machine import I2C, Pin
from mpu6050 import MPU6050

class IMU:
    def __init__(self):
        i2c = I2C(0)
        self.imu = MPU6050(i2c)
        self.wait_counted = 0
        self.prev_accel_x = 0
        self.prev_accel_y = 0
        self.prev_accel_z = 0
        
    def getIMUData(self):
        return self.imu.get_values()
    
    def breakCheck(self, waitTime):
        imu_data = self.imu.get_values()
        accel_x = imu_data.get("acceleration x")
        
        if abs(accel_x - self.prev_accel_x) >= waitTime: 
            return True
        else:
            return False
        self.prev_accel_x = accel_x
        
    def imu_stoppedCheck(self, accel_x, accel_y, accel_z):
        sensitivity = 1500
        
        imu_data = self.getIMUData()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        
        if self.wait_counted == 10:
            print("3 min has passed and i have not moved")
            print("Diff x", abs(accel_x - self.prev_accel_x), "Diff y ", abs(accel_y - self.prev_accel_y), "Diff z", abs(accel_z - self.prev_accel_z))
            if (abs(accel_x - self.prev_accel_x) > sensitivity) or (abs(accel_y - self.prev_accel_y) > sensitivity) or (abs(accel_z - self.prev_accel_z) > sensitivity):
                self.wait_counted = 0
                print("We moving again after minutes")
            return False
        else:
            print("Diff x", abs(accel_x - self.prev_accel_x), "Diff y ", abs(accel_y - self.prev_accel_y), "Diff z", abs(accel_z - self.prev_accel_z))

            if (abs(accel_x - self.prev_accel_x) <= sensitivity) and (abs(accel_y - self.prev_accel_y) <= sensitivity) and (abs(accel_z - self.prev_accel_z) <= sensitivity):
                print("Same location increase counter")
                self.wait_counted += 1     
            else:
                print("Stil moving!")
                self.wait_counted = 0
                self.prev_accel_x = accel_x
                self.prev_accel_y = accel_y
                self.prev_accel_z = accel_z
            
            # Send GPS Data
            return True
            
    
