import traceback

from GUI.Main_Window import Main_Window
from GUI.New_Simulation_Window import New_Simulation_Window
import GUI.Animate_Simulation as AS
from Main_Files import Car, Simulation_manager, Road_Network
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
        self.temporary_road_network = None

        # Simulation parameters
        self.simulation_speed = simulation_speed
        self.repeat = repeat
        self.cars_init = []
        self.cars = []
        self.simulation_duration = None
        self.add_traffic_white_noise = False
        self.simulation_starting_time = None

        # helper variables

    # view control
    def start_main_window(self):
        self.view = Main_Window(self)
        self.view.main()

    def start_new_simulation_window(self):
        self.view = New_Simulation_Window(self)
        self.view.main()

    # model control

    def start_simulation(self):
        # TODO: insert the cars to the simulation, also option to show statistics
        #  also add option to load existing simulation
        pass

    # gather settings

    def set_simulation_manager(self):
        # TODO: add checks for values (check if they exist and are valid)
        SM = Simulation_manager.Simulation_manager(self.G_name, self.simulation_duration, self.traffic_lights,
                                                   self.rain_intensity,
                                                   self.add_traffic_white_noise, self.simulation_starting_time)
        self.model = SM

    def add_car_init(self, temp_src_id, temp_dst_id, start_time, routing_alg, use_existing_q_table):
        self.cars_init.append([int(temp_src_id), int(temp_dst_id), start_time, routing_alg, use_existing_q_table])

    def remove_car_init(self):
        #TODO: add feature to remove car from the list
        pass
    def add_car(self, car_id, temp_src_id, temp_dst_id, start_time, speed, routing_alg, use_existing_q_table):
        # TODO: make sure that we have all of the parameters for the car
        start_node = self.model.get_fixed_node_id(temp_src_id)
        end_node = self.model.get_fixed_node_id(temp_dst_id)
        new_car = Car.Car(car_id, start_node, end_node, start_time, speed, routing_alg, use_existing_q_table)
        self.cars.append(new_car)

    def load_city_map(self, city_map):
        try:
            # self.G, self.G_name = Getters.get_graph(city_map)
            self.graph_loaded = True
            self.temporary_road_network = Road_Network.Road_Network(city_map)
            self.G = self.temporary_road_network.graph
            self.G_name = self.temporary_road_network.graph_name
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

    # get resources
    def get_canvas_test(self):  # TODO: remove after testing
        START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
        START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=9, minute=0, second=0)
        START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=13, minute=0, second=0)
        START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
        START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)

        # Constants for time intervals
        WEEK = 604800
        DAY = 86400
        HOUR = 3600
        MINUTE = 60

        # Simulation parameters
        NUMBER_OF_SIMULATIONS = 1
        TRAFFIC_LIGHTS = True
        ADD_TRAFFIC_WHITE_NOISE = False
        Rain_intensity = 0  # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)

        # Q-Learning parameters
        USE_ALREADY_GENERATED_Q_TABLE = True
        NUM_EPISODES = 2500

        # Animation parameters
        ANIMATE_SIMULATION = True
        REPEAT = True
        SIMULATION_SPEED = 30  # X30 faster than one second interval

        # Initialize Simulation Manager
        SM = Simulation_manager.Simulation_manager('TLV', 7 * DAY, TRAFFIC_LIGHTS, Rain_intensity,
                                                   ADD_TRAFFIC_WHITE_NOISE, START_TIME1)
        CM = SM.car_manager
        RN = SM.road_network

        # Block roads
        # RN.block_road(534)
        # SM.update_road_blockage(168, START_TIME1)
        # SM.update_road_blockage(181)
        # SM.update_road_blockage(182)
        # SM.update_road_blockage(912)
        # SM.update_road_blockage(382)

        # Initialize cars
        cars = []
        cars.append(Car.Car(1, 5, 745, START_TIME1, RN, route_algorithm="sp",
                            use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
        cars.append(Car.Car(2, 5, 745, START_TIME1, RN, route_algorithm="sp",
                            use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
        cars.append(Car.Car(3, 5, 745, START_TIME1, RN, route_algorithm="sp",
                            use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
        # cars.append(Car.Car(2, 5, 745, START_TIME2, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
        # cars.append(Car.Car(4, 1, 344, START_TIME3, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
        # cars.append(Car.Car(3, 39, 507, START_TIME5, RN, route_algorithm="sp"))

        # Run simulations
        SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS)
        routes = SM.get_simulation_routes(cars, 0)
        ASS = AS.Animate_Simulation(animation_speed=self.simulation_speed, repeat=self.repeat)
        ASS.plotting_custom_route(SM, routes, cars)
        return ASS.prepare_animation()

    def get_node_id_from_osm_id(self,osm_id):
        return self.temporary_road_network.get_node_from_osm_id(int(osm_id))


if __name__ == "__main__":
    controller = Controller()
    controller.start_main_window()
