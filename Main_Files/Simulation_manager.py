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
    Manages the simulation by creating and updating the road network, managing cars, and printing results.

    Attributes:

    road_network (Road_Network): The road network for the simulation.

    car_manager (Car_manager): The car manager responsible for managing cars in the simulation.

    simulation_datetime_start (datetime.datetime): The starting datetime of the simulation.

    simulation_datetime (datetime.datetime): The current simulation datetime.

    simulation_time (datetime.timedelta): The current simulation time in seconds.

    simulation_update_times (list): List of times the simulation was updated.

    last_speed_update_time (datetime.datetime): The last time the road speeds were updated.

    time_limit (int): The maximum time the simulation will run in seconds.

    day_int (int): Day of the week (0-6, 0-Sunday, 1-Monday, ..., 6-Saturday).

    activate_traffic_lights (bool): Indicates whether traffic lights are activated.

    simulation_results (list): List of dictionaries containing simulation results.
    """

    def __init__(self, graph, time_limit: int, activate_traffic_lights = False,
                 start_time=datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0,
                                              second=0)):  # TODO: data path
        """
        Initialize the Simulation_manager.

        Args:
        graph: The networkx graph representing the road network.
        time_limit (int): The maximum time the simulation will run in seconds.
        activate_traffic_lights (bool, optional): Indicates whether traffic lights are activated. Default is False.
        start_time (datetime.datetime, optional): The starting datetime of the simulation. Default is June 29, 2023, 08:00:00.
        """
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
        """
        Block a road in the road network.

        Args:
        road_id (int): The ID of the road to be blocked.

        Returns:
        None
        """
        self.road_network.block_road(road_id)
        print("Road", road_id, "blocked")
        return

    def unblock_road(self, road_id):
        """
        Unblock a previously blocked road.

        Args:
        road_id (int): The ID of the road to be unblocked.

        Returns:
        None
        """
        self.road_network.unblock_road(road_id)
        print("Road", road_id, "unblocked")
        return

    def unblock_all_roads(self):
        """
        Unblock all roads in the road network.

        Returns:
        None
        """
        self.road_network.unblock_all_roads()
        print("All roads unblocked")
        return


    def update_simulation_clock(self, time: int):
        """
        Update the simulation clock and road speeds.

        Args:
        time (int): The time interval to update the simulation clock in seconds.

        Returns:
        None
        """
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
        Read road speeds from a JSON file and update the road network.

        Args:
        datetime_obj (datetime.datetime): The datetime for which road speeds are to be read.

        Returns:
        None
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
        Set up the simulation by adding cars to the car manager.

        Args:
        cars (list): List of Car objects to be added to the simulation.

        Returns:
        None
        """

        self.simulation_time = datetime.timedelta(seconds=0)  # in seconds
        self.simulation_datetime = self.simulation_datetime_start

        self.car_manager.clear()
        for car in cars:
            self.car_manager.add_car(car, self.simulation_datetime_start)
        return

    def start_simulation(self):
        """
        Start the simulation and run it until all cars finish or time limit is reached.

        Returns:
        None
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
        Print the results of the simulation.

        Args:
        simulation_number (int): The index of the current simulation.

        Returns:
        None
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
        """
        Run the full simulation process including setup, execution, and result printing.

        Args:
        cars (list): List of Car objects for the simulation.
        number_of_simulations (int, optional): Number of simulations to run. Default is 1.

        Returns:
        None
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
        Write simulation results to the simulation results list.

        Args:
        copy_cars (list): List of Car objects used in the simulation.
        i (int): Index of the current simulation.

        Returns:
        None
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
        Retrieve routes passed by cars in a simulation.

        Args:
        cars (list): List of Car objects.
        simulation_number (int): Index of the simulation.

        Returns:
        list: List of routes passed by cars in the simulation.
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
        Retrieve the corresponding key from a dictionary given a value.

        Args:
        dictionary (dict): The dictionary to search in.
        value: The value to search for.

        Returns:
        key: The key corresponding to the given value.
        """
        for key, val in dictionary.items():
            if int(val) == value:
                return key
        return None

    def transform_node_id_route_to_osm_id_route(self, route):
        """
        Transform a route from node IDs to OSM IDs.

        Args:
        route (list): List of node IDs representing a route.

        Returns:
        list: List of OSM IDs representing the transformed route.
        """
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
