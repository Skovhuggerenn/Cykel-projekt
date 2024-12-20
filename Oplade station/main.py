from machine import Pin
from time import sleep
import requests

# Initialize the relay pin
relay = Pin(16, Pin.OUT)

# API call loop
while True:
    response = requests.get(
        url='https://api.energidataservice.dk/dataset/CO2Emis?limit=1')

    result = response.json()

    records = result.get('records', [])

    if records:
        co2_emission = records[0].get("CO2Emission")

        print(f"CO2 Emission: {co2_emission}")

        if co2_emission <= 50:
            relay.value(1)
            print("Der er grøn energi, Jubiiiii")
        else:
            relay.value(0)
            print("Der er ikke grøn energi, av av")
    else:
        print("Website do be down")
    sleep(300)