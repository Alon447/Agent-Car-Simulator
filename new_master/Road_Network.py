import os

import osmnx as ox
import Road
class Road_Network:
    def __init__(self):
        self.roads_array = []
        self.graph = self.get_graph()
        self.roads_speeds= {}
        self.nodes = ox.graph_to_gdfs(self.graph, edges=False)
        self.edges = ox.graph_to_gdfs(self.graph, nodes=False)
        self.nodes = self.nodes.to_dict()
        self.edges = self.edges.to_dict()

    def get_graph(self):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        return ox.load_graphml(data + '/graphTLVfix.graphml')

    # GETS
    def get_roads_array(self):
        return self.roads_array
    def get_graph(self):
        return self.graph
    def get_roads_speeds(self):
        return self.roads_speeds
    def get_nodes(self):
        return self.nodes
    def get_edges(self):
        return self.edges

    def __str__(self):
        return "Road_Network"

RN = Road_Network()
print(RN)
print(RN.get_edges())
#print(RN.get_nodes())
