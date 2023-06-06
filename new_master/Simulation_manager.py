import Road_Network
import Car_manager
from new_master import Car


class Simulation_manager:
    """
    This class manages the simulation.
    It will create the road network, the cars, the route algorithm and the q tables.
    It will also update the simulation and print the results.


    """

    def __init__(self,graph):
        self.road_network = Road_Network.Road_Network(graph)
        self.car_manager = Car_manager.CarManager()
        self.simulation_time = 0 # in seconds
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
        return




    def start_simulation(self):
        self.route_algorithm = input("Please choose a route algorithm: ")
        self.road_network.create_road_network()
        map_graph_location = input("Please enter the location of the map graph: ")

        self.create_cars()
        self.update_simulation()
        self.print_results()
        return

SM = Simulation_manager('/graphTLVfix.graphml')
RN = SM.get_road_network()
RN.generate_random_speeds()
RN.set_roads_speeds()
# roads = (RN.get_roads_array())
# for road in roads:
#     print(road)
c1 = Car.Car(1,1,4,0)
print(c1.start_car())
print(c1.decide_next_road())