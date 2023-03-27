import Road as QE
import osmnx as ox
import Cars

# Class that contains all the edges of the graph
CAR_LENGTH = 5


class Road_Network:

    def __init__(self, G):
        self.queued_edges = []  # initialize an empty list to hold the Road objects
        for i, edge in enumerate(G.edges):
            length = G.edges[edge]['length']
            # if the road is shorter than the length of a car, we mark it by max_length=-1
            if length < 5:
                length = -1
            else:
                length = int(length / CAR_LENGTH)
            queued_edge = QE.Road(G.edges[edge]['osmid'],edge[0],edge[1], edge, G.edges[edge]['maxspeed'], [], length)
            self.queued_edges.append(queued_edge)

    def get_edge(self, edge):
        # param: edge is a tuple of the form (u, v, key)
        # Return: the Road object with the given edge
        for queued_edge in self.queued_edges:
            if queued_edge.get_id() == edge:
                return queued_edge
        return None

    def get_cars_next_edge(self, car):
        # param: car is a Car object
        # return: Road object that is the next edge of the car
        return car.get_next_edge()

    def getEdgeFromIndex(self, index):
        # index is a tuple of the form (u, v, key)
        for edge in self.queued_edges:
            if edge == index:
                return edge
        return None

    def try_move_car(self, car):
        """
        Tries to move the car to the next edge
        param: car is a Car object
        Returns True if the car can move, False otherwise
        """
        next_edge = self.getEdgeFromIndex(car.get_next_edge())
        if next_edge is None:
            print("NEXT EDGE IS NONE")
            return False
        if next_edge.get_num_cars() == next_edge.get_max_length():
            print("next edge is full")
            return False
        return True

    def add_car(self, car):
        # Adds a car to the Road_Network
        # param: car is a Car object

        self.queued_edges[0].add_cars([car])
        self.queued_edges[0].update()

    def move_car(self, edge):
        # Tries to remove the first car from the edge it is currently on
        # param: edge that we want to remove the car from
        # Returns True if the car was removed, False otherwise
        if edge.get_num_cars() == 0:
            return False
        car = edge.get_cars_queue()[0]
        queue = self.getEdgeFromIndex(edge)
        if queue is None:
            return False
        if self.try_move_car(car):
            car = queue.get_cars_queue().pop(0)
            self.get_cars_next_edge(car).add_cars([car])
            return True
        else:
            return False

    def update(self, num_of_cars_to_move):
        # Updates the Road_Network to the next state
        # param: num_of_cars_to_move is the number of cars that we want to move from each edge

        num_of_cars_to_move = 1
        for queued_edge in self.queued_edges:
            for num in range(num_of_cars_to_move):
                if not self.move_car(queued_edge):
                    break
                print("Moved car")

        for queued_edge in self.queued_edges:
            queued_edge.update()  # queued_edge.update() NOT FULLY WRITTEN YET

    def __str__(self):
        st = ""
        for edge in self.queued_edges:
            if edge.get_num_cars() != 0:
                st += str(edge) + "\n"
        return st

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.queued_edges == other.queued_edges


g2 = ox.load_graphml('./data/graphTLVtime2.graphml')

q = Road_Network(g2)

c = Cars.Cars(1,
              [340368898, 2469720080, 290614029, 340318789, 2469720099, 340318978, 340309691, 336081282, 336081749,
               139708])
print(c.get_next_node())
print(c.get_next_edge())
"""
q.add_car(c)
print("finished P1")
print(q)

q.update(1)
print(q)

print("finished P2")
"""