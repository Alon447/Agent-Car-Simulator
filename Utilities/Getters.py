import os
import osmnx as ox

import Utilities.Speeds as Speeds


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

    return ox.load_graphml(path)

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

def node_route_to_osm_route(node_route, road_network):
    """
    :param node_route: a list of nodes in the route
    :param road_network: the road network
    :return: a list of roads in the route
    """
    osm_route = []
    for i, node in enumerate(node_route):
        osm_route.append(road_network.nodes_array[node].osm_id)
    return osm_route