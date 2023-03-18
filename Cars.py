


class Cars:
    def __init__(self, id, route,next_node_index, is_finished, travel_time):
        self.id = id
        self.route = route
        self.next_node_index = route[0] # we need to decide if this parameter is a node or an index of a node in the route
        self.is_finished = False
        self.travel_time = 0
        #  MAYBE WE NEED THE CARS TO STORE THE CURRENT EDGE AND THE NEXT EDGE. THE CURRENT EDGE TO CALCULATE THE TRAVEL TIME AND THE NEXT EDGE TO ASK TO MOVE TO THE EDGE IN THE NEXT TICK.

    def get_id(self):
        return self.id

    def get_route(self):
        return self.route

    def get_next_node_index(self):
        return self.next_node_index

    def get_travel_time(self):
        return self.travel_time

    def is_finished(self):
        return self.is_finished

    def set_next_node_index(self, next_node_index):
        self.next_node_index = next_node_index

    def set_route(self, route):
        self.route = route

    def set_is_finished(self):
        if len(self.route)==1: # means that the car is in the last node of the route
            is_finished=True # after the car is finished i think we need to remove it

    def update_travel_time(self):
        self.travel_time += ??

    def move_node(self):
        self.next_node_index += 1 # I think this is a mistake, we need to move the car to the next node in the route, not to the next index in the route

    def __str__(self):
        return "id: " + self.id + "\n" + "route: " + str(self.route) + "\n" + "next node: " + str(self.route[self.next_node_index])