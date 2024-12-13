from gpio_lcd import GpioLcd
from machine import Pin
from time import sleep, time

class LCDDisplay:
    def __init__(self):
        self.lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25), d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22), num_lines=4, num_columns=20)
        self.current_cursor = 0
        self.MAX_LINE = 4
        self.start_time = time()
        
        #Degree symbol
        degree_sym = bytearray([0B01110,
                                0B01010,
                                0B01110,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000])
        self.lcd.custom_char(0, degree_sym)
        
    
    
    def putDataOnLCD(self, bat_p, bat_current, bat_vol, bat_life, temp, humidity, bike_moving, brake_status, alarm, gps_data):
        if time() - self.start_time >= 3:
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr(str(bat_p)+"% " + str(bat_current)+" mA "+str(bat_vol)+" V")
            self.lcd.move_to(0, 1)
            self.lcd.putstr(str(bat_life[0])+"h" + str(bat_life[1]) + "m" + str(bat_life[2])+ "s" + " T:"+str(temp)+" H:"+str(humidity))
            self.lcd.move_to(0, 2)
            if bike_moving:
                self.lcd.putstr("M:T ")
            else:
                self.lcd.putstr("M:F ")
            if brake_status:
                self.lcd.putstr("B:T ")
            else:
                self.lcd.putstr("B:F ")
            if alarm:
                self.lcd.putstr("A:T ")
            else:
                self.lcd.putstr("A:F ")
            self.lcd.move_to(0, 3)
            if gps_data:
                self.lcd.putstr("GPS:"+str(gps_data[0])+" "+str(gps_data[1])+" "+str(gps_data[2])+" "+str(gps_data[3]))

            self.start_time = time()

"""
lcd = LCDDisplay()

while True:
    lcd.putDataOnLCD(95, 212, 4.0, (2, 33, 35), 23, 30, True, False, (85,90, 0.4, 0.3))
    sleep(1)
    """