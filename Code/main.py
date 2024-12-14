from time import sleep, time
import gc
from machine import Pin, reset, I2C

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


#thingsboard = ThingsBoard()
bat_stat = BatteryStatus()
i2c = I2C(0)
ina = INA(i2c)
imu_sen = IMU(i2c)
temp_sen = TempSensor()
gps_sen = GPS()
buzzer = Buzzer()
lcd_display = LCDDisplay()
neo_pixel = TheoPixel()
væske_reminder = VæskeReminder()
alarm_status = False

#thingsboard.client.set_server_side_rpc_request_handler(rpc_request_handler) 

# Timers
start_battery = time()
start_temp = time()
start_gps = time()
start_thingsboard = time()
start_prints = time()

temp = temp_sen.getTemp()
humidity = temp_sen.getHumidity()
bat_p = bat_stat.getPercentage_batt()
bat_current = ina.getCurrent()
bat_vol = ina.getVoltage()
gps_data = gps_sen.get_gps_data()

while True:
    try:
        print(f"free memory: {gc.mem_free()}") # monitor memory left
        
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        # Battery & INA measurements
        if time() - start_battery >= 5:
            bat_p = bat_stat.getPercentage_batt()
            bat_current = ina.getCurrent()
            bat_vol = ina.getVoltage()
            average_current = ina.getAverageCurrent(bat_current)
            bat_life = ina.getEstimateBatLifeSec(bat_p, average_current)
        
        # Temperature & Humidity measurements
        if time() - start_temp >= 60:
            temp = temp_sen.getTemp()
            humidity = temp_sen.getHumidity()
        
        
        # IMU measurements
        #imu_sen.printIMUData()
        #Brake light check
        brake_status = imu_sen.brakeCheck(2000)
        neo_pixel.ledLightOnBrake(brake_status)
        # Stopped check
        #bike_moving =  imu_sen.imu_stoppedCheck()
        
        
        # Alarm system 
        # Checking for incoming subscriptions or RPC call requests (non-blocking)
        """
        thingsboard.client.check_msg()
        alarm_activated = imu_sen.alarmCheck(alarm_status)
        if alarm_activated:
            neo_pixel.set_color(0, 100, 0)
            buzzer.buzzNonBlock(330, 2000)
        else:
            neo_pixel.clear()
            buzzer.cutOff()
        """
        
        # GPS measurements
        if time() - start_gps >= 2:
            gps_data = gps_sen.get_gps_data()
        
        # Væske reminder
        """
        væske_reminder.checkReminderStatus(bike_moving, temp, humidity)
        if gps_data:  
            væske_reminder.updateTimerBasedOnGPS((gps_data[0], gps_data[1]))
        """
        
        # Display on LCD & Print to console
        """
        if time() - start_prints >= 2:
            #lcd_display.putDataOnLCD(int(bat_p), int(bat_current), int(bat_vol), bat_life, temp, humidity, bike_moving, alarm_activated, gps_data)
            
            print("Battery: " + str(int(bat_p)) + "%")
            print("Current: " + str(int(bat_current)) + "mA")
            print("Voltage: " + str(int(bat_vol)) + "V")
            print("Bat life: " + str(int(bat_life[0])) + " h " + str(int(bat_life[1])) + " m " + str(int(bat_life[2])) + " s")
            print("Temp: " + str(temp))
            if gps_data:
                print("GPS Longitude: "+ str(gps_data[0]) + " Latitude: "+ str(gps_data[1]) + " Speed: " + str(gps_data[2]) + " Course " + str(gps_data[3]))
        """
        
        # Send data til thingsboard if not stopped
        telemetry = {}
        if time() - start_thingsboard >= 10:
            if gps_data and bike_moving:
                telemetry.update({"latitude":gps_data[0], "longitude": gps_data[1], "gps_speed": gps_data[2], "gps_course": gps_data[3]})
                    
            telemetry.update({"Battery":bat_p, "Current":bat_current, "Bat_voltage": bat_vol, "Battery_life":bat_life, "Temperature": temp, "Humidity": humidity})
            if telemetry:
                thingsboard.sendDataToThingsboard(telemetry)
                 
        sleep(0.1)

    except KeyboardInterrupt:
        print("Disconnected!")
        thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32





