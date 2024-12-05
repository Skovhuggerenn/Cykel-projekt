from adc_sub import ADC_substitute

class BatteryStatus:
    def __init__(self):
        pin_U = 34
        self.lin = self.getSlope(2363, 2500, 3.75, 4.09)
        self.adcsub = ADC_substitute(pin_U)
        

    def getSlope(self, x1, x2, y1, y2):
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return (a, b)
    
    def batt_voltage(self, adc_v):
        return self.lin[0]*adc_v+self.lin[1]
    
    #Procent:
    # 3V = 0%
    # 4.2V = 100%
    def batt_percentage(self, u_batt):
        without_offset = (u_batt-3)
        normalized = without_offset / (4.2-3.0)
        percent = normalized * 100
        return percent
    
    def getPercentage_batt(self):
        adc = self.adcsub.read_adc()
        bat_v = self.batt_voltage(adc)
        return self.batt_percentage(bat_v)

 









