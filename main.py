import folium
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import osmnx as ox
import networkx as nx
import threading
import time




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
    choice=int(input("Enter 1 for full map, 2 (or else) for minimal version: "))
    for i, edge in enumerate(g.edges):
        if choice==1:
            if g.edges[edge]['highway'] in ('tertiary', 'tertiary_link'):
                edge_colors.append('r')
            if g.edges[edge]['highway'] == 'residential':
                edge_colors.append('g')
            if g.edges[edge]['highway'] == 'unclassified':
                edge_colors.append('b')
            if g.edges[edge]['highway'] in ('secondary', 'secondary_link'):
                edge_colors.append('#3bd1ca')
            if g.edges[edge]['highway'] == 'living_street':
                edge_colors.append('y')
            if g.edges[edge]['highway'] in ('trunk', 'trunk_link'):
                edge_colors.append('pink')
        else:
            if g.edges[edge]['highway'] in ('tertiary', 'tertiary_link'):
                edge_colors.append('r')
            if g.edges[edge]['highway'] == 'residential':
                edge_colors.append('black')
            if g.edges[edge]['highway'] == 'unclassified':
                edge_colors.append('black')
            if g.edges[edge]['highway'] in ('secondary', 'secondary_link'):
                edge_colors.append('#3bd1ca')
            if g.edges[edge]['highway'] == 'living_street':
                edge_colors.append('black')
            if g.edges[edge]['highway'] in ('trunk', 'trunk_link'):
                edge_colors.append('pink')

    """
    print(f"{edge_colors.count('w')}-motorway")
    print(f"{edge_colors.count('g')}-residential")
    print(f"{edge_colors.count('r')}-tertiary")
    print(f"{edge_colors.count('b')}-unclassified")
    print(f"{edge_colors.count('#3bd1ca')}-secondary")
    print(f"{edge_colors.count('y')}-living_street")
    print(f"{edge_colors.count('pink')}-trunk")
    """
    return edge_colors

"""
if g.edges[edge]['highway'] == 'unclassified':
    edge_colors.append('b')
else:
    if g.edges[edge]['highway'] == 'living_street':
        edge_colors.append('y')
    else:
        edge_colors.append('black')
"""

    #print(i)


def colorTrafficLights(g):
    # color the nodes that have traffic lights
    nodeColor=[]

    for i, node in enumerate(g.nodes):
        if g.nodes[node].get('highway') == 'traffic_signals':
            nodeColor.append('blue')
        else:
            nodeColor.append('w')

    return nodeColor

def colorNodesByStreetCount(g):
    # color the nodes that have traffic lights
    nodeColor=[]

    for i, node in enumerate(g.nodes):
        print(type(g.nodes[node].get('street_count')))
        if g.nodes[node].get('street_count') == 1:
            nodeColor.append('red')
        elif g.nodes[node].get('street_count') == 2:
            nodeColor.append('purple')
        elif g.nodes[node].get('street_count') == 3:
            nodeColor.append('green')
        elif g.nodes[node].get('street_count') == 4:
            nodeColor.append('yellow')
        elif g.nodes[node].get('street_count') == 5:
            nodeColor.append('orange')
        elif g.nodes[node].get('street_count') == 6:
            nodeColor.append('green')
        else:
            nodeColor.append('w')

    return nodeColor
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

def printGraphWithNamesFixed(G):
    # problem with lists, the names are already backwards so no need ro reverse them, at least for now.
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

def printGraphWithNamesFixed2(G):
    # no reversing for lists
    for _, edge in ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
        c = edge['geometry'].centroid
        if type(edge['name']) == list:
            text = edge['name']
        else:
            edge['name'] = edge['name'][::-1]
            text = edge['name']
        ax.annotate(text, (c.x, c.y), c='w')
    plt.show()
    return


g2 = ox.load_graphml('./data/graphTLVFix.graphml')
edge_colors=colorByType(g2)
node_choice=int(input("Enter 1 for traffic lights, 2 for street count: "))
if node_choice == 1:
    node_colors=colorTrafficLights(g2)
else:
    node_colors=colorNodesByStreetCount(g2)
print(node_colors)

fig, ax = ox.plot_graph(g2, bgcolor='k', edge_linewidth=3, node_size=10, edge_color=edge_colors,node_color=node_colors, show=False, close=False)
printGraphWithNamesFixed2(g2)
