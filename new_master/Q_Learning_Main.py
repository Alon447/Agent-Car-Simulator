import copy
import csv
import datetime
import random
import osmnx as ox
import networkx as nx
from matplotlib import pyplot as plt
import pandas as pd

from new_master.Car import Car
from new_master.Q_Learning_Functions import QLearning
from new_master.Road_Network import Road_Network

def osm_route_to_node_route(osm_route, road_network):
    """
    :param osm_route: a list of nodes in the route
    :param road_network: the road network
    :return: a list of roads in the route
    """
    node_route = []
    for i in range(len(osm_route)):
        node_route.append(road_network.node_dict[osm_route[i]])
    return node_route
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

def calculate_route_eta(route, road_network):
    """
    :param route: a list of roads in the route
    :param road_network: the road network
    :return: the eta of the route
    """
    eta = 0
    for i in range(len(route)-1):
        src = route[i]
        j=i+1
        dst = route[j]
        eta += float(road_network.get_graph()[src][dst][0].get('eta'))
    return eta
def choose_random_src_dst(road_network):
    src = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
    dst = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
    src_osm = road_network.reverse_node_dict[src]
    dest_osm = road_network.reverse_node_dict[dst]
    while not nx.has_path(road_network.get_graph(), src_osm, dest_osm):
        # print(f"There is no path between {src} and {dst}.")
        src = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
        dst = random.Random().randint(0, len(road_network.get_node_connectivity_dict()) - 1)
        src_osm = road_network.reverse_node_dict[src]
        dest_osm = road_network.reverse_node_dict[dst]
    return src, dst

def test(road_network, number_of_tests = 1):
    """
    :param road_network:
    :param number_of_tests:
    :return:
    """
    test_rewards = []
    agent = QLearning(road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.1)
    for i in range(number_of_tests):
        print("test number: ", i)
        src, dst = choose_random_src_dst(road_network)
        # src= 945
        # dst = 712
        # print("src: ", src, "dst: ", dst)
        path = nx.shortest_path(road_network.get_graph(), road_network.reverse_node_dict[src], road_network.reverse_node_dict[dst], weight='length')
        shortest_path_time = calculate_route_eta(path, road_network)
        shortest_path = osm_route_to_node_route(path,road_network)
        print("shortest path: ", shortest_path)
        c1 = Car(1, src, dst, datetime.datetime.now(), road_network)

        # Train the agent
        num_episodes = 3000
        max_steps_per_episode = 100
        agent.train(num_episodes, c1, max_steps_per_episode=max_steps_per_episode)

        # Test the agent
        test_reward, agent_path = agent.test(c1)  # this will be the test function



        rc= []
        new_routes = [node_route_to_osm_route(agent_path, road_network), node_route_to_osm_route(shortest_path, road_network)]
        times = [calculate_route_eta(new_routes[0],road_network), calculate_route_eta(new_routes[1],road_network)]
        rc.append("r")
        rc.append("b")
        print("times: ", times)
        if times[0] <= times[1]:  # test_reward > 500:
            test_rewards.append(1)
        else:
            test_rewards.append(0)

            # test_rewards.append(test_reward)
        percentage = 100 * sum(test_rewards) / len(test_rewards)
        print("percentage: ", percentage)
        print("************************************************************************")

        # Plot the custom route
        ox.plot_graph_routes(road_network.get_graph(), new_routes, route_colors=rc, route_linewidth=6,  node_size=0, bgcolor='k')

NUM_OF_TESTS = 10
road_network = Road_Network("/TLV_with_eta.graphml")  # Replace with the correct path to your graphml file
test(road_network, number_of_tests = NUM_OF_TESTS)



agent = QLearning(road_network, learning_rate=0.1, discount_factor=0.9, epsilon=0.1)
