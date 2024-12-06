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
        
        # Temperature & Humidity measurements
        temp = temp_sen.getTemp()
        humidity = temp_sen.getHumidity()
        
        # IMU meassurements
        imu_data = imu_sen.getIMUData()
        accel_x = imu_data.get("acceleration x")
        accel_y = imu_data.get("acceleration y")
        accel_z = imu_data.get("acceleration z")
        # Brake light check
        brake_status = imu_sen.brakeCheck(5000)
        led_lights.ledLightOnBrake(brake_status)
        # Stopped check
        bike_stopped =  imu_sen.imu_stoppedCheck()
        
        # GPS meassurements
        gps_data = gps_sen.get_gps_data()
        
        # Buzzer
        buzzer.buzzNonBlock(330, 2000)
        
        # Display on LCD (Need to be done Non-blocking style)
        lcd_display.putTwoDataOnDisplay(int(bat_p), "%", int(bat_current), "mA")
        lcd_display.putTwoDataOnDisplay(int(bat_vol), "V", int(bat_life), "h")
        lcd_display.putTemp(temp)
        lcd_display.putTwoDataOnDisplay(humidity, "Humidity")
        
        # Print to console (TODO)
        
        # Send data til thingsboard if not stopped
        if bike_stopped:  
            telemetry = { "latitude":gps_data[0], "longitude":gps_data[1], "gps_speed": gps_data[2],
                         "gps_course"gps_data[3], "Temperature": temp,
                         "Humidity": humidity, "Battery":bat_p,
                         "Current":bat_current, "Bat_voltage": bat_vol }
            thingsboard.sendDataToThingsboard(telemetry)
        
        sleep(3)

    except KeyboardInterrupt:
        print("Disconnected!")
        thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32

        




