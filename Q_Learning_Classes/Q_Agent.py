import copy
import datetime

import networkx as nx
import numpy as np

from Main_Files.Road_Network import Road_Network
class Q_Agent:
    def __init__(self, src: int, dst: int, start_time: datetime, road_network: Road_Network):

        # General parameters
        self.src = src
        self.dst = dst
        self.road_network = road_network
        self.node_list = self.road_network.node_connectivity_dict
        self.start_time = start_time
        self.simulation_time = start_time

        # Q-learning parameters
        self.q_table = None


        # During simulation parameters
        self.current_road = None
        self.next_road = None
        self.num_of_steps = 0
        self.current_state = None
        self.next_state = None
        self.action = None
        self.current_reward = None

        # Path time parameters
        self.last_node_time = None
        self.next_node_time = None

        # Path saving parameters
        self.path_nodes = []
        self.path_roads = []

        # Flags
        self.blocked = False
        self.finished = False

        # results
        self.total_episode_reward = 0
        self.all_training_times = []
        self.all_training_paths_nodes = []
        self.reached_destinations = []
        self.total_reward = 0
        self.rewards = []
        self.mean_rewards = []

    def initialize_q_table(self):
        """
        Initialize the Q-values table.


        """
        self.q_table = []
        for i in range(len(self.road_network.nodes_array)):
            row_values = []
            if self.node_list.get(i) is None:
                self.q_table.append([])
                continue
            for j in range(len(self.node_list[i])):
                row_values.append(0)
            self.q_table.append(row_values)
        return

    def choose_action(self, epsilon):
        """
        Choose an action based on the current state using an epsilon-greedy policy.

        Args:
            state (int): The current state index.

        Returns:
            int: The chosen action index.
        """
        # Epsilon-greedy policy to choose an action
        if np.random.rand() < epsilon:
            return np.random.choice(len(self.q_table[self.current_state]))
        else:
            if len(self.q_table[self.current_state]) == 0:
                print("No available actions")
            return np.argmax(self.q_table[self.current_state])  # Exploit by choosing the action with the highest Q-value

    def get_next_road(self):
        """
        Get the next road to travel based on the chosen action.

        Args:
        src_node (int): The source node index.
        action (int): The chosen action index.

        Returns:
        Road: The next road to travel.
        """

        dest_node = self.node_list[self.current_state][self.action]
        self.next_road = self.road_network.get_road_from_src_dst(self.current_state,dest_node)

    def step(self, epsilon):
        self.action = self.choose_action(epsilon)
        self.get_next_road()
        self.next_state = self.next_road.destination_node.id
        return self.action, self.next_road, self.next_state
    def calculate_reward(self, next_state, src, dst, next_road, blocked_roads):
        """
        Calculate the reward for a given action.

        Args:
            next_state (int): The next node id.
            src (int): The inital source node index.
            dst (int): The final destination node index.
            eta (float): The estimated time of arrival for the next action.
            path_nodes (list): The list of nodes in the path.
            delta_time (float): The difference in travel time compared to the shortest path.

        Returns:
            float: The calculated reward.
        """
        # Calculate the reward based on the agent's progress and other factors
        id = self.next_road.id

        if self.next_road.is_blocked or\
                (id in blocked_roads.keys() and blocked_roads[id][0] <= self.simulation_time <= blocked_roads[id][1]) or\
                len(self.q_table[next_state]) == 0:
            self.blocked = True
            return -1000

        if self.dst == self.next_state:
            # High reward for reaching the destination
            self.finished = True
            return 1000

        else:
            # get the hour and minute of the current time
            # if nx.has_path(self.road_network.nx_graph, self.next_state, self.dst):
            #     self.next_node_time = nx.shortest_path_length(self.road_network.nx_graph, next_state, dst, weight = 'eta') # time to destination from the next node
            # else:
            #     # if there is no path to the destination
            #     return -1000
            #
            # if self.next_node_time < self.last_node_time:
            #     # if the agent is closer to the destination
            #     self.last_node_time = self.next_node_time
            return -1

            # self.last_node_time = self.next_node_time
            # if the agent is not closer to the destination
            # return -3

    def update_q_table(self, reward, learning_rate, discount_factor):
        """
        Update the Q-value table based on the Q-learning update rule.

        Args:
            state (int): The current state index.
            action (int): The chosen action index.
            next_state (int): The next state index.
            reward (float): The reward received from the action.
            eta (float): The estimated time of arrival for the next action.

        Returns:
            None
        """
        # Q-learning update rule
        current_q_value = self.q_table[self.current_state][self.action]
        if self.blocked:
            max_next_q_value = -1000
        else:
            if len(self.q_table[self.next_state]) == 0:
                max_next_q_value = -1000
            else:
                max_next_q_value = np.max(self.q_table[self.next_state])
        new_q_value = (1 - learning_rate) * current_q_value + learning_rate * (reward + discount_factor * max_next_q_value)
        self.q_table[self.current_state][self.action] = new_q_value

    def add_time_to_simulation_time(self):
        """
        Add the time to the simulation time.

        Args:
            next_road (Road): The next road to travel on.

        :return: Nne
        """
        rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
        time_obj = self.simulation_time.replace(minute=rounded_minutes, second=0, microsecond=0)
        time_str = time_obj.strftime("%H:%M")
        eta = float(self.next_road.get_eta(time_str))  # eta in seconds
        self.simulation_time += datetime.timedelta(seconds=eta)

    def reset(self):
        self.blocked = False
        self.finished = False
        self.rewards.append(self.total_episode_reward)
        if len(self.rewards) % 50 == 0:
            self.mean_rewards.append(np.mean(self.rewards[-10:]))
        self.all_training_paths_nodes.append(copy.deepcopy(self.path_nodes))
        self.all_training_times.append((self.simulation_time - self.start_time).total_seconds())
        self.simulation_time = self.start_time
        self.path_roads.clear()
        self.path_nodes.clear()
        self.num_of_steps = 0

        self.total_episode_reward = 0
        self.current_road = None
        self.next_road = None
        self.current_state = None
        self.next_state = None
        self.last_node_time = None