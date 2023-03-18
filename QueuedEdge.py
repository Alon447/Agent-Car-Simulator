import itertools
import copy
class QueuedEdge:

    def __init__(self, edge_graph_index, max_speed, cur_speed, reversed, cars_queue, next_queue, max_length):
        self.edge_graph_index = edge_graph_index
        self.max_speed = max_speed
        self.cur_speed = max_speed
        self.reversed = reversed
        self.cars_queue = cars_queue #actually a list that will function similarly to a qeueu
        self.next_queue = cars_queue
        self.max_length = max_length # we need to define a mex length for the queue

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

    def set_cur_speed(self, cur_speed):
        self.cur_speed = cur_speed

    def set_cars_queue(self, cars_queue):
        self.cars_queue = cars_queue

    """
    functions to update to the next state
    """
    def add_cars(self, cars):
        self.next_queue = copy.deepcopy(self.cars_queue)
        for i in range(len(cars)):
            if (len(self.next_queue) == self.max_length):
                return
            self.next_queue.append(cars.pop(0))

    def remove_cars(self, num_cars):
        self.next_queue = self.cars_queue[num_cars:]

    def update(self):
        self.cars_queue = self.next_queue
        self.next_queue = copy.deepcopy(self.cars_queue)
        # NOW WE NEED TO UPDATE THE SPEED ACCORDING TO THE QUEUE
        self.set_cur_speed()

    def set_cur_speed(self):
        self.cur_speed = self.max_speed*(1-(len(self.cars_queue)/self.max_length))

    def __str__(self):
        return "edge_graph_index: " + str(self.edge_graph_index) + "\n" + "max_speed: " \
            + str(self.max_speed) + "\n" + "cur_speed: " + str(self.cur_speed) + "\n" + "reversed: " \
            + str(self.reversed) + "\n" + "cars_queue: " + str(self.cars_queue)
