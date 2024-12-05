from time import sleep
import gc
from machine import Pin
from gpio_lcd import GpioLcd

from cykelkode.thingsboard import ThingsBoard
from cykelkode.battery_status import BatteryStatus
from cykelkode.ina_sensor import INA
from cykelkode.temp_sensor import TempSensor

lcd = GpioLcd(Pin(27), Pin(25), Pin(33), Pin(32), Pin(21), Pin(22), 4, 20)

bat_stat = BatteryStatus()
ina = INA()
temp_sen = TempSensor()

while True:
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        # Battery & INA measurements
        bat_p = bat_stat.getPercentage_batt()
        bat_current = ina.getCurrent()
        bat_vol = ina.getVoltage()
        bat_life = ina.getEstimateBatLifeHours()
        
        # Temp measurements
        temp = temp_sen.getTemp()
        humidity = temp_sen.getHumidity()
        
        # IMU
        
        # GPS 
        
        # Display on LCD & Local shell
        # Degree symbol
        degree_sym = bytearray([0B01110,
                                0B01010,
                                0B01110,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000,
                                0B00000])
        lcd.custom_char(0, degree_sym)
        
        lcd.move_to(0, 0)
        lcd.putstr(str(int(bat_p))+ "% " + str(int(bat_current))+" mA ")
        #lcd.move_to(0, 1)
        """
        lcd.putstr(str(int(bat_vol))+ " V " + str(int(bat_life)) + " h")
        print(str(int(bat_p))+ "% " + str(int(bat_current))+" mA " + str(int(bat_vol))+ " V " + str(int(bat_life)) + " h ")
        sleep(3)
        lcd.clear()
        
        lcd.putstr(str(temp) + " C")
        lcd.move_to(2, 0)
        lcd.putchar(chr(0))
        lcd.move_to(5, 0)
        lcd.putstr(str(humidity) + " Humidity")
        """
        sleep(2)
        lcd.clear()
        
    except KeyboardInterrupt:
        print("Disconnected!")
        #client.disconnect()               # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        


