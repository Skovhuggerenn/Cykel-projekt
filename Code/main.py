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
from cykelkode.neo_pixel import TheoPixel
from cykelkode.væske_reminder import VæskeReminder

#thingsboard = ThingsBoard()
bat_stat = BatteryStatus()
ina = INA()
temp_sen = TempSensor()
imu_sen = IMU()
gps_sen = GPS()
buzzer = Buzzer()
lcd_display = LCDDisplay()
neo_pixel = TheoPixel()
led_lights = LED_Lights(neo_pixel)
væske_reminder = VæskeReminder()
alarm_status = False

# the handler callback that gets called when there is a RPC request from the server
def rpc_request_handler(req_id, method, params):
    """handler callback to recieve RPC from server """
     # handler signature is callback(req_id, method, params)
    print(f'Response {req_id}: {method}, params {params}')
    print(params, "params type:", type(params))
    try:
        if method == "Alarm_status":
            global alarm_status
            alarm_status = params

    except TypeError as e:
        print(e)

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
        average_current = ina.getAverageCurrent(bat_current)
        bat_life = ina.getEstimateBatLifeSec(bat_p, average_current)
        
        # Temperature & Humidity measurements
        temp = temp_sen.getTemp()
        humidity = temp_sen.getHumidity()
        
        # IMU measurements
        imu_data = imu_sen.getIMUData()
        # Brake light check
        brake_status = imu_sen.brakeCheck(10000)
        led_lights.ledLightOnBrake(brake_status)
        # Stopped check
        bike_moving =  imu_sen.imu_stoppedCheck()
        
        # Alarm system 
        #thingsboard.client.set_server_side_rpc_request_handler(rpc_request_handler) 
        # Checking for incoming subscriptions or RPC call requests (non-blocking)
        #thingsboard.client.check_msg()
        alarm_activated = imu_sen.alarmCheck(alarm_status)
        if alarm_activated:
            led_lights.led_alarm.on()
            buzzer.buzzNonBlock(330, 2000)
        else:
            led_lights.led_alarm.off()
            buzzer.cutOff()
          
        # GPS measurements
        gps_data = gps_sen.get_gps_data()
        
        if gps_data:
            væske_reminder.checkReminderStatus(bike_moving, temp, humidity, (gps_data[0], gps_data[1]))
        
        # Display on LCD
        lcd_display.putDataOnLCD(int(bat_p), "%")
        lcd_display.putDataOnLCD(int(bat_current), "mA")
        lcd_display.putDataOnLCD(int(bat_vol), "V")
        lcd_display.putDataOnLCD(int(bat_life), "h")
        lcd_display.putTempOnLCD(temp)
        lcd_display.putDataOnLCD(humidity, "Humidity")
        
        # Print to console (TODO)
        """
        #print("Battery: " + str(int(bat_p)) + "%")
        #print("Current: " + str(int(bat_current)) + "mA")
        """
        
        # Send data til thingsboard if not stopped
        """
        if gps_data and bike_moving:
            telemetry = {"latitude":gps_data[0], "longitude": gps_data[1], "gps_speed": gps_data[2], "gps_course": gps_data[3], "Battery":bat_p, "Current":bat_current, "Bat_voltage": bat_vol, "Battery_life":bat_life, "Temperature": temp, "Humidity": humidity}
            thingsboard.sendDataToThingsboard(telemetry)
        """
        sleep(1)

    except KeyboardInterrupt:
        print("Disconnected!")
        #thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32



        












