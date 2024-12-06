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
    
    
    def putTwoDataOnDisplay(self, data1, symbol1,  data2="", symbol2=""):
        self.lcd.putstr(str(data1) + " " +symbol1 + " " + str(data2) + " " + symbol2)
        self.lcd.move_to(0, self.cursor)
        new_cursor = (self.cursor + 1) % self.max_line
        if (new_cursor == 0):
            sleep(2)
            self.lcd.clear()
        self.cursor = new_cursor
        
    def putTemp(self, temp):
        self.lcd.putstr(str(temp) + " ")
        lcd.move_to(4, 0)
        lcd.putchar(chr(0))
        lcd.move_to(0, 0)
        
        