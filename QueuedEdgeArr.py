import QueuedEdge as QE
import osmnx as ox
import Cars

# Class that contains all the edges of the graph
CAR_LENGTH = 5
class QueuedEdgeArr:
    def __init__(self, G):
        self.queued_edges = []  # initialize an empty list to hold the QueuedEdge objects

        for edge in G.edges:

            len=G.edges[edge]['length']
            # if the road is shorter than the length of a car, we mark it by max_length=-1
            if len<5:
                len=-1
            else:
                len=int(len/CAR_LENGTH)

            queued_edge= QE.QueuedEdge(edge, G.edges[edge]['maxspeed'], G.edges[edge]['maxspeed'], [], [], len)
            self.queued_edges.append(queued_edge)
        #print(self.queued_edges)

    def get_edge(self, edge):
        # Returns the QueuedEdge object with the given edge
        for queued_edge in self.queued_edges:
            if queued_edge.get_edge_graph_index() == edge:
                return queued_edge
        return None

    def get_edge_index(self, edge):
        for i, queued_edge in enumerate(self.queued_edges):
            if queued_edge.get_edge_graph_index() == edge:
                return i
        return None


    def get_cars_next_edge(self, car):
        # Returns the next edge that the car will move to
        return self.get_edge(car.get_next_edge())

    def try_move_car(self, car):
        # Tries to move the car to the next edge
        # Returns True if the car can move, False otherwise
        next_edge = self.get_cars_next_edge(car)
        if next_edge is None:
            print("NEXT EDGE IS NONE")
            return False
        if next_edge.get_num_cars() == next_edge.get_max_length():
            print("next edge is full")
            return False
        return True

    def add_car(self, car):
        self.queued_edges[0].add_cars([car])
        self.queued_edges[0].update()

    def remove_car(self, edge):
        # Tries to remove the first car from the edge it is currently on
        # Returns True if the car was removed, False otherwise
        car = self.queued_edges[edge].get_cars_queue().poll(0)
        if self.try_move_car(car):
            car = self.queued_edges[edge].get_cars_queue().pop(0)
            self.get_cars_next_edge(car).add_cars([car])
            return True
        else:
            return False

    def update(self):
        # Updates the QueuedEdgeArr to the next state
        num_of_cars_to_move = 1
        for queued_edge in self.queued_edges:
            for i in range (num_of_cars_to_move):
                if not self.remove_car(queued_edge.get_edge_graph_index()):
                    break


        for queued_edge in self.queued_edges:
            queued_edge.update() # queued_edge.update() NOT FULLY WRITTEN YET

    def __str__(self):
        return str(self.queued_edges[0])
    def __repr__(self):
        return self.__str__()






g2 = ox.load_graphml('./data/graphTLVtime2.graphml')

q=QueuedEdgeArr(g2)
for i in range(10):
    c=Cars.Cars(i)
    q.add_car(c)
    print(q)


