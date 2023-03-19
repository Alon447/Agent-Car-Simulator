import itertools
import copy
import Cars


class QueuedEdge:

    def __init__(self, edge_graph_index, max_speed, cur_speed,  cars_queue, next_queue, max_length):
        self.edge_graph_index = edge_graph_index
        self.max_speed = max_speed
        self.cur_speed = max_speed
        self.cars_queue = cars_queue  # actually a list that will function similarly to a qeueu
        self.next_queue = cars_queue
        self.max_length = max_length  # we need to define a mex length for the queue

    # GETS
    def get_edge_graph_index(self):
        return self.edge_graph_index

    def get_max_speed(self):
        return self.max_speed

    def get_cur_speed(self):
        return self.cur_speed

    def get_num_cars(self):
        return len(self.cars_queue)

    def is_reversed(self):
        return self.reversed

    def get_cars_queue(self):
        return self.cars_queue

    def get_max_length(self):
        return self.max_length
    # SETS
    def set_cur_speed(self, cur_speed):
        self.cur_speed = cur_speed

    def set_cars_queue(self, cars_queue):
        self.cars_queue = cars_queue

    """
    functions to update to the next state
    """

    def add_cars(self, cars):
        # Tries to add the cars to the next queue
        # we need to address what to do to the cars that can't be added
        self.next_queue = copy.deepcopy(self.cars_queue)
        for i in range(len(cars)):
            if (len(self.next_queue) == self.max_length):
                print("The queue is full")
                return
            self.next_queue.append(cars.pop(0))

    def remove_cars(self, num_cars):
        # Removes the cars from the queue if they can move to next edge
        cars_list = copy.deepcopy(self.cars_queue[:num_cars - 1])
        for i, car in enumerate(cars_list):
            if not self.try_move_car(car):
                break
        self.next_queue = self.cars_queue[i:]

    def try_move_car(self, car, next_edge):
        """
        MAYBE THIS FUNCTION SHOULD BE IN ANOTHER CLASS
        :param car: a car to move to the next edge
        :return: boolean: true if the car was moved to the next edge, false otherwise
        """
        if next_:
            return False
        self.next_queue.append(car)
        return True

    def update(self):
        self.cars_queue = self.next_queue
        self.next_queue = copy.deepcopy(self.cars_queue)
        # NOW WE NEED TO UPDATE THE SPEED ACCORDING TO THE QUEUE
        #self.set_cur_speed()

    def set_cur_speed(self):
        # calculate the speed according to the queue and LWR model
        self.cur_speed = self.max_speed * (1 - (len(self.cars_queue) / self.max_length))

    def __str__(self):
        return "edge_graph_index: " + str(self.edge_graph_index) + "\n" + "max_speed: " \
               + str(self.max_speed) + "\n" + "cur_speed: " + str(self.cur_speed) +\
               "\n" + "cars_queue: " + str(self.cars_queue) + "\n" + "next_queue: " + str(self.next_queue) + "\n" +\
                "max_length: " + str(self.max_length) + "\n"

    def __repr__(self):
        return self.__str__()