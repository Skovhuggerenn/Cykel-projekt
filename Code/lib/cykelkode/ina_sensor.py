# 0x68 IMU & 0x50 er eeprom & 0x40 INA

from machine import I2C, Pin
from ina219_lib import INA219

class INA:
    def __init__(self):
        i2c_port = 0
        ina219_i2c_addr = 0x40
        
        self.bat_mAh = 1800
        ic2 = I2C(i2c_port)
        self.ina219 = INA219(ic2,  ina219_i2c_addr)
        self.ina219.set_calibration_16V_400mA()
        
        self.tot_current = 0
        self.current_counter = 0
        self.prev_batlife_hours = 0
    
    def getCurrent(self):
        return self.ina219.get_current()
    
    def getVoltage(self):
        return self.ina219.get_bus_voltage()
    
    def getEstimateBatLifeHours(self, procent, average_current):
        if average_current > 0:
            self.prev_batlife_hours = (self.bat_mAh * (1/procent)) / average_current
        return self.prev_batlife_hours
        
    def getAverageCurrent(self, current):
        num_of_measurements = 20
        self.current_counter += 1
        if self.current_counter < num_of_measurements:
            self.tot_current += current
            return 0
        else:
            average = self.tot_current / num_of_measurements
            
            self.tot_current = 0
            self.current_counter = 0
            return average
        
        
# 1800 mAh

