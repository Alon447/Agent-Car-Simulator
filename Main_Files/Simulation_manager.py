import datetime
import json
import random

import networkx as nx
import pandas as pd

import Car_manager
import Road_Network
from Main_Files import Car
from Main_Files.Car import time_delta_to_seconds


class Simulation_manager:
    """
    This class manages the simulation.
    It will create the road network, the cars, the route algorithm and the q tables.
    It will also update the simulation and print the results.


    """

    def __init__(self, graph, time_limit: int, activate_traffic_lights = False,
                 start_time=datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0,
                                              second=0)):  # TODO: data path
        # MANAGERS
        self.road_network = Road_Network.Road_Network(graph, activate_traffic_lights)
        self.car_manager = Car_manager.CarManager()

        # TIME
        self.simulation_datetime_start = start_time
        self.simulation_datetime = start_time
        self.simulation_time = datetime.timedelta(seconds=0)  # in seconds
        self.simulation_update_times = []  # list of times the simulation was updated for the animation
        self.last_speed_update_time = start_time
        self.time_limit = time_limit  # the maximum time the simulation will run in seconds
        self.day_int = 0  # 0-6, 0-sunday, 1-monday, 2-tuesday, 3-wednesday, 4-thursday, 5-friday, 6-saturday
        self.activate_traffic_lights = activate_traffic_lights

        # RESULTS
        self.simulation_results = []  # list of dictionaries, each dictionary is a simulation result
        # FUNCTIONS - read speeds
        self.read_road_speeds(self.simulation_datetime_start)

    # FUNCTIONS - block/unblock roads
    def block_road(self, road_id):
        self.road_network.block_road(road_id)
        print("Road", road_id, "blocked")
        return

    def unblock_road(self, road_id):
        self.road_network.unblock_road(road_id)
        print("Road", road_id, "unblocked")
        return

    def unblock_all_roads(self):
        self.road_network.unblock_all_roads()
        print("All roads unblocked")
        return


    def update_simulation_clock(self, time: int):
        # update both the spesific simulation time and the datetime
        self.simulation_time += pd.Timedelta(seconds=time)  # time
        self.simulation_datetime += pd.Timedelta(seconds=time)  # time
        self.simulation_update_times.append(self.simulation_datetime)
        time_difference = self.simulation_datetime - self.last_speed_update_time

        if (self.simulation_datetime.minute % 10 == 0 and self.simulation_datetime.minute - self.last_speed_update_time.minute > 0) or time_difference.seconds >= 600:
            # update the road speeds according to the time
            # every 10 minutes or at the next time a car will be updated (if more than 10 minutes passed)

            minutes = int(self.simulation_datetime.minute / 10) * 10
            self.last_speed_update_time = self.simulation_datetime.replace(minute=minutes).replace(second=0).replace(microsecond=0)

            time_key = self.simulation_datetime.replace(minute=minutes).strftime("%H:%M")
            self.road_network.update_roads_speeds(time_key) #updates the road speeds according to the current time

            print(self.simulation_datetime.strftime("%H:%M:%S"))
        return
    def read_road_speeds(self, datetime_obj: datetime.datetime):
        """
        reads the road speeds from the json file and updates the road_network according to the time
        currently the time slice is every 10 minutes.
        :param datetime_obj:
        :return:
        """
        self.last_speed_update_time = datetime_obj.replace(second=0, microsecond=0)
        number_of_roads = len(self.road_network.roads_array)
        self.day_int = (datetime_obj.weekday() + 1) % 7
        with open('simulation_speeds.json', 'r') as infile:
            data = json.load(infile)

        # time_key = datetime_obj.strftime("%H:%M")  # Format the datetime object as HH:MM

        # round the minutes to the nearest 10
        minutes = int(datetime_obj.minute / 10) * 10
        time_key = datetime_obj.replace(minute=minutes).strftime("%H:%M")
        day_data = data.get(str(self.day_int), {})
        self.road_network.set_roads_speeds_from_dict(day_data, time_key, self.activate_traffic_lights)
        return

    def set_up_simulation(self, cars: list):
        """
        sets up the simulation, resets the clocks, adds the cars to the car manager
        :param cars:
        :return:
        """

        self.simulation_time = datetime.timedelta(seconds=0)  # in seconds
        self.simulation_datetime = self.simulation_datetime_start

        self.car_manager.clear()
        for car in cars:
            self.car_manager.add_car(car, self.simulation_datetime_start)
        return

    def start_simulation(self):
        """
        runs the simulation until there are no more cars in the simulation ot it gets to a time limit
        :return:
        """
        while int(self.simulation_time.total_seconds()) < self.time_limit and (self.car_manager.cars_in_simulation or self.car_manager.cars_waiting_to_enter):
            # rnd = random.randint(0, 100)
            # blocked_roads = self.road_network.get_blocked_roads_array()
            # if rnd == 0 and len(blocked_roads) !=0:
            #     self.road_network.unblock_all_roads()
            #     print("Roads unblocked")

            time = self.car_manager.calc_nearest_update_time(self.simulation_datetime)
            self.update_simulation_clock(time)
            self.car_manager.update_cars(time, self.simulation_datetime)
            # print("simulation_time:", SM.simulation_time)
            # self.car_manager.show_cars_in_simulation()

        for carInd in self.car_manager.cars_in_simulation:
            car = self.car_manager.cars_in_simulation[carInd]  # dict so we need to get the car object
            self.car_manager.cars_stuck.append(car)
        # self.car_manager.force_cars_to_finish()
        for car in self.car_manager.cars_stuck:
            car.force_finish()
        return

    def end_simulation(self, simulation_number):
        """
        prints the results of the simulation
        :param simulation_number:
        :return:
        """
        simulation_number += 1
        simulation_time_seconds = time_delta_to_seconds(self.simulation_time)
        if simulation_time_seconds >= 3600:
            if simulation_time_seconds % 3600 == 0:
                print("simulation", simulation_number, "finished after", int(simulation_time_seconds / 3600), "hours")
            else:
                print("simulation", simulation_number, "finished after", int(simulation_time_seconds / 3600),
                      "hours and ", int(simulation_time_seconds % 60), "minutes")
        else:
            print("simulation", simulation_number, "finished after", int(simulation_time_seconds / 60), "minutes")
        print("************************************")
        return

    def run_full_simulation(self, cars, number_of_simulations=1):
        """ TODO: add traffic lights
        runs the full simulation, including setting up the simulation, starting it and ending it
        :param cars:
        :param number_of_simulations:
        :return:
        """
        # self.block_road(0)
        # self.block_road(900)
        # self.block_road(901)
        # self.block_road(902)

        # self.read_road_speeds(self.simulation_datetime_start) #NOT NEEDED ANYMORE

        for i in range(number_of_simulations):
            copy_cars = []
            # make a deep copy of the cars list
            if number_of_simulations > 1:
                for car in cars:
                    new_car = Car.Car(car.id,
                                      car.source_node,
                                      car.destination_node,
                                      car.starting_time,
                                      self.road_network,
                                      car.get_routing_algorithm())
                    copy_cars.append(new_car)
            else:
                copy_cars = cars

            # set up the simulation
            self.set_up_simulation(copy_cars)
            self.start_simulation()
            self.end_simulation(i)
            # self.road_network.unblock_all_roads()
            self.write_simulation_results(copy_cars, i)

        return

    def write_simulation_results(self, copy_cars: list, i: int):
        """
        writes the simulation results to the simulation results list
        :param copy_cars: list of all the cars in the spesific simulation
        :param i:
        :return:
        """
        simulation_results = {}
        for j, car in enumerate(copy_cars):
            car_reached_destination = self.car_manager.is_car_finished(car)
            car_time_taken = int(car.total_travel_time.total_seconds()) # car.get_total_travel_time()
            car_starting_time = str(car.starting_time)
            car_ending_time = str(car.total_travel_time + car.starting_time)
            car_route = car.past_nodes
            car_key = car.id
            day_of_week_str = car.starting_time.strftime('%A')
            # save the important data
            simulation_results[car_key] = {
                'reached_destination': car_reached_destination,
                'routing_algorithm': car.get_routing_algorithm(),
                'time_taken': car_time_taken,  # in seconds
                'day_of_week': day_of_week_str,  # day of the week string
                'start_time': car_starting_time,  # datetime object string
                'end_time': car_ending_time,  # datetime object string
                'route': car_route,
                'roads_used': car.past_roads,
                'distance_travelled': int(car.distance_traveled),  # in meters, int
            }

        self.simulation_results.append({
            'simulation_number': i + 1,
            **simulation_results
        })

    def get_simulation_routes(self, cars: list, simulation_number: int):
        """
        :param cars: list of cars to get the routes they passed in the simulation
        :param simulation_number:
        :return: list of routes
        """
        cars_ids = [car.id for car in cars]
        routes = []
        for carInd in cars_ids:
            if self.simulation_results[simulation_number][carInd]['route'] == None:
                pass
            else:
                routes.append(self.simulation_results[simulation_number][carInd]['route'])
        return routes

    def get_key_from_value(self, dictionary, value):
        """
         get a corresponding key from a dict and a value
        :param dictionary:
        :param value:
        :return: key
        """
        for key, val in dictionary.items():
            if int(val) == value:
                return key

    def transform_node_id_route_to_osm_id_route(self, route):
        osm_route = []
        for node in route:
            osm_route.append(self.road_network.nodes_array[node].osm_id)
        return osm_route


