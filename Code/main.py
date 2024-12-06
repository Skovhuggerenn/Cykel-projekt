from time import sleep
import gc
from machine import Pin, reset

from cykelkode.thingsboard import ThingsBoard
from cykelkode.battery_status import BatteryStatus
from cykelkode.ina_sensor import INA
from cykelkode.temp_sensor import TempSensor
from cykelkode.imu_sensor import IMU
from cykelkode.gps_sensor import GPS
from cykelkode.buzzer import Buzzer
from cykelkode.lcd_display import LCDDisplay
from cykelkode.led_light import LED_Lights

thingsboard = ThingsBoard()
bat_stat = BatteryStatus()
ina = INA()
temp_sen = TempSensor()
imu_sen = IMU()
gps_sen = GPS()
buzzer = Buzzer()
lcd_display = LCDDisplay()
led_lights = LED_Lights()

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
        imu_data = imu_sen.getIMUData()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        # Break light check
        break_status = imu_sen.breakCheck()
        if break_status:
            led_lights.turnOnBreakLight()
            sleep(2)
            led_lights.turnOffBreakLight()
        
        # GPS
        gps_data = gps_sen.get_gps_data()
        
        # Buzzer
        buzzer.buzz(330, 1, 1)
        
        # Display on LCD
        lcd_display.putTwoDataOnDisplay(int(bat_p), "%", int(bat_current), "mA")
        lcd_display.putTwoDataOnDisplay(int(bat_vol), "V", int(bat_life), "h")
        lcd_display.putTemp(temp)
        lcd_display.putTwoDataOnDisplay(humidity, "Humidity")

        
        sleep(2)

    except KeyboardInterrupt:
        print("Disconnected!")
        thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        




