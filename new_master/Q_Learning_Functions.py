import datetime
import pickle

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from new_master.Car import Car
from new_master.Road_Network import Road_Network

def node_route_to_osm_route(node_route, road_network):
    """
    :param node_route: a list of nodes in the route
    :param road_network: the road network
    :return: a list of roads in the route
    """
    osm_route = []
    for i in range(len(node_route)):
        osm_route.append(road_network.reverse_node_dict[node_route[i]])
    return osm_route

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

    def calculate_route_eta(self, route, road_network):
        """
        :param route: a list of roads in the route
        :param road_network: the road network
        :return: the eta of the route
        """
        eta = 0
        for i in range(len(route) - 1):
            src = route[i]
            j = i + 1
            dst = route[j]
            eta += float(road_network.get_graph()[src][dst][0].get('eta'))
        return eta


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
    def calculate_reward(self, car, next_state, delta_time):
        # Calculate the reward based on the car's progress and other factors
        if car.get_destination_node() == next_state:
            # High reward for reaching the destination
            return 1000#max(1000 - 100*delta_time, 1)
        elif len(self.q_table[next_state]) == 0:
            # Penalty for getting blocked
            return -100
        else:
            return -1

    def update_q_table(self, state, action, next_state, reward, eta):
        # Q-learning update rule
        current_q_value = self.q_table[state][action]
        if reward == -100:
            max_next_q_value = -100
        else:
            max_next_q_value = np.max(self.q_table[next_state])  #
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value

    def plot_rewards(self, var:list):
        plt.plot(range(1, len(var) + 1), var)
        plt.xlabel('Interval (Every 10 Episodes)')
        plt.ylabel('Mean Episode Reward')
        plt.title('Mean Rewards over Training')
        plt.show()

    def train(self,car: Car, num_episodes: int,  max_steps_per_episode=100, epsilon_decay_rate=0.99, mean_rewards_interval=100):
        # print("*********************************************")
        # print("          Training Started                   ")
        # print("*********************************************")

        src = car.get_source_node()
        dst = car.get_destination_node()
        path = nx.shortest_path(self.road_network.get_graph(), self.road_network.reverse_node_dict[src],self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)

        mean_rewards = []  # List to store mean rewards for every 10 episodes
        mean_reward_sum = 0  # Variable to keep track of the sum of rewards in the last 10 episodes

        for episode in range(num_episodes):
            # Initialize parameters to evaluate the episode
            total_episode_reward = 0
            path_nodes = []
            path_roads = []

            # print("episode: ", episode)
            for step in range(max_steps_per_episode):
                # for car in cars:
                if step == 0:
                    # car starting now
                    state = car.get_source_node()
                    path_nodes.append(state)
                else:
                    # car is already on the road
                    state = car.get_current_road().get_destination_node()


                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                next_state = next_road.get_destination_node()
                eta = float(next_road.get_eta())

                path_roads.append(next_road.get_id())
                path_nodes.append(next_road.get_destination_node())
                path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network), self.road_network)
                delta_time = path_time - shortest_path_time # positive if the car is slower than the shortest path

                reward = self.calculate_reward(car, next_state, delta_time)
                total_episode_reward += reward
                self.update_q_table(state, action, next_state, reward, eta)



                if next_state == car.get_destination_node():
                    # print("car reached destination")
                    break

                if reward == -100:  # car is blocked
                    # print("car is blocked")
                    break
                self.update_state(car, next_road)

            self.rewards.append(total_episode_reward)
            # Calculate mean reward after every 10 episodes
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
                #     # print("convrged after ", episode, " episodes")
                #     break
                mean_reward_sum = 0  # Reset the sum for the next 10 episodes

            path_roads.clear()
            path_nodes.clear()
            total_episode_reward = 0
            self.epsilon *= epsilon_decay_rate
        #
        # print("*********************************************")
        # print("          Training Finished                  ")
        # # print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")

        # Plot mean rewards

        self.plot_rewards(mean_rewards)
        return

    def test(self,car:Car, max_steps_per_episode=100):
        src = car.get_source_node()
        dst = car.get_destination_node()
        path = nx.shortest_path(self.road_network.get_graph(), self.road_network.reverse_node_dict[src],
                                self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)
        # print("*********************************************")
        # print("          Testing Started                    ")
        print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")



        test_rewards = 0
        path_nodes = [src]
        path_roads = []
        # car = Car(1, 1, 500, datetime.datetime.now(), self.road_network)
        state = car.get_source_node()
        for step in range(max_steps_per_episode):
            action = np.argmax(self.q_table[state])
            next_road = self.get_next_road(state, action)
            next_state = next_road.get_destination_node()
            eta = float(next_road.get_eta())

            path_roads.append(next_road.get_id())
            path_nodes.append(next_road.get_destination_node())
            path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network),
                                                 self.road_network)
            delta_time = path_time - shortest_path_time  # positive if the car is slower than the shortest path

            reward = self.calculate_reward(car, next_state, delta_time)
            test_rewards += reward
            # path_roads.append(next_road.get_id())
            # path_nodes.append(next_road.get_destination_node())
            # print("path nodes: ", path_nodes)
            if reward == -100 or reward == 1000:  # car is blocked or reached destination
                if reward == -100:
                    print("Car is blocked!")
                else:
                    print("Car reached the destination!")
                break

            state = next_state
            if state == car.get_destination_node():
                # print("car reached destination")
                break
        # print("path nodes: ", path_nodes)
        # print("path roads: ", path_roads)
        print(f"Test reward: {test_rewards:.2f}")
        # print("*********************************************")
        return test_rewards, path_nodes

    def save_q_table(self, src, dst):
        filename = f'q_table_{src}_{dst}.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, src, dst):
        filename = f'q_table_{src}_{dst}.pkl'
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            print(f"Q-table file '{filename}' not found.")
            return False


    # functions for the Route class, gets src and dst instead of car
    def train_src_dst(self, src: int, dst: int, num_episodes: int,  max_steps_per_episode=100, epsilon_decay_rate=0.99, mean_rewards_interval=100):
        # print("*********************************************")
        # print("          Training Started                   ")
        # print("*********************************************")
        car = Car(1, src, dst, datetime.datetime.now(), self.road_network)
        path = nx.shortest_path(self.road_network.get_graph(), self.road_network.reverse_node_dict[src],self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)

        mean_rewards = []  # List to store mean rewards for every 10 episodes
        mean_reward_sum = 0  # Variable to keep track of the sum of rewards in the last 10 episodes

        for episode in range(num_episodes):
            # Initialize parameters to evaluate the episode
            total_episode_reward = 0
            path_nodes = []
            path_roads = []

            # print("episode: ", episode)
            for step in range(max_steps_per_episode):
                # for car in cars:
                if step == 0:
                    # car starting now
                    state = car.get_source_node()
                    path_nodes.append(state)
                else:
                    # car is already on the road
                    state = car.get_current_road().get_destination_node()


                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                next_state = next_road.get_destination_node()
                eta = float(next_road.get_eta())

                path_roads.append(next_road.get_id())
                path_nodes.append(next_road.get_destination_node())
                path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network), self.road_network)
                delta_time = path_time - shortest_path_time # positive if the car is slower than the shortest path

                reward = self.calculate_reward(car, next_state, delta_time)
                total_episode_reward += reward
                self.update_q_table(state, action, next_state, reward, eta)



                if next_state == car.get_destination_node():
                    # print("car reached destination")
                    break

                if reward == -100:  # car is blocked
                    # print("car is blocked")
                    break
                self.update_state(car, next_road)

            self.rewards.append(total_episode_reward)
            # Calculate mean reward after every 10 episodes
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
                #     # print("convrged after ", episode, " episodes")
                #     break
                mean_reward_sum = 0  # Reset the sum for the next 10 episodes

            path_roads.clear()
            path_nodes.clear()
            total_episode_reward = 0
            self.epsilon *= epsilon_decay_rate
        #
        # print("*********************************************")
        # print("          Training Finished                  ")
        # # print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")

        # Plot mean rewards

        self.plot_rewards(mean_rewards)
        return self.q_table

    def test_src_dst(self, src: int, dst: int, max_steps_per_episode=100):

        car = Car(1, src, dst, datetime.datetime.now(), self.road_network)
        path = nx.shortest_path(self.road_network.get_graph(), self.road_network.reverse_node_dict[src],
                                self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)
        # print("*********************************************")
        # print("          Testing Started                    ")
        print(f"Source: {src}, Destination: {dst}")
        # print("*********************************************")



        test_rewards = 0
        path_nodes = [src]
        path_roads = []
        # car = Car(1, 1, 500, datetime.datetime.now(), self.road_network)
        state = car.get_source_node()
        for step in range(max_steps_per_episode):
            action = np.argmax(self.q_table[state])
            next_road = self.get_next_road(state, action)
            next_state = next_road.get_destination_node()
            eta = float(next_road.get_eta())

            path_roads.append(next_road.get_id())
            path_nodes.append(next_road.get_destination_node())
            path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network),
                                                 self.road_network)
            delta_time = path_time - shortest_path_time  # positive if the car is slower than the shortest path

            reward = self.calculate_reward(car, next_state, delta_time)
            test_rewards += reward
            # path_roads.append(next_road.get_id())
            # path_nodes.append(next_road.get_destination_node())
            # print("path nodes: ", path_nodes)
            if reward == -100 or reward == 1000:  # car is blocked or reached destination
                if reward == -100:
                    print("Car is blocked!")
                else:
                    print("Car reached the destination!")
                break

            state = next_state
            if state == car.get_destination_node():
                # print("car reached destination")
                break
        # print("path nodes: ", path_nodes)
        # print("path roads: ", path_roads)
        print(f"Test reward: {test_rewards:.2f}")
        # print("*********************************************")
        return test_rewards, path_nodes

    def get_q_table(self):
        return self.q_table
