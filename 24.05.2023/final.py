#!/usr/bin/env python

import os
import sys
import optparse
from sumolib import checkBinary  # Checks for the binary in environ vars
import random
import traci
import time
import os
import paho.mqtt.client as mqtt
import threading

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Car:
    def __init__(self, _battery = 0):
        self.battery = _battery

    # getter method
    def get_battery(self):
        return self.battery

    # setter method
    def set_battery(self, x):
        self.battery = x

v0 = Car()
v1 = Car()
v2 = Car()
v3 = Car()
v4 = Car()

broker="127.0.0.1"
port =1884
ssl_port=8883 #ssl

clients = []

Normal_connections=5
SSL_Connections=0 #no ssl connections illustration only
message="test message"
topic="BATTERY"
out_queue=[] #use simple array to get printed messages in some form of order
def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   time.sleep(1)
   msg="message received",str(message.payload.decode("utf-8"))
   #print(msg)
   out_queue.append(msg)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        client.subscribe(topic)
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()
def on_disconnect(client, userdata, rc):
   pass
   #print("client disconnected ok")
def on_publish(client, userdata, mid):
   time.sleep(1)
   print("In on_pub callback mid= "  ,mid)


def Create_connections(nclients,port,SSL_Flag=False):
   for i in range(nclients):
      if SSL_Flag:
         cname ="python-ssl"+str(i)
      else:
         cname ="python-"+str(i)
      client = mqtt.Client(cname)             #create new instance

      if SSL_Flag:
         client.tls_set('c:/python34/steve/MQTT-demos/certs/ca-pi.crt')
      #client.connected_flag=False #create flag in client

      client.connect(broker,port)           #establish connection
      #client.on_log=on_log #this gives getailed logging
      client.on_connect = on_connect
      client.on_disconnect = on_disconnect
      #client.on_publish = on_publish
      client.on_message = on_message
      clients.append(client)
      client.loop_start()
      while not client.connected_flag:
         time.sleep(0.05)

