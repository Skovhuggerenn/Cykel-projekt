from uthingsboard.client import TBDeviceMqttClient
import secrets

class ThingsBoard:
    def __init__(self):
        self.client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
        self.client.connect()                           # Connecting to ThingsBoard
        print("connected to thingsboard, starting to send and receive data")
    
    def sendDataToThingsboard(self, telemetry):
        self.client.send_telemetry(telemetry)
    
    # the handler callback that gets called when there is a RPC request from the server
    def rpc_request_handler(req_id, method, params):
        """handler callback to recieve RPC from server """
         # handler signature is callback(req_id, method, params)
        print(f'Response {req_id}: {method}, params {params}')
        print(params, "params type:", type(params))
        try:
            # check if the method is "toggle_led1" (needs to be configured on thingsboard dashboard)
            if method == "toggle_led1":
            
            # check if command is send from RPC remote shell widget   
            if method == "sendCommand":
                message = params.get("command")
                

        except TypeError as e:
            print(e)
