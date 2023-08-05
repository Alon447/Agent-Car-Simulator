import datetime
import os
import osmnx as ox
import Road
import pandas as pd
import networkx as nx
import random
import numpy as np


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
    def __init__(self, graph_path, start_time = datetime.datetime(year=2023,month=6,day=29,hour=8, minute=0, second=0)):
        # graph
        self.graph = self.set_graph(graph_path)
        self.roads_array = []
        self.graph_nodes = {} # dict that includes: 0. node_id 1. osm_id 2.x (longtitude) 3.y (latitude) 4. street_count 5. traffic_light

        self.node_dict={} # maps osm ids to our new ids
        self.reverse_node_dict={} # maps our new ids to osm ids
        self.road_dict = {}
        self.node_connectivity_dict = {} # node id to list of connected nodes ids
        self.blocked_roads_array = []

        # initialize functions
        self.make_node_dict()
        self.set_graph_nodes()
        self.set_roads_array()
        self.set_adjacency_roads()
        # self.make_graph_edges_csv()

        # for shortest path
        self.next_node_matrix = [[-1] * len(self.node_dict) for _ in range(len(self.node_dict))] # cache for the distance matrix
        self.distances_matrix = [[-1] * len(self.node_dict) for _ in range(len(self.node_dict))] # cache for the distance matrix



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
    ################
    # Functions:
    def set_graph_nodes(self):
        for node in self.graph.nodes:
            traffic_light = self.graph.nodes[node].get('highway')
            if traffic_light == 'traffic_signals':
                self.graph_nodes[self.node_dict[node]] = [self.node_dict[node], int(node),self.graph.nodes[node].get('x'), self.graph.nodes[node].get('y'),self.graph.nodes[node].get('street_count'), True]
            else:
                self.graph_nodes[self.node_dict[node]] = [self.node_dict[node], int(node),self.graph.nodes[node].get('x'), self.graph.nodes[node].get('y'),self.graph.nodes[node].get('street_count'), False]

        return
    def set_roads_array(self):
        for edge in self.graph.edges:
            start_node = self.node_dict[edge[0]]
            start_node_attributes = self.graph_nodes[start_node]
            end_node =self.node_dict[edge[1]]
            end_node_attributes = self.graph_nodes[end_node]
            new_road = Road.Road(int(self.graph.edges[edge]['edge_id']), start_node_attributes ,end_node_attributes,
                                 self.graph.edges[edge]['length'],int(self.graph.edges[edge]['maxspeed']))
            self.roads_array.append(new_road)
            self.road_dict[(new_road.source_node[0],new_road.destination_node[0])] = new_road.id
            if start_node in self.node_connectivity_dict and isinstance(self.node_connectivity_dict[start_node], list):
                self.node_connectivity_dict[start_node].append(new_road.destination_node[0])
            else:
                self.node_connectivity_dict[start_node] = [new_road.destination_node[0]]

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
            node_to_node_id[i] = (int(self.graph.nodes[i]['node_id']))
        self.node_dict= node_to_node_id
        self.reverse_node_dict= {value: int(key) for key, value in self.node_dict.items()}
        return node_to_node_id

    def set_adjacency_roads(self):
        # method:
        # 1. iterate over all the edges
        # 2. for each edge, take the destination node
        # 3. find all the edges that have the same node as their source node
        # 4. add them to the edge's adjacent_roads list
        node_to_edge = {}
        for edge1 in self.roads_array:
            dest_node = edge1.destination_node[0]
            for edge2 in self.roads_array:
                src_node = edge2.source_node[0]
                if dest_node == src_node:
                    edge1.adjacent_roads.append(edge2)
        return

    def make_graph_edges_csv(self):
        edges = []
        for road in self.roads_array:
            edges.append([road.source_node[0],road.destination_node[0],road.get_eta()])
        df = pd.DataFrame(edges, columns=['source', 'target', 'eta'])
        df.to_csv('../data/graph_edges.csv', index=False)
        return

    def remove_blocked_roads(self):
        for road in self.roads_array:
            if len(road.adjacent_roads) == 0:
                self.roads_array.remove(road)
        return

    def block_road(self,road_id):
        #print("block road")
        #print(road_id)
        self.roads_array[road_id].is_blocked = True
        self.blocked_roads_array.append(road_id)
        return

    def unblock_road(self,road_id):
        #print("unblock road")
        #print(road_id)
        self.roads_array[road_id].is_blocked = False
        self.blocked_roads_array.remove(road_id)
        return

    def unblock_all_roads(self):
        for road in self.blocked_roads_array:
            self.unblock_road(road)
        return

    def set_roads_speeds_from_dict(self, roads_speeds:dict, current_time:str, activate_traffic_lights:bool):
        """
        iterates over all the roads in the graph and updates their speed based on the roads_speeds dict
        :param roads_speeds: dict of road_id: speed for every 10 minutes in the day
        :param current_time: str that represents the current time in the simulation for example: '08:00'
        :return:
        """
        for road in self.roads_array:
            road_id = road.id
            # src = road.source_node[1]
            # dst = road.destination_node[1]
            road.update_road_speed_dict(roads_speeds[str(road_id)])
            eta = road.update_speed(current_time, activate_traffic_lights) # False repesents the activate traffic lights, the simulation hasnt started so it doesnt matter yet
            # graph_road = self.graph[src][dst][0]
        return
    def update_roads_speeds(self, current_time:str, activate_traffic_lights:bool):
        for road in self.roads_array:
            eta = road.update_speed(current_time, activate_traffic_lights)
        return



    # def calc_dist_mat(self):
    #     # makes a matrix of the shortest distances between all the roads
    #     return pd.DataFrame.from_dict(dict(nx.all_pairs_dijkstra_path_length(self.graph)), orient='index')
    def make_src_node_to_dest_node_dict(self):
        src_to_dest = {}
        for edge in self.roads_array:
            if edge.source_node[0] not in src_to_dest:
                src_to_dest[edge.source_node[0]] = []
            src_to_dest[edge.source_node[0]].append(edge.destination_node[0])
        #print(src_to_dest)
        return src_to_dest

    def make_dest_node_to_src_node_dict(self):
        # make_dest_node_to_src_node_
        dest_to_src = {}
        for edge in self.roads_array:
            if edge.destination_node[0] not in dest_to_src:
                dest_to_src[edge.destination_node[0]] = []
            dest_to_src[edge.destination_node[0]].append(edge.source_node[0])
        #print(dest_to_src)
        return dest_to_src

    """
    Shortest Path Functions
    """
    def add_shortest_path_to_matrix(self, src, dest):
        #src and destination are node ids as we defined in the graph
        #we need to get the osm node ids to use the networkx's shortest path function
        temp_src = self.reverse_node_dict[src]
        temp_dest = self.reverse_node_dict[dest]
        # nodes are the osm nodes
        path = nx.shortest_path(self.graph, temp_src, temp_dest, weight='length')
        path_length = nx.shortest_path_length(self.graph, temp_src, temp_dest, weight='length')
        fixed_path = [self.node_dict[node] for node in path]

        #updating the distances matrix
        previous_edge_length = 0
        for i,node in enumerate(fixed_path[:-1]):
            self.next_node_matrix[node][fixed_path[-1]] = fixed_path[i + 1]#adds the relevant next node to the distances matrix
            self.distances_matrix[node][fixed_path[-1]] = path_length - previous_edge_length
            previous_edge_length += self.roads_array[self.road_dict[(node,fixed_path[i + 1])]].length

    def get_next_road_from_matrix(self,src_id,dst_id):
        return self.roads_array[self.road_dict[(src_id,self.next_node_matrix[src_id][dst_id])]]

    def get_next_road_shortest_path(self, src_id, dst_id):
        #checks if the next node is filled in the distance matrix.
        #if it is, returns the next road. otherwise, calculate path and update matrix.
        if self.next_node_matrix[src_id][dst_id] == -1:
            self.add_shortest_path_to_matrix(src_id,dst_id)
        return self.get_next_road_from_matrix(src_id,dst_id)

    """
    GET FUNCTIONS
    """
    #
    # def get_graph(self):
    #     return self.graph
    #
    # def get_node_connectivity_dict(self):
    #     return self.node_connectivity_dict
    # def get_roads_array(self):
    #     return self.roads_array
    def get_xy_from_node_id(self, node_id:int):
        """

        :param node_id: the id of the node
        :return:  x,y coordinates of the node
        """
        return self.graph_nodes[node_id][2], self.graph_nodes[node_id][3]
    def get_xy_from_osm_id(self, osm_id:int):
        """

        :param osm_id: the osm id of the node
        :return: x,y coordinates of the node
        """
        osm_id = self.node_dict[osm_id]
        return self.graph_nodes[osm_id][2], self.graph_nodes[osm_id][3]
    # def get_graph_nodes(self):
    #     return self.graph_nodes
    # def get_blocked_roads_array(self):
    #     return self.blocked_roads_array
    def set_graph(self, graph_path):
        cur = os.getcwd()
        parent = os.path.dirname(cur)
        data = os.path.join(parent, "data")
        return ox.load_graphml(data + graph_path)

    def __str__(self):
        return "Road_Network"

    def __repr__(self):
        return "Road_Network"




