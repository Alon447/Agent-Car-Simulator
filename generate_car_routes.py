import folium
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import osmnx as ox
import networkx as nx
import threading
import time
import random

def gen_route(G, time, start, end, chosen_weight):
    route = nx.shortest_path(G, source=start, target=end, weight=chosen_weight)
    return route

def gen_random_route(G, chosen_weight):
    node_lst = (list(G.nodes))
    start = random.choice(node_lst)
    node_lst.remove(start)
    end = random.choice(node_lst)
    route = nx.shortest_path(G, source=start, target=end, weight=chosen_weight)
    return route


def get_next_traffic_state(G, time, route_list, current_state):
    """

    :param G: the Map graph
    :param time: the current time
    :param route_list: nodes of each car's route, and starting time
    :param current_state: holds the amount of vheicles on each edge, ordered by arrival time
    :return: the next traffic state (dict) and the next time (int) after 20 seconds
    """

def sample_state(G, time, route_list, current_state, saved_states):
    """


    :param G: the Map graph
    :param time: the current time
    :param route_list: nodes of each car's route, and starting time
    :param current_state: holds the amount of vheicles on each edge, ordered by arrival time
    :return: the next traffic state (dict) and the next time (int) after 20 seconds
    """

def save_sampled_states(saved_states):
    """

    :param saved_states: the sampled states
    :return: None
    """

def create_state_dictionary(G, starting_time, route_list):
    """
    the state will contain the amount of vehicles on each edge, ordered by arrival time.
    the edge will also contain a stack of cars waiting to move to the next edge.
    :param G: the Map graph
    :param starting_time: the starting time of the simulation
    :param route_list: list of routes
    :return: the initial traffic state (dict) and the next time (int) after 20 seconds
    """
    nodes_list = []
    for route in route_list:
        nodes_list.extend(route)
    #for i,edge in enumerate(G.edges):
