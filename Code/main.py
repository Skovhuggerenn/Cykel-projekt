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
from cykelkode.neo_pixel import NeoPixel

thingsboard = ThingsBoard()
bat_stat = BatteryStatus()
ina = INA()
temp_sen = TempSensor()
imu_sen = IMU()
gps_sen = GPS()
buzzer = Buzzer()
lcd_display = LCDDisplay()
led_lights = LED_Lights()
neo_pixel = NeoPixel()

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
        average_current = ina.getBetterEstimateBatLifeHours(current)        
        
        # Temperature & Humidity measurements
        temp = temp_sen.getTemp()
        humidity = temp_sen.getHumidity()
        
        # IMU measurements
        imu_data = imu_sen.getIMUData()
        # Brake light check
        brake_status = imu_sen.brakeCheck(15000)
        led_lights.ledLightOnBrake(brake_status)
        # Stopped check
        bike_stopped =  imu_sen.imu_stoppedCheck()
        
        # GPS measurements
        gps_data = gps_sen.get_gps_data()
        
        # Buzzer
        buzzer.buzzNonBlock(330, 2000)
        
        # Neopixel
        neo_pixel.set_color(150, 0, 0)
        
        # Alarm system (TODO)
        
        
        # Display on LCD (Need to be done Non-blocking style)
        lcd_display.putDataOnLCD(int(bat_p), "%")
        lcd_display.putDataOnLCD(int(bat_current), "mA")
        lcd_display.putDataOnLCD(int(bat_vol), "V")
        lcd_display.putDataOnLCD(int(bat_life), "h")
        lcd_display.putTempOnLCD(temp)
        lcd_display.putDataOnLCD(humidity, "Humidity")
        
        # Print to console (TODO)
        """
        print("Battery: " + str(int(bat_p)) + "%")
        print("Current: " + str(int(bat_current)) + "mA")
        """
        
        # Send data til thingsboard if not stopped
        if bike_stopped:  
            telemetry = { "latitude":gps_data[0], "longitude":gps_data[1], "gps_speed": gps_data[2],
                         "gps_course"gps_data[3], "Temperature": temp,
                         "Humidity": humidity, "Battery":bat_p,
                         "Current":bat_current, "Bat_voltage": bat_vol }
            thingsboard.sendDataToThingsboard(telemetry)
        
        sleep(1)

    except KeyboardInterrupt:
        print("Disconnected!")
        thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        




