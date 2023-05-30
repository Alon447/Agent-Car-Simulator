import Road_Network
import Route


class Shortest_path_route(Route):

    def get_next_road(self, source_node, destination_node, time):
        # TODO: update according to distance matrix implementation
        return Road_Network.get_distance_matrix().get_road(source_node, destination_node)
