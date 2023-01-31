import traci

sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "sumo.sumocfg"]

traci.start(sumoCmd)

# Perform some simulation steps
for i in range(1000):
    traci.simulationStep()

# Retrieve some information from the simulation
vehicle_count = traci.vehicle.getIDCount()
vehicle_speed = traci.vehicle.getSpeed("veh0")

# Stop the simulation
traci.close()