import QueuedEdge
import osmnx as ox

# Class that contains all the edges of the graph
class QueuedEdgeArr:
    def __init__(self, G):
        self.edge_arr = []
        for edge in G.edges:
            self.a = QueuedEdge(edge, G.edges[edge]['maxspeed'], G.edges[edge]['maxspeed'], False, [], [], 10)
            self.edge_arr.append(self.a)
        print(self.edge_arr)

g2 = ox.load_graphml('./data/graphTLVFix.graphml')

QueuedEdgeArr(g2)