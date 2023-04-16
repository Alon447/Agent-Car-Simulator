import json

import osmnx as ox
import networkx as nx
import datetime
import random

class TrafficDictionary:
    def __init__(self, g):
        self._dictionary = {}
        edges = g.edges()
        max_speeds = nx.get_edge_attributes(g, 'maxspeed')

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

    def generate_state_data(self):

        return

    def generate_day_data(self):
        roads = ["road " + str(i) for i in range(1700)]
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
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M:%S")
            for road in roads:
                data[road][time_str] = random.randint(30, 70)
            current_time += interval

        # Print the dictionary
        print(data)
        return


g = ox.load_graphml(f'./data/tel aviv.graphml')
name= "tel aviv"
TrafficDictionary.add_node_id(name)