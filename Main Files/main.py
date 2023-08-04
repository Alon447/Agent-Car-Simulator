import datetime

from new_master import Car
from new_master.Simulation_Results_Manager import Simulation_Results_Manager
import Simulation_manager
import GUI.Animate_Simulation as AS

WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60
NUMBER_OF_SIMULATIONS = 1
TRAFFIC_LIGHTS = False

# initilazires
START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=21, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)

SM = Simulation_manager.Simulation_manager('/TLV_with_eta.graphml', 20 * HOUR,
                                           START_TIME1)  # graph path, time limit, starting time
CM = SM.car_manager
RN = SM.road_network

# src, dst = Simulation_manager.choose_random_src_dst(RN)
c1 = Car.Car(1, 200, 839, START_TIME1, RN, route_algorithm="q")
c2 = Car.Car(2, 200, 839, START_TIME1, RN, route_algorithm="shortest_path")
c3 = Car.Car(3, 200, 839, START_TIME3, RN, route_algorithm="shortest_path")
c4 = Car.Car(4, 113, 703, START_TIME4, RN, route_algorithm="shortest_path")
c5 = Car.Car(5, 110, 700, START_TIME5, RN, route_algorithm="shortest_path")
cars = [c1, c2]

SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS, TRAFFIC_LIGHTS)

route1 = SM.get_simulation_route(1, 0)
route2 = SM.get_simulation_route(2, 0)
# route3 = SM.get_simulation_route(3,0)
routes = [route1, route2]
cars_ids = [1, 2]
AS.plotting_custom_route(SM,routes,cars_ids)
# SM.car_times_bar_chart(1)
# SM.car_times_bar_chart(2)
# SM.car_times_bar_chart(3)

SRM = Simulation_Results_Manager()
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
AS.print_simulation_results(SM)
