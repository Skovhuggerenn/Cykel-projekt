from gpio_lcd import GpioLcd
from time import sleep

class LCDDisplay:
    def __init__(self):
        self.lcd = GpioLcd(Pin(27), Pin(25), Pin(33), Pin(32), Pin(21), Pin(22), 4, 20)
        self.cursor = 0
        self.max_line = 3
        #Degree symbol
        degree_sym = bytearray([0B01110,
                                0B01010,
                                0B01110,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000])
        lcd.custom_char(0, degree_sym)
    
    
    def putDataOnLCD(self, data, symbol):
        self.lcd.putstr(str(data1) + " " +symbol + " ")
        
    def putTempOnLCD(self, temp):
        self.lcd.putstr(str(temp) + " ")
        self.lcd.putchar(chr(0))
        self.lcd.putchar("C")
        
        