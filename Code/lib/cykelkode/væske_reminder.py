from time import time, sleep
from machine import Pin

class VæskeReminder:
    def __init__(self):
        self.BASE_TIME = 5
        self.drink_time = self.BASE_TIME
        
        self.start_time = 0
        self.temp_start_time = 0
        self.gps_start_time = 0
        
        self.latitude = -999.0
        self.longitude = -999.0
        
        self.led = Pin(13, Pin.OUT)
        self.pb = Pin(35, Pin.IN)
        
    def checkReminderStatus(self, temp, humidity, lat_lon):
        if time() - self.temp_start_time >= 10:
            temporary_time = self.BASE_TIME
            if temp >= 26:
                temporary_time = temporary_time - 2
            if humidity >= 30:
                temporary_time = temporary_time - 3
            self.drink_time = temporary_time       
        
        if time() - self.gps_start_time >= 10:
            if not lat_lon:
                if self.latitude == -999.0 and self.longitude == -999.0
                    self.latitude = lat_lon[0]
                    self.longitude = lat_lon[1]
        
        if self.pb.value() == 1:
            self.led.off()
            self.start_time = time()
        if time() - self.start_time >= self.drink_time:
            self.led.on()
"""
vr = VæskeReminder()

while True:
    vr.checkReminderStatus(23)
    sleep(1)
"""
