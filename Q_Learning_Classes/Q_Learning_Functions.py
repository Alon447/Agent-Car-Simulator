import copy
import datetime
import os
import pickle
import matplotlib.patches as mpatches

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from geopy.distance import great_circle

from Main_Files.Road_Network import Road_Network
from Q_Learning_Classes import Q_Agent
from Utilities.Getters import node_route_to_osm_route


class QLearning:
    """
    A Q-learning algorithm implementation for route optimization in a road network.

    Attributes:

        road_network (Road_Network): The road network for which the Q-learning algorithm is applied.

        learning_rate (float): The learning rate for updating Q-values.

        discount_factor (float): The discount factor for future rewards in Q-learning.

        epsilon (float): The exploration-exploitation trade-off factor.

        node_list (dict): Dictionary of node connectivity for available actions.

        q_table (list): A list of Q-values for state-action pairs.

        rewards (list): List to store the rewards during training.

        simulation_time (int): The simulation time in seconds.
    """
    def __init__(self, road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.2):
        """
        Initialize the QLearning class.

        Args:
            road_network (Road_Network): The road network for which the Q-learning algorithm is applied.
            learning_rate (float): The learning rate for updating Q-values.
            discount_factor (float): The discount factor for future rewards in Q-learning.
            epsilon (float): The exploration-exploitation trade-off factor.

        Returns:
            None
        """
        self.road_network = road_network
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.node_list = self.road_network.node_connectivity_dict
        self.q_table = self.initialize_q_table()
        self.rewards = []
        self.simulation_time = 0

    def initialize_q_table(self):
        """
        Initialize the Q-values table.

        Returns:
            list: A list of lists representing Q-values for state-action pairs.
        """
        q_values = []
        for i in range(len(self.road_network.nodes_array)):
            row_values = []
            if self.node_list.get(i) is None:
                q_values.append([])
                continue
            for j in range(len(self.node_list[i])):
                row_values.append(0)
            q_values.append(row_values)
        return q_values

    def calculate_route_eta(self, route, road_network):
        """
        Calculate the estimated time of arrival for a given route.

        Args:
            route (list): A list of roads in the route.
            road_network (Road_Network): The road network.

        Returns:
            float: Estimated time of arrival (ETA) for the given route.
        """
        eta = 0
        for i in range(len(route) - 1):
            src = route[i]
            j = i + 1
            dst = route[j]
            eta += float(road_network.nx_graph[src][dst][0].get('eta'))
        return eta


    def choose_action(self, state):
        """
        Choose an action based on the current state using an epsilon-greedy policy.

        Args:
            state (int): The current state index.

        Returns:
            int: The chosen action index.
        """
        # Epsilon-greedy policy to choose an action
        if np.random.rand() < self.epsilon:
            return np.random.choice(len(self.q_table[state]))
        else:
            return np.argmax(self.q_table[state])  # Exploit by choosing the action with the highest Q-value

    def get_next_road(self, src_node, action):
        """
        Get the next road to travel based on the chosen action.

        Args:
        src_node (int): The source node index.
        action (int): The chosen action index.

        Returns:
        Road: The next road to travel.
        """

        dest_node = self.node_list[src_node][action]
        return self.road_network.get_road_from_src_dst(src_node,dest_node)



    def update_state(self, q_agent: Q_Agent, next_road):
        """
        Update the state of the Q-Agent after taking an action.

        Args:
            q_agent (Q_Agent): The Q_Agent instance.
            next_road (Road): The next road taken.

        Returns:
            None
        """
        q_agent.current_road = next_road
        return

    def calculate_distance(self, src:int, dst:int):
        """
        Calculate the distance between two nodes using their coordinates.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.

        Returns:
            float: The distance between the two nodes.
        """
        point_src = (self.road_network.nodes_array[src].y,self.road_network.nodes_array[src].x)
        point_dst = (self.road_network.nodes_array[dst].y,self.road_network.nodes_array[dst].x)
        distance = great_circle(point_src, point_dst)
        return distance

    def calculate_reward_basic(self, agent: Q_Agent, next_state, next_road):
        if next_road.is_blocked:
            return -100
        if agent.dst == next_state:
            # High reward for reaching the destination
            return 1000
        elif len(self.q_table[next_state]) == 0:
            # Penalty for getting blocked
            return -100
        else:
            return -1

    def calculate_reward(self, agent: Q_Agent, next_state, src, dst, next_road, eta, path_nodes, delta_time):
        """
        Calculate the reward for a given action.

        Args:
            agent (Q_Agent): The Q_Agent instance.
            next_state (int): The next state index.
            src (int): The source node index.
            dst (int): The destination node index.
            eta (float): The estimated time of arrival for the next action.
            path_nodes (list): The list of nodes in the path.
            delta_time (float): The difference in travel time compared to the shortest path.

        Returns:
            float: The calculated reward.
        """
        # Calculate the reward based on the agent's progress and other factors
        src_dst_distance = self.calculate_distance(src, dst)
        next_state_dst_distance = self.calculate_distance(next_state, dst)
        distance_delta = src_dst_distance - next_state_dst_distance # positive if the agent is closer to the destination
        if next_road.is_blocked:
            return -100
        if agent.dst == next_state:
            # High reward for reaching the destination

            return 1000
        elif len(self.q_table[next_state]) == 0:
            # Penalty for getting blocked
            return -100
        else:
            # if next_state in path_nodes:
            #     return -1000
            # elif distance_delta < 0:
            #     return -1
            # else:
            if distance_delta < 0:
                return -2
            return -1

    def update_q_table(self, state, action, next_state, reward, eta):
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
        current_q_value = self.q_table[state][action]
        if reward == -100:
            max_next_q_value = -100
        else:
            if len(self.q_table[next_state]) == 0:
                max_next_q_value = 0
            else:
                max_next_q_value = np.max(self.q_table[next_state])  #
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value

    def plot_rewards(self, var:list):
        """
        Plot the mean rewards over training episodes.

        Args:
            var (list): List of mean rewards.

        Returns:
            None
        """
        plt.plot(range(1, len(var) + 1), var)
        plt.xlabel('Interval (Every 10 Episodes)')
        plt.ylabel('Mean Episode Reward')
        plt.title('Mean Rewards over Training')
        plt.show()



    def save_q_table(self, src, dst, save_path):
        """
        Save the Q-value table to a file.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            save_path (str): The path to save the Q-value table.

        Returns:
            None
        """
        blocked_roads = self.road_network.blocked_roads_array
        blocked_roads_str = 'blcoked_roads'
        if blocked_roads:
            for block_road in blocked_roads:
                blocked_roads_str += '_' + str(block_road)
        else:
            blocked_roads_str = ''
        filename = os.path.join(save_path, f'q_table_{src}_{dst}{blocked_roads_str}.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, src, dst, save_path):
        """
        Load the Q-value table from a file.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            save_path (str): The path to load the Q-value table.

        Returns:
            bool: True if Q-value table was loaded successfully, False if the file was not found.
        """
        blocked_roads = self.road_network.blocked_roads_array
        blocked_roads_str = 'blcoked_roads'
        if blocked_roads:
            for block_road in blocked_roads:
                blocked_roads_str += '_' + str(block_road)
        else:
            blocked_roads_str = ''

        filename = os.path.join(save_path, f'q_table_{src}_{dst}{blocked_roads_str}.pkl')
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            # print(f"Q-table file '{filename}' not found.")
            return False


    # functions for the Route class, gets src and dst instead of agent
    def train_src_dst(self, src: int, dst: int, start_time:datetime, num_episodes: int,  max_steps_per_episode=100, epsilon_decay_rate=0.99, mean_rewards_interval=100, plot_results=True):
        """
        Train the Q-learning agent for a source-destination pair.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            start_time (datetime): The start time of the simulation.
            num_episodes (int): The number of training episodes.
            max_steps_per_episode (int): The maximum number of steps per episode.
            epsilon_decay_rate (float): The rate of epsilon decay.
            mean_rewards_interval (int): The interval to calculate mean rewards.

        Returns:
            list: The Q-value table after training.
        """
        # print("*********************************************")
        # print("          Training Started                   ")
        # print("*********************************************")

        # creating an agent and calculating the shortest path
        agent = Q_Agent.Q_Agent(src, dst, start_time, self.road_network)
        src_osm = self.road_network.nodes_array[src].osm_id
        dst_osm = self.road_network.nodes_array[dst].osm_id
        path = nx.shortest_path(self.road_network.graph, src_osm, dst_osm, weight='length')
        # shortest_path_time = self.calculate_route_eta(path, self.road_network)
        shortest_path_time = 0

        all_training_paths_nodes = []
        all_training_times = []
        mean_rewards = []  # List to store mean rewards for every 10 episodes
        mean_reward_sum = 0  # Variable to keep track of the sum of rewards in the last 10 episodes

        for episode in range(num_episodes):
            # Initialize parameters to evaluate the episode
            self.simulation_time = start_time
            total_episode_reward = 0
            path_nodes = []
            path_roads = []


            # print("episode: ", episode)
            for step in range(max_steps_per_episode):
                if step == 0:
                    # agent starting now
                    state = agent.src
                    path_nodes.append(state)
                else:
                    # agent is already on the road
                    state = agent.current_road.destination_node.id


                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                if next_road.is_blocked:
                    print("blocked road")
                next_state = next_road.destination_node.id
                # Calculate the rounded minutes
                rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
                time_obj = self.simulation_time.replace(minute=rounded_minutes,second=0, microsecond=0)
                time_str = time_obj.strftime("%H:%M")

                eta = float(next_road.get_eta(time_str)) # eta in seconds
                self.simulation_time += datetime.timedelta(seconds=eta)
                drive_time = (self.simulation_time - start_time).total_seconds() # drive time in seconds of the agent
                delta_time = drive_time - shortest_path_time  # positive if the agent is slower than the shortest path

                reward = self.calculate_reward(agent, next_state, src, dst, next_road, eta, path_nodes, delta_time)

                path_roads.append(next_road.id)
                path_nodes.append(next_road.destination_node.id)
                # path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network), self.road_network)
                # delta_time = path_time - shortest_path_time # positive if the agent is slower than the shortest path

                total_episode_reward += reward
                self.update_q_table(state, action, next_state, reward, eta)
                # print("simulation time: ", self.simulation_time)


                if next_state == agent.dst:
                    # print("agent reached destination")
                    break

                if reward == -100:  # agent is blocked
                    # print("agent is blocked")
                    break
                self.update_state(agent, next_road)

            self.rewards.append(total_episode_reward)
            # Calculate mean reward after every 10 episodes
            mean_reward_sum += total_episode_reward

            if episode % mean_rewards_interval == 0:
                # print("episode: ", episode)
                # print("path nodes: ", path_nodes)
                # # print("path roads: ", path_roads)
                # print("total episode reward: ", total_episode_reward)
                mean_reward = mean_reward_sum / mean_rewards_interval
                mean_rewards.append(mean_reward)
                if mean_reward > 960:
                    # print("mean reward: ", mean_reward)
                    print("convrged after ", episode, " episodes")
                #     break
                mean_reward_sum = 0  # Reset the sum for the next 10 episodes
            all_training_paths_nodes.append(copy.deepcopy(path_nodes))
            all_training_times.append(int((self.simulation_time-start_time).total_seconds()))
            path_roads.clear()
            path_nodes.clear()
            self.epsilon *= epsilon_decay_rate
        #
        # print("*********************************************")
        # print("          Training Finished                  ")
        # # print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")

        # Plot mean rewards
        if plot_results:
            self.car_times_bar_chart(dst, all_training_paths_nodes, all_training_times)
            self.plot_rewards(mean_rewards)
        return self.q_table

    def test_src_dst(self, src: int, dst: int, start_time:datetime, max_steps_per_episode=100):
        """
        Test the trained Q-learning agent for a source-destination pair.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            start_time (datetime): The start time of the simulation.
            max_steps_per_episode (int): The maximum number of steps per episode.

        Returns:
            Tuple[float, list]: A tuple containing the total test reward and a list of visited nodes during testing.
        """
        self.simulation_time = start_time

        agent = Q_Agent.Q_Agent(src, dst, datetime.datetime.now(), self.road_network)
        src_osm = self.road_network.nodes_array[src].osm_id
        dst_osm = self.road_network.nodes_array[dst].osm_id
        path = nx.shortest_path(self.road_network.graph, src_osm, dst_osm, weight='length')
        # shortest_path_time = self.calculate_route_eta(path, self.road_network)
        shortest_path_time = 0
        # print("*********************************************")
        # print("          Testing Started                    ")
        print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")



        test_rewards = 0
        path_nodes = [src]
        path_roads = []
        state = agent.src
        for step in range(max_steps_per_episode):
            action = np.argmax(self.q_table[state])
            next_road = self.get_next_road(state, action)
            next_state = next_road.destination_node.id
            # Calculate the rounded minutes
            rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
            time_obj = self.simulation_time.replace(minute=rounded_minutes, second=0, microsecond=0)
            time_str = time_obj.strftime("%H:%M")
            eta = float(next_road.get_eta(time_str))  # eta in seconds
            self.simulation_time += datetime.timedelta(seconds=eta)
            drive_time = (self.simulation_time - start_time).total_seconds()
            delta_time = drive_time - shortest_path_time  # positive if the agent is slower than the shortest path
            reward = self.calculate_reward(agent, next_state, src, dst, next_road, eta, path_nodes, delta_time)

            path_roads.append(next_road.id)
            path_nodes.append(next_road.destination_node.id)
            # path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network),self.road_network)

            test_rewards += reward
            # path_roads.append(next_road.get_id())
            # path_nodes.append(next_road.destination_node[0])
            # print("path nodes: ", path_nodes)
            if reward == -100 or reward == 1000:  # agent is blocked or reached destination
                if reward == -100:
                    print("agent is blocked!")
                else:
                    print("agent reached the destination!")
                break

            state = next_state
            if state == agent.dst:
                # print("agent reached destination")
                break
        # print("path nodes: ", path_nodes)
        # print("path roads: ", path_roads)
        print(f"Test reward: {test_rewards:.2f}")
        # print("*********************************************")
        return test_rewards, path_nodes

    def get_q_table(self):
        """
        Get the current Q-value table.

        Returns:
            list: The current Q-value table.
        """
        return self.q_table

    def car_times_bar_chart(self, dst, all_training_paths_nodes, all_training_times):

        colors = []

        for path in all_training_paths_nodes:
            if path[-1] == dst:
                colors.append('green')
            else:
                colors.append('red')
        # time_seconds = [td.total_seconds() for td in times]
        plt.bar((range(1, len(all_training_times) + 1)), all_training_times, color=colors)

        # Add labels and title
        plt.xlabel('Simulation Number')
        plt.ylabel('Time taken [seconds] by Q Agent')
        plt.title('Bar Chart: Times of Q Agent {} in Simulation')
        legend_labels = ['Reached Destination', 'Not Reached Destination']
        legend_colors = ['green', 'red']
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in
                          zip(legend_colors, legend_labels)]

        plt.legend(handles=legend_patches, title='Legend', loc='upper right')

        plt.show()
