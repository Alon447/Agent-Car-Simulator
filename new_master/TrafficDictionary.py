import json
import os

import pandas as pd
import osmnx as ox
import networkx as nx
import datetime
import random

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

from new_master.Road_Network import Road_Network


class TrafficDictionary:
    def __init__(self, g):
        self._dictionary = {}
        self.graph = g
    def fix_edges_max_speed(self, name):
        g = ox.load_graphml(f'./data/{name}.graphml')
        type_30 = ['residantial', 'living_street', 'unclassified', 'service']
        graph_max_speed = {}
        for i, edge in enumerate(g.edges):
            if g.edges[edge]['highway'] in type_30:
                graph_max_speed[edge] = 30
            else:
                graph_max_speed[edge] = 50
        nx.set_edge_attributes(g, graph_max_speed, "maxspeed")
        return

    def add_edge_id(name):
        g = ox.load_graphml(f'./data/{name}.graphml')
        graph_edge_id = {}
        for i, edge in enumerate(g.edges):
            graph_edge_id[edge] = i
        nx.set_edge_attributes(g, graph_edge_id, "edge_id")
        ox.save_graphml(g, filepath=f'./data/{name}.graphml')
        return

    def add_node_id(name):
        g = ox.load_graphml(f'./data/{name}.graphml')
        graph_node_id = {}
        for i, node in enumerate(g.nodes):
            graph_node_id[node] = i
        nx.set_node_attributes(g, graph_node_id, "node_id")
        ox.save_graphml(g, filepath=f'./data/{name}.graphml')
        return

    def generate_edge_data(self, edge_id, max_speed):
        return

    def generate_day_data(self):
        number_of_roads = len(self.graph.edges)
        roads = [str(i) for i in range(number_of_roads)]
        start_time = datetime.datetime(2023, 3, 30, 0, 0)
        end_time = datetime.datetime(2023, 3, 31, 0, 0)
        # Define the interval
        interval = datetime.timedelta(minutes=10)
        # Initialize the dictionary
        data = {}
        for day in range(7):
            data[day] = {}
            for road in roads:
                data[day][road] = {}

        # Loop over the interval and generate random speeds for each road
        current_time = start_time
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            for day in range(7):
                if day == 5 or day == 6:
                    for road in roads:
                        speed=int(random.gauss(45, 1))
                        if speed<=0:
                            speed=1
                        data[day][road][time_str] = speed
                else:
                    for road in roads:
                        if current_time.hour<7 or current_time.hour>18:
                            speed=int(random.gauss(45, 1))
                            if speed<=0:
                                speed=1
                            data[day][road][time_str] = speed
                        else:
                            speed = int(random.gauss(27, 3))
                            if speed<=0:
                                speed=1
                            data[day][road][time_str]  = speed
            current_time += interval

        # Print the dictionary
        print(data)
        with open('simulation_speeds.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return


    def read_day_data(self,road_number,hour,minute):
        with open('simulation_speeds.json', 'r') as infile:
            data = json.load(infile)
        time_key = f"{hour:02d}:{minute:02d}"

        # Get the number from the JSON data
        number = data.get(str(road_number), {}).get(time_key)

        print(number)
    def create_available_roads_list(self, g):
        # makes a dictionary of all the roads and the roads that are available from them
        roads={}
        availble_roads= {}
        for road in g.edges:
            destination_node=road[1]
            for edge in g.edges:
                if edge[0]==destination_node:
                    availble_roads[edge]=g.edges[edge]['length']
            #print("a:",availble_roads,len(availble_roads))
            roads[road]=availble_roads
            availble_roads={}
        #print(roads,len(roads))
        return roads

    def create_distances_matrix(self, g):
        # makes a matrix of the shortest distances between all the roads
        dist_matrix = pd.DataFrame.from_dict(dict(nx.all_pairs_dijkstra_path_length(g)), orient='index')
        return dist_matrix

    def shortest_path(self, g, source, destination):
        return nx.shortest_path(g, source, destination)

    def plotting_custom_route(self):
        """
        this is the way for a car that finished its route to plot it on the map at the end
        saves the function here for future use
        """
        import osmnx as ox
        import matplotlib.pyplot as plt

        # Define the custom route as a list of node IDs
        custom_route = [342355075, 387519294]
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        graph = ox.load_graphml(data + '/TLV_with_eta.graphml')

        # Plot the graph
        fig, ax = ox.plot_graph(graph, show=False, close=False, edge_color='lightgray', node_color='gray',
                                bgcolor='white')

        # Plot the custom route
        ox.plot_graph_route(graph, custom_route, route_color='red', route_linewidth=6, ax=ax)

        # Show the plot
        plt.show()

    def node_date(self):
        counts = {}
        for node in self.graph.nodes:
            street_count = self.graph.nodes[node]['street_count']
            traffic_signals = self.graph.nodes[node].get('highway')
            if traffic_signals == 'traffic_signals':
                if street_count in counts:
                    counts[street_count] += 1
                else:
                    counts[street_count] = 1
        for number, count in counts.items():
            print(f"Number {number} appears {count} times")


# g = ox.load_graphml(f'../data/graphTLVFix.graphml')

RN = Road_Network('/TLV_with_eta.graphml')
g = RN.get_graph()
td = TrafficDictionary(g)
src = RN.reverse_node_dict[400]
dest = RN.reverse_node_dict[700]
for u, v, key, data in g.edges(keys=True, data=True):
    if 'eta' in data:
        # Convert the 'eta' attribute from string to float
        data['eta'] = float(data['eta'])
# td.generate_day_data()
path = nx.shortest_path(RN.graph, src, dest, weight='eta')
paths = nx.all_shortest_paths(RN.graph, src, dest, weight='eta')
for p in paths:
    print(p)
path_length = nx.shortest_path_length(RN.graph, src, dest, weight='eta')
# G = ox.load_graphml(f'../data/graphTLVFix.graphml')
route2 = [400,401,216,60,59,173,398,49,34,48,721,190,618,33,813,244,231,927,910,52,67,726,15,153,360,152,62,23,670,692,669,701,700]

# fig, ax = ox.plot_graph(G, close=False, edge_color='lightgray', node_color='gray',show=False, bgcolor='white')
# ox.plot_graph_route(G, route1, route_color='red', route_linewidth=6,ax=ax,show=False)

