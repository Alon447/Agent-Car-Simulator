import math


class Node:
    def __init__(self, id, osm_id, x, y, traffic_lights, street_count):
        self.id = id
        self.osm_id = osm_id
        self.x = x
        self.y = y
        self.traffic_lights = traffic_lights
        self.street_count = street_count

    # Gets
    def get_id(self):
        return self.id
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_traffic_lights(self):
        return self.traffic_lights
    def get_street_count(self):
        return self.street_count
    # Sets
    def set_traffic_lights(self, traffic_lights):
        self.traffic_lights = traffic_lights

    # Functions
    def calculate_distance(self, other_node):
        # Convert degrees to radians
        lat1 = math.radians(self.x)
        lon1 = math.radians(self.y)
        lat2 = math.radians(other_node.get_x())
        lon2 = math.radians(other_node.get_y())

        # Radius of the Earth in kilometers
        radius = 6371

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c

        return distance
