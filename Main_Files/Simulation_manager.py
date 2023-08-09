import datetime
import json
import random

import networkx as nx
import pandas as pd

import Car_manager
import Road_Network
from Main_Files import Car
from Utilities.Getters import time_delta_to_seconds, get_simulation_speeds_file_path


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

    last_current_speed_update_time (datetime.datetime): The last time the road speeds were updated.

    time_limit (int): The maximum time the simulation will run in seconds.

    day_int (int): Day of the week (0-6, 0 - monday, 1 - tuesday, 2 - wednesday, 3 - thursday, 4 - friday, 5 - saturday, 6 - sunday).

    activate_traffic_lights (bool): Indicates whether traffic lights are activated.

    simulation_results (list): List of dictionaries containing simulation results.
    """

    def __init__(self, graph_name, time_limit: int, activate_traffic_lights = False, rain_intensity = 0,
                 start_time = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0,second=0), speeds_file_path = "simulation_speeds.json"):
        """
        Initialize the Simulation_manager.

        :Args:
        :param graph: The networkx graph representing the road network.
        :param time_limit :(int) The maximum time the simulation will run in seconds.
        :param activate_traffic_lights: Indicates whether traffic lights are activated. Default is False.
        :param start_time : (bool, optional) The starting datetime of the simulation. Default is June 29, 2023, 08:00:00.
        """
        # MANAGERS
        self.graph_name = graph_name
        self.road_network = Road_Network.Road_Network(graph_name, activate_traffic_lights, rain_intensity)
        self.car_manager = Car_manager.CarManager()

        # TIME
        self.simulation_datetime_start = start_time
        self.simulation_datetime = start_time
        self.simulation_time = datetime.timedelta(seconds=0)  # in seconds
        self.last_current_speed_update_time = start_time # for updating the current speed of the roads
        self.last_speed_dict_update_time = start_time # for updating the speed dict of the roads
        self.time_limit = time_limit  # the maximum time the simulation will run in seconds
        self.day_int = start_time.weekday() # 0-6, 0 - monday, 1 - tuesday, 2 - wednesday, 3 - thursday, 4 - friday, 5 - saturday, 6 - sunday

        # RESULTS
        self.simulation_results = []  # list of dictionaries, each dictionary is a simulation result
        self.simulation_update_times = []  # list of times the simulation was updated for the animation

        # DATA
        self.speeds_file_path = speeds_file_path
        # FUNCTIONS - read speeds
        self.read_road_speeds(self.simulation_datetime_start)

    # FUNCTIONS - block/unblock roads

    # def block_road(self, road_id):
    #     """
    #     Block a road in the road network.
    #
    #     Args:
    #     road_id (int): The ID of the road to be blocked.
    #
    #     Returns:
    #     None
    #     """
    #     self.road_network.block_road(road_id)
    #     print("Road", road_id, "blocked")
    #     return
    #
    # def unblock_road(self, road_id):
    #     """
    #     Unblock a previously blocked road.
    #
    #     Args:
    #     road_id (int): The ID of the road to be unblocked.
    #
    #     Returns:
    #     None
    #     """
    #     self.road_network.unblock_road(road_id)
    #     print("Road", road_id, "unblocked")
    #     return
    #
    # def unblock_all_roads(self):
    #     """
    #     Unblock all roads in the road network.
    #
    #     Returns:
    #     None
    #     """
    #     self.road_network.unblock_all_roads()
    #     print("All roads unblocked")
    #     return


    def update_simulation_clocks(self, time: int):
        """
        Update the simulation clocks.

        Args:
        time (int): The time interval to update the simulation clock in seconds.

        Returns:
        None
        """
        # update both the spesific simulation time and the datetime
        self.simulation_time += pd.Timedelta(seconds=time)  # time
        self.simulation_datetime += pd.Timedelta(seconds=time)  # time
        self.simulation_update_times.append(self.simulation_datetime)
        self.day_int = self.simulation_datetime.weekday()  # 0-6, 0 - monday, 1 - tuesday, 2 - wednesday, 3 - thursday, 4 - friday, 5 - saturday, 6 - sunday
        # time_difference = self.simulation_datetime - self.last_current_speed_update_time
        return

    def update_simulation_roads_speed_dict(self):
        """
        Check if a day is passed in the simulation and update the road speeds accordingly.

        Args:
        None

        Returns:
        None
        """
        last_update_day = self.last_speed_dict_update_time.weekday()
        if self.day_int != last_update_day:
            # update the road speeds according to the day
            # every day or at the next time a car will be updated (if more than a day passed)

            self.last_speed_dict_update_time = self.simulation_datetime.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
            self.read_road_speeds(self.simulation_datetime)
        return

    def update_simulation_roads_current_speeds(self):
        """

        Check if 10 minutes passed in the simulation and update the road speeds accordingly.

        Args:
        None

        Returns:
        None
        """
        time_difference = self.simulation_datetime - self.last_current_speed_update_time
        if (self.simulation_datetime.minute % 10 == 0 and self.simulation_datetime.minute - self.last_current_speed_update_time.minute > 0) or time_difference.seconds >= 600:
            # update the road speeds according to the time
            # every 10 minutes or at the next time a car will be updated (if more than 10 minutes passed)

            minutes = int(self.simulation_datetime.minute / 10) * 10
            self.last_current_speed_update_time = self.simulation_datetime.replace(minute=minutes).replace(second=0).replace(microsecond=0)

            time_key = self.simulation_datetime.replace(minute=minutes).strftime("%H:%M")
            self.road_network.update_roads_speeds(time_key) # updates the road speeds according to the current time

            print(self.simulation_datetime.strftime("%H:%M:%S"))
        return

    def read_road_speeds(self, datetime_obj: datetime.datetime):
        """
        Read road speeds from a JSON file and update the road network.
        The Json file supposed to be in the following format:
        {day_int: {time_key: {road_id: speed}}}
        The Json file is located at /Speeds_Data/{graph_name}_speeds.json

        Args:
        datetime_obj (datetime.datetime): The datetime for which road speeds are to be read.

        Returns:
        None
        """
        self.last_current_speed_update_time = datetime_obj.replace(second=0, microsecond=0)
        self.day_int = datetime_obj.weekday()
        self.speeds_file_path = get_simulation_speeds_file_path(self.road_network.graph, self.graph_name)
        with open(self.speeds_file_path, 'r') as infile:
            data = json.load(infile)

        # round the minutes to the nearest 10

        minutes = int(datetime_obj.minute / 10) * 10
        time_key = datetime_obj.replace(minute=minutes).strftime("%H:%M")
        day_data = data.get(str(self.day_int), {})
        self.road_network.set_roads_speeds_from_dict(day_data, time_key)
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
        # while the time limit is not reached and there are cars in the simulation or cars waiting to enter the simulation
        while int(self.simulation_time.total_seconds()) < self.time_limit and (self.car_manager.cars_in_simulation or self.car_manager.cars_waiting_to_enter):

            time = self.car_manager.calc_nearest_update_time(self.simulation_datetime)
            self.update_simulation_clocks(time)
            self.update_simulation_roads_speed_dict()
            self.update_simulation_roads_current_speeds()
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
            # save the important Graphs
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
