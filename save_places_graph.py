import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import osmnx as ox
import networkx as nx


def save_area(name,distance):
    g = ox.graph_from_address(name, network_type='drive', dist=distance)
    ox.save_graphml(g, filepath=f'./data/{name}.graphml')
    return g

name = "tel aviv" #input("enter area: ")
#distance = int(input("enter distance MF: "))
#g = save_area(name, distance)
g = ox.load_graphml(f'./data/{name}.graphml')
ox.plot_graph(g)

edges = g.edges()
max_speeds = nx.get_edge_attributes(g, 'maxspeed')
print(max_speeds)