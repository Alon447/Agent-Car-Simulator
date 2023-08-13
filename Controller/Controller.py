from GUI.Main_Window import Main_Window
from GUI.New_Simulation_Window import New_Simulation_Window
import GUI.Animate_Simulation as AS
from Main_Files import Car, Simulation_manager, Road_Network
import datetime
from Utilities import Getters


class Controller:

    def __init__(self, simulation_speed=30, repeat=False):
        # TODO: remove default values after testing
        self.graph_loaded = False
        self.G = None
        self.G_path = None
        self.view = None
        self.model = None
        self.simulation_speed = simulation_speed
        self.repeat = repeat

    # view control
    def start_main(self):
        self.view = Main_Window(self)
        self.view.main()

    def start_new_simulation(self):
        # animation,fig = self.get_canvas_test()
        # self.view = New_Simulation_Window(self,animation,fig)
        # self.view.add_canvas(canvas,animation,fig,ax)
        self.view = New_Simulation_Window(self)
        self.view.main()

    # model control

    # gather settings
    def add_car(self):
        pass

    def load_city_map(self, city_map):
        try:
            self.G, self.G_path = Getters.get_graph(city_map)
            self.graph_loaded = True
            return True
        except:
            self.graph_loaded = False
            print("Error loading graph")
            return False


    def get_graph(self):
        if self.graph_loaded:
            return self.G, self.G_path
        else:
            return None, None

    # get resources
    def get_canvas_test(self):
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


if __name__ == "__main__":
    controller = Controller()
    controller.start_main()
