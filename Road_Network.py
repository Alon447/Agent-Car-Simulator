import time

import Road as QE
import osmnx as ox
import Cars
import nodes

# Class that contains all the edges of the graph
CAR_LENGTH = 5


class Road_Network:
    # this class suppose to hold all the edges of the graph
    def __init__(self, G):
        self.queued_edges = []  # initialize an empty list to hold the Road objects
        self.initialize(G)

    def initialize(self, G):
        # Initializes the Road_Network
        # mainly for __init__ to look cleaner
        for i, edge in enumerate(G.edges):
            length = G.edges[edge]['length']
            # if the road is shorter than the length of a car, we mark it by max_length=-1
            if length < 5:
                length = -1
            else:
                length = int(length / CAR_LENGTH)
            queued_edge = QE.Road(G.edges[edge]['edge_id'], edge[0], edge[1], edge, G.edges[edge]['maxspeed'], [],
                                  length)
            self.queued_edges.append(queued_edge)

    def get_edge(self, edge_id):
        """
        return the Road object that corresponds to the edge

        Parameters
        ----------
        edge: the edge to get the Road object of
        """
        return self.queued_edges[edge_id]

    def start_car_ride(self,car):
        starting_road_id = car.get_first_edge()
        self.queued_edges[starting_road_id].add_cars([car])


    def add_car_to_road(self, car, road_id):
        """
        Adds a car to the Road_Network

        Parameters
        ----------
        car: a car object to move
        road_id: the id of the road to add the car to
        """
        self.queued_edges[road_id].add_cars([car])
        car.move_next()

    def get_cars_next_edge(self, car):
        # param: car is a Car object
        # return: Road object that is the next edge of the car
        # car.get_next_edge() is the id of the road so thats why we need to get the road from self.queued_edges
        if car.get_next_edge() is None:
            return None
        return self.queued_edges[car.get_next_edge()]


    def move_car(self, current_road):
        """
        # Tries to remove the first car from the edge it is currently on
        Parameters
        ----------
        current_road: the road to remove the car from

        Returns
        ----------
        True if the car was removed, False otherwise
        """
        if current_road.get_num_cars() == 0:
            return False

        car = current_road.get_cars_queue()[0]  # get the first car in the queue
        if self.get_cars_next_edge(car) is None:
            print("NEXT EDGE IS NONE")
            current_road.get_next_state_cars_queue().pop(0)
            return True

        next_road = self.get_cars_next_edge(car)  # gets the Road object of the next edge


        if next_road is None:
            print("NEXT EDGE IS NONE")
            return False
        if next_road.get_num_cars() == next_road.get_max_length():
            print("next edge is full")
            return False

        car = current_road.get_next_state_cars_queue().pop(0)
        self.add_car_to_road(car, car.get_next_edge())
        return True

    def update(self, num_of_cars_to_move):
        # Updates the Road_Network to the next state
        # param: num_of_cars_to_move is the number of cars that we want to move from each edge

        num_of_cars_to_move = 1
        for road in self.queued_edges:  # for each road
            for num in range(num_of_cars_to_move):  # move the required number of cars
                if not self.move_car(road):
                    break
                print(f"Moved car")

        for queued_edge in self.queued_edges:
            queued_edge.update()  # queued_edge.update() NOT FULLY WRITTEN YET

    def end_simulation(self):
        for road in self.queued_edges:
            if road.get_num_cars() != 0:
                return False
        print("No more cars in the network, Simulation ended")
        return True

    def __str__(self):
        st = ""
        for road in self.queued_edges:
            if road.get_num_cars() != 0:
                st += str(road) + "\n"
        return st

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.queued_edges == other.queued_edges


g2 = ox.load_graphml('./data/graphTLVFix.graphml')

q = Road_Network(g2)

c1 = Cars.Cars(1, 1, 56)
print(c1.get_nodes_route())
c2 = Cars.Cars(2, 56, 43)
print(c2.get_nodes_route())

q.start_car_ride(c1)
q.start_car_ride(c2)
while True:

    print("*********************************************************")

    q.update(1)
    print(q)
    time.sleep(1)
    if q.end_simulation():
        break

"""
q.add_car(c)
print("finished P1")
print(q)


print(q)

print("finished P2")
"""
