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
        
    
    def ledLightOnBrake(self, brake_status):
        if brake_status and not self.brake_active:
            self.brake_timer_start = ticks_ms()
            self.brake_active = True
            #self.led_brake.on()
            self.neo_pixel.set_color(5, 0, 0)
        else:
            if (ticks_ms() - self.brake_timer_start) >= 5000:
                #self.led_brake.off()
                self.neo_pixel.clear()
                self.brake_active = False
                
            
            