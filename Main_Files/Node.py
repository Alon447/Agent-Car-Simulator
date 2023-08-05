import math


class Node:
    def __init__(self, id, osm_id, x, y, traffic_lights, street_count):
        self.id = id
        self.osm_id = osm_id
        self.x = x
        self.y = y
        self.traffic_lights = traffic_lights
        self.street_count = street_count

    def __str__(self):
        return f'Id: {self.id}, Osm_Id: {self.osm_id}, X: {self.x}, Y: {self.y}, Traffic_Lights: {self.traffic_lights}, Street_Count: {self.street_count}'
    def __repr__(self):
        return self.__str__()
    #
    # # Functions
    # def calculate_distance(self, other_node):
    #     # Convert degrees to radians
    #     lat1 = math.radians(self.x)
    #     lon1 = math.radians(self.y)
    #     lat2 = math.radians(other_node.x)
    #     lon2 = math.radians(other_node.y)
    #
    #     # Radius of the Earth in kilometers
    #     radius = 6371
    #
    #     # Haversine formula
    #     dlat = lat2 - lat1
    #     dlon = lon2 - lon1
    #     a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    #     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    #     distance = radius * c
    #
    #     return distance
