import math
import random

import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
from matplotlib import pyplot as plt

import new_master.Road as Road
import Road_Network, Road


def set_up_roads():
    road1 = Road.Road(1, 0, 1, 1, 50)
    road2 = Road.Road(2, 1, 2, 1, 50)
    road3 = Road.Road(3, 1, 3, 1, 50)
    road4 = Road.Road(4, 3, 4, 1, 50)
    road5 = Road.Road(5, 4, 5, 1, 50)
    road6 = Road.Road(6, 6, 5, 1, 50)
    road7 = Road.Road(7, 8, 6, 1, 50)
    road8 = Road.Road(8, 7, 8, 1, 50)
    road9 = Road.Road(9, 8, 0, 1, 50)
    road10 = Road.Road(10, 1, 7, 3, 50)
    road11 = Road.Road(11, 9, 1, 1, 50)
    road12 = Road.Road(12, 7, 3, 1, 50)
    road13 = Road.Road(13, 4, 9, 1, 50)
    road14 = Road.Road(14, 5, 9, 1, 50)
    road15 = Road.Road(15, 5, 7, 1, 50)
    road16 = Road.Road(16, 9, 6, 1, 50)
    road17 = Road.Road(17, 6, 7, 1, 50)
    road18 = Road.Road(18, 6, 0, 1, 50)
    # road19=Road.Road(19,2,60,50)

    road_list = []
    road_list.append(road1)
    road_list.append(road2)
    road_list.append(road3)
    road_list.append(road4)
    road_list.append(road5)
    road_list.append(road6)
    road_list.append(road7)
    road_list.append(road8)
    road_list.append(road9)
    road_list.append(road10)
    road_list.append(road11)
    road_list.append(road12)
    road_list.append(road13)
    road_list.append(road14)
    road_list.append(road15)
    road_list.append(road16)
    road_list.append(road17)
    road_list.append(road18)

    for edge1 in road_list:
        dest_node = edge1.get_destination_node()
        for edge2 in road_list:
            src_node = edge2.get_source_node()
            if dest_node == src_node:
                edge1.adjacent_roads.append(edge2)
    return road_list
def make_node_dict(g):
    # makes a dictionary of all the nodes and their id
    # node- osm node
    # node_id - the id of the node
    node_to_node_id = {}
    for i in g.nodes:
        if i not in node_to_node_id:
            node_to_node_id[i] = []
        node_to_node_id[i] = (g.nodes[i]['node_id'])
    return node_to_node_id

def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if int(val) == value:
            return key
def transform_node_id_route_to_osm_id_route(route,osm_node_to_node_id):
    osm_route = []
    for node in route:
        osm_route.append(get_key_from_value(osm_node_to_node_id, node))
    return osm_route

def calculate_distance(x1,y1,x2,y2):
    # Convert degrees to radians
    lat1 = math.radians(x1)
    lon1 = math.radians(y1)
    lat2 = math.radians(x2)
    lon2 = math.radians(y2)

    # Radius of the Earth in kilometers
    radius = 6371

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 1000 * radius * c # return distance in meters

    return distance
def calculate_reward(road, dest_node):
    current_speed = road.get_current_speed()
    road_length = road.get_length()
    road_src_node = road.get_source_node_attributes()
    road_dest_node = road.get_destination_node_attributes()

    #TODO: need to calculate if road_dest_node is closer to dest_node than road_src_node
    src_distance = calculate_distance(road_src_node[2],road_src_node[3], dest_node[2],dest_node[3])
    dst_distance = calculate_distance(road_dest_node[2],road_dest_node[3], dest_node[2],dest_node[3])



    # Speed reward
    speed_difference = current_speed

    # Length reward
    length_reward = -road_length

    # Distance reward
    distance = dst_distance - src_distance

    # distance_reward = -distances[src][dest]

    total_reward =   distance-100

    return total_reward

