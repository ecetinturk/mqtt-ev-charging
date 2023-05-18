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

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options
##TEST###

##TEST###
# contains TraCI control loop
def run():
    #client2.on_message = on_message
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()


    traci.close()
    sys.stdout.flush()

def run_test():

    traci.vehicle.setParameter("v_0", "device.battery.maximumBatteryCapacity", "100")
    traci.vehicle.setParameter("v_1", "device.battery.maximumBatteryCapacity", "100")
    traci.vehicle.setParameter("v_2", "device.battery.maximumBatteryCapacity", "100")
    traci.vehicle.setParameter("v_3", "device.battery.maximumBatteryCapacity", "100")

    traci.vehicle.setParameter("v_0", "device.battery.actualBatteryCapacity", "100")
    traci.vehicle.setParameter("v_1", "device.battery.actualBatteryCapacity", "100")
    traci.vehicle.setParameter("v_2", "device.battery.actualBatteryCapacity", "100")
    traci.vehicle.setParameter("v_3", "device.battery.actualBatteryCapacity", "100")

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for car_id in traci.vehicle.getIDList():
            current_lane = traci.vehicle.getRoadID(car_id)

            if current_lane == "697983200":
                traci.vehicle.setRouteID(car_id, "basa_don")
            if traci.vehicle.getRoadID(car_id) == "697983203":
                # car is stopped, choose a random destination edge
                route_id = random.choice(traci.route.getIDList())
                while route_id == "basa_don":
                    route_id = random.choice(traci.route.getIDList())
                traci.vehicle.setRouteID(car_id, route_id)

            #if traci.vehicle.getParameter(car_id, "device.battery.actualBatteryCapacity") == "0.00":
                #traci.vehicle.setSpeed(car_id, 0.00)
                #print(car_id + " SARJI BITTI!\n")

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
