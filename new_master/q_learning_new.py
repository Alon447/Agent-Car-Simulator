import datetime

import numpy as np
import matplotlib.pyplot as plt

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
        self.rewards = []

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



    def choose_action(self, state):
        # Epsilon-greedy policy to choose an action
        if np.random.rand() < self.epsilon:
            return np.random.choice(len(self.q_table[state]))
        else:
            return np.argmax(self.q_table[state])  # Exploit by choosing the action with the highest Q-value

    def get_next_road(self, src_node, action):
        """
        :param src_node: the src node index
        :param action: the index of the dst node in the node list
        :return:
        """
        dest_node = self.node_list[src_node][action]
        road_index = self.road_network.road_dict[(src_node,dest_node)]
        return self.road_network.get_roads_array()[road_index]



    def update_state(self, car, next_road):
        """
        update the state of the car, i.e moves the car to the next road
        :param car:
        :return:
        """
        car.set_current_road(next_road)
    def calculate_reward(self, car, next_state):
        # Calculate the reward based on the car's progress and other factors
        if car.get_destination_node() == next_state:
            return 1000  # High reward for reaching the destination
        elif len(self.q_table[next_state]) == 0:
            return -100  # Penalty for getting blocked
        else:
            # You can design a more sophisticated reward function based on factors like travel time, distance traveled, etc.
            return -1

    def update_q_table(self, state, action, next_state, reward):
        # Q-learning update rule
        current_q_value = self.q_table[state][action]
        if reward == -100:
            max_next_q_value = -100
        else:
            max_next_q_value = np.max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value


    def train(self, num_episodes: int, car: Car, max_steps_per_episode=100, epsilon_decay_rate=0.99, mean_rewards_interval=10):
        print("************************************************************************************")
        print("Training started")

        src = car.get_source_node()
        dst = car.get_destination_node()

        mean_rewards = []  # List to store mean rewards for every 10 episodes
        mean_reward_sum = 0  # Variable to keep track of the sum of rewards in the last 10 episodes

        for episode in range(num_episodes):
            total_episode_reward = 0
            path_nodes = []
            path_roads = []

            # print("episode: ", episode)
            for step in range(max_steps_per_episode):
                # for car in cars:
                if step == 0:
                    state = car.get_source_node()
                    path_nodes.append(state)
                else:
                    state = car.get_current_road().get_destination_node()

                if state == car.get_destination_node():
                    # print("car reached destination")
                    break
                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                next_state = next_road.get_destination_node()
                reward = self.calculate_reward(car, next_state)
                total_episode_reward += reward
                self.update_q_table(state, action, next_state, reward)

                path_roads.append(next_road.get_id())
                path_nodes.append(next_road.get_destination_node())

                if reward == -100:  # car is blocked
                    # print("car is blocked")
                    break
                self.update_state(car, next_road)
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
                    # print("convrged after ", episode, " episodes")
                    break
                mean_reward_sum = 0  # Reset the sum for the next 10 episodes

            path_roads.clear()
            path_nodes.clear()
            total_episode_reward = 0
            self.epsilon *= epsilon_decay_rate

        print("************************************************************************************")
        print("Training finished")
        print("src: ", src, "dst: ", dst)
        print("************************************************************************************")

        # # Plot mean rewards
        # plt.plot(range(1, len(mean_rewards) + 1), mean_rewards)
        # plt.xlabel('Interval (Every 10 Episodes)')
        # plt.ylabel('Mean Episode Reward')
        # plt.title('Mean Rewards over Training')
        # plt.show()

    def test(self,car:Car, max_steps_per_episode=100):
        print("************************************************************************************")
        print("Testing started")
        src = car.get_source_node()
        dst = car.get_destination_node()
        print("src: ", src, "dst: ", dst)


        test_rewards = 0
        path_nodes = []
        path_roads = []
        # car = Car(1, 1, 500, datetime.datetime.now(), self.road_network)
        state = car.get_source_node()
        for step in range(max_steps_per_episode):
            action = np.argmax(self.q_table[state])
            next_road = self.get_next_road(state, action)
            next_state = next_road.get_destination_node()
            reward = self.calculate_reward(car, next_state)
            test_rewards += reward
            path_roads.append(next_road.get_id())
            path_nodes.append(next_road.get_destination_node())
            if reward == -100 or reward == 1000:  # car is blocked or reached destination
                break

            state = next_state
        print("path nodes: ", path_nodes)
        print("path roads: ", path_roads)
        print("Test reward: ", test_rewards)
        return test_rewards
    def save_q_table(self, filename):
        np.save(filename, self.q_table)

    def load_q_table(self, filename):
        self.q_table = np.load(filename)

# Example usage
# road_network = Road_Network("../data/TLV_with_eta.graphml")  # Replace with the correct path to your graphml file
# q_learning = QLearning(road_network)
#
# # Train the Q-learning model
# num_episodes = 100
# cars=[]
# c1=Car(1,1,2,datetime.datetime.now(),road_network)
# cars.append(c1)
# q_learning.train(num_episodes,cars)
#
# # Save the learned Q-table for future use
# q_learning.save_q_table("q_table.npy")
#
# # Load the pre-trained Q-table from file
# q_learning.load_q_table("q_table.npy")
# Create an instance of the QLearningAgent
