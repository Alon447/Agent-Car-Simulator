import osmnx as ox
import networkx as nx
class TrafficDictionary:
    def __init__(self, g):
        self._dictionary = {}
        edges = g.edges()
        max_speeds = nx.get_edge_attributes(g, 'maxspeed')


    def fix_edges_max_speed(self):
        
        return
    def generate_edge_data(self, edge_id,max_speed):
        return


    def generate_state_data(self):

        return
    def generate_day_data(self):

        return

