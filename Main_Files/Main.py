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

# parameters

WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

SIMULATION_SPEEDS_JSON_NAME = "simulation_speeds.json"
TRAFFIC_LIGHTS = True

USE_ALREADY_GENERATED_Q_TABLE = True
NUMBER_OF_SIMULATIONS = 1

REPEAT = True
SIMULATION_SPEED = 30 # means like X30 faster than one second interval



SM = Simulation_manager.Simulation_manager('TLV_with_eta', 3 * DAY, TRAFFIC_LIGHTS, START_TIME1, SIMULATION_SPEEDS_JSON_NAME)  # graph path, time limit, activate_traffic_lights ,starting time
CM = SM.car_manager
RN = SM.road_network



# BLOCK ROADS
RN.block_road(534)
RN.block_road(116)
RN.block_road(86)
# src, dst = Simulation_manager.choose_random_src_dst(RN)

c1 = Car.Car(1, 0, 551, START_TIME1, RN, route_algorithm = "q", use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE)
# c2 = Car.Car(2, 0, 551, START_TIME4, RN, route_algorithm="q")
c3 = Car.Car(3, 0, 551, START_TIME1, RN, route_algorithm="sp")
# c4 = Car.Car(4, 200, 839, START_TIME1, RN, route_algorithm="shortest_path")
# c5 = Car.Car(5, 200, 839, START_TIME1, RN, route_algorithm="shortest_path")

cars = []
cars.append(c1)
# cars.append(c2)
cars.append(c3)
# cars.append(c4)
# cars.append(c5)

SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS)

routes = SM.get_simulation_routes(cars, 0)

ASS = AS.Animate_Simulation(animation_speed = SIMULATION_SPEED, repeat = REPEAT)
ASS.plotting_custom_route(SM, routes, cars)
# AS.car_times_bar_chart(SM, 4)
# AS.car_times_bar_chart(SM, 1)
# AS.car_times_bar_chart(SM, 3)

SRM = Simulation_Results_Manager()
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
ASS.print_simulation_results(SM)