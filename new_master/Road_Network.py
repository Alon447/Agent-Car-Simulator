import os

import osmnx as ox
import Road

import pandas as pd
import networkx as nx
from abc import abstractmethod, ABC
import random




class Road_Network:
    """
    Road_Network class:
    This class represents a road network.
    meaning that it will contain the graph of the simulation.
    all the roads in the graph
    will set the necessary data for all the roads in the simulation
    will save a shortest distance matrix of all the nodes in the graph

    #CONTAINS:
    - graph
    - roads_array
    - roads_speeds
    - distance_matrix

    """

    def __init__(self, graph_path):
        self.roads_array = []
        self.graph = self.set_graph(graph_path)
        self.set_roads_array()
        self.roads_speeds = {}
        self.distance_matrix = self.calc_dist_mat()
        self.set_adjacney_roads()
        ###############################
        # check if necessary
        self.nodes = ox.graph_to_gdfs(self.graph, edges=False)
        self.edges = ox.graph_to_gdfs(self.graph, nodes=False)
        self.nodes = self.nodes.to_dict()
        self.edges = self.edges.to_dict()
        self.adjacency_matrix = nx.adjacency_matrix(self.graph)
        ##############################

    ################
    """
    #Functions:
    set_roads_array - Creates a list of all the roads in the graph
    make_node_dict - Creates a dictionary converting between all the nodes and their node_id
    set_adjacney_roads - Adding to all the roads a list of all the adjacent roads for each road
    make_src_node_to_dest_node_dict- Creates a dictionary converting between all the source nodes and their destination nodes
    make_dest_node_to_src_node_dict- Creates a dictionary converting between all the destination nodes and their source nodes

    calc_dist_mat - Creates a distance matrix of all the roads in the graph
    set_graph - Sets a graph for the simulation



    """

    ###############
    def set_roads_array(self):
        node_to_edge = self.make_node_dict()
        for edge in self.graph.edges:
            new_road = Road.Road(self.graph.edges[edge]['edge_id'], node_to_edge[edge[0]], node_to_edge[edge[1]],
                                 self.graph.edges[edge]['length'],
                                 self.graph.edges[edge]['maxspeed'])
            self.roads_array.append(new_road)
            # print(new_road)
        return

    def make_node_dict(self):
        # makes a dictionary of all the nodes and their id
        # node- osm node
        # node_id - the id of the node
        node_to_node_id = {}
        for i in self.graph.nodes:
            if i not in node_to_node_id:
                node_to_node_id[i] = []
            node_to_node_id[i] = (self.graph.nodes[i]['node_id'])
        return node_to_node_id

    def set_adjacney_roads(self):
        # method:
        # 1. iterate over all the edges
        # 2. for each edge, take the destination node
        # 3. find all the edges that have the same node as their source node
        # 4. add them to the edge's adjacent_roads list
        node_to_edge = {}
        for edge1 in self.roads_array:
            dest_node = edge1.get_destination_node()
            for edge2 in self.roads_array:
                src_node = edge2.get_source_node()
                if dest_node == src_node:
                    edge1.adjacent_roads.append(edge2.get_id())
        return

    def set_roads_speeds(self):
        for road in self.roads_array:
            road.update_speed(self.roads_speeds[road.get_id()])
        pass

    def generate_random_speeds(self):
        start_time=0
        for road in self.roads_array:
            self.roads_speeds[road.get_id()] = (random.randint(25,int(road.get_max_speed())))
        # print(self.roads_speeds)
        return

    def calc_dist_mat(self):
        # makes a matrix of the shortest distances between all the roads
        return pd.DataFrame.from_dict(dict(nx.all_pairs_dijkstra_path_length(self.graph)), orient='index')
    def make_src_node_to_dest_node_dict(self):
        src_to_dest = {}
        for edge in self.roads_array:
            if edge.get_source_node() not in src_to_dest:
                src_to_dest[edge.get_source_node()] = []
            src_to_dest[edge.get_source_node()].append(edge.get_destination_node())
        #print(src_to_dest)
        return src_to_dest

    def make_dest_node_to_src_node_dict(self):
        # make_dest_node_to_src_node_
        dest_to_src = {}
        for edge in self.roads_array:
            if edge.get_destination_node() not in dest_to_src:
                dest_to_src[edge.get_destination_node()] = []
            dest_to_src[edge.get_destination_node()].append(edge.get_source_node())
        #print(dest_to_src)
        return dest_to_src

    # GETS
    def get_graph(self):
        return self.graph

    def get_roads_array(self):
        return self.roads_array

    def get_roads_speeds(self):
        return self.roads_speeds

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def get_road_by_road_id(self, road_id):
        return self.roads_array[road_id]

    # def set_connectivity_list(self):



    def set_graph(self, graph_path):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        return ox.load_graphml(data + graph_path)

    def __str__(self):
        return "Road_Network"

    # class Route(ABC):
    #     @abstractmethod
    #     def get_next_road(self, source_road, destination_node, time):
    #         pass
    #
    #     @abstractmethod
    #     def decide_first_road(self, source_node):
    #         pass
    # class Random_route(Route):
    #     def decide_first_road(self, source_node):
    #         for road in Road_Network.get_roads_array():
    #             if road.get_source_node() == source_node:
    #                 return road
    #
    #     def get_next_road(self, source_road, destination_node, time):
    #         """
    #         :param source_road: Road id
    #         :param destination_node:
    #         :param time: 0 for now
    #         :return:  next road to travel to : Road
    #         """
    #         # TODO: update according to connectivity list implementation
    #         road = Road_Network.get_road_by_road_id(source_road)
    #         optional_roads = road.get_adjacent_roads()  # list of IDs of optional roads
    #         choice = random.randint(0, len(optional_roads) - 1)
    #         next_road = optional_roads[choice]
    #         return next_road
    #
    # class Q_Learning_Route(Route):
    #     def get_next_road(self, source_road, destination_node, time):
    #         # Implement Q-learning route logic here
    #         # Return a new edge based on the Q-learning algorithm
    #         pass
    #
    # class Shortest_path_route(Route):
    #
    #     def get_next_road(self, source_node, destination_node, time):
    #         # TODO: update according to distance matrix implementation
    #         return Road_Network.get_distance_matrix().get_road(source_node, destination_node)

#


