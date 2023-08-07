import datetime
import os
import time

import osmnx as ox
import Road
import pandas as pd
import networkx as nx
import random

import Utilities.Getters as Getters

from Main_Files import Node


class Road_Network:
    """
    Road_Network class:
    This class represents a road network, containing the graph of the simulation,
    all the roads in the graph, and related data.

    Attributes:
    graph (networkx.Graph): The road network graph.
    roads_array (list): List of all road objects in the graph.
    nodes_array (list): List of all node objects in the graph.
    node_connectivity_dict (dict): Mapping of node IDs to connected node IDs.
    blocked_roads_array (list): List of road IDs that are currently blocked.

    """
    def __init__(self, graph_path, activate_traffic_lights = False):

        # Graph
        self.graph = Getters.get_graph(graph_path)

        # Edges and Nodes
        self.roads_array = [] # list of all the roads in the graph
        self.nodes_array = [] # list of all the nodes in the graph

        self.node_connectivity_dict = {} # node id to list of connected nodes ids
        self.blocked_roads_array = []

        # Initialize functions
        self.set_nodes_array()
        self.set_roads_array(activate_traffic_lights)
        self.set_adjacency_roads()

        # for shortest path
        self.next_node_matrix = [[-1] * len(self.nodes_array) for _ in range(len(self.nodes_array))] # cache for the distance matrix, saves the next node in the shortest path
        self.distances_matrix = [[-1] * len(self.nodes_array) for _ in range(len(self.nodes_array))] # cache for the distance matrix, saves the shortest distance between two nodes

        self.update_eta()
        # for q learning
        self.shortest_time_matrix = [[-1] * len(self.nodes_array) for _ in range(len(self.nodes_array))] # cache for the shortest time matrix, saves the shortest time between two nodes
    # Functions:

    def set_nodes_array(self):
        """
        Initialize and populate the nodes_array attribute with Node objects.

        Returns:
        None
        """
        for i, node in enumerate(self.graph.nodes):
            id = i
            osm_id = int(node)
            x = self.graph.nodes[node].get('x')
            y = self.graph.nodes[node].get('y')
            if self.graph.nodes[node].get('highway') == 'traffic_signals':
                traffic_lights = True
            else:
                traffic_lights = False
            street_count = self.graph.nodes[node].get('street_count')
            new_node = Node.Node(id, osm_id, x, y, traffic_lights, street_count)
            self.nodes_array.append(new_node)
        return
    def set_roads_array(self, activate_traffic_lights):
        """
        Initialize and populate the roads_array attribute with Road objects.

        Args:
        activate_traffic_lights (bool): Whether to activate traffic lights for roads.

        Returns:
        None
        """
        for edge in self.graph.edges:
            start_node = self.get_node_from_osm_id(edge[0])
            end_node = self.get_node_from_osm_id(edge[1])

            new_road = Road.Road(int(self.graph.edges[edge]['edge_id']), start_node ,end_node,
                                 self.graph.edges[edge]['length'], int(self.graph.edges[edge]['maxspeed']), activate_traffic_lights)
            self.roads_array.append(new_road)
            # self.road_dict[(new_road.source_node.id,new_road.destination_node.id)] = new_road.id
            start_node_id = start_node.id
            if start_node_id in self.node_connectivity_dict and isinstance(self.node_connectivity_dict[start_node_id], list):
                self.node_connectivity_dict[start_node_id].append(new_road.destination_node.id)
            else:
                self.node_connectivity_dict[start_node_id] = [new_road.destination_node.id]

            # print(new_road)
        return

    def update_eta(self):
        for edge in self.graph.edges:
            if edge[2]!=1:
                self.graph.edges[edge]['eta'] = float(self.graph.edges[edge]['length']) / float(self.graph.edges[edge]['current_speed'])
        return

    def set_adjacency_roads(self):
        """
        Set the adjacent_roads attribute for each road in the roads_array.

        Returns:
        None
        """
        # method:
        # 1. iterate over all the edges
        # 2. for each edge, take the destination node
        # 3. find all the edges that have the same node as their source node
        # 4. add them to the edge's adjacent_roads list
        for edge1 in self.roads_array:
            dest_node = edge1.destination_node.id
            for edge2 in self.roads_array:
                src_node = edge2.source_node.id
                if dest_node == src_node:
                    edge1.adjacent_roads.append(edge2)
        return
    def remove_blocked_roads(self):
        """
        Remove roads from roads_array that have no adjacent roads.

        Returns:
        None
        """
        for road in self.roads_array:
            if len(road.adjacent_roads) == 0:
                self.roads_array.remove(road)
        return

    def block_road(self,road_id):
        """
        Block a specific road by marking it as blocked.

        Args:
        road_id (int): ID of the road to be blocked.

        Returns:
        None
        """
        #print("block road")
        #print(road_id)
        self.roads_array[road_id].is_blocked = True
        self.blocked_roads_array.append(road_id)
        return

    def unblock_road(self,road_id):
        """
        Unblock a specific road by marking it as unblocked.

        Args:
        road_id (int): ID of the road to be unblocked.

        Returns:
        None
        """
        #print("unblock road")
        #print(road_id)
        self.roads_array[road_id].is_blocked = False
        self.blocked_roads_array.remove(road_id)
        return

    def unblock_all_roads(self):
        """
        Unblock all previously blocked roads.

        Returns:
        None
        """
        for road in self.blocked_roads_array:
            self.unblock_road(road)
        return

    def set_roads_speeds_from_dict(self, roads_speeds:dict, current_time:str):
        """
        Update road speeds based on the provided speeds dictionary and current time.

        Args:
        roads_speeds (dict): Dictionary of road_id: speed for different times of the day.
        current_time (str): Current time in the simulation.
        activate_traffic_lights (bool): Whether to activate traffic lights for roads.

        Returns:
        None
        """
        for road in self.roads_array:
            road_id = road.id
            road.update_road_speed_dict(roads_speeds[str(road_id)]) # update the road's speed dict
            road.update_speed(current_time) # update the road's current speed
        return
    def update_roads_speeds(self, current_time:str):
        """
        Update road speeds based on the current time.

        Args:
        current_time (str): Current time in the simulation.

        Returns:
        None
        """
        for road in self.roads_array:
            road.update_speed(current_time)
        return

    def get_shortest_time_between_nodes(self, id1, id2):
        if nx.has_path(self.graph, self.nodes_array[id1].osm_id, self.nodes_array[id2].osm_id):
            return nx.shortest_path_length(self.graph, self.nodes_array[id1].osm_id, self.nodes_array[id2].osm_id, weight='eta')
        return -1

    # def calc_dist_mat(self):
    #     # makes a matrix of the shortest distances between all the roads
    #     return pd.DataFrame.from_dict(dict(nx.all_pairs_dijkstra_path_length(self.graph)), orient='index')
    # def make_src_node_to_dest_node_dict(self):
    #     src_to_dest = {}
    #     for edge in self.roads_array:
    #         if edge.source_node.id not in src_to_dest:
    #             src_to_dest[edge.source_node.id] = []
    #         src_to_dest[edge.source_node.id].append(edge.destination_node.id)
    #     #print(src_to_dest)
    #     return src_to_dest
    #
    # def make_dest_node_to_src_node_dict(self):
    #     # make_dest_node_to_src_node_
    #     dest_to_src = {}
    #     for edge in self.roads_array:
    #         if edge.destination_node.id not in dest_to_src:
    #             dest_to_src[edge.destination_node.id] = []
    #         dest_to_src[edge.destination_node.id].append(edge.source_node.id)
    #     #print(dest_to_src)
    #     return dest_to_src

    """
    Shortest Path Functions
    """
    def add_shortest_path_to_matrix(self, src: int, dest: int):
        """
        Add the shortest path between two nodes to the distances matrix.

        Args:
        src (int): Source node ID.
        dest (int): Destination node ID.

        Returns:
        None
        """

        osm_src = self.nodes_array[src].osm_id
        osm_dest = self.nodes_array[dest].osm_id
        # nodes are the osm nodes
        path = nx.shortest_path(self.graph, osm_src, osm_dest, weight='length')
        path_length = nx.shortest_path_length(self.graph, osm_src, osm_dest, weight='length')
        fixed_path=[]
        for node in path:
            new_node = self.get_node_from_osm_id(node)
            fixed_path.append(new_node.id)

        #updating the distances matrix
        previous_edge_length = 0
        for i,node in enumerate(fixed_path[:-1]):
            self.next_node_matrix[node][fixed_path[-1]] = fixed_path[i + 1]#adds the relevant next node to the distances matrix
            self.distances_matrix[node][fixed_path[-1]] = path_length - previous_edge_length
            # previous_edge_length += self.roads_array[self.road_dict[(node,fixed_path[i + 1])]].length
            previous_edge_length += self.get_road_from_src_dst(node,fixed_path[i + 1]).length
        return

    def get_next_road_from_matrix(self,src_id,dst_id):
        """
        Get the next road on the shortest path from the matrix.

        Args:
        src_id (int): Source node ID.
        dst_id (int): Destination node ID.

        Returns:
        Road object: Next road on the shortest path.
        """
        return self.get_road_from_src_dst(src_id,self.next_node_matrix[src_id][dst_id])
    def get_next_road_shortest_path(self, src_id, dst_id):
        """
        Get the next road on the shortest path, calculating if needed.

        Args:
        src_id (int): Source node ID.
        dst_id (int): Destination node ID.

        Returns:
        Road object: Next road on the shortest path.
        """
        #checks if the next node is filled in the distance matrix.
        #if it is, returns the next road. otherwise, calculate path and update matrix.
        if self.next_node_matrix[src_id][dst_id] == -1:
            self.add_shortest_path_to_matrix(src_id,dst_id)
        return self.get_next_road_from_matrix(src_id,dst_id)

    """
    GET FUNCTIONS
    """
    def get_xy_from_node_id(self, node_id:int):
        """
        Get x, y coordinates of a node based on its node ID.

        Args:
        node_id (int): Node ID.

        Returns:
        tuple: x, y coordinates.
        """
        return self.nodes_array[node_id].x, self.nodes_array[node_id].y
    def get_xy_from_osm_id(self, osm_id: int):
        """
        Get x, y coordinates of a node based on its OSM ID.

        Args:
        osm_id (int): OSM ID of the node.

        Returns:
        tuple: x, y coordinates.
        """
        node = self.get_node_from_osm_id(osm_id)
        return node.x, node.y

    def get_node_from_osm_id(self, osm_id: int):
        """
        Get a node object based on its OSM ID.

        Args:
        osm_id (int): OSM ID of the node.

        Returns:
        Node object: Node corresponding to the OSM ID.
        """
        for node in self.nodes_array:
            if node.osm_id == osm_id:
                return node
        return None

    def get_road_from_src_dst(self, src_id, dst_id):
        """
        Get a road object based on source and destination node IDs.

        Args:
        src_id (int): Source node ID.
        dst_id (int): Destination node ID.

        Returns:
        Road object: Road between the source and destination nodes.
        """
        for road in self.roads_array:
            if road.source_node.id == src_id and road.destination_node.id == dst_id:
                return road
        return None

    def get_shortest_path(self, src_id, dst_id):
        """
        Get the shortest path between two node IDs.

        Args:
        src_id (int): Source node ID.
        dst_id (int): Destination node ID.

        Returns:
        list: List of node IDs representing the shortest path.
        """
        osm_src = self.nodes_array[src_id].osm_id
        osm_dest = self.nodes_array[dst_id].osm_id
        path = nx.shortest_path(self.graph, osm_src, osm_dest, weight='length')
        fixed_path = []
        for node in path:
            new_node = self.get_node_from_osm_id(node)
            fixed_path.append(new_node.id)
        if self.check_if_path_is_blocked(fixed_path): # if the path is blocked, return None
            return None
        # else, return the path
        return fixed_path

    def check_if_path_is_blocked(self, path):
        """
        Check if a given path is blocked by any blocked roads.

        Args:
        path (list): List of node IDs representing a path.

        Returns:
        bool: True if the path is blocked, False otherwise.
        """
        for i, node in enumerate(path[:-1]):
            if self.get_road_from_src_dst(node, path[i + 1]).is_blocked:
                return True
        return False
    def __str__(self):
        """
        Return a string representation of the Road_Network class.

        Returns:
        str: String representation.
        """
        return f'Road_Network: Roads: {self.roads_array}, Nodes: {self.nodes_array}'

    def __repr__(self):
        """
        Return a string representation of the Road_Network class.

        Returns:
        str: String representation.
        """
        return "Road_Network"





