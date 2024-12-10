from machine import Pin, PWM
from time import ticks_ms

class Buzzer:
    def __init__(self):
        self.start_time = 0
        self.making_sound = False
        self.buz = PWM(Pin(14, Pin.OUT), duty=0)

    def buzzNonBlock(self, freq, tone_duration):
        if not self.making_sound:
            self.buz.duty(512)
            self.buz.freq(freq)
            self.start_time = ticks_ms()
            self.making_sound = True
        else:
            if (ticks_ms() - self.start_time) >= tone_duration:
                self.buz.duty(0)
                self.making_sound = False
    
    def cutOff(self):
        self.buz.duty(0)
        self.making_sound = False
            
