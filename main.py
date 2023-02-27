import folium
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from neo4j import GraphDatabase, basic_auth
import pandas as pd
import osmnx as ox
import networkx as nx
import threading
import time


def printGraphWithNamesFixed(G):
    fig, ax = ox.plot_graph(G, bgcolor='k', edge_linewidth=3, node_size=0,
                            show=False, close=False)
    for _, edge in ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
        c = edge['geometry'].centroid
        if type(edge['name']) == list:
            for i, name in enumerate(edge['name']):
                name = name[::-1]
                edge['name'][i] = name
            text = edge['name']
        else:
            edge['name']=edge['name'][::-1]
            text = edge['name']
        ax.annotate(text, (c.x, c.y), c='w')
    plt.show()
    return

def test():
    # specify origin and destination coordinates
    origin = (37.7896239, -122.4011153)
    destination = (37.7888889, -122.3991668)

    # download the street network within a 1km buffer of the origin and destination
    G = ox.graph_from_point(origin, dist=3000, network_type='drive')
    G = ox.project_graph(G)

    # calculate the shortest path
    route = nx.shortest_path(G, origin, destination)

    # create a folium map centered at the origin
    m = folium.Map(location=origin, zoom_start=13)

    # add the route to the map as a red line
    folium.PolyLine(route, color='red', weight=2.5, opacity=1).add_to(m)

    # add markers for the origin and destination
    folium.Marker(origin, icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(destination, icon=folium.Icon(color='red')).add_to(m)

    # display the map
    m

def test():
    # specify origin and destination coordinates
    origin = (37.7896239, -122.4011153)
    destination = (37.7888889, -122.3991668)

    # download the street network within a 1km buffer of the origin and destination
    G = ox.graph_from_point(origin, dist=3000, network_type='drive')
    G = ox.project_graph(G)

    # calculate the shortest path
    route = nx.shortest_path(G, origin, destination)

    # create a folium map centered at the origin
    m = folium.Map(location=origin, zoom_start=13)

    # add the route to the map as a red line
    folium.PolyLine(route, color='red', weight=2.5, opacity=1).add_to(m)

    # add markers for the origin and destination
    folium.Marker(origin, icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(destination, icon=folium.Icon(color='red')).add_to(m)

    # display the map
    m


"""
printGraphWithNamesFixed(graphTelAviv)
ox.save_graphml(graphTelAviv, filepath='./data/graphTLVFix.graphml', gephi=False, encoding='utf-8')
G2 = ox.load_graphml('./data/graphTLVFix.graphml')
fig, ax = ox.plot_graph(G2, bgcolor='k', edge_linewidth=3, node_size=0,
                        show=False, close=False)
for _, edge in ox.graph_to_gdfs(G2, nodes=False).fillna('').iterrows():
    c = edge['geometry'].centroid
    text = edge['name']
    ax.annotate(text, (c.x, c.y), c='w')
plt.show()
"""


def colorByType(g):
    # specify the colors for each highway type
    # colors = {'motorway': white
    #           'trunk': pink
    #           'secondary': turquoise
    #           'tertiary': red
    #           'unclassified': blue,
    #           'residential': green
    #           'living_street': yellow
    edge_colors = []
    for i, edge in enumerate(g.edges):
        print(g.edges[edge])
        if g.edges[edge]['highway'] == 'motorway':
            edge_colors.append('w')
        if g.edges[edge]['highway'] == 'residential':
            edge_colors.append('g')
        if g.edges[edge]['highway'] == 'tertiary' or 'tertiary_link':
            edge_colors.append('r')
        if g.edges[edge]['highway'] == 'unclassified':
            edge_colors.append('b')
        if g.edges[edge]['highway'] == 'secondary' or 'secondary_link':
            edge_colors.append('#3bd1ca')
        if g.edges[edge]['highway'] == 'living_street':
            edge_colors.append('y')
        if g.edges[edge]['highway'] == 'trunk' or 'trunk_link':
            edge_colors.append('pink')

    print(i)
    return edge_colors
"""
        




g2 = ox.load_graphml('./data/graphTLVFix.graphml')
num_edges = len(g2.edges)
edge_colors = ['g'] * num_edges
for i, edge in enumerate(g2.edges):
    print(g2.edges[edge])
    if g2.edges[edge]['length'] < 100:
        edge_colors[i] = 'r'
    if 'maxspeed' in g2.edges[edge]:
        if int(g2.edges[edge]['maxspeed']) > 30:
            edge_colors[i] = 'y'
"""
g2 = ox.load_graphml('./data/graphTLVFix.graphml')
edge_colors=colorByType(g2)
print(edge_colors)

# I tried to put the names of the streets in the graph but it didn't work
fig, ax = ox.plot_graph(g2, bgcolor='k', edge_linewidth=3, node_size=0,
                        show=True, close=False,edge_color=edge_colors)
for _, edge in ox.graph_to_gdfs(g2, nodes=False).fillna('').iterrows():
    c = edge['geometry'].centroid
    text = edge['name']
    ax.annotate(text, (c.x, c.y), c='w')
plt.show()
print(g2)
