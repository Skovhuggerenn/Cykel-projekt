from machine import Pin, PWM
from time import sleep

class Buzzer:
    def __init__(self):
        self.buz = PWM(Pin(14, Pin.OUT), duty=0)

    def buzz(freq, tone_duration, silence_duration):
        self.buz.duty(512)
        self.buz.freq(freq)
        sleep(int(tone_duration*1.30))
        self.buz.duty(0)
        sleep(silence_duration)
            
