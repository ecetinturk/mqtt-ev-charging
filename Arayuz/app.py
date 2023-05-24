#app1
"""
from flask import Flask
import paho.mqtt.client as mqtt
import time

mqtt_message = "test"

def on_message(client, userdata, message):
    #print("Received message: " + str(message.payload.decode("utf-8")) + " Battery Level of EV")
    mqtt_message = str(message.payload.decode("utf-8"))

mqttBroker = "127.0.0.1"
mqttPort = 1884
client = mqtt.Client("Charge Station")
client.connect(mqttBroker, mqttPort)

client.loop_start()
client.subscribe("BATTERY")
client.on_message = on_message
time.sleep(1000000)
client.loop_end()

app = Flask(__name__)
@app.route('/')
def index():
    return f"The current parameter value is: {mqtt_message}"
    #return "<h1>Hello World!</h1>"

#if __name__ == '__main__':
    #app.run("127.0.0.1", 5000)
"""

#app2
"""
from flask import Flask
import paho.mqtt.client as mqtt

app = Flask(__name__)

# The parameter value
parameter_value = 0

def on_message(client, userdata, message):
    global parameter_value
    parameter_value = int(message.payload.decode("utf-8"))
    print("Received Message: " + str(parameter_value))

@app.route('/')
def show_parameter_value():
    return f"The current parameter value is: {parameter_value}"

if __name__ == '__main__':
    # MQTT broker details
    broker_address = "127.0.0.1"
    broker_port = 1884
    topic = "BATTERY"

    # Create MQTT client and connect
    client = mqtt.Client()
    client.connect(broker_address, broker_port)

    # Set up callback function for incoming messages
    client.on_message = on_message

    # Subscribe to the topic
    client.subscribe(topic)

    # Start the MQTT client loop in a new thread
    client.loop_start()

    # Run the Flask application
    app.run()

    # Stop the MQTT client loop
    client.loop_stop()
    client.disconnect()
"""
from flask import Flask, render_template
from flask import send_from_directory
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# MQTT broker details
mqtt_broker = '127.0.0.1'
mqtt_port = 1884
mqtt_topic = 'BATTERY'

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print('Received message:', message)
    socketio.emit('mqtt_message', message)

# Create MQTT client and set up callbacks
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('mqtt_message', 'Connected to MQTT broker')

if __name__ == '__main__':
    # Start the MQTT client in a separate thread
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.loop_start()

    # Run the Flask application
    socketio.run(app)

