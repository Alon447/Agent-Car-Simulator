import Road_Network
from Main_Files import Route
import datetime
import pandas as pd


def time_delta_to_seconds(time):
    return int(time.total_seconds())


class Car:


    def __init__(self, id:int, source_node:int, destination_node:int, starting_time:datetime, road_network:Road_Network, route_algorithm = 'random' ):

        # ID
        self.id = id # car id
        self.road_network = road_network # the road network the car is in

        # Nodes
        self.source_node = source_node # source node
        self.destination_node = destination_node # destination node

        # Roads
        self.current_road = None # the car's current road
        self.past_roads = [] # a list of the roads the car has been on, and his entering time to each one
        self.past_nodes= [] # a list of the nodes the car has been on, and his entering time to each one
        self.distance_traveled = 0 # the distance the car has traveled so far
        # self.source_road = None  # source road
        # self.destination_road = None  # destination road

        # Time
        self.starting_time = starting_time # the time the car started its journey
        self.time_until_next_road = datetime.timedelta(seconds=0) # the time until the car reaches the next road *IN SECONDS*
        self.total_travel_time = datetime.timedelta(seconds=0) # the total travel time of the car
        self.current_road_time = datetime.timedelta(seconds=0) # the time the car has been on the current road

        # Flags
        self.is_finished = False # indicates if the car has reached its destination
        self.car_in_destination = False # indicates if the car is in the destination node
        self.is_blocked = False # indicates if the car is blocked
        # Route
        self.route_algorithm = route_algorithm # the algorithm the car will use to decide its route
        self.route = self.decide_route_algorithm(route_algorithm, source_node, destination_node) # the route the car will take
        ###############################################
        # we need to pass rods to Route and not nodes
        ###############################################

    # FUNCTIONS
    def decide_route_algorithm(self, route_algorithm: str, source_node: int, destination_node: int):
        """

        :param route_algorithm: string that represents the route algorithm
        :return: route object that represents the route algorithm
        """
        q_learning_names = [ "q learning", "Q learning", "Q Learning", "q Learning","q","Q"]
        shortest_path_names = ["shortest_path", "shortest path", "Shortest Path", "Shortest path", "shortest", "Shortest","SP","sp"]
        if route_algorithm in q_learning_names:
           return Route.Q_Learning_Route(source_node, destination_node, self.road_network, self.starting_time)
        elif route_algorithm in shortest_path_names:
            return Route.Shortest_path_route(source_node,destination_node, self.road_network)
        else:
            return Route.Random_route()

    def start_car(self):
        """
        move the car to the first road-based on starting node and update car's time until next road

        :return:  the first road the car will travel to
        """
        first_road = self.route.decide_first_road(self.source_node, self.road_network)
        self.current_road = first_road
        self.update_time_until_next_road(self.current_road)
        self.past_nodes.append(self.source_node)
        return self.current_road

    def decide_next_road(self):
        """
        decide the next road the car will travel to
        :return: Road object that corresponds the next road place in the roads_array in road_network
        """
        #self.route.get_next_road parameters: (source_road_id, destination_node, time)
        next_road = self.route.get_next_road(self.current_road.destination_node.id,
                                             self.destination_node, self.current_road.adjacent_roads,
                                             self.road_network,
                                             self.total_travel_time + self.starting_time)
        # if next_road is None: # case of no adjacent roads
        #     return None
        return next_road

    def decide_alt_road(self):
        # return the ID of the next road the car will travel to

        # self.route.get_next_road parameters: (source_road_id, destination_node, time)
        next_road = self.route.get_alt_road(self.current_road.destination_node[0], self.destination_node,
                                            self.current_road.adjacent_roads, self.road_network,
                                            self.total_travel_time + self.starting_time)
        return next_road

    def move_next_road(self, time):
        """
        move the car to the next road-based on route's next node
        update car's time until next road

        :return:
        """
        self.current_road_time += pd.Timedelta(seconds=time)  # time
        if self.check_if_finished():
            return None

        next_road = self.decide_next_road()  # gets a road object
        if next_road is None:
            self.is_finished = True
            self.car_in_destination = True
            return None
        elif next_road.is_blocked:
            next_road = self.decide_alt_road()
            if next_road is None:  # all roads are blocked
                self.is_blocked = True
                return "blocked"

        # appends and adds distance only if moved to next road
        self.distance_traveled += self.current_road.length
        self.past_nodes.append(self.current_road.destination_node.id)
        self.past_roads.append({self.current_road.id: round(time_delta_to_seconds(self.current_road_time), 2)})

        id = int(next_road.id)
        self.current_road = self.road_network.roads_array[id]
        # self.road_network.get_roads_array()[id].add_car_to_road(self)
        # TODO: remove car from current road
        self.update_time_until_next_road(self.current_road)
        # self.set_time_until_next_road(self.current_road.get_length()*3.6 / self.current_road.get_current_speed())
        self.current_road_time = datetime.timedelta(seconds=0)
        return self.current_road

    def check_if_finished(self):
        # assuming reaching for the destination road is sufficient
        """
        check if the car has reached its destination
        :return: True if the car has reached its destination, False otherwise
        """
        if self.current_road.destination_node.id == self.destination_node:
            self.past_roads.append(
                {self.current_road.id: round(time_delta_to_seconds(self.current_road_time), 2)})
            self.past_nodes.append(self.current_road.destination_node.id)
            self.is_finished = True
            self.car_in_destination = True
            # print("Car " + str(self.id) + " has reached its destination")

        return self.is_finished

    def force_finish(self):
        """
        force the car to finish its route,
        used in car manager when the simulation has to end and the car hasn't reached its destination
        :return:
        """
        self.past_roads.append({self.current_road.id: round(time_delta_to_seconds(self.current_road_time), 2)})
        # self.past_nodes.append(self.current_road.destination_node[0])
        return



    def update_time_until_next_road(self, road):
        """
        updates the time until the car reaches the next road
        :param road: Road object
        :return:
        """
        time = road.calculate_time()
        self.time_until_next_road += datetime.timedelta(
            seconds=time)  # round((road.get_length() * 3.6 / road.get_current_speed()),2) # need to convert km/h to m/s
        return

    def update_travel_time(self, time):
        """
        update the total travel time and the time until the next road
        :param time:
        :return:
        """
        # used when we fast-forward the simulation
        self.total_travel_time += datetime.timedelta(seconds=time)  # time
        self.time_until_next_road -= datetime.timedelta(seconds=time)  # time
        return

    # Gets
    # def get_travel_data(self):
    #     # return the  total travel time, path taken, travel time in each road, starting time, ending time.
    #     return self.total_travel_time, self.past_roads, self.starting_time, self.total_travel_time
    # def get_ending_time(self):
    #     return time_delta_to_seconds(self.total_travel_time + self.starting_time)

    # starting time and ending time for the simulation end

    def get_routing_algorithm(self):
        """
        :return: the routing algorithm the car will use
        """
        q_learning_names = ["q learning", "Q learning", "Q Learning", "q Learning", "q", "Q"]
        shortest_path_names = ["shortest_path", "shortest path", "Shortest Path", "Shortest path", "shortest",
                               "Shortest", "SP", "sp"]
        if self.route_algorithm in q_learning_names:
            return "Q Learning"
        elif self.route_algorithm in shortest_path_names:
            return "Shortest Path"
        else:
            return "Random Route"

    def get_time_until_next_road(self):
        """
        :return: the time until the car reaches the next road
        """
        if self.is_blocked:
            self.time_until_next_road = 600
        return int(self.time_until_next_road.total_seconds())

    # def get_total_travel_time(self):
    #     return time_delta_to_seconds(self.total_travel_time)
    def get_xy_source(self):
        """
        :return: the x,y coordinates of the source node
        """
        return self.road_network.get_xy_from_node_id(self.source_node)

    def get_xy_destination(self):
        """
        :return: the x,y coordinates of the destination node
        """
        return self.road_network.get_xy_from_node_id(self.destination_node)

    def get_xy_current(self):
        """
        :return: the x,y coordinates of the current node
        """
        return self.road_network.get_xy_from_node_id(self.current_road.source_node.id)

    def __str__(self) -> str:
        return "Car_id: " + str(self.id) + ", " + "Travel_time: " + str(
            self.total_travel_time) + ", " + "Current Road: " + str(
            self.current_road.id) + ", " + "Length: " + str(
            self.current_road.length) + "," + "Time until update: " + str(self.time_until_next_road) + "\n"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id and self.source_node == other.source_node and self.destination_node == other.destination_node and self.starting_time == other.starting_time