import datetime

from Main_Files import Car
from Main_Files.Simulation_Results_Manager import Simulation_Results_Manager
import Simulation_manager
import GUI.Animate_Simulation as AS



# initilazires
START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=21, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)

# Constants for time intervals
WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

# Simulation parameters
SIMULATION_SPEEDS_JSON_NAME = "simulation_speeds.json"
TRAFFIC_LIGHTS = True
USE_ALREADY_GENERATED_Q_TABLE = True
NUMBER_OF_SIMULATIONS = 1
Rain_intensity = 0 # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)
REPEAT = True
SIMULATION_SPEED = 4  # X30 faster than one second interval

# Initialize Simulation Manager
# SM = Simulation_manager.Simulation_manager('TLV_with_eta', 3 * DAY, TRAFFIC_LIGHTS, Rain_intensity, START_TIME1, SIMULATION_SPEEDS_JSON_NAME)
SM = Simulation_manager.Simulation_manager('TLV', 4 * DAY, TRAFFIC_LIGHTS, Rain_intensity, START_TIME1, SIMULATION_SPEEDS_JSON_NAME)
CM = SM.car_manager
RN = SM.road_network

# Block roads
# RN.block_road(534)
RN.plan_road_blockage(100, START_TIME1, START_TIME3)
RN.plan_road_blockage(555, START_TIME1, START_TIME3)
RN.plan_road_blockage(1000, START_TIME1, START_TIME3)
# Initialize cars
cars = []
cars.append(Car.Car(1, 10, 400, START_TIME1, RN, route_algorithm="q", use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
cars.append(Car.Car(3, 10, 400, START_TIME4, RN, route_algorithm="sp"))

# Run simulations
SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS)
routes = SM.get_simulation_routes(cars, 0)

# Initialize Animation
ASS = AS.Animate_Simulation(animation_speed=SIMULATION_SPEED, repeat=REPEAT)

# Plot and display simulation results
ASS.plotting_custom_route(SM, routes, cars)
# AS.car_times_bar_chart(SM, 4)
# AS.car_times_bar_chart(SM, 1)
# AS.car_times_bar_chart(SM, 3)

# Manage and display simulation results
SRM = Simulation_Results_Manager(SM.graph_name)
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
ASS.print_simulation_results(SM)
