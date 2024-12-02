from machine import ADC, Pin
from time import sleep

pin_U = 34

u_value = ADC(Pin(pin_U))
u_value.atten(ADC.ATTN_11DB)

def getSlope(x1, x2, y1, y2):
    a = (y2 - y1) / (x2 - x1)
    b = a * x1 + y1
    return (a, b)

#lin = getSlope(2390, 453, 4.16, 1)

#Funktioner
def batt_voltage(adc_v, a, b):
    u_batt = a*adc_v+b
    return u_batt

#Procent:
# 3V = 0%
# 4.2V = 100%
def batt_percentage(u_batt):
    without_offset = (u_batt-3)
    normalized = without_offset / (4.2-3.0)
    percent = normalized * 100
    return percent

while True:
    adc_val = u_value.read()
    lin = getSlope(0, 4095, 3.0, 4.2)
    print(adc_val)
    tot_u = batt_voltage(adc_val, lin[0], lin[1])
    bat_p = batt_percentage(tot_u)
    print("Total spænding: ", tot_u)
    print("Procent: ", bat_p)
    sleep(2)


