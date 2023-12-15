import datetime
import random
import numpy as np
from Main_Files import Node
class Road:
    """
    Represents a road segment in a road network.

    Attributes:

    id (int): The unique identifier of the road.

    source_node (Node): The source node of the road.

    destination_node (Node): The destination node of the road.

    length (int): The length of the road in meters.

    max_speed (int): The maximum speed limit on the road in km/h.

    road_speed_dict (dict): A dictionary mapping times to road speeds (key: time, value: speed).

    current_speed (int): The current speed of traffic on the road in km/h.

    eta_dict (dict): A dictionary mapping times to estimated time of arrival (ETA) (key: time, value: ETA).

    estimated_time (float): The estimated time it takes to travel the road in seconds.

    activate_traffic_lights (bool): Indicates whether traffic lights are activated on the road (True) or not (False).

    is_blocked (bool): Indicates whether the road is currently blocked (True) or not (False).

    adjacent_roads (list): A list of IDs of adjacent roads to this road.
    """
    def __init__(self, id:int , source_node:Node, destination_node:Node, length: int, max_speed: int, type: str, activate_traffic_lights: bool, rain_intensity: int = 0):

        # Attributes
        self.id = id
        self.source_node = source_node  # class Node (id, osm_id, lat, lon, street_count, traffic_lights)
        self.destination_node = destination_node  # class Node (id, osm_id, lat, lon, street_count, traffic_lights)
        self.length = length
        self.type = type
        self.max_speed = max_speed
        self.current_speed = 10
        self.estimated_time = float('inf')

        # Dicts
        self.road_speed_dict = {}  # key: time (for example "08:00"), value: speed
        self.eta_dict = {}  # key: time (for example "08:00"), value: eta

        # Past Information
        self.past_speeds = {}

        # Flags
        self.activate_traffic_lights = activate_traffic_lights
        self.rain_intensity = rain_intensity
        self.is_blocked = False

        # Adjacency
        self.adjacent_roads = []  # list of adjacent roads to this road, includes only the ids of the roads

        # Initialize
        self.calculate_time()  # initialize the estimated time



    # Functions
    def calculate_time(self):
        """
        Calculate the estimated time it takes to travel the road.

        Returns:
        float: The estimated time in seconds.
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

    def update_speed(self, current_time: datetime, traffic_white_noise: bool = True):
        """
        Update the current speed of the road based on the provided time and recalculate ETA.

        Args:
        current_time (str): The current time.

        Returns:
        float: The updated estimated time of arrival (ETA) in seconds.
        """
        current_hour_and_minute = current_time.strftime("%H:%M")
        projected_speed = self.road_speed_dict[current_hour_and_minute]
        if traffic_white_noise:
            # add white noise to the speed
            mean = 0  # Mean of the normal distribution (adjust as needed)
            if type == 'living_street' or type == 'residential' or type == 'unclassified':
                std_dev = 1
            else:
                std_dev = 4  # Standard deviation of the normal distribution (adjust as needed)
            noise = int(np.random.normal(mean, std_dev))
            if noise < 0:
                projected_speed = max(projected_speed + noise, 1)
            else:
                projected_speed = min(projected_speed + noise, self.max_speed)

        # check if there is rain
        if self.rain_intensity == 0:
            reduction_factor = 1.0  # No rain, no reduction
        elif self.rain_intensity == 1:
            reduction_factor = 0.95  # Light rain, 5% reduction
        elif self.rain_intensity == 2:
            reduction_factor = 0.85  # Moderate rain, 15% reduction
        else: # self.rain_intensity == 3:
            reduction_factor = 0.70  # Heavy rain, 30% reduction

        self.current_speed = max(int(projected_speed * reduction_factor), 1)
        self.past_speeds[current_time.replace(second=0)] = self.current_speed
        eta = self.calculate_time()
        return eta

    def update_road_speed_dict(self, new_speed: dict):
        """
        Update the road speed dictionary and recalculate ETA values.

        Args:
        new_speed (dict): A dictionary containing times and corresponding road speeds.

        Returns:
        None
        """
        self.road_speed_dict = new_speed
        self.update_eta_dict()
        return

    def update_eta_dict(self):
        """
        Update the ETA dictionary based on the current road speeds.

        Returns:
        None
        """
        for key, value in self.road_speed_dict.items():
            new_val = self.calculate_eta(value)
            self.eta_dict[key] = new_val
        return

    def calculate_eta(self, speed: int):
        """
        Calculate the estimated time of arrival (ETA) based on the provided speed.

        Args:
        speed (int): The speed of travel on the road in km/h.

        Returns:
        float: The estimated time of arrival (ETA) in seconds.
        """
        total_time = round(3.6 * self.length / speed,2)
        if self.destination_node.traffic_lights and self.activate_traffic_lights: # has traffic lights
            street_count = self.destination_node.street_count # get the street count of the destination node

            # Activate the traffic lights
            if street_count > 1:
                total_time += random.randrange(0, 20 * (street_count - 1), 1)
            else:
                total_time += random.randrange(0, 5, 1)
        return total_time

    # Gets

    def get_eta(self, time: str):
        """
        Get the estimated time of arrival (ETA) for the specified time.

        Args:
        time (str): The time for which ETA is requested.

        Returns:
        float: The estimated time of arrival (ETA) in seconds.
        """
        return self.eta_dict[time]

    def block(self):
        """
        Block the road.

        Returns:
        None
        """
        self.is_blocked = True
        self.estimated_time = float('inf')
        return

    def unblock(self):
        """
        Unblock the road.

        Returns:
        None
        """
        self.is_blocked = False
        new_eta = self.calculate_time()
        return new_eta, self.current_speed
    def __str__(self):
        return "Road id: " + str(self.id) + ", source node: " + str(self.source_node.id) + ", destination node: " + str(self.destination_node.id) + ", length: " + str(self.length) + ", max speed: " + str(self.max_speed) + ", current speed: " + str(self.current_speed) + ", is blocked: " + str(self.is_blocked) #+ ", cars on road: " + str(self.cars_on_road)


    def __repr__(self):
        return f"Road(road_id={self.id}, source_node={self.source_node.id}, destination_node={self.destination_node.id}, length={self.length}, speed={self.current_speed})"
