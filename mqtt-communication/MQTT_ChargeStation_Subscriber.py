import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")) + " Battery Level of EV")

mqttBroker = "127.0.0.1"
client = mqtt.Client("Charge Station")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("BATTERY")
client.on_message = on_message
time.sleep(1000000)
client.loop_end()