# WEEK = 604800
# DAY = 86400
# HOUR = 3600
# MINUTE = 60
#
# # initilazires
# START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
# START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
# START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=21, minute=0, second=0)
# START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
# START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)
#
# SM = Simulation_manager('/TLV_with_eta.graphml', 20 * HOUR, START_TIME1)  # graph path, time limit, starting time
# CM = SM.car_manager
# RN = SM.road_network

#
# def choose_random_src_dst(road_network):
#     src = random.Random().randint(0, len(road_network.node_connectivity_dict) - 1)
#     dst = random.Random().randint(0, len(road_network.node_connectivity_dict) - 1)
#     src_osm = road_network.reverse_node_dict[src]
#     dest_osm = road_network.reverse_node_dict[dst]
#     while (not nx.has_path(road_network.graph, src_osm, dest_osm)) or src == dst:
#         # print(f"There is no path between {src} and {dst}.")
#         src = random.Random().randint(0, len(road_network.node_connectivity_dict) - 1)
#         dst = random.Random().randint(0, len(road_network.node_connectivity_dict) - 1)
#         src_osm = road_network.reverse_node_dict[src]
#         dest_osm = road_network.reverse_node_dict[dst]
#     return src, dst
#

# def Test():
#     res = []
#     for i in range(1):
#         src, dst = choose_random_src_dst(RN)
#         print("simulation number: ", i)
#         print("src: ", src, "dst: ", dst)
#         c1 = Car.Car(1, src, dst, START_TIME1, RN, route_algorithm="q")
#         c2 = Car.Car(2, src, dst, START_TIME1, RN, route_algorithm="shortest_path")
#         cars = [c1, c2]
#
#         SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS, TRAFFIC_LIGHTS)
#
#         # route1 = SM.get_simulation_route(1, 0)
#         # route2 = SM.get_simulation_route(2, 0)
#         print(c1.total_travel_time)
#         print( c2.total_travel_time)
#         if c1.total_travel_time <= c2.total_travel_time:
#             print("Q learning is better")
#             res.append(1)
#         else:
#             print("Shortest path is better")
#             res.append(0)
#         percent = 100 * sum(res) / len(res)
#         print("percent: ", percent, "%")
#         print("************************************")

