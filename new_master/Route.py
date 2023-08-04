import datetime
import os
from abc import abstractmethod, ABC
import random

import numpy as np

from new_master.Q_Learning_Functions import QLearning
from new_master.Road_Network import Road_Network


class Route(ABC):
    @abstractmethod
    def decide_first_road(self, source_node, road_network):
        pass
    @abstractmethod
    def get_next_road(self, source_road, destination_node, adjacency_list,road_network,time):
        pass



    def get_alt_road(self, source_road, destination_node, adjacency_list,road_network,time):
        """

        :param source_road:
        :param destination_node:
        :param adjacency_list:
        :param road_network:
        :param time:
        :return:
        """
        pass

class Random_route(Route):

    def decide_first_road(self, source_node, road_network):
        for road in road_network.get_roads_array():
            if road.get_source_node() == source_node:
                return road

    def get_next_road(self, source_node, destination_node, adjacency_list,road_network,time):
        """
        :param source_node: int
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

    def get_alt_road(self, source_road, destination_node, adjacency_list, road_network, time):
        for road in adjacency_list:
            if not road.get_is_blocked():
                return road
        return None

class Q_Learning_Route(Route):
    def __init__(self, src_node: int, dst_node: int, road_network: Road_Network, start_time: datetime.datetime):
        # self.q_table = None
        # src and dst dosent change during the run
        self.src_node = src_node
        self.dst_node = dst_node
        # current node changes during the run, it represents the current's road destination node
        self.current_node = src_node
        self.start_time = start_time
        self.road_network = road_network
        self.agent = QLearning(road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.2)

        num_episodes = 2000
        max_steps_per_episode = 100
        full_tables_path = self.get_tables_directory(r"q_learning_data")
        if self.agent.load_q_table(self.src_node, self.dst_node, full_tables_path):
            self.q_table = self.agent.get_q_table()
        else:
            self.q_table = self.agent.train_src_dst(src_node, dst_node, self.start_time, num_episodes, max_steps_per_episode=max_steps_per_episode)
            self.agent.save_q_table(self.src_node, self.dst_node, full_tables_path)
        # Test the agent
        test_reward, agent_path = self.agent.test_src_dst(src_node, dst_node, self.start_time)  # this will be the test function
        self.path = agent_path

    def get_tables_directory(self, tables_directory):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, tables_directory)
        return data


    def decide_first_road(self, source_node, road_network):

        """

        :param source_node:
        :param road_network:
        :return:
        """
        action = np.argmax(self.q_table[self.src_node]) # action is the index of the destination node in the q table
        dest_node = self.road_network.get_node_connectivity_dict()[self.src_node][action]
        self.current_node = dest_node
        road_index = self.road_network.road_dict[(self.src_node, dest_node)]
        return self.road_network.get_roads_array()[road_index]
        # for road in road_network.get_roads_array():
        #     if road.get_source_node() == source_node:
        #         return road


    def get_next_road(self, source_road, destination_node, adjacency_list, road_network,time):
        """

        :param adjacency_list:
        :param source_road:
        :param destination_node:
        :param time:
        :param road_network:
        :return:
        """
        action = np.argmax(self.q_table[self.current_node])  # action is the index of the destination node in the q table
        dest_node = self.road_network.get_node_connectivity_dict()[self.current_node][action]

        road_index = self.road_network.road_dict[(self.current_node, dest_node)]
        self.current_node = dest_node
        return self.road_network.get_roads_array()[road_index]
        # Implement Q-learning route logic here
        # Return a new edge based on the Q-learning algorithm



    def get_alt_road(self, source_road, destination_node, adjacency_list, road_network, time):
        pass #TODO: implement

class Shortest_path_route(Route):
    def __init__(self, src_node, dst_node, road_network):
        self.src_node = src_node
        self.dst_node = dst_node

        # current node changes during the run, it represents the current's road destination node
        self.current_node = src_node
        self.road_network = road_network

    def decide_first_road(self, source_node, road_network):
        if self.src_node == self.dst_node:
            return None
        first_road = self.road_network.get_next_road_shortest_path(self.src_node, self.dst_node)
        self.current_node = first_road.get_destination_node()
        return first_road
        # for road in road_network.get_roads_array():
        #     if road.get_source_node() == source_node:
        #         return road

    def get_next_road(self, source_node, destination_node, adjacency_list, road_network,time):
        # TODO: update according to distance matrix implementation
        if self.current_node == self.dst_node:
            return None
        next_road = self.road_network.get_next_road_shortest_path(self.current_node, self.dst_node)
        self.current_node = next_road.get_destination_node()
        return next_road

    def get_alt_road(self, source_road, destination_node, adjacency_list, road_network, time):
        minimum_distance = 999999999
        next_road = None
        for road in adjacency_list:
            if not road.get_is_blocked() :
                next_next_road = road_network.get_next_road(road.get_destination_node(), destination_node)
                current_distance = road.get_length() + road_network.distances_matrix[road.get_destination_node()][destination_node]
                if current_distance < minimum_distance:
                    minimum_distance = current_distance
                    next_road = road
        return next_road