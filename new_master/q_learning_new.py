import datetime

import numpy as np

from new_master.Car import Car
from new_master.Road_Network import Road_Network


class QLearning:
    def __init__(self, road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.2):
        self.road_network = road_network
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.node_list = self.road_network.get_node_connectivity_dict()

        self.q_table = self.initialize_q_table()

    # def initialize_q_table(self):
    #     # Initialize the Q-table with zeros for all state-action pairs
    #     num_states = len(self.road_network.get_graph_nodes())
    #     num_actions = 4 # Replace with the correct number of actions
    #     return np.zeros((num_states, num_actions))

    def update_q_table(self, state, action, next_state, reward):
        # Q-learning update rule
        current_q_value = self.q_table[state][action]
        max_next_q_value = np.max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value

    def choose_action(self, state):
        # Epsilon-greedy policy to choose an action
        if np.random.rand() < self.epsilon:
            return np.random.choice(4)
            # return np.random.choice(len(self.road_network.get_roads_array()))  # Explore by choosing a random action
        else:
            return np.argmax(self.q_table[state])  # Exploit by choosing the action with the highest Q-value

    def train(self, num_episodes:int, cars:list ,epsilon_decay_rate=0.99):
        for episode in range(num_episodes):
            for car in cars:
                state = car.get_current_road().get_destination_node()
                if state == car.get_destination_node():
                    break
                action = self.choose_action(state)
                next_road = self.road_network.get_roads_array()[action]
                next_state = next_road.get_id()

                reward = self.calculate_reward(car)

                self.update_q_table(state, action, next_state, reward)
                car.move_next_road()

            self.epsilon *= epsilon_decay_rate

    def calculate_reward(self, car):
        # Calculate the reward based on the car's progress and other factors
        if car.get_car_in_destination():
            return 1000  # High reward for reaching the destination
        elif car.get_is_blocked():
            return -100  # Penalty for getting blocked
        else:
            # You can design a more sophisticated reward function based on factors like travel time, distance traveled, etc.
            return -1

    def initialize_q_table(self):
        q_values = []
        for i in range(len(self.road_network.get_graph_nodes())):
            row_values = []
            if self.node_list.get(i) is None:
                q_values.append([])
                continue
            for j in range(len(self.node_list[i])):
                row_values.append(0)
            q_values.append(row_values)
        return q_values
    def save_q_table(self, filename):
        np.save(filename, self.q_table)

    def load_q_table(self, filename):
        self.q_table = np.load(filename)

# Example usage
road_network = Road_Network("../data/TLV_with_eta.graphml")  # Replace with the correct path to your graphml file
q_learning = QLearning(road_network)

# Train the Q-learning model
num_episodes = 100
cars=[]
c1=Car(1,1,2,datetime.datetime.now(),road_network)
cars.append(c1)
q_learning.train(num_episodes,cars)

# Save the learned Q-table for future use
q_learning.save_q_table("q_table.npy")

# Load the pre-trained Q-table from file
q_learning.load_q_table("q_table.npy")
