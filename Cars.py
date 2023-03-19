
class Cars:
    def __init__(self, id, route ,next_node_index, is_finished, starting_time, travel_time):
        self.id = id
        self.route = route # nodes route
        self.edges_route = []
        self.next_node_index = 1 # the next node that the car will go to
        self.next_edge_index = 1 # the next edge that the car will go to
        self.is_finished = False
        self.starting_time = starting_time
        self.travel_time = 0

        #  MAYBE WE NEED THE CARS TO STORE THE CURRENT EDGE AND THE NEXT EDGE. THE CURRENT EDGE TO CALCULATE THE TRAVEL TIME AND THE NEXT EDGE TO ASK TO MOVE TO THE EDGE IN THE NEXT TICK.

    # GETS
    def get_id(self):
        return self.id

    def get_route(self):
        return self.route

    def get_next_node(self):
        return self.route[self.next_node_index]

    def get_next_edge(self):
        return self.edges_route[self.next_edge_index]

    def get_travel_time(self):
        return self.travel_time

    def is_finished(self):
        return self.is_finished

    # SETS
    def set_next_node_index(self, next_node_index):
        self.next_node_index = next_node_index

    def set_route(self, route):
        self.route = route

    def set_is_finished(self):
        if len(self.route )==1: # means that the car is in the last node of the route
            is_finished =True # after the car is finished i think we need to remove it

    def update_travel_time(self, finishing_time):
        #  Calculate the travel time of the car
        self.travel_time = finishing_time - self.starting_time

    def create_edges_route(self, G):
        # Create the edges route of the car from the route that contains the nodes
        edges_route = []
        for i in range(len(self.route)-1):
            current_edge = (self.route[i] ,self.route[i +1] ,0)
            edges_route.append(current_edge)
        self.edges_route = edges_route
        return edges_route

    def move_next(self):
        self.next_node_index += 1
        self.next_edge_index += 1

    def __str__(self):
        return "id: " + self.id + "\n" + "route: " + str(self.route) + "\n" + "next node: " + str \
            (self.route[self.next_node_index])
