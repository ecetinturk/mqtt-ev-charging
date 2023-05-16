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
import traci
import os

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# contains TraCI control loop
def run():
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        #get the id of the vehicle and charging station
        my_vehicle = traci.vehicle.getIDList()[0]
        charging_station = traci.chargingstation.getIDList()[0]
        my_charge = int(traci.vehicle.getParameter(my_vehicle, "actualBatteryCapacity"))
        #maximumBatteryCapacity = traci.vehicle.getParameter(my_vehicle, "device.battery.maximumBatteryCapacity")
        curr_charging_vehicles = traci.chargingstation.getVehicleIDs(charging_station)

        if len(curr_charging_vehicles) != 0:
            traci.vehicle.setParameter(my_vehicle, "actualBatteryCapacity", my_charge + 1)
            print('Vehicle Charge: ' + str(my_charge) + ' (CHARGING)')
        elif my_charge <= 25:
            print('Vehicle Charge: ' + str(my_charge) + ' (LOW BATTERY)')
            traci.vehicle.setParameter(my_vehicle, "actualBatteryCapacity", my_charge - 1)
            if traci.vehicle.getLaneID(my_vehicle) == 'E0_0':
                curr_charge = int(traci.vehicle.getParameter(my_vehicle, "actualBatteryCapacity"))
                tmp = 109 - curr_charge
                traci.vehicle.setChargingStationStop(my_vehicle, charging_station, tmp)
        else:
            print('Vehicle Charge: ' + str(my_charge))
            traci.vehicle.setParameter(my_vehicle, "actualBatteryCapacity", my_charge - 1)


    traci.close()
    sys.stdout.flush()

def run_test():
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        my_vehicle = traci.vehicle.getIDList()[0]
        test = traci.vehicle.getParameter(my_vehicle, "device.battery.vehicleMass")
        print(test)

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
    traci.start([sumoBinary, "-c", "karalama.sumocfg"])
    run()
    #run_test()
