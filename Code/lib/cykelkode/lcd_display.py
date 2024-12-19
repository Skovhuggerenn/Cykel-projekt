from gpio_lcd import GpioLcd
from machine import Pin

class LCDDisplay:
    def __init__(self):
        self.lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25), d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22), num_lines=4, num_columns=20)
        
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
        
        #Check symbol
        check_sym = bytearray([0B00000,
                                0B00001,
                                0B00001,
                                0B00010,
                                0B10010,
                                0B10100,
                                0B01000,
                                0B00000])
        self.lcd.custom_char(1, check_sym)
        
        #Cross symbol
        cross_sym = bytearray([0B00000,
                                0B10001,
                                0B11011,
                                0B01110,
                                0B01110,
                                0B11011,
                                0B10001,
                                0B00000])
        self.lcd.custom_char(2, cross_sym)
        
    
    
    def putDataOnLCD(self, bat_p, bat_current, bat_vol, bat_life, temp, humidity, bike_moving, alarm, gps_data, væske_timer):
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(str(bat_p)+"% " + str(bat_current)+" mA "+str(bat_vol)+" V")
        self.lcd.move_to(0, 1)
        self.lcd.putstr(str(int(bat_life[0]))+"h" + str(int(bat_life[1])) + "m" + str(int(bat_life[2]))+ "s")
        self.lcd.move_to(9, 1)
        self.lcd.putstr(" T:"+str(temp)+" H:"+str(humidity)+"%")
        self.lcd.move_to(14, 1)
        self.lcd.putchar(chr(0))
        self.lcd.move_to(0, 2)
        if bike_moving:
            self.lcd.putstr("M: ")
            self.lcd.move_to(2, 2)
            self.lcd.putchar(chr(1))
        else:
            self.lcd.putstr("M: ")
            self.lcd.move_to(2, 2)
            self.lcd.putchar(chr(2))
        if alarm:
            self.lcd.putstr(" A: ")
            self.lcd.move_to(6, 2)
            self.lcd.putchar(chr(1))
        else:
            self.lcd.putstr(" A: ")
            self.lcd.move_to(6, 2)
            self.lcd.putchar(chr(2))
        if gps_data:
            self.lcd.move_to(8, 2)
            self.lcd.putstr("S:"+str(round(gps_data[2],2))+" C:"+str(gps_data[3]))
            #self.lcd.putstr(str(væske_timer[0]) + "m "+ str(væske_timer[1])+"s")
        self.lcd.move_to(0, 3)
        if gps_data:
            self.lcd.putstr("G:"+str(gps_data[0])+" "+str(gps_data[1]))


