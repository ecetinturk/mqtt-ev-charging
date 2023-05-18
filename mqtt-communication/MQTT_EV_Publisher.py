import paho.mqtt.client as mqtt
import time

mqttBroker = "127.0.0.1"
client = mqtt.Client("Electric Vehicle")
client.connect(mqttBroker)

charge_level = 100

for _ in range(100, -1, -1):
    client.publish("BATTERY", charge_level)
    if charge_level > 25: 
        print(f"Just published {charge_level} to EV Charge Station")
    if charge_level < 25:
        print(f"Just published {charge_level} to EV Charge Station  -  BATTERY LOW") 
    if charge_level == 0:
        print(f"Just published {charge_level} to EV Charge Station  -  BATTERY DEAD") 
    charge_level -= 1
    time.sleep(1)
    

