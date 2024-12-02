from machine import Pin
from time import sleep
from dht import DHT11

dht11_pin = 19

dht11 = DHT11(Pin(dht11_pin))

while True:
    dht11.measure() #Make the measurement
    temp = dht11.temperature() #Get the temperature
    hum = dht11.humidity() #Get the humidity
    
    print("Temperatur: %3d °C" % temp)
    print("Fugtighed : %3d %%" % hum)
    
    sleep(1)