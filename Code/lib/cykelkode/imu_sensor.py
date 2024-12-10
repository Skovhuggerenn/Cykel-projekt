from machine import I2C, Pin
from mpu6050 import MPU6050
from time import ticks_ms, time

class IMU:
    def __init__(self):
        i2c = I2C(0)
        self.imu = MPU6050(i2c)
        self.wait_counted = 0
        self.start_time_gps = 0
        
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
        imu_data = self.imu.get_values()
        accel_y = imu_data.get("acceleration y")
        
        if accel_y <= -brake_sensitivity: 
            return True
        else:
            return False
        
    def imu_stoppedCheck(self):
        sensitivity = 1500
        if (time() - self.start_time_gps) >= 60:
            imu_data = self.getIMUData()
            accel_x = imu_data.get("acceleration x")
            accel_y = imu_data.get("acceleration y")
            accel_z = imu_data.get("acceleration z")
            
            if self.wait_counted == 3:
                print("3 min has passed and i have not moved")
                print("Diff x", abs(accel_x - self.prev_accel_x), "Diff y ", abs(accel_y - self.prev_accel_y), "Diff z", abs(accel_z - self.prev_accel_z))
                if (abs(accel_x - self.prev_accel_x) > sensitivity) or (abs(accel_y - self.prev_accel_y) > sensitivity) or (abs(accel_z - self.prev_accel_z) > sensitivity):
                    self.wait_counted = 0
                    print("We moving again after minutes")
                    return True
                else: 
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
            self.start_time_gps = time()
            
    def alarmCheck(self, alarm_status):
        if alarm_status:
            sensitivity = 1500
            imu_data = self.getIMUData()
            accel_x = imu_data.get("acceleration x")
            accel_y = imu_data.get("acceleration y")
            accel_z = imu_data.get("acceleration z")
            print("Diff x", abs(accel_x - self.prev2_accel_x), "Diff y ", abs(accel_y - self.prev2_accel_y), "Diff z", abs(accel_z - self.prev2_accel_z))

            if (abs(accel_x - self.prev2_accel_x) > sensitivity) or (abs(accel_y - self.prev2_accel_y) > sensitivity) or (abs(accel_z - self.prev2_accel_z) > sensitivity):
                return True
            else:
                self.prev2_accel_x = accel_x
                self.prev2_accel_y = accel_y
                self.prev2_accel_z = accel_z
                return False
        else:
            return False
    

