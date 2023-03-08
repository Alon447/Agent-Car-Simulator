import folium
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import osmnx as ox
import networkx as nx
import threading
import time
import l5kit as l5



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
    choice = 1
    for i, edge in enumerate(g.edges):
        if choice == 1:
            if g.edges[edge]['highway'] in ('tertiary', 'tertiary_link'):
                edge_colors.append('orange')
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


# print(i)


def colorTrafficLights(g):
    # color the nodes that have traffic lights
    nodeColor = []

    for i, node in enumerate(g.nodes):
        if g.nodes[node].get('highway') == 'traffic_signals':
            nodeColor.append('blue')
        else:
            nodeColor.append('w')

    return nodeColor


def colorNodesByStreetCount(g):
    # color the nodes that have traffic lights
    nodeColor = []

    for i, node in enumerate(g.nodes):
        print(g.nodes[node].get('street_id'))
        # print(type(g.nodes[node].get('street_count')))
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
            edge['name'] = edge['name'][::-1]
            text = edge['name']
        ax.annotate(text, (c.x, c.y), c='w')
    plt.show()
    return


def printGraphWithNamesFixed2(G):
    # no reversing for lists
    fig, ax = ox.plot_graph(G, bgcolor='k', edge_linewidth=3, node_size=0,
                            show=False, close=False)
    for _, edge in ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
        if edge['highway'] in ('secondary', 'secondary_link', 'trunk', 'trunk_link'):
            c = edge['geometry'].centroid
            if type(edge['name']) == list:
                text = edge['name']
            else:
                edge['name'] = edge['name'][::-1]
                text = edge['name']
            ax.annotate(text, (c.x, c.y), c='w')
    plt.show()
    return

def printGraph(g2):
    # print Tel Aviv's graph
    edge_colors = colorByType(g2)
    node_choice = int(input("Enter 1 for traffic lights, 2 for street count: "))
    if node_choice == 1:
        node_colors = colorTrafficLights(g2)
    else:
        node_colors = colorNodesByStreetCount(g2)
    # print(node_colors)

    fig, ax = ox.plot_graph(g2, bgcolor='black', edge_linewidth=3, node_size=10, edge_color=edge_colors,
                            node_color=node_colors, show=False, close=False)
    printGraphWithNamesFixed2(g2)

g2 = ox.load_graphml('./data/graphTLVFix.graphml')
edge_colors = colorByType(g2)

orig1 = 352934665
dest1 = 139712

# print(g2)
route1=ox.distance.shortest_path(g2, orig1, dest1, weight='length', cpus=1)

ox.plot.plot_graph_route(g2, route1, route_color='r', route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None, edge_color=edge_colors)
route_map = {'color': 'red', 'weight': 5, 'opacity': 0.7}
my_map = folium.Map(location=[32.0926596, 34.7746982], zoom_start=13, tiles='CartoDB positron')

ox.folium.plot_route_folium(g2, route1, route_map=route_map, popup_attribute=None, tiles='cartodbpositron', zoom=1, fit_bounds=True, map=my_map)
route_streets=[]
for i,node in enumerate(route1):
    if i+1<len(route1):
        next_node= route1[i+1]
    for edge in g2.edges:
        if edge[0]==node and edge[1]==next_node:
            if g2.edges[edge]['name'] not in route_streets:
                print(g2.edges[edge]['name'])
                route_streets.append(g2.edges[edge]['name'])
                break

print(route_streets)