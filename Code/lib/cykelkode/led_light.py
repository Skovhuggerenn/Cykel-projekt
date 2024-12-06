from machine import Pin
from time import ticks_ms

class LED_Lights:
    def __init__(self):
        self.brake_active = False
        self.led_brake = Pin(26, Pin.OUT)
        #self.led_drink = Pin(18, Pin.OUT)
        #self.led_alarm = Pin(18, Pin.OUT)
        
    def turnOnBrakeLight(self):
        self.led_brake.on()
        
    def turnOffBrakeLight(self):
        self.led_brake.off()
    
    def ledLightOnBrake(self, break_status):
        if brake_status and not brake_active:
            brake_timer = ticks_ms()
            brake_active = True
        else:
            
            