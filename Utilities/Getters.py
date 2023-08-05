import os
import osmnx as ox


def get_graph(graph_name: str):
    cur = os.getcwd()
    parent = os.path.dirname(cur)
    data = os.path.join(parent, "data")
    return ox.load_graphml(data + "/" + graph_name + ".graphml")
