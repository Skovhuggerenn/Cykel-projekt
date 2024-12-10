from time import time, sleep
import math
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
        
    # NOT WORKING     
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
                if self.latitude == -999.0 and self.longitude == -999.0:
                    self.latitude = lat_lon[0]
                    self.longitude = lat_lon[1]
                else:
                    dist = getDistanceFromLatLonInKm(self.latitude, self.longitude, lat_lon[0], lat_lon[1])
                    if dist >= 5:
                        temporary_time = temporary_time - 5
        
        if self.pb.value() == 1:
            self.led.off()
            self.start_time = time()
        if time() - self.start_time >= self.drink_time:
            self.led.on()
            
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

vr = VæskeReminder()

while True:
    #vr.checkReminderStatus(23)
    print(vr.getDistanceFromLatLonInKm(55.68613, 12.57913, 55.66984, 12.59736))
    sleep(1)



