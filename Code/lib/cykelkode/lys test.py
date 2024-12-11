from machine import ADC, Pin
import time

adc = ADC(Pin())

adc.width(ADC.WIDTH_12BIT)

adc.atten(ADC.ATTN_11DB)

while True:
    
    value= adc.read()
    
    if value < 41:
        print("Mørkt")
    elif value < 819:
        print("Semi-Mørkt")
    elif value < 2048:
        print("Lyst")
    elif value < 3277:
        print("Meget Lyst")
    else:
        print("Solen")
    
    sleep(0.5)