import datetime
import random

import networkx as nx
from matplotlib import pyplot as plt

from new_master.Car import Car
from new_master.Road_Network import Road_Network
from new_master.q_learning_new import QLearning

def choose_random_src_dst(road_network):
    src = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
    dst = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
    src_osm = road_network.reverse_node_dict[src]
    dest_osm = road_network.reverse_node_dict[dst]
    while not nx.has_path(road_network.get_graph(), src_osm, dest_osm):
        print(f"There is no path between {src} and {dst}.")
        src = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
        dst = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
        src_osm = road_network.reverse_node_dict[src]
        dest_osm = road_network.reverse_node_dict[dst]
    return src, dst

def test(road_network, number_of_tests = 100):
    """
    :param road_network:
    :param number_of_tests:
    :return:
    """
    test_rewards = []
    agent = QLearning(road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.1)
    for _ in range(number_of_tests):
        src, dst = choose_random_src_dst(road_network)
        print("src: ", src, "dst: ", dst)

        c1 = Car(1, src, dst, datetime.datetime.now(), road_network)
        # Train the agent
        num_episodes = 1500
        max_steps_per_episode = 100
        agent.train(num_episodes, c1, max_steps_per_episode=max_steps_per_episode)
        test_reward = agent.test(c1)  # this will be the test function
        if test_reward > 500:
            test_rewards.append(1)
        else:
            test_rewards.append(0)
        # test_rewards.append(test_reward)
    percentage = 100*sum(test_rewards) / number_of_tests
    print("percentage: ", percentage)


road_network = Road_Network("/TLV_with_eta.graphml")  # Replace with the correct path to your graphml file
test(road_network, number_of_tests=5)
# agent = QLearning(road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.1)
# src = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
# dst = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
# print("src: ", src, "dst: ", dst)
# src_osm = road_network.reverse_node_dict[src]
# dest_osm = road_network.reverse_node_dict[dst]
# if not nx.has_path(road_network.get_graph(), src_osm, dest_osm):
#     print(f"There is no path between {src} and {dst}.")
#     exit(1)
# c1 = Car(1, src, dst, datetime.datetime.now(), road_network)
# cars = [c1]
# # Train the agent
# num_episodes = 6200
# max_steps_per_episode = 100
# agent.train(num_episodes, c1,  max_steps_per_episode=max_steps_per_episode)
# agent.test(c1) # this will be the test function

# Print average test rewards
# average_test_reward = sum(test_rewards) / num_test_episodes
# print("Average test reward: ", average_test_reward)