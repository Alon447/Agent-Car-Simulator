import copy
import json
import os
import sys
import osmnx as ox
import matplotlib.pyplot as plt
import Road_Network
import Car_manager
from new_master import Car
import pandas as pd
import matplotlib.patches as mpatches




class Simulation_manager:
    """
    This class manages the simulation.
    It will create the road network, the cars, the route algorithm and the q tables.
    It will also update the simulation and print the results.


    """
    def __init__(self,graph): # TODO: data path
        self.road_network = Road_Network.Road_Network(graph)
        self.car_manager = Car_manager.CarManager()
        self.simulation_time = 0 # in seconds
        self.route_algorithm = None
        self.q_tables = {}
        self.map_graph = None
        self.simulation_results = [] # list of dictionaries, each dictionary is a simulation result


    def create_q_tables(self,starting_time_str,ending_tim_str,sample_time_str,day_of_week):
        """

        :param starting_time: starting hour+minute
        :param ending_time: ending hour+minute
        :param sample_time: time gap between each sample
        :param day_of_week:
        :return: skeletone of the q tables, to be filled by the agents

        """
        # cur_time_str = starting_time_str.split(":")
        # cur_time = int(cur_time_str[0])*60+int(cur_time_str[1])
        # ending_time = int(ending_tim_str.split(":")[0])*60+int(ending_tim_str.split(":")[1])
        # sample_time = int(sample_time_str.split(":")[0])*60+int(sample_time_str.split(":")[1])
        # time_slice_dict = create_time_slice_dict(self)
        # while cur_time<ending_time:
        #
        #
        # pass


    def load_q_tables(self,data_path):

        """
        Creates the q tables for the simulation.
        q table state consists of the following:
        - current road/the node at the end of the current road
        - destination node/road.
        - time and day of the week.

        :return:
        """
        q_tables = {}
        #q table formats:
        #q_table = {state: {action: value}}
        #state is a tuple of (current_road,destination_road), each day has its own q table for each time slice.
        #action is taking one of the possible next routes.
        directory = os.fsencode(data_path)

        for file in os.listdir(directory):
            self.add_time_slice_from_file(file,q_tables)#parse the file and add to the q tables

    def get_road_network(self):
        return self.road_network

    def get_car_manager(self):
        return self.car_manager

    def set_map(self):
        return

    def add_time_slice_from_file(self,file,q_tables):
        # TODO: implement
        #assuming the file name is in the following format:"hour:minute"
        #assuming that the file is a JSON file with the format of: {source_road:{target_road:{optional_road:time}}}
        time_str = file.name
        q_tables[time_str] = json.load(file)

        pass

    def create_time_slice_dict(self):
        q_slice_dict = {}

        return q_slice_dict

    def update_simulation_clock(self, time):
        self.simulation_time += time
        #self.car_manager.update_cars(time)
        return
    def get_simulation_time(self):
        return self.simulation_time

    def generate_random_speeds(self):
        self.road_network.generate_random_speeds()
        self.road_network.set_roads_speeds()
    def set_up_simulation(self, cars):
        # set up simulation
        self.simulation_time = 0
        self.car_manager.clear()
        for car in cars:
            self.car_manager.add_car(car)

    def start_simulation(self):
        #self.route_algorithm = input("Please choose a route algorithm: ")
        #map_graph_location = input("Please enter the location of the map graph: ")

        # start the simulation
        Time_limit = 7200
        while self.get_simulation_time() < Time_limit and self.car_manager.get_cars_in_simulation():
            time = self.car_manager.get_nearest_update_time()
            SM.update_simulation_clock(time)
            #print("simulation_time:", SM.simulation_time)
            self.car_manager.update_cars(time)
           # self.car_manager.show_cars_in_simulation()

        for carInd in self.car_manager.get_cars_in_simulation():
            car = self.car_manager.get_cars_in_simulation()[carInd] # dict so we need to get the car object
            self.car_manager.cars_stuck.append(car)


        return

    def end_simulation(self):
        print("***************************")
        print("simulation finished, after", round(self.simulation_time / 3600,2), "hours")
        # print("***************************")
        #print("Cars finished:")
        # for car in self.car_manager.get_cars_finished():
            #print(car.get_id(), car.get_total_travel_time())
        #print("***************************")
        #print("Cars stuck:")
        # for car in self.car_manager.get_cars_stuck():
        #     print(car.get_id(), car.get_total_travel_time())

    def run_full_simulation(self, cars, number_of_simulations=1):
        self.generate_random_speeds()
        #sys.setrecursionlimit(10000)  # default is 1000 in my installation

        for i in range(number_of_simulations):
            copy_cars= []
            # make a deep copy of the cars list
            for car in cars:
                new_car = Car.Car(car.get_id(),
                                  car.get_source_node(),
                                  car.get_destination_node(),
                                  car.get_starting_time(),
                                  self.road_network)
                copy_cars.append(new_car)

            self.set_up_simulation(copy_cars)
            self.start_simulation()
            self.end_simulation()
            """
            #this is where we will save the results of the simulation
            #we want it to be more generic so we can change the parameters of the simulation.
            
            car1_reached_destination = self.car_manager.is_car_finished(copy_cars[0])
            car1_time_taken = copy_cars[0].get_total_travel_time()
            car2_reached_destination = self.car_manager.is_car_finished(copy_cars[1])
            car2_time_taken = copy_cars[1].get_total_travel_time()
            self.simulation_results.append({
                'simulation_number': i + 1,
                'car1_reached_destination': car1_reached_destination,
                'car1_time_taken': car1_time_taken,
                'car1_route': copy_cars[0].get_past_nodes(),
                'car2_reached_destination': car2_reached_destination,
                'car2_time_taken': car2_time_taken,
                'car2_route': copy_cars[1].get_past_nodes()
            })
            """
            simulation_results = {}
            for j, car in enumerate(copy_cars):
                car_reached_destination = self.car_manager.is_car_finished(car)
                car_time_taken = car.get_total_travel_time()
                car_route = car.get_past_nodes()

                car_key = f'car{j + 1}'
                simulation_results[car_key] = {
                    'reached_destination': car_reached_destination,
                    'time_taken': car_time_taken,
                    'route': car_route
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
                        if key != "route":
                            print(key,": ", value)
                        else:
                            print("Route length: ", len(value),"roads")

        return

    def get_simulation_route(self):
        for d in self.simulation_results:
            if d == 'car1':
                print(d)
        return

    def get_key_from_value(self, dictionary, value):
        for key, val in dictionary.items():
            if int(val) == value:
                return key
    def transform_node_id_route_to_osm_id_route(self, route):
        osm_route = []
        for node in route:
            osm_route.append(self.get_key_from_value(self.road_network.node_dict, node))
        return osm_route

    def car_1_times_bar_chart(self):
        """
        This function plots a bar chart of the times of car 1 in the simulation.
        """
        times = []
        colors = []

        for result in self.simulation_results:
            times.append(result['car1_time_taken'])
            if result['car1_reached_destination']:
                colors.append('green')
            else:
                colors.append('red')

        plt.bar(range(len(times)), times, color=colors)

        # Add labels and title
        plt.xlabel('Simulation Number')
        plt.ylabel('Time taken by Car 1')
        plt.title('Bar Chart: Times of Car 1 in Simulation')
        legend_labels = ['Reached Destination', 'Not Reached Destination']
        legend_colors = ['green', 'red']
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in
                          zip(legend_colors, legend_labels)]

        # a legend that says green- reached destination, red- not reached
        # plt.legend(legend_labels, title='Legend', loc='upper right')
        plt.legend(handles=legend_patches, title='Legend', loc='lower right')

        plt.show()
        return

    def plotting_custom_route(self,custom_route):
        """
        this is the way for a car that finished its route to plot it on the map at the end
        saves the function here for future use
        """
        # Define the custom route as a list of node IDs
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



# initilazires
SM = Simulation_manager('/graphTLVfix.graphml')
CM = SM.get_car_manager()
RN = SM.get_road_network()


# roads = (RN.get_roads_array())
# for road in roads:
#     print(road)
NUMBER_OF_SIMULATIONS = 3
c1 = Car.Car(1,1,5,0,RN)
c2 = Car.Car(2,2,10,0,RN)
cars = [c1,c2]

SM.run_full_simulation(cars,NUMBER_OF_SIMULATIONS)
print("***************************")

print("simulation results:")
SM.print_simulation_results()
print("***************************")

#route = SM.get_simulation_route()
#print(SM.get_road_network().node_dict)
# print(route[0])
# route1 = SM.transform_node_id_route_to_osm_id_route(route[0])
# SM.plotting_custom_route(route1)
# print(route[1])
# route2 = SM.transform_node_id_route_to_osm_id_route(route[1])
# SM.plotting_custom_route(route2)
# SM.car_1_times_bar_chart()




