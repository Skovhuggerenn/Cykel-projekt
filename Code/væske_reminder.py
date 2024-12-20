from time import time, sleep
import math
from machine import Pin

class VæskeReminder:
    def __init__(self):
        self.drink_time = 900
        
        self.start_time = time()
        self.temp_start_time = time()
        self.gps_start_time = time()
        
        self.prev_latitude = -999.0
        self.prev_longitude = -999.0
        
        self.led = Pin(4, Pin.OUT)
        self.pb = Pin(2, Pin.IN)
    
    
    def updateTimerBasedOnGPS(self, lat_lon):     
        if time() - self.gps_start_time >= 300:
            if not lat_lon:
                if self.prev_latitude == -999.0 and self.prev_longitude == -999.0:
                    self.prev_latitude = lat_lon[0]
                    self.prev_longitude = lat_lon[1]
                else:
                    dist = getDistanceFromLatLonInKm(self.prev_latitude, self.prev_longitude, lat_lon[0], lat_lon[1])
                    if dist >= 2.0:
                        self.drink_time -= 180
                    elif dist <= 1.0:
                        self.drink_time -= 60
                    else:
                        self.drink_time -= 120
                    self.prev_latitude = lat_lon[0]
                    self.prev_longitude = lat_lon[1]      
            self.gps_start_time = time()
    

    def updateTimerBasedOnTemp(self, temp, humidity):
        self.drink_time = 900
        if temp >= 15:
            self.drink_time -= 60
        elif temp <= 5:
            self.drink_time -= 120
        
        if humidity >= 65:
            self.drink_time -= 120 
        elif humidity <= 50:
            self.drink_time -= 60 
            
    def checkReminderStatus(self, bike_moving, temp, humidity):
        if bike_moving:
            if self.pb.value() == 1:
                self.led.off()
                self.start_time = time()
                self.updateTimerBasedOnTemp(temp, humidity)
            if time() - self.start_time >= self.drink_time:
                self.led.on()
        else:
            self.led.off()
            self.start_time = time()
            self.updateTimerBasedOnTemp(temp, humidity)
        remain_time = self.formatTimerFromSec((self.drink_time-(time() - self.start_time)))
        return remain_time
    
    def getDistanceFromLatLonInKm(self, lat1,lon1,lat2,lon2):
        R = 6371; 
        dLat = self.deg2rad(lat2-lat1) 
        dLon = self.deg2rad(lon2-lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(self.deg2rad(lat1)) * math.cos(self.deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d
    
    def formatTimerFromSec(self, tot_sec):
        if tot_sec > 0:
            totM = divmod(tot_sec, 60)
            return (totM[0], totM[1])
        return (0, 0)

    def deg2rad(self, deg):
        return deg * (math.pi/180)
