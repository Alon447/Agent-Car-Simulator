import datetime
import osmnx as ox

class Cars:
    def __init__(self, id, route = [340368898, 2469720080, 290614029, 340318789, 2469720099, 340318978, 340309691, 336081282, 336081749, 139708]):
        self.id = id
        self.graph = ox.load_graphml('./data/graphTLVtime2.graphml')
        self.node_route = route # nodes node_route
        self.edges_route = ox.utils_graph.get_route_edge_attributes(self.graph,  self.node_route, 'osmid') # edges node_route
        self.next_node_index = 1 # the next node that the car will go to
        self.next_edge_index = 1 # the next edge that the car will go to
        self.is_finished = False # indicates if the car has reached its destination
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

    def get_next_node(self):
        return self.node_route[self.next_node_index]

    def get_next_edge(self):
        # return a tuple of the form (u, v, key)
        return self.edges_route[self.next_edge_index]

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
        if len(self.node_route)==1: # means that the car is in the last node of the node_route
            is_finished =True # after the car is finished i think we need to remove it

    def update_travel_time(self, finishing_time):
        #  Calculate the travel time of the car
        self.travel_time = finishing_time - self.starting_time

    def create_edges_route(self):
        # Create the edges node_route of the car from the node_route that contains the nodes
        edges_route = []
        for i in range(len(self.node_route) - 1):
            current_edge = (self.node_route[i] , self.node_route[i + 1] , 0)
            edges_route.append(current_edge)
        self.edges_route = edges_route
        return edges_route

    def move_next(self):
        self.next_node_index += 1
        self.next_edge_index += 1


    def __str__(self):
        return "id: " + str(self.id) + "\n"

    def __repr__(self):
        return self.__str__()
