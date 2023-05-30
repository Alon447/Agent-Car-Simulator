import Route
class Car:

    def __init__(self, id, source_node, destination_node, starting_time,route_algorithm = "random"):
        self.id = id # car id
        self.source_node = source_node # source node
        self.destination_node = destination_node # destination node
        self.current_road = None # the car's current road
        self.past_roads = [] # a list of the roads the car has been on
        self.total_travel_time = 0 # the total travel time of the car
        self.time_until_next_road = 0 # the time until the car reaches the next road
        self.is_finished = False # indicates if the car has reached its destination
        self.starting_time = starting_time # the time the car started its journey
        self.route=Route.Route(source_node,destination_node,route_algorithm) # the route the car will take
        ###############################################
        # we need to pass rods to Route and not nodes
        ###############################################
    # Gets
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
    def get_travel_time(self):
        return self.total_travel_time
    def get_time_until_next_road(self):
        return self.time_until_next_road
    def is_finished(self):
        return self.is_finished
    def get_starting_time(self):
        return self.starting_time
    def get_route(self):
        return self.route
    # Sets
    def set_source_node(self, source_node):
        self.source_node = source_node
    def set_destination_node(self, destination_node):
        self.destination_node = destination_node
    def set_current_road(self, current_road):
        self.current_road = current_road
    def set_past_roads(self, past_roads):
        self.past_roads = past_roads
    def set_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time
    def set_time_until_next_road(self, time_until_next_road):
        self.time_until_next_road = time_until_next_road
    def set_finished(self):
        self.is_finished = True
    def set_starting_time(self, starting_time):
        self.starting_time = starting_time


    # Functions

    def get_next_road(self):
        #  move the car to the next road based on route's next node
        pass
    def move_next_road(self):
        pass

    def start_car(self):
        #  move the car to the first road based on starting node
        #  update car's time until next road
        pass
    def get_travel_data(self):
        # return the  total travel time, path taken, travel time in each road, starting time, ending time.
        return self.total_travel_time,self.past_roads, self.starting_time, self.total_travel_time
    def __str__(self) -> str:
        return "car_id: " + str(self.id) + "\n" + "travel_time: " + str(self.total_travel_time) + "\n"

    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.id == other.id and self.source_node == other.source_node and self.destination_node == other.destination_node and self.starting_time == other.starting_time


