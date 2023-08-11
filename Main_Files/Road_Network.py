import datetime
import os
import time

import osmnx as ox
from matplotlib import pyplot as plt

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
    all the roads in the graph, and related Graphs.

    Attributes:
    graph (networkx.Graph): The road network graph.
    roads_array (list): List of all road objects in the graph.
    nodes_array (list): List of all node objects in the graph.
    node_connectivity_dict (dict): Mapping of node IDs to connected node IDs.
    blocked_roads_array (list): List of road IDs that are currently blocked.

    """

    def __init__(self, graph_path, activate_traffic_lights = False, rain_intensity = 0, traffic_white_noise = True):

        # Graph
        self.graph_name = graph_path
        self.graph = Getters.get_graph(graph_path) # use graphml file
        self.nx_graph = None # create_graph() will initialize this attribute
        """
        self.nx_graph attributes:
        nodes - 'osmid', 'x', 'y', 'highway', 'street_count'
        edges - 'id', 'eta', 'current_speed', 'length', 'blocked', 'max_speed'
                        
        """
        # Edges and Nodes
        self.roads_array = [] # list of all the roads in the graph
        self.nodes_array = [] # list of all the nodes in the graph

        self.node_connectivity_dict = {} # node id to list of connected nodes ids
        self.blocked_roads_array = []
        self.blocked_roads_dict = {}  # key: road id, value: list of blocked times


        # Initialize functions
        self.set_nodes_array()
        self.set_roads_array(activate_traffic_lights, rain_intensity)
        self.set_adjacency_roads()
        self.create_graph()

        # Shortest path
        self.next_node_matrix = [[-1] * len(self.nodes_array) for _ in range(len(self.nodes_array))] # cache for the distance matrix, saves the next node in the shortest path
        self.distances_matrix = [[-1] * len(self.nodes_array) for _ in range(len(self.nodes_array))] # cache for the distance matrix, saves the shortest distance between two nodes

        # Flags
        self.traffic_white_noise = traffic_white_noise

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
    def set_roads_array(self, activate_traffic_lights, rain_intensity):
        """
        Initialize and populate the roads_array attribute with Road objects.

        Args:
        activate_traffic_lights (bool): Whether to activate traffic lights for roads.

        Returns:
        None
        """
        for i,edge in enumerate(self.graph.edges):
            # make new road
            id = i
            start_node = self.get_node_from_osm_id(edge[0])
            end_node = self.get_node_from_osm_id(edge[1])
            length = round(self.graph.edges[edge]['length'],2) # round to 2 decimal places
            # max_speed = int(self.graph.edges[edge]['maxspeed'])
            max_speed = (self.graph.edges[edge]['maxspeed'])
            if isinstance(max_speed, list):
                max_speed = int(max_speed[0])  # Use the first element of the list
            else:
                max_speed = int(max_speed)
            type = self.graph.edges[edge]['highway']

            new_road = Road.Road(id, start_node ,end_node, length, max_speed,type, activate_traffic_lights, rain_intensity)

            self.roads_array.append(new_road)

            # update node_connectivity_dict
            start_node_id = start_node.id

            if start_node_id in self.node_connectivity_dict and isinstance(self.node_connectivity_dict[start_node_id], list):
                self.node_connectivity_dict[start_node_id].append(new_road.destination_node.id)
            else:
                self.node_connectivity_dict[start_node_id] = [new_road.destination_node.id]

            # print(new_road)
        return

    def create_graph(self):
        """
        Create a graph from the roads_array attribute.
        :return:
        """
        # Create a MultiDiGraph
        G = nx.MultiDiGraph()

        # Add nodes with attributes to the graph
        for node in self.nodes_array:
            G.add_node(node.id, osm_id = node.osm_id, x = node.x, y = node.y, traffic_lights = node.traffic_lights,
                       street_count = node.street_count)

        # Add directed edges with attributes
        for road in self.roads_array:
            G.add_edge(road.source_node.id, road.destination_node.id, id = road.id,  eta=road.estimated_time, current_speed = road.current_speed,
                       length = road.length, blocked = road.is_blocked, max_speed = road.max_speed)

        self.nx_graph = G
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

    def plan_road_blockage(self, road_id, start_time, end_time):
        """
        Plan a road blockage for a specific road.
        :param road_id:
        :param start_time:
        :param end_time:
        :return:
        """
        self.blocked_roads_dict[road_id] = [start_time, end_time]
        return

    def block_road(self,road_id):
        # TODO: add start and end times
        """
        Block a specific road by marking it as blocked.

        Args:
        road_id (int): ID of the road to be blocked.


        Returns:
        None
        """
        print(road_id,"blocked")
        self.roads_array[road_id].block()

        # update self.nx_graph
        src = self.roads_array[road_id].source_node.id
        dest = self.roads_array[road_id].destination_node.id
        self.nx_graph.edges[src,dest,0]['blocked'] = True
        self.nx_graph.edges[src,dest,0]['eta'] = float('inf')
        self.nx_graph.edges[src,dest,0]['current_speed'] = 0
        self.nx_graph.edges[src,dest,0]['length'] = float('inf')

        # add to self.blocked_roads_array
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
        print(road_id,"unblocked")
        new_eta, new_speed = self.roads_array[road_id].unblock()

        # update self.nx_graph
        src = self.roads_array[road_id].source_node.id
        dest = self.roads_array[road_id].destination_node.id
        self.nx_graph.edges[src, dest, 0]['blocked'] = False
        self.nx_graph.edges[src, dest, 0]['eta'] = new_eta
        self.nx_graph.edges[src, dest, 0]['current_speed'] = new_speed
        self.nx_graph.edges[src,dest,0]['length'] = self.roads_array[road_id].length

        # remove from self.blocked_roads_array
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

    def set_roads_speeds_from_dict(self, roads_speeds:dict, current_time:datetime):
        """
        Update road speeds based on the provided speeds dictionary and current time.

        Args:
        roads_speeds (dict): Dictionary of road_id: speed for different times of the day.
        current_time (datetime): Current time in the simulation.
        activate_traffic_lights (bool): Whether to activate traffic lights for roads.

        Returns:
        None
        """
        for road in self.roads_array:
            road_id = road.id
            road.update_road_speed_dict(roads_speeds[str(road_id)]) # update the road's speed dict
            new_eta = road.update_speed(current_time, self.traffic_white_noise) # update the road's current speed
            src = road.source_node.id
            dest = road.destination_node.id
            self.nx_graph.edges[src, dest, 0]['current_speed'] = road.current_speed
            self.nx_graph.edges[src, dest, 0]['eta'] = new_eta
        return

    def update_roads_speeds(self, current_time:datetime):
        """
        Update road speeds based on the current time.

        Args:
        current_time (datetime): Current time in the simulation.

        Returns:
        None
        """
        for road in self.roads_array:
            new_eta = road.update_speed(current_time, self.traffic_white_noise)
            src = road.source_node.id
            dest = road.destination_node.id
            block = road.is_blocked
            if block:
                print("blocked road",road.id)
            else:
                self.nx_graph.edges[src, dest, 0]['current_speed'] = road.current_speed
                self.nx_graph.edges[src, dest, 0]['eta'] = new_eta
        return

    def get_shortest_time_between_nodes(self, id1, id2):
        if nx.has_path(self.nx_graph, self.nodes_array[id1].osm_id, self.nodes_array[id2].osm_id):
            return nx.shortest_path_length(self.nx_graph, self.nodes_array[id1].osm_id, self.nodes_array[id2].osm_id, weight='eta')
        return -1
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

        path = nx.shortest_path(self.nx_graph, src, dest, weight='length')
        path_length = nx.shortest_path_length(self.nx_graph, src, dest, weight='length')

        #updating the distances matrix
        previous_edge_length = 0
        for i,node in enumerate(path[:-1]):
            self.next_node_matrix[node][path[-1]] = path[i + 1]#adds the relevant next node to the distances matrix
            self.distances_matrix[node][path[-1]] = path_length - previous_edge_length
            previous_edge_length += self.get_road_from_src_dst(node,path[i + 1]).length
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
        # osm_src = self.nodes_array[src_id].osm_id
        # osm_dest = self.nodes_array[dst_id].osm_id
        path = nx.shortest_path(self.nx_graph, src_id, dst_id, weight='length')
        # fixed_path = []
        # for node in path:
        #     new_node = self.get_node_from_osm_id(node)
        #     fixed_path.append(new_node.id)
        if self.check_if_path_is_blocked(path): # if the path is blocked, return None
            return None
        # else, return the path
        return path

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