def Q_Learning(start_node,end_node):


    # g = ox.load_graphml('../test/tel aviv.graphml')
    # osm_node_to_node_id = make_node_dict(g)
    RN = Road_Network.Road_Network('/tel aviv.graphml')
    start=start_node
    end=end_node

    road_list=RN.roads_array
    node_list=RN.node_roads_count
    # for edge in g.edges:
    #     new_road = Road.Road(g.edges[edge]['edge_id'], osm_node_to_node_id[edge[0]], osm_node_to_node_id[edge[1]],
    #                          g.edges[edge]['length'],50)
    #     road_list.append(new_road)
    # for edge1 in road_list:
    #     dest_node = edge1.get_destination_node()
    #     for edge2 in road_list:
    #         src_node = edge2.get_source_node()
    #         if dest_node == src_node:
    #             edge1.adjacent_roads.append(edge2)

    # start implementing q learning
    len_of_node_list = list(node_list)[-1]

    destination_osmid = RN.reverse_node_dict[end] # destination node osm id
    destination_node_attributes = RN.graph_nodes[end] # destination node attribute
    # distances = nx.shortest_path_length(g, target=destination, weight='length')


    q_values = []
    for i in range(len_of_node_list+1):
        row_values = []
        if node_list.get(i) is None:
            q_values.append([])
            continue
        for j in range(len(node_list[i])):
            row_values.append(0)
        q_values.append(row_values)


    rewards = []
    for i in range(len_of_node_list+1):
        if len(q_values[i]) == 0:
            rewards.append(-10000)
            continue
        row_values = []
        for j in range(len(node_list[i])):
            if i == end:
                row_values.append(0)
            else:
                road_id = node_list[i][j]
                road = RN.roads_array[road_id]
                row_values.append(calculate_reward(road,destination_node_attributes))
        rewards.append(row_values)

    epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9 #discount factor for future rewards
    learning_rate = 0.9 #the rate at which the AI agent should learn
    def is_terminal_state(index):
      #if the reward for this location is -10000, then it is a terminal state
      if rewards[index] == -10000.:
        return True
      else:
        return False

    def get_next_action(current_node_index, epsilon):

        if np.random.uniform(0, 1) > epsilon:
            # random
            length = len(node_list[current_node_index])
            action_index = np.random.randint(length)
            # next_road = adjacent_roads[action_index]
        else:
            # greedy
            if len(q_values[current_node_index]) == 0:
                action_index = -1
                return action_index

            action_index = np.argmax(q_values[current_node_index])
            # next_road = current_road.get_adjacent_roads()[action_index]

        return action_index

    def get_next_road(current_node_index, action_index):
        road = RN.roads_array[node_list[current_node_index][action_index]]
        return road

    shortest_route = ox.shortest_path(RN.graph, orig=RN.reverse_node_dict[start], dest=RN.reverse_node_dict[end], weight='length')
    shortest_route=transform_node_id_route_to_osm_id_route(shortest_route, RN.reverse_node_dict)
    for episode in range(5000):
        current_node_index=start

        while not current_node_index == end:
            """"
            state - current node
            action - next road
            """
            action_index = get_next_action(current_node_index, epsilon)
            if action_index == -1:
                q_values[current_node_index]=-10000
                break
            next_road = get_next_road(current_node_index, action_index)
            reward = rewards[current_node_index][action_index]
            if reward == -10000:
                q_values[current_node_index][action_index]= -10000
                break

            old_q_value = q_values[current_node_index][action_index]
            temporal_difference = reward + (discount_factor * np.max(q_values[current_node_index])) - old_q_value

            # update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[current_node_index][action_index] = new_q_value
            current_node_index = next_road.get_destination_node()
            #print("episode: ", episode)


    print('Training complete!')

    def find_starting_road():
        for road in road_list:
            if road.get_source_node() == TESTING_START_NODE:
                return road

    src=TESTING_START_NODE
    dest=TESTING_END_NODE
    path=[src]
    current_road = find_starting_road()
    current_node_index = current_road.get_destination_node()
    path.append(current_node_index)
    count=0
    is_dest_reached = False
    while current_node_index != dest and count<20:
        q_value = q_values[int(current_road.get_id())]
        if len(q_value) == 0:
            print("No adjacent roads")
            break
        action = np.argmax(q_value)
        next_road = current_road.get_adjacent_roads()[action]
        next_node_index = next_road.get_destination_node()
        current_node_index = next_node_index
        if current_node_index in path[1:]:
            path.append(current_node_index)
            print("Loop detected")
            break
        path.append(current_node_index)
        current_road = next_road
        count+=1
        if current_node_index == dest:
            is_dest_reached = True
            break

    print("Path:", path)




    route = transform_node_id_route_to_osm_id_route(path,RN.reverse_node_dict)
    # print("Route:", route)
    # fig, ax = ox.plot_graph(RN.graph, show=False, close=False, edge_color='lightgray', node_color='gray', bgcolor='black')

    # Plot the custom route
    # if is_dest_reached:
    #     ox.plot_graph_route(g, route, route_color='pink', route_linewidth=6, ax=ax)
    # else:
    #     ox.plot_graph_route(g, route, route_color='red', route_linewidth=6, ax=ax)

    # Show the plot
    #plt.show()
    return is_dest_reached

test_res={}
end=[0,1,2,3,4,5,6,7,9,11,12,13]
for i in end:
    print(i)
    test_res[i] = Q_Learning(10,i)
    # end+=2
print(test_res)
total_values = len(test_res)
false_count = sum(value == False for value in test_res.values())
false_percentage = (false_count / total_values) * 100
print("True percentage:", 100-false_percentage)