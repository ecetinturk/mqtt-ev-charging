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
import traci
import os
import paho.mqtt.client as mqtt

mqttBroker = "127.0.0.1"

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
def charge(car_id, cs_id, charging_time):
    client_ev = mqtt.Client("Electric Vehicle")
    client_cs = mqtt.Client("Charging Station")
    client_cs.subscribe("BATTERY")
    client_cs.on_message = on_message

    for x in range(charging_time):
        current_charge = traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity")
        client_ev.publish("BATTERY", current_charge)


def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")) + " Battery Level of EV")

def run_test():

    traci.vehicle.setParameter("v_0", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_1", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_2", "device.battery.maximumBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_3", "device.battery.maximumBatteryCapacity", "1000")

    traci.vehicle.setParameter("v_0", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_1", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_2", "device.battery.actualBatteryCapacity", "1000")
    traci.vehicle.setParameter("v_3", "device.battery.actualBatteryCapacity", "1000")

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
            if current_lane == "-368620842#10" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_1")
                traci.vehicle.setChargingStationStop(car_id, "cs_0", 1000 - current_charge)
            if current_lane == "-368620842#100.25" and current_route == "r_1":
                traci.vehicle.setRouteID(car_id, "r_9")

            # station: cs_7
            if current_lane == "-668817633" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_3")
                traci.vehicle.setChargingStationStop(car_id, "cs_7", 1000 - current_charge)
            if current_lane == "-6688176330" and current_route == "r_3":
                traci.vehicle.setRouteID(car_id, "r_6")
            #if traci.chargingstation.getVehicleIDs(cs_7)

            # station: cs_6
            if current_lane == "369625682#1" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_4")
                traci.vehicle.setChargingStationStop(car_id, "cs_6", 1000 - current_charge)
            if current_lane == "369625682#1.62" and current_route == "r_4":
                traci.vehicle.setRouteID(car_id, "r_8")

            # station: cs_3
            if current_lane == "369628890#10" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_12")
                traci.vehicle.setChargingStationStop(car_id, "cs_3", 1000 - current_charge)
            if current_lane == "369628890#10.115" and current_route == "r_12":
                traci.vehicle.setRouteID(car_id, "r_8")

            # station: cs_2
            if current_lane == "-212712097#5" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_14")
                traci.vehicle.setChargingStationStop(car_id, "cs_2", 1000 - current_charge)
            if current_lane == "-212712097#40" and current_route == "r_14":
                traci.vehicle.setRouteID(car_id, "r_5")

            # station: cs_1
            if current_lane == "212712097#4" and current_charge < 250:
                traci.vehicle.setRouteID(car_id, "r_13")
                traci.vehicle.setChargingStationStop(car_id, "cs_1", 1000 - current_charge)
            if current_lane == "212712097#5" and current_route == "r_13":
                traci.vehicle.setRouteID(car_id, "r_9")

            #sarj biterse
            if traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity") == "0.00":
                traci.vehicle.setSpeed(car_id, 0.00)

            tuketim0 = traci.vehicle.getParameter("v_0", "device.battery.actualBatteryCapacity")
            tuketim1 = traci.vehicle.getParameter("v_1", "device.battery.actualBatteryCapacity")
            tuketim2 = traci.vehicle.getParameter("v_2", "device.battery.actualBatteryCapacity")
            tuketim3 = traci.vehicle.getParameter("v_3", "device.battery.actualBatteryCapacity")
            print(tuketim0 + " " + tuketim1 + " " + tuketim2 + " " + tuketim3 + "\n")



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
