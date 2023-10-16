import os
import random
import time
import traceback

from GUI.Main_Window import Main_Window
from GUI.New_Load_Simulation_Window import New_Load_Simulation_Window
from GUI.New_Simulation_Window import New_Simulation_Window
import GUI.Animate_Simulation as AS
from GUI.Routings_Comparisons_Window import Routing_Comparisons_Window
import GUI.Animate_Past_Simulation as APS
from Main_Files import Car, Simulation_manager, Road_Network
from Utilities.Results import save_results_to_JSON, plot_simulation_overview
import datetime
from Utilities import Getters


class Controller:
    """
    This is the main class of the project, it runs the GUI and the simulation
    This class is used to control the simulation and connect between it and the GUI
    """

    def __init__(self, simulation_speed=30, repeat=False):

        # GUI and Simulation managers
        self.view = None
        self.model = None  # simulation manager
        self.road_network = None  # the simulation's road network

        # Simulation parameters
        self.G = None  # graph
        self.G_name = None  # graph name
        self.traffic_lights = None
        self.rain_intensity = 0
        self.add_traffic_white_noise = False
        self.graph_loaded = False
        self.simulation_speed = simulation_speed
        self.repeat = repeat
        self.simulation_duration = None
        self.simulation_starting_time = None
        self.plot_results = False

        # Insert Car parameters
        self.cars = []
        self.cars_values_dict = {}

        # Insert Block Road parameters
        self.blocked_roads_array = []
        self.blocked_roads_dict = {}  # key: road id, value: list of blocked times

        # multiple runs parameters
        self.simulation_ending_time = None
        self.src_list = []
        self.dst_list = []
        self.num_of_runs = 0
        self.num_of_cars = 0
        self.algorithms = []
        self.use_existing_q_tables = False

    # view control
    def start_main_window(self):
        self.view = Main_Window(self)
        self.view.main()

    def start_new_simulation_window(self):
        self.view = New_Simulation_Window(self)
        self.view.main()

    def load_simulation_window(self):
        self.view = New_Load_Simulation_Window(self)
        self.view.main()

    def start_routing_comparisons_window(self):
        self.view = Routing_Comparisons_Window(self)
        self.view.main()

    # model control
    def start_simulation(self, traffic_lights, rain_intensity, add_traffic_white_noise,
                         plot_results, num_episodes=2000, max_steps_per_episode=100, simulation_speed=5, repeat=True):

        simulation_starting_time = self.calculate_starting_time()
        self.set_simulation_manager(traffic_lights, rain_intensity, add_traffic_white_noise,
                                    plot_results, simulation_starting_time)
        self.set_cars()
        self.model.run_full_simulation(self.cars, num_episodes=num_episodes,
                                       max_steps_per_episode=max_steps_per_episode)
        ASS = AS.Animate_Simulation(animation_speed=simulation_speed, repeat=repeat)
        routes = self.model.get_simulation_routes(self.cars, 0)
        json_name = save_results_to_JSON(self.model.graph_name, self.model.simulation_results)
        plot_simulation_overview(json_name)
        ASS.plotting_custom_route(self.model, routes, self.cars)

    def load_simulation(self, simulation_name, simulation_speed=5, repeat=True):
        ASS = APS.Animate_Past_Simulation(animation_speed=simulation_speed, repeat=repeat)
        ASS.plotting_custom_route(simulation_name)

    # gather settings
    def set_cars(self):
        self.cars = []
        for car_id in self.cars_values_dict:
            car = self.cars_values_dict[car_id]
            self.add_car(car[0], car[1], car[2], car[3], self.road_network, car[4], car[5])
        return

    def set_simulation_manager(self, traffic_lights, rain_intensity, add_traffic_white_noise,
                               plot_results, simulation_starting_time):
        # TODO: add checks for values (check if they exist and are valid)
        self.model = Simulation_manager.Simulation_manager(graph_name=self.G_name,
                                                           activate_traffic_lights=traffic_lights,
                                                           rain_intensity=rain_intensity,
                                                           traffic_white_noise=add_traffic_white_noise,
                                                           is_plot_results=plot_results,
                                                           start_time=simulation_starting_time)
        self.road_network = self.model.road_network
        for road_id in self.blocked_roads_array:
            self.model.update_road_blockage(road_id, self.blocked_roads_dict[road_id][3],
                                            self.blocked_roads_dict[road_id][4])

    def add_car_values(self, car_values, car_id):
        self.cars_values_dict[car_id] = car_values

    def add_blockage_values(self, blockage_values, blockage_id, start_time, end_time):
        self.blocked_roads_dict[blockage_id] = blockage_values
        self.blocked_roads_array.append(blockage_id)

    def remove_car_values(self, car_id):
        self.cars_values_dict.pop(car_id)
        return

    def remove_blockage_values(self, blockage_id):
        self.blocked_roads_dict.pop(blockage_id)
        self.blocked_roads_array.remove(blockage_id)
        return

    def add_car(self, car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table):
        # TODO: make sure that we have all of the parameters for the car

        new_car = Car.Car(car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table)
        self.cars.append(new_car)

    def get_cars_values_dict(self):
        return self.cars_values_dict

    def get_past_simulations(self):
        directory_path = Getters.get_results_directory_path()
        json_files = [file for file in os.listdir(directory_path)]
        return json_files, directory_path

    def get_blocked_roads_dict(self):
        return self.blocked_roads_dict

    def load_city_map(self, city_map):
        try:
            # self.G, self.G_name = Getters.get_graph(city_map)
            self.graph_loaded = True
            self.road_network = Road_Network.Road_Network(city_map)
            self.G = self.road_network.graph
            self.G_name = self.road_network.graph_name
            self.cars_values_dict = {}
            self.blocked_roads_array = []
            self.blocked_roads_dict = {}
            return True

        except Exception as e:
            self.graph_loaded = False
            print("Error loading graph")
            print(e)
            traceback.print_exc()
            return False

    def get_graph(self):
        if self.graph_loaded:
            return self.G, self.G_name
        else:
            return None, None

    def unblock_road(self, road_id):
        self.blocked_roads.remove(road_id)

    def unblock_all_roads(self):
        self.blocked_roads = []

    # get resources
    def get_fixed_node_id(self, osm_id):
        return self.road_network.get_node_from_osm_id(osm_id)

    def get_fixed_road_id(self, src_osm_id, dst_osm_id):
        src_node_id = self.get_fixed_node_id(src_osm_id)
        dst_node_id = self.get_fixed_node_id(dst_osm_id)
        return self.road_network.get_road_from_src_dst(src_node_id, dst_node_id).id

    def calculate_starting_time(self):
        cur_time = self.cars_values_dict[next(iter(self.cars_values_dict))][3]  # car's starting datetime
        for car in self.cars_values_dict:
            cur_time = min(cur_time, self.cars_values_dict[car][3])
        return cur_time

    def check_can_run_simulation(self):
        if not self.graph_loaded:
            return False
        # elif self.simulation_duration is None:
        #     return False
        # elif self.simulation_starting_time is None:
        #     return False
        elif len(self.cars_values_dict) == 0:
            print("No cars to run simulation with")
            return False
        return True

    ##########################################
    #   controller for the multiple runs     #
    ##########################################

    def run_multiple_simulations(self):
        self.model = Simulation_manager.Simulation_manager(graph_name=self.G_name,
                                                           activate_traffic_lights=self.traffic_lights,
                                                           rain_intensity=self.rain_intensity,
                                                           traffic_white_noise=self.add_traffic_white_noise,
                                                           is_plot_results=self.plot_results,
                                                           start_time=self.simulation_starting_time)
        self.road_network = self.model.road_network
        run_time_data = {}
        for i in range(self.num_of_runs):
            run_time_data[i] = {}
            for j in range(len(self.algorithms)):
                cur_cars = self.generate_random_cars(j, self.road_network)
                cur_alg_start_time = time.time()
        pass

    def set_multiple_runs_parameters(self, num_of_cars, num_of_runs, algorithms, src_list, dst_list, rain_intesity,
                                     traffic_light, add_trafic_white_noise, use_existing_q_tables, num_episodes, max_steps_per_episode,
                                     earliest_time, latest_time):
        pass

    def choose_random_src_dst(self):
        src = random.choice(self.src_list)
        dst = random.choice(self.dst_list)
        return src, dst

    def check_if_path_is_exist(self, src, dst, RN):
        try:
            path = RN.get_shortest_path(src, dst)
            return True
        except:
            return False

    def generate_random_starting_time(self):
        time_difference_seconds = (self.simulation_ending_time - self.simulation_starting_time).total_seconds()
        random_seconds = random.randint(0, time_difference_seconds)
        random_timedelta = datetime.timedelta(seconds=random_seconds)
        return self.simulation_starting_time + random_timedelta

    def generate_random_cars(self, algorithm_ind, RN):
        # cars are in the same road network, same day, different starting times, different src and dst
        cars = []
        for i in range(self.num_of_cars):

            # time_delta = create_time_delta(day)
            src, dst = self.choose_random_src_dst()
            while not self.check_if_path_is_exist(src, dst, RN) or src==dst:
                src, dst = self.choose_random_src_dst()
            cur_starting_time = self.generate_random_starting_time()
            cars.append(Car.Car(i, src, dst, cur_starting_time, RN, route_algorithm=self.algorithms[algorithm_ind],
                                use_existing_q_table=self.use_existing_q_tables))
        return cars

    def organize_simulation_times(self, times):
        organized_times = {}  # key = simulation index, value = dictionary of times of cars in the simulation grouped
        # by algorithm
        # every even index is the shortest path, every odd index is q learning
        for i in range(0, self.num_of_runs):
            organized_times[i] = {}
            for k in range(0, len(self.algorithms)):
                for j in range(0, self.num_of_cars):
                    # the times are organized in the following way:
                    # every self.num_of_cars times are for the same simulation number and same algorithm.
                    # so the first car of the i-th simulation and k-th algorithm is in index i*k
                    organized_times[i][self.algorithms[k]].append(times[i * k + j])
        return organized_times


if __name__ == "__main__":
    controller = Controller()
    controller.start_main_window()
