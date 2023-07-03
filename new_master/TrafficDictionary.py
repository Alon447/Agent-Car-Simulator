import json
import os

import pandas as pd
import osmnx as ox
import networkx as nx
import datetime
import random

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
        for road in roads:
            data[road] = {}

        # Loop over the interval and generate random speeds for each road
        current_time = start_time
        speed=1
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            for road in roads:
                if current_time.hour<7 or current_time.hour>18:
                    speed=int(random.gauss(45, 1))
                    if speed<=0:
                        speed=1
                    data[road][time_str] = speed
                else:
                    speed = int(random.gauss(27, 3))
                    if speed<=0:
                        speed=1
                    data[road][time_str]  = speed
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
        graph = ox.load_graphml(data + '/graphTLVfix.graphml')

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

# a=ox.graph_from_place("tel aviv")

g = ox.load_graphml(f'../data/graphTLVFix.graphml')
# availble_roads=[]
# roads=[]
#
td = TrafficDictionary(g)
# tr_dic=td.create_available_roads_list(g)
# sum=0
# for i in tr_dic:
#     # print(i,tr_dic[i], len(tr_dic[i]))
#     sum+=len(tr_dic[i])
#
# dis=td.create_distances_matrix(g)
#
# print(max(dis[139713]))

# for i,edge in enumerate(g.edges):
#     destination_node = edge[
#    ]
#     for road in (g.edges):
#         if road[0] == destination_node:
#             availble_roads.append(edge)
#             if road not in roads:
#                 roads.append(edge)
#         print(availble_roads,len(availble_roads))
#     availble_roads=[]
# print(roads,len(roads))

td.generate_day_data()