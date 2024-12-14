from machine import I2C, Pin
from mpu6050 import MPU6050
from time import time, sleep

class IMU:
    def __init__(self, i2c):
        self.imu = MPU6050(i2c)
        self.wait_counted = 0
        self.start_time_gps = time()
        
        imu_data = self.imu.get_values()
        self.prev_accel_x = imu_data.get("acceleration x")
        self.prev_accel_y = imu_data.get("acceleration y")
        self.prev_accel_z = imu_data.get("acceleration z")
        
        self.prev2_accel_x = imu_data.get("acceleration x")
        self.prev2_accel_y = imu_data.get("acceleration y")
        self.prev2_accel_z = imu_data.get("acceleration z")
        
    def getIMUData(self):
        return self.imu.get_values()
    
    def brakeCheck(self, brake_sensitivity):
        imu_data = self.getIMUData()
        accel_y = imu_data.get("acceleration y")
        
        if accel_y <= -brake_sensitivity: 
            return accel_y
        else:
            return 0
     
    def imu_stoppedCheck(self, sensitivity):
        imu_data = self.getIMUData()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")

        if (time() - self.start_time_gps) >= 5:  
            if self.wait_counted == 3:
                print("3 min has passed and i have not moved")
                print("Diff x", abs(accel_x - self.prev_accel_x), "Diff y ", abs(accel_y - self.prev_accel_y), "Diff z", abs(accel_z - self.prev_accel_z))
                if (abs(accel_x - self.prev_accel_x) > sensitivity) or (abs(accel_y - self.prev_accel_y) > sensitivity) or (abs(accel_z - self.prev_accel_z) > sensitivity):
                    self.wait_counted = 0
                    print("We moving again after minutes")
                    self.moving_status = True
                else:
                    self.moving_status = False
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
                self.moving_status = True
            self.start_time_gps = time()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        return self.moving_status
            
    def alarmCheck(self, alarm_status, sensitivity):
        imu_data = self.getIMUData()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        status = False
        if alarm_status:      
            print("Diff x", abs(accel_x - self.prev2_accel_x), "Diff y ", abs(accel_y - self.prev2_accel_y), "Diff z", abs(accel_z - self.prev2_accel_z))
            if (abs(accel_x - self.prev2_accel_x) > sensitivity) or (abs(accel_y - self.prev2_accel_y) > sensitivity) or (abs(accel_z - self.prev2_accel_z) > sensitivity):
                status = True              
        self.prev2_accel_x = accel_x
        self.prev2_accel_y = accel_y
        self.prev2_accel_z = accel_z
        return status

    def printIMUData(self):
        imu_data = self.getIMUData()
        print("Accel x: " + str(imu_data.get("acceleration x")) + " Accel y: " + str(imu_data.get("acceleration y")) + " Accel z: "+str(imu_data.get("acceleration z"))  )
        
