from time import sleep
import gc
from machine import Pin, reset

from cykelkode.thingsboard import ThingsBoard
from cykelkode.battery_status import BatteryStatus
from cykelkode.ina_sensor import INA
from cykelkode.temp_sensor import TempSensor
from cykelkode.imu_sensor import IMU
from cykelkode.gps_sensor import GPS
from cykelkode.lcd_display import LCDDisplay

thingsboard = ThingsBoard()
bat_stat = BatteryStatus()
ina = INA()
temp_sen = TempSensor()
imu_sen = IMU()
gps_sen = GPS()
lcd_display = LCDDisplay()

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
        
        # GPS
        gps_data = gps_sen.get_gps_data()
        
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

        




