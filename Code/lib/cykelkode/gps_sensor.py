from machine import UART
from gps_simple import GPS_SIMPLE

class GPS:
    def __init__(self):
        gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
        gps_speed = 9600                           # UART speed, defauls u-blox speed
        uart = UART(gps_port, gps_speed)           # UART object creation
        self.gps = GPS_SIMPLE(uart)                     # GPS object creation

    def get_gps_data(self):
        lat = lon = None # create lat and lon variable with None as default value
        
        if self.gps.receive_nmea_data():            # check if data is recieved
                                                  # check if the data is valid
            if self.gps.get_latitude() != -999.0 and self.gps.get_longitude() != -999.0 and self.gps.get_validity() == "A":
                print("Valid GPS DATA!!!")
                lat = self.gps.get_latitude()  # store latitude in lat variable
                lon = self.gps.get_longitude() # stor longitude in lon variable
                speed = self.gps.get_speed()
                course = self.gps.get_course()
                return lat, lon, speed, course               # multiple return values, needs unpacking or it will be tuple format
            else:                              # if latitude and longitude are invalid
                #print(f"GPS data to server not valid:\nlatitude: {lat}\nlongtitude: {lon}")
                return False
        else:
            return False
        