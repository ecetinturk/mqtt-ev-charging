#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import random
import time
import traci
import os
import paho.mqtt.client as mqtt
from functools import partial

mqttBroker = "127.0.0.1"
client_ev = mqtt.Client("Electric Vehicle")
client_cs = mqtt.Client("Charging Station")
client_cs.connect(mqttBroker, 1884)
client_ev.connect(mqttBroker, 1884)

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# contains TraCI control loop
def run():
    #client2.on_message = on_message
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()


    traci.close()
    sys.stdout.flush()

#traci.vehicle.setChargingStationStop(car_id, cs_id, charging_time)
def charge(car_id):
    client_cs.loop_start()
    client_cs.subscribe("BATTERY")
    client_cs.on_message = partial(on_message, car_id)
    #time.sleep(5)
    client_cs.loop_end()

    current_charge = traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity")
    client_ev.publish("BATTERY", current_charge)

def on_message(client, userdata, message, car_id):
    #arac sarj oluyor
    charge = str(int(str(message.payload.decode("utf-8"))) + 1)
    traci.vehicle.setParameter(car_id, "device.battery.actualBatteryCapacity", charge)
    print("Received message: " + str(message.payload.decode("utf-8")) + " Battery Level of EV")


def run_test():

    traci.vehicle.setParameter("v_0", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_1", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_2", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_3", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_4", "device.battery.maximumBatteryCapacity", "1000")

    traci.vehicle.setParameter("v_0", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_1", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_2", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_3", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_4", "device.battery.actualBatteryCapacity", "1000")

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

            #if current_lane == "" and current_charge < 250:
                #traci.vehicle.setRouteID(car_id, "")
            #if current_lane == "" and current_route == "":
                #traci.vehicle.setRouteID(car_id, "")

            current_charge = float(traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity"))
            current_route = traci.vehicle.getRouteID(car_id)
            # station: cs_0
            if current_lane == "-368620842#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_1")
                traci.vehicle.setChargingStationStop(car_id, "cs_0", 1000 - current_charge)
            if current_lane == "-368620842#100.25" and current_route == "r_1":
                traci.vehicle.setRouteID(car_id, "r_8")
            try:
                if traci.chargingstation.getVehicleIDs("cs_0")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")


            # station: cs_4
            if current_lane == "368620842#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_0")
                traci.vehicle.setChargingStationStop(car_id, "cs_4", 1000 - current_charge)
            if current_lane == "368620842#10.79" and current_route == "r_0":
                traci.vehicle.setRouteID(car_id, "r_7")
            try:
                if traci.chargingstation.getVehicleIDs("cs_4")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_5
            if current_lane == "668817633" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_2")
                traci.vehicle.setChargingStationStop(car_id, "cs_5", 1000 - current_charge)
            if current_lane == "6688176330" and current_route == "r_2":
                traci.vehicle.setRouteID(car_id, "r_6")
            try:
                if traci.chargingstation.getVehicleIDs("cs_5")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_7
            if current_lane == "-668817633" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_3")
                traci.vehicle.setChargingStationStop(car_id, "cs_7", 1000 - current_charge)
            if current_lane == "-6688176330" and current_route == "r_3":
                traci.vehicle.setRouteID(car_id, "r_7")
            try:
                if traci.chargingstation.getVehicleIDs("cs_7")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_6
            if current_lane == "369625682#1" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_4")
                traci.vehicle.setChargingStationStop(car_id, "cs_6", 1000 - current_charge)
            if current_lane == "369625682#1.62" and current_route == "r_4":
                traci.vehicle.setRouteID(car_id, "r_8")
            try:
                if traci.chargingstation.getVehicleIDs("cs_6")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_3
            if current_lane == "369628890#10" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_12")
                traci.vehicle.setChargingStationStop(car_id, "cs_3", 1000 - current_charge)
            if current_lane == "369628890#10.115" and current_route == "r_12":
                traci.vehicle.setRouteID(car_id, "r_5")
            try:
                if traci.chargingstation.getVehicleIDs("cs_3")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_2
            if current_lane == "-212712097#5" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_14")
                traci.vehicle.setChargingStationStop(car_id, "cs_2", 1000 - current_charge)
            if current_lane == "-212712097#40" and current_route == "r_14":
                traci.vehicle.setRouteID(car_id, "r_6")
            try:
                if traci.chargingstation.getVehicleIDs("cs_2")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

            # station: cs_1
            if current_lane == "212712097#4" and current_charge < 350:
                traci.vehicle.setRouteID(car_id, "r_13")
                traci.vehicle.setChargingStationStop(car_id, "cs_1", 1000 - current_charge)
            if current_lane == "212712097#5" and current_route == "r_13":
                traci.vehicle.setRouteID(car_id, "r_9")
            try:
                if traci.chargingstation.getVehicleIDs("cs_1")[0] == car_id:
                    for x in range(1000 - int(current_charge)):
                        charge(car_id)
            except:
                print("")

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
    run_test()

