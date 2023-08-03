import random


class Road:
    def __init__(self, id:int , source_node, destination_node, length, max_speed):

        self.id= id
        self.source_node = source_node # class Node
        self.destination_node = destination_node # class Node
        self.length = length

        self.max_speed = max_speed
        self.road_speed_dict = {} # key: time (for example "08:00") , value: speed
        self.current_speed = 10
        self.eta_dict={} # key: time (for example "08:00") , value: eta
        self.estimated_time = float('inf')

        self.is_blocked= False
        # self.cars_on_road = []
        self.adjacent_roads = [] # list of adjacent roads to this road, includes only the ids of the roads

        self.calculate_time() # initialize the estimated time

    # Functions
    def block(self):
        self.is_blocked = True

    def unblock(self):
        self.is_blocked = False

    def calculate_time(self):
        """
        Calculates the time it takes to travel on this road
        length - meters
        speed - km/h
        time - seconds
        so, we need to convert speed to m/s by dividing by 3.6
        :return: time in seconds
        """
        if self.current_speed is None:
            print("error")

        total_time = 3.6 * self.length / self.current_speed
        if self.get_traffic_lights():
            street_count = self.get_street_count()
            # Activate the traffic lights
            # if street_count > 1:
            #     total_time += random.randrange(0, 20 * (self.get_street_count() - 1), 1)
            # else:
            #     total_time += random.randrange(0, 5, 1)
        self.estimated_time = round(total_time, 2)
        return self.estimated_time

    def update_speed(self, current_time: str):
        self.current_speed = self.road_speed_dict[current_time]
        eta = self.calculate_time()
        return eta

    def update_road_speed_dict(self, new_speed: dict):
        """
        updates the road speed dict, and calls for update eta dict based on the new speeds
        :param new_speed:dict of time and speed
        :return:
        """
        self.road_speed_dict = new_speed
        self.update_eta_dict()
        return

    def update_eta_dict(self):
        for key, value in self.road_speed_dict.items():
            new_val = self.calculate_eta(value)
            self.eta_dict[key] = new_val
        return

    def calculate_eta(self, speed: int):
        return round(3.6 * self.length / speed,2)

    # Gets
    def get_id(self):
        return self.id

    def get_length(self):
        return self.length
    def get_current_speed(self):
        return self.current_speed
    def get_max_speed(self):
        return self.max_speed
    def get_is_blocked(self):
        return self.is_blocked
    def get_adjacent_roads(self):
        return self.adjacent_roads

    def get_source_node_attributes(self):
        return self.source_node
    def get_destination_node_attributes(self):
        return self.destination_node

    def get_source_node(self):
        # return the new id of the source node
        return self.source_node[0]
    def get_source_node_osm_id(self):
        # return the osm id of the source node
        return self.source_node[1]

    def get_destination_node(self):
        # return the new id of the destination node
        return self.destination_node[0]
    def get_destination_node_osm_id(self):
        # return the osm id of the destination node
        return self.destination_node[1]
    def get_destination_node_lat(self):
        # return the destination node lat
        return self.destination_node[2]
    def get_destination_node_lon(self):
        # return the destination node lon
        return self.destination_node[3]
    def get_street_count(self):
        # return the destination node street count
        return self.destination_node[4]
    def get_traffic_lights(self):
        # return the destination node traffic lights
        return self.destination_node[5]

    def get_eta(self, time: str):
        return self.eta_dict[time]
    # Sets
    def set_current_speed(self, speed):
        self.current_speed = speed




    def __str__(self):
        return "Road id: " + str(self.id) + ", source node: " + str(self.source_node) + ", destination node: " + str(self.destination_node) + ", length: " + str(self.length) + ", max speed: " + str(self.max_speed) + ", current speed: " + str(self.current_speed) + ", is blocked: " + str(self.is_blocked) #+ ", cars on road: " + str(self.cars_on_road)


    def __repr__(self):
        return f"Road(road_id={self.id}, source_node={self.source_node}, destination_node={self.destination_node}, length={self.length}, speed={self.current_speed})"
