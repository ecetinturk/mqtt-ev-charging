import os
import traci
import paho.mqtt.client as mqtt

# Define MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Additional actions to take upon successful connection

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    # Additional actions to take upon receiving a message

# Create MQTT client instance and connect to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)

# Start the MQTT client loop
client.loop_start()

# Connect to SUMO and start the simulation
sumo_cmd = "a.sumocfg"  # Replace with your SUMO configuration file
traci.start(sumo_cmd)

# Main simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Publish traffic information to MQTT topics
    traffic_data = {
        "vehicles": traci.vehicle.getIDList(),
        "edges": traci.edge.getIDList(),
        # Additional traffic data to publish
    }
    # Publish traffic data as a JSON string to a specific topic
    client.publish("traffic_data", str(traffic_data))

# Stop the MQTT client loop and disconnect from the broker
client.loop_stop()
client.disconnect()

# Close the SUMO simulation
traci.close()
