from time import sleep, time, ticks_ms
import gc
from machine import Pin, reset, I2C, SoftI2C

from cykelkode.thingsboard import ThingsBoard
from cykelkode.battery_status import BatteryStatus
from cykelkode.ina_sensor import INA
from cykelkode.temp_sensor import TempSensor
from cykelkode.imu_sensor import IMU
from cykelkode.gps_sensor import GPS
from cykelkode.buzzer import Buzzer
from cykelkode.lcd_display import LCDDisplay
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


thingsboard = ThingsBoard()
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

# Thresholds
battery_threshold = 10
temp_threshold = 60
gps_threshold = 1
print_threshold = 3
thingsboard_threshold = 20
alarm_active_threshold = 2000

# IMU sensitivity
alarm_sensitivity = 1000
brake_sensitivity = 700
moving_sensitivity = 1000

# Non-blocking timers
start_battery = time()
start_temp = time()
start_gps = time()
start_thingsboard = time()
start_prints = time()
alarm_active_time = ticks_ms()

temp = temp_sen.getTemp()
humidity = temp_sen.getHumidity()
bat_p = bat_stat.getPercentage_batt()
bat_current = ina.getCurrent()
bat_vol = ina.getVoltage()
gps_data = gps_sen.get_gps_data()
bat_life = (0, 0 ,0)
bike_moving = True
alarm_status = False
alarm_active = False
thingsboard.client.set_server_side_rpc_request_handler(rpc_request_handler) 

while True:
    try:
        if gc.mem_free() < 2000:          # free memory if below 2000 bytes left
            print("Garbage collected!")
            gc.collect()                  # free memory 
        
        # Battery & INA measurements
        if time() - start_battery >= battery_threshold:
            bat_p = bat_stat.getPercentage_batt()
            bat_current = ina.getCurrent()
            bat_vol = ina.getVoltage()
            average_current = ina.getAverageCurrent(bat_current)
            bat_life = ina.getEstimateBatLife(bat_p, average_current)
            start_battery = time()
        
        # Temperature & Humidity measurements
        if time() - start_temp >= temp_threshold:
            temp = temp_sen.getTemp()
            humidity = temp_sen.getHumidity()
            start_temp = time()
            
        # GPS measurements
        if time() - start_gps >= gps_threshold:
            gps_data = gps_sen.get_gps_data()
            start_gps = time()
        
        
        # Alarm system 
        alarm_activated = imu_sen.alarmCheck(alarm_status, alarm_sensitivity)
        if alarm_activated:
            alarm_active = True
            alarm_active_time = ticks_ms() 
        if alarm_active:
            neo_pixel.set_color(150, 90, 0)
            buzzer.buzzNonBlock(300, alarm_active_threshold)
            if ticks_ms() - alarm_active_time >= alarm_active_threshold:
                neo_pixel.clear()
                buzzer.cutOff()
                alarm_active = False
        
        # IMU measurements
        if not alarm_status:
            #Brake light check
            brake_status = imu_sen.brakeCheck(brake_sensitivity)
            neo_pixel.ledLightOnBrake(brake_status)
            # Stopped check
            bike_moving =  imu_sen.imu_stoppedCheck(moving_sensitivity)
            
            # Væske reminder
            væske_timer = væske_reminder.checkReminderStatus(bike_moving, temp, humidity)
            if gps_data:  
                væske_reminder.updateTimerBasedOnGPS((gps_data[0], gps_data[1]))
               
            
        
        # Display on LCD & Print to console   
        if time() - start_prints >= print_threshold:
            lcd_display.putDataOnLCD(int(bat_p), int(bat_current), bat_vol, bat_life, temp, humidity, bike_moving, alarm_status, gps_data, væske_timer)
            
            imu_sen.printIMUData()
            print(f"free memory: {gc.mem_free()}") # monitor memory left
            print("Battery: " + str(int(bat_p)) + "%")
            print("Current: " + str(int(bat_current)) + "mA")
            print("Voltage: " + str(int(bat_vol)) + "V")
            if bat_life:
                print("Bat life: " + str(bat_life[0]) + " h " + str(bat_life[1]) + " m " + str(bat_life[2]) + " s")
            print("Temp: " + str(temp))
            print("Humidity: " + str(humidity))
            print("Moving: " + str(bike_moving))
            if væske_timer:   
                print("Væske timer: " + str(væske_timer[0]) + "m "+ str(væske_timer[1])+"s")
            if gps_data:
                print("GPS Longitude: "+ str(gps_data[0]) + " Latitude: "+ str(gps_data[1]) + " Speed: " + str(gps_data[2]) + " Course " + str(gps_data[3]))
            start_prints = time()
        
        
        # Send data til thingsboard if not stopped
        telemetry = {}
        if time() - start_thingsboard >= thingsboard_threshold:
            # Checking for incoming subscriptions or RPC call requests (non-blocking)
            thingsboard.client.check_msg()
            if gps_data and bike_moving:
                telemetry.update({"latitude":gps_data[0], "longitude": gps_data[1], "gps_speed": gps_data[2], "gps_course": gps_data[3], "moving_status":bike_moving})
                    
            telemetry.update({"Battery":bat_p, "Current":bat_current, "Bat_voltage": bat_vol, "Battery_life":bat_life, "Temperature": temp, "Humidity": humidity, "væske_reminder":væske_timer})
            if telemetry:
                thingsboard.sendDataToThingsboard(telemetry)
            start_thingsboard = time()
        
        sleep(0.1)

    except KeyboardInterrupt:
        print("Disconnected!")
        thingsboard.client.disconnect()   # Disconnecting from ThingsBoard
        reset()                           # reset ESP32






