from abc import abstractmethod, ABC
from random import random

from new_master.Road_Network import Road_Network


class Route(ABC):
    @abstractmethod
    def get_next_road(self, source_road, destination_node, time):
        pass

class Random_route(Route):

    def get_next_road(self, source_road, destination_node, time):
        """
        :param source_road: Road
        :param destination_node:
        :param time: 0 for now
        :return:  next road to travel to : Road
        """
        # TODO: update according to connectivity list implementation
        optional_roads = source_road.get_adjacent_roads()  # list of IDs of optional roads

        return random.choice(optional_roads)

class Q_Learning_Route(Route):
    def get_next_road(self, source_road, destination_node, time):
        # Implement Q-learning route logic here
        # Return a new edge based on the Q-learning algorithm
        pass

class Shortest_path_route(Route):

    def get_next_road(self, source_node, destination_node, time):
        # TODO: update according to distance matrix implementation
        return Road_Network.get_distance_matrix().get_road(source_node, destination_node)
