from time import time, sleep
import math
from machine import Pin

class VæskeReminder:
    def __init__(self):
        self.drink_time = 10
        
        self.start_time = time()
        self.temp_start_time = time()
        self.gps_start_time = time()
        
        self.prev_latitude = -999.0
        self.prev_longitude = -999.0
        
        self.led = Pin(13, Pin.OUT)
        self.pb = Pin(35, Pin.IN)
    
    def updateTimerBasedOnGPS(self, lat_lon):     
        if time() - self.gps_start_time >= 300:
            if not lat_lon:
                if self.latitude == -999.0 and self.longitude == -999.0:
                    self.latitude = lat_lon[0]
                    self.longitude = lat_lon[1]
                else:
                    dist = getDistanceFromLatLonInKm(self.latitude, self.longitude, lat_lon[0], lat_lon[1])
                    if dist >= 1.5:
                        self.drink_time *= 0.90
                    elif dist <= 0.8:
                        self.drink_time *= 1.05
                    else:
                        self.drink_time *= 0.95
                    self.prev_latitude = lat_lon[0]
                    self.prev_longitude = lat_lon[1]      
            self.gps_start_time = time()
    

    def updateTimerBasedOnTemp(self, temp, humidity):
        if temp >= 25:
            self.drink_time = 10
        elif temp <= 10:
            self.drink_time = 20
        else:
            self.drink_time = 15
        if humidity >= 75:
            self.drink_time -= 2
        elif humidity <= 25:
            self.drink_time += 2
        else:
            self.drink_time -= 1
            
    def checkReminderStatus(self, bike_moving, temp, humidity):
        if bike_moving:
            if pb.value() == 1:
                self.led.off()
                self.start_time = time()
                self.drink_time = updateTimerBasedOnTemp(temp, humidity)
            if time() - self.start_time >= self.drink_time:
                self.led.on()
        else:
            self.led.off()
            self.start_time = time()
            self.drink_time = updateTimerBasedOnTemp(temp, humidity)
            
    def getDistanceFromLatLonInKm(self, lat1,lon1,lat2,lon2):
        R = 6371; 
        dLat = self.deg2rad(lat2-lat1) 
        dLon = self.deg2rad(lon2-lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(self.deg2rad(lat1)) * math.cos(self.deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d


    def deg2rad(self, deg):
        return deg * (math.pi/180)



