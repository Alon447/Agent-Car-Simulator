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
