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
        self.node_list = self.road_network.node_connectivity_dict # list of lists representing the nodes connectivity in the road network.
        self.start_time = start_time
        self.simulation_time = start_time # The current simulation time.
        self.end_time = None # The end time of the simulation.

        # Q-learning parameters
        self.q_table = None # A list of lists representing the Q-table.

        # During simulation parameters
        self.current_road = None # The current road the agent is on.
        self.next_road = None # The next road the agent will travel on.
        self.num_of_steps = 0 # The number of steps the agent has taken.
        # self.visited_nodes = [self.src] # A list of visited nodes.
        # nodes
        self.current_state = None # The current node id.
        self.next_state = None # The next node id that the agent will go to.
        self.action = None # The chosen action index.

        # Path time parameters
        self.last_node_time = None # The time to destination from the last node.
        self.next_node_time = None # The time to destination from the next node.

        # Path saving parameters
        self.path_nodes = [] # The list of nodes in the path.
        self.path_roads = [] # The list of roads in the path.

        # Flags
        self.blocked = False # A flag indicating whether the agent is blocked.
        self.finished = False # A flag indicating whether the agent has reached its destination.

        # results
        self.total_episode_reward = 0 # The total reward received in the current episode.
        self.all_training_times = [] # A list of the total time for each episode.
        self.all_training_paths_nodes = [] # A list of lists of the nodes in the path for each episode.
        self.reached_destinations = [] # A list of booleans indicating whether the agent reached its destination in each episode.
        self.total_reward = 0 # The total reward received in all episodes.
        self.rewards = [] # A list of rewards received in each episode.
        self.mean_rewards = [] # A list of the mean rewards received in the last 10 episodes.

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
            epsilon (float): The epsilon value.

        Returns:
            int: The chosen action index.
        """
        # Epsilon-greedy policy to choose an action
        if np.random.rand() < epsilon:
            return np.random.choice(len(self.q_table[self.current_state]))
        else:
            if len(self.q_table[self.current_state]) == 0:
                print("No available actions")
                self.blocked = True
            else:
                return np.argmax(self.q_table[self.current_state])  # Exploit by choosing the action with the highest Q-value

    def get_next_road(self):
        """
        Get the next road to travel based on the chosen action.

        Returns:
        Road: The next road to travel.
        """

        dest_node = self.node_list[self.current_state][self.action]
        self.next_road = self.road_network.get_road_from_src_dst(self.current_state,dest_node)

        return self.next_road

    def update_q_table(self, reward, learning_rate, discount_factor):
        """
        Update the Q-value table based on the Q-learning update rule.

        Args:
            reward (float): The reward received for the current action.
            learning_rate (float): The learning rate.
            discount_factor (float): The discount factor.

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
        return

    def add_time_to_simulation_time(self):
        """
        Adds the time of the next road to the simulation time.


        :return: Nne
        """
        rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
        time_obj = self.simulation_time.replace(minute=rounded_minutes, second=0, microsecond=0)
        time_str = time_obj.strftime("%H:%M")
        eta = float(self.next_road.get_eta(time_str))  # eta in seconds
        self.simulation_time += datetime.timedelta(seconds=eta)
        return

    def update_state(self):
        """
        Update the current state to the next state.

        Args:
            next_state (int): The next state index.

        Returns:
            None
        """
        if self.num_of_steps == 0:
            # agent starting now
            self.current_state = self.src
            self.path_nodes.append(self.current_state)
        else:
            # agent is already on the road
            self.current_state = self.current_road.destination_node.id
        return

    def update_path(self):
        """
        Update the paths with the next road and the next state (aka next node).


        Returns:
            None
        """
        self.path_roads.append(self.next_road.id)
        self.path_nodes.append(self.next_state)
        return

    def move_to_next_road(self, max_steps_per_episode):
        """
        Move the agent to the next road.

        Args:
            max_steps_per_episode (int): The maximum number of steps per episode.

        Returns:
            None
        """
        self.current_road = self.next_road
        self.num_of_steps += 1
        if self.num_of_steps >= max_steps_per_episode:
            self.reached_destinations.append(False)
            self.blocked = True
        return

    def step(self, epsilon):
        """
        Perform one step in the simulation.
        Uses the epsilon-greedy policy to choose an action, and then updates the state, action, next_state.
        Adds the time to the simulation time.
        Updates the path with the next road.

        :param epsilon (float): The epsilon value.
        :return: (int,Road, int): The chosen action, the next road, the next state.
        """
        self.update_state()
        self.action = self.choose_action(epsilon)
        self.get_next_road()
        self.next_state = self.next_road.destination_node.id
        self.add_time_to_simulation_time()
        self.update_path()
        return self.action, self.next_road, self.next_state

    def calculate_reward(self, blocked_roads):
        """
        Calculate the reward for a given action.

        Args:
            blocked_roads (dict): A dictionary of blocked roads and their blockage times.

        Returns:
            float: The calculated reward.
        """
        # Calculate the reward based on the agent's progress and other factors
        id = self.next_road.id

        if self.next_road.is_blocked or\
                (id in blocked_roads.keys() and blocked_roads[id][0] <= self.simulation_time <= blocked_roads[id][1]) or\
                len(self.q_table[self.next_state]) == 0:
            self.blocked = True
            return -1000

        if self.dst == self.next_state:
            # High reward for reaching the destination
            self.finished = True
            if self.end_time is None:
                self.end_time = self.simulation_time
            else:
                self.end_time = min(self.end_time, self.simulation_time)
            return 1000

        else:
            # get the hour and minute of the current time
            if nx.has_path(self.road_network.nx_graph, self.next_state, self.dst):
                self.next_node_time = nx.shortest_path_length(self.road_network.nx_graph, self.next_state, self.dst, weight = 'eta') # time to destination from the next node
            else:
                # if there is no path to the destination
                return -1000

            if self.next_node_time < self.last_node_time:
                # if the agent is closer to the destination
                self.last_node_time = self.next_node_time
                return -1

            self.last_node_time = self.next_node_time
            # if the agent is not closer to the destination
            return -3

    def calculate_reward_basic(self, blocked_roads):
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
                len(self.q_table[self.next_state]) == 0:
            self.blocked = True

            return -1000

        if self.dst == self.next_state:
            # High reward for reaching the destination
            self.finished = True
            if self.end_time is None:
                self.end_time = self.simulation_time
            else:
                self.end_time = min(self.end_time, self.simulation_time)
            return 1000

        else:
            return -1
            # rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
            # time_obj = self.simulation_time.replace(minute = rounded_minutes, second = 0, microsecond = 0)
            # time_str = time_obj.strftime("%H:%M")
            # eta = float(self.next_road.get_eta(time_str))  # eta in seconds
            # if self.next_road.destination_node.id in self.visited_nodes:
            #     return -eta-200
            # else:
            #     self.visited_nodes.append(self.next_road.destination_node.id)
            #     return -eta

    def reset(self):
        """
        Reset the agent's parameters.
        Used at the end of each episode.

        """
        # Flags
        self.blocked = False
        self.finished = False
        # Rewards
        self.rewards.append(self.total_episode_reward)
        if len(self.rewards) % 50 == 0:
            self.mean_rewards.append(np.mean(self.rewards[-50:]))
        self.total_episode_reward = 0

        # Path saving parameters
        self.all_training_paths_nodes.append(copy.deepcopy(self.path_nodes))
        self.all_training_times.append((self.simulation_time - self.start_time).total_seconds())
        self.path_roads.clear()
        self.path_nodes.clear()
        # self.visited_nodes.clear()
        # Time
        self.simulation_time = self.start_time
        self.last_node_time = None

        # During simulation parameters
        self.num_of_steps = 0
        self.current_road = None
        self.next_road = None
        self.current_state = None
        self.next_state = None
        return None
