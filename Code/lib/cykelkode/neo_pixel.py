from neopixel import NeoPixel
from machine import Pin
from time import ticks_ms

class TheoPixel:
    def __init__(self):
        self.np = NeoPixel(Pin(26, Pin.OUT), 12)
        self.braking_active = False
        self.timer = ticks_ms()
    
    def set_color(self, r, g, b):
        for x in range(12):
            self.np[x] = (r, g, b)
            self.np.write()      

    def clear(self):
        for x in range(12):
            self.np[x] = (0, 0, 0)
            self.np.write()

    def ledLightOnBrakeTest(self, brake_status):
        if self.braking_active:
            if ticks_ms() - self.timer >= 10:
                self.braking_active = False
                self.clear()
        else:
            # -32768 -> 0
            brightness = (abs(brake_status)/10000) * 255
            if brightness >= 255:
                brightness = 255
            self.set_color(int(brightness), 0, 0)
            self.braking_active = True
            self.timer = ticks_ms()
    
    def ledLightOnBrake(self, brake_status):
        if brake_status >= 0:
            self.clear()
        else:
            # -32768 -> 0
            brightness = (abs(brake_status)/10000) * 255
            if brightness >= 255:
                brightness = 255
            self.set_color(int(brightness), 0, 0)
        
        
    

