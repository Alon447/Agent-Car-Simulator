import datetime

from Main_Files import Car
from Main_Files.Simulation_Results_Manager import Simulation_Results_Manager
import Simulation_manager
import GUI.Animate_Simulation as AS
from Utilities.Getters import get_random_src_dst

# initilazires
START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=19, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=13, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)

# Constants for time intervals
WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

# Simulation parameters
NUMBER_OF_SIMULATIONS = 1
TRAFFIC_LIGHTS = True
ADD_TRAFFIC_WHITE_NOISE = False
Rain_intensity = 0 # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)


# Q-Learning parameters
USE_ALREADY_GENERATED_Q_TABLE = True
NUM_EPISODES = 1000

# Animation parameters
ANIMATE_SIMULATION = True
REPEAT = True
SIMULATION_SPEED = 10  # X30 faster than one second interval

# Initialize Simulation Manager
SM = Simulation_manager.Simulation_manager('eilat', 7 * DAY, TRAFFIC_LIGHTS, Rain_intensity, ADD_TRAFFIC_WHITE_NOISE, START_TIME1)
CM = SM.car_manager
RN = SM.road_network

# Block roads
# RN.block_road(534)
# SM.update_road_blockage(168, START_TIME1)
# SM.update_road_blockage(181)
# SM.update_road_blockage(182)
# SM.update_road_blockage(912)
# SM.update_road_blockage(382)

# Initialize cars
cars = []
src, dst = get_random_src_dst(RN)
# cars.append(Car.Car(1, 15, 745, START_TIME2, RN, route_algorithm="rand", use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(Car.Car(2, src, dst, START_TIME2, RN, route_algorithm="sp", use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
cars.append(Car.Car(3, src, dst, START_TIME1, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
cars.append(Car.Car(4, src, dst, START_TIME2, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
cars.append(Car.Car(5, src, dst, START_TIME3, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))


# Run simulations
SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS)
routes = SM.get_simulation_routes(cars, 0)

# Initialize Animation
ASS = AS.Animate_Simulation(animation_speed=SIMULATION_SPEED, repeat=REPEAT)

# Plot and display simulation results
if ANIMATE_SIMULATION:
    ASS.plotting_custom_route(SM, routes, cars)
# AS.car_times_bar_chart(SM, 4)
# AS.car_times_bar_chart(SM, 1)
# AS.car_times_bar_chart(SM, 3)

# Manage and display simulation results
SRM = Simulation_Results_Manager(SM.graph_name)
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
ASS.print_simulation_results(SM)
