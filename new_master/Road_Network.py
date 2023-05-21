import os

import osmnx as ox
import Road
import pandas as pd
import networkx as nx
class Road_Network:
    def __init__(self, graph_path):
        self.roads_array = []
        self.graph = self.set_graph(graph_path)
        self.roads_speeds= {}
        self.distance_matrix = self.calc_dist_mat()
        #check if necessary
        self.nodes = ox.graph_to_gdfs(self.graph, edges=False)
        self.edges = ox.graph_to_gdfs(self.graph, nodes=False)
        self.nodes = self.nodes.to_dict()
        self.edges = self.edges.to_dict()

    def set_roads_array(self):
        for edge in self.graph.edges:
            self.road_array.append(G.edges[edge]['edge_id'], edge[0], edge[1], edge, G.edges[edge]['maxspeed'])

    #def set_connectivity_list(self):


    def calc_dist_mat(self):
        # makes a matrix of the shortest distances between all the roads
        return pd.DataFrame.from_dict(dict(nx.all_pairs_dijkstra_path_length(self.graph)), orient='index')

    def set_graph(self, graph_path):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        return ox.load_graphml(data + graph_path)

    # GETS
    def get_roads_array(self):
        return self.roads_array

    def get_roads_speeds(self):
        return self.roads_speeds
    def get_nodes(self):
        return self.nodes
    def get_edges(self):
        return self.edges

    def __str__(self):
        return "Road_Network"


RN = Road_Network('/graphTLVfix.graphml')
print(RN.get_edges())

# print(RN)
# print(RN.get_edges())
print(RN.distance_matrix[476379129])
