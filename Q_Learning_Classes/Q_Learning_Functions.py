import datetime
import os
import pickle

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from geopy.distance import great_circle

from new_master.Road_Network import Road_Network
from Q_Learning_Classes import Q_Agent


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
        self.node_list = self.road_network.node_connectivity_dict
        self.q_table = self.initialize_q_table()
        self.rewards = []
        self.simulation_time = 0

    def initialize_q_table(self):
        q_values = []
        for i in range(len(self.road_network.graph_nodes)):
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
            eta += float(road_network.graph[src][dst][0].get('eta'))
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
        return self.road_network.roads_array[road_index]



    def update_state(self, q_agent: Q_Agent, next_road):
        """
        update the state of the agent, i.e moves the agent to the next road
        :param Q_Agent:
        :return:
        """
        q_agent.current_road = next_road
        return

    def calculate_distance(self, src:int, dst:int):
        """
        :param src: source node
        :param dst: destination node
        :return: the distance between the two nodes
        """
        point_src = (self.road_network.graph_nodes[src][3],self.road_network.graph_nodes[src][2])
        point_dst = (self.road_network.graph_nodes[dst][3],self.road_network.graph_nodes[dst][2])
        distance = great_circle(point_src, point_dst)
        return distance

    def calculate_reward(self, agent: Q_Agent, next_state, src, dst, eta, path_nodes, delta_time):
        # Calculate the reward based on the agent's progress and other factors
        src_dst_distance = self.calculate_distance(src, dst)
        next_state_dst_distance = self.calculate_distance(next_state, dst)
        distance_delta = src_dst_distance - next_state_dst_distance # positive if the agent is closer to the destination

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
                return -1

    def update_q_table(self, state, action, next_state, reward, eta):
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
        plt.plot(range(1, len(var) + 1), var)
        plt.xlabel('Interval (Every 10 Episodes)')
        plt.ylabel('Mean Episode Reward')
        plt.title('Mean Rewards over Training')
        plt.show()



    def save_q_table(self, src, dst, save_path):
        filename = os.path.join(save_path, f'q_table_{src}_{dst}.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, src, dst, save_path):
        filename = os.path.join(save_path, f'q_table_{src}_{dst}.pkl')
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            # print(f"Q-table file '{filename}' not found.")
            return False


    # functions for the Route class, gets src and dst instead of agent
    def train_src_dst(self, src: int, dst: int, start_time:datetime, num_episodes: int,  max_steps_per_episode=100, epsilon_decay_rate=0.99, mean_rewards_interval=100):
        # print("*********************************************")
        # print("          Training Started                   ")
        # print("*********************************************")
        agent = Q_Agent.Q_Agent(src, dst, start_time, self.road_network)
        path = nx.shortest_path(self.road_network.graph, self.road_network.reverse_node_dict[src],self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)



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
                    state = agent.current_road.destination_node[0]


                action = self.choose_action(state)
                next_road = self.get_next_road(state, action)
                next_state = next_road.destination_node[0]


                # Calculate the rounded minutes
                rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
                time_obj = self.simulation_time.replace(minute=rounded_minutes,second=0, microsecond=0)
                time_str = time_obj.strftime("%H:%M")

                eta = float(next_road.get_eta(time_str)) # eta in seconds
                self.simulation_time += datetime.timedelta(seconds=eta)
                drive_time = (self.simulation_time - start_time).total_seconds()
                delta_time = drive_time - shortest_path_time  # positive if the agent is slower than the shortest path
                reward = self.calculate_reward(agent, next_state, src, dst, eta, path_nodes, delta_time)

                path_roads.append(next_road.id)
                path_nodes.append(next_road.destination_node[0])
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

        # self.plot_rewards(mean_rewards)
        return self.q_table

    def test_src_dst(self, src: int, dst: int, start_time:datetime, max_steps_per_episode=100):
        self.simulation_time = start_time

        agent = Q_Agent.Q_Agent(src, dst, datetime.datetime.now(), self.road_network)
        path = nx.shortest_path(self.road_network.graph, self.road_network.reverse_node_dict[src],
                                self.road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = self.calculate_route_eta(path, self.road_network)
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
            next_state = next_road.destination_node[0]
            # Calculate the rounded minutes
            rounded_minutes = self.simulation_time.minute - (self.simulation_time.minute % 10)
            time_obj = self.simulation_time.replace(minute=rounded_minutes, second=0, microsecond=0)
            time_str = time_obj.strftime("%H:%M")
            eta = float(next_road.get_eta(time_str))  # eta in seconds
            self.simulation_time += datetime.timedelta(seconds=eta)
            drive_time = (self.simulation_time - start_time).total_seconds()
            delta_time = drive_time - shortest_path_time  # positive if the agent is slower than the shortest path
            reward = self.calculate_reward(agent, next_state, src, dst, eta, path_nodes, delta_time)

            path_roads.append(next_road.id)
            path_nodes.append(next_road.destination_node[0])
            path_time = self.calculate_route_eta(node_route_to_osm_route(path_nodes, self.road_network),
                                                 self.road_network)
            delta_time = path_time - shortest_path_time  # positive if the agent is slower than the shortest path

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
        return self.q_table

