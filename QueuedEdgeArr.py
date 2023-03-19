import QueuedEdge
class QueuedEdgeArr:
    def __init__(self, G):
        self.edge_arr = []
        for edge in G.edges:
            self.edge_arr.append(QueuedEdge(edge, G.edges[edge]['maxspeed'], G.edges[edge]['maxspeed'], False, [], [], 10))