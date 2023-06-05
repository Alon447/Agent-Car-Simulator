"""
This class is implementing usage of q learning algorithm for route planning.
It will be used in the car class.
It will utilize the q table that will be created in the simulation manager.
Each car (agent) will have its own q table, derived from the simulation manager's q table.
In the future, the q-tables could be stored in a database, and adjustments might be neede.
"""
from new_master.Route import Route


class Q_Learning_Route(Route):
    def get_next_road(self, source_road, destination_node, time):
        # Implement Q-learning route logic here
        # Return a new edge based on the Q-learning algorithm
        pass