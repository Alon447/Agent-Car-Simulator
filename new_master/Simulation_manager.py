import Road_Network
import Route
import Car_manager


class Simulation_manager:
    """


    """

    def __init__(self):
        self.road_network = Road_Network.RoadNetwork()
        self.car_manager = Car_manager.CarManager()
        self.simulation_time = 0
        self.route_algorithm = None
        self.q_tables = {}
        self.map_graph = None

    def create_q_tables(self):
        """
        Creates the q tables for the simulation.
        q table state consists of the following:
        - current road/the node at the end of the current road
        - destination node/road.
        - time and day of the week.

        :return:
        """
        self.q_tables = {}
        #q table formats:
        #q_table = {state: {action: value}}

    def get_road_network(self):
        return self.road_network


    def set_map(self):




    def start_simulation(self):
        self.route_algorithm = input("Please choose a route algorithm: ")
        self.road_network.create_road_network()
        map_graph_location = input("Please enter the location of the map graph: ")

        self.create_cars()
        self.update_simulation()
        self.print_results()
