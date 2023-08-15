import copy
import datetime
import os
import pickle
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from geopy.distance import great_circle
from tqdm import tqdm

from Main_Files.Road_Network import Road_Network
from Q_Learning_Classes import Q_Agent
from Utilities.Results import plot_results


class Q_Learning:
    """
    A Q-learning algorithm implementation for route optimization in a road network.

    Attributes:

        road_network (Road_Network): The road network for which the Q-learning algorithm is applied.
        node_list (list): A list of lists representing the nodes connectivity in the road network.
        simulation_time (datetime): The current simulation time.
        learning_rate (float): The learning rate for updating Q-values.
        discount_factor (float): The discount factor for future rewards in Q-learning.
        epsilon (float): The exploration-exploitation trade-off factor.
        q_table (dict): A dictionary representing the Q-table.
        rewards (list): A list of rewards received in each episode.
        blocked (bool): A flag indicating whether the agent is blocked.
        finished (bool): A flag indicating whether the agent has reached its destination.




    """
    def __init__(self, road_network, cars, num_episodes = 1000, max_steps_per_episode = 100, learning_rate=0.05, discount_factor=0.9, epsilon=0.2):
        """
        Initialize the Q_Learning class.

        Args:
            road_network (Road_Network): The road network for which the Q-learning algorithm is applied.
            learning_rate (float): The learning rate for updating Q-values.
            discount_factor (float): The discount factor for future rewards in Q-learning.
            epsilon (float): The exploration-exploitation trade-off factor.

        Returns:
            None
        """
        # General
        self.road_network = road_network
        self.node_list = self.road_network.node_connectivity_dict

        # Train and Test
        self.simulation_time = None # datetime object
        self.cars_list = cars # list of cars
        self.agent_list = [] # list of agents
        self.last_node_times = [] # will store the time from the last node to the destination

        # Q Learning Parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.max_steps_per_episode = max_steps_per_episode

        # Q Learning Variables
        # self.q_table = self.initialize_q_table()
        self.rewards = []

        # Flags
        self.blocked = False
        self.finished = False

    # def initialize_q_table(self):
    #     """
    #     Initialize the Q-values table.
    #
    #     Returns:
    #         list: A list of lists representing Q-values for state-action pairs.
    #     """
    #     q_values = []
    #     for i in range(len(self.road_network.nodes_array)):
    #         row_values = []
    #         if self.node_list.get(i) is None:
    #             q_values.append([])
    #             continue
    #         for j in range(len(self.node_list[i])):
    #             row_values.append(0)
    #         q_values.append(row_values)
    #     return q_values
    #
    # def choose_action(self, state):
    #     """
    #     Choose an action based on the current state using an epsilon-greedy policy.
    #
    #     Args:
    #         state (int): The current state index.
    #
    #     Returns:
    #         int: The chosen action index.
    #     """
    #     # Epsilon-greedy policy to choose an action
    #     if np.random.rand() < self.epsilon:
    #         return np.random.choice(len(self.q_table[state]))
    #     else:
    #         if len(self.q_table[state]) == 0:
    #             print("No available actions")
    #         return np.argmax(self.q_table[state])  # Exploit by choosing the action with the highest Q-value

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



    def calculate_reward_basic(self, agent: Q_Agent, next_state, next_road):
        """
        THIS IS THE BASIC REWARD FUNCTION FOR THE Q-LEARNING ALGORITHM.
        ITS TRYING TO MINIMIZE THE NUMBER OF ROADS TAKEN TO REACH THE DESTINATION.

        Calculate the reward for a given action.
        :param agent:
        :param next_state:
        :param next_road:
        :return:
        """
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

    def calculate_reward(self, agent: Q_Agent, next_state, src, dst, next_road, blocked_roads):
        """
        Calculate the reward for a given action.

        Args:
            agent (Q_Agent): The Q_Agent instance.
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
        id = next_road.id

        if next_road.is_blocked or\
                (id in blocked_roads.keys() and blocked_roads[id][0] <= self.simulation_time <= blocked_roads[id][1]) or\
                len(self.q_table[next_state]) == 0:
            self.blocked = True
            return -1000

        if agent.dst == next_state:
            # High reward for reaching the destination
            self.finished = True
            return 1000
        else:
            # get the hour and minute of the current time
            if nx.has_path(self.road_network.nx_graph, next_state, dst):
                next_node_time = nx.shortest_path_length(self.road_network.nx_graph, next_state, dst, weight = 'eta') # time to destination from the next node
            else:
                # if there is no path to the destination
                return -1000

            if next_node_time < self.last_node_time:
                # if the agent is closer to the destination
                self.last_node_time = next_node_time
                return -1

            self.last_node_time = next_node_time
            # if the agent is not closer to the destination
            return -3

    def update_q_table(self, state, action, next_state, reward):
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
                max_next_q_value = np.max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value

    def save_q_table(self, agent, save_path):
        """
        Save the Q-value table to a file.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            save_path (str): The path to save the Q-value table.

        Returns:
            None
        """
        blocked_roads = self.road_network.blocked_roads_dict
        blocked_roads_str = '_blocked_roads'
        if blocked_roads:
            for block_road in blocked_roads:
                blocked_roads_str += '_' + str(block_road)
        else:
            blocked_roads_str = ''
        filename = os.path.join(save_path, f'q_table_{self.road_network.graph_name}_{agent.src}_{agent.dst}{blocked_roads_str}.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(agent.q_table, f)

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
        blocked_roads = self.road_network.blocked_roads_dict
        blocked_roads_str = '_blocked_roads'
        if blocked_roads:
            for block_road in blocked_roads.keys():
                blocked_roads_str += '_' + str(block_road)
        else:
            blocked_roads_str = ''

        filename = os.path.join(save_path, f'q_table_{self.road_network.graph_name}_{src}_{dst}{blocked_roads_str}.pkl')
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            # print(f"Q-table file '{filename}' not found.")
            return False

    def add_time_to_simulation_time(self, next_road):
        """
        Add the time to the simulation time.

        Args:
            next_road (Road): The next road to travel on.

        :return: Nne
        """
        rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
        time_obj = self.simulation_time.replace(minute=rounded_minutes, second=0, microsecond=0)
        time_str = time_obj.strftime("%H:%M")
        eta = float(next_road.get_eta(time_str))  # eta in seconds
        self.simulation_time += datetime.timedelta(seconds=eta)


    # train and test for one car
    def train(self, src: int, dst: int, start_time: datetime, num_episodes: int,  max_steps_per_episode=100, epsilon_decay_rate=0.9999, mean_rewards_interval=100, is_plot_results=True):
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
        print("*********************************************")
        print("          Training Started                   ")
        print(f"Source: {src}, Destination: {dst}")
        print("*********************************************")

        # creating an agent and calculating the shortest path
        agent = Q_Agent.Q_Agent(src, dst, start_time, self.road_network)
        blocked_roads = self.road_network.blocked_roads_dict

        all_training_paths_nodes = []
        all_training_times = []
        mean_rewards = []  # List to store mean rewards for every 10 episodes
        mean_reward_sum = 0  # Variable to keep track of the sum of rewards in the last 10 episodes

        for episode in range(num_episodes):
            # Initialize parameters to evaluate the episode
            self.last_node_time = nx.shortest_path_length(self.road_network.nx_graph, src, dst, weight='eta')  # time to dest from the current node
            self.simulation_time = start_time
            total_episode_reward = 0
            path_nodes = []
            path_roads = []


            # print("episode: ", episode)
            for step in range(max_steps_per_episode):
                if agent.num_of_steps == 0:
                    # agent starting now
                    state = agent.src
                    path_nodes.append(state)
                else:
                    # agent is already on the road
                    state = agent.current_road.destination_node.id

                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                next_state = next_road.destination_node.id

                # Calculate the rounded minutes
                # rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
                # time_obj = self.simulation_time.replace(minute=rounded_minutes,second=0, microsecond=0)
                # time_str = time_obj.strftime("%H:%M")
                # eta = float(next_road.get_eta(time_str)) # eta in seconds
                # self.simulation_time += datetime.timedelta(seconds=eta)
                self.add_time_to_simulation_time(next_road)
                reward = self.calculate_reward(agent, next_state, src, dst, next_road, blocked_roads)


                path_roads.append(next_road.id)
                path_nodes.append(next_road.destination_node.id)

                total_episode_reward += reward
                self.update_q_table(state, action, next_state, reward)

                if self.finished:
                    # print("agent reached destination")
                    break

                if self.blocked:  # agent is blocked
                    # print("agent is blocked")
                    break

                agent.current_road = next_road
                agent.num_of_steps += 1
                if agent.num_of_steps >= max_steps_per_episode:
                    break

            self.rewards.append(total_episode_reward)
            # Calculate mean reward after every {mean_rewards_interval} episodes
            mean_reward_sum += total_episode_reward

            if episode % mean_rewards_interval == 0:
                print("episode: ", episode)
                # print("path nodes: ", path_nodes)
                # # print("path roads: ", path_roads)
                print("total episode reward: ", total_episode_reward)
                mean_reward = mean_reward_sum / mean_rewards_interval
                mean_rewards.append(mean_reward)
                # if mean_reward > 960:
                #     # print("mean reward: ", mean_reward)
                #     print("convrged after ", episode, " episodes")
                mean_reward_sum = 0  # Reset the sum for the next mean_rewards_interval episodes

            self.blocked = False
            self.finished = False
            all_training_paths_nodes.append(copy.deepcopy(path_nodes))
            all_training_times.append(int((self.simulation_time-start_time).total_seconds()))
            path_roads.clear()
            path_nodes.clear()
            self.epsilon *= epsilon_decay_rate


        print("*********************************************")
        print("          Training Finished                  ")
        print("*********************************************")

        # Plot mean rewards
        if is_plot_results:
            plot_results(src, dst, all_training_paths_nodes, all_training_times, mean_rewards)
        return self.q_table

    def test(self, src: int, dst: int, start_time:datetime, max_steps_per_episode=100):
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
        self.finished = False
        self.blocked = False
        self.simulation_time = start_time

        agent = Q_Agent.Q_Agent(src, dst, datetime.datetime.now(), self.road_network)

        blocked_roads = self.road_network.blocked_roads_dict
        self.last_node_time = nx.shortest_path_length(self.road_network.nx_graph, src, dst, weight='eta')  # time to dest from the current node

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

            self.add_time_to_simulation_time(next_road)

            reward = self.calculate_reward(agent, next_state, src, dst, next_road, blocked_roads)

            path_roads.append(next_road.id)
            path_nodes.append(next_road.destination_node.id)
            # path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network),self.road_network)

            test_rewards += reward

            if self.blocked:
                print("agent is blocked!")
                break
            elif self.finished:
                print("agent reached the destination!")
                break

            state = next_state
            if state == agent.dst:
                # print("agent reached destination")
                break

        print(f"Test reward: {test_rewards:.2f}")
        return test_rewards, path_nodes

    # for many cars
    def train_cars(self, start_time: datetime, epsilon_decay_rate=0.99, mean_rewards_interval=100, is_plot_results=True):
        """
        Train the Q-learning agent for a source-destination pair.

        Args:
            src (int): The source node index.
            dst (int): The destination node index.
            start_time (datetime): The start time of the simulation.
            epsilon_decay_rate (float): The rate of epsilon decay.
            mean_rewards_interval (int): The interval to calculate mean rewards.

        Returns:
            list: The Q-value table after training.
        """
        print("*********************************************")
        print("          Training Started                   ")
        print("*********************************************")
        # agents = []
        # creating an agent and calculating the shortest path
        for car in self.cars_list:
            self.agent_list.append(Q_Agent.Q_Agent(car.source_node, car.destination_node, start_time, self.road_network))
            self.agent_list[-1].initialize_q_table()

        blocked_roads = self.road_network.blocked_roads_dict
        for episode in tqdm(range(self.num_episodes), desc="Episodes", unit="episode"):

            # print("episode: ", episode)

            # Initialize parameters to evaluate the episode
            # for agent in self.agent_list:
            #     inital_eta = nx.shortest_path_length(self.road_network.nx_graph, agent.src, agent.dst, weight='eta')  # time to dest from the current node
            #     agent.last_node_time = inital_eta

            for step in range(self.max_steps_per_episode): # every car can take max_steps_per_episode steps

                # Initialize a flag to check if all agents are done
                all_agents_done = True

                for agent in self.agent_list:
                    if not (agent.finished or agent.blocked):
                        all_agents_done = False
                        break  # No need to check further if we found an active agent

                if all_agents_done:
                    # print("All agents are either finished or blocked.")
                    break  # Exit the episode loop

                for i, agent in enumerate(self.agent_list):

                    # for every agent we need to update the state, action, next_state, reward
                    if agent.finished or agent.blocked:
                        # print(f"agent {i} reached destination or blocked!")
                        continue

                    # print("agent: ", i)
                    if agent.num_of_steps == 0:
                        # agent starting now
                        agent.current_state = agent.src
                        agent.path_nodes.append(agent.current_state)
                    else:
                        # agent is already on the road
                        agent.current_state = agent.current_road.destination_node.id

                    action, next_road, next_state = agent.step(self.epsilon)

                    # calculate the simulation time for the agent
                    agent.add_time_to_simulation_time()
                    # calculate the reward
                    reward = agent.calculate_reward_basic(next_state, agent.src, agent.dst, next_road, blocked_roads)

                    # update the agent's path
                    agent.path_roads.append(next_road.id)
                    agent.path_nodes.append(next_road.destination_node.id)

                    agent.total_episode_reward += reward
                    agent.update_q_table(reward, self.learning_rate, self.discount_factor)

                    agent.current_road = agent.next_road
                    agent.num_of_steps += 1
                    if agent.num_of_steps >= self.max_steps_per_episode:
                        agent.reached_destinations.append(False)
                        agent.is_blocked = True
                        continue


            # agent.rewards.append(total_episode_reward)
            # Calculate mean reward after every {mean_rewards_interval} episodes

            for agent in self.agent_list:
                # end of episode, we need to update the agent and get him ready for the next episode
                agent.reset()

            self.epsilon *= epsilon_decay_rate


        print("*********************************************")
        print("          Training Finished                  ")
        print("*********************************************")

        # Plot mean rewards
        if is_plot_results:
            for agent in self.agent_list:
                plot_results(agent.src, agent.dst, agent.all_training_paths_nodes, agent.all_training_times, agent.mean_rewards)
                self.save_q_table(agent,self.get_tables_directory())

    def get_tables_directory(self):
        tables_directory = "Q Tables Data"
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        path = os.path.join(parent, tables_directory)
        return path