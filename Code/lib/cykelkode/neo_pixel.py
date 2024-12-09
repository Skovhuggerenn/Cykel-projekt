from neopixel import NeoPixel
from machine import Pin

class NeoPixel:
    def __init__(self):
        self.np = NeoPixel(Pin(26, Pin.OUT), 12)
    
    def set_color(self, r, g, b):
        for x in range(12):
            self.np[x] = (r, g, b)
            self.np.write()      

    def clear(self):
        for x in range(12):
            self.np[x] = (0, 0, 0)
            self.np.write()

        
    