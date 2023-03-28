import datetime
import osmnx as ox
import nodes


class Cars:
    def __init__(self, id, start_node_id, end_node_id):

        self.id = id
        self.graph = ox.load_graphml('./data/graphTLVfix.graphml')
        self.node_route = ox.shortest_path(self.graph, nodes.NODES_ID[start_node_id],  nodes.NODES_ID[end_node_id], weight='length')# nodes node_route
        #print(f"CAR {self.id} ROUTE: {self.node_route}")
        self.edges_route = ox.utils_graph.get_route_edge_attributes(self.graph, self.node_route, 'edge_id')  # edges node_route
        self.next_node_index = 1  # the next node that the car will go to
        self.next_edge_index = 1  # the next edge that the car will go to
        self.is_finished = False  # indicates if the car has reached its destination
        self.starting_time = datetime.datetime.now()
        self.travel_time = 0

        #  MAYBE WE NEED THE CARS TO STORE THE CURRENT EDGE AND THE NEXT EDGE. THE CURRENT EDGE TO CALCULATE THE TRAVEL TIME AND THE NEXT EDGE TO ASK TO MOVE TO THE EDGE IN THE NEXT TICK.

    # GETS
    def get_id(self):
        return self.id

    def get_nodes_route(self):
        return self.node_route

    def get_edges_route(self):
        return self.edges_route

    def get_first_edge(self):
        return int(self.edges_route[0])

    def get_next_node(self):
        # return the next node_id that the car will go to
        return int(self.node_route[self.next_node_index])

    def get_next_edge(self):
        # return the next edge_id that the car will go to
        if self.next_edge_index == len(self.edges_route):
            self.is_finished = True
            print(f"CAR {self.id} IS FINISHED")
            return None
        return int(self.edges_route[self.next_edge_index])

    def get_travel_time(self):
        return self.travel_time

    def is_finished(self):
        return self.is_finished

    # SETS
    def set_next_node_index(self, next_node_index):
        self.next_node_index = next_node_index

    def set_route(self, route):
        self.node_route = route

    def set_is_finished(self):
        if len(self.node_route) == 1:  # means that the car is in the last node of the node_route
            self.is_finished = True  # after the car is finished i think we need to remove it

    def update_travel_time(self, finishing_time):
        #  Calculate the travel time of the car
        self.travel_time = finishing_time - self.starting_time



    """
    WE DONT NEED THIS FUNCTION ANYMORE
    
    def create_edges_route(self):
        # Create the edges node_route of the car from the node_route that contains the nodes
        edges_route = []
        for i in range(len(self.node_route) - 1):
            current_edge = (self.node_route[i] , self.node_route[i + 1] , 0)
            edges_route.append(current_edge)
        self.edges_route = edges_route
        return edges_route
"""

    def move_next(self):
        # Function to use when we want to move the car to the next road
        self.next_node_index += 1
        self.next_edge_index += 1

    def __str__(self):
        return "car_id: " + str(self.id) + "\n"

    def __repr__(self):
        return self.__str__()
