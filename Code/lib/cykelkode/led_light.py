from machine import Pin
from time import ticks_ms

class LED_Lights:
    def __init__(self, neo_pixel):
        self.brake_active = False
        self.brake_timer_start = 0
        self.led_alarm = Pin(26, Pin.OUT)
        self.neo_pixel = neo_pixel
        
        #self.led_drink = Pin(18, Pin.OUT)
        #self.led_alarm = Pin(18, Pin.OUT)
        
    

                
            
            