import itertools
import copy
import Cars


class Road:

    def __init__(self, id, start_node, end_node, edge_index, max_speed, cars_queue, max_length):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.edge_index = edge_index  # edge is a tuple of the form (u, v, key)
        self.max_speed = max_speed
        self.cur_speed = max_speed
        self.cars_queue = cars_queue  # a list of the current cars on the road
        self.next_queue = copy.deepcopy(self.cars_queue)  # a list of the cars that will be on the road in the next state
        self.max_length = max_length  # we need to define a mex length for the queue

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

    def get_num_cars(self):
        return len(self.cars_queue)

    def get_next_state_num_cars(self):
        return len(self.next_queue)

    def get_cars_queue(self):
        return self.cars_queue

    def get_next_state_cars_queue(self):
        return self.next_queue

    def get_max_length(self):
        return self.max_length

    # SETS

    def set_current_speed(self, cur_speed):
        self.cur_speed = cur_speed

    def set_cars_queue(self, cars_queue):
        self.cars_queue = cars_queue

    """
    functions to update to the next state
    """

    def add_cars(self, cars):
        # Tries to add the cars to the next queue
        # we need to address what to do to the cars that can't be added
        #self.next_queue = copy.deepcopy(self.cars_queue)
        for i in range(len(cars)):
            if len(self.next_queue) == self.max_length:
                print("********************")
                print("THE QUEUE IS FULL")
                print("********************")
                return
            self.next_queue.append(cars.pop(0))

    def remove_cars(self, num_cars):
        # Removes the cars from the queue if they can move to next edge
        cars_list = copy.deepcopy(self.cars_queue[:num_cars - 1])
        self.next_queue = self.cars_queue[num_cars:]

    """
    MAYBE THIS FUNCTION SHOULD BE IN ANOTHER CLASS
    CURRENTLY IN Road_Network
    def try_move_car(self, car, next_edge):
        
        :param car: a car to move to the next edge
        :return: boolean: true if the car was moved to the next edge, false otherwise
        
        if next_:
            return False
        self.next_queue.append(car)
        return True
    """

    def update(self):
        self.cars_queue = self.next_queue
        self.next_queue = copy.deepcopy(self.cars_queue)
        # NOW WE NEED TO UPDATE THE SPEED ACCORDING TO THE QUEUE
        # self.set_cur_speed()

    def set_cur_speed(self):
        # calculate the speed according to the queue and LWR model
        self.cur_speed = self.max_speed * (1 - (len(self.cars_queue) / self.max_length))

    def __str__(self):
        return "road_id: " + str(self.id) + "\n" + "start node: " + str(self.start_node) + "\n" + "end node: " + str(
            self.end_node) + "\n" + "edge_index: " + str(self.edge_index) + "\n" + "max_speed: " \
               + str(self.max_speed) + "\n" + "cur_speed: " + str(self.cur_speed) + \
               "\n" + "cars_queue: " + str(self.cars_queue) + "\n" + "next_queue: " + str(self.next_queue) + "\n" + \
               "max_length: " + str(self.max_length) + "\n"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node
