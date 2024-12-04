from machine import ADC, Pin
from time import sleep

pin_U = 34

u_value = ADC(Pin(pin_U))
u_value.atten(ADC.ATTN_11DB)

def getSlope(x1, x2, y1, y2):
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return (a, b)

#lin = getSlope(2528, 3133, 3.30, 4.06)
# volt 4.06  adc 3133
# volt 3.30 adc 2528
 
#Funktioner
def batt_voltage(adc_v, a, b):
    return a*adc_v+b

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
    print(adc_val)
    lin = getSlope(2528, 3133, 3.30, 4.06)
    #print(batt_voltage(3133, lin[0], lin[1]))
    
    tot_u = batt_voltage(adc_val, lin[0], lin[1])
    bat_p = batt_percentage(tot_u)
    print("Total spænding: ", tot_u)
    print("Procent: ", bat_p)
    
    sleep(2)


