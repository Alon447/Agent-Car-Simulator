import itertools
import copy
import random

import Cars


class Road:

    def __init__(self, id, start_node, end_node, edge_index, length, max_speed, cars_queue):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.edge_index = edge_index  # edge is a tuple of the form (u, v, key)
        self.length = length # the length of the road
        self.max_speed = int(max_speed)
        self.cur_speed = random.randint(1, self.max_speed - 10)  # the current speed of the road
        self.cars_queue = cars_queue  # a list of the current cars on the road
        self.time_to_cross = self.length/self.cur_speed  # the time it takes to cross the road
        self.is_blocked = False
        # self.next_queue = copy.deepcopy(self.cars_queue)  # a list of the cars that will be on the road in the next state
        # self.max_length = max_length  # we need to define a mex length for the queue

    # GETS
    def get_id(self):
        return self.id

    def get_start_node(self):
        return self.start_node

    def get_end_node(self):
        return self.end_node

    def get_edge_graph_index(self):
        # return a tuple of the form (u, v, key)
        return self.edge_index

    def get_max_speed(self):
        return self.max_speed

    def get_current_speed(self):
        return self.cur_speed

    def get_num_cars_in_road(self):
        return len(self.cars_queue)

    def get_cars_queue(self):
        return self.cars_queue

    # SETS

    def set_current_speed(self, cur_speed):
        self.cur_speed = cur_speed

    def set_cars_queue(self, cars_queue):
        self.cars_queue = cars_queue

    # FUNCTIONS FOR USE

    # def add_cars(self, cars):
    #     # Tries to add the cars to the next queue
    #     # we need to address what to do to the cars that can't be added
    #     # self.next_queue = copy.deepcopy(self.cars_queue)
    #     for i in range(len(cars)):
    #         if len(self.next_queue) == self.max_length:
    #             print("********************")
    #             print("THE QUEUE IS FULL")
    #             print("********************")
    #             return
    #         self.next_queue.append(cars.pop(0))

    # def remove_cars(self, num_cars):
    #     # Removes the cars from the queue if they can move to next edge
    #     cars_list = copy.deepcopy(self.cars_queue[:num_cars - 1])
    #     self.next_queue = self.cars_queue[num_cars:]

    # def update(self):
    #     self.cars_queue = self.next_queue
    #     self.next_queue = copy.deepcopy(self.cars_queue)
    #     # NOW WE NEED TO UPDATE THE SPEED ACCORDING TO THE QUEUE
    #     # self.set_cur_speed()

    # def calculate_speed(self):
    #     # calculate the speed according to the queue and LWR model
    #     cur_speed = self.max_speed * (1 - (self.get_num_cars() / self.max_length))
    #     return cur_speed

    def update_time_to_cross(self):
        # calculate the time it takes to cross the road
        self.time_to_cross = self.length/self.cur_speed

    def block_road(self):
        # block the road
        self.is_blocked = True
        self.cur_speed = 0
        self.time_to_cross = float('inf')

    def unblock_road(self):
        # unblock the road
        self.is_blocked = False
        self.cur_speed = random.randint(1, self.max_speed - 10)
        self.update_time_to_cross()

    def __str__(self):
        return "road_id: " + str(self.id) + "\n" + "start node: " + str(self.start_node) + "\n" + "end node: " + str(
            self.end_node) + "\n" + "edge_index: " + str(self.edge_index) + "\n" + "max_speed: " \
               + str(self.max_speed) + "\n" + "cur_speed: " + str(self.cur_speed) + \
               "\n" + "cars_queue: " + str(self.cars_queue) + "\n" + "next_queue: " + "\n"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node
