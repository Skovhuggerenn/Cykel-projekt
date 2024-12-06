from machine import Pin

class LED_Lights:
    def __init__(self):
        self.led_break = Pin(26, Pin.OUT)
        #self.led_drink = Pin(18, Pin.OUT)
        #self.led_alarm = Pin(18, Pin.OUT)
        
    def turnOnBreakLight(self):
        self.led_break.on()
        
    def turnOffBreakLight(self):
        self.led_break.off()