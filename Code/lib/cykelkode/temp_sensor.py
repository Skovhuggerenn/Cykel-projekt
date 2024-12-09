from machine import Pin
from dht import DHT11

class TempSensor:
    def __init__(self):
        dht11_pin = 19
        self.dht11 = DHT11(Pin(dht11_pin))
    
    def getTemp(self):
        self.dht11.measure()
        return self.dht11.temperature()
    
    def getHumidity(self):
        self.dht11.measure()
        return self.dht11.humidity()
        
