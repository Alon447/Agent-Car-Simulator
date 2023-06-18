import Road_Network
from new_master import Route


class Car:

    def __init__(self, id, source_node, destination_node, starting_time, road_network, route_algorithm = 'random' ):

        # ID
        self.id = id # car id

        # Nodes
        self.source_node = source_node # source node
        self.destination_node = destination_node # destination node

        # Roads
        self.current_road = None # the car's current road
        self.past_roads = [] # a list of the roads the car has been on, and his entering time to each one
        self.past_nodes= [] # a list of the nodes the car has been on, and his entering time to each one
        # self.source_road = None  # source road
        # self.destination_road = None  # destination road

        # Time
        self.starting_time = starting_time # the time the car started its journey
        self.time_until_next_road = 0 # the time until the car reaches the next road *IN SECONDS*
        self.total_travel_time = 0 # the total travel time of the car

        # Flags
        self.is_finished = False # indicates if the car has reached its destination
        self.car_in_destination = False # indicates if the car is in the destination node

        # Route
        self.route_algorithm = route_algorithm # the algorithm the car will use to decide its route
        self.route = self.decide_route_algorithm(route_algorithm) # the route the car will take
        #self.route=Route.Route() # the route the car will take
        self.road_network = road_network # the road network the car is in
        ###############################################
        # we need to pass rods to Route and not nodes
        ###############################################

    # FUNCTIONS
    def decide_route_algorithm(self, route_algorithm):
        if route_algorithm == "q learning":
           return Route.Q_Learning_Route()
        elif route_algorithm == "shortest_path":
            return Route.Shortest_path_route()
        else:
            return Route.Random_route()

    def start_car(self):
        #  move the car to the first road-based on starting node
        #  update car's time until next road
        self.current_road =self.road_network.get_road_by_source_node(self.source_node)
        #print(self.current_road)
        self.update_time_until_next_road(self.current_road)
        self.past_nodes.append(self.source_node)
        return self.current_road

    def decide_next_road(self):
        # return the ID of the next road the car will travel to

        #self.route.get_next_road parameters: (source_road_id, destination_node, time)
        next_road = self.route.get_next_road(self.current_road.get_destination_node(), self.destination_node,self.current_road.get_adjacent_roads(), self.road_network,self.total_travel_time+self.starting_time)
        if next_road is None: # case of no adjacent roads
            return None
        return next_road

    def move_next_road(self):
        """
        move the car to the next road-based on route's next node
        update car's time until next road

        :return:
        """
        if(self.check_if_finished()):
            return None

        self.past_roads.append(self.current_road)
        self.past_nodes.append(self.current_road.get_destination_node())
        next_road = self.decide_next_road() # gets a road object
        if next_road is None:
            self.is_finished = True
            self.car_in_destination = True
            return None
        id = int(next_road.get_id())
        self.current_road = self.road_network.get_roads_array()[id]
        self.road_network.get_roads_array()[id].add_car_to_road(self)
        #TODO: remove car from current road
        self.update_time_until_next_road(self.current_road)
        #self.set_time_until_next_road(self.current_road.get_length()*3.6 / self.current_road.get_current_speed())
        return self.current_road

    def check_if_finished(self):#assuming reaching for the destination road is sufficient
        if self.current_road.get_destination_node() == self.destination_node:
            self.past_roads.append(self.current_road)
            self.past_nodes.append(self.current_road.get_destination_node())
            self.is_finished = True
            self.car_in_destination = True
            #print("Car " + str(self.id) + " has reached its destination")

        return self.is_finished
    def get_travel_data(self):
        # return the  total travel time, path taken, travel time in each road, starting time, ending time.
        return self.total_travel_time, self.past_roads, self.starting_time, self.total_travel_time

    def get_past_nodes(self):
        return self.past_nodes
    def update_time_until_next_road(self, road):
        self.time_until_next_road += round((road.get_length() * 3.6 / road.get_current_speed()),2) # need to convert km/h to m/s
        return

    def update_travel_time(self, time):
        # used when we fast-forward the simulation
        self.total_travel_time += time
        self.time_until_next_road -= time
        return

    # Gets
    def get_id(self):
        return self.id
    def get_source_node(self):
        return self.source_node
    def get_destination_node(self):
        return self.destination_node
    def get_starting_time(self):
        return self.starting_time

    def get_routing_algorithm(self):
        return self.route_algorithm
    def get_time_until_next_road(self):
        return self.time_until_next_road
    def get_total_travel_time(self):
        return self.total_travel_time
    def get_past_roads(self):
        return self.past_roads
    def get_car_in_destination(self):
        return self.car_in_destination
    # Sets
    def set_time_until_next_road(self, time_until_next_road):
        self.time_until_next_road = time_until_next_road


    def __str__(self) -> str:
        return "Car_id: " + str(self.id) + ", " + "Travel_time: " + str(self.total_travel_time)+ ", " + "Current Road: " + str(self.current_road.get_id())+", " +"Length: "+str(self.current_road.get_length())+","+"Time until update: " + str(self.time_until_next_road)+ "\n"

    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.id == other.id and self.source_node == other.source_node and self.destination_node == other.destination_node and self.starting_time == other.starting_time




