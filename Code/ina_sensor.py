# 0x68 IMU & 0x50 er eeprom & 0x40 INA

from machine import Pin
from ina219_lib import INA219

class INA:
    def __init__(self, i2c):
        self.BAT_MAH = 1800
        ina219_i2c_addr = 0x40
        self.ina219 = INA219(i2c,  ina219_i2c_addr)
        self.ina219.set_calibration_16V_400mA()
        
        self.tot_current = 0
        self.current_counter = 0
        self.prev_batlife = (0,0,0)
    
    def getCurrent(self):
        return self.ina219.get_current()
    
    def getVoltage(self):
        return self.ina219.get_bus_voltage()
    
    def getEstimateBatLife(self, procent, average_current):
        if average_current > 0:
            tot_sec = ((self.BAT_MAH * (procent/100)) / average_current) * 3600
            totH = divmod(tot_sec, 3600)
            totM = divmod(totH[1], 60)
            self.prev_batlife = (totH[0], totM[0], totM[1])
        return self.prev_batlife
        
    def getAverageCurrent(self, current):
        num_of_measurements = 10
        
        if self.current_counter < num_of_measurements and current > 0:
            self.current_counter += 1
            self.tot_current += current
            return 0
        else:
            average = self.tot_current / num_of_measurements
            
            self.tot_current = 0
            self.current_counter = 0
            return average
        


