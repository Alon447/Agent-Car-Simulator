

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import osmnx as ox
import networkx as nx


def create_and_save_area(name,distance):
    g = ox.graph_from_address(name, network_type='drive', dist=distance)
    ox.save_graphml(g, filepath=f'./data/{name}.graphml')
    return g

def save_graph(g,name):
    ox.save_graphml(g, filepath=f'./data/{name}.graphml')

"""
name = "tel aviv" #input("enter area: ")
#distance = int(input("enter distance MF: "))
#g = create_and_save_area(name, distance)
g = ox.load_graphml(f'./data/{name}.graphml')
ox.plot_graph(g)

edges = g.edges()
max_speeds = nx.get_edge_attributes(g, 'maxspeed')

type_30 = ['residantial', 'living_street', 'unclassified', 'service']
graph_max_speed = {}
for i, edge in enumerate(g.edges):
    if g.edges[edge]['highway'] in type_30:
        graph_max_speed[edge] = 30
    else:
        graph_max_speed[edge] = 50

print(len(max_speeds))

#save_graph(g)
"""
