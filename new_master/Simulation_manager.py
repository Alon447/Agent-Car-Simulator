import copy
import datetime
import json
import os
import sys
import random

import osmnx as ox
import matplotlib.pyplot as plt
import Road_Network
import Car_manager
from new_master import Car
import pandas as pd
import matplotlib.patches as mpatches

from new_master.Car import time_delta_to_seconds
from new_master.Simulation_Results_Manager import Simulation_Results_Manager


class Simulation_manager:
    """
    This class manages the simulation.
    It will create the road network, the cars, the route algorithm and the q tables.
    It will also update the simulation and print the results.


    """
    def __init__(self, graph,time_limit, start_time = datetime.datetime(year=2023,month=6,day=29,hour=8, minute=0, second=0)): # TODO: data path

        # MANAGERS
        self.road_network = Road_Network.Road_Network(graph)
        self.car_manager = Car_manager.CarManager()

        # TIME
        self.simulation_datetime_start = start_time
        self.simulation_datetime = start_time
        self.simulation_time = datetime.timedelta(seconds=0) # in seconds
        self.last_speed_update_time = start_time
        self.time_limit= time_limit

        # RESULTS
        self.simulation_results = [] # list of dictionaries, each dictionary is a simulation result

    # FUNCTIONS - block/unblock roads
    def block_road(self, road_id):
        self.road_network.block_road(road_id)
        print("Road",road_id ,"blocked")
        return

    def unblock_road(self, road_id):
        self.road_network.unblock_road(road_id)
        print("Road",road_id ,"unblocked")
        return

    def unblock_all_roads(self):
        self.road_network.unblock_all_roads()
        print("All roads unblocked")
        return

    def get_road_network(self):
        return self.road_network

    def get_car_manager(self):
        return self.car_manager

    def update_simulation_clock(self, time):
        # update both the spesific simulation time and the datetime
        self.simulation_time += pd.Timedelta(seconds=time) #time
        self.simulation_datetime += pd.Timedelta(seconds=time) #  time
        time_difference = self.simulation_datetime - self.last_speed_update_time
        if time_difference.seconds>= 600: # 10 minutes
            # print("Speed updated at:", self.simulation_datetime.strftime("%H:%M:%S"))
            self.read_road_speeds(self.simulation_datetime)
        return

    def get_simulation_time(self):
        return int(self.simulation_time.total_seconds())

    def generate_random_speeds(self):
        self.road_network.generate_random_speeds()
        self.road_network.set_roads_speeds()

    def read_road_speeds(self, datetime_obj):
        """
        reads the road speeds from the json file and updates the road_network according to the time
        currently the time slice is every 10 minutes.
        :param datetime_obj:
        :return:
        """
        self.last_speed_update_time = datetime_obj.replace(second=0, microsecond=0)
        number_of_roads = len(self.road_network.roads_array)
        with open('simulation_speeds.json', 'r') as infile:
            data = json.load(infile)

        #time_key = datetime_obj.strftime("%H:%M")  # Format the datetime object as HH:MM

        # round the minutes to the nearest 10
        minutes = int(datetime_obj.minute / 10) * 10
        time_key = datetime_obj.replace(minute=minutes).strftime("%H:%M")

        # Get the number from the JSON data
        for road_number in range(number_of_roads):
            speed = data.get(str(road_number), {}).get(time_key)
            self.road_network.add_road_speed(road_number, speed)

        # now make sure every road has the right speed
        self.road_network.set_roads_speeds()
        return

    def set_up_simulation(self, cars):
        # set up simulation
        # resets the clocks
        # adds the cars to the car manager
        self.simulation_time = datetime.timedelta(seconds=0) # in seconds

        self.simulation_datetime = self.simulation_datetime_start
        self.car_manager.clear()
        for car in cars:
            self.car_manager.add_car(car)



    def start_simulation(self):
        """
        runs the simulation until there are no more cars in the simulation ot it gets to a time limit
        :return:
        """
        # rnd = random.randint(0, 1)
        # if rnd == 0:
        # self.road_network.block_road(542)

        while self.get_simulation_time() < self.time_limit and self.car_manager.get_cars_in_simulation():

            # rnd = random.randint(0, 100)
            # blocked_roads = self.road_network.get_blocked_roads_array()
            # if rnd == 0 and len(blocked_roads) !=0:
            #     self.road_network.unblock_all_roads()
            #     print("Roads unblocked")

            time = self.car_manager.get_nearest_update_time()
            SM.update_simulation_clock(time)
            #print("simulation_time:", SM.simulation_time)
            self.car_manager.update_cars(time)
            #self.car_manager.show_cars_in_simulation()

        for carInd in self.car_manager.get_cars_in_simulation():
            car = self.car_manager.get_cars_in_simulation()[carInd] # dict so we need to get the car object
            self.car_manager.cars_stuck.append(car)
        self.car_manager.force_cars_to_finish()

        return

    def end_simulation(self, simulation_number):
        # prints end message
        simulation_number+=1
        simulation_time_seconds = time_delta_to_seconds(self.simulation_time)
        if simulation_time_seconds>= 3600:
            if simulation_time_seconds%3600 == 0:
                print("simulation",simulation_number,"finished after", int(simulation_time_seconds/3600),"hours")
            else:
                print("simulation",simulation_number,"finished after", int(simulation_time_seconds/3600),"hours and ",int(simulation_time_seconds%60),"minutes")
        else:
            print("simulation",simulation_number,"finished after", int(simulation_time_seconds/60),"minutes")
        print("***************************")

        #print("Cars finished:")
        # for car in self.car_manager.get_cars_finished():
            #print(car.get_id(), car.get_total_travel_time())
        #print("***************************")
        #print("Cars stuck:")
        # for car in self.car_manager.get_cars_stuck():
        #     print(car.get_id(), car.get_total_travel_time())

    def run_full_simulation(self, cars, number_of_simulations=1):
        self.read_road_speeds(self.simulation_datetime_start)
        for i in range(number_of_simulations):
            copy_cars= []
            # make a deep copy of the cars list
            for car in cars:
                new_car = Car.Car(car.get_id(),
                                  car.get_source_node(),
                                  car.get_destination_node(),
                                  car.get_starting_time(),
                                  self.road_network,
                                    car.get_routing_algorithm())
                copy_cars.append(new_car)

            # block a random road

            # set up the simulation
            self.set_up_simulation(copy_cars)
            self.start_simulation()
            self.end_simulation(i)
            self.road_network.unblock_all_roads()
            simulation_results = {}
            for j, car in enumerate(copy_cars):
                car_reached_destination = self.car_manager.is_car_finished(car)
                car_time_taken = car.get_total_travel_time()
                car_starting_time = car.get_starting_time_end()
                car_ending_time = car.get_ending_time_end()
                car_route = car.get_past_nodes()
                car_key = car.get_id()
                day_of_week_str = self.simulation_datetime_start.strftime('%A')
                # save the important data
                simulation_results[car_key] = {
                    'reached_destination': car_reached_destination,
                    'routing_algorithm': car.get_routing_algorithm(),
                    'time_taken': car_time_taken, # in seconds
                    'day_of_week': day_of_week_str, # day of the week string
                    'start_time': car_starting_time, # datetime object string
                    'end_time': car_ending_time, # datetime object string
                    'route': car_route,
                    'roads_used': car.get_past_roads(),
                    'distance_travelled': int(car.get_distance_travelled()), # in meters, int
                }

            self.simulation_results.append({
                'simulation_number': i + 1,
                **simulation_results
            })
        return

    def print_simulation_results(self):
        """
        self.simulation_results =  all_simulations : [ simulation_1:{simulation_number, car_1_info:{..},car_2_info:{..} }, { {},{} }, { {},{} } ]
        list - every simulation
        outer dict - single simulation
        inner dict - number of simulation and cars
        :return:
        """
        for result in self.simulation_results:
            for array_index, result_dict in result.items():
                if array_index != "simulation_number":
                    print("*******************************************")
                    print("Simulation number: ", result['simulation_number'])

                    print(array_index, ": ")
                    for key, value in result_dict.items():
                        if key != "route" and key != "time_taken" and key != "distance_travelled":
                            print(key,": ", value)
                        elif key == "time_taken":
                            print(key, ": ", int(value/60), "minutes")
                        elif key == "distance_travelled":
                            print(key, ": ", round(value/1000,1), "km")
                        else:
                            print("Route length: ", len(value),"roads")

        return

    def get_simulation_route(self, carInd, simulation_number):
        """
        get the wanted route drom the wanted simulation
        :return:
        """
        return self.simulation_results[simulation_number][carInd]['route']


    def get_key_from_value(self, dictionary, value):
        for key, val in dictionary.items():
            if int(val) == value:
                return key
    def transform_node_id_route_to_osm_id_route(self, route):
        osm_route = []
        for node in route:
            osm_route.append(self.get_key_from_value(self.road_network.node_dict, node))
        return osm_route

    def car_times_bar_chart(self, car_number):
        """
        This function plots a bar chart of the times of a specific car in the simulation.

        Parameters:
        - car_number: The car number for which the chart will be plotted.
        """
        times = []
        colors = []

        for result in self.simulation_results:
            car_key = car_number
            times.append(result[car_key]['time_taken'])
            if result[car_key]['reached_destination']:
                colors.append('green')
            else:
                colors.append('red')
        # time_seconds = [td.total_seconds() for td in times]
        plt.bar((range(1, len(times)+1)), times, color=colors)

        # Add labels and title
        plt.xlabel('Simulation Number')
        plt.ylabel('Time taken [seconds] by Car {}'.format(car_number))
        plt.title('Bar Chart: Times of Car {} in Simulation'.format(car_number))
        legend_labels = ['Reached Destination', 'Not Reached Destination']
        legend_colors = ['green', 'red']
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in
                          zip(legend_colors, legend_labels)]

        plt.legend(handles=legend_patches, title='Legend', loc='upper right')

        plt.show()

    def plotting_custom_route(self,custom_route):
        """
        this is the way for a car that finished its route to plot it on the map at the end
        saves the function here for future use
        """
        # Define the custom route as a list of node IDs
        custom_route = self.transform_node_id_route_to_osm_id_route(custom_route)
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        graph = ox.load_graphml(data + '/graphTLVfix.graphml')

        # Plot the graph
        fig, ax = ox.plot_graph(graph, show=False, close=False, edge_color='lightgray', node_color='gray', bgcolor='black')

        # Plot the custom route
        ox.plot_graph_route(graph, custom_route, route_color='red', route_linewidth=6, ax=ax)

        # Show the plot
        plt.show()
        return

WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

# initilazires
START_TIME1 =datetime.datetime(year=2023,month=6,day=29,hour=7, minute=10, second=0)
START_TIME2 =datetime.datetime(year=2023,month=6,day=29,hour=19, minute=10, second=0)

SM = Simulation_manager('/graphTLVfix.graphml',2*HOUR,START_TIME1) # graph path, time limit, starting time
CM = SM.get_car_manager()
RN = SM.get_road_network()



NUMBER_OF_SIMULATIONS = 1
c1 = Car.Car(1,110,700,START_TIME1,RN,route_algorithm="random")
c2 = Car.Car(2,110,700,START_TIME1,RN,route_algorithm = "shortest_path")
cars = [c1,c2]

SM.run_full_simulation(cars,NUMBER_OF_SIMULATIONS)
print("***************************")


route1 = SM.get_simulation_route(1,0)
route2 = SM.get_simulation_route(2,0)

# SM.plotting_custom_route(route2)
SM.car_times_bar_chart(1)
SM.car_times_bar_chart(2)

SRM = Simulation_Results_Manager()
SRM.save_results_to_JSON(SM.simulation_results,1)
SM.simulation_results = SRM.read_results_from_JSON()
SM.print_simulation_results()











