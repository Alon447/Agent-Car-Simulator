import random

from Main_Files import Node


class Road:
    def __init__(self, id:int , source_node:Node, destination_node:Node, length: int, max_speed: int, activate_traffic_lights: bool):

        self.id= id
        self.source_node = source_node # class Node (id, osm_id, lat, lon, street_count, traffic_lights)
        self.destination_node = destination_node # class Node (id, osm_id, lat, lon, street_count, traffic_lights)
        self.length = length

        self.max_speed = max_speed
        self.road_speed_dict = {} # key: time (for example "08:00") , value: speed
        self.current_speed = 10
        self.eta_dict={} # key: time (for example "08:00") , value: eta
        self.estimated_time = float('inf')
        self.activate_traffic_lights = activate_traffic_lights
        self.is_blocked= False
        # self.cars_on_road = []
        self.adjacent_roads = [] # list of adjacent roads to this road, includes only the ids of the roads

        self.calculate_time() # initialize the estimated time

    # Functions

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
        if self.destination_node.traffic_lights and self.activate_traffic_lights: # has traffic lights
            street_count = self.destination_node.street_count# get the street count of the destination node

            # Activate the traffic lights
            if street_count > 1:
                total_time += random.randrange(0, 20 * (street_count - 1), 1)
            else:
                total_time += random.randrange(0, 5, 1)
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

    def get_eta(self, time: str):
        return self.eta_dict[time]
    # Sets
    def set_current_speed(self, speed):
        self.current_speed = speed




    def __str__(self):
        return "Road id: " + str(self.id) + ", source node: " + str(self.source_node) + ", destination node: " + str(self.destination_node) + ", length: " + str(self.length) + ", max speed: " + str(self.max_speed) + ", current speed: " + str(self.current_speed) + ", is blocked: " + str(self.is_blocked) #+ ", cars on road: " + str(self.cars_on_road)


    def __repr__(self):
        return f"Road(road_id={self.id}, source_node={self.source_node}, destination_node={self.destination_node}, length={self.length}, speed={self.current_speed})"
