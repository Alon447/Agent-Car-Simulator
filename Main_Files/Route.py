import datetime
import os
from abc import abstractmethod, ABC
import random

import numpy as np

from Q_Learning_Classes.Q_Learning_Functions import QLearning
from Main_Files.Road_Network import Road_Network


class Route(ABC):
    """
    Route class (abstract):
    This abstract class represents a route that a car can take within a road network.

    Methods:
    decide_first_road(self): Decide the first road the car will take when starting its journey.
        Returns:
        Road object: The first road the car will take.

    get_next_road(self): Decide the next road the car will take while it's on a road.
        Returns:
        Road object: The next road the car will take.

    get_alt_road(self): Try to find an alternative road to the current road if it's blocked.
        Returns:
        Road object or None: An alternative road or None if no alternative is found.
    """
    @abstractmethod
    def decide_first_road(self):
        """
        Decide the first road the car will take when starting its journey.

        Returns:
        Road object: The first road the car will take.
        """
        pass
    @abstractmethod
    def get_next_road(self):
        """
        Decide the next road the car will take while it's on a road.

        Returns:
        Road object: The next road the car will take.
        """
        pass
    @abstractmethod
    def get_alt_road(self):
        """
        Try to find an alternative road to the current road if it's blocked.

        Returns:
        Road object or None: An alternative road or None if no alternative is found.
        """
        pass

class Random_route(Route):
    def __init__(self, src_node: int, dst_node: int, road_network: Road_Network):
        self.src_node = src_node
        self.dst_node = dst_node
        self.road_network = road_network
        # current node changes during the run, it represents the current's road destination node
        self.current_node = src_node

    def decide_first_road(self):
        for road in self.road_network.roads_array:
            if road.source_node[0] == self.src_node:
                self.current_node = road.destination_node.id
                return road

    def get_next_road(self):

        adjacency_list = self.road_network.node_connectivity_dict[self.current_node] # list of all the adjacent nodes ids
        choice = random.randint(0, len(adjacency_list) - 1)
        next_node = adjacency_list[choice]
        next_road = self.road_network.get_road_from_src_dst(self.current_node, next_node)
        count=0
        while len(next_road.adjacent_roads) == 0:
            choice = random.randint(0, len(adjacency_list) - 1)
            next_node = adjacency_list[choice]
            next_road = self.road_network.get_road_from_src_dst(self.current_node, next_node)
            count+=1

            if count>5: # case of no adjacent roads
                print("no adjacent roads")
                return None

        self.current_node = next_node
        return next_road

    def get_alt_road(self):
        adjacency_list = self.road_network.node_connectivity_dict[self.current_node] # list of all the adjacent nodes ids
        for next_node in adjacency_list:
            road = self.road_network.get_road_from_src_dst(self.current_node, next_node)
            if not road.is_blocked:
                self.current_node = next_node
                return road
        return None

class Q_Learning_Route(Route):
    def __init__(self, src_node: int, dst_node: int, road_network: Road_Network, start_time: datetime.datetime):

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
        full_tables_path = self.get_tables_directory(r"Q Tables Data")
        if self.agent.load_q_table(self.src_node, self.dst_node, full_tables_path):
            self.q_table = self.agent.get_q_table()
        else:
            self.q_table = self.agent.train_src_dst(src_node, dst_node, self.start_time, num_episodes, max_steps_per_episode=max_steps_per_episode)
            self.agent.save_q_table(self.src_node, self.dst_node, full_tables_path)
        # Test the agent
        test_reward, agent_path = self.agent.test_src_dst(src_node, dst_node, self.start_time)  # this will be the Test function
        self.path = agent_path

    def get_tables_directory(self, tables_directory):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, tables_directory)
        return data


    def decide_first_road(self):

        action = np.argmax(self.q_table[self.src_node]) # action is the index of the destination node in the q table
        dest_node = self.road_network.node_connectivity_dict[self.src_node][action]
        self.current_node = dest_node
        # road_index = self.road_network.road_dict[(self.src_node, dest_node)]
        return self.road_network.get_road_from_src_dst(self.src_node,dest_node)


    def get_next_road(self):
        action = np.argmax(self.q_table[self.current_node])  # action is the index of the destination node in the q table
        dest_node = self.road_network.node_connectivity_dict[self.current_node][action]
        next_road = self.road_network.get_road_from_src_dst(self.current_node, dest_node)
        self.current_node = dest_node
        return next_road




    def get_alt_road(self):
        action = np.argmax(self.q_table[self.current_node])  # action is the index of the destination node in the q table
        dest_node = self.road_network.node_connectivity_dict[self.current_node][action]
        next_road = self.road_network.get_road_from_src_dst(self.current_node, dest_node)
        while next_road.is_blocked:
            valid_actions = [a for a in range(len(self.q_table[self.current_node])) if a != action]

            if not valid_actions:
                return None

            second_best_action = np.argmax([self.q_table[self.current_node][a] for a in valid_actions])
            action = valid_actions[second_best_action]
            dest_node = self.road_network.node_connectivity_dict[self.current_node][action]
            next_road = self.road_network.get_road_from_src_dst(self.current_node, dest_node)

        self.current_node = dest_node
        return next_road

class Shortest_path_route(Route):
    def __init__(self, src_node: int, dst_node: int, road_network: Road_Network):

        self.src_node = src_node
        self.dst_node = dst_node
        # current node changes during the run, it represents the current's road destination node
        self.current_node = src_node
        self.road_network = road_network

    def decide_first_road(self):
        if self.src_node == self.dst_node:
            return None
        first_road = self.road_network.get_next_road_shortest_path(self.src_node, self.dst_node)
        self.current_node = first_road.destination_node.id
        return first_road


    def get_next_road(self):
        # TODO: update according to distance matrix implementation
        if self.current_node == self.dst_node:
            return None
        next_road = self.road_network.get_next_road_shortest_path(self.current_node, self.dst_node)
        self.current_node = next_road.destination_node.id
        return next_road

    def get_alt_road(self):
        adjacency_list = self.road_network.node_connectivity_dict[self.current_node]  # list of all the adjacent nodes ids
        for next_node in adjacency_list:
            road = self.road_network.get_road_from_src_dst(self.current_node, next_node) # this is "road"
            if not road.is_blocked:
                # if the road is not blocked, we check if the any road on the shortest path is blocked
                # if not, we return the road
                if self.road_network.get_shortest_path(next_node, self.dst_node) is not None:
                    self.current_node = next_node
                    return road
                pass
        return None