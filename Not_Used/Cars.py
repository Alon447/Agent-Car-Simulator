import datetime
import osmnx as ox
import nodes
import Road


class Cars:
    def __init__(self, id, start_node, end_node):

        self.id = id
        self.source_node= start_node
        self.destination_node = end_node
        self.graph = ox.load_graphml('../data/graphTLVFix.graphml')
        self.current_road = None
        self.past_roads = []
        self.is_finished = False  # indicates if the car has reached its destination
        self.starting_time = datetime.datetime.now()
        self.total_travel_time = 0
        self.time_until_next_road = 0
        # self.node_route = ox.shortest_path(self.graph, nodes.NODES_ID[start_node_id], nodes.NODES_ID[end_node_id],
        #                                    weight='length')  # nodes node_route
        # self.edges_route = ox.utils_graph.get_route_edge_attributes(self.graph, self.node_route,
        #                                                             'edge_id')  # edges node_route
        # self.next_node_index = 1  # the next node that the car will go to
        # self.next_edge_index = 1  # the next edge that the car will go to

    # GETS
    def get_id(self):
        return self.id

    def get_source_node(self):
        return self.source_node

    def get_destination_node(self):
        return self.destination_node

    def get_current_road(self):
        return self.current_road

    def get_past_roads(self):
        return self.past_roads

    def get_starting_time(self):
        return self.starting_time

    def get_travel_time(self):
        return self.total_travel_time

    def is_finished(self):
        return self.is_finished

    def get_time_until_next_road(self):
        return self.time_until_next_road

    # SETS
    # def set_next_node_index(self, next_node_index):
    #     self.next_node_index = next_node_index
    #
    # def set_route(self, route):
    #     self.node_route = route

    def set_finished(self):
        self.is_finished = True  # after the car is finished i think we need to remove it

    def update_travel_time(self, travel_time):
        #  update the travel time of the car every time it moves to the next road
        self.total_travel_time += travel_time


    # FUNCTIONS

    def get_next_road(self):
        # Function to use when we want to move the car to the next road
        pass

    def move_next_road(self):
        pass

    def __str__(self):
        return "car_id: " + str(self.id) + "\n" + "travel_time: " + str(self.total_travel_time) + "\n"


    def __repr__(self):
        return self.__str__()

