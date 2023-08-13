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
Distance_travelled = 'Distance_travelled'


def get_graph(graph_name: str):
    """
    Load an OSMnx MultiDiGraph from a graphml file.

    :param graph_name: the name of the graph file, without the extension
    :return: osmnx multiDiGraph
    """
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    data = os.path.join(parent, "Graphs")
    path = data + "/" + graph_name + ".graphml"
    if not os.path.exists(path):
        graph = ox.graph_from_place(graph_name, network_type='drive')
        modified_graph = Speeds.add_max_speed_to_graph(graph) # add max speed to the graph
        ox.save_graphml(modified_graph, filepath=path)

    return ox.load_graphml(path),path

def get_simulation_speeds_file_path(graph, city_name):
    """
    Load a dictionary of speeds for each road in the graph.

    :param graph_name: the name of the graph file, without the extension
    :return: dictionary of speeds for each road in the graph
    """
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    Speeds_Data = os.path.join(parent, "Speeds_Data")
    path = Speeds_Data + "/" + city_name + "_speeds.json"
    if not os.path.exists(path):
        Speeds.generate_day_data(graph, city_name)
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
    :param graph: the road network
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