def send_message():
    mqtt.Client.connected_flag = False  # create flag in class
    no_threads = threading.active_count()
    print("current threads =", no_threads)
    print("Creating Normal Connections ", Normal_connections, " clients")
    Create_connections(Normal_connections, port, False)
    if SSL_Connections != 0:
        print("Creating SSL Connections ", SSL_Connections, " clients")
        Create_connections(SSL_Connections, ssl_port, True)

    print("All clients connected ")
    time.sleep(5)
    #
    count = 0
    no_threads = threading.active_count()
    print("current threads =", no_threads)
    print("Publishing ")

    Run_Flag = True
    try:
        while Run_Flag:
            i = 0
            for client in clients:
                counter = str(count).rjust(6, "0")
                #msg = "client " + str(i) + " " + counter + "XXXXXX " + message

                msg = "deneme"

                if i == 0:
                    msg = "vehicle v_0: " + str(v0.get_battery())
                elif i == 1:
                    msg = "vehicle v_1: " + str(v1.get_battery())
                elif i == 2:
                    msg = "vehicle v_2: " + str(v2.get_battery())
                elif i == 3:
                    msg = "vehicle v_3: " + str(v3.get_battery())
                elif i == 4:
                    msg = "vehicle v_4: " + str(v4.get_battery())
                else:
                    msg = "unknown vehicle: " + "NULL"

                client.publish(topic, msg)
                time.sleep(0.1)
                print("publishing client " + str(i))
                i += 1
            time.sleep(10)  # now print messages
            print("queue length=", len(out_queue))
            for x in range(len(out_queue)):
                print(out_queue.pop())
            count += 1
            # time.sleep(5)#wait
    except KeyboardInterrupt:
        print("interrupted  by keyboard")

    # client.loop_stop() #stop loop
    for client in clients:
        client.disconnect()
        client.loop_stop()
    # allow time for allthreads to stop before existing
    time.sleep(10)

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run():

    battery_capacity = "1000"
    traci.vehicle.setParameter("v_0", "device.battery.maximumBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_1", "device.battery.maximumBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_2", "device.battery.maximumBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_3", "device.battery.maximumBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_4", "device.battery.maximumBatteryCapacity", battery_capacity)

    traci.vehicle.setParameter("v_0", "device.battery.actualBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_1", "device.battery.actualBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_2", "device.battery.actualBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_3", "device.battery.actualBatteryCapacity", battery_capacity)
    traci.vehicle.setParameter("v_4", "device.battery.actualBatteryCapacity", battery_capacity)

    v0.battery = battery_capacity
    v1.battery = battery_capacity
    v2.battery = battery_capacity
    v3.battery = battery_capacity
    v4.battery = battery_capacity

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for car_id in traci.vehicle.getIDList():
            current_lane = traci.vehicle.getRoadID(car_id)

            if current_lane == "697983200":
                traci.vehicle.setRouteID(car_id, "basa_don")

            if traci.vehicle.getRoadID(car_id) == "697983203":
                # car is stopped, choose a random destination edge
                route_id = random.choice(traci.route.getIDList())
                while route_id == "basa_don" or route_id == "r_0" or route_id == "r_1" or route_id == "r_2" or route_id == "r_3" or route_id == "r_4" or route_id == "r_12" or route_id == "r_13" or route_id == "r_14":
                    route_id = random.choice(traci.route.getIDList())
                traci.vehicle.setRouteID(car_id, route_id)

            current_charge = float(traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity"))
            current_route = traci.vehicle.getRouteID(car_id)

            if(car_id == "v_0"):
                v0.battery = current_charge
            elif(car_id == "v_1"):
                v1.battery = current_charge
            elif (car_id == "v_2"):
                v2.battery = current_charge
            elif (car_id == "v_3"):
                v3.battery = current_charge
            elif (car_id == "v_4"):
                v4.battery = current_charge


            # station: cs_0
            if current_lane == "-368620842#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_1")
                traci.vehicle.setChargingStationStop(car_id, "cs_0", 1000 - current_charge)
            if current_lane == "-368620842#100.25" and current_route == "r_1":
                traci.vehicle.setRouteID(car_id, "r_8")

            # station: cs_4
            if current_lane == "368620842#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_0")
                traci.vehicle.setChargingStationStop(car_id, "cs_4", 1000 - current_charge)
            if current_lane == "368620842#10.79" and current_route == "r_0":
                traci.vehicle.setRouteID(car_id, "r_7")

            # station: cs_5
            if current_lane == "668817633" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_2")
                traci.vehicle.setChargingStationStop(car_id, "cs_5", 1000 - current_charge)
            if current_lane == "6688176330" and current_route == "r_2":
                traci.vehicle.setRouteID(car_id, "r_6")

            # station: cs_7
            if current_lane == "-668817633" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_3")
                traci.vehicle.setChargingStationStop(car_id, "cs_7", 1000 - current_charge)
            if current_lane == "-6688176330" and current_route == "r_3":
                traci.vehicle.setRouteID(car_id, "r_7")

            # station: cs_6
            if current_lane == "369625682#1" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_4")
                traci.vehicle.setChargingStationStop(car_id, "cs_6", 1000 - current_charge)
            if current_lane == "369625682#1.62" and current_route == "r_4":
                traci.vehicle.setRouteID(car_id, "r_8")

            # station: cs_3
            if current_lane == "369628890#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_12")
                traci.vehicle.setChargingStationStop(car_id, "cs_3", 1000 - current_charge)
            if current_lane == "369628890#10.115" and current_route == "r_12":
                traci.vehicle.setRouteID(car_id, "r_5")

            # station: cs_2
            if current_lane == "-212712097#5" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_14")
                traci.vehicle.setChargingStationStop(car_id, "cs_2", 1000 - current_charge)
            if current_lane == "-212712097#40" and current_route == "r_14":
                traci.vehicle.setRouteID(car_id, "r_6")

            # station: cs_1
            if current_lane == "212712097#4" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_13")
                traci.vehicle.setChargingStationStop(car_id, "cs_1", 1000 - current_charge)
            if current_lane == "212712097#5" and current_route == "r_13":
                traci.vehicle.setRouteID(car_id, "r_9")

            #sarj biterse
            if traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity") == "0.00":
                traci.vehicle.setSpeed(car_id, 0.00)

            tuketim0 = traci.vehicle.getParameter("v_0", "device.battery.actualBatteryCapacity")
            print(tuketim0)


    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "final.sumocfg"])
    #run()
    t1 = threading.Thread(target=run)
    t2 = threading.Thread(target=send_message)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
