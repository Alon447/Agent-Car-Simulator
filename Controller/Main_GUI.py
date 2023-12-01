import datetime
import json
import statistics
import time
import traceback

import GUI.Animate_Past_Simulation as APS
import GUI.Animate_Simulation as AS
from GUI.Display_Comparisons_Results_Window import Display_Comparisons_Results_Window
from GUI.Main_Window import Main_Window
from GUI.Load_Simulation_Window import New_Load_Simulation_Window
from GUI.Settings_Window import Settings_Window
from GUI.New_Simulation_Window import New_Simulation_Window
from GUI.Routings_Comparisons_Window import Routing_Comparisons_Window
from Main_Files import Car, Simulation_manager, Road_Network
from Utilities.Getters import *
from Utilities.Results import save_results_to_JSON, plot_simulation_overview, get_simulation_times, get_results_files


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

        # graph parameters
        self.G = None  # graph
        self.G_name = None  # graph name
        self.graph_loaded = False

        # Simulation parameters
        self.traffic_lights = None
        self.rain_intensity = 0
        self.add_traffic_white_noise = False
        self.max_time_for_car = datetime.timedelta(hours=2)

        # q learning parameters
        self.episodes = 2000
        self.steps_per_episode = 200
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.2

        self.simulation_duration = None
        self.simulation_starting_time = None

        # animation parameters
        self.simulation_speed = simulation_speed
        self.repeat = repeat
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
        self.run_time_data = {}

    # view control - load windows according to user's choice
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
    def load_settings_window(self):
        self.view = Settings_Window(self)
        self.view.main()

    # def load_about_window(self):
    #     self.view = New_About_Window(self)
    #     self.view.main()

    def start_display_comparisons_results_window(self):
        self.view = Display_Comparisons_Results_Window(self)
        self.view.main()

    # controller control
    def start_simulation(self, traffic_lights, rain_intensity, add_traffic_white_noise,
                         plot_results, simulation_speed=5, repeat=True):

        simulation_starting_time = self.calculate_starting_time()
        self.set_simulation_manager(traffic_lights, rain_intensity, add_traffic_white_noise,
                                    plot_results, simulation_starting_time)
        self.set_cars()

        self.model.run_full_simulation(self.cars, num_episodes=self.episodes,
                                       max_steps_per_episode=self.steps_per_episode,
                                       learning_rate = self.learning_rate,
                                       discount_factor = self.discount_factor,
                                       epsilon = self.epsilon)
        ASS = AS.Animate_Simulation(animation_speed=simulation_speed, repeat=repeat)
        routes = self.model.get_simulation_routes(self.cars, 0)
        json_name = save_results_to_JSON(self.model.graph_name, self.model.simulation_results)
        plot_simulation_overview(json_name)
        ASS.plot_simulation(self.model, routes, self.cars)

    def load_simulation(self, simulation_name, simulation_speed=5, repeat=True):
        ASS = APS.Animate_Past_Simulation(animation_speed=simulation_speed, repeat=repeat)
        ASS.plot_simulation(simulation_name)

    # gather settings
    def set_cars(self):
        self.cars = []
        for car_id in self.cars_values_dict:
            car = self.cars_values_dict[car_id]
            self.add_car(car[0], car[1], car[2], car[3], self.road_network, car[4], car[5])
        return

    def set_simulation_manager(self, traffic_lights, rain_intensity, add_traffic_white_noise,
                               plot_results, simulation_starting_time):
        self.model = Simulation_manager.Simulation_manager(graph_name=self.G_name,
                                                           activate_traffic_lights=traffic_lights,
                                                           rain_intensity=rain_intensity,
                                                           traffic_white_noise=add_traffic_white_noise,
                                                           is_plot_results=plot_results,
                                                           max_time_for_car=self.max_time_for_car,
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

        new_car = Car.Car(car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table)
        self.cars.append(new_car)

    def get_cars_values_dict(self):
        return self.cars_values_dict

    def get_past_simulations(self):
        directory_path = get_results_directory_path()
        json_files = [file for file in os.listdir(directory_path)]
        return json_files, directory_path

    def get_blocked_roads_dict(self):
        return self.blocked_roads_dict

    def load_city_map(self, city_map):
        try:
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
        elif len(self.cars_values_dict) == 0:
            print("No cars to run simulation with")
            return False
        return True

    def get_xy_from_node_id(self, node_id):
        return self.road_network.get_xy_from_node_id(node_id)

    ##################################################################
    #   controller for the multiple runs for routing comparisons     #
    ##################################################################

    def prepare_routing_comparisons(self):
        self.model = Simulation_manager.Simulation_manager(graph_name=self.G_name,
                                                           activate_traffic_lights=self.traffic_lights,
                                                           rain_intensity=self.rain_intensity,
                                                           traffic_white_noise=self.add_traffic_white_noise,
                                                           is_plot_results=self.plot_results,
                                                           start_time=self.simulation_starting_time)
        self.road_network = self.model.road_network
        self.run_route_comparisons()

    def run_route_comparisons(self):
        run_time_data = {}
        for i in range(self.num_of_runs):
            print("run number: ", i)
            run_time_data[i] = {}
            cur_cars = self.generate_random_cars(0, self.road_network)
            for j in range(len(self.algorithms)):
                cur_cars = self.set_cars_algorithm(j, cur_cars)
                cur_alg_start_time = time.time()
                learning_time = self.model.run_full_simulation(cur_cars, num_episodes=self.episodes,
                                                               max_steps_per_episode=self.steps_per_episode,
                                                               simulation_number_added=i,
                                                               learning_rate=self.learning_rate,
                                                               discount_factor=self.discount_factor,
                                                               epsilon=self.epsilon)
                cur_alg_end_time = time.time()
                run_time_data[i][self.algorithms[j]] = cur_alg_end_time - cur_alg_start_time - learning_time
                if self.algorithms[j] in routing_learning_algorithms:
                    run_time_data[i][self.algorithms[j] + " learning_time"] = learning_time
        save_results_to_JSON(self.model.graph_name, self.model.simulation_results)
        json.dump(run_time_data, open(f'../{Route_comparisons_results_directory}/{self.model.graph_name + "_" + run_time_data_file_name}', 'w'),
                  indent=4)
        organized_times = self.organize_simulation_times(get_simulation_times(self.model))
        json.dump(organized_times, open(f'../{Route_comparisons_results_directory}/{self.model.graph_name + "_" + cars_times_file_name}', 'w'),
                  indent=4)

    def set_multiple_runs_parameters(self, num_of_cars, num_of_runs, algorithms, src_list, dst_list, rain_intesity,
                                     traffic_light, add_trafic_white_noise, use_existing_q_tables,
                                     earliest_time, latest_time):
        self.num_of_cars = num_of_cars
        self.num_of_runs = num_of_runs
        self.algorithms = algorithms
        self.src_list = src_list
        self.dst_list = dst_list
        self.rain_intensity = rain_intesity
        self.traffic_lights = traffic_light
        self.add_traffic_white_noise = add_trafic_white_noise
        self.use_existing_q_tables = use_existing_q_tables
        self.simulation_starting_time = earliest_time
        self.simulation_ending_time = latest_time

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
            src, dst = self.choose_random_src_dst()
            while not self.check_if_path_is_exist(src, dst, RN) or src == dst:
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
                organized_times[i][self.algorithms[k]] = []
                for j in range(0, self.num_of_cars):
                    # the times are organized in the following way:
                    # every self.num_of_cars times are for the same simulation number and same algorithm.
                    # so the first car of the i-th simulation and k-th algorithm is in index i*k
                    current_time = times[i * len(self.algorithms) * self.num_of_cars + k * self.num_of_cars + j]
                    organized_times[i][self.algorithms[k]].append(current_time)
        return organized_times

    def set_cars_algorithm(self, algorithm_ind, cars):
        for car in cars:
            car.set_new_routing_algorithm(self.algorithms[algorithm_ind])
        return cars

    def confirm_settings(self, **kwargs):

        def check_if_input_correct(input):
            # check if the input is between 0 and 1
            if input < 0:
                input = 0
            elif input > 1:
                input = 1
            return input

        for key, value in kwargs.items():
            if key == "episodes":
                self.episodes = int(value)
                print("episodes: ", self.episodes)
            elif key == "steps":
                self.steps_per_episode = int(value)
                print("steps: ", self.steps_per_episode)
            elif key == "car_duration":
                self.max_time_for_car = datetime.timedelta(hours=float(value))
                print("car_duration: ", self.max_time_for_car)
            elif key == "learning_rate":
                self.learning_rate = check_if_input_correct(float(value))
                print("learning_rate: ", self.learning_rate)
            elif key == "discount_factor":
                self.discount_factor = check_if_input_correct(float(value))
                print("discount_factor: ", self.discount_factor)
            elif key == "epsilon":
                self.epsilon = check_if_input_correct(float(value))
                print("epsilon: ", self.epsilon)
            else:
                print("Error in confirm_settings")

    def get_run_times_and_cars_times_files(self):
        return get_results_files(cars_times_file_name, run_time_data_file_name)

    def calculate_car_times_statistics(self, car_times_file):
        with open(f'../{Route_comparisons_results_directory}/{car_times_file}') as json_file:
            data = json.load(json_file)
        algorithms = list(data['0'].keys())
        algorithm_drive_times = {}
        for algorithm in algorithms:
            algorithm_drive_times[algorithm] = []
        for run in data:
            for algorithm in data[run]:
                algorithm_drive_times[algorithm].extend(data[run][algorithm])
        algorithm_statistics = {}
        for algorithm in algorithms:
            algorithm_statistics[algorithm] = {}
            algorithm_statistics[algorithm][Average_key] = sum(algorithm_drive_times[algorithm]) / len(
                algorithm_drive_times[algorithm])
            algorithm_statistics[algorithm][Standard_deviation_key] = statistics.stdev(algorithm_drive_times[algorithm])
        return algorithm_statistics

    def calculate_run_times_statistics(self, run_times_file):
        with open(f'../{Route_comparisons_results_directory}/{run_times_file}') as json_file:
            data = json.load(json_file)
        algorithms = list(data['0'].keys())
        algorithm_run_times = {}
        for algorithm in algorithms:
            algorithm_run_times[algorithm] = []
        for run in data:
            for algorithm in data[run]:
                algorithm_run_times[algorithm].append(data[run][algorithm])
        algorithm_statistics = {}
        for algorithm in algorithms:
            algorithm_statistics[algorithm] = {}
            algorithm_statistics[algorithm][Average_key] = sum(algorithm_run_times[algorithm]) / len(
                algorithm_run_times[algorithm])
            algorithm_statistics[algorithm][Standard_deviation_key] = statistics.stdev(algorithm_run_times[algorithm])
        return algorithm_statistics


if __name__ == "__main__":
    controller = Controller()
    controller.start_main_window()
