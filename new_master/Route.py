from abc import abstractmethod, ABC
import random

from new_master.Road_Network import Road_Network


class Route(ABC):
    @abstractmethod
    def get_next_road(self, source_road, destination_node, time,road_network):
        pass

    @abstractmethod
    def decide_first_road(self, source_node, road_network):
        pass


class Random_route(Route):

    def decide_first_road(self, source_node, road_network):
        for road in road_network.get_roads_array():
            if road.get_source_node() == source_node:
                return road

    def get_next_road(self, source_road, destination_node, adjacency_list,road_network):
        """
        :param source_road: Road
        :param destination_node:
        :param adjacency_list: list of adjacent roads
        :param time: 0 for now
        :param road_network: Road_Network
        :return:  next road to travel to : Road

        """
        # TODO: update according to connectivity list implementation

        choice = random.randint(0, len(adjacency_list) - 1)
        next_road = adjacency_list[choice]
        count=0
        while len(next_road.get_adjacent_roads()) == 0:
            choice = random.randint(0, len(adjacency_list) - 1)
            next_road = adjacency_list[choice]
            count+=1

            if count>5: # case of no adjacent roads
                print("no adjacent roads")
                return None

        return next_road


class Q_Learning_Route(Route):
    def get_next_road(self, source_road, destination_node, time, road_network):
        """

        :param source_road:
        :param destination_node:
        :param time:
        :param road_network:
        :return:
        """

        # Implement Q-learning route logic here
        # Return a new edge based on the Q-learning algorithm
        pass

    def decide_first_road(self, source_node, road_network):
        for road in road_network.get_roads_array():
            if road.get_source_node() == source_node:
                return road


class Shortest_path_route(Route):

    def get_next_road(self, source_node, destination_node, time,road_network):
        # TODO: update according to distance matrix implementation
        return road_network.get_next_road(source_node, destination_node)

    def decide_first_road(self, source_node, road_network):
        for road in road_network.get_roads_array():
            if road.get_source_node() == source_node:
                return road

