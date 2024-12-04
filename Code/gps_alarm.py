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
            lat = str(gps.get_latitude())  # store latitude in lat variable
            lon = str(gps.get_longitude()) # stor longitude in lon variable
            speed = str(gps.get_speed())
            course = str(gps.get_course())
            return lat, lon, speed, course               # multiple return values, needs unpacking or it will be tuple format
        else:                              # if latitude and longitude are invalid
            print(f"GPS data to server not valid:\nlatitude: {lat}\nlongtitude: {lon}")
            return False
    else:
        return False
                                           # Make client object to connect to thingsboard
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()                           # Connecting to ThingsBoard
print("connected to thingsboard, starting to send and receive data")

while True:
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        gps_data = get_gps_data()           # multiple returns in tuple format
        
        
        print(gps_data)
        if gps_data:
            # store telemetry in dictionary      
            telemetry = {'latitude': gps_data[0], 'longitude': gps_data[1], 'speed_gps': gps_data[2], 'course_gps': gps_data[3]}
            client.send_telemetry(telemetry) #Sending telemetry  
    
        sleep(1)                          # send telemetry once every second
    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()               # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        
