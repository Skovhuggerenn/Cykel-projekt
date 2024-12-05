from uthingsboard.client import TBDeviceMqttClient
import secrets

class ThingsBoard:
    def __init__(self):
        client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
        client.connect()                           # Connecting to ThingsBoard
        print("connected to thingsboard, starting to send and receive data")
    
    def sendDataToThingsboard(self, telemetry):
        self.client.send_telemetry(telemetry)