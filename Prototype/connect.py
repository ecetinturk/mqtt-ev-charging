import traci
import paho.mqtt.client as mqtt

# Define MQTT broker settings
broker_address = "localhost"  # Replace with your broker's IP address or hostname
broker_port = 1883  # Replace with your broker's port number

# Create a MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Connect to SUMO
traci.start(["sumo", "-c", "path/to/your/simulation.sumocfg"])

# Simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Get information from SUMO and publish it via MQTT
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)
        topic = "sumo/vehicle/{}".format(vehicle_id)
        message = "Speed: {}".format(vehicle_speed)
        client.publish(topic, message)

# Disconnect from SUMO and MQTT broker
traci.close()
client.disconnect()
