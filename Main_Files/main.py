import datetime

from Main_Files import Car
from Main_Files.Simulation_Results_Manager import Simulation_Results_Manager
import Simulation_manager
import GUI.Animate_Simulation as AS

WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60


# initilazires
START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=21, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)



# src, dst = Simulation_manager.choose_random_src_dst(RN)

TRAFFIC_LIGHTS = True
SM = Simulation_manager.Simulation_manager('/TLV_with_eta.graphml', 3 * DAY, TRAFFIC_LIGHTS, START_TIME1)  # graph path, time limit, activate_traffic_lights ,starting time
CM = SM.car_manager
RN = SM.road_network
NUMBER_OF_SIMULATIONS = 1
c1 = Car.Car(1, 200, 839, START_TIME1, RN, route_algorithm="q")
c2 = Car.Car(2, 200, 839, START_TIME1, RN, route_algorithm="shortest_path")
c3 = Car.Car(3, 200, 839, START_TIME3, RN, route_algorithm="shortest_path")
c4 = Car.Car(4, 113, 703, START_TIME4, RN, route_algorithm="shortest_path")
c5 = Car.Car(5, 110, 700, START_TIME5, RN, route_algorithm="shortest_path")

cars = []
cars.append(c1)
cars.append(c2)
cars.append(c3)
cars.append(c4)
cars.append(c5)

SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS)


# route1 = SM.get_simulation_route(1, 0)
# route2 = SM.get_simulation_route(2, 0)
# route3 = SM.get_simulation_route(3,0)
# routes = [route1, route2]
routes = SM.get_simulation_routes(cars, 0)
AS.plotting_custom_route(SM, routes, cars)
# AS.car_times_bar_chart(SM, 4)
# SM.car_times_bar_chart(SM, 2)
# SM.car_times_bar_chart(SM, 3)

SRM = Simulation_Results_Manager()
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
AS.print_simulation_results(SM)
