import os
import random

import networkx as nx
import osmnx as ox

import Utilities.Speeds as Speeds

# Simulation results dictionary keys
Simulation_number = 'Simulation_number'
Source = 'Source'
Destination = 'Destination'
Reached_destination = 'Reached_destination'
Routing_algorithm = 'Routing_algorithm'
Time_taken = 'Time_taken'
Day_of_week = 'Day_of_week'
Start_time = 'Start_time'
End_time = 'End_time'
Route = 'Route'
Roads_used = 'Roads_used'
Blocked_roads = 'Blocked_roads'
Distance_travelled = 'Distance_travelled'

minute_in_seconds = 60
hour_in_seconds = 60 * minute_in_seconds
day_in_seconds = 24 * hour_in_seconds
week_in_seconds = 7 * day_in_seconds

rain_intensity_values = ["None", "Light", "Moderate", "Heavy"] # TODO: change to none, light, medium, heavy

hours = [i for i in range(0, 24)]
minutes = [i for i in range(0, 60)]
seconds = [i for i in range(0, 60)]

days = [i for i in range(0, 7)]
weeks = [i for i in range(0, 4)]
months = [i for i in range(0, 12)]

# for testing and statistics in TLV map:
# TODO: check if neccessary
top_right_nodes = [714,428,963,720,242,969,677,319,206,653,404,970,964,406,684,870]
bottom_left_nodes = [650,604,651,652,135,602,647,803,480,637,644,640,872,884,497,166]

top_left_nodes = [991,989,749,115,113,107,731,730,0,1,9,877,992,704,762]
bottom_right_nodes = [866,443,912,898,960,819,829,506,203,865,505,508,627,658,99,597]
#

days_of_the_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

routing_algorithms = [
    "Shortest Path",
    "Random Path",
    "Q Learning"
]

def get_graph(graph_name: str):
    """
    Load an OSMnx MultiDiGraph from a graphml file.
    If the file does not exist, download the graph from OSMnx and save it as a graphml file.
    The donwloaded graph will be saved in the Graphs folder.

    :param graph_name: the name of the graph file, without the extension

    :returns:
    osmnx multiDiGraph
    """
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    data = os.path.join(parent, "Graphs")
    path = data + "\\" + graph_name + ".graphml"
    if not os.path.exists(path):
        graph = ox.graph_from_address(graph_name, network_type='drive', dist = 3000, simplify = True)
        modified_graph = Speeds.add_max_speed_to_graph(graph) # add max speed to the graph
        ox.save_graphml(modified_graph, filepath=path)

    return ox.load_graphml(path),path

def get_q_tables_directory():
    """
    get the directory of the q tables

    :return:
    (str): the updated path
    """
    tables_directory = "Q Tables Data"
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    path = os.path.join(parent, tables_directory)
    return path
def get_simulation_speeds_file_path(graph, graph_name):
    """
    Load a dictionary of speeds for each road in the graph.

    :param graph: the graph
    :param graph_name: the name of the graph file, without the extension


    :return: dictionary of speeds for each road in the graph
    """
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    Speeds_Data = os.path.join(parent, "Speeds_Data")
    path = Speeds_Data + "/" + graph_name + "_speeds.json"
    if not os.path.exists(path):
        Speeds.generate_day_data(graph, graph_name)
        print("file created")
    return path
def get_lat_lng(address):
    """
    can get hebrew and english addresses
    :param address: hebrew or english address
    :return: latitude and longitude of the address
    """
    # Perform geocoding
    location = ox.geocode(address)
    latitude = location[0]
    longitude = location[1]
    return latitude, longitude

def time_delta_to_seconds(time):
    """
    transform a time delta to seconds
    :param time: timedelta
    :return:
    """
    return int(time.total_seconds())

def node_route_to_osm_route(road_network, node_route):
    """
    :param node_route: a list of nodes in the route
    :param road_network: the road network
    :return: a list of roads in the route
    """
    osm_route = []
    for i, node in enumerate(node_route):
        osm_route.append(road_network.nodes_array[node].osm_id)
    return osm_route

def get_random_src_dst(RN):
    """
    get a random source and destination from the road network that have a path between them
    :param RN: the road network
    :return: a random source and destination
    """
    src = RN.nodes_array[random.randint(0, len(RN.nodes_array) - 1)]
    dst = RN.nodes_array[random.randint(0, len(RN.nodes_array) - 1)]
    while not nx.has_path(RN.nx_graph, src.id, dst.id) and src.id != dst.id:
        src = RN.nodes_array[random.randint(0, len(RN.nodes_array) - 1)]
        dst = RN.nodes_array[random.randint(0, len(RN.nodes_array) - 1)]

    return src.id, dst.id



def get_key_from_value(dictionary, value):
    """
    Retrieve the corresponding key from a dictionary given a value.

    Args:
    dictionary (dict): The dictionary to search in.
    value: The value to search for.

    Returns:
    key: The key corresponding to the given value.
    """
    for key, val in dictionary.items():
        if int(val) == value:
            return key
    return None

def calaulate_starting_ending_times(datetimes_list):
    """
    :param datetimes_list: list of datetimes
    :return: starting and ending times of the datetimes
    """
    starting_time = datetimes_list[0]
    ending_time = datetimes_list[0]
    for time in datetimes_list:
        starting_time = min(starting_time, time)
        ending_time = max(ending_time, time)
    return starting_time, ending_time