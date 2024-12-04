from uthingsboard.client import TBDeviceMqttClient
from time import sleep
from machine import reset, UART
import gc
import secrets
from gps_simple import GPS_SIMPLE

from machine import Pin, ADC
from time import sleep_ms
from neopixel import NeoPixel
from random import choice

from machine import I2C
from mpu6050 import MPU6050

gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_SIMPLE(uart)                     # GPS object creation  

def get_gps_data():
    lat = lon = None                       # create lat and lon variable with None as default value
    if gps.receive_nmea_data():            # check if data is recieved
                                           # check if the data is valid
        if gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            lat = gps.get_latitude()  # store latitude in lat variable
            lon = gps.get_longitude() # stor longitude in lon variable
            speed = gps.get_speed()
            course = gps.get_course()
            return lat, lon, speed, course               # multiple return values, needs unpacking or it will be tuple format
        else:                              # if latitude and longitude are invalid
            print(f"GPS data to server not valid:\nlatitude: {lat}\nlongtitude: {lon}")
            return False
    else:
        return False
                                           # Make client object to connect to thingsboard
#client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
#client.connect()                           # Connecting to ThingsBoard
#print("connected to thingsboard, starting to send and receive data")

counter = 0
prev_lat = 0
prev_long = 0

#Initialisering af I2C objekt
i2c = I2C(0)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)

prev_accel_x = 0
prev_accel_y = 0
prev_accel_z = 0

while True:
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        #gps_data = get_gps_data()           # multiple returns in tuple format
        imu_data = imu.get_values()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        
        print(accel_x, accel_y, accel_z)
        
        #if gps_data:
            
        if counter == 10:
            print("3 min has passed and i have not moved")
            #print(gps_data)
            print("Diff x", abs(accel_x - prev_accel_x), "Diff y ", abs(accel_y - prev_accel_y), "Diff z", abs(accel_z - prev_accel_z))
            if (abs(accel_x - prev_accel_x) > 1500) or (abs(accel_y - prev_accel_y) > 1500) or (abs(accel_z - prev_accel_z) > 1500):
                counter = 0
                print("We moving again after minutes")
        else:
            print("Diff x", abs(accel_x - prev_accel_x), "Diff y ", abs(accel_y - prev_accel_y), "Diff z", abs(accel_z - prev_accel_z))

            if (abs(accel_x - prev_accel_x) <= 1500) and (abs(accel_y - prev_accel_y) <= 1500) andåå (abs(accel_z - prev_accel_z) <= 1500):
                print("Same location increase counter")
                counter += 1     
            else:
                print("Stil moving!")
                counter = 0
                prev_accel_x = accel_x
                prev_accel_y = accel_y
                prev_accel_z = accel_z
            """
            print(gps_data) 
            if gps_data:   
                    telemetry = {'latitude': str(gps_data[0]), 'longitude': str(gps_data[1]), 'speed_gps': str(gps_data[2]), 'course_gps': str(gps_data[3])}
                    client.send_telemetry(telemetry)
            """
    
        print(counter)
        
        sleep(2)                          # send telemetry once every second
    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()               # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        