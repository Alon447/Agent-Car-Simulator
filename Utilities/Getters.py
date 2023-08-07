import os
import osmnx as ox


def get_graph(graph_name: str):
    """

    :param graph_name: the name of the graph file, without the extension
    :return: osmnx multiDiGraph
    """
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    data = os.path.join(parent, "data")
    return ox.load_graphml(data + "/" + graph_name + ".graphml")


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