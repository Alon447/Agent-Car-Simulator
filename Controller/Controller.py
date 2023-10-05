import traceback

from GUI.Main_Window import Main_Window
from GUI.New_Simulation_Window import New_Simulation_Window
import GUI.Animate_Simulation as AS
from Main_Files import Car, Simulation_manager, Road_Network
from Utilities.Results import save_results_to_JSON,plot_past_result
import datetime
from Utilities import Getters


# TODO-s:
#  - document the code
#  - add functionality of showing the cars animation for chosen run when done running the simulations -
#  - add option for custom speeds generating (choose algorithm) and load custom speeds from file (optional?) - add
#  - functionality of blocking roads with interactive map (principle similar to choosing src and dst) (i think we
#    should have it)
#  - maybe polish the user interface a bit more (add some more options, maybe add some more windows, idk)
#

class Controller:

    def __init__(self, simulation_speed=30, repeat=False):
        # TODO: remove default values after testing (if needed)
        #  also add number of simulations to run
        self.traffic_lights = None
        self.rain_intensity = None
        self.graph_loaded = False
        self.G = None
        self.G_name = None
        self.view = None
        self.model = None
        self.road_network = None

        # Simulation parameters
        self.simulation_speed = simulation_speed
        self.repeat = repeat
        self.cars_values_dict = {}
        self.cars = []
        self.simulation_duration = None
        self.add_traffic_white_noise = False
        self.simulation_starting_time = None
        self.plot_results = False
        self.blocked_roads = []
        self.planned_blockages = []
        # helper variables

    # view control
    def start_main_window(self):
        self.view = Main_Window(self)
        self.view.main()

    def start_new_simulation_window(self):
        self.view = New_Simulation_Window(self)
        self.view.main()

    # model control

    def start_simulation(self, simulation_duration, traffic_lights, rain_intensity, add_traffic_white_noise,
                         plot_results, num_episodes=2000, max_steps_per_episode=100,simulation_speed=5, repeat=True):
        # TODO: insert the cars to the simulation, also option to show statistics
        #  also add option to load existing simulation
        simulation_starting_time = self.calculate_starting_time()
        self.set_simulation_manager(simulation_duration, traffic_lights, rain_intensity, add_traffic_white_noise,
                                    plot_results, simulation_starting_time)
        self.set_cars()
        self.model.run_full_simulation(self.cars, num_episodes=num_episodes, max_steps_per_episode=max_steps_per_episode)
        ASS = AS.Animate_Simulation(animation_speed=simulation_speed, repeat=repeat)
        routes = self.model.get_simulation_routes(self.cars, 0)
        json_name = save_results_to_JSON(self.model.graph_name, self.model.simulation_results)
        plot_past_result(json_name, self.model)
        ASS.plotting_custom_route(self.model, routes, self.cars)
    # gather settings

    def set_cars(self):
        self.cars = []
        for car_id in self.cars_values_dict:
            car = self.cars_values_dict[car_id]
            self.add_car(car[0], car[1], car[2], car[3],self.road_network, car[4], car[5])
        pass

    def set_simulation_manager(self, simulation_duration, traffic_lights, rain_intensity, add_traffic_white_noise,
                               plot_results, simulation_starting_time):
        # TODO: add checks for values (check if they exist and are valid)
        SM = Simulation_manager.Simulation_manager(graph_name=self.G_name, time_limit=simulation_duration,
                                                   activate_traffic_lights=traffic_lights,
                                                   rain_intensity=rain_intensity,
                                                   traffic_white_noise=add_traffic_white_noise,
                                                   is_plot_results=plot_results, start_time=simulation_starting_time)
        self.model = SM

    # def add_car_values(self, temp_src_id, temp_dst_id, start_time, routing_alg, use_existing_q_table):
    #     self.cars_values.append([int(temp_src_id), int(temp_dst_id), start_time, routing_alg, use_existing_q_table])

    def add_car_values(self, car_values, car_id):
        self.cars_values_dict[car_id] = car_values

    def remove_car_values(self, car_id):
        self.cars_values_dict.pop(car_id)
        pass

    def add_car(self, car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table):
        # TODO: make sure that we have all of the parameters for the car
        # start_node = self.model.get_fixed_node_id(temp_src_id)
        # end_node = self.model.get_fixed_node_id(temp_dst_id)
        new_car = Car.Car(car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table)
        self.cars.append(new_car)

    def get_cars_values_dict(self):
        return self.cars_values_dict

    def load_city_map(self, city_map):
        try:
            # self.G, self.G_name = Getters.get_graph(city_map)
            self.graph_loaded = True
            self.road_network = Road_Network.Road_Network(city_map)
            self.G = self.road_network.graph
            self.G_name = self.road_network.graph_name
            self.cars_values_dict = {}

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

    def get_fixed_node_id(self, node_id):
        return self.road_network.get_node_from_osm_id(node_id)

    def calculate_starting_time(self):
        cur_time = self.cars_values_dict[next(iter(self.cars_values_dict))][3]
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


if __name__ == "__main__":
    controller = Controller()
    controller.start_main_window()
