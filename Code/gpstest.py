from time import sleep
from machine import reset, UART
import gc
import secrets
from gps_simple import GPS_SIMPLE

class GPS:
    def __init__(self):
        gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
        gps_speed = 9600                           # UART speed, defauls u-blox speed
        uart = UART(gps_port, gps_speed)           # UART object creation
        gps = GPS_SIMPLE(uart)                     # GPS object creation
        counter = 0
        prev_accel_x = 0
        prev_accel_y = 0
        prev_accel_z = 0
    
    def get_gps_data(self):
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
        
                
    
    
while True:
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        
        gps_data = get_gps_data()           # multiple returns in tuple format
        imu_data = imu.imu.get_values()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        
        
        print(accel_x, accel_y, accel_z)
        
        
        sleep(2)                          # send telemetry once every second
    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()               # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        