#
# NUMBER_OF_SIMULATIONS = 1
# TRAFFIC_LIGHTS = False
# Test()
"""
src, dst = choose_random_src_dst(RN)
c1 = Car.Car(1,src,dst,START_TIME1,RN,route_algorithm = "q")
c2 = Car.Car(2,200,839,START_TIME1,RN,route_algorithm = "shortest_path")
c3 = Car.Car(3,200,839,START_TIME3,RN,route_algorithm = "shortest_path")
c4 = Car.Car(4,113,703,START_TIME4,RN,route_algorithm = "shortest_path")
c5 = Car.Car(5,110,700,START_TIME5,RN,route_algorithm = "shortest_path")
cars = [c1,c2]

SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS,TRAFFIC_LIGHTS)
print("***************************")


route1 = SM.get_simulation_route(1,0)
route2 = SM.get_simulation_route(2,0)
# route3 = SM.get_simulation_route(3,0)
routes=[route1,route2]
SM.plotting_custom_route(routes)
# SM.car_times_bar_chart(1)
# SM.car_times_bar_chart(2)
# SM.car_times_bar_chart(3)

SRM = Simulation_Results_Manager()
SRM.save_results_to_JSON(SM.simulation_results)
SM.simulation_results = SRM.read_results_from_JSON()
SM.print_simulation_results()
"""