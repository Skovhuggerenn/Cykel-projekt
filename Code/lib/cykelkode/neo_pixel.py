from neopixel import NeoPixel
from machine import Pin

class TheoPixel:
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

    def ledLightOnBrake(self, brake_status):
        if brake_status >= 0:
            self.clear()
        # -32768 -> 0
        brightness = (abs(brake_status)/10000) * 255
        self.set_color(int(brightness), 0, 0)
    
